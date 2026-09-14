"""
Request/Response Data Models
Pydantic schemas for API validation and documentation
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, List, Any
from datetime import datetime


class GenerateRequest(BaseModel):
    """Request model for local LLM generation"""
    prompt: str = Field(..., min_length=1, max_length=10000, description="Input prompt for LLM")
    model: Optional[str] = Field(None, description="Specific model to use (if not set, uses default)")
    temperature: Optional[float] = Field(0.7, ge=0.0, le=2.0, description="Temperature for generation")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "prompt": "Explain the importance of data privacy",
                "temperature": 0.7
            }
        }
    )


class GenerateResponse(BaseModel):
    """Response model for LLM generation"""
    success: bool
    response: str
    llm_model_used: str
    generation_time_ms: float
    data_sensitivity: str
    timestamp: datetime

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "response": "Data privacy is crucial because...",
                "llm_model_used": "llama2",
                "generation_time_ms": 1234.56,
                "data_sensitivity": "public",
                "timestamp": "2024-09-13T10:30:00"
            }
        }
    )


class ChatMessage(BaseModel):
    """Chat message model"""
    role: str = Field(..., description="Role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")


class ChatRequest(BaseModel):
    """Request model for chat interaction"""
    messages: List[ChatMessage] = Field(..., description="List of chat messages")
    session_id: Optional[str] = Field(None, description="Session identifier for context tracking")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "messages": [
                    {"role": "user", "content": "What is data privacy?"}
                ],
                "session_id": "session_123"
            }
        }
    )


class ChatResponse(BaseModel):
    """Response model for chat interaction"""
    success: bool
    response: str
    session_id: str
    messages_processed: int
    timestamp: datetime

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "response": "Data privacy refers to...",
                "session_id": "session_123",
                "messages_processed": 1,
                "timestamp": "2024-09-13T10:30:00"
            }
        }
    )


class ComplianceReport(BaseModel):
    """Compliance status report"""
    report_date: datetime
    gdpr_enabled: bool
    hipaa_enabled: bool
    pci_dss_enabled: bool
    data_retention_days: int
    log_sensitive_data: bool
    audit_entries: int
    status: str
    allowed_requests: int
    blocked_requests: int
    active_clients: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "report_date": "2024-09-13T10:30:00",
                "gdpr_enabled": True,
                "hipaa_enabled": True,
                "pci_dss_enabled": True,
                "data_retention_days": 90,
                "log_sensitive_data": False,
                "audit_entries": 1250,
                "status": "compliant",
                "allowed_requests": 5000,
                "blocked_requests": 12,
                "active_clients": 42
            }
        }
    )


class HealthStatus(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Operational status")
    ollama_available: bool
    version: str
    timestamp: datetime
    uptime_seconds: float

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "operational",
                "ollama_available": True,
                "version": "1.0.0",
                "timestamp": "2024-09-13T10:30:00",
                "uptime_seconds": 3600.5
            }
        }
    )


class ErrorResponse(BaseModel):
    """Error response model"""
    success: bool = False
    error_type: str
    detail: str
    status_code: int
    timestamp: datetime

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": False,
                "error_type": "ValidationError",
                "detail": "Invalid input parameters",
                "status_code": 422,
                "timestamp": "2024-09-13T10:30:00"
            }
        }
    )


class TrafficStats(BaseModel):
    """Traffic control statistics"""
    allowed_requests: int
    blocked_requests: int
    active_clients: int
    block_rate_percent: float
    timestamp: datetime

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "allowed_requests": 5000,
                "blocked_requests": 12,
                "active_clients": 42,
                "block_rate_percent": 0.24,
                "timestamp": "2024-09-13T10:30:00"
            }
        }
    )
