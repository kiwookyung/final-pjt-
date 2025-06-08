<template>
  <div>
    <div
      v-for="comment in commentStore.getCommentsByArticle(props.article.id)"
      :key="comment.pk"
      class="comment p-3 rounded-3 mb-2"
      style="background-color: #222; color: white;"
    >
      <span class="comment-content" data-bs-dismiss="modal">
        <RouterLink :to="`/user/profile/${comment.user.pk}/pick`">
          <img
            :src="comment.user.profile_pic ? userProfilePic(comment.user.profile_pic) : AvatarSrc"
            class="profile-pic"
            alt="Profile Picture"
          />
          <span class="me-2">{{ comment.user.username.split('@')[0] }}</span>
        </RouterLink>
        {{ comment.content }}
      </span>

      <button
        v-if="comment.user && userStore.userData.pk === comment.user.pk"
        @click="deleteComment(comment)"
        class="delete-button btn btn-sm btn-outline-secondary"
      >
        <i class="bi bi-trash text-secondary"></i>
      </button>
    </div>

    <div class="comment-input-section d-flex">
      <input
        v-model="newCommentContent"
        placeholder="댓글을 입력하세요..."
        class="comment-input form-control me-2"
      />
      <button @click="createComment" class="comment-submit-button btn btn-info">
        <i class="bi bi-send"></i>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watchEffect } from 'vue'
import { useUserStore } from '@/stores/userStore'
import { useCommentStore } from '@/stores/commentStore'
import AvatarSrc from '@/assets/avatar.png'

const props = defineProps(['article'])

const userStore = useUserStore()
const commentStore = useCommentStore()
const newCommentContent = ref('')

const userProfilePic = (path) => `http://localhost:8000${path}`

const createComment = () => {
  commentStore
    .createNewComment(props.article.movie, props.article.id, {
      content: newCommentContent.value,
    })
    .then(() => {
      newCommentContent.value = ''
    })
}

const deleteComment = (comment) => {
  console.log('[🗑️] Delete comment clicked. Full comment object:', comment)

  const commentPk = comment.pk
  if (!commentPk) {
    console.error('❌ commentPk가 undefined입니다. 댓글 구조 확인 필요:', comment)
    return
  }

  commentStore
    .deleteOldComment(props.article.movie, props.article.id, commentPk)
    .then(() => {
      console.log('[✅] Comment deleted')
    })
    .catch((err) => {
      console.error('[❌] Delete failed:', err)
    })
}

watchEffect(() => {
  const comments = commentStore.getCommentsByArticle(props.article.id)
  console.log('[🐞] Comments for article:', comments)
})

onMounted(() => {
  const movieId = props.article.movie?.pk ?? props.article.movie
  commentStore.initializeComments(movieId, props.article.id)
})
</script>

<style scoped>
.comment {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #222;
  padding: 12px 16px;
  border-radius: 12px;
  margin-bottom: 12px;
  color: #eee;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.6);
  transition: background-color 0.3s ease;
}

.comment:hover {
  background-color: #2c2c2c;
}

.comment-content {
  flex: 1;
  color: #ddd;
}

.comment-content a {
  text-decoration: none;
  color: #7db9ff;
  font-weight: 600;
}

.comment-content a:hover {
  text-decoration: underline;
  color: #a0c4ff;
}

.delete-button {
  margin-left: 1rem;
  background: transparent;
  border: none;
  color: #ff6b6b;
  cursor: pointer;
  transition: color 0.2s ease;
}

.delete-button:hover {
  color: #ff3b3b;
}

.comment-input-section {
  display: flex;
  margin-top: 1.5rem;
  gap: 8px;
}

.comment-input {
  flex: 1;
  padding: 10px 12px;
  border-radius: 12px;
  border: none;
  background-color: #2c2c2c;
  color: #eee;
  font-size: 1rem;
  outline: none;
  transition: background-color 0.3s ease;
}

.comment-input::placeholder {
  color: #999;
}

.comment-input:focus {
  background-color: #3a3a3a;
}

.comment-submit-button {
  background-color: #3a82f6;
  border: none;
  border-radius: 12px;
  color: white;
  padding: 0 16px;
  font-size: 1.2rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.comment-submit-button:hover {
  background-color: #2565d8;
}

.profile-pic {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
  object-fit: cover;
  border: 2px solid #3a82f6;
}
</style>