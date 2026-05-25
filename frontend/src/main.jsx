import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css' // 이 파일이 src/index.css인지 다시 한번 확인하세요!
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)