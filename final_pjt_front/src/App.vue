<template>
  <div id="app" class="app-container">
    <HeaderNavbar />
    <RouterView />
  </div>
</template>

<script setup>
import HeaderNavbar from '@/components/common/HeaderNavbar.vue'
import '@/assets/css/global-splide-style.css'
import '@/assets/css/layout.css'
</script>

<style>
body {
  background-color: #111 !important;
  color: white !important;
  font-family: 'Noto Sans KR', sans-serif;
  margin: 0;
}

.app-container {
  min-width: 1000px; /* nav-bar 고정폭 기준 */
  overflow-x: auto;   /* 전체 페이지 가로 스크롤 허용 */
}

</style>

