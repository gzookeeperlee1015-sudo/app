import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Dashboard from './pages/Dashboard.jsx'
import StockGame from './pages/StockGame.jsx'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* 기존 대시보드 */}
        <Route path="/" element={<Dashboard />} />
        {/* 주식 미니게임 */}
        <Route path="/game" element={<StockGame />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
