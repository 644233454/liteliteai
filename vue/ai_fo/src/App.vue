
<template>
  <router-view :key="route.fullPath" />
</template>

<script setup lang="ts">
import {onMounted,ref } from 'vue'
import { useRoute } from 'vue-router'
import Mp3 from '@/assets/guanyinxinzhou.mp3'
import {useAppStore} from '@/store/index'

const userStore = useAppStore()

const audioRef = ref<HTMLAudioElement>()
const isShowStart = ref(true)
const route = useRoute()



onMounted(()=>{


  

  // document.body.addEventListener('scroll', function() {
  //   // do something when scrolling
  //   console.log('scrollscrollscrollscrollscroll')
  //   });

  //   window.addEventListener('scroll', function() {
  //   // do something when scrolling
  //   console.log('window scrollscrollscrollscrollscroll')
  //   });
    // jsSdk.ready(function() {
    //   console.log('jsSdk.ready')
    //   audioRef.value?.play()
    //   });
    // document.addEventListener(
    //   "WeixinJSBridgeReady",
    //   function() {
    //     console.log('addEventListener')
    //     console.log('audioRef.value =',audioRef.value)
    //     // audioRef.value?.play()
    //     audioRef.value?.pause()
    //     setTimeout(() => {
    //       console.log('setTimeout')
    //       audioRef.value?.play()
    //     }, 1000);
    //   },
    //   false
    // );
})


</script>

<style lang='scss' scoped>
.warp{
  overflow: auto;
}
</style>



