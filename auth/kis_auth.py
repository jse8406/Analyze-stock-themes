import requests
import os
from dotenv import load_dotenv

# .env 로드
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path=env_path)

APP_KEY = os.getenv('g_appkey')
APP_SECRET = os.getenv('g_appsecret')
DOMAIN = "https://openapi.koreainvestment.com:9443"

def get_approval_key(appkey=APP_KEY, appsecret=APP_SECRET):
    """
    한국투자증권 OpenAPI Approval Key 발급
    :param appkey: 앱키 (없으면 .env에서 로드)
    :param appsecret: 앱시크릿 (없으면 .env에서 로드)
    :return: approval_key (str) or None
    """
    url = f"{DOMAIN}/oauth2/Approval"
    payload = {
        "grant_type": "client_credentials",
        "appkey": appkey or APP_KEY,
        "secretkey": appsecret or APP_SECRET
    }
    try:
        r = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=10)
        if r.status_code == 200:
            body = r.json()
            return body.get("approval_key")
    except Exception as e:
        print(f"[KIS Auth] Approval Key Error: {e}")
    return None


def get_access_token(appkey=None, appsecret=None):
    """
    실시간 가격이 아닌 현재가 정보를 받기 위한 access token을 발급

    Args:
        appkey (_type_, optional): 앱키
        appsecret (_type_, optional): 앱시크릿
    """
    url = f"{DOMAIN}/oauth2/tokenP"
    payload = {
        "grant_type": "client_credentials",
        "appkey": appkey or APP_KEY,
        "appsecret": appsecret or APP_SECRET
    }
    try:
        print("payload : ", payload)
        r = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=10)
        print("status code : ", r.status_code)
        print("response : ", r.text)
        if r.status_code == 200:
            body = r.json()
            print(body)
            return body
    except Exception as e:
        print(f"[KIS Auth] Approval Key Error: {e}")
    return None