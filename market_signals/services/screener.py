"""
market_signals/services/screener.py

수집된 DataFrame을 4가지 카테고리로 분류합니다.

  1. 저평가 성장주  : PER ≤ 20, ROE ≥ 10%
  2. 저렴한 가치주  : PBR ≤ 1.5, PER ≤ 15
  3. 꾸준한 배당주  : 배당수익률 ≥ 3%, ROE ≥ 5%, PBR ≤ 3.0, PER ≤ 25
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
    저평가 성장주 선별
    - PER > 0, PER ≤ 20
    - ROE ≥ 10%
    - 정렬: ROE/PER 내림차순 (성장성 대비 저렴한 순)
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
    max_pbr: float = 1.5,
    max_per: float = 15.0,
    top_n:   int   = 20,
) -> pd.DataFrame:
    """
    저렴한 가치주 선별
    - PBR > 0, PBR ≤ 1.5
    - PER > 0, PER ≤ 15
    - 정렬: PBR 오름차순 (자산 대비 가장 저렴한 순)
    """
    mask = (
        (df["pbr"] > 0)        &
        (df["pbr"] <= max_pbr) &
        (df["per"] > 0)        &
        (df["per"] <= max_per)
    )
    return (
        df[mask]
        .sort_values("pbr", ascending=True)
        .head(top_n)
        .reset_index(drop=True)
    )


# ── 3. 꾸준한 배당주 ──────────────────────────
def screen_dividend_stock(
    df:            pd.DataFrame,
    min_div_yield: float = 3.0,
    min_roe:       float = 5.0,
    max_pbr:       float = 3.0,
    max_per:       float = 25.0,
    top_n:         int   = 20,
) -> pd.DataFrame:
    """
    꾸준한 배당주 선별
    - 배당수익률 ≥ 3%  (기본 조건)
    - ROE ≥ 5%         (수익성 확인 - 배당 줄 능력 있는 기업)
    - PBR ≤ 3.0        (자산 건전성)
    - PER ≤ 25         (주가 거품 방지)
    - 정렬: 배당수익률 내림차순
    """
    mask = (
        (df["div_yield"] >= min_div_yield) &
        (df["roe"]       >= min_roe)       &
        (df["pbr"]       >  0)             &
        (df["pbr"]       <= max_pbr)       &
        (df["per"]       >  0)             &
        (df["per"]       <= max_per)
    )
    return (
        df[mask]
        .sort_values("div_yield", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )


# ── 4. 거래량 상위 ────────────────────────────
def screen_high_volume(
    df:    pd.DataFrame,
    top_n: int = 10,
) -> pd.DataFrame:
    """
    거래량 상위 10개 선별
    - 당일 거래량 기준 내림차순
    """
    return (
        df[df["volume"] > 0]
        .sort_values("volume", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )


# ── 전체 실행 ─────────────────────────────────
def run_all_screens(df: pd.DataFrame) -> dict:
    """
    4가지 스크리닝 결과를 딕셔너리로 반환

    Returns
    -------
    {
        "growth_undervalued" : pd.DataFrame,  # 저평가 성장주
        "value_stock"        : pd.DataFrame,  # 저렴한 가치주
        "dividend_stock"     : pd.DataFrame,  # 꾸준한 배당주
        "high_volume"        : pd.DataFrame,  # 거래량 상위 10
    }
    """
    results = {
        "growth_undervalued": screen_growth_undervalued(df),
        "value_stock":        screen_value_stock(df),
        "dividend_stock":     screen_dividend_stock(df),
        "high_volume":        screen_high_volume(df),
    }
    for category, result_df in results.items():
        print(f"[{category}] {len(result_df)}개 종목 선별")
    return results