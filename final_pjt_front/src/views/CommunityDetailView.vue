<template>
  <div class="detail-page" v-if="post">
    <h2 class="post-title">{{ post.title }}</h2>
    <p class="meta">{{ post.user }} | {{ post.created_at.slice(0, 10) }}</p>

    <img v-if="post.image" :src="`http://localhost:8000${post.image}`" class="detail-image" />
    <p class="content">{{ post.content }}</p>

    <!-- 좋아요 / 수정삭제 버튼 양쪽 배치 -->
    <div class="button-row-split">
      <!-- 왼쪽: 좋아요 -->
      <button @click="toggleLike" class="like-btn">
        {{ post.is_liked ? '❤️' : '🤍' }} {{ post.like_count }}
      </button>

      <!-- 오른쪽: 수정 / 삭제 (작성자만 표시) -->
      <div v-if="isOwner" class="edit-delete-group">
        <RouterLink :to="`/community/edit/${post.id}`" class="edit-btn">수정</RouterLink>
        <button @click="deletePost" class="delete-btn">삭제</button>
      </div>
    </div>


    <hr class="divider" />

    <h4 class="comment-title">댓글 ({{ commentCount }})</h4>
    <CommunityComment v-if="post" :post-id="post.id" @update-count="updateCommentCount" />
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import axios from 'axios'
import CommunityComment from '@/components/community/CommunityComment.vue'
import { useUserStore } from '@/stores/userStore'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const post = ref(null)

const commentCount = ref(0)
const updateCommentCount = (count) => {
  commentCount.value = count
}

const toggleLike = async () => {
  try {
    await axios.post(`http://localhost:8000/movies/community/${post.value.id}/like/`, null, {
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`,
      }
    })
    fetchPost() // 좋아요 상태 다시 받아오기
  } catch (err) {
    console.error('❌ 좋아요 토글 실패:', err)
  }
}


const fetchPost = async () => {
  try {
    const res = await axios.get(`http://localhost:8000/movies/community/${route.params.postId}/`, {
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`,
      }
    })
    post.value = res.data
  } catch (err) {
    console.error('❌ fetchPost 에러:', err)
  }
}

onMounted(fetchPost)

const isOwner = computed(() => {
  return post.value?.user === userStore.userData.username
})

const deletePost = async () => {
  if (!confirm('정말 삭제하시겠습니까?')) return

  try {
    await axios.delete(`http://localhost:8000/movies/community/${post.value.id}/`, {
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`,
      }
    })
    alert('삭제되었습니다.')
    router.push('/community')
  } catch (err) {
    console.error('❌ 삭제 실패:', err)
  }
}
</script>

<style scoped>
.detail-page {
  max-width: 700px;
  margin: 90px auto 0;
  padding: 2rem;
  background-color: #1e1e1e;
  color: #f1f1f1;
  border-radius: 12px;
}

/* 제목 / 날짜 */
.post-title {
  font-size: 1.8rem;
  margin-bottom: 0.5rem;
}

.meta {
  font-size: 0.9rem;
  color: #aaa;
}

/* 이미지 */
.detail-image {
  width: 100%;
  margin: 1rem 0;
  border-radius: 12px;
}

/* 본문 내용 */
.content {
  font-size: 1.1rem;
  line-height: 1.7;
  margin-bottom: 1.5rem;
}

/* 버튼 영역: 좋아요 왼쪽, 수정/삭제 오른쪽 */
.button-row-split {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.edit-delete-group {
  display: flex;
  gap: 0.8rem;
}

/* 공통 버튼 */
.like-btn,
.edit-btn,
.delete-btn {
  padding: 0.5rem 1rem;
  border-radius: 6px;
  border: 2px solid;
  font-weight: bold;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.25s ease;
  background-color: transparent;
}

/* 좋아요 버튼 스타일 */
.like-btn {
  color: #ff6b6b;
  border-color: #ff6b6b;
  box-shadow: 0 0 8px rgba(255, 107, 107, 0.4);
}
.like-btn:hover {
  background-color: #ff6b6b;
  color: #121212;
  box-shadow: 0 0 12px rgba(255, 107, 107, 0.9), 0 0 20px rgba(255, 107, 107, 0.6);
}

/* 수정 버튼 스타일 */
.edit-btn {
  color: #3a82f6;
  border-color: #3a82f6;
  box-shadow: 0 0 8px rgba(58, 130, 246, 0.4);
}
.edit-btn:hover {
  background-color: #3a82f6;
  color: #121212;
  box-shadow: 0 0 12px rgba(58, 130, 246, 0.8), 0 0 20px rgba(58, 130, 246, 0.5);
}

/* 삭제 버튼 스타일 */
.delete-btn {
  color: #ff6b6b;
  border-color: #ff6b6b;
  box-shadow: 0 0 8px rgba(255, 107, 107, 0.4);
}
.delete-btn:hover {
  background-color: #ff6b6b;
  color: #121212;
  box-shadow: 0 0 12px rgba(255, 107, 107, 0.9), 0 0 20px rgba(255, 107, 107, 0.6);
}

/* 구분선 */
.divider {
  border: none;
  border-top: 1px solid #444;
  margin: 2rem 0 1rem;
}

/* 댓글 제목 */
.comment-title {
  font-size: 1.2rem;
  margin-bottom: 1rem;
}
</style>

