<template>
  <div class="ranked-card">
    <div class="rank-label">{{ rank }}</div>
    <RouterLink :to="{ name: 'MovieDetailView', params: { moviePk: movie.id } }" class="card-link">
      <img v-if="props.movie && props.movie.poster_path" :src="getImageUrl(props.movie.poster_path)" class="poster"
        alt="Poster" />

      <div class="info-overlay">
        <p class="title">{{ props.movie.title }}</p>
        <p class="rating">⭐ {{ props.movie.vote_average?.toFixed(1) ?? '평점 없음' }}</p>
      </div>
    </RouterLink>
  </div>
</template>

<script setup>
const props = defineProps({
  movie: Object,
  rank: Number
})

const getImageUrl = (path) => {
  return path ? `https://image.tmdb.org/t/p/w500${path}` : ''
}
</script>


<style scoped>
.ranked-card {
  position: relative;
  border-radius: 10px;
  overflow: hidden;
  background-color: #111;
  aspect-ratio: 2 / 3;
}

.rank-label {
  position: absolute;
  bottom: -10px;
  right: 15px;
  font-size: 7rem;
  font-weight: 700;
  font-style: italic;
  color: white;
  text-shadow: 2px 2px 4px black;
  z-index: 2;
}

.card-link {
  display: block;
  position: relative;
  width: 100%;
  height: 100%;
}

.poster {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 10px;
}

.info-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 0.5rem;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.85), transparent);
  color: white;
  font-size: 0.9rem;
  opacity: 0;
  transition: opacity 0.3s ease;
  text-align: left;
}

.card-link:hover .info-overlay {
  opacity: 1;
}

.title {
  font-weight: bold;
  font-size: 1rem;
  margin-bottom: 0.2rem;
}

.rating {
  font-size: 0.9rem;
  color: var(--accent-yellow);
}
</style>
