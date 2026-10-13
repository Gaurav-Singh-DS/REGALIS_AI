import requests
import sys

BASE_URL = "http://localhost:8080"
REPORT_ID = "rep_credit_risk_2026_09"
HEADERS = {"Authorization": "Bearer mock-dev-token", "Content-Type": "application/json"}

def verify():
    print("🚀 Starting Local AI Verification...")
    
    # 1. Check Health
    try:
        r = requests.get(f"{BASE_URL}/health")
        print(f"✅ Server Health: {r.status_code}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        sys.exit(1)

    # 2. Trigger Investigation
    print("🔍 Triggering AI Investigation (this may take a few minutes)...")
    try:
        r = requests.post(f"{BASE_URL}/api/investigations/{REPORT_ID}", headers=HEADERS, timeout=300)
        if r.status_code != 200:
            print(f"❌ Investigation failed with status {r.status_code}: {r.text}")
            sys.exit(1)
        
        data = r.json()
        root_cause = data.get("root_cause", "").lower()
        print("\n--- AI RESPONSE ---")
        print(data.get("root_cause"))
        print("------------------\n")
        
        if "root cause" in root_cause:
            print("✅ SUCCESS: AI mentioned 'root cause'!")
        else:
            print("❌ FAILURE: AI did not mention 'root cause'.")
            
    except Exception as e:
        print(f"❌ Error during investigation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    verify()
