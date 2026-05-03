# market_signals/services.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

APP_KEY = os.environ.get("KIS_APP_KEY")
APP_SECRET = os.environ.get("KIS_APP_SECRET")
BASE_URL = os.environ.get("KIS_BASE_URL")

def get_access_token():
    """앱키와 시크릿키를 이용해 접근 토큰을 발급받습니다."""
    url = f"{BASE_URL}/oauth2/tokenP"
    headers = {"content-type": "application/json"}
    body = {
        "grant_type": "client_credentials",
        "appkey": APP_KEY,
        "appsecret": APP_SECRET
    }
    response = requests.post(url, headers=headers, json=body)
    return response.json().get("access_token")

def fetch_index_price(access_token, market_code):
    """
    특정 시장(코스피/코스닥)의 실시간 지수 데이터를 KIS API에서 가져옵니다.
    market_code: '0001' (코스피), '1001' (코스닥)
    """
    url = f"{BASE_URL}/uapi/domestic-stock/v1/quotations/inquire-index-price"
    
    headers = {
        "content-type": "application/json; charset=utf-8",
        "authorization": f"Bearer {access_token}",
        "appkey": APP_KEY,
        "appsecret": APP_SECRET,
        "tr_id": "FHPUP02100000", # KIS API 국내 업종/지수 조회용 TR ID
        "custtype": "P" # 개인(P)
    }
    
    params = {
        "fid_cond_mrkt_div_code": "U", # 업종(U)
        "fid_input_iscd": market_code
    }
    
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def get_kis_market_data():
    """발급받은 토큰을 이용해 코스피, 코스닥 지표를 종합하여 반환합니다."""
    access_token = get_access_token()
    
    # 1. KIS 서버에서 코스피(0001), 코스닥(1001) 데이터 받아오기
    kospi_raw = fetch_index_price(access_token, "0001")
    kosdaq_raw = fetch_index_price(access_token, "1001")

    print("====== KIS 서버 에러 원인 확인 ======")
    print(kospi_raw)
    
    # 2. 받아온 복잡한 원본 데이터에서 우리가 화면에 그릴 알맹이만 쏙 빼냅니다.
    # KIS API 응답값 기준: bstp_nmix_prpr(현재가), prdy_ctrt(전일대비율)
    kospi_data = kospi_raw.get("output", {})
    kosdaq_data = kosdaq_raw.get("output", {})

    processed_data = {
        "kospi_price": kospi_data.get("bstp_nmix_prpr", "0"),     # 코스피 현재 지수
        "kospi_change": kospi_data.get("prdy_ctrt", "0") + "%",   # 코스피 등락률
        "kosdaq_price": kosdaq_data.get("bstp_nmix_prpr", "0"),   # 코스닥 현재 지수
        "kosdaq_change": kosdaq_data.get("prdy_ctrt", "0") + "%", # 코스닥 등락률
        
        # 신호등 로직은 임시 유지 (추후 알고리즘 적용 예정)
        "short_term_signal": {"status": "Y", "label": "주의"},
        "long_term_signal": {"status": "G", "label": "양호"},
    }
    
    return processed_data