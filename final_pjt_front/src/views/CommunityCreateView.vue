<template>
  <div class="create-page">
    <div class="top-bar">
      <h2>게시글 작성</h2>
    </div>
    <CommunityPostForm @submit="createPost" />
  </div>
</template>

<script setup>
import axios from 'axios'
import { useRouter } from 'vue-router'
import CommunityPostForm from '@/components/community/CommunityPostForm.vue'

const router = useRouter()

const createPost = async (formData) => {
  try {
    const res = await axios.post('http://localhost:8000/movies/community/', formData, {
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`,
        'Content-Type': 'multipart/form-data',
      }
    })
    const newPostId = res.data.id
    alert('글이 작성되었습니다!')
    router.push(`/community/${newPostId}`)
  } catch (err) {
    console.error('작성 실패:', err)
    alert('작성에 실패했습니다.')
  }
}
</script>

<style scoped>
.create-page {
  max-width: 700px;
  margin: 90px auto 0;
  padding: 2rem;
  background-color: #1e1e1e;
  color: #f1f1f1;
  border-radius: 12px;
}

.top-bar {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.back-btn {
  background-color: #444;
  color: white;
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  text-decoration: none;
  font-weight: bold;
}

.back-btn:hover {
  background-color: #666;
}
</style>
