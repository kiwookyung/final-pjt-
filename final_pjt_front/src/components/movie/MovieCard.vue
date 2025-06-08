<template>
  <div class="movie-card">
    <RouterLink :to="{ name: 'MovieDetailView', params: { moviePk: movie.id || movie.pk } }" class="card-link">
      <img :src="getImageUrl(movie.poster_path)" alt="poster" class="poster-img" />
      <div class="info-overlay">
        <p class="title">{{ movie.title }}</p>
        <p class="rating">⭐ {{ movie.vote_average?.toFixed(1) ?? 'N/A' }}</p>
      </div>
    </RouterLink>
  </div>
</template>


<script setup>
const props = defineProps({
  movie: Object
})

const getImageUrl = (path) => {
  return path ? `https://image.tmdb.org/t/p/w500${path}` : ''
}
</script>

<style scoped>
.movie-card {
  max-width: 250px;
  aspect-ratio: 2 / 3;
  overflow: hidden;
  border-radius: 12px;
  position: relative;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  background-color: #1a1a1a;
  margin: 0 auto;
}

.movie-card:hover {
  transform: scale(1.04);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.6);
}

.card-link {
  display: block;
  position: relative;
  width: 100%;
  height: 100%;
}

.poster-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 12px;
  display: block;
}

.info-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 0.5rem;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.8), transparent);
  color: #fff;
  font-size: 0.9rem;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.movie-card:hover .info-overlay {
  opacity: 1;
}

.title {
  font-weight: bold;
  font-size: 1rem;
  margin-bottom: 0.2rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.rating {
  font-size: 0.85rem;
  color: #feca57;
}

</style>