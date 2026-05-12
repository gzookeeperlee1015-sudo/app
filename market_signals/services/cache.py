"""
market_signals/services/cache.py

데이터 캐시 & 자동 갱신 스케줄러
- 메모리 캐시 : 30분마다 자동 갱신
- 파일 캐시   : 서버 재시작 후에도 직전 데이터 즉시 제공
- 스케줄러    : 평일 장중(09:00~15:30) 30분마다 자동 수집
"""

import json
import logging
import threading
import time
from datetime import datetime
from pathlib import Path

import pandas as pd

from .fetcher  import fetch_all_markets
from .screener import run_all_screens

logger = logging.getLogger(__name__)

CACHE_FILE       = Path(__file__).resolve().parent.parent / "cache_data.json"
REFRESH_INTERVAL = 30 * 60   # 30분 (초 단위)

# ── 인메모리 캐시 ──────────────────────────────
_cache: dict = {
    "data":       None,
    "updated_at": None,
}
_lock = threading.Lock()


# ── 직렬화 헬퍼 ───────────────────────────────
def _df_to_records(df: pd.DataFrame) -> list:
    """DataFrame → JSON 직렬화 가능한 list[dict]"""
    return df.to_dict(orient="records")


# ── 파일 캐시 ─────────────────────────────────
def _save_to_file(data: dict):
    try:
        CACHE_FILE.write_text(
            json.dumps(data, ensure_ascii=False, default=str),
            encoding="utf-8"
        )
        logger.info("파일 캐시 저장 완료")
    except Exception as e:
        logger.warning(f"파일 캐시 저장 실패: {e}")


def _load_from_file() -> dict | None:
    if not CACHE_FILE.exists():
        return None
    try:
        return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    except Exception as e:
        logger.warning(f"파일 캐시 로드 실패: {e}")
        return None


# ── 데이터 갱신 ───────────────────────────────
def refresh_data() -> dict:
    """
    yfinance로 최신 데이터를 가져와
    4가지 카테고리로 분류 후 캐시에 저장합니다.
    """
    logger.info("데이터 갱신 시작...")

    raw_df = fetch_all_markets()

    if raw_df.empty:
        logger.error("수집된 데이터 없음 - 갱신 중단")
        # 기존 캐시 유지
        with _lock:
            return _cache["data"] or {}

    screens = run_all_screens(raw_df)

    payload = {
        "screens": {
            "growth_undervalued": _df_to_records(screens["growth_undervalued"]),  # 저평가 성장주
            "value_stock":        _df_to_records(screens["value_stock"]),         # 저렴한 가치주
            "dividend_stock":     _df_to_records(screens["dividend_stock"]),      # 꾸준한 배당주
            "high_volume":        _df_to_records(screens["high_volume"]),         # 거래량 상위 10
        },
        "total":      len(raw_df),
        "updated_at": datetime.now().isoformat(),
    }

    with _lock:
        _cache["data"]       = payload
        _cache["updated_at"] = datetime.now()

    _save_to_file(payload)
    logger.info(f"데이터 갱신 완료: 총 {payload['total']}개 종목")
    return payload


def get_cached_data() -> dict:
    """
    캐시된 데이터 반환
    캐시가 없거나 30분 이상 지났으면 새로 수집
    """
    with _lock:
        updated_at = _cache["updated_at"]
        data       = _cache["data"]

    # 메모리 캐시 유효 확인 (30분 이내)
    if data and updated_at:
        elapsed = (datetime.now() - updated_at).total_seconds()
        if elapsed < REFRESH_INTERVAL:
            return data

    # 파일 캐시 시도
    file_data = _load_from_file()
    if file_data:
        with _lock:
            _cache["data"]       = file_data
            _cache["updated_at"] = datetime.now()

        # 백그라운드에서 최신 데이터 갱신
        t = threading.Thread(target=refresh_data, daemon=True)
        t.start()
        return file_data

    # 캐시 없으면 동기 수집 (최초 1회)
    return refresh_data()


# ── 자동 스케줄러 ─────────────────────────────
def _scheduler_loop():
    """평일 장중(09:00~15:30) 30분마다 자동 갱신"""
    while True:
        now             = datetime.now()
        is_weekday      = now.weekday() < 5
        is_market_hours = 9 <= now.hour < 16

        if is_weekday and is_market_hours:
            try:
                refresh_data()
            except Exception as e:
                logger.error(f"스케줄러 갱신 실패: {e}")
            time.sleep(REFRESH_INTERVAL)
        else:
            time.sleep(60 * 60)  # 장 외: 1시간마다 체크


def start_scheduler():
    """백그라운드 스케줄러 스레드 시작 (Django apps.py 에서 호출)"""
    t = threading.Thread(
        target=_scheduler_loop,
        daemon=True,
        name="Stock-Scheduler",
    )
    t.start()
    logger.info("자동 갱신 스케줄러 시작")