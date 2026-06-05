"""
market_signals/services/screener.py

4가지 카테고리로 분류합니다.

  1. 저평가 성장주  : PER ≤ 20, ROE ≥ 10%
  2. 저렴한 가치주  : PER ≤ 10 (PBR 제거 - yfinance 데이터 부실)
  3. 52주 신고가 근접 종목 : 현재가가 52주 최고가의 90% 이상
  4. 거래량 상위    : 당일 거래량 Top 10
"""

import pandas as pd


# ── 1. 저평가 성장주 ──────────────────────────
def screen_growth_undervalued(
    df:      pd.DataFrame,
    max_per: float = 20.0,
    min_roe: float = 10.0,
    top_n:   int   = 20,
) -> pd.DataFrame:
    """
    저평가 성장주
    - PER > 0, PER ≤ 20
    - ROE ≥ 10%
    - 정렬: ROE/PER 내림차순
    """
    mask = (
        (df["per"] > 0)        &
        (df["per"] <= max_per) &
        (df["roe"] >= min_roe)
    )
    filtered = df[mask].copy()
    filtered["score"] = filtered["roe"] / filtered["per"]
    return (
        filtered
        .sort_values("score", ascending=False)
        .drop(columns=["score"])
        .head(top_n)
        .reset_index(drop=True)
    )


# ── 2. 저렴한 가치주 ──────────────────────────
def screen_value_stock(
    df:      pd.DataFrame,
    max_per: float = 10.0,
    top_n:   int   = 20,
) -> pd.DataFrame:
    """
    저렴한 가치주
    - PER > 0, PER ≤ 10 (시장 평균 이하로 매우 저평가)
    - 정렬: PER 오름차순
    """
    mask = (
        (df["per"] > 0)        &
        (df["per"] <= max_per)
    )
    return (
        df[mask]
        .sort_values("per", ascending=True)
        .head(top_n)
        .reset_index(drop=True)
    )


# ── 3. 52주 신고가 근접 종목 ──────────────────
def screen_52week_high(
    df:           pd.DataFrame,
    min_ratio:    float = 0.90,   # 52주 최고가의 90% 이상
    top_n:        int   = 20,
) -> pd.DataFrame:
    """
    52주 신고가 근접 종목
    - 52주 최고가 데이터 있는 종목만
    - 현재가 / 52주 최고가 ≥ 90%
    - 정렬: 비율 내림차순 (신고가에 가장 근접한 순)

    의미: 52주 최고가에 근접했다는 건 강한 상승 모멘텀을 가진 종목
    """
    if "week52_high" not in df.columns:
        return pd.DataFrame()

    mask = (
        (df["week52_high"] > 0) &
        (df["price"] > 0)       &
        (df["price"] / df["week52_high"] >= min_ratio)
    )
    filtered = df[mask].copy()
    filtered["high_ratio"] = round(filtered["price"] / filtered["week52_high"] * 100, 1)

    return (
        filtered
        .sort_values("high_ratio", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )


# ── 4. 거래량 상위 ────────────────────────────
def screen_high_volume(
    df:    pd.DataFrame,
    top_n: int = 10,
) -> pd.DataFrame:
    """거래량 상위 10개"""
    return (
        df[df["volume"] > 0]
        .sort_values("volume", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )


# ── 전체 실행 ─────────────────────────────────
def run_all_screens(df: pd.DataFrame) -> dict:
    """
    4가지 스크리닝 결과 반환

    Returns
    -------
    {
        "growth_undervalued" : pd.DataFrame,  # 저평가 성장주
        "value_stock"        : pd.DataFrame,  # 저렴한 가치주
        "week52_high"        : pd.DataFrame,  # 52주 신고가 근접
        "high_volume"        : pd.DataFrame,  # 거래량 상위 10
    }
    """
    results = {
        "growth_undervalued": screen_growth_undervalued(df),
        "value_stock":        screen_value_stock(df),
        "week52_high":        screen_52week_high(df),
        "high_volume":        screen_high_volume(df),
    }
    for category, result_df in results.items():
        print(f"[{category}] {len(result_df)}개 종목 선별")
    return results