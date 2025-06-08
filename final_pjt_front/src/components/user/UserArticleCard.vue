<template>
  <div class="article-card">
    <RouterLink
      :to="{ name: 'MovieDetailView', params: { moviePk: article.movie.id || article.movie.pk } }"
    >
      <div class="image-container">
        <img :src="getImageUrl(article.movie.poster_path)" :alt="article.movie.title || article.movie.name" />
        <div class="overlay">
          <h5 class="title">{{ getFormattedTitle }}</h5>
        </div>
      </div>
      <div class="card-body">
        <div class="review-title">{{ formatContent(article.title) }}</div>
        <div class="rating">⭐ {{ article.rate }} / 10</div>
      </div>
    </RouterLink>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import DefaultImage from '@/assets/default-movie.png' // 기본 이미지 추가!

const props = defineProps({
  article: Object
})

const getImageUrl = (path) => {
  return path ? `https://image.tmdb.org/t/p/w500${path}` : DefaultImage
}

const getFormattedTitle = computed(() => {
  const title = props.article.movie.title || props.article.movie.name
  return title.length > 20 ? title.slice(0, 20) + '...' : title
})

const formatContent = (content) => {
  return content.length > 20 ? content.slice(0, 20) + '...' : content
}
</script>

<style scoped>
.article-card {
  width: 100%; /* 여기도 col 너비에 딱 맞춤 */
  border-radius: 12px;
  overflow: hidden;
  transition: transform 0.3s ease;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.article-card:hover {
  transform: scale(1.05);
}

.image-container {
  position: relative;
  width: 100%;
  height: 270px;
  overflow: hidden;
  border-radius: 12px 12px 0 0;
}

.image-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  border-radius: 12px 12px 0 0;
}

.overlay {
  position: absolute;
  bottom: 0;
  width: 100%;
  padding: 8px;
  background: rgba(0, 0, 0, 0.6);
  text-align: center;
}

.title {
  color: white;
  font-size: 1rem;
  font-weight: bold;
  margin: 0;
}

.card-body {
  padding: 12px;
  background: transparent;
}

.review-title {
  font-size: 1rem;
  font-weight: bold;
  margin-bottom: 6px;
  color: white;
}

.rating {
  font-size: 0.9rem;
  color: #e50914;
  font-weight: bold;
}


</style>