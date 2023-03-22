<template>
  <div class="content">
   <div class='head'>
    <div class="back_view">
     
     <div class="left"></div>
     <van-image class="logo"  :src="MainHead"></van-image>
    </div>
     <div class="tip">
       -<br />施主，<br />说出你的烦恼
     </div>
   </div>
   <div class="bottom">
     <van-field 
       type="textarea"
       class="input"
       v-model="content" 
       autosize
       placeholder="佛祖，人生的意义是什么？" />
     <div class="input-tip">请不要输入个人信息。此外，如果有关于佛教方面的任何不准确之处，请宽容地接受。</div>
     <van-button class="reply-btn" :loading="replyLoading" type="success" loading-text="佛陀回答中..."  @click="reply">
     <div>
       向佛陀咨询
       <img :src="ReplyIcon" class="reply_icon" />
     </div >
     </van-button>
     <div class="reply_content" v-if="showReply">
       <div class="reply_content_title">佛曰</div>
       <div class="reply_content_info">{{ replyText }}</div>
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
     <div class="reply_content" v-else>
       <QuestionList class="question_view"/>
     </div>
   </div>
  </div>
 
 
 </template>
 <script setup lang='ts'>
 import { ref,nextTick,onMounted } from 'vue'
 import MainHead from '@/assets/main_head.png'
 import ReplyIcon from '@/assets/reply_icon.svg'
 import { QuestionList} from '@/components'
 import { useClipboard } from '@vueuse/core'
 import { showToast } from 'vant';

//  问题
 const content = ref()
//  定时器
 const timeCount = ref(0)
//  回答加载loading
 const replyLoading = ref(false)
//  是否展示回复内容的界面
 const showReply = ref(false)
 
//  回复的内容
 const replyText = ref('')
// 粘贴板
 const { copy } = useClipboard()
//  TODO 需要接入websocket
 const chat_id = "chat_app_fotuo"
 
// 界面加载完毕事件
 onMounted(()=>{
 

 })
// 复制当前url
 const copyURL = ()=>{
    const text =  location.href
    try {
      copy(text).then(() => {
        showToast('复制成功')
      })
    } catch (err) {
      showToast('复制失败')
      console.error(err)
    }

 }
 // 复制佛陀回答内容
 const copyContent = ()=>{
  try {
      copy(replyText.value).then(() => {
        showToast('复制成功')
      })
    } catch (err) {
      showToast('复制失败')
      console.error(err)
    }
}
//  点击咨询按钮 
// TODO 需要接入推流数据
 const reply = ()=>{
   console.log('佛陀回答');



// 以下是测试数据  接入实际数据时 需要删掉
   timeCount.value = 0
   replyLoading.value = true
    // 模拟网络数据
  const time =  setInterval(()=>{
    if(timeCount.value >= 10){
      clearInterval(time)
    }
    timeCount.value++,
    console.log('我是定时器')
    replyText.value = replyText.value + '我是定时器'
    document.body.scroll({
      top: document.body.scrollHeight,
      behavior: 'smooth'
    })
  },1000)
   setTimeout(() => {
     replyLoading.value = false
     showReply.value = true
   }, 1000);
 
 }
 
 
 </script>
 <style lang='scss' scoped>
 .content{
   display: flex;
   flex-direction: column;
   height: 100%;
   .head{
     width: 100%;
     flex-shrink: 0;
     height: 289px;
     position: relative;
     .back_view{
      z-index: 0;
      display: flex;
      .left{
       flex-grow:1;
      }
     }
     .tip{
      z-index: 1;
       position: absolute;
       float: left;
       left: 24px;
       bottom: 44px;
       font-size: 32px;
       line-height: 45px;
       font-weight: 600;
     }
  }
   .bottom{
     z-index: 1;
     display: flex;
     flex: 1;
     flex-direction: column;
     align-items: center;
     background-color: #F2F3F5;
     border-top-right-radius: 16px;
     border-top-left-radius: 16px;
     padding: 24px;
     .input{
       flex-shrink: 0;
         background: #FFFFFF;
         border: 1px solid rgba(255, 255, 255, 0.3);
         border-radius: 8px;
         font-size: 18px;
       }
       .input-tip{
         flex-shrink: 0;
         margin-top: 8px;
         width: calc(100% - 24px);
         color: #999999;
         font-weight: 400;
         font-size: 11px;
         line-height: 15px;
       }
       ::v-deep(.van-button__content){
           display: flex;
           flex-direction: row-reverse;
       }
       .reply-btn{
         flex-shrink: 0;
         margin-top: 18px;
         width: 100%;
         background-color: #000000;
         color: #FFFFFF;
         border-radius: 100px;
         height: 54px;
         .reply_icon{
           margin-left: 10px;
         }
       }
       .reply_content{
         flex-grow: 1;
         margin-top: 44px;
         display: flex;
         flex-direction: column;
         align-items: center;
         width: 100%;
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
       .question_view{
         margin-top: 44px;
         width: 100%;
       }
   }
 }
 
 
 </style>