class MarketAnalyzer:
    def __init__(self):
        # 지표별 가중치 설정 (총합 100)
        self.weights = {
            "adr": 40,
            "high_low": 30,
            "moving_avg": 30
        }

    def analyze(self, raw_data):
        """
        KIS API 응답 데이터를 뜯어서 최종 점수를 산출합니다.[cite: 1]
        """
        try:
            # 1. 데이터 추출 (API 응답 필드 기준)
            output = raw_data.get("output", {})
            inc_cnt = int(output.get("ascn_issu_cnt", 0))   # 상승 종목 수
            dec_cnt = int(output.get("dwn_issu_cnt", 1))    # 하락 종목 수
            
            # 2. 지표별 점수 계산
            # (1) ADR 점수 계산
            adr_value = (inc_cnt / dec_cnt) * 100
            # 여기서 self._get_adr_score를 호출합니다.
            adr_score = self._get_adr_score(adr_value)

            # (2) 신고가 비율 (현재 데이터 부재 시 기본값 50점)[cite: 1]
            hl_score = 50 

            # (3) 이동평균선 점수 (기본값 50점)[cite: 1]
            ma_score = 50 

            # 3. 최종 가중치 합산
            total_score = (
                (adr_score * self.weights["adr"] / 100) +
                (hl_score * self.weights["high_low"] / 100) +
                (ma_score * self.weights["moving_avg"] / 100)
            )

            return self._determine_signal(total_score)
        
        except Exception as e:
            print(f"분석 로직 에러: {e}")
            return {"color": "Gray", "label": "데이터 분석 중", "message": "실시간 데이터를 분석하고 있습니다."}

    # --- 여기서부터는 클래스 내부의 헬퍼 함수들입니다. 인덴트(들여쓰기)를 꼭 맞추세요! ---

    def _get_adr_score(self, adr):
        """ADR 값에 따른 점수화[cite: 1]"""
        if adr >= 120: return 100
        elif adr >= 100: return 80
        elif adr >= 75: return 50
        else: return 20

    def _determine_signal(self, score):
        """최종 점수에 따른 신호등 결정[cite: 1]"""
        if score >= 70:
            return {"color": "Green", "label": "양호", "exposure": "80-100%", "message": "적극적 투자 권장"}
        elif score >= 40:
            return {"color": "Yellow", "label": "주의", "exposure": "40-60%", "message": "시장 변동성 주의"}
        else:
            return {"color": "Red", "label": "매우 주의", "exposure": "0-20%", "message": "현금 비중 확대 권고"}