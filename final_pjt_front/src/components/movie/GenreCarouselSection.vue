<!-- src/components/movie/GenreCarouselSection.vue -->
<template>
  <section class="genre-section">
    <div class="genre-header">
      <h2 class="section-heading">{{ genre.name }}</h2>
      <RouterLink :to="`/genre/${genre.id}`" class="more-link">더보기 ></RouterLink>
    </div>

    <div class="carousel-inner">
      <MovieCarousel :movies="movies" :title="null" />
    </div>
  </section>
</template>


<script setup>
import { onMounted, ref } from 'vue'
import { getMoviesByGenre } from '@/apis/movieApi'
import MovieCarousel from './MovieCarousel.vue'

const props = defineProps({
  genre: Object,
})

const movies = ref([])

onMounted(() => {
  getMoviesByGenre(props.genre.id, 20)
    .then((res) => {
      movies.value = res.data
    })
    .catch((err) => console.error(err))
})
</script>

<style scoped>
.more-link {
  color: #aaa;
  font-size: 0.95rem;
  transition: color 0.2s ease;
}
.more-link:hover {
  color: #fff;
}

.genre-section {
  width: 100%;
  padding-inline: 2rem;
  margin-bottom: 3rem;
}

.genre-header {
  max-width: 1400px;
  margin: 0 auto 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-inline: 0.25rem;
}

.section-heading {
  font-size: 26px;
  font-weight: bold;
  color: white;
  margin: 0;
}

.carousel-inner {
  max-width: 1400px;
  margin: 0 auto;
}

</style>
