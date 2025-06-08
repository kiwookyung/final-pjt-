<template>
  <div class="movie-detail" style="margin-top: 90px">
    <!-- 상단 예고편 배경 (iframe) -->
    <div class="trailer-wrapper">
      <iframe v-if="trailerUrl" :src="trailerUrl" frameborder="0" allowfullscreen class="trailer-iframe"></iframe>
    </div>

    <!-- 포스터 + 개요/정보 -->
    <div class="detail-main">
      <div class="poster-box">
        <img :src="getImageUrl(movie.poster_path)" alt="Poster" />
      </div>
      <div class="info-box">
        <h1>{{ movie.title }}</h1>
        <p class="overview">{{ movie.overview }}</p>
        <div class="info-row">
          <p><strong>개봉일:</strong> {{ movie.release_date }}</p>
          <p><strong>런타임:</strong> {{ movie.runtime }} 분</p>
          <p><strong>예산:</strong> ${{ movie.budget.toLocaleString() }}</p>
          <p><strong>매출:</strong> ${{ movie.revenue.toLocaleString() }}</p>
          <p><strong>평점:</strong> {{ movie.vote_average }} / 10</p>
        </div>
        <div class="genre-box">
          <h3>장르</h3>
          <ul>
            <li v-for="genre in movie.genres" :key="genre.name">{{ genre.name }}</li>
          </ul>
        </div>
        <button class="pick-button" @click="addToMyPickList">
          <div class="pick-icon">{{ isPicked ? '❤️' : '🤍' }}</div>
          <div class="pick-label">관심</div>
        </button>
      </div>
    </div>

    <!-- 출연진 -->
    <div class="cast-section text-center mb-4">
      <h3>출연진</h3>
      <div class="actor-scroll">
        <div class="actor-card" v-for="actor in movie.actors" :key="actor.pk">
          <img :src="getImageUrl(actor.profile_path)" />
          <span>{{ actor.name }}</span>
        </div>
      </div>
    </div>
    <!-- 댓글 정렬 옵션 -->

    <!-- 게시판 -->
    <div class="movie-articles">
      <h2 class="text-center mb-4">게시판</h2>
      <div class="select-wrapper">
        <select v-model="sort" @change="fetchArticles" class="form-select w-auto">
          <option value="popular">인기순</option>
          <option value="recent">최신순</option>
        </select>
      </div>
      <div>
        <div v-for="article in articleStore.articles" :key="article.id" class="article-item">
          <MovieArticleCard :article="article" />
        </div>
      </div>

      <MovieArticleInput />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'
import { usePickStore } from '@/stores/pickListStore'
import { useArticleStore } from '@/stores/articleStore'
import { addListMovie } from '@/apis/movieApi'
import { youtubeTrailerApi } from '@/apis/youtubeApi'
import MovieArticleCard from '@/components/movie/MovieArticleCard.vue'
import MovieArticleInput from '@/components/movie/MovieArticleInput.vue'


const props = defineProps(['movie'])
const trailerUrl = ref('')

const userStore = useUserStore()
const pickStore = usePickStore()
const articleStore = useArticleStore()
const router = useRouter()
const sort = ref('popular')

const fetchArticles = () => articleStore.initializeArticles(props.movie.id, sort.value)
const getImageUrl = (path) => path ? `https://image.tmdb.org/t/p/w500${path}` : ''

onMounted(async () => {
  if (userStore.isLogin) pickStore.initializePickList()
  fetchArticles()
  trailerUrl.value = await youtubeTrailerApi(props.movie.title)
})

const isPicked = computed(() => userStore.isLogin && pickStore.pickList?.some(m => m.id === props.movie.id))
const addToMyPickList = () => {
  if (!userStore.isLogin) return router.push({ name: 'userLogin' })
  addListMovie(props.movie.id).then(() => pickStore.addPick(props.movie))
}
</script>

<style scoped>
.movie-detail {
  color: white;
  background-color: #000;
}

.trailer-wrapper {
  width: 100%;
  height: 50vh;
  overflow: hidden;
}

.trailer-iframe {
  width: 100%;
  height: 100%;
}

.detail-main {
  display: flex;
  flex-wrap: wrap;
  padding: 2rem;
  gap: 2rem;
  justify-content: center;
}

.poster-box img {
  width: 300px;
  border-radius: 10px;
}

.info-box {
  max-width: 600px;
}

.overview {
  margin: 1rem 0;
  font-size: 1.1rem;
}

.info-row p {
  margin: 0.5rem 0;
}

.genre-box ul {
  padding: 0;
  list-style: none;
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.cast-section {
  padding: 2rem;
}

.actor-scroll {
  display: flex;
  overflow-x: auto;
  gap: 1rem;
  padding-top: 1rem;
  justify-content: center;
}

.actor-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 80px;
  font-size: 0.8rem;
  color: #eee;
}

.actor-card img {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  object-fit: cover;
}

.movie-articles {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.select-wrapper {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1rem;
}

.pick-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: transparent;
  border: none;
  color: white;
  cursor: pointer;
}

.pick-icon {
  font-size: 24px;
}

.pick-label {
  font-size: 14px;
  margin-top: 4px;
}
</style>