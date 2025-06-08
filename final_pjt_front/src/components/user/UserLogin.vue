<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="text-center mb-4">
          <h2>로그인</h2>
        </div>
        <div class="mb-3">
          <label for="email" class="form-label">이메일</label>
          <input
            v-model="username"
            type="email"
            class="form-control"
            id="email"
            placeholder="you@example.com"
          />
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">비밀번호</label>
          <input
            v-model="password"
            @keyup.enter="logIn"
            type="password"
            class="form-control"
            id="password"
          />
        </div>
        <div class="d-grid gap-2">
          <button @click="logIn" class="btn btn-info mt-4">로그인</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/userStore'
import Swal from 'sweetalert2'

// 로그인
const username = ref(null)
const password = ref(null)
const userStore = useUserStore()

const alertMessage = (msg) => {
  Swal.fire({
    title: `${msg} 입력해주세요`,
    icon: 'error',
    confirmButtonColor: '#682cd48c',
    confirmButtonText: '확인'
  })
}

const logIn = () => {
  if (!username.value) {
    alertMessage('아이디를')
    return
  }
  if (!password.value) {
    alertMessage('비밀번호를')
    return
  }

  const payload = {
    username: username.value,
    password: password.value
  }
  userStore.loginUser(payload)
}
</script>

<style></style>
