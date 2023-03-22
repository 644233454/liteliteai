<template>
<div class='question-content'>
  <div class="title">{{ count}}个烦恼已回答</div>
  <div class="list-item" v-for="(item,index) in list" :key="index" @click="questionDetail"
  >
  {{ item.text }}
  </div>
  <van-overlay :show="visible" @click="visible = false">
  <div class="wrapper" >
   <div class="block" @click.stop>
    <div class="title">{{title}}</div>
    <div class="content">{{ content }}</div>
   </div>
   <img :src="Close" class="close" />
  </div>
</van-overlay>
</div>
</template>
<script setup lang='ts'>

import { ref,onMounted,nextTick } from 'vue'
import Close from '@/assets/close.svg'


interface ListItem {
  text: string;
}

const count = ref(3423)
const list = ref<ListItem[]>([])
const visible = ref(false)
const title = ref("为什么会一段时间一段时间感觉自己处于逆境中")
const content = ref("亲爱的朋友，我理解你的感受。有时候我们会感到自己处于逆境中，。")

onMounted(()=>{
  for (var i = 1; i <= 10; i++) {
    const item = {
      text:"烦恼问题烦恼问题烦恼问题烦恼问题烦恼问题烦恼问题" + i
    }
    list.value.push(item)
  }
})
const questionDetail = ()=>{
  visible.value = true
}


</script>
<style lang='scss' scoped>
 .question-content{
    display: flex;
    flex-direction: column;
    align-items: center;
    .title{
      text-align: center;
      height: 40px;
      line-height: 22px;
      font-weight: 500;
      font-size: 14px;
    }
    .list-item{
      width: 100%;
      border: 1px solid rgba(0, 0, 0, 0.1);
      border-radius: 8px;
      padding: 12px;
      line-height: 24px;
      align-items: center;
      margin-bottom: 8px;
      // overflow: hidden;
      // text-overflow: ellipsis;
      // white-space: nowrap;
    }
    .wrapper{
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100%;
      .block {
        width: calc(100% - 48px);
        max-height: calc(50% - 50px);
        background-color: #fff;
        display: flex;
        flex-direction: column;
        padding: 24px 10px;
        border-radius: 8px;
        .title{
          padding: 10px;
          font-weight: 500;
          font-size: 15px;
          flex-shrink: 1;
          text-align: start;
        }
        .content{
          flex-grow: 1;
          margin-top: 10px;
          font-weight: 400;
          font-size: 14px;
          overflow-y: auto;
        }
      }
      .close{
        margin-top: 20px;
      }
    }
  }

</style>