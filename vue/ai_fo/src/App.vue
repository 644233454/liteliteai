
<template>
  <router-view :key="route.fullPath" />
</template>

<script setup lang="ts">
import {onMounted,ref } from 'vue'
import { useRoute } from 'vue-router'

const isShowStart = ref(true)
const route = useRoute()

onMounted(()=>{

})
</script>

<style lang='scss' scoped>
.body{
 margin: 0;
 background-color: red;
}
</style>



