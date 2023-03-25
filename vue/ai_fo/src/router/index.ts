import { createRouter, createWebHashHistory } from 'vue-router'

export const routerHistory = createWebHashHistory('/')
export const isWebHashHistory = routerHistory.base.includes('#')


// 首页
import {MainView,TextView,Reply} from '@/views/index'

// 路由配置
const routes = [
  { path: '/', name: 'main', component: MainView },
  { path: '/main_test', name: 'main_test', component: TextView },
  { path: '/reply', name: 'reply', component: Reply },
]

const router = createRouter({
  history: routerHistory,
  routes,
})
export default router
