import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import StockSelector from '../components/StockSelector.jsx'
import CandleChart from '../components/CandleChart.jsx'
import { TrendingUp } from 'lucide-react'

function StockGame() {
  const [gameData, setGameData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [selectedName, setSelectedName] = useState('')
  const navigate = useNavigate()

  const handleSelectStock = async (ticker, name) => {
    setLoading(true)
    setSelectedName(name)
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
    <div className="min-h-screen bg-[#F8F9FB] font-sans text-slate-900 p-6 md:p-12">
      <div className="max-w-6xl mx-auto">

        {/* 헤더 */}
        <header className="flex justify-between items-center mb-12">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                <TrendingUp className="text-white w-5 h-5" />
              </div>
              <h1 className="text-2xl font-black tracking-tighter text-slate-900 uppercase">
                Stock<span className="text-blue-600">Easy</span>
                <span className="text-slate-300 font-light mx-2">|</span>
                <span className="italic text-slate-500 text-lg">GAME</span>
              </h1>
            </div>
            <p className="text-slate-400 text-[10px] font-bold ml-10 uppercase tracking-widest">
              Stock Market Simulation
            </p>
          </div>

          {/* 대시보드로 이동 */}
          <button
            onClick={() => navigate('/')}
            className="text-xs font-bold text-slate-400 hover:text-slate-700 uppercase tracking-widest transition"
          >
            ← 대시보드
          </button>
        </header>

        {/* 종목 선택 카드 */}
        <div className="bg-white rounded-[2rem] border border-slate-100 shadow-sm p-8 mb-8 flex flex-col md:flex-row items-center justify-between gap-6">
          <div>
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1 block">
              Select Stock
            </span>
            <h2 className="text-xl font-black text-slate-800">종목을 선택하고 게임을 시작하세요</h2>
            <p className="text-xs text-slate-400 mt-1">과거 60일 차트를 보고 매매 전략을 세워보세요</p>
          </div>
          <StockSelector onSelect={handleSelectStock} />
        </div>

        {/* 로딩 */}
        {loading && (
          <div className="bg-white rounded-[2rem] border border-slate-100 shadow-sm p-12 flex flex-col items-center gap-4">
            <div className="w-10 h-10 border-4 border-blue-600 border-t-transparent rounded-full animate-spin" />
            <p className="text-slate-400 font-bold text-sm uppercase tracking-widest">
              데이터 불러오는 중...
            </p>
          </div>
        )}

        {/* 차트 카드 */}
        {gameData && !loading && (
          <div className="bg-white rounded-[2rem] border border-slate-100 shadow-sm p-8">
            <div className="flex justify-between items-center mb-6">
              <div>
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1 block">
                  Chart View
                </span>
                <h3 className="text-xl font-black text-slate-800">
                  {selectedName} <span className="text-slate-300 font-light">|</span> 과거 60일
                </h3>
              </div>
              <div className="flex items-center gap-2 text-emerald-500 bg-emerald-50 px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest">
                <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-ping" />
                데이터 로드 완료
              </div>
            </div>
            <CandleChart data={gameData.history} />
          </div>
        )}

      </div>
    </div>
  )
}

export default StockGame
