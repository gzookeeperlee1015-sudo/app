"""
market_signals/views.py

4가지 카테고리 API 응답 처리
각 URL 요청이 들어오면 캐시에서 데이터를 꺼내 JSON으로 반환합니다.
"""

import logging
from django.http import JsonResponse
from .services.cache import get_cached_data
from .services import get_kis_market_data  # 팀원 기존 코드 유지

logger = logging.getLogger(__name__)


# ── 팀원 기존 코드 (건드리지 않음) ───────────
def get_market_dashboard_data(request):
    try:
        real_data = get_kis_market_data()

        def safe_get(key, default="0.00"):
            return real_data.get(key, default)

        dashboard_data = {
            "market_signals": {
                "short_term": real_data.get("short_term_signal", {"label": "중립 (노랑)", "status": "Y"}),
                "long_term":  real_data.get("long_term_signal",  {"label": "매수 (초록)", "status": "G"}),
            },
            "indices": {
                "kospi": {
                    "name":                   "코스피",
                    "price":                  safe_get("kospi_price"),
                    "change_percent":         safe_get("kospi_change"),
                    "change_price":           safe_get("kospi_diff", "0.00"),
                    "trend_status":           "상승 추세",
                    "exposure_guide":         "80-100%",
                    "distribution_day":       real_data.get("kospi_dist_day", 0),
                    "last_follow_through_day":"2025.09.12",
                    "is_up": float(safe_get("kospi_change").replace('%', '')) > 0
                        if isinstance(safe_get("kospi_change"), str) else False,
                },
                "kosdaq": {
                    "name":                   "코스닥",
                    "price":                  safe_get("kosdaq_price"),
                    "change_percent":         safe_get("kosdaq_change"),
                    "change_price":           safe_get("kosdaq_diff", "0.00"),
                    "trend_status":           "상승 추세",
                    "exposure_guide":         "80-100%",
                    "distribution_day":       real_data.get("kosdaq_dist_day", 2),
                    "last_follow_through_day":"2025.12.29",
                    "is_up": float(safe_get("kosdaq_change").replace('%', '')) > 0
                        if isinstance(safe_get("kosdaq_change"), str) else False,
                },
            },
            "last_updated": real_data.get("last_updated", ""),
            "chart_data": [
                {"date": "03-01", "kospi": 2600, "ma20": 0.2, "ma200": 0.4,  "adr": 80},
                {"date": "03-08", "kospi": 2620, "ma20": 0.3, "ma200": 0.38, "adr": 95},
                {"date": "03-15", "kospi": 2680, "ma20": 0.6, "ma200": 0.45, "adr": 110},
                {"date": "03-22", "kospi": 2650, "ma20": 0.5, "ma200": 0.42, "adr": 100},
                {"date": "03-29", "kospi": 2750, "ma20": 0.8, "ma200": 0.5,  "adr": 120},
            ],
        }
        return JsonResponse(dashboard_data, json_dumps_params={"ensure_ascii": False})

    except Exception as e:
        logger.error(f"Dashboard Data Error: {str(e)}")
        return JsonResponse({"error": "데이터를 불러오는 중 문제가 발생했습니다.", "details": str(e)}, status=500)


# ── 공통 헬퍼 함수 ────────────────────────────
def _make_response(request, category_key: str):
    """
    캐시에서 특정 카테고리 데이터를 꺼내 JSON으로 반환하는 공통 함수
    4개 카테고리 뷰가 모두 이 함수를 사용합니다
    """
    try:
        data   = get_cached_data()
        stocks = data["screens"].get(category_key, [])

        # rank 번호 추가 (1위, 2위, 3위...)
        for i, stock in enumerate(stocks, 1):
            stock["rank"] = i

        return JsonResponse({
            "category":   category_key,
            "count":      len(stocks),
            "updated_at": data.get("updated_at", ""),
            "stocks":     stocks,
        }, json_dumps_params={"ensure_ascii": False})

    except Exception as e:
        logger.error(f"[{category_key}] 오류: {str(e)}")
        return JsonResponse({"error": "데이터를 불러오는 중 문제가 발생했습니다.", "details": str(e)}, status=500)


# ── 4가지 카테고리 뷰 ─────────────────────────
def get_growth_stocks(request):
    """
    저평가 성장주
    GET /api/stocks/growth/
    조건: PER ≤ 20, ROE ≥ 10%
    """
    return _make_response(request, "growth_undervalued")


def get_value_stocks(request):
    """
    저렴한 가치주
    GET /api/stocks/value/
    조건: PBR ≤ 1.5, PER ≤ 15
    """
    return _make_response(request, "value_stock")


def get_dividend_stocks(request):
    """
    꾸준한 배당주
    GET /api/stocks/dividend/
    조건: 배당수익률 ≥ 3%, ROE ≥ 5%, PBR ≤ 3.0, PER ≤ 25
    """
    return _make_response(request, "dividend_stock")


def get_volume_stocks(request):
    """
    거래량 상위 10
    GET /api/stocks/volume/
    조건: 거래량 Top 10
    """
    return _make_response(request, "high_volume")