<template>
  <div class="card" @click="goToDetail">
    <div v-if="post.image">
      <img :src="`http://localhost:8000${post.image}`" class="post-image" />
    </div>
    <div class="post-info">
      <div class="top-row">
        <h3 class="post-title">{{ post.title }}</h3>
        <p class="likes">{{ post.like_count }} Likes</p>
      </div>
      <div class="bottom-row">
        <p class="meta">{{ post.user }}</p>
        <p class="meta">{{ post.created_at.slice(0, 10) }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const props = defineProps({ post: Object })
const router = useRouter()

const goToDetail = () => {
  router.push({ name: 'CommunityDetailView', params: { postId: props.post.id } })
}
</script>

<style scoped>
.card {
  background-color: #1e1e1e;
  color: #f0f0f0;
  padding: 1.2rem;
  border-radius: 12px;
  margin-bottom: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.6);
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.8);
}

.post-image {
  width: 100%;
  max-height: 240px;
  object-fit: cover;
  border-radius: 10px;
  margin-bottom: 1rem;
}

.post-info {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.top-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.bottom-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.85rem;
  color: #aaa;
}

.post-title {
  font-size: 1.2rem;
  font-weight: bold;
  color: #ffffff;
  margin: 0;
}

.likes {
  font-size: 0.9rem;
  color: #ff4d6d;
  font-weight: 500;
}
</style>
