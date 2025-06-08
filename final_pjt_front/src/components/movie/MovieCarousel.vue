<template>
  <section class="carousel-wrapper">
    <div class="carousel-header">
      <h2 v-if="title" class="section-heading">{{ title }}</h2>
    </div>

    <div class="carousel-inner">
      <Splide :options="splideOptions" class="movie-carousel">
        <SplideSlide v-for="movie in movies" :key="movie.id">
          <MovieCard :movie="movie" />
        </SplideSlide>
      </Splide>
    </div>
  </section>

</template>

<script setup>
import MovieCard from './MovieCard.vue'
import { Splide, SplideSlide } from '@splidejs/vue-splide'

const props = defineProps({
  movies: Array,
  title: String,
})

const splideOptions = {
  type: 'slide',
  gap: '20px',
  pagination: false,
  arrows: true,
  drag: true,
  perPage: 5,
  autoWidth: true, // allow dynamic sizing
  breakpoints: {
    1400: { perPage: 4 },
    1200: { perPage: 3 },
    992: { perPage: 2 },
    576: { perPage: 1 },
  },
}
</script>

<style scoped>
.movie-carousel {
  margin-bottom: 5rem;
  padding: 0 1rem;
}

@media (max-width: 768px) {
  .movie-carousel {
    padding: 0 0.5rem;
  }
}

.carousel-wrapper {
  width: 100%;
  padding-inline: 2.5rem; /* ← 양옆 여백 살짝 확보 */
  margin-bottom: 3rem;
}

.carousel-inner {
  max-width: 1400px;  /* 이전보다 살짝 넓게 */
  margin: 0 auto;
}

.carousel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1400px;
  margin: 0 auto 1rem;
  padding-inline: 0.25rem;
}

.section-heading {
  font-size: 28px;
  font-weight: 700;
  color: white;
}

</style>
