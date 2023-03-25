import { defineStore } from 'pinia'


export const useAppStore = defineStore('app', {
  state: () => ({
    showTabbar:false, // 是否展示导航
    AIReply:''  // ai回复
  }),
  getters: {
    getShowTabbar(state) {
      return state.showTabbar
    },
    getAIReply(state) {
      return state.AIReply
    },

  },
  actions: {
    setShowTabbar(show:boolean){
      this.showTabbar = show
    },
    setAIReply(content:string){
      console.log('content=',content)
      this.AIReply = content
    }
  },
})