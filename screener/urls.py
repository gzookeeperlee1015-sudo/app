from django.urls import path
from . import views

urlpatterns = [
    path('api/stocks/growth/', views.get_growth_stocks,      name='growth_stocks'),
    path('api/stocks/value/',  views.get_value_stocks,       name='value_stocks'),
    path('api/stocks/week52/', views.get_week52_high_stocks, name='week52_stocks'),
    path('api/stocks/volume/', views.get_volume_stocks,      name='volume_stocks'),
]
