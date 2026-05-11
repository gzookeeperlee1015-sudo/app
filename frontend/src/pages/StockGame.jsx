import { useState, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import StockSelector from '../components/StockSelector.jsx'
import CandleChart from '../components/CandleChart.jsx'
import { TrendingUp } from 'lucide-react'

function StockGame() {
  const [gameData, setGameData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [selectedName, setSelectedName] = useState('')
  const [dayIndex, setDayIndex] = useState(0)
  const [isGameOver, setIsGameOver] = useState(false)
  const chartRef = useRef(null)
  const navigate = useNavigate()

  const handleSelectStock = async (ticker, name) => {
    setLoading(true)
    setSelectedName(name)
    setDayIndex(0)
    setIsGameOver(false)
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

  const handleAction = (action) => {
    if (!gameData || isGameOver) return
    const nextCandle = gameData.future[dayIndex]
    if (!nextCandle) return

    chartRef.current?.addCandle(nextCandle)

    const nextDay = dayIndex + 1
    if (nextDay >= gameData.future.length) {
      setIsGameOver(true)
    }
    setDayIndex(nextDay)
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
          <button
            onClick={() => navigate('/')}
            className="text-xs font-bold text-slate-400 hover:text-slate-700 uppercase tracking-widest transition"
          >
            ← 대시보드
          </button>
        </header>

        {/* 인트로 화면 */}
        {!gameData && !loading && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div className="bg-white rounded-[2rem] border border-slate-100 shadow-sm p-10 flex flex-col justify-between gap-10">
              <div>
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-3 block">
                  Game Start
                </span>
                <h2 className="text-3xl font-black text-slate-900 leading-tight mb-4">
                  과거 차트를 보고<br />수익을 올려보세요
                </h2>
                <ul className="text-sm text-slate-400 space-y-2">
                  <li>📅 랜덤 종목 · 랜덤 날짜로 시작</li>
                  <li>💰 시작 자본 <span className="font-bold text-slate-600">1,000만원</span></li>
                  <li>📈 30일 동안 매수 · 매도 · 홀드 선택</li>
                  <li>🏆 최종 수익률로 랭킹 등록</li>
                </ul>
              </div>
              <StockSelector onSelect={handleSelectStock} />
            </div>

            {/* 랭킹 자리 */}
            <div className="bg-white rounded-[2rem] border border-slate-100 shadow-sm p-10 flex flex-col">
              <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-3 block">
                Ranking
              </span>
              <h2 className="text-xl font-black text-slate-900 mb-6">명예의 전당</h2>
              <div className="flex-1 flex items-center justify-center">
                <p className="text-slate-300 text-sm font-bold uppercase tracking-widest">Coming Soon</p>
              </div>
            </div>
          </div>
        )}

        {/* 로딩 */}
        {loading && (
          <div className="bg-white rounded-[2rem] border border-slate-100 shadow-sm p-12 flex flex-col items-center gap-4">
            <div className="w-10 h-10 border-4 border-blue-600 border-t-transparent rounded-full animate-spin" />
            <p className="text-slate-400 font-bold text-sm uppercase tracking-widest">
              데이터 불러오는 중...
            </p>
          </div>
        )}

        {/* 게임 화면 */}
        {gameData && !loading && (
          <div className="bg-white rounded-[2rem] border border-slate-100 shadow-sm p-8">
            <div className="flex justify-between items-center mb-6">
              <div>
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1 block">
                  Chart View
                </span>
                <h3 className="text-xl font-black text-slate-800">
                  {selectedName}
                  <span className="text-slate-300 font-light mx-2">|</span>
                  {isGameOver ? '게임 종료' : `${dayIndex} / 30일`}
                </h3>
              </div>
              <div className="flex items-center gap-4">
                {!isGameOver && (
                  <div className="flex items-center gap-2 text-emerald-500 bg-emerald-50 px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest">
                    <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-ping" />
                    진행중
                  </div>
                )}
                <button
                  onClick={() => { setGameData(null); setDayIndex(0); setIsGameOver(false) }}
                  className="text-xs font-bold text-slate-400 hover:text-slate-700 uppercase tracking-widest transition"
                >
                  ← 처음으로
                </button>
              </div>
            </div>

            {/* 차트 */}
            <CandleChart ref={chartRef} data={gameData.history} />

            {/* 액션 버튼 */}
            {!isGameOver ? (
              <div className="mt-6 grid grid-cols-4 gap-3">
                <button
                  onClick={() => handleAction('buy')}
                  className="bg-red-50 hover:bg-red-500 hover:text-white text-red-500 font-black py-4 rounded-2xl text-sm uppercase tracking-widest transition-all border border-red-100"
                >
                  매수
                </button>
                <button
                  onClick={() => handleAction('sell')}
                  className="bg-blue-50 hover:bg-blue-500 hover:text-white text-blue-500 font-black py-4 rounded-2xl text-sm uppercase tracking-widest transition-all border border-blue-100"
                >
                  매도
                </button>
                <button
                  onClick={() => handleAction('hold')}
                  className="bg-slate-50 hover:bg-slate-700 hover:text-white text-slate-600 font-black py-4 rounded-2xl text-sm uppercase tracking-widest transition-all border border-slate-200"
                >
                  홀드
                </button>
                <button
                  onClick={() => handleAction('skip')}
                  className="bg-slate-50 hover:bg-slate-300 text-slate-400 font-black py-4 rounded-2xl text-sm uppercase tracking-widest transition-all border border-slate-200"
                >
                  넘기기
                </button>
              </div>
            ) : (
              <div className="mt-6 bg-slate-50 rounded-2xl p-8 text-center border border-slate-100">
                <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-2">Game Over</p>
                <p className="text-2xl font-black text-slate-900 mb-6">30일이 지났습니다!</p>
                <button
                  onClick={() => { setGameData(null); setDayIndex(0); setIsGameOver(false) }}
                  className="bg-slate-900 hover:bg-blue-600 text-white px-10 py-3 rounded-xl text-xs font-black uppercase tracking-widest transition-all"
                >
                  다시 시작
                </button>
              </div>
            )}
          </div>
        )}

      </div>
    </div>
  )
}

export default StockGame
