import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Dashboard from './pages/Dashboard.jsx'
import StockGame from './pages/StockGame.jsx'
import Screener  from './pages/Screener.jsx'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/"         element={<Dashboard />} />
        <Route path="/game"     element={<StockGame />} />
        <Route path="/screener" element={<Screener />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App