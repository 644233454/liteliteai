import { createRouter, createWebHashHistory } from 'vue-router'

export const routerHistory = createWebHashHistory('/')
export const isWebHashHistory = routerHistory.base.includes('#')

// 正常路由加载,会将所有路由的js跟css合并到一个文件
// 首页
import {MainView} from '@/views/index'

// 路由配置
const routes = [
  { path: '/', name: 'main', component: MainView },

]

const router = createRouter({
  history: routerHistory,
  routes,
})
export default router
