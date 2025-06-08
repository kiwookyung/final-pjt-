import { ref } from 'vue'
import { defineStore } from 'pinia'
import {
  fetchCommunityPosts,
  createCommunityPost,
  deleteCommunityPost,
  updateCommunityPost
} from '@/apis/communityApi'

export const useCommunityStore = defineStore('community', () => {
  const posts = ref([])

  const initializePosts = () => {
    fetchCommunityPosts()
      .then(res => {
        posts.value = res.data
      })
      .catch(err => {
        console.error('게시글 로딩 실패:', err)
      })
  }

  const addPost = (newPost) => {
    return createCommunityPost(newPost)
      .then(res => {
        if (res.status === 201) {
          posts.value.unshift(res.data)
        }
      })
  }

  const deletePost = (postPk) => {
    return deleteCommunityPost(postPk)
      .then(res => {
        posts.value = posts.value.filter(p => p.pk !== postPk)
      })
  }

  const updatePost = (postPk, updatedData) => {
    return updateCommunityPost(postPk, updatedData)
      .then(res => {
        const post = posts.value.find(p => p.pk === postPk)
        if (post) Object.assign(post, res.data)
      })
  }

  return {
    posts,
    initializePosts,
    addPost,
    deletePost,
    updatePost
  }
})
