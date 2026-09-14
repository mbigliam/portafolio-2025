"""
API Routes - CORRECTED
Defines all endpoints for the IA Security Gateway
Routes match dashboard.js expectations
"""
from fastapi import APIRouter, HTTPException, Depends, Header, Request, Query, File, UploadFile
from datetime import datetime, timedelta
from typing import Optional
import logging
import base64

from app.models.schemas import (
    GenerateRequest, GenerateResponse,
    ChatRequest, ChatResponse,
    ComplianceReport, HealthStatus,
    ErrorResponse, TrafficStats
)
from app.core.config import settings
from app.core.security import verify_token, sanitize_input, classify_data_sensitivity
from app.services.ollama_service import ollama_service
from app.services.traffic_control import TrafficController
from app.services.compliance import ComplianceLogger

logger = logging.getLogger(__name__)

# Initialize services
traffic_controller = TrafficController()
compliance_logger = ComplianceLogger()

# Create router
router = APIRouter(prefix="/api", tags=["Gateway"])


def get_client_id(request: Request, authorization: Optional[str] = Header(None)) -> str:
    """Extract client ID from request or token"""
    if authorization and authorization.startswith("Bearer "):
        try:
            token = authorization.split(" ")[1]
            payload = verify_token(token)
            return payload.get("sub", request.client.host)
        except Exception:
            pass
    return request.client.host


# ============================================================
# AI GATEWAY ENDPOINTS (with /ai/ prefix to match dashboard)
# ============================================================

@router.get("/ai/status", response_model=HealthStatus, tags=["AI Gateway"])
async def get_status():
    """
    Get gateway operational status

    Returns:
    - Overall system status (online/offline/degraded)
    - Ollama availability
    - Version information
    """
    try:
        ollama_available = await ollama_service.health_check()

        return HealthStatus(
            status="online" if ollama_available else "offline",
            ollama_available=ollama_available,
            version="1.0.0",
            timestamp=datetime.now(),
            uptime_seconds=0
        )
    except Exception as e:
        logger.error(f"Status check error: {e}")
        return HealthStatus(
            status="offline",
            ollama_available=False,
            version="1.0.0",
            timestamp=datetime.now(),
            uptime_seconds=0
        )


@router.get("/ai/traffic-stats", response_model=TrafficStats, tags=["AI Gateway"])
async def get_traffic_stats():
    """
    Get traffic control statistics

    Returns:
    - Request counts (allowed/blocked)
    - Active clients
    - Block rate percentage
    """
    try:
        stats = traffic_controller.get_stats()
        total = stats.get("allowed_requests", 0) + stats.get("blocked_requests", 0)
        block_rate = (stats.get("blocked_requests", 0) / total * 100) if total > 0 else 0

        return TrafficStats(
            allowed_requests=stats.get("allowed_requests", 0),
            blocked_requests=stats.get("blocked_requests", 0),
            active_clients=stats.get("active_clients", 0),
            block_rate_percent=round(block_rate, 2),
            timestamp=datetime.now()
        )
    except Exception as e:
        logger.error(f"Traffic stats error: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve traffic stats")


@router.get("/ai/compliance", tags=["AI Gateway"])
async def get_compliance_report(
    client_id: str = Depends(get_client_id)
):
    """
    Get comprehensive compliance and audit report

    Returns:
    - GDPR/HIPAA/PCI-DSS compliance status
    - Audit trail statistics
    - Traffic control metrics
    - Data retention policy
    """
    try:
        compliance_data = compliance_logger.generate_compliance_report()
        traffic_stats = traffic_controller.get_stats()

        return {
            "report_date": datetime.now().isoformat(),
            "status": compliance_data.get("status", "UNKNOWN"),
            "violations": compliance_data.get("violations", 0),
            "last_check": datetime.now().isoformat(),
            "gdpr_enabled": compliance_data.get("gdpr_enabled", False),
            "hipaa_enabled": compliance_data.get("hipaa_enabled", False),
            "pci_dss_enabled": compliance_data.get("pci_dss_enabled", False),
            "data_retention_days": compliance_data.get("data_retention_days", 30),
            "log_sensitive_data": compliance_data.get("log_sensitive_data", False),
            "audit_entries": compliance_data.get("audit_entries", 0),
            "allowed_requests": traffic_stats.get("allowed_requests", 0),
            "blocked_requests": traffic_stats.get("blocked_requests", 0),
            "active_clients": traffic_stats.get("active_clients", 0)
        }
    except Exception as e:
        logger.error(f"Compliance report error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate compliance report")


@router.post("/ai/generate", tags=["AI Gateway"])
async def generate_text(
    prompt: str = Query(...),
    client_request: Request = None,
    client_id: str = Depends(get_client_id)
):
    """
    Generate text using local Ollama LLM

    Features:
    - Rate limiting per client
    - Data sensitivity detection
    - Compliance logging
    - No external API calls - all local
    """
    try:
        # Check rate limiting
        allowed, stats = traffic_controller.check_rate_limit(
            client_id,
            settings.RATE_LIMIT_REQUESTS,
            settings.RATE_LIMIT_WINDOW
        )

        if not allowed:
            compliance_logger.log_security_event(
                event_type="RATE_LIMIT_EXCEEDED",
                severity="MEDIUM",
                description=f"Client {client_id} exceeded rate limit"
            )
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded: {stats['current']}/{stats['limit']} requests"
            )

        # Sanitize input
        safe_prompt = sanitize_input(prompt)

        # Classify data sensitivity
        sensitivity = classify_data_sensitivity(prompt)

        # Log the request for compliance
        compliance_logger.log_data_classification(prompt, sensitivity)

        # Generate using local Ollama
        start_time = datetime.now()
        response = await ollama_service.generate_local(safe_prompt)
        generation_time = (datetime.now() - start_time).total_seconds() * 1000

        if response is None:
            compliance_logger.log_error(
                error_type="GENERATION_FAILED",
                status_code=503,
                detail="Local Ollama generation failed"
            )
            raise HTTPException(
                status_code=503,
                detail="Local LLM service temporarily unavailable"
            )

        # Log successful response
        compliance_logger.log_response(200, generation_time)

        return {
            "success": True,
            "generated_text": response,
            "llm_model_used": ollama_service.model,
            "generation_time_ms": round(generation_time, 2),
            "data_sensitivity": sensitivity,
            "timestamp": datetime.now().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Generation error: {e}")
        compliance_logger.log_error(
            error_type="GENERATION_ERROR",
            status_code=500,
            detail=str(e)
        )
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/ai/chat", tags=["AI Gateway"])
async def chat(
    message: str = Query(...),
    client_request: Request = None,
    client_id: str = Depends(get_client_id)
):
    """
    Chat interface with conversation support

    Features:
    - Message processing
    - Rate limiting
    - Compliance logging
    """
    try:
        # Check rate limiting
        allowed, stats = traffic_controller.check_rate_limit(
            client_id,
            settings.RATE_LIMIT_REQUESTS * 2,  # Higher limit for chat
            settings.RATE_LIMIT_WINDOW
        )

        if not allowed:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")

        # Sanitize input
        content = sanitize_input(message)

        # Classify combined sensitivity
        sensitivity = classify_data_sensitivity(content)
        compliance_logger.log_data_classification(content, sensitivity)

        # Generate response
        start_time = datetime.now()
        response = await ollama_service.generate_local(content)
        generation_time = (datetime.now() - start_time).total_seconds() * 1000

        if response is None:
            raise HTTPException(status_code=503, detail="LLM service unavailable")

        compliance_logger.log_response(200, generation_time)

        return {
            "success": True,
            "response": response,
            "timestamp": datetime.now().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat error: {e}")
        compliance_logger.log_error("CHAT_ERROR", 500, str(e))
        raise HTTPException(status_code=500, detail="Chat error")


# ============================================================
# LEGACY ENDPOINTS (redirect to /ai/ for backward compatibility)
# ============================================================

@router.get("/status", tags=["Deprecated"])
async def get_status_legacy():
    """Legacy endpoint - use /api/ai/status instead"""
    return await get_status()


@router.get("/traffic-stats", tags=["Deprecated"])
async def get_traffic_stats_legacy():
    """Legacy endpoint - use /api/ai/traffic-stats instead"""
    return await get_traffic_stats()


@router.get("/compliance", tags=["Deprecated"])
async def get_compliance_legacy(client_id: str = Depends(get_client_id)):
    """Legacy endpoint - use /api/ai/compliance instead"""
    return await get_compliance_report(client_id)
