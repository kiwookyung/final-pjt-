<!-- src/components/common/ScrollButton.vue -->
<!-- ScrollButton.vue -->
<template>
  <div class="scroll-buttons">
    <button class="scroll-btn" @click="scrollToTop" title="맨 위로 이동">
      <!-- 위로 화살표 SVG -->
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="white"
        class="icon">
        <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 18.75 7.5-7.5 7.5 7.5" />
        <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 7.5-7.5 7.5 7.5" />
      </svg>
    </button>
    <button class="scroll-btn" @click="scrollToBottom" title="맨 아래로 이동">
      <!-- 아래로 화살표는 위 SVG를 뒤집거나 다른 아이콘을 사용 -->
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
        class="size-6">
        <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 5.25 7.5 7.5 7.5-7.5m-15 6 7.5 7.5 7.5-7.5" />
      </svg>
    </button>
  </div>
</template>


<script setup>
const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const scrollToBottom = () => {
  window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })
}
</script>

<style scoped>
.scroll-buttons {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
  z-index: 1000;
}

.scroll-btn {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(4px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  font-size: 1.5rem;
  border-radius: 50%;
  width: 48px;
  height: 48px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
}

.scroll-btn:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: scale(1.1);
}
</style>
