<template>
  <div class="comments">
    <div v-for="comment in comments" :key="comment.id" class="comment">
      <div class="left">
        <strong>{{ comment.user }} :</strong>
        <span class="text">{{ comment.content }}</span>
      </div>
      <button 
        v-if="comment.user === userStore.userData.username" 
        @click="deleteComment(comment.id)"
        class="delete-btn"
      >
        삭제
      </button>
    </div>

    <div class="comment-input">
      <input v-model="newComment" placeholder="댓글을 입력하세요" />
      <button @click="submitComment" class="submit-btn">등록</button>
    </div>
    <RouterLink to="/community" class="back-btn">뒤로가기</RouterLink>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'
import { useUserStore } from '@/stores/userStore'

const props = defineProps({ postId: Number })
const comments = ref([])
const newComment = ref('')
const userStore = useUserStore()
const emit = defineEmits(['update-count'])


const fetchComments = async () => {
  try {
    const res = await axios.get(`http://localhost:8000/movies/community/${props.postId}/comments/`, {
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`,
      }
    })
    comments.value = res.data
    emit('update-count', comments.value.length)  // ✅ 댓글 수 전달
  } catch (err) {
    console.error('❌ 댓글 불러오기 실패:', err)
  }
}

watch(comments, () => {
  emit('update-count', comments.value.length)
})

const submitComment = async () => {
  if (!newComment.value.trim()) return
  try {
    await axios.post(
      `http://localhost:8000/movies/community/${props.postId}/comments/`,
      { content: newComment.value },
      {
        headers: {
          Authorization: `Token ${localStorage.getItem('token')}`,
        }
      }
    )
    newComment.value = ''
    fetchComments()
  } catch (err) {
    console.error('❌ 댓글 등록 실패:', err)
  }
}

const deleteComment = async (commentId) => {
  if (!confirm('정말 댓글을 삭제하시겠습니까?')) return
  try {
    await axios.delete(`http://localhost:8000/movies/community/${props.postId}/comments/${commentId}/`, {
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`,
      }
    })
    fetchComments()
  } catch (err) {
    console.error('❌ 댓글 삭제 실패:', err)
  }
}

onMounted(fetchComments)
</script>

<style scoped>
.comments {
  margin-top: 1rem;
}

.comment {
  padding: 0.7rem 0;
  border-bottom: 1px solid #333;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.left {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  flex: 1;
  overflow: hidden;
}

.text {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
}

.comment-input {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.comment-input input {
  flex: 1;
  padding: 0.5rem;
  background-color: #2c2c2c;
  border: none;
  color: #f1f1f1;
  border-radius: 6px;
}
.submit-btn {
  background-color: transparent;
  color: #3a82f6;
  border: 2px solid #3a82f6;
  padding: 0.5rem 0.9rem;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s ease;
  box-shadow: 0 0 8px rgba(58, 130, 246, 0.5);
}
.submit-btn:hover {
  background-color: #3a82f6;
  color: #121212;
  box-shadow: 0 0 12px rgba(58, 130, 246, 0.9), 0 0 18px rgba(58, 130, 246, 0.6);
}

.delete-btn {
  background-color: transparent;
  color: #ff6b6b;
  border: 2px solid #ff6b6b;
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s ease;
  box-shadow: 0 0 8px rgba(255, 107, 107, 0.5);
}
.delete-btn:hover {
  background-color: #ff6b6b;
  color: #121212;
  box-shadow: 0 0 12px rgba(255, 107, 107, 0.9), 0 0 18px rgba(255, 107, 107, 0.6);
}


.back-btn {
  display: inline-block;
  margin-top: 1.5rem;
  background-color: transparent;
  color: #bbbbbb;
  border: 2px solid #bbbbbb;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-weight: bold;
  text-decoration: none;
  transition: all 0.25s ease;
  box-shadow: 0 0 6px rgba(187, 187, 187, 0.4);
}
.back-btn:hover {
  background-color: #bbbbbb;
  color: #121212;
  box-shadow: 0 0 12px rgba(187, 187, 187, 0.9), 0 0 18px rgba(187, 187, 187, 0.6);
}

</style>
