<template>
  <div class="modal fade" :id="'modal' + article.id" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ article.title }}</h5>
          <button class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body">
          <p v-html="formatContent(article.content)"></p>
          <p>
            <RouterLink :to="`/user/profile/${article.user.pk}/pick`">
              <img :src="article.user.profile_pic ? userProfilePic : AvatarSrc" class="profile-pic" />
              {{ username }}
            </RouterLink>
          </p>
          <p>평점: {{ article.rate }}/10</p>
          <p>작성일: {{ formattedDate }}</p>
          <p>좋아요: {{ article.like_user_count }}</p>
          <MovieArticleComment :article="article" />
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import AvatarSrc from '@/assets/avatar.png'
import { useUserStore } from '@/stores/userStore'
import MovieArticleComment from '@/components/movie/MovieArticleComment.vue'

const props = defineProps(['article'])

const userStore = useUserStore()
const isOwner = computed(() => props.article.user.pk === userStore.userData.pk)
const username = computed(() => props.article.user.username.split('@')[0])
const userProfilePic = computed(() => `http://localhost:8000${props.article.user.profile_pic}`)

const formatContent = (content) => content.replace(/\n/g, '<br />')
const formattedDate = computed(() => {
  const d = new Date(props.article.created_at)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
})
</script>

<style scoped>
.profile-pic {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}
.modal-body {
  background-color: #222;
  color: white;
}
.modal-header,
.modal-footer {
  background-color: #222;
}
</style>