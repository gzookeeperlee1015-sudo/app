import logging
from django.http import JsonResponse
from .market_data import get_kis_market_data

logger = logging.getLogger(__name__)

def get_market_dashboard_data(request):
    try:
        real_data = get_kis_market_data()

        def safe_get(key, default="0.00"):
            return real_data.get(key, default)

        dashboard_data = {
            "market_signals": {
                "short_term": real_data.get("short_term_signal", {"label": "주의 (🟡)", "status": "Y"}),
                "long_term":  real_data.get("long_term_signal",  {"label": "양호 (🟢)", "status": "G"}),
            },
            "indices": {
                "kospi": {
                    "name":                    "코스피",
                    "price":                   safe_get("kospi_price"),
                    "change_percent":          safe_get("kospi_change"),
                    "change_price":            safe_get("kospi_diff", "0.00"),
                    "trend_status":            "상승 추세",
                    "exposure_guide":          "80-100%",
                    "distribution_day":        real_data.get("kospi_dist_day", 0),
                    "last_follow_through_day": "2025.09.12",
                    "is_up": float(safe_get("kospi_change").replace('%', '')) > 0
                        if isinstance(safe_get("kospi_change"), str) else False,
                },
                "kosdaq": {
                    "name":                    "코스닥",
                    "price":                   safe_get("kosdaq_price"),
                    "change_percent":          safe_get("kosdaq_change"),
                    "change_price":            safe_get("kosdaq_diff", "0.00"),
                    "trend_status":            "상승 추세",
                    "exposure_guide":          "80-100%",
                    "distribution_day":        real_data.get("kosdaq_dist_day", 2),
                    "last_follow_through_day": "2025.12.29",
                    "is_up": float(safe_get("kosdaq_change").replace('%', '')) > 0
                        if isinstance(safe_get("kosdaq_change"), str) else False,
                },
            },
            "last_updated": real_data.get("last_updated", "실시간"),
            
            "chart_data": real_data.get("chart_data", []),
            
            # 기존의 하드코딩 데이터를 지우고 동적 데이터로 연결합니다.
            "fifty_two_week_data": real_data.get("fifty_two_week_data", []),
        }
        return JsonResponse(dashboard_data, json_dumps_params={"ensure_ascii": False})

    except Exception as e:
        logger.error(f"Dashboard Data Error: {str(e)}")
        return JsonResponse({
            "error": "데이터를 불러오는 중 문제가 발생했습니다.",
            "details": str(e),
        }, status=500)
