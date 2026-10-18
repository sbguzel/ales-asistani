import { defineConfig } from 'vite';

export default defineConfig({
  root: './',
  server: {
    host: true,
    port: 3000,
    open: false
  },
  build: {
    outDir: 'dist',
    emptyOutDir: true,
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          firebase: ['firebase/app', 'firebase/auth', 'firebase/firestore'],
          katex: ['katex']
        }
      }
    }
  }
});
