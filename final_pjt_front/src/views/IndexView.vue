<template>
  <div class="main-content">

    <div>
      <!-- Top Rated Movies -->
      <RankedMovieCarousel title="🏆 Top Rated Movies" :movies="movies" />
      <!-- 날씨 기반 추천 영화 -->
      <h2 class="weather-heading">
        <span class="emoji">{{ weatherEmoji }}</span>
        <span class="gradient-text">{{ weatherText }} 이런 영화 어때요?</span>
      </h2>

      <MovieCarousel :movies="weatherMovies" :title="null" />



      <MovieCarousel title=" 개봉 예정" :movies="latestMovies" class="section-title" />
      <MovieCarousel title=" 누적 인기 영화" :movies="popularMovies" class="section-title" />
    </div>

    <div v-for="genre in genres" :key="genre.id">
      <GenreCarouselSection :genre="genre" />
    </div>

    <ScrollToTop />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import MovieCard from '@/components/movie/MovieCard.vue'
import { getLatestMovies, getMostWatchedMovies, getGenres, fetchWeather, selectGenreByWeather, getRecommendedMovies, getTopRatedMoviesFromDB } from '@/apis/movieApi'
import MovieCarousel from '@/components/movie/MovieCarousel.vue'
import GenreCarouselSection from '@/components/movie/GenreCarouselSection.vue'
import RankedMovieCarousel from '@/components/movie/RankedMovieCarousel.vue'
import ScrollToTop from '@/components/common/ScrollToTop.vue'

const movies = ref([])
const latestMovies = ref([])
const popularMovies = ref([])
const genres = ref([])
const weatherMovies = ref([])
const weatherText = ref('')
const weatherEmoji = ref('')


const topRankedMovies = [
  { id: 1, title: 'Inception', poster_path: '', vote_average: 8.8 },
  { id: 2, title: 'The Dark Knight', poster_path: '', vote_average: 9.0 },
  // 실제 API 연결 예정
]

// Top Rated 영화 목록
const fetchMovie = () => {
  getTopRatedMoviesFromDB()
    .then((res) => {
      console.log('🔥 Top Rated (DB 기반) 응답:', res.data)
      movies.value = res.data
    })
    .catch((error) => {
      console.error('추천 영화 로딩 실패:', error)
    })
}



// 최신 영화
const fetchLatestMovies = () => {
  getLatestMovies()
    .then((response) => {
      console.log('🎉 최신 응답:', response.data)
      latestMovies.value = response.data
    })
    .catch((error) => console.error(error))
}

// 누적 영화
const fetchPopularMovies = () => {
  getMostWatchedMovies()
    .then((response) => {
      popularMovies.value = response.data
    })
    .catch((error) => console.error(error))
}

// 장르
const fetchGenres = () => {
  getGenres()
    .then((res) => {
      genres.value = res.data
    })
    .catch((err) => console.error(err))
}

// 날씨 기반 추천 영화
const fetchWeatherBasedMovies = async () => {
  try {
    const weather = await fetchWeather()
    const genrePk = selectGenreByWeather(weather)
    const movies = await getRecommendedMovies(genrePk)
    switch (weather) {
      case 'Rain':
        weatherEmoji.value = '🌧️'
        weatherText.value = '비 오는 날에는'
        break
      case 'Clear':
        weatherEmoji.value = '☀️'
        weatherText.value = '맑은 날엔'
        break
      case 'Clouds':
        weatherEmoji.value = '☁️'
        weatherText.value = '구름 낀 날엔'
        break
      case 'Snow':
        weatherEmoji.value = '❄️'
        weatherText.value = '눈 오는 날엔'
        break
      default:
        weatherEmoji.value = ''
        weatherText.value = '오늘 같은 날엔'
    }

    weatherMovies.value = movies
  } catch (error) {
    console.error('날씨 기반 추천 영화 로딩 실패:', error)
  }
}


onMounted(() => {
  fetchMovie()
  fetchLatestMovies()
  fetchPopularMovies()
  fetchGenres()
  fetchWeatherBasedMovies()
})
</script>

<style scoped>
.section-title {
  display: inline-block;
  vertical-align: middle;
  color: #fff;
  font-size: 24px;
  line-height: 36px;
  font-style: normal;
  word-break: break-word;
}
</style>