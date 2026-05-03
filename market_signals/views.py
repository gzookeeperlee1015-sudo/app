from django.http import JsonResponse
from .services import get_kis_market_data
import logging

# 에러 로그 기록을 위해 설정
logger = logging.getLogger(__name__)

def get_market_dashboard_data(request):
    try:
        # services.py를 통해 KIS 실시간 데이터를 가져옵니다.
        real_data = get_kis_market_data()
        
        # 데이터가 비어있을 경우를 대비한 기본값 처리 (에러 방지)
        def safe_get(key, default="0.00"):
            return real_data.get(key, default)

        # 프론트엔드 UI(image_0a7067.png 및 차트)에 필요한 모든 정보를 구조화합니다.
        dashboard_data = {
            "market_signals": {
                "short_term": real_data.get("short_term_signal", {"label": "데이터 없음", "status": "G"}),
                "long_term": real_data.get("long_term_signal", {"label": "데이터 없음", "status": "G"})
            },
            "indices": {
                "kospi": {
                    "name": "코스피",
                    "price": safe_get("kospi_price"), # 현재가
                    "change_percent": safe_get("kospi_change"), # 변동률
                    "change_price": safe_get("kospi_diff", "0.00"), # 변동폭
                    "trend_status": "상승 추세",
                    "exposure_guide": "80-100%",
                    "distribution_day": real_data.get("kospi_dist_day", 0),
                    "last_follow_through_day": "2025.09.12",
                    "is_up": float(safe_get("kospi_change").replace('%', '')) > 0 if isinstance(safe_get("kospi_change"), str) else False
                },
                "kosdaq": {
                    "name": "코스닥",
                    "price": safe_get("kosdaq_price"),
                    "change_percent": safe_get("kosdaq_change"),
                    "change_price": safe_get("kosdaq_diff", "0.00"),
                    "trend_status": "상승 추세",
                    "exposure_guide": "80-100%",
                    "distribution_day": real_data.get("kosdaq_dist_day", 2),
                    "last_follow_through_day": "2025.12.29",
                    "is_up": float(safe_get("kosdaq_change").replace('%', '')) > 0 if isinstance(safe_get("kosdaq_change"), str) else False
                }
            },
            "last_updated": real_data.get("last_updated", "실시간"), # 마지막 업데이트 시간
            
            # 👇 [새로 추가된 부분] 프론트엔드 차트를 그리기 위한 시계열 데이터
            "chart_data": [
                { "date": "03-01", "kospi": 2600, "ma20": 0.2, "ma200": 0.4, "adr": 80 },
                { "date": "03-08", "kospi": 2620, "ma20": 0.3, "ma200": 0.38, "adr": 95 },
                { "date": "03-15", "kospi": 2680, "ma20": 0.6, "ma200": 0.45, "adr": 110 },
                { "date": "03-22", "kospi": 2650, "ma20": 0.5, "ma200": 0.42, "adr": 100 },
                { "date": "03-29", "kospi": 2750, "ma20": 0.8, "ma200": 0.5, "adr": 120 },
            ]
        }
        
        return JsonResponse(dashboard_data, json_dumps_params={'ensure_ascii': False})
        
    except Exception as e:
        # 에러 발생 시 로그를 남기고 클라이언트에게 에러를 알립니다.
        logger.error(f"Dashboard Data Error: {str(e)}")
        return JsonResponse({
            "error": "데이터를 불러오는 중 문제가 발생했습니다.",
            "details": str(e)
        }, status=500)