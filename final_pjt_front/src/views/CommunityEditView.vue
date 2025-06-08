<template>
  <div class="edit-page" v-if="post" style="margin-top: 90px;">
    <h2>게시글 수정</h2>
    <CommunityPostForm :initial-data="post" @submit="updatePost" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import CommunityPostForm from '@/components/community/CommunityPostForm.vue'

const route = useRoute()
const router = useRouter()
const postId = route.params.postId  // ← 요기 수정!!

const post = ref(null)

onMounted(async () => {
  console.log('📦 수정할 postId:', postId)
  try {
    const res = await axios.get(`http://localhost:8000/movies/community/${postId}/`, {
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`
      }
    })
    post.value = res.data
  } catch (err) {
    console.error('❌ 게시글 로딩 실패:', err)
  }
})

const updatePost = async (formData) => {
  try {
    await axios.put(`http://localhost:8000/movies/community/${postId}/`, formData, {
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`,
        'Content-Type': 'multipart/form-data',
      }
    })
    alert('수정되었습니다.')
    router.push({ name: 'CommunityDetailView', params: { postId } })
  } catch (err) {
    console.error('❌ 수정 실패:', err)
  }
}
</script>


<style scoped>
.edit-page {
  max-width: 700px;
  margin: 0 auto;
  padding: 2rem;
}
</style>
