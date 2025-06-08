<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="text-center mb-4" style="margin-top: 90px">
          <h2>비밀번호 변경</h2>
        </div>

        <form @submit.prevent="submitPasswordChange">
          <div class="mb-3">
            <input
              type="password"
              v-model="oldPassword"
              placeholder="기존 비밀번호"
              class="form-control"
              required
            />
          </div>

          <div class="mb-3">
            <input
              type="password"
              v-model="password"
              placeholder="새 비밀번호"
              class="form-control"
              required
            />
          </div>

          <div class="mb-3">
            <input
              type="password"
              v-model="passwordConfirm"
              placeholder="비밀번호 확인"
              class="form-control"
              required
            />
          </div>

          <div class="d-grid gap-2">
            <button type="submit" class="btn btn-info">비밀번호 변경</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Swal from 'sweetalert2'
import { changePasswordApi } from '@/apis/userApi'

const router = useRouter()
const route = useRoute()
const token = localStorage.getItem('token')
console.log('토큰 값:', token)

const oldPassword = ref('')
const password = ref('')
const passwordConfirm = ref('')

const alertMessage = (msg) => {
  Swal.fire({
    title: msg,
    icon: 'error',
    confirmButtonColor: '#682cd48c',
    confirmButtonText: '확인'
  })
}

const submitPasswordChange = () => {
  if (!oldPassword.value) {
    alertMessage('기존 비밀번호를 입력해주세요')
    return
  }

  if (!password.value) {
    alertMessage('새 비밀번호를 입력해주세요')
    return
  }

  if (password.value !== passwordConfirm.value) {
    alertMessage('비밀번호가 일치하지 않습니다')
    return
  }

  changePasswordApi(token, {
    old_password: oldPassword.value,
    new_password: password.value
  })
    .then(() => {
      Swal.fire({
        title: '비밀번호가 변경되었습니다.',
        icon: 'success',
        confirmButtonColor: '#3085d6',
        confirmButtonText: '확인'
      }).then(() => {
        router.push(`/user/profile/${route.params.userId}/pick`)
      })
    })
    .catch(err => {
      alertMessage('비밀번호 변경 실패: ' + err)
    })
}
</script>