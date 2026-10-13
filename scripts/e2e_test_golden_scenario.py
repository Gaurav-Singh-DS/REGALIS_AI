import os
import requests
import sys
from typing import Dict, Any

# Configuration
CONFIG = {
    "BASE_URL": os.getenv("API_BASE_URL", "http://localhost:8080"),
    "REPORT_ID": "rep_credit_risk_2026_09",
    "AUTH_TOKEN": "mock-dev-token",
    "ENVIRONMENT": "development"
}

class GoldenScenarioTester:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {CONFIG['AUTH_TOKEN']}",
            "Content-Type": "application/json"
        })
        self.base_url = CONFIG["BASE_URL"]

    def log(self, message: str):
        print(f"🔍 {message}")

    def assert_true(self, condition: bool, success_msg: str, failure_msg: str):
        if not condition:
            print(f"❌ ASSERTION FAILED: {failure_msg}")
            sys.exit(1)
        print(f"✅ {success_msg}")

    def test_health(self):
        self.log("Checking server health...")
        resp = self.session.get(f"{self.base_url}/health")
        self.assert_true(
            resp.status_code == 200,
            "Server is reachable",
            f"Health check failed with status {resp.status_code}"
        )
        self.assert_true(
            resp.json().get("status") == "healthy",
            "Server status is healthy",
            f"Server is not healthy: {resp.json()}"
        )

    def test_report_status(self):
        self.log(f"Verifying report status for {CONFIG['REPORT_ID']}...")
        resp = self.session.get(f"{self.base_url}/api/reports/{CONFIG['REPORT_ID']}")
        self.assert_true(
            resp.status_code == 200,
            "Report fetched successfully",
            f"Failed to fetch report: {resp.text}"
        )

        data = resp.json()
        self.assert_true(
            data.get("status") == "Anomaly Detected",
            "Report status is 'Anomaly Detected'",
            f"Expected 'Anomaly Detected', got '{data.get('status')}'"
        )

    def test_report_metrics(self):
        self.log("Verifying metrics for Credit Risk jump...")
        resp = self.session.get(f"{self.base_url}/api/reports/{CONFIG['REPORT_ID']}/metrics")
        self.assert_true(
            resp.status_code == 200,
            "Metrics fetched successfully",
            f"Failed to fetch metrics: {resp.text}"
        )

        metrics = resp.json()

        # Verify High Risk Count jump
        high_risk = next((m for m in metrics if "High Risk Count" in m["metric_name"]), None)
        self.assert_true(
            high_risk is not None,
            "High Risk Count metric found",
            "High Risk Count metric not found"
        )
        self.assert_true(
            high_risk["current_value"] >= 120000,
            "High Risk Count jump detected",
            f"High Risk Count jump not detected: {high_risk['current_value']}"
        )

        # Verify Total Exposure jump
        exposure = next((m for m in metrics if "Total Exposure" in m["metric_name"]), None)
        self.assert_true(
            exposure is not None,
            "Total Exposure metric found",
            "Total Exposure metric not found"
        )
        self.assert_true(
            exposure["current_value"] >= 110000000,
            "Total Exposure jump detected",
            f"Total Exposure jump not detected: {exposure['current_value']}"
        )

    def test_ai_investigation(self):
        self.log("Triggering AI Investigation (RCA)...")
        # Increased timeout to 300 seconds for local LLM processing
        resp = self.session.post(f"{self.base_url}/api/investigations/{CONFIG['REPORT_ID']}", timeout=300)
        self.assert_true(
            resp.status_code == 200,
            "Investigation triggered successfully",
            f"Investigation failed: {resp.text}"
        )

        data = resp.json()
        self.assert_true(
            "investigationId" in data,
            "Investigation ID returned",
            "No investigationId returned in response"
        )

        # Validate RCA content
        # The result is usually a dictionary containing the agent's findings
        result_text = str(data.get("root_cause", "")).lower()

        required_keywords = [
            ("root cause", "Root Cause mentioned"),
            ("anomaly", "Anomaly mentioned"),
            ("credit risk", "Credit Risk mentioned"),
            ("policy", "Policy mentioned")
        ]
        for kw, success_msg in required_keywords:
            self.assert_true(
                kw in result_text,
                success_msg,
                f"AI result missing critical keyword: '{kw}'"
            )

        self.log("AI Investigation successfully validated!")

    def run_all(self):
        print("🚀 Starting Golden Scenario E2E Test Suite")
        print(f"Environment: {CONFIG['ENVIRONMENT']} | Base URL: {CONFIG['BASE_URL']}")
        print("-" * 50)

        try:
            self.test_health()
            self.test_report_status()
            self.test_report_metrics()
            self.test_ai_investigation()
            print("-" * 50)
            print("🎉 GOLDEN SCENARIO E2E TEST PASSED SUCCESSFULLY!")
        except Exception as e:
            print(f"💥 Unexpected error during test execution: {e}")
            sys.exit(1)

if __name__ == "__main__":
    tester = GoldenScenarioTester()
    tester.run_all()
