# IA Security Gateway - Professional Security API Routes
# CORRECTED - Routes match dashboard.js expectations
# Complete API for IP control, file analysis, and network tracking

from fastapi import APIRouter, File, UploadFile, Query, HTTPException, Request
from fastapi.responses import JSONResponse
from typing import List, Optional
from datetime import datetime
import base64

# Import security modules
from app.security.ip_control import ip_controller, IPAction
from app.security.file_analyzer import file_analyzer
from app.security.network_tracking import network_tracker, DeviceStatus, ViolationType

router = APIRouter(prefix="/api", tags=["security"])

# ============================================================
# IP CONTROL ENDPOINTS
# ============================================================

@router.get("/security/ip/rules")
async def get_ip_rules():
    """Get all IP whitelist and blacklist rules"""
    try:
        rules = ip_controller.get_rules()
        return {
            "timestamp": datetime.now().isoformat(),
            "whitelist": rules.get("whitelist", {}),
            "blacklist": rules.get("blacklist", {}),
            "stats": ip_controller.get_stats()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/security/ip/verify")
async def verify_ip_access(ip: str = Query(..., description="IP address to verify")):
    """Check if an IP is allowed to access IA services

    Query parameters:
    - ip: IP address to check
    """
    try:
        is_allowed, message = ip_controller.check_access(ip)
        rules = ip_controller.get_rules()

        # Determine rule type
        rule_type = None
        description = None
        if ip in rules.get("whitelist", {}):
            rule_type = "WHITELIST"
            description = rules["whitelist"][ip]
        elif ip in rules.get("blacklist", {}):
            rule_type = "BLACKLIST"
            description = rules["blacklist"][ip]

        return {
            "ip_address": ip,
            "allowed": is_allowed,
            "status": "ALLOWED" if is_allowed else "BLOCKED",
            "message": message,
            "rule_type": rule_type,
            "description": description,
            "risk_level": "HIGH" if not is_allowed else "LOW",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/security/ip/whitelist")
async def add_ip_whitelist(
    ip: str = Query(..., description="IP address to whitelist"),
    description: str = Query("Added via Dashboard", description="Reason for whitelisting"),
    added_by: str = Query("dashboard", description="User adding the rule")
):
    """Add IP to whitelist (allow access)"""
    try:
        success, message = ip_controller.add_whitelist(ip, description, added_by)
        return {
            "success": success,
            "message": message,
            "action": "whitelist_added",
            "ip": ip,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/security/ip/blacklist")
async def add_ip_blacklist(
    ip: str = Query(..., description="IP address to block"),
    reason: str = Query("SECURITY_VIOLATION", description="Reason for blocking"),
    description: str = Query("Added via Dashboard", description="Additional description"),
    added_by: str = Query("dashboard", description="User adding the rule")
):
    """Add IP to blacklist (block access completely)"""
    try:
        success, message = ip_controller.add_blacklist(ip, description, added_by, reason)
        return {
            "success": success,
            "message": message,
            "action": "blacklist_added",
            "ip_address": ip,
            "reason": reason,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/security/ip/rules/{ip_address}")
async def remove_ip_rule(ip_address: str):
    """Remove an IP rule (whitelist or blacklist)"""
    try:
        success, message = ip_controller.remove_rule(ip_address)
        return {
            "success": success,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# FILE ANALYSIS ENDPOINTS
# ============================================================

@router.post("/security/file/analyze")
async def analyze_file(
    file: UploadFile = File(...),
    client_ip: str = Query("unknown", description="Client IP address")
):
    """Analyze a file for security threats before sending to IA

    Expects multipart form data with:
    - file: The file to analyze
    - client_ip: (optional) Client IP address
    """
    try:
        # Read file content
        content = await file.read()

        # Attempt to decode as text (for document analysis)
        try:
            text_content = content.decode('utf-8')
        except:
            text_content = base64.b64encode(content).decode('utf-8')

        # Perform analysis
        result = file_analyzer.analyze_file(
            filename=file.filename or "unknown",
            content=text_content[:10000],  # Limit to first 10KB for analysis
            file_size=len(content),
            client_ip=client_ip
        )

        return {
            "filename": result.filename,
            "file_type": result.file_type,
            "mime_type": result.mime_type,
            "file_size_bytes": result.file_size_bytes,
            "risk_level": result.risk_level.value,
            "is_allowed": result.is_allowed,
            "reason": result.reason,
            "patterns_found": result.detected_patterns,
            "sensitive_content": {
                "has_credentials": result.has_credentials,
                "has_personal_data": result.has_personal_data,
                "has_financial_data": result.has_financial_data,
                "has_trade_secrets": result.has_trade_secrets
            },
            "timestamp": result.timestamp
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"File analysis error: {str(e)}")


@router.get("/security/file/analysis-summary")
async def get_file_analysis_summary():
    """Get summary of file analysis activity"""
    try:
        summary = file_analyzer.get_analysis_summary()
        return {
            "total_analyzed": summary.get("total_analyzed", 0),
            "safe": summary.get("safe", 0),
            "at_risk": summary.get("at_risk", 0),
            "top_patterns": summary.get("top_patterns", {}),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# NETWORK TRACKING ENDPOINTS
# ============================================================

@router.post("/network/track-device")
async def track_device_request(
    ip: str = Query(...),
    hostname: str = Query("unknown"),
    user_agent: str = Query("unknown"),
    ai_model: str = Query("unknown")
):
    """Track a device request on the network

    Query parameters:
    - ip: Client IP (required)
    - hostname: Device hostname
    - user_agent: Browser user agent
    - ai_model: AI model accessed
    """
    try:
        device = network_tracker.track_request(
            client_ip=ip,
            hostname=hostname,
            user_agent=user_agent,
            model_accessed=ai_model,
            request_size=0
        )

        return {
            "success": True,
            "ip": device.ip_address,
            "total_requests": device.total_requests,
            "status": device.status.value,
            "risk_level": getattr(device, 'risk_level', 'UNKNOWN'),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/network/record-block")
async def record_blocked_request(client_ip: str = Query(...)):
    """Record a blocked request from a device"""
    try:
        device = network_tracker.record_block(client_ip)

        if device:
            total_reqs = device.total_requests or 1
            block_rate = (device.total_blocks / total_reqs * 100) if total_reqs > 0 else 0

            return {
                "ip_address": device.ip_address,
                "total_blocks": device.total_blocks,
                "block_rate_percent": round(block_rate, 2),
                "status": device.status.value,
                "risk_level": getattr(device, 'risk_level', 'UNKNOWN'),
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=404, detail="Device not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/network/device-profile")
async def get_device_profile(ip: str = Query(..., description="Device IP address")):
    """Get detailed profile of a device

    Query parameters:
    - ip: Device IP address (required)
    """
    try:
        profile = network_tracker.get_device_profile(ip)

        if not profile:
            raise HTTPException(status_code=404, detail="Device not tracked yet")

        return {
            "ip": ip,
            "hostname": profile.get("hostname", "Unknown"),
            "user_agent": profile.get("user_agent", "N/A"),
            "ai_model": profile.get("model_accessed", "N/A"),
            "risk_level": profile.get("risk_level", "UNKNOWN"),
            "total_requests": profile.get("total_requests", 0),
            "blocked_requests": profile.get("total_blocks", 0),
            "first_seen": profile.get("first_seen", "N/A"),
            "last_activity": profile.get("last_seen", "N/A"),
            "status": profile.get("status", "unknown"),
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/network/summary")
async def get_network_summary():
    """Get summary of network activity and security"""
    try:
        summary = network_tracker.get_network_summary()
        return {
            "connected_devices": summary.get("total_devices", 0),
            "whitelist_ips": summary.get("whitelist_count", 0),
            "blacklist_ips": summary.get("blacklist_count", 0),
            "average_risk": summary.get("average_risk_level", "UNKNOWN"),
            "total_violations": summary.get("total_violations", 0),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/network/devices")
async def get_all_devices(
    status: Optional[str] = Query(None, description="Filter by status"),
    min_risk_score: float = Query(0, description="Minimum risk score filter")
):
    """Get list of all tracked devices

    Query parameters:
    - status: (optional) Filter by status (trusted, monitored, suspected, blocked)
    - min_risk_score: (optional) Minimum risk score
    """
    try:
        devices = []

        for ip, device in network_tracker.devices.items():
            # Apply filters
            if status and device.status.value != status:
                continue

            risk_val = getattr(device, 'risk_score', 0)
            if risk_val < min_risk_score:
                continue

            devices.append({
                "ip": device.ip_address,
                "hostname": device.hostname,
                "total_requests": device.total_requests,
                "blocked_requests": device.total_blocks,
                "status": device.status.value,
                "risk_level": getattr(device, 'risk_level', 'UNKNOWN'),
                "first_seen": device.first_seen,
                "last_activity": device.last_seen
            })

        return {
            "devices": devices,
            "total": len(devices),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# VIOLATIONS ENDPOINTS
# ============================================================

@router.get("/security/violations")
async def get_security_violations(
    limit: int = Query(20, description="Maximum violations to return"),
    resolved: Optional[bool] = Query(None, description="Filter by resolved status")
):
    """Get recent security violations

    Query parameters:
    - limit: (optional, default 20) Maximum violations to return
    - resolved: (optional) Filter by resolved status
    """
    try:
        violations = []

        for v in network_tracker.violations[-limit:]:
            if resolved is not None and v.resolved != resolved:
                continue

            violations.append({
                "ip": v.device_ip,
                "type": v.violation_type.value,
                "description": v.description,
                "timestamp": v.timestamp,
                "resolved": v.resolved
            })

        return {
            "violations": violations,
            "total": len(violations),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/security/violations")
async def report_violation(
    ip: str = Query(...),
    type: str = Query(...),
    description: str = Query("Reported via Dashboard")
):
    """Manually report a security violation

    Query parameters:
    - ip: Device IP (required)
    - type: Violation type (required)
    - description: Detailed description
    """
    try:
        try:
            vtype = ViolationType[type.upper()]
        except KeyError:
            raise HTTPException(status_code=400, detail=f"Unknown violation type: {type}")

        network_tracker.record_violation(
            device_ip=ip,
            violation_type=vtype,
            severity="medium",
            description=description,
            evidence={"manual_report": True}
        )
        return {
            "success": True,
            "message": f"Violation reported for {ip}",
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
