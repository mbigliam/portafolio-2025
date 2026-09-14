#!/usr/bin/env python3
"""
IA Security Gateway - Complete Endpoint Testing Script
Tests all 17+ endpoints to verify they work correctly
FIXED VERSION - Handles Windows temp files and correct violation types
"""

import requests
import json
import sys
import os
import tempfile
from datetime import datetime
from typing import Tuple

# Configuration
API_BASE_URL = "http://localhost:8000/api"
TIMEOUT = 10

# Colors for output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """Print a formatted header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")

def print_test(name: str, passed: bool, message: str = "", response_time: float = 0):
    """Print test result"""
    status = f"{Colors.GREEN}✅ PASS{Colors.RESET}" if passed else f"{Colors.RED}❌ FAIL{Colors.RESET}"
    time_str = f" ({response_time:.2f}ms)" if response_time > 0 else ""
    print(f"{status} {name}{time_str}")
    if message:
        print(f"   └─ {message}")

def test_endpoint(method: str, endpoint: str, params=None, data=None, files=None) -> Tuple[bool, str, float]:
    """Test a single endpoint"""
    try:
        url = f"{API_BASE_URL}{endpoint}"

        if method == "GET":
            response = requests.get(url, params=params, timeout=TIMEOUT)
        elif method == "POST":
            response = requests.post(url, params=params, data=data, files=files, json=data if not files else None, timeout=TIMEOUT)
        elif method == "DELETE":
            response = requests.delete(url, params=params, timeout=TIMEOUT)
        else:
            return False, f"Unknown method: {method}", 0

        response_time = response.elapsed.total_seconds() * 1000

        if response.status_code in [200, 201, 204]:
            try:
                json_data = response.json() if response.text else {}
                return True, json.dumps(json_data, indent=2)[:200], response_time
            except:
                return True, response.text[:200], response_time
        else:
            error_msg = f"HTTP {response.status_code}"
            try:
                error_msg += f": {response.json()}"
            except:
                error_msg += f": {response.text[:100]}"
            return False, error_msg, response_time

    except requests.exceptions.ConnectionError:
        return False, "❌ Cannot connect to backend. Is it running on :8000?", 0
    except requests.exceptions.Timeout:
        return False, "❌ Request timeout (>10s)", 0
    except Exception as e:
        return False, str(e), 0

def main():
    """Run all endpoint tests"""
    print(f"{Colors.BOLD}{Colors.BLUE}")
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║   IA Security Gateway - ENDPOINT VERIFICATION TEST        ║
    ║   Complete test suite for all API endpoints               ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    print(Colors.RESET)

    total_tests = 0
    passed_tests = 0
    failed_tests = 0

    # ====================================================================
    # 1. AI GATEWAY ENDPOINTS (with /ai/ prefix)
    # ====================================================================
    print_header("1️⃣  AI GATEWAY ENDPOINTS (/api/ai/*)")

    # Test 1.1: Get Status
    print(f"{Colors.BOLD}[1.1] GET /api/ai/status{Colors.RESET}")
    passed, msg, time = test_endpoint("GET", "/ai/status")
    print_test("System Status Check", passed, msg, time)
    total_tests += 1
    passed_tests += passed
    failed_tests += not passed

    # Test 1.2: Traffic Stats
    print(f"\n{Colors.BOLD}[1.2] GET /api/ai/traffic-stats{Colors.RESET}")
    passed, msg, time = test_endpoint("GET", "/ai/traffic-stats")
    print_test("Traffic Statistics", passed, msg, time)
    total_tests += 1
    passed_tests += passed
    failed_tests += not passed

    # Test 1.3: Compliance Report
    print(f"\n{Colors.BOLD}[1.3] GET /api/ai/compliance{Colors.RESET}")
    passed, msg, time = test_endpoint("GET", "/ai/compliance")
    print_test("Compliance Report", passed, msg, time)
    total_tests += 1
    passed_tests += passed
    failed_tests += not passed

    # Test 1.4: Generate Text
    print(f"\n{Colors.BOLD}[1.4] POST /api/ai/generate{Colors.RESET}")
    passed, msg, time = test_endpoint("POST", "/ai/generate", params={"prompt": "Test prompt"})
    print_test("Text Generation", passed, msg, time)
    total_tests += 1
    passed_tests += passed
    failed_tests += not passed

    # Test 1.5: Chat
    print(f"\n{Colors.BOLD}[1.5] POST /api/ai/chat{Colors.RESET}")
    passed, msg, time = test_endpoint("POST", "/ai/chat", params={"message": "Hello"})
    print_test("Chat Interface", passed, msg, time)
    total_tests += 1
    passed_tests += passed
    failed_tests += not passed

    # ====================================================================
    # 2. SECURITY IP CONTROL ENDPOINTS
    # ====================================================================
    print_header("2️⃣  SECURITY IP CONTROL ENDPOINTS (/api/security/ip/*)")

    # Test 2.1: Get IP Rules
    print(f"{Colors.BOLD}[2.1] GET /api/security/ip/rules{Colors.RESET}")
    passed, msg, time = test_endpoint("GET", "/security/ip/rules")
    print_test("Get IP Rules", passed, msg, time)
    total_tests += 1
    passed_tests += passed
    failed_tests += not passed

    # Test 2.2: Verify IP
    print(f"\n{Colors.BOLD}[2.2] GET /api/security/ip/verify (Query: ip=192.168.1.100){Colors.RESET}")
    passed, msg, time = test_endpoint("GET", "/security/ip/verify", params={"ip": "192.168.1.100"})
    print_test("IP Verification", passed, msg, time)
    total_tests += 1
    passed_tests += passed
    failed_tests += not passed

    # Test 2.3: Add Whitelist
    print(f"\n{Colors.BOLD}[2.3] POST /api/security/ip/whitelist{Colors.RESET}")
    passed, msg, time = test_endpoint("POST", "/security/ip/whitelist", params={"ip": "10.0.0.1", "description": "Test IP"})
    print_test("Add to Whitelist", passed, msg, time)
    total_tests += 1
    passed_tests += passed
    failed_tests += not passed

    # Test 2.4: Add Blacklist
    print(f"\n{Colors.BOLD}[2.4] POST /api/security/ip/blacklist{Colors.RESET}")
    passed, msg, time = test_endpoint("POST", "/security/ip/blacklist", params={"ip": "203.0.113.1", "reason": "SECURITY_VIOLATION"})
    print_test("Add to Blacklist", passed, msg, time)
    total_tests += 1
    passed_tests += passed
    failed_tests += not passed

    # ====================================================================
    # 3. FILE ANALYSIS ENDPOINTS
    # ====================================================================
    print_header("3️⃣  SECURITY FILE ANALYSIS ENDPOINTS (/api/security/file/*)")

    # Test 3.1: Analyze File (create temp file)
    print(f"{Colors.BOLD}[3.1] POST /api/security/file/analyze (multipart form){Colors.RESET}")
    try:
        # Create temp file in proper location (Windows compatible)
        temp_fd, temp_path = tempfile.mkstemp(suffix=".txt", text=True)
        try:
            os.write(temp_fd, b"Test content for email: test@example.com and SSN: 123-45-6789")
            os.close(temp_fd)

            # Now read and send the file
            with open(temp_path, "rb") as f:
                files = {"file": f}
                response = requests.post(
                    f"{API_BASE_URL}/security/file/analyze",
                    params={"client_ip": "192.168.1.1"},
                    files=files,
                    timeout=TIMEOUT
                )

            passed = response.status_code == 200
            msg = response.json().get("risk_level", "No risk level") if response.status_code == 200 else response.text[:100]
            time = response.elapsed.total_seconds() * 1000
        finally:
            # Clean up temp file
            try:
                os.unlink(temp_path)
            except:
                pass
    except Exception as e:
        print_test("File Analysis", False, str(e))
        passed = False
        time = 0

    print_test("File Analysis", passed, msg if passed else str(e), time)
    total_tests += 1
    passed_tests += passed
    failed_tests += not passed

    # Test 3.2: Analysis Summary
    print(f"\n{Colors.BOLD}[3.2] GET /api/security/file/analysis-summary{Colors.RESET}")
    passed, msg, time = test_endpoint("GET", "/security/file/analysis-summary")
    print_test("File Analysis Summary", passed, msg, time)
    total_tests += 1
    passed_tests += passed
    failed_tests += not passed

    # ====================================================================
    # 4. NETWORK TRACKING ENDPOINTS
    # ====================================================================
    print_header("4️⃣  NETWORK TRACKING ENDPOINTS (/api/network/*)")

    # Test 4.1: Get All Devices
    print(f"{Colors.BOLD}[4.1] GET /api/network/devices{Colors.RESET}")
    passed, msg, time = test_endpoint("GET", "/network/devices")
    print_test("Get All Devices", passed, msg, time)
    total_tests += 1
    passed_tests += passed
    failed_tests += not passed

    # Test 4.2: Network Summary
    print(f"\n{Colors.BOLD}[4.2] GET /api/network/summary{Colors.RESET}")
    passed, msg, time = test_endpoint("GET", "/network/summary")
    print_test("Network Summary", passed, msg, time)
    total_tests += 1
    passed_tests += passed
    failed_tests += not passed

    # Test 4.3: Track Device
    print(f"\n{Colors.BOLD}[4.3] POST /api/network/track-device{Colors.RESET}")
    passed, msg, time = test_endpoint("POST", "/network/track-device",
        params={"ip": "192.168.1.50", "hostname": "TEST-PC", "user_agent": "Testing"})
    print_test("Track Device", passed, msg, time)
    total_tests += 1
    passed_tests += passed
    failed_tests += not passed

    # Test 4.4: Get Device Profile
    print(f"\n{Colors.BOLD}[4.4] GET /api/network/device-profile (Query: ip=192.168.1.50){Colors.RESET}")
    passed, msg, time = test_endpoint("GET", "/network/device-profile", params={"ip": "192.168.1.50"})
    print_test("Get Device Profile", passed, msg, time)
    total_tests += 1
    passed_tests += passed
    failed_tests += not passed

    # ====================================================================
    # 5. VIOLATIONS ENDPOINTS
    # ====================================================================
    print_header("5️⃣  VIOLATIONS ENDPOINTS (/api/security/violations)")

    # Test 5.1: Get Violations
    print(f"{Colors.BOLD}[5.1] GET /api/security/violations{Colors.RESET}")
    passed, msg, time = test_endpoint("GET", "/security/violations")
    print_test("Get Violations", passed, msg, time)
    total_tests += 1
    passed_tests += passed
    failed_tests += not passed

    # Test 5.2: Report Violation (FIXED - using correct violation type)
    print(f"\n{Colors.BOLD}[5.2] POST /api/security/violations{Colors.RESET}")
    passed, msg, time = test_endpoint("POST", "/security/violations",
        params={"ip": "203.0.113.50", "type": "UNAUTHORIZED_ACCESS", "description": "Test violation"})
    print_test("Report Violation", passed, msg, time)
    total_tests += 1
    passed_tests += passed
    failed_tests += not passed

    # ====================================================================
    # SUMMARY
    # ====================================================================
    print_header("📊 TEST SUMMARY")

    total_str = f"Total Tests: {total_tests}"
    passed_str = f"Passed: {passed_tests}"
    failed_str = f"Failed: {failed_tests}"
    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0

    print(f"{total_str}")
    print(f"{Colors.GREEN}{passed_str}{Colors.RESET}")
    if failed_tests > 0:
        print(f"{Colors.RED}{failed_str}{Colors.RESET}")

    print(f"\n{Colors.BOLD}Success Rate: {success_rate:.1f}%{Colors.RESET}")

    if success_rate == 100:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✅ SUCCESS: All endpoints working! (100%){Colors.RESET}\n")
        return 0
    elif success_rate >= 80:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️  MOSTLY WORKING: {success_rate:.1f}% of endpoints working{Colors.RESET}")
        print(f"Failed tests: {failed_tests}/{total_tests}")
        print(f"\nMake sure:")
        print(f"  1. Ollama is running (ollama serve)")
        print(f"  2. Ollama has mistral model (ollama pull mistral)")
        print(f"  3. Backend is running on http://localhost:8000")
        return 1
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ FAILURE: Backend may not be running or routes not updated ({success_rate:.1f}%){Colors.RESET}")
        print(f"Make sure:")
        print(f"  1. Backend is running on http://localhost:8000")
        print(f"  2. Route files have been replaced with CORRECTED versions")
        print(f"  3. Backend has been restarted after file replacement")
        return 1

if __name__ == "__main__":
    sys.exit(main())
