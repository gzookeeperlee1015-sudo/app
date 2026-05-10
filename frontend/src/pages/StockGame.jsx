import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import StockSelector from '../components/StockSelector.jsx'
import CandleChart from '../components/CandleChart.jsx'

function StockGame() {
  const [gameData, setGameData] = useState(null)
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleSelectStock = async (ticker) => {
    setLoading(true)
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/game/start/?ticker=${ticker}`)
      const data = await res.json()
      setGameData(data)
    } catch (err) {
      console.error('데이터 로딩 실패:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white p-6">
      <div className="max-w-5xl mx-auto">

        {/* 헤더 */}
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-2xl font-black">📈 주식 미니게임</h1>
          {/* 대시보드로 돌아가기 버튼 */}
          <button
            onClick={() => navigate('/')}
            className="text-sm text-gray-400 hover:text-white transition"
          >
            ← 대시보드로
          </button>
        </div>

        {/* 종목 선택 */}
        <StockSelector onSelect={handleSelectStock} />

        {/* 로딩 */}
        {loading && (
          <p className="text-gray-400 mt-8">데이터 불러오는 중...</p>
        )}

        {/* 차트 */}
        {gameData && !loading && (
          <div className="mt-8">
            <CandleChart data={gameData.history} />
          </div>
        )}

      </div>
    </div>
  )
}

export default StockGame
