from django.urls import path
from . import views

urlpatterns = [
    # 대시보드 (팀원 코드)
    path('api/dashboard/',       views.get_market_dashboard_data, name='market_dashboard'),

    # 저평가 성장주
    path('api/stocks/growth/',   views.get_growth_stocks,         name='growth_stocks'),

    # 저렴한 가치주
    path('api/stocks/value/',    views.get_value_stocks,          name='value_stocks'),

    # 52주 신고가 근접
    path('api/stocks/week52/',   views.get_week52_high_stocks,    name='week52_stocks'),

    # 거래량 상위 10
    path('api/stocks/volume/',   views.get_volume_stocks,         name='volume_stocks'),
]