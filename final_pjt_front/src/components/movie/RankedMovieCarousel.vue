<template>
  <section class="ranked-section">
    <h2 class="top-heading">🏆 TOP 추천 영화</h2>
    <Splide :options="{
      perPage: 5,
      gap: '1rem',
      type: 'loop',
      pagination: false,
      arrows: true,
      drag: true,
      autoplay: true,
      interval: 6000,
      speed: 1200,
      breakpoints: {
        1200: { perPage: 4 },
        992: { perPage: 3 },
        768: { perPage: 2 },
        480: { perPage: 1 }
      },
      extensions: { AutoScroll }
    }" class="ranked-carousel">
      <SplideSlide v-for="(movie, index) in movies" :key="movie.id">
        <RankedMovieCard :movie="movie" :rank="index + 1" />
      </SplideSlide>
    </Splide>
  </section>
</template>

<script setup>
import { Splide, SplideSlide } from '@splidejs/vue-splide'
import { RouterLink } from 'vue-router'
import { AutoScroll } from '@splidejs/splide-extension-auto-scroll'
import RankedMovieCard from '@/components/movie/RankedMovieCard.vue'
defineProps({
  movies: Array,
})

const getImageUrl = (path) => {
  return path ? `https://image.tmdb.org/t/p/w500${path}` : ''
}
</script>

<style scoped>
.ranked-section {
  margin-bottom: 2rem;
}

.ranked-card {
  position: relative;
  width: 100%;
  aspect-ratio: 2/3;
  /* 2:3 비율 (예: 300x450)로 고정 */
  overflow: hidden;
  border-radius: 10px;
  background-color: #111;
  /* 비어있을 때 대비 */
}

.poster-img {
  width: 100%;
  height: 90%;
  object-fit: cover;
  border-radius: 10px;
}


</style>
