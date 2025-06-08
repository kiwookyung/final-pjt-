<template>
  <div v-if="movie">
    <MovieDetailInfo :movie="movie" />
    <ChatBot/>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import MovieDetailInfo from '@/components/movie/MovieDetailInfo.vue'
import { getMovieDetail } from '@/apis/movieApi'
import ChatBot from '@/components/movie/MovieChatBot.vue'

const movie = ref(null)
const route = useRoute()

// 영화 상세정보 요청
const fetchMovieDetail = () => {
  getMovieDetail(route.params.moviePk)
    .then((response) => {
      movie.value = response.data
    })
    .catch((err) => {
      alert(err)
    })
}

onMounted(() => {
  fetchMovieDetail()
})
</script>

<style></style>
