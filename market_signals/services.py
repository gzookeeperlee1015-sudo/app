import os
import requests
from dotenv import load_dotenv

load_dotenv()

APP_KEY = os.environ.get("KIS_APP_KEY")
APP_SECRET = os.environ.get("KIS_APP_SECRET")
BASE_URL = os.environ.get("KIS_BASE_URL")

def get_access_token():
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
    url = f"{BASE_URL}/uapi/domestic-stock/v1/quotations/inquire-index-price"
    headers = {
        "content-type": "application/json; charset=utf-8",
        "authorization": f"Bearer {access_token}",
        "appkey": APP_KEY,
        "appsecret": APP_SECRET,
        "tr_id": "FHPUP02100000",
        "custtype": "P"
    }
    params = {
        "fid_cond_mrkt_div_code": "U",
        "fid_input_iscd": market_code
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def get_kis_market_data():
    access_token = get_access_token()
    
    # 1. 코스피와 코스닥 데이터 각각 가져오기
    kospi_raw = fetch_index_price(access_token, "0001")
    kosdaq_raw = fetch_index_price(access_token, "1001")
    
    kospi_out = kospi_raw.get("output", {})
    kosdaq_out = kosdaq_raw.get("output", {})
    
    # 2. 시장 신호 알고리즘 (ADR 기반)
    advancing = int(kospi_out.get("ascn_issu_cnt", 1))
    declining = int(kospi_out.get("down_issu_cnt", 1))
    adr_ratio = (advancing / declining) * 100 if declining > 0 else 100
    
    if adr_ratio >= 120:
        short_signal = {"status": "G", "label": "양호 (🟢)"}
    elif adr_ratio >= 80:
        short_signal = {"status": "Y", "label": "주의 (🟡)"}
    else:
        short_signal = {"status": "R", "label": "매우 주의 (🔴)"}
        
    # 3. 데이터 조립 (에러가 났던 코스닥 데이터들도 꼼꼼히 추가!)
    processed_data = {
        "kospi_price": kospi_out.get("bstp_nmix_prpr", "0"),
        "kospi_change": kospi_out.get("bstp_nmix_prdy_ctrt", "0") + "%",
        "kosdaq_price": kosdaq_out.get("bstp_nmix_prpr", "0"),   # <--- 추가됨!
        "kosdaq_change": kosdaq_out.get("bstp_nmix_prdy_ctrt", "0") + "%", # <--- 추가됨!
        "short_term_signal": short_signal,
        "long_term_signal": {"status": "G", "label": "양호"},
    }
    
    return processed_data