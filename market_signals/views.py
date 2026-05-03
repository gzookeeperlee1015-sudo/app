from django.http import JsonResponse

def get_market_dashboard_data(request):
    """
    프런트엔드(React) 메인 화면의 시장 신호 대시보드에 필요한 데이터를 반환하는 API입니다.
    추후 한국투자증권 Open API와 연동하여 실시간 데이터로 교체해야 합니다.
    """
    
    # UI 화면에 맞춰 하드코딩된 초기 Mock 데이터 
    dashboard_data = {
        # 1. 시장 신호 (신호등 상태: G=양호, Y=주의, R=매우주의)
        "market_signals": {
            "short_term": {"status": "Y", "label": "주의"},
            "long_term": {"status": "G", "label": "양호"}
        },
        
        # 2. 지수 및 상승 추세 정보
        "indices": {
            "kospi": {
                "name": "코스피",
                "price": "6,598.87",
                "change_percent": "-1.38%",
                "trend_status": "상승 추세",
                "exposure_guide": "80-100%",
                "distribution_day": 0,
                "last_follow_through_day": "2025.09.12",
                "advancing_issues": 196,
                "declining_issues": 668
            },
            "kosdaq": {
                "name": "코스닥",
                "price": "1,192.35",
                "change_percent": "-2.29%",
                "trend_status": "상승 추세",
                "exposure_guide": "80-100%",
                "distribution_day": 2,
                "last_follow_through_day": "2025.12.29",
                "advancing_issues": 419,
                "declining_issues": 1185
            }
        },
        
        # 3. 시장지표 (차트용 데이터) - 프런트의 TradingView Lightweight Charts 등에 사용
        "market_indicators": {
            "description": "20/200일선 하락비율, 52주 신고가/신저가, ADR 비율",
            "last_updated": "04/30 15:55",
            # 향후 이 부분에 날짜별 시계열 배열 데이터가 들어가야 합니다.
            "chart_data_endpoints": {
                "moving_average_ratio": "/api/signals/charts/ma-ratio/",
                "new_high_low": "/api/signals/charts/new-high-low/",
                "adr": "/api/signals/charts/adr/"
            }
        }
    }
    
    return JsonResponse(dashboard_data, json_dumps_params={'ensure_ascii': False})