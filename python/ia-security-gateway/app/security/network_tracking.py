# IA Security Gateway - Network Origin Tracking
# Track devices using IA services and detect security violations

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timedelta
import json
from pathlib import Path

class DeviceStatus(str, Enum):
    TRUSTED = "trusted"
    MONITORED = "monitored"
    SUSPECTED = "suspected"
    BLOCKED = "blocked"

class ViolationType(str, Enum):
    EXCESSIVE_REQUESTS = "excessive_requests"
    SUSPICIOUS_PATTERNS = "suspicious_patterns"
    MULTIPLE_FAILED_ATTEMPTS = "multiple_failed_attempts"
    POLICY_VIOLATION = "policy_violation"
    UNAUTHORIZED_FILE_ATTEMPT = "unauthorized_file_attempt"
    CREDENTIAL_EXPOSURE = "credential_exposure"

@dataclass
class DeviceProfile:
    """Profile of a device accessing IA services"""
    ip_address: str
    hostname: str
    first_seen: str
    last_seen: str
    total_requests: int
    total_blocks: int
    status: DeviceStatus
    risk_score: float  # 0-100
    violations: List[str]
    user_agents: List[str]
    ai_models_accessed: List[str]
    average_request_size_bytes: float

@dataclass
class SecurityViolation:
    """Record of a security violation"""
    device_ip: str
    violation_type: ViolationType
    severity: str  # low, medium, high, critical
    description: str
    timestamp: str
    evidence: Dict
    resolved: bool = False

class NetworkTracker:
    """Track network devices and detect security violations"""

    def __init__(self, devices_file: str = "data/network_devices.json"):
        self.devices_file = devices_file
        self.devices: Dict[str, DeviceProfile] = {}
        self.violations: List[SecurityViolation] = []

        # Thresholds
        self.RATE_LIMIT_THRESHOLD = 1000  # requests per hour
        self.FAILED_ATTEMPTS_THRESHOLD = 10
        self.RISK_SCORE_THRESHOLD = 70  # Auto-flag for review

        self.load_devices()

    def load_devices(self):
        """Load device profiles from storage"""
        try:
            if Path(self.devices_file).exists():
                with open(self.devices_file, 'r') as f:
                    data = json.load(f)
                    for ip, dev_dict in data.get('devices', {}).items():
                        dev_dict['status'] = DeviceStatus(dev_dict['status'])
                        self.devices[ip] = DeviceProfile(**dev_dict)
        except Exception as e:
            print(f"Error loading device profiles: {e}")

    def save_devices(self):
        """Save device profiles to storage"""
        try:
            Path(self.devices_file).parent.mkdir(parents=True, exist_ok=True)
            data = {
                'devices': {ip: asdict(dev) for ip, dev in self.devices.items()}
            }
            with open(self.devices_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving device profiles: {e}")

    def track_request(self, client_ip: str, hostname: str = "unknown",
                     user_agent: str = "unknown", model_accessed: str = "unknown",
                     request_size: int = 0) -> DeviceProfile:
        """Track a request from a device"""

        now = datetime.now().isoformat()

        if client_ip not in self.devices:
            # New device
            self.devices[client_ip] = DeviceProfile(
                ip_address=client_ip,
                hostname=hostname,
                first_seen=now,
                last_seen=now,
                total_requests=1,
                total_blocks=0,
                status=DeviceStatus.MONITORED,
                risk_score=10.0,  # Start with low risk
                violations=[],
                user_agents=[user_agent] if user_agent else [],
                ai_models_accessed=[model_accessed] if model_accessed else [],
                average_request_size_bytes=request_size
            )
        else:
            # Update existing device
            device = self.devices[client_ip]
            device.last_seen = now
            device.total_requests += 1

            if user_agent and user_agent not in device.user_agents:
                device.user_agents.append(user_agent)

            if model_accessed and model_accessed not in device.ai_models_accessed:
                device.ai_models_accessed.append(model_accessed)

            # Update average request size
            device.average_request_size_bytes = (
                (device.average_request_size_bytes * (device.total_requests - 1) + request_size) /
                device.total_requests
            )

        self.save_devices()
        return self.devices[client_ip]

    def record_block(self, client_ip: str) -> Optional[DeviceProfile]:
        """Record a blocked request from a device"""
        if client_ip in self.devices:
            device = self.devices[client_ip]
            device.total_blocks += 1

            # Increase risk score based on blocks
            block_rate = device.total_blocks / device.total_requests if device.total_requests > 0 else 0
            device.risk_score = min(100, 10 + (block_rate * 50))

            # If too many blocks, flag for review
            if device.total_blocks >= self.FAILED_ATTEMPTS_THRESHOLD:
                if ViolationType.MULTIPLE_FAILED_ATTEMPTS.value not in device.violations:
                    device.violations.append(ViolationType.MULTIPLE_FAILED_ATTEMPTS.value)
                    self.record_violation(
                        client_ip,
                        ViolationType.MULTIPLE_FAILED_ATTEMPTS,
                        "high",
                        f"Device {client_ip} exceeded failed attempt threshold ({device.total_blocks})",
                        {'total_blocks': device.total_blocks, 'block_rate': f"{block_rate*100:.1f}%"}
                    )

            self.save_devices()
            return device
        return None

    def detect_suspicious_patterns(self, client_ip: str) -> List[Tuple[str, float]]:
        """Detect suspicious patterns in device behavior"""
        if client_ip not in self.devices:
            return []

        device = self.devices[client_ip]
        suspicious = []

        # Pattern 1: Rapid escalation of requests
        if device.total_requests > 100:
            time_active = datetime.fromisoformat(device.last_seen) - datetime.fromisoformat(device.first_seen)
            if time_active.total_seconds() > 0:
                requests_per_minute = device.total_requests / (time_active.total_seconds() / 60)
                if requests_per_minute > 50:  # More than 50 requests per minute
                    suspicious.append(("excessive_request_rate", requests_per_minute))

        # Pattern 2: Multiple user agents (credential sharing indicator)
        if len(device.user_agents) > 5:
            suspicious.append(("multiple_user_agents", float(len(device.user_agents))))

        # Pattern 3: High block rate
        block_rate = device.total_blocks / device.total_requests if device.total_requests > 0 else 0
        if block_rate > 0.5:  # More than 50% blocks
            suspicious.append(("high_block_rate", block_rate))

        # Pattern 4: Unusual access times (would need timestamp data)
        if len(device.ai_models_accessed) > 10:
            suspicious.append(("accessing_many_models", float(len(device.ai_models_accessed))))

        return suspicious

    def record_violation(self, device_ip: str, violation_type: ViolationType,
                        severity: str, description: str, evidence: Dict):
        """Record a security violation"""
        violation = SecurityViolation(
            device_ip=device_ip,
            violation_type=violation_type,
            severity=severity,
            description=description,
            timestamp=datetime.now().isoformat(),
            evidence=evidence
        )

        self.violations.append(violation)

        # Update device status based on violation
        if device_ip in self.devices:
            device = self.devices[device_ip]

            if severity == "critical":
                device.status = DeviceStatus.BLOCKED
                device.risk_score = 100
            elif severity == "high":
                if device.status != DeviceStatus.BLOCKED:
                    device.status = DeviceStatus.SUSPECTED
                device.risk_score = min(100, device.risk_score + 30)
            elif severity == "medium":
                device.risk_score = min(100, device.risk_score + 15)

            self.save_devices()

    def get_device_profile(self, client_ip: str) -> Optional[Dict]:
        """Get detailed profile of a device"""
        if client_ip not in self.devices:
            return None

        device = self.devices[client_ip]
        suspicious = self.detect_suspicious_patterns(client_ip)

        return {
            'ip_address': device.ip_address,
            'hostname': device.hostname,
            'first_seen': device.first_seen,
            'last_seen': device.last_seen,
            'total_requests': device.total_requests,
            'total_blocks': device.total_blocks,
            'block_rate_percent': (device.total_blocks / device.total_requests * 100) if device.total_requests > 0 else 0,
            'status': device.status.value,
            'risk_score': device.risk_score,
            'violations': device.violations,
            'user_agents_count': len(device.user_agents),
            'models_accessed': device.ai_models_accessed,
            'average_request_size_mb': device.average_request_size_bytes / (1024 * 1024),
            'suspicious_patterns': [{'pattern': p[0], 'value': p[1]} for p in suspicious]
        }

    def get_network_summary(self) -> Dict:
        """Get summary of network activity"""
        total_devices = len(self.devices)
        trusted = sum(1 for d in self.devices.values() if d.status == DeviceStatus.TRUSTED)
        monitored = sum(1 for d in self.devices.values() if d.status == DeviceStatus.MONITORED)
        suspected = sum(1 for d in self.devices.values() if d.status == DeviceStatus.SUSPECTED)
        blocked = sum(1 for d in self.devices.values() if d.status == DeviceStatus.BLOCKED)

        high_risk_devices = [
            ip for ip, device in self.devices.items()
            if device.risk_score >= self.RISK_SCORE_THRESHOLD
        ]

        recent_violations = [v for v in self.violations if not v.resolved][-10:]

        return {
            'total_devices': total_devices,
            'trusted_devices': trusted,
            'monitored_devices': monitored,
            'suspected_devices': suspected,
            'blocked_devices': blocked,
            'high_risk_count': len(high_risk_devices),
            'high_risk_devices': high_risk_devices,
            'recent_violations': len(recent_violations),
            'total_violations': len(self.violations),
            'active_violations': len([v for v in self.violations if not v.resolved])
        }

# Initialize global network tracker
network_tracker = NetworkTracker()
