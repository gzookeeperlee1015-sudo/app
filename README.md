# -
EasyMoney (이지머니)"Financial Data Made Easy" – 복잡한 금융 데이터를 정제하여 직관적인 인사이트를 전달하는 투자 입문 보조 플랫폼
1.  프로젝트 개요 (Introduction)초보 투자자들이 겪는 심리적 진입 장벽과 정보의 불균형을 해소하기 위한 웹 기반 통합 투자 가이드 플랫폼입니다. 단순한 정보 나열이 아닌, 가상 트레이딩 게임과 AI 기반 시장 분석을 결합하여 '근거 있는 투자'를 돕습니다.
  
2. 주요 기능 (Key Features) Back-Testing GameTradingView Lightweight Charts를 커스텀하여 과거 특정 구간의 실시간 캔들 차트 구현사용자의 가상 매수/매도 시점에 따른 수익률을 실시간으로 계산하여 투자 감각 배양 Market Signal Display한국투자증권 API를 통한 실시간 데이터 수신 및 가공'양호(초록)', '주의(노랑)', '매우 주의(빨강)'의 신호등 UI를 통해 시장 시황을 직관적으로 파악 AI Insight ReportGemini Pro / GPT-4o 연동을 통한 종목별 뉴스 감성 분석(Sentiment Analysis)현직 애널리스트의 사고 프레임워크를 적용한 재무 건전성 요약 보고서 자동 생성 Smart Listing테마별/조건별(52주 신고가, RSI 70 이상 등) 종목 자동 분류시장을 주도하는 핵심 대장주 리스트를 즉각적으로 포착

3.  기술 스택 (Tech Stack)구분기술FrontendReact.js, TradingView Lightweight Charts, CSS ModulesBackendPython, FastAPI, Redis (Caching)AI/LLMGemini Pro API, GPT-4o APIData API한국투자증권 Open API, FinanceDataReaderDevOpsGitHub, Git LFS

    역할담당
  윤종빈
   -Data & FE종목 데이터 분석 및 파이프라인 설계, 리스트 프로그램 구현
  이현구
   -Game & FE과거 차트 트레이딩 게임 로직 설계 및 인터랙티브 UI 개발
  이정준
   -Algorithm & FE시장 신호 분석 알고리즘 설계 및 대시보드 시각화 최적화
  정준영
   -AI & UXLLM 기반 인사이트 모델 통합 및 메인 인터페이스 총괄
