import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],
  // 👇 이 부분을 추가해 줍니다! (중복된 React를 하나로 합쳐주는 설정)
  resolve: {
    dedupe: ['react', 'react-dom'],
  }
})