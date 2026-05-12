import { useEffect, useState } from 'react'

function StockSelector({ onSelect }) {
  const [stocks, setStocks] = useState([])

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/stocks/')
      .then(res => res.json())
      .then(data => setStocks(data.stocks))
      .catch(err => console.error('종목 목록 로딩 실패:', err))
  }, [])

  const handleStart = () => {
    if (stocks.length === 0) return
    // 종목 랜덤 선택
    const random = stocks[Math.floor(Math.random() * stocks.length)]
    onSelect(random.ticker, random.name)
  }

  return (
    <button
      className="bg-slate-900 hover:bg-blue-600 text-white px-8 py-2.5 rounded-xl text-xs font-black uppercase tracking-widest transition-all shadow-lg shadow-slate-200 disabled:opacity-40 disabled:cursor-not-allowed"
      onClick={handleStart}
      disabled={stocks.length === 0}
    >
      게임 시작
    </button>
  )
}

export default StockSelector
