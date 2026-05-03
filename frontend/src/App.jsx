import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { TrendingUp, Activity, BarChart3, AlertCircle, CheckCircle2 } from 'lucide-react';
// 👇 새로 추가된 차트 라이브러리
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    // 10초마다 데이터를 갱신하여 실시간 대시보드 구현
    const fetchData = () => {
      axios.get('http://127.0.0.1:8000/api/dashboard/')
        .then(res => setData(res.data))
        .catch(err => console.error("데이터 로드 실패:", err));
    };

    fetchData();
    const interval = setInterval(fetchData, 10000); // 10초 주기
    return () => clearInterval(interval);
  }, []);

  // 데이터 로딩 중 화면
  if (!data) return (
    <div className="min-h-screen flex items-center justify-center bg-[#F8F9FB]">
      <div className="flex flex-col items-center gap-4">
        <div className="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin" />
        <div className="text-slate-400 font-bold tracking-tighter">EasyMoney Engine Loading...</div>
      </div>
    </div>
  );

  // 상승/하락 여부에 따른 색상 결정 함수
  const getStockColor = (val) => {
    const num = parseFloat(val);
    if (num > 0) return 'text-red-500';
    if (num < 0) return 'text-blue-500';
    return 'text-slate-500';
  };

  return (
    <div className="min-h-screen bg-[#F8F9FB] p-6 md:p-12 font-sans text-slate-900">
      <div className="max-w-6xl mx-auto">
        
        {/* 헤더 섹션: StockEasy 스타일의 상단 바 */}
        <header className="flex flex-col md:flex-row justify-between items-start md:items-center mb-12 gap-6">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                <TrendingUp className="text-white w-5 h-5" />
              </div>
              <h1 className="text-2xl font-black tracking-tighter text-slate-900">
                Stock<span className="text-blue-600">Easy</span> <span className="text-slate-300 font-light">|</span> <span className="italic text-slate-500 text-lg">ASFE</span>
              </h1>
            </div>
            <p className="text-slate-400 text-xs font-semibold ml-10">QUANTITATIVE ANALYSIS ENGINE</p>
          </div>

          {/* 시장 신호 알림창 */}
          <div className="flex items-center space-x-4 bg-white px-6 py-3 rounded-2xl shadow-sm border border-slate-100">
            <div className="flex flex-col items-end border-r pr-4 border-slate-100">
              <span className="text-[10px] font-bold text-slate-400 uppercase">Market Signal</span>
              <span className="text-sm font-black text-slate-700">{data.market_signals.short_term.label}</span>
            </div>
            <div className="pl-1">
              {data.market_signals.short_term.status === 'R' ? (
                <AlertCircle className="text-red-500 w-6 h-6 animate-pulse" />
              ) : (
                <CheckCircle2 className="text-emerald-500 w-6 h-6" />
              )}
            </div>
          </div>
        </header>

        {/* 지수 카드 섹션: 그리드 배치 최적화 */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* 코스피 카드 */}
          <div className="group bg-white p-8 rounded-[2rem] shadow-sm hover:shadow-xl transition-all duration-300 border border-slate-100 relative overflow-hidden">
            <div className="absolute top-0 right-0 p-8 opacity-5 group-hover:opacity-10 transition-opacity">
              <Activity size={120} />
            </div>
            <div className="flex justify-between items-center mb-8">
              <div className="flex items-center gap-2">
                <span className="bg-slate-900 text-white px-3 py-1 rounded-md text-[10px] font-black uppercase tracking-tighter">KOSPI</span>
                <span className="text-slate-400 text-[10px] font-bold italic underline decoration-blue-500/30">REAL-TIME</span>
              </div>
              <div className={`flex flex-col items-end ${getStockColor(data.indices.kospi.change_percent)}`}>
                <span className="text-lg font-black">{data.indices.kospi.change_percent}</span>
                <span className="text-[10px] font-bold">{data.indices.kospi.is_up ? '▲' : '▼'} {data.indices.kospi.change_price}</span>
              </div>
            </div>
            <div className="text-6xl font-black text-slate-900 mb-4 tracking-tighter">
              {data.indices.kospi.price}
            </div>
            <div className="flex items-center gap-2 text-emerald-500 bg-emerald-50 w-fit px-3 py-1 rounded-full">
              <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-ping" />
              <span className="text-[10px] font-black uppercase tracking-widest">Market Index Connected</span>
            </div>
          </div>

          {/* 코스닥 카드 */}
          <div className="group bg-white p-8 rounded-[2rem] shadow-sm hover:shadow-xl transition-all duration-300 border border-slate-100 relative overflow-hidden">
            <div className="absolute top-0 right-0 p-8 opacity-5 group-hover:opacity-10 transition-opacity">
              <BarChart3 size={120} />
            </div>
            <div className="flex justify-between items-center mb-8">
              <div className="flex items-center gap-2">
                <span className="bg-blue-600 text-white px-3 py-1 rounded-md text-[10px] font-black uppercase tracking-tighter">KOSDAQ</span>
                <span className="text-slate-400 text-[10px] font-bold italic underline decoration-blue-500/30">REAL-TIME</span>
              </div>
              <div className={`flex flex-col items-end ${getStockColor(data.indices.kosdaq.change_percent)}`}>
                <span className="text-lg font-black">{data.indices.kosdaq.change_percent}</span>
                <span className="text-[10px] font-bold">{data.indices.kosdaq.is_up ? '▲' : '▼'} {data.indices.kosdaq.change_price}</span>
              </div>
            </div>
            <div className="text-6xl font-black text-slate-900 mb-4 tracking-tighter">
              {data.indices.kosdaq.price}
            </div>
            <div className="flex items-center gap-2 text-emerald-500 bg-emerald-50 w-fit px-3 py-1 rounded-full">
              <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-ping" />
              <span className="text-[10px] font-black uppercase tracking-widest">Market Index Connected</span>
            </div>
          </div>
        </div>

        {/* 하단 점수/가이드 섹션 */}
        <div className="bg-white p-8 rounded-[2rem] border border-slate-100 flex flex-col md:flex-row items-center justify-between gap-6 mb-8">
          <div className="flex flex-col text-center md:text-left">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Current Strategy Score</span>
            <h3 className="text-xl font-black text-slate-800">시장 주도주 분석 결과</h3>
          </div>
          <div className="flex items-center gap-8">
            <div className="text-center">
              <div className="text-3xl font-black text-emerald-500">{data.indices.kospi.exposure_guide}</div>
              <div className="text-[10px] font-bold text-slate-400">권장 비중</div>
            </div>
            <div className="h-10 w-[1px] bg-slate-100 hidden md:block" />
            <button className="bg-slate-900 text-white px-8 py-3 rounded-xl text-xs font-black hover:bg-blue-600 transition-colors shadow-lg shadow-slate-200">
              상세 전략 리포트 보기
            </button>
          </div>
        </div>

        {/* 🚀 백엔드 API에서 받아온 진짜 데이터로 그리는 차트 섹션 */}
        {data.chart_data && (
          <div className="bg-white p-8 rounded-[2rem] border border-slate-100 shadow-sm">
            <div className="mb-6">
              <h3 className="text-xl font-black text-slate-800">20일선 / 200일선 이격비율 & KOSPI</h3>
              <p className="text-xs font-bold text-slate-400 mt-1">시장 중장기 추세 분석</p>
            </div>
            
            <div className="h-[400px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                {/* data={data.chart_data}를 통해 백엔드 데이터와 차트를 직접 연결합니다. */}
                <LineChart data={data.chart_data} margin={{ top: 5, right: 20, left: 20, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
                  <XAxis dataKey="date" tick={{ fill: '#94a3b8', fontSize: 12 }} axisLine={false} tickLine={false} />
                  
                  {/* 왼쪽 축: 코스피 지수용 (자동 스케일 조정) */}
                  <YAxis yAxisId="left" domain={['auto', 'auto']} tick={{ fill: '#3b82f6', fontSize: 12 }} axisLine={false} tickLine={false} />
                  {/* 오른쪽 축: 비율(%)용 (자동 스케일 조정) */}
                  <YAxis yAxisId="right" domain={['auto', 'auto']} orientation="right" tick={{ fill: '#22c55e', fontSize: 12 }} axisLine={false} tickLine={false} />
                  
                  <Tooltip contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
                  <Legend wrapperStyle={{ paddingTop: '20px', fontSize: '12px', fontWeight: 'bold' }} />
                  
                  {/* 실제 그래프 선 그리기 */}
                  <Line yAxisId="left" type="monotone" dataKey="kospi" name="KOSPI" stroke="#3b82f6" strokeWidth={3} dot={false} />
                  <Line yAxisId="right" type="monotone" dataKey="ma20" name="20일선 하락비율" stroke="#f97316" strokeWidth={2} dot={false} />
                  <Line yAxisId="right" type="monotone" dataKey="ma200" name="200일선 하락비율" stroke="#22c55e" strokeWidth={2} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}

      </div>
    </div>
  );
}

export default App;