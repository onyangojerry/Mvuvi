import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
// Vite config with proxy for backend API
// This proxy allows frontend code to use relative URLs (e.g., /api/v1/ocr/extract)
// and have them forwarded to the FastAPI backend at http://localhost:8000 during development.
// No CORS issues, and no need to hardcode backend URLs in React code.
//
// To use: just run `npm run dev` as usual. All /api requests will go to the backend.
//
// See: https://vitejs.dev/config/server-options.html#server-proxy

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
      // Optionally, proxy WebSocket if needed:
      // '/ws': {
      //   target: 'ws://localhost:8000',
      //   ws: true,
      // },
    },
  },
})
