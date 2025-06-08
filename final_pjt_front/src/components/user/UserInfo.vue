<template>
  <div class="profile-container bg-dark text-white shadow rounded-4 p-4 mt-5">
    <!-- 프로필 이미지 -->
    <div class="text-center mb-4">
      <img
        :src="user.profile_pic ? userProfilePic : AvatarSrc"
        alt="No Image"
        class="profile-pic rounded-circle border border-secondary shadow"
      />
    </div>

    <div class="text-center mb-3">
      <h3 class="fw-bold">{{ username }}</h3>
      <button
        v-if="isCurrentUser"
        @click="changeProfilePic"
        class="btn btn-outline-light mt-2"
      >
        프로필 사진 변경
      </button>
    </div>

    <hr class="border-secondary" />

    <!-- 유저 정보 -->
    <div class="user-details text-center">
      <div class="mb-2">
        <i class="bi bi-pencil-fill me-2 text-info"></i>
        작성한 기사 수: <strong>{{ user.articles_count }}</strong>
      </div>
      <div class="mb-2">
        <i class="bi bi-heart-fill me-2 text-danger"></i>
        좋아요 수: <strong>{{ user.like_count }}</strong>
      </div>
      <div class="mb-2">
        <i class="bi bi-calendar-check me-2 text-success"></i>
        가입일: <strong>{{ formattedDateJoined }}</strong>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import AvatarSrc from '@/assets/avatar.png'
import { profilePicEdit } from '@/apis/userApi'

const props = defineProps(['user', 'isCurrentUser'])

const username = computed(() => props.user.username.split('@')[0])
const userProfilePic = computed(() => `http://localhost:8000${props.user.profile_pic}`)

const selectedFile = ref(null)

const changeProfilePic = () => {
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = 'image/*'
  input.onchange = (e) => {
    selectedFile.value = e.target.files[0]
    uploadProfilePic()
  }
  input.click()
}

const uploadProfilePic = () => {
  const formData = new FormData()
  formData.append('profile_pic', selectedFile.value)

  profilePicEdit(props.user.id, formData)
    .then((response) => {
      if (response && response.data) {
        props.user.profile_pic = response.data.profile_pic
      } else {
        props.user.profile_pic = URL.createObjectURL(selectedFile.value)
      }
    })
    .catch((error) => {
      console.error(error)
    })
}

const formattedDateJoined = computed(() => {
  const date = new Date(props.user.date_joined)
  return new Intl.DateTimeFormat('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(date)
})
</script>

<style scoped>
.profile-container {
  max-width: 500px;
  margin: 0 auto;
  background-color: #1a1a1a; /* 어두운 카드 배경 */
  border: 1px solid #333;
}

.profile-pic {
  width: 150px;
  height: 150px;
  object-fit: cover;
  transition: transform 0.3s;
}

.profile-pic:hover {
  transform: scale(1.05);
}
</style>