import os
import requests
import pandas as pd
import FinanceDataReader as fdr
import traceback
from datetime import datetime, timedelta
from dotenv import load_dotenv

print("🚀🚀🚀 market_data.py 파일이 정상적으로 연결되었습니다!!! 🚀🚀🚀")

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

def get_market_historical_data():
    """
    KOSPI 데이터를 바탕으로 이동평균, 이격도, ADR(추정치), 52주 데이터(추정치)를 한 번에 계산합니다.
    """
    try:
        start_date = (datetime.today() - timedelta(days=500)).strftime('%Y-%m-%d')
        df = fdr.DataReader('KS11', start_date)
        
        if df.empty:
            return [], []
        
        # 1. 일일 수익률 계산 (ADR 및 신고/신저가 추정을 위함)
        df['Return'] = df['Close'].pct_change() * 100
        
        # 2. 이동평균 및 이격도 계산
        df['MA20'] = df['Close'].rolling(window=20).mean().round(2)
        df['MA200'] = df['Close'].rolling(window=200).mean().round(2)
        df['Disp20'] = (df['Close'] / df['MA20']).round(4)
        df['Disp200'] = (df['Close'] / df['MA200']).round(4) 
        
        clean_df = df.dropna()
        
        # --- [차트 1 & 3] 일별 이격도 및 ADR 데이터 추출 (최근 6일) ---
        recent_daily_df = clean_df.tail(6)
        chart_data = []
        
        for date, row in recent_daily_df.iterrows():
            # 실제 수익률에 비례하여 ADR 추정 (기본 100 기준, 변동폭 증폭)
            # 향후 DB 구축 시 `MarketBreadth.objects.get(date=date).adr` 로 교체
            estimated_adr = max(50.0, min(150.0, 100 + (row['Return'] * 15)))
            
            chart_data.append({
                "date": date.strftime("%m-%d"),
                "kospi": row['Close'],
                "ma20": row['MA20'],
                "ma200": row['MA200'],
                "disp20": row['Disp20'],
                "disp200": row['Disp200'],
                "adr": round(estimated_adr, 2)
            })
            
        # --- [차트 2] 주간 52주 신고/신저가 추이 데이터 추출 (최근 6주) ---
        # 매주 금요일(또는 마지막 거래일) 데이터를 샘플링
        weekly_df = clean_df.resample('W-FRI').last().tail(6)
        fifty_two_week_data = []
        
        for date, row in weekly_df.iterrows():
            weekly_return = row['Return']
            
            # 주간 수익률을 바탕으로 신고/신저가 비율 역산 (프록시)
            high_ratio = max(0.5, min(15.0, 4.0 + (weekly_return * 2)))
            low_ratio = max(0.5, min(15.0, 4.0 - (weekly_return * 2.5)))
            
            # 순증: (신고가 비율 - 신저가 비율) * 시장 가중치
            net_increase = int((high_ratio - low_ratio) * 12.5)
            
            fifty_two_week_data.append({
                "date": date.strftime("%m-%d"),
                "high_ratio": round(high_ratio, 2),
                "low_ratio": round(low_ratio, 2),
                "net_increase": net_increase
            })
            
        return chart_data, fifty_two_week_data
        
    except Exception as e:
        print(f"[디버그] 🚨 Historical Data Error: {e}")
        traceback.print_exc()
        return [], []
    
def get_kis_market_data():
    access_token = get_access_token()
    
    kospi_raw = fetch_index_price(access_token, "0001")
    kosdaq_raw = fetch_index_price(access_token, "1001")
    
    kospi_out = kospi_raw.get("output", {})
    kosdaq_out = kosdaq_raw.get("output", {})
    
    advancing = int(kospi_out.get("ascn_issu_cnt", 1))
    declining = int(kospi_out.get("down_issu_cnt", 1))
    adr_ratio = (advancing / declining) * 100 if declining > 0 else 100
    
    if adr_ratio >= 120:
        short_signal = {"status": "G", "label": "양호 (🟢)"}
    elif adr_ratio >= 80:
        short_signal = {"status": "Y", "label": "주의 (🟡)"}
    else:
        short_signal = {"status": "R", "label": "매우 주의 (🔴)"}

    # 함수 하나로 2개의 차트 데이터를 모두 받아옵니다.
    historical_chart_data, weekly_breadth_data = get_market_historical_data()    
        
    processed_data = {
        "kospi_price": kospi_out.get("bstp_nmix_prpr", "0"),
        "kospi_change": kospi_out.get("bstp_nmix_prdy_ctrt", "0") + "%",
        "kosdaq_price": kosdaq_out.get("bstp_nmix_prpr", "0"),   
        "kosdaq_change": kosdaq_out.get("bstp_nmix_prdy_ctrt", "0") + "%", 
        "short_term_signal": short_signal,
        "long_term_signal": {"status": "G", "label": "양호"},
        "chart_data": historical_chart_data,
        "fifty_two_week_data": weekly_breadth_data, # <--- 추가됨!
    }
    
    return processed_data
