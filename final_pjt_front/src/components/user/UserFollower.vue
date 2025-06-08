<template>
  <div class="modal-backdrop" @click.self="$emit('close')">
    <div class="modal-content">
      <button class="close-btn" @click="$emit('close')">×</button>

      <h3 v-if="show === 'followers'">팔로워 목록</h3>
      <h3 v-else-if="show === 'followings'">팔로잉 목록</h3>
      <h3 v-else>목록을 선택하세요</h3>

      <ul v-if="show === 'followers'">
        <li v-for="follower in user.followers || []" :key="follower.id">
          <RouterLink :to="`/user/profile/${follower.id}`" class="clickable">
            {{ follower.username.split('@')[0] }}
          </RouterLink>
        </li>
        <li v-if="(user.followers || []).length === 0">팔로워가 없습니다.</li>
      </ul>

      <ul v-if="show === 'followings'">
        <li v-for="following in user.followings || []" :key="following.id">
          <RouterLink :to="`/user/profile/${following.id}`" class="clickable">
            {{ following.username.split('@')[0] }}
          </RouterLink>
        </li>
        <li v-if="(user.followings || []).length === 0">팔로잉이 없습니다.</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
defineProps({
  user: Object,
  show: String
})
</script>

<style scoped>
.modal-backdrop {
  position: fixed !important;
  top: 90px !important;
  right: 20px !important;
  left: auto !important;
  width: 300px !important;
  max-height: 500px !important;
  background-color: #222 !important;
  border-radius: 8px !important;
  padding: 16px !important;
  color: white !important;
  overflow-y: auto !important;
  box-shadow: 0 0 10px rgba(0,0,0,0.8) !important;
  z-index: 1000 !important;
}

.modal-backdrop::before {
  content: "";
  position: fixed;
  top: 0; left: 0; bottom: 0; right: 0;
  background: rgba(0,0,0,0.5);
  z-index: -1;
}

.close-btn {
  position: absolute;
  top: 8px;
  right: 12px;
  background: transparent;
  border: none;
  color: #e50914;
  font-size: 24px;
  cursor: pointer;
}

h3 {
  margin-bottom: 12px;
  color: #e50914;
  margin-top: 0;
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

li {
  padding: 8px 0;
  border-bottom: 1px solid #444;
  color: white;
}

.clickable {
  color: #e50914;
  cursor: pointer;
  text-decoration: none;
}

.clickable:hover {
  text-decoration: underline;
}
</style>