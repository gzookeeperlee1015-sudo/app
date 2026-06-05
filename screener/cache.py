"""
screener/cache.py

30분 주기 자동 갱신 캐시
- JSON 파일(cache_data.json)을 screener/ 폴더에 저장
- 메모리 캐시 → 파일 캐시 → 실시간 수집 순으로 fallback
"""
import json, logging, threading, time
from datetime import datetime
from pathlib import Path
import pandas as pd
from .fetcher  import fetch_all_markets
from .screener import run_all_screens

logger           = logging.getLogger(__name__)
CACHE_FILE       = Path(__file__).resolve().parent / "cache_data.json"
REFRESH_INTERVAL = 30 * 60  # 30분

_cache = {"data": None, "updated_at": None}
_lock  = threading.Lock()


def _df_to_records(df):
    return df.to_dict(orient="records")


def _save_to_file(data):
    try:
        CACHE_FILE.write_text(
            json.dumps(data, ensure_ascii=False, default=str), encoding="utf-8"
        )
    except Exception as e:
        logger.warning(f"파일 캐시 저장 실패: {e}")


def _load_from_file():
    if not CACHE_FILE.exists():
        return None
    try:
        return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return None


def refresh_data() -> dict:
    logger.info("데이터 갱신 시작...")
    raw_df = fetch_all_markets()

    if raw_df.empty:
        with _lock:
            return _cache["data"] or {}

    screens = run_all_screens(raw_df)
    payload = {
        "screens": {
            "growth_undervalued": _df_to_records(screens["growth_undervalued"]),
            "value_stock":        _df_to_records(screens["value_stock"]),
            "week52_high":        _df_to_records(screens["week52_high"]),
            "high_volume":        _df_to_records(screens["high_volume"]),
        },
        "total":      len(raw_df),
        "updated_at": datetime.now().isoformat(),
    }

    with _lock:
        _cache["data"]       = payload
        _cache["updated_at"] = datetime.now()

    _save_to_file(payload)
    logger.info(f"갱신 완료: {payload['total']}개")
    return payload


def get_cached_data() -> dict:
    with _lock:
        updated_at = _cache["updated_at"]
        data       = _cache["data"]

    if data and updated_at:
        if (datetime.now() - updated_at).total_seconds() < REFRESH_INTERVAL:
            return data

    file_data = _load_from_file()
    if file_data:
        with _lock:
            _cache["data"]       = file_data
            _cache["updated_at"] = datetime.now()
        threading.Thread(target=refresh_data, daemon=True).start()
        return file_data

    return refresh_data()


def _scheduler_loop():
    while True:
        now = datetime.now()
        if now.weekday() < 5 and 9 <= now.hour < 16:
            try:
                refresh_data()
            except Exception as e:
                logger.error(f"스케줄러 오류: {e}")
            time.sleep(REFRESH_INTERVAL)
        else:
            time.sleep(3600)


def start_scheduler():
    threading.Thread(
        target=_scheduler_loop, daemon=True, name="Screener-Scheduler"
    ).start()
    logger.info("스크리너 스케줄러 시작")
