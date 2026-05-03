import os
import requests
from dotenv import load_dotenv

load_dotenv()

class KISDataFetcher:
    def __init__(self):
        self.api_key = os.getenv("KIS_API_KEY")
        self.api_secret = os.getenv("KIS_API_SECRET")
        self.base_url = "https://openapi.koreainvestment.com:9443"

    def get_access_token(self):
        """실제 토큰 발급 요청 로직입니다."""
        headers = {"content-type": "application/json"}
        body = {
            "grant_type": "client_credentials",
            "appkey": self.api_key,
            "appsecret": self.api_secret
        }
        url = f"{self.base_url}/oauth2/tokenP"
        res = requests.post(url, headers=headers, json=body)
        
        if res.status_code == 200:
            return res.json().get("access_token")
        else:
            print(f"Error: {res.status_code}") # 제안서의 예외 처리 원칙 반영
            return None