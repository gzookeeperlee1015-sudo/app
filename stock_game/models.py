from django.db import models


class Player(models.Model):
    """
    플레이어 모델
    - 닉네임으로 사용자를 구분
    - 게임을 거듭할수록 누적 자산이 쌓임
    """
    nickname = models.CharField(max_length=20, unique=True)  # 닉네임 (고유값)
    balance = models.BigIntegerField(default=10000000)        # 현재 보유 자산 (기본 1000만원)
    created_at = models.DateTimeField(auto_now_add=True)      # 최초 생성일
    updated_at = models.DateTimeField(auto_now=True)          # 마지막 업데이트일

    def __str__(self):
        return f"{self.nickname} ({self.balance:,}원)"


class GameResult(models.Model):
    """
    게임 결과 모델
    - 한 판이 끝날 때마다 결과를 저장
    - 플레이어의 누적 자산 변화 기록
    """
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='results')
    # on_delete=CASCADE: 플레이어 삭제 시 관련 결과도 함께 삭제

    ticker = models.CharField(max_length=20)          # 플레이한 종목 티커 (예: 005930.KS)
    stock_name = models.CharField(max_length=20)      # 종목 한글명 (예: 삼성전자)
    start_balance = models.BigIntegerField()          # 게임 시작 시 자산
    end_balance = models.BigIntegerField()            # 게임 종료 시 자산
    profit = models.BigIntegerField()                 # 수익금 (end - start, 음수 가능)
    profit_rate = models.FloatField()                 # 수익률 (%)
    played_at = models.DateTimeField(auto_now_add=True)  # 게임 플레이 일시

    def __str__(self):
        return f"{self.player.nickname} | {self.stock_name} | {self.profit:+,}원"
