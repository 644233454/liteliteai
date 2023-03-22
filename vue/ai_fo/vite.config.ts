import { defineConfig,loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import {resolve} from 'path'



export default defineConfig(({mode})=>{

  const env = loadEnv(mode, process.cwd())
  return  {
    base: './',
    plugins: [vue()],
    resolve: {
      alias: {
        '@': resolve(__dirname, './src'),
      },
    },
    server: {
      host: true,
      port: 8011,
      proxy: {
        '/ws': {
          changeOrigin: true,
          ws:true,
          target: env.VITE_API_PROXY,
          // rewrite: (path)=> path.replace(/~\/ws/,""), //拦截路径去除
        },
      },
    },
  }
})
