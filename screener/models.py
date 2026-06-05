from django.db import models

# 스크리너는 외부 API(yfinance, 네이버증권)에서 실시간으로 데이터를 가져오므로
# DB 모델 없이 운영합니다. cache_data.json이 캐시 역할을 합니다.
