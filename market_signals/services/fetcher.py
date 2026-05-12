"""
market_signals/services/fetcher.py

yfinance 기반 데이터 수집 모듈 (임시 - API 키 없이 사용)
- 한국투자증권 API 키 발급 후 이 파일만 교체하면 됩니다
- KOSPI / KOSDAQ 주요 종목 데이터를 yfinance로 수집합니다

설치: pip install yfinance pandas
"""

import logging
import pandas as pd
import yfinance as yf

logger = logging.getLogger(__name__)

# ── KOSPI 주요 종목 ────────────────────────────
KOSPI_TICKERS = {
    "005930": "삼성전자",     "000660": "SK하이닉스",
    "005490": "POSCO홀딩스",  "005380": "현대차",
    "000270": "기아",         "051910": "LG화학",
    "006400": "삼성SDI",      "035420": "NAVER",
    "035720": "카카오",       "055550": "신한지주",
    "105560": "KB금융",       "086790": "하나금융지주",
    "032830": "삼성생명",     "003550": "LG",
    "066570": "LG전자",       "096770": "SK이노베이션",
    "017670": "SK텔레콤",     "030200": "KT",
    "010950": "S-Oil",        "011170": "롯데케미칼",
    "009150": "삼성전기",     "028260": "삼성물산",
    "000810": "삼성화재",     "034730": "SK",
    "012330": "현대모비스",   "207940": "삼성바이오로직스",
    "068270": "셀트리온",     "051900": "LG생활건강",
    "034020": "두산에너빌리티","010140": "삼성중공업",
    "042660": "한화오션",     "329180": "현대중공업",
    "003490": "대한항공",     "000100": "유한양행",
    "128940": "한미약품",     "002790": "아모레퍼시픽",
    "011780": "금호석유",     "009830": "한화솔루션",
    "047050": "포스코인터내셔널", "018260": "삼성에스디에스",
}

# ── KOSDAQ 주요 종목 ───────────────────────────
KOSDAQ_TICKERS = {
    "247540": "에코프로비엠",  "086520": "에코프로",
    "373220": "LG에너지솔루션","196170": "알테오젠",
    "009420": "한올바이오파마","145020": "휴젤",
    "214150": "클래시스",      "112040": "위메이드",
    "263750": "펄어비스",      "293490": "카카오게임즈",
    "035760": "CJ ENM",        "067160": "아프리카TV",
    "357780": "솔브레인",      "039030": "이오테크닉스",
    "041510": "에스엠",        "035900": "JYP Ent.",
    "122870": "와이지엔터테인먼트", "016360": "삼성증권",
    "091990": "셀트리온헬스케어",  "036540": "SFA반도체",
}


def _fetch_one(ticker_code: str, name: str, market: str) -> dict | None:
    """
    종목 하나의 데이터를 yfinance로 수집합니다.
    한국 주식 티커 형식:
      KOSPI  → 005930.KS
      KOSDAQ → 247540.KQ
    """
    suffix   = ".KS" if market == "KOSPI" else ".KQ"
    yf_code  = ticker_code + suffix

    try:
        info = yf.Ticker(yf_code).info

        price      = info.get("currentPrice") or info.get("regularMarketPrice") or 0
        prev_close = info.get("previousClose") or price
        volume     = info.get("volume") or info.get("regularMarketVolume") or 0
        market_cap = info.get("marketCap") or 0

        if price == 0:
            return None

        change_rate = round(((price - prev_close) / prev_close) * 100, 2) if prev_close else 0.0

        # yfinance는 ROE, 배당수익률을 소수(0.14 = 14%)로 반환 → *100 해서 % 단위로 변환
        per       = round(float(info.get("trailingPE")     or 0), 2)
        pbr       = round(float(info.get("priceToBook")    or 0), 2)
        roe       = round(float(info.get("returnOnEquity") or 0) * 100, 2)
        div_yield = round(float(info.get("dividendYield")  or 0) * 100, 2)

        return {
            "ticker":      ticker_code,
            "name":        name,
            "market":      market,
            "price":       int(price),
            "change_rate": change_rate,
            "per":         per,
            "pbr":         pbr,
            "roe":         roe,
            "div_yield":   div_yield,
            "volume":      int(volume),
            "market_cap":  int(market_cap),
        }

    except Exception as e:
        logger.debug(f"{ticker_code}({name}) 수집 실패: {e}")
        return None


def fetch_market_data(market: str = "KOSPI") -> pd.DataFrame:
    """KOSPI 또는 KOSDAQ 종목 데이터 수집 후 DataFrame 반환"""
    tickers = KOSPI_TICKERS if market == "KOSPI" else KOSDAQ_TICKERS
    logger.info(f"[{market}] {len(tickers)}개 종목 수집 시작")

    records = []
    for i, (code, name) in enumerate(tickers.items(), 1):
        result = _fetch_one(code, name, market)
        if result:
            records.append(result)
        if i % 10 == 0:
            logger.info(f"  [{market}] {i}/{len(tickers)} 처리 중...")

    df = pd.DataFrame(records)
    logger.info(f"[{market}] 수집 완료: {len(df)}개 종목")
    return df


def fetch_all_markets() -> pd.DataFrame:
    """
    KOSPI + KOSDAQ 데이터를 합쳐서 반환합니다.

    ※ 한국투자증권 API 키 발급 후 교체할 파일은 이 파일(fetcher.py)뿐입니다.
       screener.py / cache.py / views.py 는 수정 불필요.
    """
    kospi  = fetch_market_data("KOSPI")
    kosdaq = fetch_market_data("KOSDAQ")

    if kospi.empty and kosdaq.empty:
        logger.error("전체 수집 실패: 빈 데이터")
        return pd.DataFrame()

    return pd.concat([kospi, kosdaq], ignore_index=True)