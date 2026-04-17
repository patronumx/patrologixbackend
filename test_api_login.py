import requests
import sys

def test_login(username, password):
    url = "http://127.0.0.1:8000/api/token/"
    payload = {"username": username, "password": password}
    try:
        response = requests.post(url, json=payload)
        print(f"Login attempt for {username}: Status {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

# Test for admin
test_login("admin", "Admin@1234")
