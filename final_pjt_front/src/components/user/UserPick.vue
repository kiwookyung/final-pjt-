<template>
  <div class="like-movie-info container">
    <div
      v-if="user && user.like_movies && user.like_movies.length"
      class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 row-cols-xl-5 g-4"
    >
      <div class="col" v-for="like_movie in user.like_movies" :key="like_movie.id">
        <UserPickCard :movie="like_movie" />
      </div>
    </div>
    <div v-else class="d-flex justify-content-center align-items-center mt-5">
      <p>
        <span
          style="color: rgb(53, 194, 226); font-weight: bold; margin-right: 0.5rem; font-size: 2rem"
          >Pick</span
        >한 영화가 없습니다.
      </p>
    </div>
  </div>
</template>

<script setup>
import UserPickCard from '@/components/user/UserPickCard.vue'

const props = defineProps(['user'])
</script>

<style scoped>
.like-movie-info {
  width: 80%;
  padding: 20px;
}
</style>
