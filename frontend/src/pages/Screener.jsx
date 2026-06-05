/**
 * frontend/src/pages/Screener.jsx
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  TrendingUp, DollarSign, Flame, BarChart2,
  X, ChevronRight, ArrowLeft, RefreshCw,
  ArrowUp, ArrowDown, Minus, Star
} from 'lucide-react';

const BASE_URL = 'http://127.0.0.1:8000';

const CATEGORIES = {
  growth: {
    key:      'growth',
    apiPath:  '/api/stocks/growth/',
    label:    '저평가 성장주',
    eng:      'GROWTH',
    sub:      'PER ≤ 20  ·  ROE ≥ 10%',
    desc:     '이익 대비 저렴하면서 높은 수익성을 가진 종목',
    icon:     TrendingUp,
    color:    '#3b82f6',
    dimColor: '#1d4ed8',
    bg:       '#eff6ff',
    getMetrics: (s) => [
      { label: 'PER', value: s.per,  unit: '',  highlight: false },
      { label: 'ROE', value: s.roe,  unit: '%', highlight: true  },
    ],
  },
  value: {
    key:      'value',
    apiPath:  '/api/stocks/value/',
    label:    '저렴한 가치주',
    eng:      'VALUE',
    sub:      'PER ≤ 10',
    desc:     '시장 평균 대비 주가가 매우 저렴한 종목',
    icon:     DollarSign,
    color:    '#10b981',
    dimColor: '#047857',
    bg:       '#f0fdf4',
    getMetrics: (s) => [
      { label: 'PER', value: s.per, unit: '', highlight: true },
      { label: 'ROE', value: s.roe, unit: '%', highlight: false },
    ],
  },
  week52: {
    key:      'week52',
    apiPath:  '/api/stocks/week52/',
    label:    '52주 신고가 근접',
    eng:      '52W HIGH',
    sub:      '현재가 ≥ 52주 최고가의 90%',
    desc:     '강한 상승 모멘텀으로 신고가에 근접한 종목',
    icon:     Star,
    color:    '#8b5cf6',
    dimColor: '#6d28d9',
    bg:       '#f5f3ff',
    getMetrics: (s) => [
      { label: '고가비율', value: s.high_ratio, unit: '%', highlight: true },
      { label: '52주고가', value: s.week52_high?.toLocaleString(), unit: '원', highlight: false },
    ],
  },
  volume: {
    key:      'volume',
    apiPath:  '/api/stocks/volume/',
    label:    '거래량 상위',
    eng:      'VOLUME',
    sub:      '당일 거래량 Top 10',
    desc:     '시장의 관심이 집중된 핫한 종목',
    icon:     Flame,
    color:    '#ef4444',
    dimColor: '#b91c1c',
    bg:       '#fef2f2',
    getMetrics: (s) => [
      { label: '거래량', value: (s.volume / 10000).toFixed(0), unit: '만주', highlight: true },
    ],
  },
};

function ChangeDisplay({ value }) {
  const n = parseFloat(value);
  if (n > 0) return <span className="flex items-center gap-0.5 text-red-500 font-bold text-xs"><ArrowUp className="w-3 h-3" />{Math.abs(n)}%</span>;
  if (n < 0) return <span className="flex items-center gap-0.5 text-blue-500 font-bold text-xs"><ArrowDown className="w-3 h-3" />{Math.abs(n)}%</span>;
  return <span className="flex items-center gap-0.5 text-slate-400 font-bold text-xs"><Minus className="w-3 h-3" />0%</span>;
}

function StockModal({ catKey, onClose }) {
  const [stocks, setStocks] = useState([]);
  const [loading, setLoading] = useState(true);
  const cfg  = CATEGORIES[catKey];
  const Icon = cfg.icon;

  useEffect(() => {
    axios.get(BASE_URL + cfg.apiPath)
      .then(res => { setStocks(res.data.stocks || []); setLoading(false); })
      .catch(() => setLoading(false));
  }, [catKey]);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4"
      style={{ background: 'rgba(0,0,0,0.5)', backdropFilter: 'blur(4px)' }}
      onClick={e => e.target === e.currentTarget && onClose()}
    >
      <div className="bg-white rounded-3xl shadow-2xl w-full max-w-2xl max-h-[88vh] flex flex-col overflow-hidden">
        <div className="flex items-center justify-between px-7 py-5"
          style={{ background: cfg.bg, borderBottom: `2px solid ${cfg.color}20` }}>
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-2xl text-white" style={{ background: cfg.color }}>
              <Icon className="w-5 h-5" />
            </div>
            <div>
              <div className="font-black text-base tracking-tight" style={{ color: cfg.dimColor }}>{cfg.label}</div>
              <div className="text-[11px] font-bold text-slate-400 mt-0.5">{cfg.sub}</div>
            </div>
          </div>
          <button onClick={onClose} className="p-2 rounded-full hover:bg-black/5 transition-colors text-slate-400">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="overflow-y-auto flex-1 px-7 py-5">
          {loading ? (
            <div className="flex flex-col items-center justify-center py-20 gap-4">
              <div className="w-10 h-10 border-4 border-t-transparent rounded-full animate-spin"
                style={{ borderColor: cfg.color, borderTopColor: 'transparent' }} />
              <p className="text-slate-400 text-sm font-bold">데이터 불러오는 중...</p>
            </div>
          ) : stocks.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-20 gap-3">
              <BarChart2 className="w-10 h-10 text-slate-200" />
              <p className="text-slate-400 text-sm font-bold">조건에 맞는 종목이 없습니다</p>
            </div>
          ) : (
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b-2 border-slate-100">
                  <th className="text-left py-3 px-2 text-[10px] font-black text-slate-400 uppercase">#</th>
                  <th className="text-left py-3 px-2 text-[10px] font-black text-slate-400 uppercase">종목</th>
                  <th className="text-left py-3 px-2 text-[10px] font-black text-slate-400 uppercase">현재가</th>
                  <th className="text-left py-3 px-2 text-[10px] font-black text-slate-400 uppercase">등락률</th>
                  {cfg.getMetrics(stocks[0] || {}).map(m => (
                    <th key={m.label} className="text-left py-3 px-2 text-[10px] font-black uppercase" style={{ color: cfg.color }}>{m.label}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {stocks.map((stock, idx) => (
                  <tr key={stock.ticker} className="border-b border-slate-50 hover:bg-slate-50/80 transition-colors">
                    <td className="py-4 px-2">
                      <span className="text-[11px] font-black" style={{ color: idx < 3 ? cfg.color : '#cbd5e1' }}>{idx + 1}</span>
                    </td>
                    <td className="py-4 px-2">
                      <div className="font-black text-slate-800 text-sm">{stock.name}</div>
                      <div className="text-[10px] text-slate-400 font-mono mt-0.5">{stock.ticker}</div>
                    </td>
                    <td className="py-4 px-2 font-black text-slate-700 text-sm">{stock.price?.toLocaleString('ko-KR')}원</td>
                    <td className="py-4 px-2"><ChangeDisplay value={stock.change_rate} /></td>
                    {cfg.getMetrics(stock).map(m => (
                      <td key={m.label} className="py-4 px-2">
                        <span className="font-black text-sm" style={{ color: m.highlight ? cfg.color : '#475569' }}>
                          {m.value}{m.unit}
                        </span>
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
}

function CategoryCard({ catKey, onOpenModal }) {
  const [stocks, setStocks]   = useState([]);
  const [loading, setLoading] = useState(true);
  const cfg  = CATEGORIES[catKey];
  const Icon = cfg.icon;

  useEffect(() => {
    axios.get(BASE_URL + cfg.apiPath)
      .then(res => { setStocks(res.data.stocks || []); setLoading(false); })
      .catch(() => setLoading(false));
  }, [catKey]);

  const preview = stocks.slice(0, 3);

  return (
    <div className="bg-white rounded-3xl border border-slate-100 shadow-sm hover:shadow-lg transition-all duration-300 overflow-hidden flex flex-col">
      <div className="px-6 pt-6 pb-4">
        <div className="flex items-start justify-between mb-4">
          <div className="p-2.5 rounded-2xl text-white" style={{ background: cfg.color }}>
            <Icon className="w-5 h-5" />
          </div>
          <span className="font-mono text-[10px] font-black px-2.5 py-1 rounded-full"
            style={{ background: cfg.bg, color: cfg.color }}>{cfg.eng}</span>
        </div>
        <h3 className="font-black text-lg text-slate-900 tracking-tight leading-tight">{cfg.label}</h3>
        <p className="text-[11px] text-slate-400 font-bold mt-1">{cfg.sub}</p>
        <p className="text-xs text-slate-500 mt-2 leading-relaxed">{cfg.desc}</p>
      </div>

      <div className="mx-6 border-t border-slate-100" />

      <div className="px-6 py-4 flex-1">
        {loading ? (
          <div className="flex items-center justify-center py-6">
            <div className="w-6 h-6 border-2 border-t-transparent rounded-full animate-spin"
              style={{ borderColor: cfg.color, borderTopColor: 'transparent' }} />
          </div>
        ) : preview.length === 0 ? (
          <p className="text-center text-slate-300 text-xs font-bold py-6">조건 충족 종목 없음</p>
        ) : (
          <div className="flex flex-col gap-3">
            {preview.map((stock, idx) => (
              <div key={stock.ticker} className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <span className="text-[11px] font-black w-4 text-right"
                    style={{ color: idx === 0 ? cfg.color : '#cbd5e1' }}>{idx + 1}</span>
                  <div>
                    <div className="text-sm font-black text-slate-800">{stock.name}</div>
                    <div className="text-[10px] text-slate-400 font-mono">{stock.ticker}</div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-xs font-black text-slate-700">{stock.price?.toLocaleString('ko-KR')}원</div>
                  <div className="text-[11px] font-bold mt-0.5" style={{ color: cfg.color }}>
                    {cfg.getMetrics(stock)[0]?.value}{cfg.getMetrics(stock)[0]?.unit}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="px-6 pb-6">
        <button
          onClick={() => onOpenModal(catKey)}
          className="w-full flex items-center justify-center gap-2 py-3 rounded-2xl text-xs font-black transition-all hover:opacity-80"
          style={{ background: cfg.bg, color: cfg.color }}
        >
          전체 종목 보기 <ChevronRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}

export default function Screener() {
  const [modal, setModal]           = useState(null);
  const [lastUpdate, setLastUpdate] = useState('');

  useEffect(() => {
    axios.get(BASE_URL + '/api/stocks/volume/')
      .then(res => setLastUpdate(res.data.updated_at || ''))
      .catch(() => {});
  }, []);

  const formatTime = (iso) => {
    if (!iso) return '-';
    const d = new Date(iso);
    return `${d.getHours().toString().padStart(2,'0')}:${d.getMinutes().toString().padStart(2,'0')} 기준`;
  };

  return (
    <div className="min-h-screen bg-[#F8F9FB] font-sans">
      <header className="bg-white border-b border-slate-100 sticky top-0 z-40">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <a href="/" className="flex items-center gap-1.5 text-slate-400 hover:text-slate-700 transition-colors text-xs font-bold">
              <ArrowLeft className="w-4 h-4" />대시보드
            </a>
            <div className="w-px h-4 bg-slate-200" />
            <div>
              <div className="flex items-center gap-2">
                <BarChart2 className="w-4 h-4 text-blue-600" />
                <span className="font-black text-sm text-slate-900 tracking-tight">
                  Stock<span className="text-blue-600">Easy</span> Screener
                </span>
              </div>
              <p className="text-[10px] text-slate-400 font-bold uppercase tracking-widest mt-0.5">Quantitative Stock Analysis</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-1.5 text-[11px] font-bold text-slate-400">
              <RefreshCw className="w-3 h-3" />{formatTime(lastUpdate)}
            </div>
            <div className="flex items-center gap-1.5 bg-emerald-50 text-emerald-600 px-3 py-1.5 rounded-full text-[10px] font-black">
              <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-ping" />LIVE
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-10">
        <div className="mb-10">
          <p className="text-[11px] font-black text-blue-600 uppercase tracking-widest mb-2">Stock Screener</p>
          <h1 className="text-3xl font-black text-slate-900 tracking-tight leading-tight">종목 분류 스크리너</h1>
          <p className="text-slate-500 text-sm mt-2 font-medium">KOSPI · KOSDAQ 주요 종목을 4가지 기준으로 분류합니다</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {Object.keys(CATEGORIES).map(catKey => (
            <CategoryCard key={catKey} catKey={catKey} onOpenModal={setModal} />
          ))}
        </div>

        <div className="mt-10 p-5 bg-white rounded-2xl border border-slate-100 text-center">
          <p className="text-xs text-slate-400 font-bold">
            ※ 본 정보는 투자 참고용이며 투자 권유가 아닙니다 · 데이터는 30분 주기로 자동 갱신됩니다
          </p>
        </div>
      </main>

      {modal && <StockModal catKey={modal} onClose={() => setModal(null)} />}
    </div>
  );
}
