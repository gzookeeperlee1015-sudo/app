class MarketAnalyzer:
    @staticmethod
    def calculate_signal(index_data):
        """
        상승/하락 종목 비율과 지수 변동을 분석하여 신호를 결정합니다.
        - 초록(양호): 상승 종목이 압도적일 때
        - 노랑(주의): 혼조세이거나 상승세가 둔화될 때
        - 빨강(위험): 하락 종목이 급증할 때
        """
        # API에서 받아온 실제 값을 대입하는 로직이 들어갑니다.
        # 예: 상승 종목 수 / 전체 종목 수 비율 계산
        advancing_ratio = 0.6  # 예시 데이터
        
        if advancing_ratio >= 0.6:
            return {"status": "Green", "message": "시장 건전성이 양호합니다. 적극적인 투자를 권장합니다."}
        elif advancing_ratio >= 0.4:
            return {"status": "Yellow", "message": "시장 변동성이 감지됩니다. 관망이 필요합니다."}
        else:
            return {"status": "Red", "message": "시장 하락 압력이 강합니다. 현금 비중을 높이세요."}