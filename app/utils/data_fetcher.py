import os
import requests
from dotenv import load_dotenv

load_dotenv()

class KisDataFetcher:
    def __init__(self):
        self.app_key = os.getenv("KIS_APP_KEY")
        self.app_secret = os.getenv("KIS_APP_SECRET")
        self.base_url = os.getenv("KIS_BASE_URL")

    def get_access_token(self):
        """API 접근을 위한 OAuth2 토큰을 발급받습니다."""
        url = f"{self.base_url}/oauth2/tokenP"
        headers = {"content-type": "application/json"}
        body = {
            "grant_type": "client_credentials",
            "appkey": self.app_key,
            "appsecret": self.app_secret
        }
        res = requests.post(url, headers=headers, json=body)
        return res.json().get("access_token")

    def get_market_status(self, token):
        """코스피/코스닥 지수 및 등락 종목 수를 가져옵니다."""
        # 실제 API 명세에 따른 TR_ID와 파라미터를 설정해야 합니다.
        # 예시로 지수 데이터를 가져오는 구조를 보여드립니다.
        url = f"{self.base_url}/uapi/domestic-stock/v1/quotations/inquire-index-price"
        headers = {
            "content-type": "application/json",
            "authorization": f"Bearer {token}",
            "appkey": self.app_key,
            "appsecret": self.app_secret,
            "tr_id": "FHKUP03500100"
        }
        params = {"fid_cond_mrkt_div_code": "U", "fid_input_iscd": "0001"} # 0001: 코스피
        res = requests.get(url, headers=headers, params=params)
        return res.json()