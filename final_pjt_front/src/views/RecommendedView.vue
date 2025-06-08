<template>
  <!-- 로딩 -->
  <div v-if="isLoading" class="d-flex justify-content-center align-items-center vh-100">
    <div class="spinner-border text-info" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
  <!-- 로딩이 끝나면 출력 -->
  <div
    v-else-if="recommendedMovie"
    class="container movie-container d-flex flex-column align-items-center justify-content-center mt-4"
  >
    <h5 class="weather-div">
      현재
      <span style="font-size: 2.5rem; margin: 1rem; font-weight: bold">{{ weatherStatus }}</span>
      기반 추천 영화
    </h5>
    <!-- Pick 버튼 -->
    <button
      :class="{
        'btn-info': !isPicked(recommendedMovie),
        'btn-outline-info': isPicked(recommendedMovie)
      }"
      class="btn mt-1 mb-2"
      style="width: 500px"
      @click="addToMyPickList"
    >
      {{ isPicked(recommendedMovie) ? 'Unpick' : 'Pick' }}
    </button>
    <div class="card mt-2 mb-3 movie-card">
      <div class="d-flex flex-column align-items-center">
        <img
          :src="getImageUrl(recommendedMovie.poster_path)"
          class="img-fluid rounded-top movie-image"
          alt="..."
        />
        <div class="card-body text-center">
          <h5 class="card-title">{{ recommendedMovie.title }}</h5>
        </div>
        <div class="card-footer bg-transparent">
          <button
            type="button"
            class="btn"
            @click="openModal"
            data-bs-toggle="modal"
            data-bs-target="#youtubeTrailerModal"
          >
            <img :src="youtubeLogo" alt="YouTube" class="youtube-logo" />
          </button>
          <YoutubeTrailerModal :movieTitle="recommendedMovie.title" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { usePickStore } from '@/stores/pickListStore'
import { useUserStore } from '@/stores/userStore'
import {
  addListMovie,
  getRecommendedMovieDetail,
  fetchWeather,
  selectGenreByWeather
} from '@/apis/movieApi'
import youtubeLogo from '@/assets/youtubeLogo.svg'
import YoutubeTrailerModal from '@/components/youtube/YoutubeTrailerModal.vue'

const weatherStatus = ref('')
const recommendedMovie = ref(null)
const isLoading = ref(true)

const pickStore = usePickStore()
const userStore = useUserStore()
const router = useRouter()

// 이미 Pick 했는지 여부를 판단
const isPicked = (movie) => {
  return pickStore.pickList.some((m) => m.id === movie.id || m.id === movie.pk)
}

// 날씨 정보 요청 및 이에 해당하는 추천 영화
const fetchMovie = () => {
  fetchWeather()
    .then((weather) => {
      const genrePk = selectGenreByWeather(weather)
      return getRecommendedMovieDetail(genrePk).then((movie) => {
        recommendedMovie.value = movie
        switch (weather) {
          case 'Rain':
            weatherStatus.value = '비 내리는'
            break
          case 'Snow':
            weatherStatus.value = '눈 내리는'
            break
          case 'Clear':
            weatherStatus.value = '쾌청한 날씨'
            break
          case 'Clouds':
            weatherStatus.value = '흐린'
            break
          default:
            weatherStatus.value = '흐린'
        }
      })
    })
    .catch((error) => {
      console.error(error)
    })
    .finally(() => {
      isLoading.value = false
    })
}

// Pick logic
const addToMyPickList = () => {
  if (!userStore.isLogin) {
    const userConfirmation = window.confirm(
      '로그인이 필요합니다. 로그인 페이지로 이동하시겠습니까?'
    )
    if (userConfirmation) {
      router.push({ name: 'userLogin' })
    }
    return
  }
  addListMovie(recommendedMovie.value.id || recommendedMovie.value.pk)
    .then((response) => {
      pickStore.addPick(recommendedMovie.value)
    })
    .catch((error) => {
      console.error('Error adding to list:', error)
    })
}

const getImageUrl = (path) => {
  // 이미지가 없는경우 예외처리
  if (!path) {
    return
  }
  return `https://image.tmdb.org/t/p/w500${path}`
}

onMounted(fetchMovie)
</script>

<style scoped>
.movie-card {
  max-width: 800px;
  margin: 0 auto;
  border-radius: 0.25rem;
}

.weather-div {
  margin: 1rem 0 2rem 0;
}

.youtube-logo {
  width: 36px;
  height: 36px;
}
</style>
