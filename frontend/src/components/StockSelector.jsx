import { useEffect, useState } from 'react'

function StockSelector({ onSelect }) {
  const [stocks, setStocks] = useState([])
  const [selected, setSelected] = useState('')

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/stocks/')
      .then(res => res.json())
      .then(data => setStocks(data.stocks))
      .catch(err => console.error('종목 목록 로딩 실패:', err))
  }, [])

  const handleStart = () => {
    if (!selected) return
    const stock = stocks.find(s => s.ticker === selected)
    onSelect(selected, stock?.name || selected)
  }

  return (
    <div className="flex gap-3 items-center">
      <select
        className="bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-slate-800 text-sm font-bold focus:outline-none focus:ring-2 focus:ring-blue-500"
        value={selected}
        onChange={(e) => setSelected(e.target.value)}
      >
        <option value="">종목 선택</option>
        {stocks.map(stock => (
          <option key={stock.ticker} value={stock.ticker}>
            {stock.name}
          </option>
        ))}
      </select>

      <button
        className="bg-slate-900 hover:bg-blue-600 text-white px-8 py-2.5 rounded-xl text-xs font-black uppercase tracking-widest transition-all shadow-lg shadow-slate-200 disabled:opacity-40 disabled:cursor-not-allowed"
        onClick={handleStart}
        disabled={!selected}
      >
        게임 시작
      </button>
    </div>
  )
}

export default StockSelector
