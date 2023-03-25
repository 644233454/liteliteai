import { createApp } from 'vue'
import App from './App.vue'
import vant from 'vant'
import { ConfigProvider } from 'vant'
import { createPinia } from 'pinia'
import router from '@/router'
import 'vant/lib/index.css'
import '@/styles/index.scss'

 
(async () => {
  if (
    import.meta.env.MODE === 'development'
    || import.meta.env.MODE === 'daily'
    || import.meta.env.MODE === 'dev'
    || import.meta.env.MODE === 'test'
  ) {
    const { default: VConsole } = await import('vconsole')
    new VConsole()
  }
})()

const pinia = createPinia()

const app = createApp(App)
app.use(pinia)
app.use(router)
app.use(vant)
app.use(ConfigProvider)
app.mount('#app')




