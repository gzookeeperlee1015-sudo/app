import React, { useState } from 'react';
import axios from 'axios';
import './AiInsight.css';
import { useNavigate } from 'react-router-dom';
import { TrendingUp, Sparkles, Loader2, ArrowLeft, BarChart3 } from 'lucide-react';

function AiInsight() {
  const navigate = useNavigate();

  const [ticker, setTicker]           = useState('');
  const [report, setReport]           = useState('');
  const [financialData, setFinancialData] = useState(null);
  const [loading, setLoading]         = useState(false);
  const [error, setError]             = useState('');

  const handleAnalyze = async (e) => {
    e.preventDefault();
    if (!ticker.trim()) return;

    setLoading(true);
    setError('');
    setReport('');
    setFinancialData(null);

    try {
      const response = await axios.post('http://127.0.0.1:8000/api/ai/analyze/', {
        ticker: ticker.toUpperCase()
      });

      const data = response.data;
      // 백엔드는 { ai_report, financial_data, ticker, sentiment } 반환
      if (data && data.ai_report) {
        setReport(data.ai_report);
        setFinancialData(data.financial_data || null);
      } else {
        setError('리포트 데이터를 받아오지 못했습니다.');
      }
    } catch (err) {
      console.error(err);
      setError('AI 분석 중 오류가 발생했습니다. 티커를 확인하거나 잠시 후 다시 시도해주세요.');
    } finally {
      setLoading(false);
    }
  };

  // 재무 지표 라벨 매핑
  const financialLabels = {
    market: '시장',
    market_cap: '시가총액',
    high_250: '52주 최고가',
    low_250: '52주 최저가',
    per: 'PER',
    pbr: 'PBR',
    roe: 'ROE',
    eps: 'EPS',
    bps: 'BPS',
    revenue: '매출액',
    operating_income: '영업이익',
    net_income: '당기순이익',
  };

  return (
    <div className="min-h-screen bg-[#F8F9FB] p-6 md:p-12 font-sans text-slate-900">
      <div className="max-w-6xl mx-auto">

        {/* 헤더 */}
        <header className="flex flex-col lg:flex-row justify-between items-start lg:items-center mb-12 gap-6">
          <div>
            <div className="flex items-center gap-2 mb-1 cursor-pointer" onClick={() => navigate('/')}>
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                <TrendingUp className="text-white w-5 h-5" />
              </div>
              <h1 className="text-2xl font-black tracking-tighter text-slate-900 uppercase">
                Stock<span className="text-blue-600">Easy</span>{' '}
                <span className="text-slate-300 font-light">|</span>{' '}
                <span className="italic text-slate-500 text-lg">AI</span>
              </h1>
            </div>
            <p className="text-slate-400 text-[10px] font-bold ml-10 uppercase tracking-widest leading-none">
              Generative Investment Insights
            </p>
          </div>
          <div className="flex items-center gap-8">
            <button
              onClick={() => navigate('/')}
              className="text-slate-400 hover:text-blue-600 font-black text-sm flex items-center gap-2 transition-colors duration-200 uppercase tracking-wider"
            >
              <ArrowLeft className="w-4 h-4" /> 메인 대시보드
            </button>
          </div>
        </header>

        {/* 메인 카드 */}
        <div className="bg-white p-8 md:p-12 rounded-[2rem] border border-slate-100 shadow-sm overflow-hidden mb-8">
          <div className="mb-10">
            <div className="flex items-center gap-2 mb-2">
              <span className="bg-blue-600 text-white px-3 py-1 rounded-md text-[10px] font-black uppercase tracking-tighter">AI AGENT</span>
              <span className="text-slate-400 text-[10px] font-bold italic">DEEP ANALYSIS</span>
            </div>
            <h3 className="text-3xl font-black text-slate-900 tracking-tighter">🤖 EasyMoney AI Insight</h3>
            <p className="text-slate-500 font-medium text-sm mt-2 leading-relaxed">
              원하는 주식 종목의 티커(예: 삼성전자 <span className="font-bold text-blue-600">005930</span>, 테슬라 <span className="font-bold text-blue-600">TSLA</span>)를 입력하세요.<br />
              Google Gemini 모델이 재무 데이터와 실시간 뉴스를 결합하여 전문가 수준의 리포트를 즉시 발간합니다.
            </p>
          </div>

          {/* 검색 폼 */}
          <form onSubmit={handleAnalyze} className="flex flex-col sm:flex-row gap-4 mb-8 max-w-xl">
            <input
              type="text"
              value={ticker}
              onChange={(e) => setTicker(e.target.value)}
              placeholder="종목 코드 또는 티커 입력 (ex. TSLA, 005930)"
              disabled={loading}
              className="flex-1 bg-slate-50 border border-slate-200 px-6 py-4 rounded-2xl text-slate-800 placeholder-slate-400 font-semibold focus:outline-none focus:border-blue-500 transition-all text-sm shadow-inner"
            />
            <button
              type="submit"
              disabled={loading}
              className="bg-slate-900 hover:bg-blue-600 text-white font-black px-8 py-4 rounded-2xl flex items-center justify-center gap-2 transition-all duration-200 shadow-sm disabled:bg-slate-200 text-sm tracking-wider uppercase"
            >
              {loading ? (
                <><Loader2 className="w-4 h-4 animate-spin" /> 분석 중...</>
              ) : (
                <><Sparkles className="w-4 h-4" /> 리포트 발간</>
              )}
            </button>
          </form>

          {/* 에러 */}
          {error && (
            <div className="bg-red-50 border border-red-100 text-red-600 px-6 py-4 rounded-2xl text-sm font-bold flex items-center gap-3 mb-6">
              <span>⚠️</span> {error}
            </div>
          )}

          {/* 재무 지표 그리드 */}
          {financialData && (
            <div className="mt-8 border-t border-slate-100 pt-8">
              <div className="flex items-center gap-2 mb-4">
                <BarChart3 className="w-5 h-5 text-blue-600" />
                <h4 className="text-lg font-black tracking-tighter text-slate-900">📊 핵심 재무 지표</h4>
              </div>
              <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3 mb-8">
                {Object.entries(financialLabels).map(([key, label]) =>
                  financialData[key] ? (
                    <div key={key} className="bg-slate-50 rounded-2xl px-4 py-3 border border-slate-100">
                      <p className="text-[10px] font-black text-slate-400 uppercase tracking-wider mb-1">{label}</p>
                      <p className="text-sm font-black text-slate-800">{financialData[key]}</p>
                    </div>
                  ) : null
                )}
              </div>
            </div>
          )}

          {/* AI 리포트 본문 */}
          {report && (
            <div className={financialData ? '' : 'mt-8 border-t border-slate-100 pt-8'}>
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-blue-600 animate-ping" />
                  <h4 className="text-xl font-black tracking-tighter text-slate-900">✨ AI 정밀 분석 보고서</h4>
                </div>
                <span className="text-[11px] font-black text-slate-400 bg-slate-100 px-3 py-1 rounded-full uppercase">Verified Document</span>
              </div>
              <div className="bg-[#FAFAFB] border border-slate-100 rounded-3xl p-6 md:p-8 text-slate-800 leading-relaxed font-medium text-sm shadow-inner whitespace-pre-wrap">
                {report}
              </div>
            </div>
          )}

          {/* 초기 빈 상태 */}
          {!loading && !report && !error && (
            <div className="border border-dashed border-slate-200 rounded-3xl p-12 text-center mt-4">
              <Sparkles className="w-8 h-8 text-slate-300 mx-auto mb-3" />
              <p className="text-slate-400 text-xs font-bold uppercase tracking-wider">Awaiting Analysis Request</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default AiInsight;
