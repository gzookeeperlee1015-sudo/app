import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Dashboard  from './pages/Dashboard.jsx'
import StockGame  from './pages/StockGame.jsx'
import Screener   from './pages/Screener.jsx'
import AiInsight  from './pages/AiInsight.jsx'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* 메인 대시보드 */}
        <Route path="/"           element={<Dashboard />} />
        {/* 주식 미니게임 */}
        <Route path="/game"       element={<StockGame />} />
        {/* 종목 스크리너 */}
        <Route path="/screener"   element={<Screener />} />
        {/* AI 분석 인사이트 */}
        <Route path="/ai-insight" element={<AiInsight />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
