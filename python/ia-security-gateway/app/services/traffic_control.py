"""
Traffic Control Service
Monitors and controls data flow to external AI services
"""
import logging
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, Tuple

logger = logging.getLogger(__name__)

class TrafficController:
    """Controls and monitors traffic to external services"""

    def __init__(self):
        self.request_history: Dict[str, list] = defaultdict(list)
        self.blocked_requests = 0
        self.allowed_requests = 0

    def check_rate_limit(self, client_id: str, limit: int, window: int) -> Tuple[bool, Dict]:
        """
        Check if client is within rate limits
        Returns: (is_allowed, stats)
        """
        now = datetime.now()
        cutoff_time = now - timedelta(seconds=window)

        # Clean old requests
        self.request_history[client_id] = [
            timestamp for timestamp in self.request_history[client_id]
            if timestamp > cutoff_time
        ]

        request_count = len(self.request_history[client_id])

        if request_count >= limit:
            self.blocked_requests += 1
            logger.warning(
                f"⚠️  Rate limit exceeded for {client_id}: "
                f"{request_count}/{limit} in last {window}s"
            )
            return False, {
                "current": request_count,
                "limit": limit,
                "window": window
            }

        # Record this request
        self.request_history[client_id].append(now)
        self.allowed_requests += 1

        return True, {
            "current": request_count + 1,
            "limit": limit,
            "window": window
        }

    def detect_data_exfiltration(self, payload: str, destination: str) -> Tuple[bool, str]:
        """
        Detect suspicious patterns that indicate data exfiltration
        Returns: (is_suspicious, reason)
        """
        # Check for multiple sensitive patterns in one request
        sensitive_patterns = [
            'password', 'token', 'api_key', 'secret',
            'credit_card', 'ssn', 'dni'
        ]

        pattern_count = sum(
            1 for pattern in sensitive_patterns
            if pattern.lower() in payload.lower()
        )

        if pattern_count > 2:
            reason = f"Multiple sensitive data patterns detected ({pattern_count})"
            logger.critical(f"🚨 SUSPICIOUS: {reason} → {destination}")
            return True, reason

        # Check for unusually large payloads
        if len(payload) > 1_000_000:  # 1MB
            reason = f"Unusually large payload: {len(payload)} bytes"
            logger.warning(f"⚠️  SUSPECT: {reason}")
            return True, reason

        return False, "Safe"

    def get_stats(self) -> Dict:
        """Get traffic control statistics"""
        return {
            "allowed_requests": self.allowed_requests,
            "blocked_requests": self.blocked_requests,
            "active_clients": len(self.request_history),
            "timestamp": datetime.now().isoformat()
        }
