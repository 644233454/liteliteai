import { createApp } from 'vue'
// import './style.css'
import App from './App.vue'
import vant from 'vant'
import { ConfigProvider } from 'vant'
import router from '@/router'
import 'vant/lib/index.css'
import '@/styles/index.scss'


const app = createApp(App)

app.use(router)
app.use(vant)
app.use(ConfigProvider)
app.mount('#app')

