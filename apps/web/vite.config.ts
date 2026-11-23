import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import { tanstackRouter } from '@tanstack/router-plugin/vite'
import { resolve } from 'node:path'

export default defineConfig({
  // base relativa para poder desplegar en un subpath (GitHub Pages /projecte/)
  base: './',
  plugins: [tanstackRouter({ target: 'react', autoCodeSplitting: true }), react(), tailwindcss()],
  resolve: { alias: { '@': resolve(__dirname, './src') } },
  server: {
    proxy: {
      '/api': {
        // En Docker (docker-compose.yml) se inyecta VCC_API_PROXY=http://api:3001;
        // en local se usa el backend de apps/api en localhost.
        target: process.env.VCC_API_PROXY ?? 'http://localhost:3001',
        changeOrigin: true,
      },
    },
  },
})
