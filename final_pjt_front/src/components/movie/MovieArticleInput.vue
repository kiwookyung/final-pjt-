<template>
  <div class="container mt-5">
    <div v-if="!userStore.isLogin" class="text-center">
      <p>게시글 작성을 위해선 로그인이 필요합니다.</p>
      <button class="btn btn-info mb-5" @click="redirectToLogin">로그인</button>
    </div>
    <div v-else>
      <div class="mb-3">
        <label for="rate" class="form-label">평점 </label>
        <select v-model="article.rate" class="form-select" style="width: auto">
          <option v-for="n in 10" :key="n" :value="n">{{ n }}</option>
        </select>
      </div>

      <div class="mb-3">
        <label for="title" class="form-label">제목</label>
        <input
          type="text"
          class="form-control"
          id="title"
          placeholder="게시판 제목"
          v-model="article.title"
          required
        />
      </div>
      <div class="mb-3">
        <label for="content" class="form-label">내용</label>
        <textarea
          class="form-control"
          v-model="article.content"
          placeholder="내용을 입력하세요"
          rows="5"
          required
        ></textarea>
      </div>
      <button @click="submitArticle" class="btn btn-info mb-5">제출</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'
import { useArticleStore } from '@/stores/articleStore'

const route = useRoute()
const router = useRouter()

const userStore = useUserStore()
const articleStore = useArticleStore()

const moviePk = route.params.moviePk

const article = ref({
  rate: 5,
  title: '',
  content: ''
})

const redirectToLogin = () => {
  router.push({ name: 'userLogin' })
}

const submitArticle = () => {
  articleStore
    .addArticle(moviePk, article.value)
    .then(() => {
      article.value = {
        rate: 5,
        title: '',
        content: ''
      }
    })
    .catch((error) => {
      console.error(error)
    })
}
</script>

<style scoped>
/* 입력 폼 컨테이너 꾸미기 */
.container {
  background-color: #121212; /* 진한 검은색 배경 */
  border-radius: 12px;
  padding: 2rem 2.5rem;
  box-shadow: 0 0 15px rgba(255, 255, 255, 0.1);
  color: #eee;
}

/* 폼 레이블 */
.form-label {
  color: #bbb;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

/* 입력, 셀렉트, 텍스트에어리어 */
.form-control,
.form-select {
  background-color: #222;
  border: 1px solid #444;
  color: #eee;
  border-radius: 8px;
  transition: border-color 0.3s ease;
}

.form-control:focus,
.form-select:focus,
textarea.form-control:focus {
  border-color: #08f;
  box-shadow: 0 0 6px #08f;
  outline: none;
}

/* 제출 버튼 */
.btn-info {
  background-color: #08f;
  border-color: #08f;
  color: #fff;
  font-weight: 600;
  padding: 0.5rem 1.5rem;
  border-radius: 10px;
  transition: background-color 0.3s ease;
  cursor: pointer;
  user-select: none;
}

.btn-info:hover {
  background-color: #005fcc;
  border-color: #005fcc;
  color: #fff;
}

</style>