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

  return (
    <div className="flex gap-3 items-center">
      <select
        className="bg-gray-800 border border-gray-600 rounded px-4 py-2 text-white"
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
        className="bg-blue-600 hover:bg-blue-500 px-6 py-2 rounded font-bold disabled:opacity-40"
        onClick={() => selected && onSelect(selected)}
        disabled={!selected}
      >
        게임 시작
      </button>
    </div>
  )
}

export default StockSelector
