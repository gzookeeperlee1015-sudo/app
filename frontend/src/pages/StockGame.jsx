import { useState, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import StockSelector from '../components/StockSelector.jsx'
import CandleChart from '../components/CandleChart.jsx'
import NicknameModal from '../components/NicknameModal.jsx'
import Ranking from '../components/Ranking.jsx'
import { TrendingUp } from 'lucide-react'
import ResultModal from '../components/ResultModal.jsx'

// 시작 자본금 상수
const INITIAL_CASH = 10000000

function StockGame() {

  // ────────────────────────────────────────
  // 플레이어 상태
  // null이면 닉네임 모달 표시
  // ────────────────────────────────────────
  const [player, setPlayer] = useState(null)

  // ────────────────────────────────────────
  // 게임 데이터 상태
  // ────────────────────────────────────────
  const [gameData, setGameData] = useState(null)        // 백엔드에서 받아온 주가 데이터
  const [loading, setLoading] = useState(false)         // 데이터 로딩 중 여부
  const [selectedName, setSelectedName] = useState('')  // 선택된 종목 한글명
  const [selectedTicker, setSelectedTicker] = useState('')  // 선택된 종목 티커
  const [dayIndex, setDayIndex] = useState(0)           // 현재 진행 날수 (0~30)
  const [isGameOver, setIsGameOver] = useState(false)   // 30일 완료 여부
  const [showResult, setShowResult] = useState(false)   // 결과 모달 표시 여부
  const [isBankrupt, setIsBankrupt] = useState(false)   // 파산 여부

  // ────────────────────────────────────────
  // 자산 관련 상태
  // ────────────────────────────────────────
  const [cash, setCash] = useState(0)               // 현재 보유 현금
  const [shares, setShares] = useState(0)           // 보유 주식 수량
  const [avgPrice, setAvgPrice] = useState(0)       // 평균 매수가
  const [currentPrice, setCurrentPrice] = useState(0)   // 현재 주가
  const [startBalance, setStartBalance] = useState(0)   // 이번 게임 시작 시 자산

  // ────────────────────────────────────────
  // 매수/매도 UI 상태
  // ────────────────────────────────────────
  const [mode, setMode] = useState(null)            // null | 'buy' | 'sell'
  const [customPercent, setCustomPercent] = useState('')  // 직접 입력 퍼센트
  const [isProcessing, setIsProcessing] = useState(false)  // 처리 중 여부
  const chartRef = useRef(null)
  const navigate = useNavigate()

  // 숫자 천단위 포맷
  const fmt = (n) => Math.round(n).toLocaleString('ko-KR')

  // 수익률: 보유 주식 있을 때만 계산
  const profitRate = shares > 0 && avgPrice > 0
    ? (((currentPrice - avgPrice) / avgPrice) * 100).toFixed(2)
    : null

  // 보유 주식 평가금액
  const stockValue = shares * currentPrice

  // 총 자산 = 현금 + 주식 평가금액
  const totalAsset = cash + stockValue

  // 이번 게임 수익금
  const profit = totalAsset - startBalance

  // ────────────────────────────────────────
  // 닉네임 확인 후 플레이어 정보 세팅
  // ────────────────────────────────────────
  const handlePlayerConfirm = (playerData) => {
    setPlayer(playerData)
    setCash(playerData.balance)
  }

  // ────────────────────────────────────────
  // 로그아웃: 플레이어 초기화 → 닉네임 모달 다시 표시
  // ────────────────────────────────────────
  const handleLogout = () => {
    setPlayer(null)
    setGameData(null)
    setDayIndex(0)
    setIsGameOver(false)
    setCash(0)
    setShares(0)
    setAvgPrice(0)
    setCurrentPrice(0)
    setMode(null)
  }

  // ────────────────────────────────────────
  // 게임 시작
  // ────────────────────────────────────────
  const handleSelectStock = async (ticker, name) => {
    setLoading(true)
    setSelectedName(name)
    setSelectedTicker(ticker)
    setDayIndex(0)
    setIsGameOver(false)
    setShares(0)
    setAvgPrice(0)
    setMode(null)
    setStartBalance(cash)  // 게임 시작 시 자산 기록

    try {
      const res = await fetch(`http://127.0.0.1:8000/api/game/start/?ticker=${ticker}`)
      const data = await res.json()
      setCurrentPrice(data.history[data.history.length - 1].close)
      setGameData(data)
    } catch (err) {
      console.error('데이터 로딩 실패:', err)
    } finally {
      setLoading(false)
    }
  }

  // ────────────────────────────────────────
  // 게임 결과 저장 (자동 호출)
  // finalPrice: 마지막 캔들 종가 (상태 업데이트 지연 방지를 위해 인자로 받음)
  // ────────────────────────────────────────
  const handleSaveResult = async (finalPrice) => {
    if (!player) return
    const finalCash = cash + shares * finalPrice

    try {
      const res = await fetch('http://127.0.0.1:8000/api/game/result/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          nickname: player.nickname,
          ticker: selectedTicker,
          stock_name: selectedName,
          start_balance: startBalance,
          end_balance: Math.round(finalCash),
        }),
      })
      const data = await res.json()
      setShares(0)
      setAvgPrice(0)
      setCash(Math.round(finalCash))
      setPlayer(prev => ({ ...prev, balance: data.balance }))
      setShowResult(true)  // 모달 표시
    } catch (err) {
      console.error('결과 저장 실패:', err)
    }
  }
  // 파산 처리: 결과 저장 후 자산 1000만원으로 초기화
  const handleBankrupt = async () => {
    if (!player) return
    try {
      const res = await fetch('http://127.0.0.1:8000/api/game/result/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          nickname: player.nickname,
          ticker: selectedTicker,
          stock_name: selectedName,
          start_balance: startBalance,
          end_balance: 10000000,  // 1000만원으로 초기화
        }),
    })
      const data = await res.json()
      setPlayer(prev => ({ ...prev, balance: data.balance }))
      setCash(data.balance)
    } catch (err) {
      console.error('파산 저장 실패:', err)
    }
  }

  // ────────────────────────────────────────
  // 다음 캔들로 이동 (홀드/넘기기/매수·매도 완료 후 공통 호출)
  // ────────────────────────────────────────
  const nextCandle = async () => {
    if (!gameData || isGameOver || isProcessing) return
    setIsProcessing(true)
    const candle = gameData.future[dayIndex]
    if (!candle) return

    // 차트에 캔들 추가
    chartRef.current?.addCandle(candle)
    setCurrentPrice(candle.close)

    const nextDay = dayIndex + 1

    // 30일 소진 시 게임 종료 + 자동 저장
    if (nextDay >= gameData.future.length) {
      setIsGameOver(true)
      await handleSaveResult(candle.close)
    }

      // 200원 이하로 떨어지면 즉시 파산 처리
    const finalCash = cash + shares * candle.close
    if (finalCash <= 2000000) {
        setIsGameOver(true)
    // 자산 1000만원으로 초기화 후 저장
    await handleBankrupt()
  }

   setDayIndex(nextDay)
    setMode(null)
    setCustomPercent('')
    setIsProcessing(false)
  }

  // ────────────────────────────────────────
  // 매수 처리
  // ────────────────────────────────────────
  const handleBuy = (percent) => {
    const p = parseFloat(percent)
    if (!p || p <= 0 || p > 100) return

    const useCash = cash * (p / 100)
    const buyShares = Math.floor(useCash / currentPrice)
    if (buyShares <= 0) return

    const totalCost = buyShares * currentPrice
    const newAvgPrice = shares === 0
      ? currentPrice
      : ((avgPrice * shares) + totalCost) / (shares + buyShares)

    setCash(prev => prev - totalCost)
    setShares(prev => prev + buyShares)
    setAvgPrice(newAvgPrice)
    nextCandle()
  }

  // ────────────────────────────────────────
  // 매도 처리
  // ────────────────────────────────────────
  const handleSell = (percent) => {
    const p = parseFloat(percent)
    if (!p || p <= 0 || p > 100 || shares === 0) return

    const sellShares = Math.floor(shares * (p / 100))
    if (sellShares <= 0) return

    const revenue = sellShares * currentPrice
    setCash(prev => prev + revenue)
    setShares(prev => prev - sellShares)
    if (shares - sellShares === 0) setAvgPrice(0)
    nextCandle()
  }

  // ────────────────────────────────────────
  // 게임 초기화 (다시 시작)
  // ────────────────────────────────────────
  const handleReset = async () => {
    const finalCash = cash + shares * currentPrice

    if (gameData && !isGameOver && player) {
      await handleSaveResult(currentPrice)
      return  // 모달이 뜨고 확인 누르면 초기화됨
    }

    setCash(finalCash)
    setGameData(null)
    setDayIndex(0)
    setIsGameOver(false)
    setShares(0)
    setAvgPrice(0)
    setCurrentPrice(0)
    setMode(null)
    setShowResult(false)
    setIsBankrupt(false)
  }

  const handleResultClose = () => {
    setShowResult(false)
    setIsBankrupt(false)
    setGameData(null)
    setDayIndex(0)
    setIsGameOver(false)
    setShares(0)
    setAvgPrice(0)
    setCurrentPrice(0)
    setMode(null)
  }

  // 오늘 캔들 정보 (사이드패널 시세 표시용)
  const todayCandle = gameData
    ? dayIndex === 0
      ? gameData.history[gameData.history.length - 1]
      : gameData.future[dayIndex - 1]
    : null

  return (
    <div className="min-h-screen bg-[#F8F9FB] font-sans text-slate-900 p-6 md:p-12">
      <div className="max-w-7xl mx-auto">

        {/* 닉네임 모달: player가 없으면 표시 */}
        {!player && <NicknameModal onConfirm={handlePlayerConfirm} />}

        {/* 결과 모달 */}
        {showResult && (
          <ResultModal
            profit={profit}
            totalAsset={cash}
            onClose={handleResultClose}
            isBankrupt={isBankrupt}
          />
        )}

        {/* ── 헤더 ── */}
        <header className="flex justify-between items-center mb-12">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                <TrendingUp className="text-white w-5 h-5" />
              </div>
              <h1 className="text-2xl font-black tracking-tighter text-slate-900 uppercase">
                Easy<span className="text-blue-600">Money</span>
                <span className="text-slate-300 font-light mx-2">|</span>
                <span className="italic text-slate-500 text-lg">GAME</span>
              </h1>
            </div>
            <p className="text-slate-400 text-[10px] font-bold ml-10 uppercase tracking-widest">
              Stock Market Simulation
            </p>
          </div>
          <div className="flex items-center gap-6">
            {/* 닉네임 클릭 시 로그아웃 */}
            {player && (
              <button
                onClick={handleLogout}
                className="text-right group"
              >
                <p className="text-xs font-black text-slate-700 group-hover:text-red-400 transition">
                  {player.nickname} ✕
                </p>
                <p className="text-[10px] text-slate-400 font-bold">
                  누적 자산 {fmt(player.balance)}원
                </p>
              </button>
            )}
            <button
              onClick={() => navigate('/')}
              className="text-xs font-bold text-slate-400 hover:text-slate-700 uppercase tracking-widest transition"
            >
              ← 대시보드
            </button>
          </div>
        </header>

        {/* ── 인트로 화면 ── */}
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
                  <li>💰 현재 보유 자산 <span className="font-bold text-slate-600">{fmt(cash)}원</span></li>
                  <li>📈 30일 동안 매수 · 매도 · 홀드 선택</li>
                  <li>🏆 최종 수익률로 랭킹 자동 등록</li>
                </ul>
              </div>
              <StockSelector onSelect={handleSelectStock} />
            </div>
            <Ranking />
          </div>
        )}

        {/* ── 로딩 화면 ── */}
        {loading && (
          <div className="bg-white rounded-[2rem] border border-slate-100 shadow-sm p-12 flex flex-col items-center gap-4">
            <div className="w-10 h-10 border-4 border-blue-600 border-t-transparent rounded-full animate-spin" />
            <p className="text-slate-400 font-bold text-sm uppercase tracking-widest">
              데이터 불러오는 중...
            </p>
          </div>
        )}

        {/* ── 게임 화면 ── */}
        {gameData && !loading && (
          <div className="bg-white rounded-[2rem] border border-slate-100 shadow-sm p-8">

            {/* 상단 */}
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
                  onClick={handleReset}
                  className="text-xs font-bold text-slate-400 hover:text-slate-700 uppercase tracking-widest transition"
                >
                  ← 처음으로
                </button>
              </div>
            </div>

            {/* 차트(7) + 사이드패널(3) */}
            <div className="flex gap-6">

              {/* 차트 */}
              <div className="flex-[7]">
                <CandleChart ref={chartRef} data={gameData.history} />
              </div>

              {/* 사이드 패널 */}
              <div className="flex-[3] flex flex-col gap-4">

                {/* 자산 정보 */}
                <div className="bg-slate-50 rounded-2xl p-5 border border-slate-100">
                  <div className="flex justify-between items-start mb-3">
                    <div>
                      <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1">보유 주식</p>
                      <p className="text-lg font-black text-slate-900">{fmt(stockValue)}원</p>
                      {shares > 0 && (
                        <p className="text-xs text-slate-400">{shares}주 · 평균 {fmt(avgPrice)}원</p>
                      )}
                    </div>
                    {profitRate !== null && (
                      <div className="text-right">
                        <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1">수익률</p>
                        <p className={`text-lg font-black ${parseFloat(profitRate) >= 0 ? 'text-red-500' : 'text-blue-500'}`}>
                          {parseFloat(profitRate) >= 0 ? '+' : ''}{profitRate}%
                        </p>
                      </div>
                    )}
                  </div>
                  <div className="border-t border-slate-200 pt-3">
                    <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1">보유 현금</p>
                    <p className="text-sm font-black text-slate-600">{fmt(cash)}원</p>
                  </div>
                  <div className="mt-2">
                    <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1">총 자산</p>
                    <p className={`text-sm font-black ${profit >= 0 ? 'text-red-500' : 'text-blue-500'}`}>
                      {fmt(totalAsset)}원 ({profit >= 0 ? '+' : ''}{fmt(profit)}원)
                    </p>
                  </div>
                </div>

                {/* 버튼 영역 */}
                {!isGameOver ? (
                  <>
                    {mode === null && (
                      <div className="flex flex-col gap-2">
                        <button onClick={() => setMode('buy')}
                          disabled={cash < currentPrice}
                          className="bg-red-500 hover:bg-red-600 text-white font-black py-4 rounded-2xl text-sm uppercase tracking-widest transition-all disabled:opacity-30 disabled:cursor-not-allowed">
                          매수
                        </button>
                        <button onClick={() => setMode('sell')} disabled={shares === 0}
                          className="bg-blue-500 hover:bg-blue-600 text-white font-black py-4 rounded-2xl text-sm uppercase tracking-widest transition-all disabled:opacity-30 disabled:cursor-not-allowed">
                          매도
                        </button>
                        <button onClick={nextCandle}
                          disabled={isProcessing}
                          className="bg-slate-100 hover:bg-slate-200 text-slate-600 font-black py-4 rounded-2xl text-sm uppercase tracking-widest transition-all border border-slate-200x disabled:opacity-30 disabled:cursor-not-allowed">
                          홀드
                        </button>
                        <button onClick={nextCandle}
                          disabled={isProcessing}
                          className="text-slate-300 hover:text-slate-400 font-bold py-2 text-xs uppercase tracking-widest transition-all disabled:opacity-30 disabled:cursor-not-allowed">
                          넘기기 →
                        </button>
                      </div>
                    )}

                    {/* 매수 퍼센트 선택 */}
                    {mode === 'buy' && (
                      <div className="flex flex-col gap-2">
                        <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">현금의 몇 % 매수?</p>
                        <div className="grid grid-cols-3 gap-2">
                          {[10, 50, 100].map(p => (
                            <button key={p} onClick={() => handleBuy(p)}
                              className="bg-red-50 hover:bg-red-500 hover:text-white text-red-500 font-black py-3 rounded-xl text-sm border border-red-100 transition-all">
                              {p}%
                            </button>
                          ))}
                        </div>
                        <div className="flex gap-2 mt-1">
                          <input type="number" placeholder="직접 입력 %"
                            value={customPercent} onChange={e => setCustomPercent(e.target.value)}
                            className="flex-1 bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-sm font-bold focus:outline-none focus:ring-2 focus:ring-red-300" />
                          <button onClick={() => handleBuy(customPercent)}
                            disabled={isProcessing}
                            className="bg-red-500 hover:bg-red-600 text-white font-black px-4 rounded-xl text-sm transition-all disabled:opacity-40">
                            확인
                          </button>
                        </div>
                        <button onClick={() => { setMode(null); setCustomPercent('') }}
                          className="text-slate-300 hover:text-slate-400 font-bold py-1 text-xs uppercase tracking-widest">
                          취소
                        </button>
                      </div>
                    )}

                    {/* 매도 퍼센트 선택 */}
                    {mode === 'sell' && (
                      <div className="flex flex-col gap-2">
                        <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">보유 주식의 몇 % 매도?</p>
                        <div className="grid grid-cols-3 gap-2">
                          {[25, 50, 100].map(p => (
                            <button key={p} onClick={() => handleSell(p)}
                              className="bg-blue-50 hover:bg-blue-500 hover:text-white text-blue-500 font-black py-3 rounded-xl text-sm border border-blue-100 transition-all">
                              {p}%
                            </button>
                          ))}
                        </div>
                        <div className="flex gap-2 mt-1">
                          <input type="number" placeholder="직접 입력 %"
                            value={customPercent} onChange={e => setCustomPercent(e.target.value)}
                            className="flex-1 bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-sm font-bold focus:outline-none focus:ring-2 focus:ring-blue-300" />
                          <button onClick={() => handleSell(customPercent)}
                            disabled={isProcessing}
                            className="bg-blue-500 hover:bg-blue-600 text-white font-black px-4 rounded-xl text-sm transition-all disabled:opacity-40">
                            확인
                          </button>
                        </div>
                        <button onClick={() => { setMode(null); setCustomPercent('') }}
                          className="text-slate-300 hover:text-slate-400 font-bold py-1 text-xs uppercase tracking-widest">
                          취소
                        </button>
                      </div>
                    )}

                    {/* 오늘 시세 */}
                    {todayCandle && (
                      <div className="bg-slate-50 rounded-2xl p-5 border border-slate-100 mt-auto">
                        <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-3">오늘 시세</p>
                        <div className="grid grid-cols-2 gap-y-2 text-xs">
                          <div>
                            <p className="text-slate-400 font-bold">시가</p>
                            <p className="font-black text-slate-700">{fmt(todayCandle.open)}원</p>
                          </div>
                          <div>
                            <p className="text-slate-400 font-bold">종가</p>
                            <p className="font-black text-slate-700">{fmt(todayCandle.close)}원</p>
                          </div>
                          <div>
                            <p className="text-slate-400 font-bold">고가</p>
                            <p className="font-black text-red-400">{fmt(todayCandle.high)}원</p>
                          </div>
                          <div>
                            <p className="text-slate-400 font-bold">저가</p>
                            <p className="font-black text-blue-400">{fmt(todayCandle.low)}원</p>
                          </div>
                          <div className="col-span-2">
                            <p className="text-slate-400 font-bold">거래량</p>
                            <p className="font-black text-slate-700">{todayCandle.volume.toLocaleString()}</p>
                          </div>
                        </div>
                      </div>
                    )}
                  </>
                ) : (
                  /* 게임 종료 화면 */
                  <div className="bg-slate-50 rounded-2xl p-6 text-center border border-slate-100">
                    <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-2">Game Over</p>
                    <p className="text-xl font-black text-slate-900 mb-2">30일 종료!</p>
                    {cash + shares * currentPrice <= 200 ? (
                      <div className="mb-4">
                        <p className="text-2xl font-black text-slate-900 mb-1">파산!</p>
                        <p className="text-sm text-slate-400">자산이 200원 이하로 떨어졌어요</p>
                        <p className="text-sm font-black text-blue-500 mt-2">자본금 1,000만원으로 초기화됐어요</p>
                      </div>
                    ) : (
                     <p className={`text-2xl font-black mb-4 ${profit >= 0 ? 'text-red-500' : 'text-blue-500'}`}>
                       {profit >= 0 ? '+' : ''}{fmt(profit)}원
                     </p>
                    )}
                    <div className="flex items-center gap-2 justify-center mb-6">
                      <div className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
                      <p className="text-[10px] font-bold text-emerald-500 uppercase tracking-widest">
                        자동 저장 완료
                      </p>
                    </div>
                    <button
                      onClick={handleReset}
                      className="bg-slate-900 hover:bg-blue-600 text-white px-8 py-3 rounded-xl text-xs font-black uppercase tracking-widest transition-all w-full"
                    >
                      다시 시작
                    </button>
                  </div>
                )}

              </div>
            </div>
          </div>
        )}

      </div>
    </div>
  )
}

export default StockGame
