<template>
  <div v-if="user" class="profile-page-wrapper" style="margin-top: 90px">
    <!-- 상단 고정 회원 정보 -->
    <div class="profile-header">
      <div class="profile-image">
        <img :src="user.profile_pic ? userProfilePic : AvatarSrc" alt="profile" />
        <div class="change-pic-btn-container">
          <button @click="changeProfilePic" class="change-pic-btn">프로필 사진 변경</button>
        </div>
      </div>
      <div class="profile-info">
        <h2>{{ username }}</h2>
        <p>가입일: {{ formattedDateJoined }}</p>
        <p>작성 리뷰: {{ user.articles_count }} | 좋아요: {{ user.like_count }}</p>
        <p>
          <span class="clickable" @click="showList = 'followings'">
            팔로잉: {{ user.following_count || 0 }}
          </span>
          |
          <span class="clickable" @click="showList = 'followers'">
            팔로워: {{ user.follower_count || 0 }}
          </span>
        </p>

        <!-- 내가 아닌 경우에만 팔로우 버튼 표시 -->
        <button v-if="!isCurrentUser" @click="toggleFollow" class="follow-btn" :class="{ following: isFollowing }">
          {{ isFollowing ? '언팔로우' : '팔로우' }}
        </button>

        <!-- 내가 맞다면 회원정보 수정/탈퇴 버튼 추가 -->
        <div v-if="isCurrentUser" class="user-actions">
          <button @click="editProfile" class="edit-btn">회원정보 수정</button>
          <button @click="deleteAccount" class="delete-btn">회원 탈퇴</button>
        </div>
      </div>
    </div>

    <!-- 하단 탭 메뉴 -->
    <div class="profile-tabs">
      <RouterLink class="tab" :to="`/user/profile/${user.id}/pick`" :class="{ active: route.path.includes('pick') }">픽
        영화</RouterLink>
      <RouterLink class="tab" :to="`/user/profile/${user.id}/article`"
        :class="{ active: route.path.includes('article') }">작성리뷰</RouterLink>
    </div>

    <!-- 선택된 탭 콘텐츠 -->
    <div class="tab-content">
      <RouterView :user="user" :isCurrentUser="isCurrentUser" />
    </div>

    <!-- 팔로워/팔로잉 리스트 모달 -->
    <UserFollower v-if="showList" :user="user" :show="showList" @close="showList = null" />
    <ChatBot/>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter, onBeforeRouteUpdate } from 'vue-router'
import {
  userProfileApi,
  followApi,
  unfollowApi,
  checkFollowingApi,
  deleteUserApi,
  profilePicEdit
} from '@/apis/userApi'
import AvatarSrc from '@/assets/avatar.png'
import UserFollower from '@/components/user/UserFollower.vue'
import { useUserStore } from '@/stores/userStore.js'
import ChatBot from '@/components/movie/MovieChatBot.vue'


const user = ref(null)
const route = useRoute()
const router = useRouter()
const userId = ref(route.params.userId)
const loggedInUserId = ref(localStorage.getItem('userPk'))
const token = localStorage.getItem('token')
const isCurrentUser = computed(() => loggedInUserId.value === userId.value)
const userStore = useUserStore()

// 팔로우 상태 관리
const isFollowing = ref(false)

// 리스트 보여줄 상태 ('followers', 'followings', null)
const showList = ref(null)

// 컴퓨티드
const username = computed(() => user.value?.username?.split('@')[0] || '')
const userProfilePic = computed(() =>
  user.value?.profile_pic ? `http://localhost:8000${user.value.profile_pic}` : ''
)

const formattedDateJoined = computed(() => {
  if (!user.value?.date_joined) return ''
  const date = new Date(user.value.date_joined)
  return new Intl.DateTimeFormat('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(date)
})

// 프로필 불러오기
const fetchUserProfile = () => {
  return new Promise((resolve, reject) => {
    let idToFetch = isCurrentUser.value ? loggedInUserId.value : userId.value
    userProfileApi(idToFetch)
      .then((response) => {
        user.value = response.data
        if (!isCurrentUser.value) {
          checkFollowing()
        }
        resolve()
      })
      .catch((err) => {
        alert(err)
        reject(err)
      })
  })
}

// 팔로우 상태 확인
const checkFollowing = () => {
  checkFollowingApi(token, userId.value)
    .then(res => {
      isFollowing.value = res.data.is_following
    })
    .catch(err => {
      console.error('팔로우 상태 확인 실패:', err)
    })
}

// 팔로우/언팔로우 토글
const toggleFollow = () => {
  if (isFollowing.value) {
    unfollowApi(token, userId.value)
      .then(() => {
        isFollowing.value = false
        user.value.follower_count = Math.max((user.value.follower_count || 1) - 1, 0)
      })
      .catch(err => {
        alert('언팔로우 실패: ' + err)
      })
  } else {
    followApi(token, userId.value)
      .then(() => {
        isFollowing.value = true
        user.value.follower_count = (user.value.follower_count || 0) + 1
      })
      .catch(err => {
        alert('팔로우 실패: ' + err)
      })
  }
}

// 라우트 변경 시 다시 불러오기
onBeforeRouteUpdate((to, from, next) => {
  if (to.params.userId !== from.params.userId) {
    userId.value = to.params.userId
    fetchUserProfile()
      .then(() => next())
      .catch(() => next())
  } else {
    next()
  }
})

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

  profilePicEdit(user.value.id, formData)
    .then((response) => {
      if (response && response.data) {
        user.value.profile_pic = response.data.profile_pic
      } else {
        user.value.profile_pic = URL.createObjectURL(selectedFile.value)
      }
    })
    .catch((error) => {
      console.error(error)
    })
}

const editProfile = () => {
  router.push(`/user/profile/${user.value.id}/edit`)
}

//회원 탈퇴
const deleteAccount = async () => {
  const confirmDelete = confirm("정말로 삭제하시겠습니까?");
  if (!confirmDelete) return;  // 사용자가 취소하면 함수 종료

  console.log("토큰:", userStore.token);
  console.log("유저 pk:", userStore.userData.pk);

  if (!userStore.token || !userStore.userData.pk) {
    alert("로그인 정보가 올바르지 않습니다. 다시 로그인 해주세요.");
    return;
  }

  try {
    await deleteUserApi(userStore.token, userStore.userData.pk);

    localStorage.removeItem("token");
    localStorage.removeItem("userPk");
    userStore.logout();
    router.push("/");

    alert("회원 탈퇴가 완료되었습니다.");
  } catch (error) {
    console.error("회원탈퇴 실패:", error);
    alert("회원 탈퇴에 실패했습니다.");
  }
};




onMounted(fetchUserProfile)
</script>

<style scoped>
.profile-page-wrapper {
  width: 100%;
  max-width: 100%;
  margin: 0 auto;
  padding: 20px;
  box-sizing: border-box;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 32px;
  margin-bottom: 32px;
  padding-bottom: 20px;
  border-bottom: 1px solid #444;
}

.profile-image img {
  width: 140px;
  height: 140px;
  object-fit: cover;
  border-radius: 50%;
  border: 3px solid #555;
}

.profile-info h2 {
  margin: 0;
  font-size: 2.6rem;
  color: white;
  font-weight: 700;
}

.profile-info p {
  margin: 8px 0;
  color: #ccc;
  font-size: 1.1rem;
}

.profile-tabs {
  display: flex;
  justify-content: space-around;
  margin-bottom: 24px;
  border-bottom: 2px solid #444;
}

.tab {
  padding: 12px;
  font-weight: bold;
  color: #aaa;
  text-decoration: none;
}

.tab.active {
  color: #e50914;
  border-bottom: 3px solid #e50914;
}

.tab:hover {
  color: #e50914;
}

.tab-content {
  padding: 12px 0;
}

.follow-btn {
  margin-top: 16px;
  padding: 12px 28px;
  font-weight: 700;
  border-radius: 30px;
  font-size: 1.2rem;
}

.follow-btn.following {
  background-color: #666;
}

.follow-btn:hover {
  background-color: #b0060f;
}

.clickable {
  font-size: 1.1rem;
  cursor: pointer;
  color: #e50914;
  font-weight: 600;
}

.clickable:hover {
  text-decoration: underline;
}

.user-actions {
  margin-top: 16px;
  display: flex;
  gap: 12px;
}

.edit-btn {
  padding: 8px 20px;
  background-color: #007bff;
  color: white;
  border-radius: 24px;
  border: none;
  cursor: pointer;
  font-weight: 600;
}

.edit-btn:hover {
  background-color: #0056b3;
}

.delete-btn {
  padding: 8px 20px;
  background-color: #dc3545;
  color: white;
  border-radius: 24px;
  border: none;
  cursor: pointer;
  font-weight: 600;
}

.delete-btn:hover {
  background-color: #a71d2a;
}

/* 반응형 */
@media (max-width: 800px) {
  .profile-page-wrapper {
    padding: 12px;
  }
}

@media (max-width: 480px) {
  .profile-header {
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 12px;
  }

  .profile-image img {
    width: 80px;
    height: 80px;
  }

  .profile-info h2 {
    font-size: 1.4rem;
  }

  .profile-tabs {
    flex-direction: column;
    gap: 8px;
  }

  .tab {
    padding: 8px;
  }
}

.change-pic-btn-container {
  margin-top: 12px;
  text-align: center;
}

.change-pic-btn {
  padding: 4px 12px;
  font-size: 0.9rem;
  border-radius: 16px;
  border: none;
  background-color: #e50914;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.change-pic-btn:hover {
  background-color: #b0060f;
}
</style>