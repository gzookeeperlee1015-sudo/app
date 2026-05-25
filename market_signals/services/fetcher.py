"""
market_signals/services/fetcher.py

네이버 증권 종목 리스트 + yfinance 배치 수집
- 가격/거래량    : yfinance download() 배치
- 재무/52주고가  : yfinance Ticker().info 개별
"""

import logging
import requests
import pandas as pd
import yfinance as yf
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def _get_naver_tickers(market: str = "KOSPI", max_page: int = 4) -> pd.DataFrame:
    """네이버 증권에서 시가총액 순 종목 리스트 수집"""
    headers = {"User-Agent": "Mozilla/5.0"}
    records = []

    for page in range(1, max_page + 1):
        url = (
            f"https://finance.naver.com/sise/sise_market_sum.naver"
            f"?sosok={'0' if market == 'KOSPI' else '1'}&page={page}"
        )
        try:
            res = requests.get(url, headers=headers, timeout=10)
            res.encoding = "euc-kr"
            soup = BeautifulSoup(res.text, "html.parser")
            rows = soup.select("table.type_2 tbody tr")

            for row in rows:
                link = row.select_one("a")
                if not link:
                    continue
                name   = link.text.strip()
                href   = link.get("href", "")
                ticker = href.split("code=")[-1][:6] if "code=" in href else ""
                if ticker and name:
                    records.append({"ticker": ticker, "name": name})

            logger.info(f"[{market}] 페이지 {page} 완료")

        except Exception as e:
            logger.warning(f"[{market}] 페이지 {page} 실패: {e}")

    df = pd.DataFrame(records).drop_duplicates(subset="ticker")
    logger.info(f"[{market}] 총 {len(df)}개 종목 리스트 완료")
    return df


def _fetch_fundamental(ticker_code: str, market: str) -> dict:
    """
    yfinance로 재무 데이터 + 52주 최고가 수집
    """
    suffix  = ".KS" if market == "KOSPI" else ".KQ"
    yf_code = ticker_code + suffix

    try:
        info = yf.Ticker(yf_code).info

        per       = round(float(info.get("trailingPE")     or info.get("forwardPE") or 0), 2)
        pbr       = round(float(info.get("priceToBook")    or 0), 2)
        roe       = round(float(info.get("returnOnEquity") or 0) * 100, 2)

        # 배당수익률: yfinance가 소수(0.04)로 주면 *100, 이미 %(4.0)이면 그대로
        raw_div   = float(info.get("dividendYield") or 0)
        div_yield = round(raw_div * 100 if raw_div < 1 else raw_div, 2)

        # 52주 최고가
        week52_high = round(float(info.get("fiftyTwoWeekHigh") or 0), 0)

        return {
            "per":         per,
            "pbr":         pbr,
            "roe":         roe,
            "div_yield":   div_yield,
            "week52_high": week52_high,
        }
    except Exception:
        return {"per": 0, "pbr": 0, "roe": 0, "div_yield": 0, "week52_high": 0}


def fetch_market_data(market: str = "KOSPI", max_page: int = 4) -> pd.DataFrame:
    """네이버 종목 리스트 + yfinance 배치 수집"""

    # 1. 종목 리스트
    ticker_df = _get_naver_tickers(market, max_page)
    if ticker_df.empty:
        return pd.DataFrame()

    tickers  = ticker_df["ticker"].tolist()
    names    = dict(zip(ticker_df["ticker"], ticker_df["name"]))
    suffix   = ".KS" if market == "KOSPI" else ".KQ"
    yf_codes = [t + suffix for t in tickers]

    logger.info(f"[{market}] {len(tickers)}개 종목 배치 수집 시작")

    # 2. 배치로 가격 수집
    try:
        raw = yf.download(
            yf_codes,
            period="2d",
            auto_adjust=True,
            progress=False,
            group_by="ticker",
        )
    except Exception as e:
        logger.error(f"배치 수집 실패: {e}")
        return pd.DataFrame()

    # 3. 가격 데이터 파싱
    records = []
    for ticker in tickers:
        yf_code = ticker + suffix
        try:
            if len(tickers) == 1:
                close  = raw["Close"].dropna()
                volume = raw["Volume"].dropna()
            else:
                close  = raw[yf_code]["Close"].dropna()
                volume = raw[yf_code]["Volume"].dropna()

            if len(close) < 1:
                continue

            price      = float(close.iloc[-1])
            prev_close = float(close.iloc[-2]) if len(close) >= 2 else price
            vol        = int(volume.iloc[-1]) if len(volume) >= 1 else 0

            if price == 0:
                continue

            change_rate = round(((price - prev_close) / prev_close) * 100, 2) if prev_close else 0.0

            records.append({
                "ticker":      ticker,
                "name":        names.get(ticker, ticker),
                "market":      market,
                "price":       int(price),
                "change_rate": change_rate,
                "volume":      vol,
                "market_cap":  0,
            })
        except Exception as e:
            logger.debug(f"{ticker} 파싱 실패: {e}")

    logger.info(f"[{market}] 가격 {len(records)}개 완료, 재무 수집 시작")

    # 4. 재무 + 52주 최고가 수집
    for i, record in enumerate(records, 1):
        fund = _fetch_fundamental(record["ticker"], market)
        record.update(fund)
        if i % 20 == 0:
            logger.info(f"  [{market}] 재무 {i}/{len(records)} 처리 중...")

    df = pd.DataFrame(records)
    logger.info(f"[{market}] 전체 완료: {len(df)}개")
    return df


def fetch_all_markets() -> pd.DataFrame:
    """KOSPI + KOSDAQ 전체 데이터 합쳐서 반환"""
    kospi  = fetch_market_data("KOSPI",  max_page=4)
    kosdaq = fetch_market_data("KOSDAQ", max_page=3)

    if kospi.empty and kosdaq.empty:
        logger.error("전체 수집 실패")
        return pd.DataFrame()

    return pd.concat([kospi, kosdaq], ignore_index=True)