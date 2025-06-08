<template>
  <div class="container py-4" style="margin-top: 70px;">
    <h2 class="section-heading genre-title">{{ genreName }} 장르의 영화</h2>
    <div class="row row-cols-1 row-cols-md-4 g-4">
      <div class="col" v-for="movie in movies" :key="movie.id">
        <MovieCard :movie="movie" />
      </div>
    </div>
    <ScrollToTop />
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import MovieCard from '@/components/movie/MovieCard.vue'
import { getMoviesByGenre, getGenres } from '@/apis/movieApi'
import ScrollToTop from '@/components/common/ScrollToTop.vue'

const route = useRoute()

const genreId = ref(route.params.genreId)  // ref로 바꾸기
const movies = ref([])
const genreName = ref('')

const fetchData = async (id) => {
  try {
    const movieRes = await getMoviesByGenre(id, 100)
    movies.value = movieRes.data

    const genreRes = await getGenres()
    genreName.value = genreRes.data.find(g => g.id == id)?.name || ''
  } catch (error) {
    console.error(error)
  }
}

onMounted(() => {
  fetchData(genreId.value)
})

// route.params.genreId가 바뀔 때마다 fetchData 호출해서 다시 데이터 로드
watch(() => route.params.genreId, (newId) => {
  genreId.value = newId
  fetchData(newId)
})
</script>
