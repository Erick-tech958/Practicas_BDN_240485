import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  root: 'docs',
  base: './',
  publicDir: '../data',
  build: { outDir: '../dist', emptyOutDir: true },
});
