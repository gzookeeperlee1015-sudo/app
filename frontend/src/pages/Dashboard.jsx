import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { TrendingUp, Activity, BarChart3, AlertCircle, CheckCircle2, BarChart2 } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { useNavigate } from 'react-router-dom';

function Dashboard() {
  const navigate = useNavigate();
  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchData = () => {
      axios.get('http://127.0.0.1:8000/api/dashboard/')
        .then(res => setData(res.data))
        .catch(err => console.error("데이터 로드 실패:", err));
    };

    fetchData();
    const interval = setInterval(fetchData, 10000);
    return () => clearInterval(interval);
  }, []);

  if (!data) return (
    <div className="min-h-screen flex items-center justify-center bg-[#F8F9FB]">
      <div className="flex flex-col items-center gap-4">
        <div className="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin" />
        <div className="text-slate-400 font-bold tracking-tighter text-lg">EasyMoney Engine Loading...</div>
      </div>
    </div>
  );

  const getStockColor = (val) => {
    const num = parseFloat(val);
    if (num > 0) return 'text-red-500';
    if (num < 0) return 'text-blue-500';
    return 'text-slate-500';
  };

  const getSignalConfig = (status) => {
    switch (status) {
      case 'G': return { color: 'text-emerald-500', bg: 'bg-emerald-50', icon: <CheckCircle2 className="w-5 h-5" /> };
      case 'Y': return { color: 'text-amber-500',   bg: 'bg-amber-50',   icon: <AlertCircle className="w-5 h-5" /> };
      case 'R': return { color: 'text-red-500',     bg: 'bg-red-50',     icon: <AlertCircle className="w-5 h-5 animate-pulse" /> };
      default:  return { color: 'text-slate-300',   bg: 'bg-slate-50',   icon: <Activity className="w-5 h-5" /> };
    }
  };

  const shortTerm = getSignalConfig(data.market_signals.short_term.status);
  const longTerm  = getSignalConfig(data.market_signals.long_term.status);

  return (
    <div className="min-h-screen bg-[#F8F9FB] p-6 md:p-12 font-sans text-slate-900">
      <div className="max-w-6xl mx-auto">

        {/* 헤더 */}
        <header className="flex flex-col lg:flex-row justify-between items-start lg:items-center mb-12 gap-6">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                <TrendingUp className="text-white w-5 h-5" />
              </div>
              <h1 className="text-2xl font-black tracking-tighter text-slate-900 uppercase">
                Stock<span className="text-blue-600">Easy</span> <span className="text-slate-300 font-light">|</span> <span className="italic text-slate-500 text-lg">ASFE</span>
              </h1>
            </div>
            <p className="text-slate-400 text-[10px] font-bold ml-10 uppercase tracking-widest leading-none">Quantitative Market Analysis</p>
          </div>

          <div className="flex items-center gap-4">
            {/* 시장 신호 */}
            <div className="flex items-center gap-4 bg-white p-2 pr-6 rounded-2xl shadow-sm border border-slate-100">
              <div className="bg-slate-900 text-white px-4 py-3 rounded-xl flex flex-col justify-center">
                <span className="text-[10px] font-black opacity-60 leading-tight uppercase">Market</span>
                <span className="text-xs font-black tracking-tighter">SIGNAL</span>
              </div>
              <div className="flex gap-8 items-center ml-2">
                <div className="flex items-center gap-3">
                  <div className="flex flex-col text-right">
                    <span className="text-[9px] font-bold text-slate-400 uppercase tracking-tighter">Short-term</span>
                    <span className="text-xs font-black text-slate-700">단기</span>
                  </div>
                  <div className={`p-2 rounded-full ${shortTerm.bg} ${shortTerm.color}`}>{shortTerm.icon}</div>
                </div>
                <div className="w-[1px] h-8 bg-slate-100" />
                <div className="flex items-center gap-3">
                  <div className="flex flex-col text-right">
                    <span className="text-[9px] font-bold text-slate-400 uppercase tracking-tighter">Long-term</span>
                    <span className="text-xs font-black text-slate-700">장기</span>
                  </div>
                  <div className={`p-2 rounded-full ${longTerm.bg} ${longTerm.color}`}>{longTerm.icon}</div>
                </div>
              </div>
            </div>

            {/* 주식 게임 버튼 */}
            <button
              onClick={() => navigate('/game')}
              className="text-slate-400 hover:text-blue-600 font-black text-sm flex items-center gap-2 transition-colors duration-200 uppercase tracking-wider"
            >
              주식 게임 →
            </button>

            {/* 스크리너 버튼 (우리가 추가) */}
            <button
              onClick={() => navigate('/screener')}
              className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2.5 rounded-xl text-xs font-black hover:bg-blue-700 transition-all shadow-lg shadow-blue-200"
            >
              <BarChart2 className="w-4 h-4" />
              종목 스크리너
            </button>
          </div>
        </header>

        {/* 지수 카드 */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          <div className="group bg-white p-8 rounded-[2rem] shadow-sm hover:shadow-xl transition-all duration-300 border border-slate-100 relative overflow-hidden">
            <div className="absolute top-0 right-0 p-8 opacity-5 group-hover:opacity-10 transition-opacity">
              <Activity size={120} />
            </div>
            <div className="flex justify-between items-center mb-8">
              <div className="flex items-center gap-2">
                <span className="bg-slate-900 text-white px-3 py-1 rounded-md text-[10px] font-black uppercase tracking-tighter">KOSPI</span>
                <span className="text-slate-400 text-[10px] font-bold italic">REAL-TIME</span>
              </div>
              <div className={`flex flex-col items-end ${getStockColor(data.indices.kospi.change_percent)}`}>
                <span className="text-lg font-black">{data.indices.kospi.change_percent}</span>
                <span className="text-[10px] font-bold">{data.indices.kospi.is_up ? '▲' : '▼'} {data.indices.kospi.change_price}</span>
              </div>
            </div>
            <div className="text-6xl font-black text-slate-900 mb-4 tracking-tighter">{data.indices.kospi.price}</div>
            <div className="flex items-center gap-2 text-emerald-500 bg-emerald-50 w-fit px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest">
              <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-ping" />
              Connected
            </div>
          </div>

          <div className="group bg-white p-8 rounded-[2rem] shadow-sm hover:shadow-xl transition-all duration-300 border border-slate-100 relative overflow-hidden">
            <div className="absolute top-0 right-0 p-8 opacity-5 group-hover:opacity-10 transition-opacity">
              <BarChart3 size={120} />
            </div>
            <div className="flex justify-between items-center mb-8">
              <div className="flex items-center gap-2">
                <span className="bg-blue-600 text-white px-3 py-1 rounded-md text-[10px] font-black uppercase tracking-tighter">KOSDAQ</span>
                <span className="text-slate-400 text-[10px] font-bold italic">REAL-TIME</span>
              </div>
              <div className={`flex flex-col items-end ${getStockColor(data.indices.kosdaq.change_percent)}`}>
                <span className="text-lg font-black">{data.indices.kosdaq.change_percent}</span>
                <span className="text-[10px] font-bold">{data.indices.kosdaq.is_up ? '▲' : '▼'} {data.indices.kosdaq.change_price}</span>
              </div>
            </div>
            <div className="text-6xl font-black text-slate-900 mb-4 tracking-tighter">{data.indices.kosdaq.price}</div>
            <div className="flex items-center gap-2 text-emerald-500 bg-emerald-50 w-fit px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest">
              <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-ping" />
              Connected
            </div>
          </div>
        </div>

        {/* 차트 */}
        {data.chart_data && (
          <div className="bg-white p-8 rounded-[2rem] border border-slate-100 shadow-sm overflow-hidden">
            <div className="mb-8">
              <h3 className="text-xl font-black text-slate-800">20일 / 200일선 이격비율 및 KOSPI</h3>
              <p className="text-xs font-bold text-slate-400 mt-1 uppercase tracking-tighter">Market Trend Monitoring</p>
            </div>
            <div className="h-[420px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={data.chart_data} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
                  <XAxis dataKey="date" tick={{ fill: '#94a3b8', fontSize: 11 }} axisLine={false} tickLine={false} />
                  <YAxis yAxisId="left"  domain={['auto', 'auto']} tick={{ fill: '#3b82f6', fontSize: 11 }} axisLine={false} tickLine={false} />
                  <YAxis yAxisId="right" domain={['auto', 'auto']} orientation="right" tick={{ fill: '#22c55e', fontSize: 11 }} axisLine={false} tickLine={false} />
                  <Tooltip contentStyle={{ borderRadius: '16px', border: 'none', boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)' }} />
                  <Legend wrapperStyle={{ paddingTop: '30px', fontSize: '11px', fontWeight: '900', textTransform: 'uppercase' }} />
                  <Line yAxisId="left"  type="monotone" dataKey="kospi" name="KOSPI"     stroke="#3b82f6" strokeWidth={3} dot={false} />
                  <Line yAxisId="right" type="monotone" dataKey="ma20"  name="20D Ratio"  stroke="#f97316" strokeWidth={2} dot={false} />
                  <Line yAxisId="right" type="monotone" dataKey="ma200" name="200D Ratio" stroke="#22c55e" strokeWidth={2} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}

      </div>
    </div>
  );
}

export default Dashboard;