# market_signals/views.py
from django.http import JsonResponse
from .services import get_kis_market_data

def get_market_dashboard_data(request):
    try:
        # services.py를 호출하여 KIS 실시간 데이터를 가져옵니다!
        real_data = get_kis_market_data()
        
        dashboard_data = {
            "market_signals": {
                "short_term": real_data["short_term_signal"],
                "long_term": real_data["long_term_signal"]
            },
            "indices": {
                "kospi": {
                    "name": "코스피",
                    "price": real_data["kospi_price"],          # KIS 실시간 데이터 맵핑!
                    "change_percent": real_data["kospi_change"],# KIS 실시간 데이터 맵핑!
                    "trend_status": "상승 추세",
                    "exposure_guide": "80-100%",
                    "distribution_day": 0,
                    "last_follow_through_day": "2025.09.12"
                },
                "kosdaq": {
                    "name": "코스닥",
                    "price": real_data["kosdaq_price"],         # KIS 실시간 데이터 맵핑!
                    "change_percent": real_data["kosdaq_change"],# KIS 실시간 데이터 맵핑!
                    "trend_status": "상승 추세",
                    "exposure_guide": "80-100%",
                    "distribution_day": 2,
                    "last_follow_through_day": "2025.12.29"
                }
            }
        }
        
        return JsonResponse(dashboard_data, json_dumps_params={'ensure_ascii': False})
        
    except Exception as e:
        # 혹시 API 통신에 문제가 생기면 에러 메시지를 보여줍니다.
        return JsonResponse({"error": str(e)}, status=500)