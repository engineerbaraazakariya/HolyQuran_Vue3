import legacy from '@vitejs/plugin-legacy'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import { defineConfig } from 'vite'

export default defineConfig(({ command, mode }) => {
  // تحديد قيمة base حسب الـ mode
  const base = mode === 'web' ? '/HolyQuran/' : '/'

  return {
    base,

    plugins: [
      vue(),
      legacy()
    ],

    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
      },
    },

    build: {
      rollupOptions: {
        output: {
          entryFileNames: 'assets/[name].js',
          chunkFileNames: 'assets/[name].js',
          assetFileNames: 'assets/[name][extname]',
        }
      }
    },

    test: {
      globals: true,
      environment: 'jsdom'
    }
  }
})
