import { defineConfig,loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import {resolve} from 'path'
import { createHtmlPlugin } from 'vite-plugin-html'



export default defineConfig(({mode})=>{

  const env = loadEnv(mode, process.cwd())
  const isShowDevtool = mode !== 'pro'


  console.log('mode =',mode);
  console.log('isShowDevtool =',isShowDevtool);

  return  {
    base: './',
    plugins: [
      vue(),
      // createHtmlPlugin({
      //   minify: true,
      //   inject: {
      //     ...env,
      //     data: {
      //       erudaScript: isShowDevtool ? '<script>import </script>' : '',
      //       erudaInit: isShowDevtool ? '<script>eruda.init()</script>' : '',
      //     },
      //   },
      // }),
    ],
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
