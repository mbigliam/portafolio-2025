# IA Security Gateway - File Analysis Module
# Analyze documents for sensitive data, credentials, and restricted file types

from typing import Dict, Tuple, List, Optional
from enum import Enum
import re
import base64
from dataclasses import dataclass
from datetime import datetime

class FileType(str, Enum):
    ALLOWED = "allowed"
    RESTRICTED = "restricted"
    UNKNOWN = "unknown"

class RiskLevel(str, Enum):
    SAFE = "safe"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class FileAnalysisResult:
    filename: str
    file_type: str
    mime_type: str
    file_category: FileType
    risk_level: RiskLevel
    file_size_bytes: int
    has_credentials: bool
    has_personal_data: bool
    has_financial_data: bool
    has_trade_secrets: bool
    detected_patterns: List[str]
    is_allowed: bool
    reason: str
    timestamp: str

class FileAnalyzer:
    """Analyze files for security threats before sending to IA"""

    # Restricted file types that cannot be shared with IA
    RESTRICTED_TYPES = {
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',  # .docx
        'application/msword',  # .doc
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',  # .xlsx
        'application/vnd.ms-excel',  # .xls
        'application/pdf',  # .pdf
        'application/x-rar-compressed',  # .rar
        'application/x-zip-compressed',  # .zip
        'application/x-7z-compressed',  # .7z
        'image/jpeg', 'image/png', 'image/gif',  # Images with potential metadata
        'application/x-msaccess',  # .mdb
        'application/x-mspublisher',  # .pub
    }

    # Patterns for sensitive data detection
    PATTERNS = {
        'passwords': [
            r'password\s*[=:]\s*[\'"]?([^\s\'"]+)[\'"]?',
            r'pwd\s*[=:]\s*[\'"]?([^\s\'"]+)[\'"]?',
            r'pass\s*[=:]\s*[\'"]?([^\s\'"]+)[\'"]?',
        ],
        'api_keys': [
            r'api[_-]?key\s*[=:]\s*[\'"]?([a-zA-Z0-9\-_]+)[\'"]?',
            r'apikey\s*[=:]\s*[\'"]?([a-zA-Z0-9\-_]+)[\'"]?',
            r'sk-[a-zA-Z0-9]{20,}',  # OpenAI style
            r'AKIA[0-9A-Z]{16}',  # AWS style
        ],
        'database_credentials': [
            r'(mysql|postgres|mongodb|oracle)://[^\s]+',
            r'connection[_-]?string\s*[=:]\s*[\'"]?([^\s\'"]+)[\'"]?',
        ],
        'credit_cards': [
            r'\b(?:\d{4}[-\s]?){3}\d{4}\b',  # Generic credit card
            r'\b4[0-9]{12}(?:[0-9]{3})?\b',  # Visa
        ],
        'ssn': [
            r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
            r'\b\d{3}\.\d{2}\.\d{4}\b',  # SSN with dots
        ],
        'emails_corporate': [
            r'([a-zA-Z0-9._%+-]+@[company-domain-here])',  # Corporate emails
        ],
        'personal_data': [
            r'\b(?:DOB|Date of Birth|Fecha Nacimiento)\s*[=:]\s*([^\s]+)',
            r'\b(?:DNI|Cédula|ID)\s*[=:]\s*([^\s]+)',
        ],
        'confidential_markers': [
            r'\b(CONFIDENTIAL|SECRETO|RESTRICTED|CLASSIFIED)\b',
            r'\b(TOP SECRET|ULTRA SECRETO)\b',
        ],
        'trade_secrets': [
            r'\b(algorithm|proprietary|patent pending|trade secret)\b',
            r'\b(confidential formula|secret recipe)\b',
        ],
    }

    def __init__(self):
        self.analysis_history: List[FileAnalysisResult] = []

    def analyze_filename(self, filename: str) -> Tuple[str, FileType]:
        """Analyze filename and extension"""
        filename_lower = filename.lower()

        # Get MIME type from extension
        mime_types = {
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.doc': 'application/msword',
            '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            '.xls': 'application/vnd.ms-excel',
            '.pdf': 'application/pdf',
            '.txt': 'text/plain',
            '.csv': 'text/csv',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.zip': 'application/x-zip-compressed',
            '.rar': 'application/x-rar-compressed',
            '.7z': 'application/x-7z-compressed',
        }

        mime_type = None
        for ext, mime in mime_types.items():
            if filename_lower.endswith(ext):
                mime_type = mime
                break

        if mime_type is None:
            mime_type = 'application/octet-stream'

        # Determine file category
        if mime_type in self.RESTRICTED_TYPES:
            file_type = FileType.RESTRICTED
        else:
            file_type = FileType.ALLOWED

        return mime_type, file_type

    def detect_sensitive_content(self, content: str) -> Tuple[RiskLevel, List[str], Dict[str, bool]]:
        """Detect sensitive patterns in file content"""
        detected = []
        data_flags = {
            'credentials': False,
            'personal_data': False,
            'financial_data': False,
            'trade_secrets': False,
        }

        # Search for patterns
        for category, patterns in self.PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    detected.append(category)
                    if category in ['passwords', 'api_keys', 'database_credentials']:
                        data_flags['credentials'] = True
                    elif category in ['ssn', 'emails_corporate', 'personal_data']:
                        data_flags['personal_data'] = True
                    elif category in ['credit_cards']:
                        data_flags['financial_data'] = True
                    elif category in ['trade_secrets', 'confidential_markers']:
                        data_flags['trade_secrets'] = True

        # Determine risk level
        if data_flags['credentials'] or data_flags['financial_data']:
            risk = RiskLevel.CRITICAL
        elif data_flags['trade_secrets']:
            risk = RiskLevel.HIGH
        elif data_flags['personal_data']:
            risk = RiskLevel.MEDIUM
        elif detected:
            risk = RiskLevel.LOW
        else:
            risk = RiskLevel.SAFE

        return risk, detected, data_flags

    def analyze_file(self, filename: str, content: str, file_size: int = 0,
                    client_ip: str = "unknown") -> FileAnalysisResult:
        """Comprehensive file analysis"""

        # Get MIME type and file category
        mime_type, file_category = self.analyze_filename(filename)

        # Extract file extension
        file_ext = filename.split('.')[-1] if '.' in filename else 'unknown'

        # Detect sensitive content
        risk_level, detected_patterns, data_flags = self.detect_sensitive_content(content)

        # Determine if file is allowed
        is_restricted = file_category == FileType.RESTRICTED
        is_sensitive = risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]

        is_allowed = not (is_restricted or is_sensitive)

        if not is_allowed:
            if is_restricted:
                reason = f"File type .{file_ext} is restricted (Word, Excel, PDF not allowed)"
            elif data_flags['credentials']:
                reason = "CRITICAL: Credentials/API keys detected - BLOCKED"
            elif data_flags['financial_data']:
                reason = "CRITICAL: Financial data detected - BLOCKED"
            elif data_flags['trade_secrets']:
                reason = "HIGH RISK: Trade secrets/confidential markers detected - BLOCKED"
            else:
                reason = f"MEDIUM RISK: Sensitive content detected - BLOCKED"
        else:
            reason = "File analysis passed - safe to send to IA"

        result = FileAnalysisResult(
            filename=filename,
            file_type=file_ext.upper(),
            mime_type=mime_type,
            file_category=file_category,
            risk_level=risk_level,
            file_size_bytes=file_size,
            has_credentials=data_flags['credentials'],
            has_personal_data=data_flags['personal_data'],
            has_financial_data=data_flags['financial_data'],
            has_trade_secrets=data_flags['trade_secrets'],
            detected_patterns=detected_patterns,
            is_allowed=is_allowed,
            reason=reason,
            timestamp=datetime.now().isoformat()
        )

        self.analysis_history.append(result)
        return result

    def get_analysis_summary(self) -> Dict:
        """Get summary of file analysis activity"""
        total = len(self.analysis_history)
        allowed = sum(1 for r in self.analysis_history if r.is_allowed)
        blocked = total - allowed

        risk_counts = {
            'safe': sum(1 for r in self.analysis_history if r.risk_level == RiskLevel.SAFE),
            'low': sum(1 for r in self.analysis_history if r.risk_level == RiskLevel.LOW),
            'medium': sum(1 for r in self.analysis_history if r.risk_level == RiskLevel.MEDIUM),
            'high': sum(1 for r in self.analysis_history if r.risk_level == RiskLevel.HIGH),
            'critical': sum(1 for r in self.analysis_history if r.risk_level == RiskLevel.CRITICAL),
        }

        return {
            'total_analyzed': total,
            'allowed': allowed,
            'blocked': blocked,
            'block_rate_percent': (blocked / total * 100) if total > 0 else 0,
            'risk_distribution': risk_counts,
        }

# Initialize global file analyzer
file_analyzer = FileAnalyzer()
