"""
market_signals/urls.py
"""
from django.urls import path
from . import views

urlpatterns = [
    # 저평가 성장주 : PER ≤ 20, ROE ≥ 10%
    path('api/stocks/growth/',   views.get_growth_stocks,   name='growth_stocks'),

    # 저렴한 가치주 : PBR ≤ 1.5, PER ≤ 15
    path('api/stocks/value/',    views.get_value_stocks,    name='value_stocks'),

    # 꾸준한 배당주 : 배당수익률 ≥ 3%, ROE ≥ 5%, PBR ≤ 3.0, PER ≤ 25
    path('api/stocks/dividend/', views.get_dividend_stocks, name='dividend_stocks'),

    # 거래량 상위 10
    path('api/stocks/volume/',   views.get_volume_stocks,   name='volume_stocks'),
]