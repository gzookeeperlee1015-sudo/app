import os
import requests
from dotenv import load_dotenv

# .env 파일 안의 내용들을 파이썬이 읽을 수 있게 불러옵니다.
load_dotenv()

# 진짜 API 키는 코드에 안 적고 변수로만 가져옵니다.
APP_KEY = os.environ.get("KIS_APP_KEY")
APP_SECRET = os.environ.get("KIS_APP_SECRET")
BASE_URL = os.environ.get("KIS_BASE_URL")

def get_access_token():
    """앱키와 시크릿키를 이용해 24시간 동안 유효한 접근 토큰을 자동 발급받습니다."""
    url = f"{BASE_URL}/oauth2/tokenP"
    headers = {"content-type": "application/json"}
    body = {
        "grant_type": "client_credentials",
        "appkey": APP_KEY,
        "appsecret": APP_SECRET
    }
    response = requests.post(url, headers=headers, json=body)
    # 발급된 임시 비밀번호(토큰)만 쏙 뽑아서 전달합니다.
    return response.json().get("access_token")

def get_kis_market_data():
    """발급받은 토큰을 이용해 현재 시장 지표 데이터를 요청합니다."""
    # 1. 여기서 자동으로 방금 발급된 토큰을 받아옵니다.
    access_token = get_access_token()
    
    # --- 나중에 여기에 진짜 실시간 시세 API 요청 로직이 들어갑니다 ---
    # (일단은 화면에 에러 안 나게 기존 가짜 데이터를 유지합니다)
    processed_data = {
        "short_term": {"status": "Y", "label": "주의"},
        "kospi_price": "6,598.87",
        "message": "안전한 토큰 발급 로직이 적용되었습니다!"
    }
    
    return processed_data