<template>
<div class='content'>
  <van-nav-bar
      title="AI佛陀"
      left-arrow
      @click-left="backClick"
    />
    <div class="reply_content">
       <div class="reply_content_title">佛曰</div>
       <div class="reply_content_info">{{ userStore.AIReply }}</div>
       <div class="btn_arr">
         <van-button class="copy_url" @click="copyURL">
          渡化众生
         </van-button>
         <div class="middle"/>
         <van-button class="copy_content" @click="copyContent">
          复制佛言
         </van-button>
       </div>
     </div>
     <div class="bottom">
      <van-image class="bottom-icon" :src="Bottom"></van-image>
     </div>
</div>
</template>
<script setup lang='ts'>
import router from '@/router'
import { copyToClipboard } from "@/utils/tools"
import { showToast } from 'vant'
import {useAppStore} from '@/store/index'
import Bottom from '@/assets/bottom.png'

const userStore = useAppStore()
// 返回
const backClick = () => {
  userStore.setAIReply('')
  router.go(-1)
}
// 复制当前url
const copyURL = ()=>{
    const text =  location.href
    copyToClipboard(text).then(data =>{
      showToast('复制成功')
    }).catch(error =>{
      showToast('复制失败')
    })
 }
 // 复制佛陀回答内容
 const copyContent = ()=>{
  const text =  userStore.AIReply
    copyToClipboard(text).then(data =>{
      showToast('复制成功')
    }).catch(error =>{
      showToast('复制失败')
    })
}
</script>
<style lang='scss' scoped>
.content{
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  .reply_content{
    width: calc(100% - 48px);
    padding: 24px;
    flex-grow: 1;
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
        .reply_content_title{
          height: 42px;
          line-height: 22px
        }
        .reply_content_info{
          margin-top: 5px;
          padding: 12px;
          border: 1px solid rgba(0, 0, 0, 0.1);
          border-radius: 8px;
          width: 100%;
        }
        .btn_arr{
        display: flex;
        justify-content: space-around;
        width: 100%;
        height: 70px;
        margin-top: 20px;
        .copy_url{
          background-color: #000000;
          color: #FFFFFF;
          height: 46px;
          border-radius: 100px;
          flex: 1;
        }
        .middle{
          flex-shrink: 0;
          width: 20px;
        }
        .copy_content{
          background-color: #999999;
          color: #FFFFFF;
          border-radius: 100px;
          flex: 1;
        }
     }
  }
  .bottom{
    display: flex;
    justify-content: center;
    .bottom-icon{
      height: 104px;
      width: 212px;
    }
  } 
  ::v-deep(.van-icon-arrow-left){
    color: #000000;
  } 
}
</style>