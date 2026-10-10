import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,              // bind 0.0.0.0 for the preview network
    port: 3000, // reserved preview port for this chat
    // exact preview host for this VM (set VITE_PREVIEW_HOST when it changes)
    allowedHosts: [
      'pv-c144c45cf3b3-51ba47b5-0ac4-41f9-8bd3-4eb08ebd494e.style.dev',
      ...(process.env.VITE_PREVIEW_HOST ? [process.env.VITE_PREVIEW_HOST] : []),
    ],
    proxy: {
      '/api': { target: 'http://127.0.0.1:8000', changeOrigin: true },
      '/predict': { target: 'http://127.0.0.1:8000', changeOrigin: true },
    },
  },
})
