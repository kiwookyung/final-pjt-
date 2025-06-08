<template>
  <header class="nav-header">
    <nav class="nav-bar" :class="{ open: isMobileMenuOpen }">
      <RouterLink to="/" class="logo">
        <img src="@/assets/logo.png" alt="ReeLoom 로고" class="logo-image" />
      </RouterLink>

      <!-- 장르 드롭다운 -->
      <div class="dropdown" :class="{ open: isGenreOpen }">
        <button @click="toggleGenreMenu" class="dropdown-btn" aria-haspopup="true"
          :aria-expanded="isGenreOpen.toString()">
          🎞️ {{ selectedGenreName }} ▼
        </button>

        <div v-if="isGenreOpen" class="dropdown-menu" role="menu">
          <button v-for="genre in genres" :key="genre.id" class="dropdown-item" role="menuitem"
            @click="goToGenre(genre.id)">
            {{ genre.name }}
          </button>
        </div>
      </div>


      <div class="nav-right">
        <!-- 검색창 -->
        <div class="search-container">
          <input v-model="search" type="text" placeholder="영화 검색..." class="search-input" @keyup.enter="goSearch" />
          <button @click="goSearch" class="search-button">🔍</button>
        </div>

        <RouterLink to="/community" class="btn">커뮤니티</RouterLink>

        <!-- 로그인 상태 분기 -->
        <template v-if="isLoggedIn">
          <RouterLink :to="`/user/profile/${userStore.userData.pk}/pick`" class="btn">
            <span>{{ userStore.userData.username }}</span>
          </RouterLink>
          <RouterLink to="/logout" class="btn">로그아웃</RouterLink>
        </template>
        <template v-else>
          <RouterLink to="/user/login" class="btn">로그인</RouterLink>
          <RouterLink to="/user/signup" class="btn">회원가입</RouterLink>
        </template>
      </div>
    </nav>
      <!-- 모바일 햄버거 버튼 -->
      <button class="mobile-menu-btn" @click="toggleMobileMenu" aria-label="메뉴 토글">
        ☰
      </button>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useUserStore } from '@/stores/userStore'
import { useRouter, useRoute } from 'vue-router'
import defaultAvatar from '@/assets/avatar.png'
import { getGenres } from '@/apis/movieApi'

const userStore = useUserStore()
const isLoggedIn = computed(() => !!userStore.token)
const router = useRouter()
const route = useRoute()

const search = ref('')
const isGenreOpen = ref(false)
const isMobileMenuOpen = ref(false)  // 모바일 메뉴 토글 상태
const genres = ref([])
const selectedGenreName = ref('장르 선택')

const toggleGenreMenu = () => {
  isGenreOpen.value = !isGenreOpen.value
}

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

const goToGenre = (genreId) => {
  const genre = genres.value.find(g => g.id === genreId)
  if (genre) selectedGenreName.value = genre.name
  router.push({ name: 'GenreMoreView', params: { genreId } })
  isGenreOpen.value = false
  isMobileMenuOpen.value = false  // 메뉴 선택시 모바일 메뉴 닫기
}

const goSearch = () => {
  if (search.value.trim()) {
    router.push({ name: 'SearchView', query: { query: search.value } })
    search.value = ''
    isGenreOpen.value = false
    isMobileMenuOpen.value = false // 검색 후 모바일 메뉴 닫기
  }
}

const fetchGenres = async () => {
  try {
    const res = await getGenres()
    genres.value = res.data
    updateSelectedGenreName()
  } catch (err) {
    console.error('장르 불러오기 실패', err)
  }
}

const updateSelectedGenreName = () => {
  if (route.name === 'GenreMoreView' && route.params.genreId && genres.value.length > 0) {
    const genre = genres.value.find(g => g.id == route.params.genreId)
    selectedGenreName.value = genre ? genre.name : '장르 선택'
  } else {
    selectedGenreName.value = '장르 선택'
  }
}

onMounted(() => {
  fetchGenres()
})

// 라우터 경로 바뀔 때마다 selectedGenreName 업데이트
watch(() => route.fullPath, () => {
  updateSelectedGenreName()
})

const userImage = computed(() => {
  const pic = userStore.userData?.profile_pic
  return pic ? `http://localhost:8000${pic}` : defaultAvatar
})
</script>

<style scoped>
.nav-header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 999;
  background-color: #222;
  padding: 1rem;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
}

.dropdown-menu {
  z-index: 2000; /* 높게 설정 */
  position: absolute;
}


.nav-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  flex-wrap: nowrap;
  min-width: 900px;
}

.logo {
  color: #fff;
  font-size: 1.5rem;
  font-weight: bold;
  text-decoration: none;
  white-space: nowrap;
  margin-right: auto;
}

.mobile-menu-btn {
  display: none;
}

.dropdown {
  position: relative;
  user-select: none;
}

.dropdown-btn {
  background-color: #444;
  border: none;
  color: white;
  font-size: 1rem;
  cursor: pointer;
  padding: 0.4rem 0.8rem;
  border-radius: 4px;
  transition: background-color 0.2s ease;
  white-space: nowrap;
}

.dropdown-btn:hover {
  background-color: #682cd4;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  background-color: #222;
  border-radius: 6px;
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.4);
  padding: 0.5rem 0;
  display: flex;
  flex-direction: column;
  min-width: 160px;
  z-index: 1000;
}

.dropdown-item {
  background: none;
  border: none;
  color: white;
  padding: 0.6rem 1rem;
  text-align: left;
  cursor: pointer;
  font-size: 0.95rem;
  transition: background-color 0.2s ease;
}

.dropdown-item:hover {
  background-color: #682cd4;
  border-radius: 4px;
}

.nav-right {
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: nowrap;
  white-space: nowrap;
}

.search-container {
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.search-input {
  padding: 0.5rem;
  border-radius: 4px;
  border: none;
  min-width: 150px;
  max-width: 200px;
}

.search-button {
  background-color: #444;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0.5rem;
  cursor: pointer;
}

.btn {
  color: rgba(255, 255, 255, 0.466);
  text-decoration: none;
  font-weight: 500;
  white-space: nowrap;
}

.profile-pic {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 0.4rem;
}


.logo-image {
  height: 48px; /* 이미지 자체 크기 ↑ */
  margin-right: 0.5rem;
  object-fit: contain;
}


</style>
