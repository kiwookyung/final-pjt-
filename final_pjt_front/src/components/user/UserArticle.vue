<template>
  <div class="like-movie-info container">
    <div
      v-if="user && user.articles && user.articles.length"
      class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 row-cols-xl-5 g-4"
    >
      <div class="col" v-for="article in user.articles" :key="article.id">
        <UserArticleCard :article="article" style="cursor: pointer" />
      </div>
    </div>
    <div v-else class="d-flex justify-content-center align-items-center mt-5">
      <p>작성한 리뷰가 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import UserArticleCard from '@/components/user/UserArticleCard.vue'

const props = defineProps(['user', 'isCurrentUser'])
</script>

<style scoped>
.like-movie-info {
  width: 80%;
  padding: 20px;
}
</style>
