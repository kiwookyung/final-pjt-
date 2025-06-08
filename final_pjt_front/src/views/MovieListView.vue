<template>
  <div class="container mt-4">
    <div class="row row-cols-1 row-cols-sm-1 row-cols-md-2 row-cols-lg-3 row-cols-xl-4 g-4">
      <div class="col" v-for="movie in movies" :key="movie.id">
        <MovieCard :movie="movie" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import MovieCard from '@/components/movie/MovieCard.vue'
import { getMoviesList } from '@/apis/movieApi'

const movies = ref([])

// infinity scroll Logic
const currentPage = ref(1)
const fetchMovies = (page) => {
  getMoviesList(page)
    .then((response) => {
      movies.value = [...movies.value, ...response.data]
    })
    .catch((err) => {
      alert(err)
    })
}
const fetchMoreMovies = () => {
  currentPage.value += 1
  fetchMovies(currentPage.value)
}

const handleScroll = () => {
  const nearBottom = window.innerHeight + window.scrollY >= document.body.offsetHeight - 500
  if (nearBottom) {
    fetchMoreMovies()
  }
}

onMounted(() => {
  fetchMovies(currentPage.value)
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>
