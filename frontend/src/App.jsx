import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { TrendingUp, Activity, BarChart3 } from 'lucide-react';

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    // 장고 서버 주소입니다. (서버가 8000번에서 돌아야 합니다)
    axios.get('http://127.0.0.1:8000/api/dashboard/')
      .then(res => setData(res.data))
      .catch(err => console.error("데이터 로드 실패:", err));
  }, []);

  if (!data) return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50">
      <div className="text-slate-400 font-bold animate-bounce text-xl">EasyMoney Engine Loading...</div>
    </div>
  );

  return (
    <div className="min-h-screen bg-[#F8F9FB] p-8 font-sans text-slate-900">
      <div className="max-w-5xl mx-auto">
        <header className="flex justify-between items-end mb-12">
          <div>
            <h1 className="text-3xl font-black tracking-tighter text-slate-900">
              EasyMoney <span className="text-blue-600 italic">ASFE</span>
            </h1>
            <p className="text-slate-400 text-sm font-medium mt-1">Real-time Quantitative Analysis</p>
          </div>
          <div className="flex items-center space-x-3 bg-white px-5 py-2.5 rounded-2xl shadow-sm border border-slate-100">
            <div className={`w-3 h-3 rounded-full ${data.market_signals.short_term.status === 'R' ? 'bg-red-500' : 'bg-emerald-500'} animate-pulse`} />
            <span className="text-sm font-black text-slate-700">{data.market_signals.short_term.label}</span>
          </div>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* 코스피 카드 */}
          <div className="bg-white p-10 rounded-[2.5rem] shadow-xl shadow-slate-200/50 border border-white">
            <div className="flex justify-between items-start mb-6">
              <span className="bg-blue-50 text-blue-600 px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest">KOSPI</span>
              <span className="text-blue-500 font-bold text-sm">{data.indices.kospi.change_percent}</span>
            </div>
            <div className="text-5xl font-black text-slate-900 mb-2 tracking-tight">{data.indices.kospi.price}</div>
            <p className="text-slate-400 text-xs font-medium uppercase">Market Index Connected</p>
          </div>

          {/* 코스닥 카드 */}
          <div className="bg-white p-10 rounded-[2.5rem] shadow-xl shadow-slate-200/50 border border-white">
            <div className="flex justify-between items-start mb-6">
              <span className="bg-indigo-50 text-indigo-600 px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest">KOSDAQ</span>
              <span className="text-blue-500 font-bold text-sm">{data.indices.kosdaq.change_percent}</span>
            </div>
            <div className="text-5xl font-black text-slate-900 mb-2 tracking-tight">{data.indices.kosdaq.price}</div>
            <p className="text-slate-400 text-xs font-medium uppercase">Market Index Connected</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;