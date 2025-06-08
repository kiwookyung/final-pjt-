<template>
  <div class="community-wrapper">
    <div class="title-area">
      <h1 class="title">CineTalk</h1>
      <p class="subtitle">영화를 사랑하는 사람들의 이야기</p>
    </div>


    <!-- 정렬 셀렉트 박스 -->
    <div class="select-wrapper">
      <select v-model="sortType" class="form-select w-auto">
        <option value="latest">최신순</option>
        <option value="likes">좋아요순</option>
      </select>
    </div>

    <!-- 헤더 -->
    <div class="list-header">
      <span class="title-col">제목</span>
      <span class="user-col">작성자</span>
      <span class="date-col">작성일</span>
      <span class="like-col">좋아요</span>
    </div>

    <!-- 게시글 목록 -->
    <div class="post-list">
      <div class="post-row" v-for="post in paginatedPosts" :key="post.id" @click="goToDetail(post.id)">
        <span class="title-col">{{ post.title }}</span>
        <span class="user-col">{{ post.user }}</span>
        <span class="date-col">{{ post.created_at.slice(0, 10) }}</span>
        <span class="like-col">❤️ {{ post.like_count }}</span>
      </div>
    </div>

    <!-- 글이 없을 경우 -->
    <div v-if="paginatedPosts.length === 0" class="empty-msg">
      아직 게시글이 없습니다. 첫 글을 작성해보세요!
    </div>

    <!-- 하단 고정 바 -->
    <div class="bottom-bar">
      <div class="pagination">
        <button @click="setPage(currentPage - 1)" :disabled="currentPage === 1">&lt;</button>
        <button v-for="page in totalPages" :key="page" @click="setPage(page)" :class="{ active: currentPage === page }">
          {{ page }}
        </button>
        <button @click="setPage(currentPage + 1)" :disabled="currentPage === totalPages">&gt;</button>
      </div>

      <div class="button-row">
        <RouterLink to="/" class="back-btn">메인으로</RouterLink>
        <RouterLink to="/community/create" class="write-btn">글쓰기</RouterLink>
      </div>
    </div>

    <!-- 하단 공간 확보용 -->
    <div class="bottom-spacer"></div>
  </div>
  <!-- index.html 또는 main.js에 추가 -->
  <link href="https://fonts.googleapis.com/css2?family=Cinzel&display=swap" rel="stylesheet">
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import axios from 'axios'

const posts = ref([])
const perPage = 10
const currentPage = ref(1)
const sortType = ref('latest')
const router = useRouter()

const fetchPosts = async () => {
  try {
    const res = await axios.get('http://localhost:8000/movies/community/', {
      headers: { Authorization: `Token ${localStorage.getItem('token')}` }
    })
    posts.value = res.data
  } catch (err) {
    console.error('게시글 불러오기 실패:', err)
  }
}

const sortedPosts = computed(() => {
  if (sortType.value === 'likes') {
    return [...posts.value].sort((a, b) => b.like_count - a.like_count)
  } else {
    return [...posts.value].sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
  }
})

const paginatedPosts = computed(() => {
  const start = (currentPage.value - 1) * perPage
  const end = start + perPage
  return sortedPosts.value.slice(start, end)
})

const totalPages = computed(() => Math.ceil(sortedPosts.value.length / perPage))

const setPage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
  }
}

const goToDetail = (id) => {
  router.push({ name: 'CommunityDetailView', params: { postId: id } })
}

onMounted(fetchPosts)
</script>

<style scoped>
.community-wrapper {
  background-color: #121212;
  color: #f1f1f1;
  max-width: 800px;
  margin: 80px auto 0;
  padding: 2rem 1.5rem;
  border-radius: 12px;
  padding-bottom: 200px;
  min-height: calc(100vh - 200px);
}

.title {
  text-align: center;
  font-size: 2rem;
  margin-bottom: 2rem;
}

.select-wrapper {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1.2rem;
}

.select-wrapper select {
  background-color: #121212;
  color: #ff6b6b;
  border: 2px solid #ff6b6b;
  border-radius: 6px;
  padding: 0.4rem 0.8rem;
  font-weight: bold;
  outline: none;
  transition: all 0.25s ease;
}

.select-wrapper select:hover,
.select-wrapper select:focus {
  background-color: #ff6b6b;
  color: #121212;
  box-shadow: 0 0 8px rgba(255, 107, 107, 0.7);
}

.list-header,
.post-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #333;
}

.list-header {
  border-bottom: 2px solid #444;
  font-weight: bold;
  color: #bbbbbb;
}

.post-row {
  cursor: pointer;
  transition: background 0.2s;
}

.post-row:hover {
  background-color: #1f1f1f;
}

.title-col {
  flex: 2;
  text-align: left;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-col,
.date-col,
.like-col {
  flex: 1;
  text-align: center;
}

.like-col {
  color: white;
  font-weight: bold;
}

.empty-msg {
  text-align: center;
  padding: 2rem 1rem;
  font-style: italic;
  color: #888;
  font-size: 1.1rem;
}

.bottom-bar {
  position: fixed;
  bottom: 200px;
  max-width: 800px;
  left: 0;
  right: 0;
  margin: 0 auto;
  width: 100%;
  background-color: #121212;
  padding: 1rem 1.5rem;
  border-top: 1px solid #333;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.bottom-bar .pagination {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
}

.bottom-bar .pagination button {
  background-color: transparent;
  color: #ff6b6b;
  border: 2px solid #ff6b6b;
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.25s ease;
  box-shadow: 0 0 6px rgba(255, 107, 107, 0.5);
}

.bottom-bar .pagination button:hover {
  background-color: #ff6b6b;
  color: #121212;
  box-shadow: 0 0 10px rgba(255, 107, 107, 0.9), 0 0 16px rgba(255, 107, 107, 0.5);
}

.bottom-bar .pagination .active {
  background-color: #ff6b6b;
  color: white;
}

.bottom-bar .pagination button:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.bottom-bar .button-row {
  display: flex;
  justify-content: space-between;
}

.bottom-bar .write-btn,
.bottom-bar .back-btn {
  display: inline-block;
  background-color: transparent;
  color: #ff6b6b;
  border: 2px solid #ff6b6b;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.25s ease;
  box-shadow: 0 0 8px rgba(255, 107, 107, 0.6);
}

.bottom-bar .write-btn:hover,
.bottom-bar .back-btn:hover {
  background-color: #ff6b6b;
  color: #121212;
  box-shadow: 0 0 12px rgba(255, 107, 107, 0.9), 0 0 20px rgba(255, 107, 107, 0.6);
}

.bottom-spacer {
  height: 200px;
}

.title-area {
  text-align: center;
  margin-bottom: 2rem;
  background: linear-gradient(145deg, #1f1f1f, #181818);
  padding: 2rem 1rem;
  border-radius: 12px;
  box-shadow: 0 0 20px rgba(255, 107, 107, 0.1);
}

.title {
  font-family: 'DM Serif Display', serif;
  font-size: 2.6rem;
  color: #ff6b6b;
  margin: 0;
}

.subtitle {
  font-size: 1rem;
  color: #aaa;
  margin-top: 0.4rem;
}


</style>