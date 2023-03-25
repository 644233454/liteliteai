<template>
  <div class="warp">
    <div class="content">
    <div class="top">
      <img class="icon"  :src="MainHead" />
    </div>
    <div class="bottom">
      <div class="test">123123123</div>
       <textarea class="content-input" v-model="content" />
    </div>
  </div>

  </div>
 

 </template>
 <script setup lang='ts'>
import { ref,onMounted } from 'vue'
 import MainHead from '@/assets/main_head.png'

const content = ref()
const list = ref([])


 </script>
 <style lang='scss' scoped>
 .warp{
  height: 100%;
  width: 100%;
  display: flex;
  overflow: auto;
  .content{
    width: 100%;
  flex-shrink: 0;
   display: flex;
   flex-direction: column;
   height: 100%;
   .top{

    flex-basis: 289px;
    flex-shrink: 0;
    // height: 289px;

    .icon{
      width: 100px;
      height: 200px;
    }

   }
   .bottom{
    flex-shrink: 0;
  //  height: calc(100% - 289px);
    flex-grow: 1;
    .test{
      width: 100%;
      height: 100px;
    }
    .input{
    border-color: red;
    width: 100%;
    height: 80px;
    }
   }
 }

 }
 


 </style>