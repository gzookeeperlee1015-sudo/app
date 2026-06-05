import yfinance as yf
import random
from datetime import datetime, timedelta

# ──────────────────────────────────────────────
# 게임에 사용할 한국 주식 종목 목록
# yfinance 티커 형식: 코스피 → .KS / 코스닥 → .KQ
# ──────────────────────────────────────────────
KOREAN_STOCKS = {
    "삼성전자": "005930.KS",
    "SK하이닉스": "000660.KS",
    "LG에너지솔루션": "373220.KS",
    "삼성바이오로직스": "207940.KS",
    "현대차": "005380.KS",
    "카카오": "035720.KS",
    "네이버": "035420.KS",
    "셀트리온": "068270.KS",
    "기아": "000270.KS",
    "포스코홀딩스": "005490.KS",
    "에코프로비엠": "247540.KQ",  # 코스닥
    "에코프로": "086520.KQ",      # 코스닥
    "HLB": "028300.KQ",           # 코스닥
    "카카오게임즈": "293490.KQ",  # 코스닥
    "펄어비스": "263750.KQ",      # 코스닥
}


def get_stock_list():
    """
    프론트엔드 종목 선택 화면에 보여줄 종목 목록을 반환합니다.
    반환 예시: [{"name": "삼성전자", "ticker": "005930.KS"}, ...]
    """
    return [{"name": name, "ticker": ticker} for name, ticker in KOREAN_STOCKS.items()]


def get_stock_data(ticker: str, start_date: str, end_date: str):
    """
    yfinance를 통해 특정 종목의 일별 OHLCV 데이터를 가져옵니다.

    Args:
        ticker: yfinance 티커 (예: "005930.KS")
        start_date: 시작일 (예: "2020-01-01")
        end_date: 종료일 (예: "2024-01-01")

    Returns:
        OHLCV 딕셔너리 리스트 또는 None (데이터 없을 때)
        [
            {
                "date": "2023-05-10",
                "open": 65400,   # 시가
                "high": 66800,   # 고가
                "low": 65100,    # 저가
                "close": 66500,  # 종가
                "volume": 12345678  # 거래량
            },
            ...
        ]
    """
    # yfinance로 데이터 다운로드 (auto_adjust=True: 배당/액면분할 자동 보정)
    df = yf.download(ticker, start=start_date, end=end_date, progress=False, auto_adjust=True)

    # 데이터가 없으면 None 반환
    if df.empty:
        return None

    # DataFrame을 딕셔너리 리스트로 변환
    result = []
    for date, row in df.iterrows():
        result.append({
            "date": date.strftime("%Y-%m-%d"),
            "open": round(float(row["Open"]), 2),
            "high": round(float(row["High"]), 2),
            "low": round(float(row["Low"]), 2),
            "close": round(float(row["Close"]), 2),
            "volume": int(row["Volume"]),
        })
    return result


def get_random_game_data(ticker: str):
    """
    게임 시작 시 호출되는 함수입니다.
    전체 데이터에서 랜덤 기준점을 골라 과거 60일 + 미래 30일로 분리해 반환합니다.

    - history (과거 60일): 플레이어에게 보여주는 차트 데이터
    - future  (미래 30일): 플레이어가 하루씩 넘기며 플레이할 데이터 (처음엔 숨김)

    Args:
        ticker: yfinance 티커 (예: "005930.KS")

    Returns:
        {
            "ticker": "005930.KS",
            "pivot_date": "2022-07-15",  # 게임 시작 기준일
            "history": [...],            # 과거 60일 OHLCV
            "future": [...],             # 미래 30일 OHLCV
        }
        또는 None (데이터 부족 시)
    """
    # 데이터 범위: 2020년 ~ 1년 전까지 (너무 최근 데이터는 정답이 뻔해서 제외)
    data_end = datetime.today() - timedelta(days=365)
    data_start = datetime(2020, 1, 1)

    # 전체 기간 데이터 가져오기
    all_data = get_stock_data(
        ticker,
        data_start.strftime("%Y-%m-%d"),
        data_end.strftime("%Y-%m-%d"),
    )

    # 과거 60일 + 미래 30일 = 최소 90일치 데이터가 필요
    if not all_data or len(all_data) < 90:
        return None

    # 랜덤 기준점 선택 (앞 60일, 뒤 30일 확보 가능한 범위 내에서)
    pivot = random.randint(60, len(all_data) - 30)

    history = all_data[pivot - 60 : pivot]  # 기준점 이전 60일 (차트에 표시)
    future  = all_data[pivot : pivot + 30]  # 기준점 이후 30일 (게임 진행용)

    return {
        "ticker": ticker,
        "pivot_date": all_data[pivot]["date"],  # 게임 시작 기준일
        "history": history,
        "future": future,
    }
