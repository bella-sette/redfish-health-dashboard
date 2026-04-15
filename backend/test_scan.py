import requests
import json

print("=== Dell Redfish Health Analyzer - Interactive Tester ===\n")

print("Choose a test scenario:")
print("1. Mixed Issues (Current default)")
print("2. Healthy System (No issues)")
print("3. Warning Only")
print("4. Critical System")
print("5. Custom Input")

choice = input("\nEnter choice (1-5) [1]: ").strip() or "1"

scenario_map = {
    "1": "mixed",
    "2": "healthy",
    "3": "warning",
    "4": "critical",
    "5": "mixed"
}

scenario = scenario_map.get(choice, "mixed")

# Default credentials
ip = "192.168.1.100"
username = "root"
password = "calvin"

if choice == "5":
    print("\nCustom Input:")
    ip = input(f"iDRAC IP [{ip}]: ").strip() or ip
    username = input(f"Username [{username}]: ").strip() or username
    password = input(f"Password [{password}]: ").strip() or password

print(f"\n🧪 Running scenario: {scenario.upper()}")

url = "http://127.0.0.1:8000/scan"

payload = {
    "ip": ip,
    "username": username,
    "password": password
}

# Important: Pass scenario as query parameter
params = {"scenario": scenario}

print("\n" + "="*70)
print("Sending scan request...")
print(f"Target IP     : {ip}")
print(f"Username      : {username}")
print(f"Scenario      : {scenario}")
print("-" * 70)

try:
    response = requests.post(url, json=payload, params=params, timeout=15)
    
    print(f"\nStatus Code: {response.status_code}\n")
    
    if response.status_code == 200:
        result = response.json()
        
        print("✅ SUCCESS - Health Analysis Report")
        print("=" * 80)
        print(json.dumps(result, indent=2))
        print("=" * 80)
        
        score = result.get('health_score', 0)
        risk = result.get('risk_level', 'UNKNOWN')
        issues_count = len(result.get('issues', []))
        
        print(f"\n📊 SUMMARY:")
        print(f"   Health Score : {score}/100")
        print(f"   Risk Level   : {risk}")
        print(f"   Issues       : {issues_count}")
        
        if score >= 80:
            print("   Overall Status: 🟢 GOOD / HEALTHY")
        elif score >= 50:
            print("   Overall Status: 🟡 MODERATE")
        else:
            print("   Overall Status: 🔴 NEEDS ATTENTION")
            
    else:
        print("❌ Request failed")
        print(response.text)

except requests.exceptions.ConnectionError:
    print("❌ Could not connect to FastAPI server.")
    print("   Make sure the server is running:")
    print("   py -m uvicorn app:app --reload")
except Exception as e:
    print(f"❌ Error: {e}")

print("\nTip: You can add more scenarios in redfish_client.py")