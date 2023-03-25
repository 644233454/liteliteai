<template>
  <div class="content" @click="clickContent">
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
     <div class="reply_content" >
      <QuestionList class="question_view"/>
     </div>
   </div>
  </div>

  <audio
      ref="audioRef"
      class="audio"
      preload="metadata"
      controls
      loop
      :src="Mp3"
      :hidden="true"
      @ended="onEnded"
    />
 </template>
 <script setup lang='ts'>
 import { ref,onMounted,watch,nextTick } from 'vue'
 import MainHead from '@/assets/main_head.png'
 import ReplyIcon from '@/assets/reply_icon.svg'
 import { QuestionList} from '@/components'
 import { io } from 'socket.io-client';
 import { useRouter } from 'vue-router'
 import {useAppStore} from '@/store/index'
 import Mp3 from '@/assets/guanyinxinzhou.mp3'


const userStore = useAppStore()
const router = useRouter()
const audioRef = ref<HTMLAudioElement>()

const jsSdk = window.wx
//  问题
 const content = ref()
//  定时器
 const timeCount = ref(0)
//  回答加载loading
 const replyLoading = ref(false)
//  回复的内容
 const replyText = ref('')


 function generateRandomString(): string {
  const length = 10;
  const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let result = '';
  for (let i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * characters.length));
  }
  return result;
}


 const chat_id = "chat_app_fotuo_" + generateRandomString()

 // socket
 const socket = io("/");
 // 监听 chat_ws 消息事件
 socket.on("chat_ws", ({chat_id: receivedChatId, message: content}) => {
   if (receivedChatId === chat_id) {
     // 处理收到的消息
     replyText.value += content;
     userStore.setAIReply(replyText.value)
   }
 });
 socket.on('connect', () => {
   console.log('Connected to server');
   socket.emit('join', {'chat_id': chat_id});
 });

//  点击咨询按钮
 const reply = () => {
   console.log('佛陀回答');
   if (!content.value) {
     content.value = '佛祖，人生的意义是什么？'
   }
   replyLoading.value = true
   userStore.setAIReply('')
   replyText.value = ''
   socket.emit('fotuo_ws', {
     'msg': content.value,
     'chat_id': chat_id
   });

// 以下是测试数据  接入实际数据时 需要删掉
   timeCount.value = 0
    // 模拟网络数据
  const time =  setInterval(()=>{
    if(timeCount.value >= 10){
      clearInterval(time)
    }
    timeCount.value++,
    console.log('我是定时器')

    replyText.value = replyText.value + '我是定时器'

    console.log('replyText.value =',replyText.value)

    console.log('userStore =',userStore)

    userStore.setAIReply(replyText.value)

  },1000)
 }

 onMounted(()=>{
  const content = document.getElementsByClassName('content')[0]

  console.log('onMounted')

//  方案1
  // content.addEventListener('scroll', listenerScroll)
  // setTimeout(() => {
  //   content.scroll({
  //     top:  1,
  //     behavior: 'smooth',
  //     })
  //  }, 1000);

      // 方案五
  setTimeout(() => {
    console.log('setTimeout')
          const eventType = 'click'; 
          const event = new Event(eventType, {
            bubbles: true, // 事件是否冒泡
            cancelable: true, // 事件是否可取消
          });
          content.dispatchEvent(event); 
  }, 1000);
 
 })

 const clickContent = ()=>{
  console.log('clickContent')
  audioRef.value?.play()
 }

 const listenerScroll = ()=>{
  console.log('listenerScroll')
  // audioRef.value?.play()
 }
//  监听ai回复
 watch(()=>replyText.value,data =>{
  if(data.length > 0){
    replyLoading.value = false
    router.push({
      name: 'reply',
    })
  }
 })
 function onEnded(e: Event) {
  console.log('测试')
  audioRef.value?.load()

}

 </script>
 <style lang='scss' scoped>
 .content{
   display: flex;
   flex-direction: column;
   height: 100%;
   overflow: auto;
   .head{
     width: 100%;
     flex-shrink: 0;
     flex-basis: 289px;
     position: relative;
     .back_view{
      z-index: 0;
      display: flex;
      height: 300px;
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
     flex-shrink: 0;
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
         font-size: 15px;
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
