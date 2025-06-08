<template>
  <div class="container py-4">
    <h2 class="mb-4">"{{ query }}" 검색 결과</h2>

    <div v-if="movies.length">
      <div class="row row-cols-1 row-cols-md-4 g-4">
        <div class="col" v-for="movie in movies" :key="movie.id">
          <MovieCard :movie="movie" />
        </div>
      </div>
    </div>
    <p v-else>검색 결과가 없습니다.</p>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { getMoviesList, getAllMovies } from '@/apis/movieApi'
import MovieCard from '@/components/movie/MovieCard.vue'

const route = useRoute()
const query = ref(route.query.query || '')
const movies = ref([])

const fetchSearchResults = async () => {
  try {
    const res = await getAllMovies()
    // 검색어가 제목에 포함되는 영화만 필터링
    movies.value = res.data.filter(movie =>
      movie.title.toLowerCase().includes(query.value.toLowerCase())
    )
  } catch (error) {
    console.error('검색 오류:', error)
  }
}

watch(() => route.query.query, (newVal) => {
  query.value = newVal
  fetchSearchResults()
})

onMounted(fetchSearchResults)
</script>
