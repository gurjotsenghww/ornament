import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://localhost:5050',
      '/favicon.png': 'http://localhost:5050',
      '/bg.jpg': 'http://localhost:5050',
      '/preview': 'http://localhost:5050'
    }
  }
})
