<template>
  <div class="movie-article-card">
    <!-- 영화 리뷰 카드를 클릭하면 modal 활성화 -->
    <div :data-bs-toggle="!editMode ? 'modal' : null" :data-bs-target="'#modal' + article.id">
      <div class="review-display">
        <div class="article-info">
          <div class="article-title">
            <span v-if="!editMode">{{ article.title }}</span>
            <input v-if="editMode" v-model="editedArticleTitle" type="text" class="form-control" />
          </div>
          <div class="article-content">
            <span v-if="!editMode" v-html="formatContent(article.content)"></span>
            <textarea
              v-if="editMode"
              v-model="editedArticleContent"
              class="form-control"
            ></textarea>
          </div>
        </div>
        <div class="article-author">
          <img
            :src="article.user.profile_pic ? userProfilePic : AvatarSrc"
            class="profile-pic"
            alt="Profile Picture"
          />
          <span style="text-decoration: none !important">
            {{ username }}
          </span>
        </div>
      </div>
    </div>
    <!-- 활성화 되는 modal -->
    <MovieArticleCardModal :article="article" />
    <!-- 부가정보 -->
    <div class="review-sub-display">
      <div>
        <div class="article-rating">
          <span v-if="!editMode">평점: {{ article.rate }} / 10</span>
          <div v-if="editMode" class="d-flex align-items-center">
            <select v-model="editedArticleRate" class="form-select" style="width: auto">
              <option v-for="n in 10" :key="n" :value="n">{{ n }}</option>
            </select>
            <span style="font-weight: bold; font-size: 1rem; margin-left: 0.5rem"> / 10 </span>
          </div>
        </div>
        <div class="article-date">작성일: {{ formattedDate }}</div>
      </div>
      <div v-if="userStore.isLogin">
        <div v-if="isOwner" class="article-edit-delete-container">
          <button
            v-if="!editMode"
            @click="deleteArticle(article.movie?.pk ?? article.movie, article.id)"
            class="btn btn-danger"
          >
            삭제
          </button>
          <div class="edit-button-container">
            <button v-if="!editMode" @click="startEdit" class="btn btn-info text">
              수정
            </button>
            <button
              v-if="editMode"
              @click="updateArticle(article.movie, article.id)"
              class="btn btn-info update-button"
            >
              저장
            </button>
            <button v-if="editMode" @click="cancelEdit" class="btn btn-outline-info text-secondary">
              취소
            </button>
          </div>
        </div>
        <div
          v-if="!isOwner"
          class="like-button-container"
          @click="likeArticle(article.movie, article.id)"
        >
          <i
            :class="isLiked ? 'bi bi-chat-square-heart-fill' : 'bi bi-chat-square-heart'"
            style="font-size: 24px"
          ></i>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import AvatarSrc from '@/assets/avatar.png'
import { useUserStore } from '@/stores/userStore'
import { useArticleStore } from '@/stores/articleStore'
import { likeArticleApi } from '@/apis/movieApi'
import MovieArticleCardModal from '@/components/movie/MovieArticleCardModal.vue'

const props = defineProps(['article', 'profile_pic'])

const userStore = useUserStore()
const articleStore = useArticleStore()

const isOwner = computed(() => props.article.user.pk === userStore.userData.pk)
const username = computed(() => props.article.user.username.split('@')[0])
const userProfilePic = computed(() => `http://localhost:8000${props.article.user.profile_pic}`)

// edit mode
const editMode = ref(false)
const editedArticleTitle = ref(props.article.title)
const editedArticleContent = ref(props.article.content)
const editedArticleRate = ref(props.article.rate)

const startEdit = () => {
  editMode.value = true
  editedArticleTitle.value = props.article.title
  editedArticleContent.value = props.article.content
}

const cancelEdit = () => {
  editMode.value = false
  editedArticleContent.value = ''
}

const deleteArticle = (moviePk, articlePk) => {
  articleStore
    .deleteArticle(moviePk, articlePk)
    .then(() => {
      articleStore.initializeArticles(moviePk)
      alert('성공적으로 글이 삭제됐습니다!')
    })
    .catch((error) => {
      console.error(error)
    })
}

const updateArticle = (moviePk, articlePk) => {
  articleStore
    .updateArticle(moviePk, articlePk, {
      rate: editedArticleRate.value,
      title: editedArticleTitle.value,
      content: editedArticleContent.value
    })
    .then(() => {
      articleStore.initializeArticles(moviePk)
      alert('성공적으로 글이 수정됐습니다!')
      cancelEdit()
    })
    .catch((error) => {
      console.error(error)
    })
}

// 게시글 좋아요
const isLiked = ref(
  Array.isArray(props.article.like_users)
    ? props.article.like_users.some((user) => user.pk === userStore.userData.pk)
    : false
)

const likeArticle = (moviePk, articlePk) => {
  likeArticleApi(moviePk, articlePk)
    .then((response) => {
      if (response.status === 200) {
        isLiked.value = !isLiked.value
        if (isLiked.value) {
          props.article.like_user_count += 1
        } else {
          props.article.like_user_count -= 1
        }
      } else {
        alert('서버 오류')
      }
    })
    .catch((error) => {
      console.error(error)
    })
}

// 각종 format
const formatContent = (content) => {
  const cont = content.length > 300 ? content.slice(0, 300) + '...' : content
  return cont.replace(/\n/g, '<br />')
}

const formattedDate = computed(() => {
  let date = new Date(props.article.created_at)
  let year = date.getFullYear()
  let month = ('0' + (date.getMonth() + 1)).slice(-2)
  let day = ('0' + date.getDate()).slice(-2)
  let hours = ('0' + date.getHours()).slice(-2)
  let minutes = ('0' + date.getMinutes()).slice(-2)
  return `${year}-${month}-${day} ${hours}:${minutes}`
})
</script>

<style scoped>
.review-sub-display {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-content: center;
  align-items: flex-end;
  padding: 1rem;
  color: #000;
}
.movie-article-card {
  border: 1px solid #444;           /* 진한 회색 테두리 */
  margin-top: 15px;
  padding: 20px;
  border-radius: 12px;
  background-color: #222;           /* 진한 검정 배경 */
  box-shadow: 0 1px 8px rgba(0, 0, 0, 0.7); /* 좀 더 어두운 그림자 */
  color: #eee;                     /* 밝은 글자색 */
}

.article-edit-delete-container {
  display: flex;
  flex-direction: row;
  gap: 1rem;
  margin-top: 1rem;
}
.like-button-container {
  display: flex;
  flex-direction: row;
  gap: 1rem;
  margin: 1rem;
}
.update-button {
  margin-right: 1rem;
}

.review-display {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: start;
}
.article-title {
  font-weight: bold;
  font-size: 20px;
  margin-bottom: 8px;
  color: white;
  padding: 1rem;
}
.article-info {
  width: 100%;
}
.article-title input {
  width: 100%;
  padding: 0.5rem;
}
.article-content textarea {
  width: 100%;
  height: 150px;
  padding: 0.5rem;
}

.article-content {
  font-size: 16px;
  margin-bottom: 8px;
  color: white;
  line-height: 1.5;
  padding: 1rem;
}

.article-date {
  margin-top: 0.3rem;
}

.article-author,
.article-rating,
.article-date {
  font-size: 12px;
  color: white;
}

.article-author {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin-bottom: 10px;
  padding: 1rem;
}

.article-author a {
  color: white;
  text-decoration: none;
  font-weight: 500;
  margin-right: 1rem;
}

.article-author a:hover {
  text-decoration: none;
}

.profile-pic {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.article-rating {
  margin-right: 1.5rem;
}
</style>