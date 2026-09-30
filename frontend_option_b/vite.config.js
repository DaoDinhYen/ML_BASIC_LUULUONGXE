import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// Cấu hình Vite với Proxy kết nối Backend FastAPI (Port 8000)
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    open: true,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/reports': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      }
    }
  }
});
