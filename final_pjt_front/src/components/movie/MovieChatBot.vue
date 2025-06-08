<template>
  <div class="chatbot-wrapper" v-if="isChatOpen">
    <div class="chat-window">
      <div
        v-for="(msg, index) in chatHistory"
        :key="index"
        class="chat-bubble"
        :class="msg.role"
      >
        <p v-if="msg.loading">💬 답변을 불러오는 중...</p>
        <p v-else v-html="formatText(msg.content)"></p>
      </div>
    </div>

    <div class="input-area">
      <input
        v-model="userInput"
        type="text"
        placeholder="영화에 대해 물어보세요..."
        @keyup.enter="handleSend"
        :disabled="isLoading"
      />
      <button @click="handleSend" :disabled="isLoading">
        <span v-if="isLoading">⏳</span>
        <span v-else>➤</span>
      </button>
    </div>
  </div>

  <!-- 토글 버튼 -->
  <img
    src="@/assets/ai_icon.png"
    alt="AI 토글"
    class="ai-toggle-button"
    @click="toggleChat"
  />
</template>

<script setup>
import { ref } from 'vue'
import { askChatbot } from '@/apis/chatApi'

const userInput = ref('')
const chatHistory = ref([])
const isChatOpen = ref(false)
const isLoading = ref(false)

const toggleChat = () => {
  isChatOpen.value = !isChatOpen.value
}

const handleSend = async () => {
  const message = userInput.value.trim()
  if (!message || isLoading.value) return

  // 사용자 메시지 추가
  chatHistory.value.push({ role: 'user', content: message })
  userInput.value = ''
  isLoading.value = true

  // 로딩 메시지 추가
  const loadingIndex = chatHistory.value.push({ role: 'assistant', content: '', loading: true }) - 1

  try {
    const res = await askChatbot(message)
    chatHistory.value[loadingIndex] = { role: 'assistant', content: res.data.reply }
  } catch (err) {
    chatHistory.value[loadingIndex] = {
      role: 'assistant',
      content: '⚠️ 오류가 발생했습니다. 다시 시도해주세요.',
    }
  } finally {
    isLoading.value = false
  }
}

// 줄바꿈과 마크다운 기초 처리
const formatText = (text) => {
  return text.replace(/\n/g, '<br />')
             .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
}
</script>

<style scoped>
.chatbot-wrapper {
  position: fixed;
  bottom: 90px;
  right: 1.5rem;
  width: 320px;
  height: 420px;
  background-color: #1c1c1c;
  color: #f1f1f1;
  border-radius: 12px;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
  z-index: 999;
}

.chat-window {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
}

.chat-bubble {
  max-width: 85%;
  padding: 0.6rem 1rem;
  margin-bottom: 0.6rem;
  border-radius: 1rem;
  word-break: break-word;
  white-space: pre-wrap;
}

.chat-bubble.user {
  align-self: flex-end;
  background-color: #517397;
  color: white;
  text-align: right;
  margin-left: auto;
}

.chat-bubble.assistant {
  align-self: flex-start;
  background-color: #333;
  color: #eee;
}

.input-area {
  display: flex;
  padding: 0.6rem;
  background-color: #222;
  border-top: 1px solid #444;
}

input {
  flex: 1;
  border: none;
  padding: 0.5rem 0.75rem;
  background: #333;
  color: white;
  border-radius: 20px;
  outline: none;
}

button {
  background: #007bff;
  color: white;
  border: none;
  padding: 0 1rem;
  margin-left: 0.5rem;
  border-radius: 20px;
  cursor: pointer;
  font-weight: bold;
}

.ai-toggle-button {
  position: fixed;
  bottom: 1.5rem;
  right: 1.5rem;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: white;
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.2);
  cursor: pointer;
  z-index: 999;
}
</style>
