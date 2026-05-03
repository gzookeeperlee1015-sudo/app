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
        KIS API 응답 데이터를 뜯어서 최종 점수를 산출합니다.
        """
        # 1. 데이터 추출 (API 응답 구조에 맞게 파싱)
        # stck_prpr: 현재 지수, bstp_nmix_prdy_ctrt: 등락률
        # ascn_issu_cnt: 상승 종목 수, dwn_issu_cnt: 하락 종목 수
        
        inc_cnt = int(raw_data.get("ascn_issu_cnt", 0))
        dec_cnt = int(raw_data.get("dwn_issu_cnt", 1)) # 0 나누기 방지
        
        # 2. 지표 계산
        adr = (inc_cnt / dec_cnt) * 100
        
        # 3. 점수화 (0~100점 스케일링)
        adr_score = self._get_adr_score(adr)
        
        # 4. 최종 가중치 합산
        total_score = (adr_score * (self.weights["adr"] / 100))
        # (나머지 지표들도 동일하게 합산...)

        return self._determine_signal(total_score)

    def _determine_signal(self, score):
        """최종 점수에 따른 신호등 결정[cite: 1]"""
        if score >= 70:
            return {"color": "Green", "label": "양호", "exposure": "80-100%"}
        elif score >= 40:
            return {"color": "Yellow", "label": "주의", "exposure": "40-60%"}
        else:
            return {"color": "Red", "label": "매우 주의", "exposure": "0-20%"}