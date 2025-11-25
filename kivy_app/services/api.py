import requests

BASE_URL = "http://127.0.0.1:5000"

def backend_login(username, password):
    url = f"{BASE_URL}/login"
    data = {"username": username, "password": password}

    try:
        response = requests.post(url, json=data)
        return response.json()
    except Exception as e:
        return {"success": False, "message": str(e)}
