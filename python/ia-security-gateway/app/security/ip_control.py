# IA Security Gateway - IP Control Module
# Professional IP Whitelist/Blacklist Management

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import json
from datetime import datetime
import ipaddress
from pathlib import Path

class IPAction(str, Enum):
    ALLOW = "allow"
    BLOCK = "block"

@dataclass
class IPRule:
    """Represent an IP rule (allow or block)"""
    ip_address: str
    action: IPAction
    description: str
    added_by: str
    timestamp: str
    reason: str  # SECURITY_VIOLATION, POLICY, TESTING, etc

class IPController:
    """Manage IP-based access control for IA services"""

    def __init__(self, rules_file: str = "data/ip_rules.json"):
        self.rules_file = rules_file
        self.whitelist: Dict[str, IPRule] = {}
        self.blacklist: Dict[str, IPRule] = {}
        self.load_rules()

    def load_rules(self):
        """Load IP rules from storage"""
        try:
            if Path(self.rules_file).exists():
                with open(self.rules_file, 'r') as f:
                    data = json.load(f)
                    # Reconstruct IPRule objects
                    for ip, rule_dict in data.get('whitelist', {}).items():
                        rule_dict['action'] = IPAction(rule_dict['action'])
                        self.whitelist[ip] = IPRule(**rule_dict)
                    for ip, rule_dict in data.get('blacklist', {}).items():
                        rule_dict['action'] = IPAction(rule_dict['action'])
                        self.blacklist[ip] = IPRule(**rule_dict)
        except Exception as e:
            print(f"Error loading IP rules: {e}")

    def save_rules(self):
        """Save IP rules to storage"""
        try:
            Path(self.rules_file).parent.mkdir(parents=True, exist_ok=True)
            data = {
                'whitelist': {ip: asdict(rule) for ip, rule in self.whitelist.items()},
                'blacklist': {ip: asdict(rule) for ip, rule in self.blacklist.items()}
            }
            with open(self.rules_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving IP rules: {e}")

    def validate_ip(self, ip_address: str) -> bool:
        """Validate IP format"""
        try:
            ipaddress.ip_address(ip_address)
            return True
        except ValueError:
            return False

    def add_whitelist(self, ip_address: str, description: str, added_by: str,
                     reason: str = "APPROVED") -> Tuple[bool, str]:
        """Add IP to whitelist"""
        if not self.validate_ip(ip_address):
            return False, "Invalid IP format"

        if ip_address in self.blacklist:
            del self.blacklist[ip_address]

        rule = IPRule(
            ip_address=ip_address,
            action=IPAction.ALLOW,
            description=description,
            added_by=added_by,
            timestamp=datetime.now().isoformat(),
            reason=reason
        )
        self.whitelist[ip_address] = rule
        self.save_rules()
        return True, f"IP {ip_address} added to whitelist"

    def add_blacklist(self, ip_address: str, description: str, added_by: str,
                     reason: str = "SECURITY_VIOLATION") -> Tuple[bool, str]:
        """Add IP to blacklist (blocks access)"""
        if not self.validate_ip(ip_address):
            return False, "Invalid IP format"

        if ip_address in self.whitelist:
            del self.whitelist[ip_address]

        rule = IPRule(
            ip_address=ip_address,
            action=IPAction.BLOCK,
            description=description,
            added_by=added_by,
            timestamp=datetime.now().isoformat(),
            reason=reason
        )
        self.blacklist[ip_address] = rule
        self.save_rules()
        return True, f"IP {ip_address} added to blacklist - ACCESS DENIED"

    def remove_rule(self, ip_address: str) -> Tuple[bool, str]:
        """Remove an IP rule"""
        if ip_address in self.whitelist:
            del self.whitelist[ip_address]
            self.save_rules()
            return True, f"IP {ip_address} removed from whitelist"
        elif ip_address in self.blacklist:
            del self.blacklist[ip_address]
            self.save_rules()
            return True, f"IP {ip_address} removed from blacklist"
        return False, "IP not found in any list"

    def check_access(self, ip_address: str) -> Tuple[bool, str]:
        """Check if IP is allowed to access IA services"""
        # Blacklist takes priority - immediate block
        if ip_address in self.blacklist:
            rule = self.blacklist[ip_address]
            return False, f"BLOCKED: {rule.description} (Reason: {rule.reason})"

        # If whitelist exists and IP is in it, allow
        if ip_address in self.whitelist:
            return True, "ALLOWED: IP in whitelist"

        # If whitelist exists but IP not in it, deny (strict mode)
        if self.whitelist:
            return False, "BLOCKED: IP not in whitelist (strict mode)"

        # If no whitelist, allow by default (permissive mode)
        return True, "ALLOWED: Permissive mode (no whitelist configured)"

    def get_stats(self) -> Dict:
        """Get IP control statistics"""
        return {
            'whitelist_count': len(self.whitelist),
            'blacklist_count': len(self.blacklist),
            'total_rules': len(self.whitelist) + len(self.blacklist),
            'mode': 'strict' if self.whitelist else 'permissive'
        }

    def get_rules(self) -> Dict:
        """Get all IP rules"""
        return {
            'whitelist': {ip: asdict(rule) for ip, rule in self.whitelist.items()},
            'blacklist': {ip: asdict(rule) for ip, rule in self.blacklist.items()}
        }

# Initialize global IP controller
ip_controller = IPController()
