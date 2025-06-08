<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="text-center mb-4" style="margin-top: 90px">
          <h2>회원정보 수정</h2>
        </div>

        <form @submit.prevent="submitEdit">
         

          <div class="mb-3">
            <label for="username" class="form-label">Email</label>
            <input v-model="username" type="text" class="form-control" id="username" placeholder="사용자명을 입력하세요" required />
          </div>

          <!-- 버튼 -->
          <div class="d-grid gap-2">
            <button type="submit" class="btn btn-info">수정 완료</button>
            <button type="button" @click="cancelEdit" class="btn btn-secondary mt-2">취소</button>
          </div>
        </form>

        <!-- 비밀번호 변경 -->
        <button @click="goToChangePassword" class="btn btn-warning mt-3">
          비밀번호 변경
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Swal from 'sweetalert2'
import { userProfileApi, updateUserProfileApi } from '@/apis/userApi'
import { useUserStore } from '@/stores/userStore'   // 여기 임포트 꼭 추가

const router = useRouter()
const route = useRoute()
const token = localStorage.getItem('token')

const userStore = useUserStore()   // 유저 스토어 사용

// 상태 변수
const email = ref('')
const username = ref('')

// 알림 함수
const alertMessage = (msg) => {
  Swal.fire({
    title: msg,
    icon: 'error',
    confirmButtonColor: '#682cd48c',
    confirmButtonText: '확인'
  })
}

// 프로필 정보 불러오기
const loadProfile = () => {
  userProfileApi(route.params.userId)
    .then(res => {
      email.value = res.data.email
      username.value = res.data.username
    })
    .catch(() => {
      alertMessage('프로필 정보를 불러오는데 실패했습니다.')
      router.back()
    })
}

// 수정 요청 보내기
const submitEdit = () => {
  if (!email.value || !username.value) {
    alertMessage('모든 항목을 입력해주세요')
    return
  }

  const formData = new FormData()
  formData.append('email', email.value)
  formData.append('username', username.value)

  updateUserProfileApi(token, route.params.userId, formData)
    .then(res => {
      // 프로필 수정 성공 시 유저 스토어에 데이터 즉시 업데이트
      userStore.updateUserData({
        pk: route.params.userId,
        username: username.value
      })

      Swal.fire({
        title: '프로필이 수정되었습니다.',
        icon: 'success',
        confirmButtonColor: '#3085d6',
        confirmButtonText: '확인'
      }).then(() => {
        router.push(`/user/profile/${route.params.userId}/info`)
      })
    })
    .catch(err => {
      alertMessage('수정 실패: ' + err)
    })
}

// 취소 버튼
const cancelEdit = () => {
  router.back()
}

// 비밀번호 변경 이동
const goToChangePassword = () => {
  router.push(`/user/profile/${route.params.userId}/change-password`)
}

// 페이지 진입 시 데이터 로드
onMounted(() => {
  loadProfile()
})
</script>