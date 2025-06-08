<template>
  <div class="movie-card">
    <RouterLink :to="{ name: 'MovieDetailView', params: { moviePk: movie.id || movie.pk } }">
      <div class="image-container">
        <img :src="getImageUrl(movie.poster_path)" :alt="movie.title || movie.name" />
        <div class="overlay">
          <h5 class="title">{{ getFormattedTitle }}</h5>
        </div>
      </div>
    </RouterLink>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import DefaultImage from '@/assets/default-movie.png' // 기본 이미지 준비해둬!

const props = defineProps({
  movie: Object
})

const getImageUrl = (path) => {
  return path ? `https://image.tmdb.org/t/p/w500${path}` : DefaultImage
}

const getFormattedTitle = computed(() => {
  const title = props.movie.title || props.movie.name
  return title.length > 20 ? title.slice(0, 20) + '...' : title
})
</script>

<style scoped>
.movie-card {
  width: 100%; /* col 너비에 맞춰 꽉 차게 */
  border-radius: 12px;
  overflow: hidden;
  transition: transform 0.3s ease;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.movie-card:hover {
  transform: scale(1.05);
}

.image-container {
  position: relative;
  width: 100%;
  height: 270px; /* 너가 원하는 이미지 높이 유지 */
  overflow: hidden;
  border-radius: 12px;
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
  padding: 10px;
  background: rgba(0, 0, 0, 0.6);
  text-align: center;
}

.title {
  color: white;
  font-size: 1rem;
  font-weight: bold;
  margin: 0;
}

</style>