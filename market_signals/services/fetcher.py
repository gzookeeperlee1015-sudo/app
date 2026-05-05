"""
market_signals/services/fetcher.py

한국투자증권 Open API 데이터 수집 모듈
- API 키는 .env 파일에서 불러옵니다
- 키 발급 후 .env 파일에 값만 채우면 바로 동작합니다

필요 라이브러리: pip install requests python-dotenv pandas
"""

import os
import logging
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# ── 환경변수에서 키 불러오기 ──────────────────
APP_KEY    = os.environ.get("KIS_APP_KEY", "")
APP_SECRET = os.environ.get("KIS_APP_SECRET", "")
BASE_URL   = os.environ.get("KIS_BASE_URL", "https://openapi.koreainvestment.com:9443")


# ── 1. 토큰 발급 ──────────────────────────────
def get_access_token() -> str:
    """
    한국투자증권 API Access Token 발급
    모든 API 요청에 이 토큰이 필요합니다
    토큰 유효시간: 24시간
    """
    url = f"{BASE_URL}/oauth2/tokenP"
    headers = {"content-type": "application/json"}
    body = {
        "grant_type": "client_credentials",
        "appkey":     APP_KEY,
        "appsecret":  APP_SECRET,
    }
    response = requests.post(url, headers=headers, json=body, timeout=10)
    token = response.json().get("access_token", "")
    logger.info("Access Token 발급 완료")
    return token


# ── 2. 공통 헤더 ──────────────────────────────
def _make_headers(access_token: str, tr_id: str) -> dict:
    """
    한국투자증권 API 공통 헤더
    tr_id: API마다 다른 거래 ID
    """
    return {
        "content-type":  "application/json; charset=utf-8",
        "authorization": f"Bearer {access_token}",
        "appkey":        APP_KEY,
        "appsecret":     APP_SECRET,
        "tr_id":         tr_id,
        "custtype":      "P",
    }


# ── 3. 종목 리스트 조회 ───────────────────────
def fetch_ticker_list(access_token: str, market: str = "J") -> list:
    """
    KOSPI/KOSDAQ 전체 종목 코드 리스트 조회

    market: "J" = KOSPI, "Q" = KOSDAQ
    반환값: ["005930", "000660", ...] 티커 리스트
    """
    url = f"{BASE_URL}/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"
    headers = _make_headers(access_token, "FHKST03010100")
    params = {
        "fid_cond_mrkt_div_code": market,
        "fid_input_iscd":         "0000",  # 전체 종목
    }
    response = requests.get(url, headers=headers, params=params, timeout=10)
    data = response.json()
    output = data.get("output", [])
    return [item["mksc_shrn_iscd"] for item in output if "mksc_shrn_iscd" in item]


# ── 4. 종목별 기본 시세 조회 ──────────────────
def fetch_stock_price(access_token: str, ticker: str) -> dict:
    """
    개별 종목 현재가 / 거래량 / 등락률 조회

    반환값:
        price       : 현재가
        change_rate : 등락률 (%)
        volume      : 거래량
    """
    url = f"{BASE_URL}/uapi/domestic-stock/v1/quotations/inquire-price"
    headers = _make_headers(access_token, "FHKST01010100")
    params = {
        "fid_cond_mrkt_div_code": "J",
        "fid_input_iscd":         ticker,
    }
    response = requests.get(url, headers=headers, params=params, timeout=10)
    output = response.json().get("output", {})

    return {
        "ticker":      ticker,
        "price":       int(output.get("stck_prpr", 0) or 0),       # 현재가
        "change_rate": float(output.get("prdy_ctrt", 0) or 0),     # 등락률
        "volume":      int(output.get("acml_vol", 0) or 0),        # 누적 거래량
        "market_cap":  int(output.get("hts_avls", 0) or 0),        # 시가총액
    }


# ── 5. 종목별 재무 데이터 조회 ────────────────
def fetch_stock_fundamental(access_token: str, ticker: str) -> dict:
    """
    개별 종목 PER / PBR / ROE / 배당수익률 조회

    반환값:
        per       : PER
        pbr       : PBR
        roe       : ROE (%)
        div_yield : 배당수익률 (%)
    """
    url = f"{BASE_URL}/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"
    headers = _make_headers(access_token, "FHKST03010100")
    params = {
        "fid_cond_mrkt_div_code": "J",
        "fid_input_iscd":         ticker,
        "fid_period_div_code":    "D",
        "fid_org_adj_prc":        "1",
    }
    response = requests.get(url, headers=headers, params=params, timeout=10)
    output = response.json().get("output1", {})

    return {
        "ticker":    ticker,
        "per":       float(output.get("per",  0) or 0),   # PER
        "pbr":       float(output.get("pbr",  0) or 0),   # PBR
        "roe":       float(output.get("roe",  0) or 0),   # ROE
        "div_yield": float(output.get("divi", 0) or 0),   # 배당수익률
    }


# ── 6. 전체 시장 데이터 수집 ──────────────────
def fetch_market_data(market: str = "J", max_stocks: int = 300) -> pd.DataFrame:
    """
    특정 시장 전체 종목 데이터 수집

    market     : "J" = KOSPI, "Q" = KOSDAQ
    max_stocks : 최대 수집 종목 수
    반환값     : DataFrame (ticker, name, price, change_rate,
                            per, pbr, roe, div_yield, volume, market_cap)
    """
    access_token = get_access_token()
    tickers = fetch_ticker_list(access_token, market)
    tickers = tickers[:max_stocks]
    logger.info(f"[{market}] {len(tickers)}개 종목 수집 시작")

    records = []
    for i, ticker in enumerate(tickers, 1):
        try:
            # 시세 + 재무 데이터 합치기
            price_data       = fetch_stock_price(access_token, ticker)
            fundamental_data = fetch_stock_fundamental(access_token, ticker)

            record = {**price_data, **fundamental_data}  # 두 딕셔너리 합치기
            record["market"] = "KOSPI" if market == "J" else "KOSDAQ"

            if record["price"] == 0:
                continue

            records.append(record)

            if i % 50 == 0:
                logger.info(f"  [{market}] {i}/{len(tickers)} 처리 중...")

        except Exception as e:
            logger.debug(f"  {ticker} 오류: {e}")
            continue

    df = pd.DataFrame(records)
    logger.info(f"[{market}] 수집 완료: {len(df)}개 종목")
    return df


def fetch_all_markets(max_stocks_per_market: int = 300) -> pd.DataFrame:
    """KOSPI + KOSDAQ 전체 데이터 합쳐서 반환"""
    kospi  = fetch_market_data("J", max_stocks_per_market)
    kosdaq = fetch_market_data("Q", max_stocks_per_market)
    return pd.concat([kospi, kosdaq], ignore_index=True)