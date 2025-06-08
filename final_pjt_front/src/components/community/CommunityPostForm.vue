<template>
  <form @submit.prevent="submitPost" class="post-form">
    <input
      v-model="title"
      type="text"
      placeholder="제목을 입력하세요"
      required
    />
    <textarea
      v-model="content"
      placeholder="내용을 입력하세요"
      required
    ></textarea>

    <!-- 양쪽 정렬 -->
    <div class="form-footer">
      <RouterLink to="/community" class="back-btn">뒤로가기</RouterLink>
      <button type="submit" class="submit-btn">작성하기</button>
    </div>
  </form>
</template>

<script setup>
import { ref, watch } from 'vue'
import { RouterLink } from 'vue-router'

const props = defineProps({
  initialData: {
    type: Object,
    default: () => ({
      title: '',
      content: '',
      image: null,
    }),
  },
})

const emit = defineEmits(['submit'])

const title = ref(props.initialData.title)
const content = ref(props.initialData.content)
const imageFile = ref(null)
const previewUrl = ref('')

watch(
  () => props.initialData.image,
  (newImage) => {
    if (newImage) {
      previewUrl.value = `http://localhost:8000${newImage}`
    }
  },
  { immediate: true }
)

const handleFileChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    imageFile.value = file
    previewUrl.value = URL.createObjectURL(file)
  }
}

const submitPost = () => {
  const formData = new FormData()
  formData.append('title', title.value)
  formData.append('content', content.value)
  if (imageFile.value) {
    formData.append('image', imageFile.value)
  }

  emit('submit', formData)
}
</script>

<style scoped>
.post-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

input[type="text"],
textarea {
  padding: 0.8rem;
  background-color: #2c2c2c;
  border: none;
  border-radius: 8px;
  color: #f1f1f1;
  font-size: 1rem;
}

input::placeholder,
textarea::placeholder {
  color: #888;
}

textarea {
  height: 150px;
  resize: vertical;
}

input[type="file"] {
  color: #ccc;
}

.preview-container {
  margin-top: 0.5rem;
}

.preview-image {
  width: 100%;
  max-height: 200px;
  object-fit: cover;
  border-radius: 8px;
}

/* 하단 버튼 줄 */
.form-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1.5rem;
}

.submit-btn,
.back-btn {
  background-color: transparent;
  font-weight: bold;
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  text-decoration: none;
  border: 2px solid;
  cursor: pointer;
  transition: all 0.25s ease;
}

/* 작성하기 → 파란 네온 */
.submit-btn {
  color: #3a82f6;
  border-color: #3a82f6;
  box-shadow: 0 0 8px rgba(58, 130, 246, 0.5);
}
.submit-btn:hover {
  background-color: #3a82f6;
  color: #121212;
  box-shadow: 0 0 12px rgba(58, 130, 246, 0.9), 0 0 20px rgba(58, 130, 246, 0.6);
}

/* 커뮤니티로 → 빨간 네온 */
.back-btn {
  color: #ff6b6b;
  border-color: #ff6b6b;
  box-shadow: 0 0 8px rgba(255, 107, 107, 0.5);
}
.back-btn:hover {
  background-color: #ff6b6b;
  color: #121212;
  box-shadow: 0 0 12px rgba(255, 107, 107, 0.9), 0 0 20px rgba(255, 107, 107, 0.6);
}

</style>
