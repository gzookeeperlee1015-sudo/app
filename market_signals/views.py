"""
market_signals/views.py

팀원 dashboard + 우리 4가지 카테고리 뷰
"""
import logging
from django.http import JsonResponse
from .services.cache import get_cached_data

logger = logging.getLogger(__name__)


# ── 팀원 대시보드 ──────────────────────────────
def get_market_dashboard_data(request):
    """
    대시보드 API
    KIS API 키 없을 때는 임시 더미 데이터 반환
    키 발급 후 services.py 연결하면 실시간 데이터로 전환 가능
    """
    try:
        # KIS API 키가 있으면 실시간 데이터 사용
        from .services import get_kis_market_data
        real_data = get_kis_market_data()

        def safe_get(key, default="0.00"):
            return real_data.get(key, default)

        dashboard_data = {
            "market_signals": {
                "short_term": real_data.get("short_term_signal", {"label": "주의", "status": "Y"}),
                "long_term":  real_data.get("long_term_signal",  {"label": "양호", "status": "G"}),
            },
            "indices": {
                "kospi": {
                    "name":           "코스피",
                    "price":          safe_get("kospi_price"),
                    "change_percent": safe_get("kospi_change"),
                    "change_price":   safe_get("kospi_diff", "0.00"),
                    "exposure_guide": "80-100%",
                    "is_up": float(safe_get("kospi_change").replace('%', '')) > 0
                        if isinstance(safe_get("kospi_change"), str) else False,
                },
                "kosdaq": {
                    "name":           "코스닥",
                    "price":          safe_get("kosdaq_price"),
                    "change_percent": safe_get("kosdaq_change"),
                    "change_price":   safe_get("kosdaq_diff", "0.00"),
                    "exposure_guide": "80-100%",
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
            "fifty_two_week_data": [
                {"date": "04-24", "high_ratio": 0.03, "low_ratio": 0.03},
                {"date": "07-03", "high_ratio": 0.08, "low_ratio": 0.03},
                {"date": "09-05", "high_ratio": 0.04, "low_ratio": 0.05},
                {"date": "11-14", "high_ratio": 0.06, "low_ratio": 0.04},
                {"date": "01-21", "high_ratio": 0.07, "low_ratio": 0.02},
                {"date": "04-01", "high_ratio": 0.05, "low_ratio": 0.03},
            ],
        }
        return JsonResponse(dashboard_data, json_dumps_params={"ensure_ascii": False})

    except Exception:
        # KIS API 키 없거나 오류 → 임시 더미 데이터
        return JsonResponse({
            "market_signals": {
                "short_term": {"label": "주의", "status": "Y"},
                "long_term":  {"label": "양호", "status": "G"},
            },
            "indices": {
                "kospi":  {"name": "코스피", "price": "2500.00", "change_percent": "0.5%",
                           "change_price": "12.5", "exposure_guide": "80-100%", "is_up": True},
                "kosdaq": {"name": "코스닥", "price": "750.00",  "change_percent": "0.3%",
                           "change_price": "2.3",  "exposure_guide": "80-100%", "is_up": True},
            },
            "last_updated": "",
            "chart_data": [
                {"date": "03-01", "kospi": 2600, "ma20": 0.2, "ma200": 0.4,  "adr": 80},
                {"date": "03-08", "kospi": 2620, "ma20": 0.3, "ma200": 0.38, "adr": 95},
                {"date": "03-15", "kospi": 2680, "ma20": 0.6, "ma200": 0.45, "adr": 110},
                {"date": "03-22", "kospi": 2650, "ma20": 0.5, "ma200": 0.42, "adr": 100},
                {"date": "03-29", "kospi": 2750, "ma20": 0.8, "ma200": 0.5,  "adr": 120},
            ],
            "fifty_two_week_data": [
                {"date": "04-24", "high_ratio": 0.03, "low_ratio": 0.03},
                {"date": "07-03", "high_ratio": 0.08, "low_ratio": 0.03},
                {"date": "09-05", "high_ratio": 0.04, "low_ratio": 0.05},
                {"date": "11-14", "high_ratio": 0.06, "low_ratio": 0.04},
                {"date": "01-21", "high_ratio": 0.07, "low_ratio": 0.02},
                {"date": "04-01", "high_ratio": 0.05, "low_ratio": 0.03},
            ],
        }, json_dumps_params={"ensure_ascii": False})


# ── 공통 헬퍼 ─────────────────────────────────
def _make_response(request, category_key: str):
    try:
        data   = get_cached_data()
        stocks = data.get("screens", {}).get(category_key, [])
        for i, stock in enumerate(stocks, 1):
            stock["rank"] = i
        return JsonResponse({
            "category":   category_key,
            "count":      len(stocks),
            "total":      data.get("total", 0),
            "updated_at": data.get("updated_at", ""),
            "stocks":     stocks,
        }, json_dumps_params={"ensure_ascii": False})
    except Exception as e:
        logger.error(f"[{category_key}] 오류: {e}")
        return JsonResponse({"error": "데이터를 불러오는 중 문제가 발생했습니다.", "details": str(e)}, status=500)


# ── 4가지 카테고리 뷰 ─────────────────────────
def get_growth_stocks(request):
    """저평가 성장주 - GET /api/stocks/growth/"""
    return _make_response(request, "growth_undervalued")

def get_value_stocks(request):
    """저렴한 가치주 - GET /api/stocks/value/"""
    return _make_response(request, "value_stock")

def get_week52_high_stocks(request):
    """52주 신고가 근접 - GET /api/stocks/week52/"""
    return _make_response(request, "week52_high")

def get_volume_stocks(request):
    """거래량 상위 10 - GET /api/stocks/volume/"""
    return _make_response(request, "high_volume")