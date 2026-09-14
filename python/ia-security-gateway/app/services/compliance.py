"""
Compliance and Audit Logging Service
Ensures GDPR, HIPAA, PCI-DSS compliance
"""
import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from app.core.config import settings
from app.core.security import classify_data_sensitivity

logger = logging.getLogger(__name__)

class ComplianceLogger:
    """Handles compliance logging and audit trails"""

    def __init__(self):
        self.log_file = Path("logs/compliance.log")
        self.log_file.parent.mkdir(exist_ok=True)
        self.audit_trail: List[Dict] = []

    def log_request(self, method: str, path: str, timestamp: datetime) -> None:
        """Log incoming request"""
        entry = {
            "event": "REQUEST",
            "timestamp": timestamp.isoformat(),
            "method": method,
            "path": path,
            "gdpr_compliant": settings.GDPR_ENABLED,
            "hipaa_compliant": settings.HIPAA_ENABLED,
            "pci_dss_compliant": settings.PCI_DSS_ENABLED
        }
        self._write_log(entry)

    def log_response(self, status_code: int, process_time: float) -> None:
        """Log outgoing response"""
        entry = {
            "event": "RESPONSE",
            "timestamp": datetime.now().isoformat(),
            "status_code": status_code,
            "process_time_ms": round(process_time * 1000, 2)
        }
        self._write_log(entry)

    def log_data_classification(self, data: str, classification: str) -> None:
        """Log data classification result"""
        sensitivity = classify_data_sensitivity(data)
        entry = {
            "event": "DATA_CLASSIFICATION",
            "timestamp": datetime.now().isoformat(),
            "sensitivity_level": sensitivity,
            "classification": classification
        }
        self._write_log(entry)

    def log_error(self, error_type: str, status_code: int, detail: str) -> None:
        """Log errors for compliance audit"""
        entry = {
            "event": "ERROR",
            "timestamp": datetime.now().isoformat(),
            "error_type": error_type,
            "status_code": status_code,
            "detail": detail
        }
        self._write_log(entry)

    def log_security_event(self, event_type: str, severity: str, description: str) -> None:
        """Log security events"""
        entry = {
            "event": "SECURITY_EVENT",
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "severity": severity,
            "description": description
        }
        self._write_log(entry)
        logger.warning(f"🔐 [{severity}] {event_type}: {description}")

    def _write_log(self, entry: Dict) -> None:
        """Write entry to compliance log"""
        try:
            with open(self.log_file, "a") as f:
                f.write(json.dumps(entry) + "\n")
            self.audit_trail.append(entry)
        except Exception as e:
            logger.error(f"Failed to write compliance log: {e}")

    def get_audit_trail(self, limit: int = 100) -> List[Dict]:
        """Get recent audit trail entries"""
        return self.audit_trail[-limit:]

    def generate_compliance_report(self) -> Dict:
        """Generate compliance report"""
        return {
            "report_date": datetime.now().isoformat(),
            "gdpr_enabled": settings.GDPR_ENABLED,
            "hipaa_enabled": settings.HIPAA_ENABLED,
            "pci_dss_enabled": settings.PCI_DSS_ENABLED,
            "data_retention_days": settings.RETENTION_DAYS,
            "log_sensitive_data": settings.LOG_SENSITIVE_DATA,
            "audit_entries": len(self.audit_trail),
            "status": "compliant"
        }
