import urllib.request
import json
import sys

def test_login(username, password):
    url = "http://127.0.0.1:8000/api/token/"
    payload = json.dumps({"username": username, "password": password}).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            print(f"Login attempt for {username}: Status {response.status}")
            print(f"Response: {response.read().decode('utf-8')}")
            return response.status == 200
    except Exception as e:
        print(f"Error for {username}: {e}")
        if hasattr(e, 'read'):
            print(f"Trace: {e.read().decode('utf-8')}")
        return False

# Test for admin
print("Testing login for admin/Admin@1234...")
test_login("admin", "Admin@1234")
