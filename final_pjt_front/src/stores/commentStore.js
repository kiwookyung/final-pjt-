// src/stores/commentStore.js
import { ref } from 'vue'
import { defineStore } from 'pinia'
import { getCommentList, createNewCommentAPI, deleteComment } from '@/apis/movieApi'

export const useCommentStore = defineStore('comment', () => {
  // articleId -> comments 배열
  const commentMap = ref({})

  const initializeComments = (moviePk, articlePk) => {
    return getCommentList(moviePk, articlePk)
      .then((response) => {
        if (response && response.data) {
          commentMap.value[articlePk] = response.data
        }
      })
      .catch((error) => {
        console.error('Error initializing comments:', error)
      })
  }

  const createNewComment = (moviePk, articlePk, payload) => {
    return createNewCommentAPI(moviePk, articlePk, payload)
      .then((response) => {
        if (response.status === 201) {
          commentMap.value[articlePk] = response.data
        }
      })
      .catch((error) => {
        console.error('Error creating a new comment:', error)
      })
  }

  const deleteOldComment = (moviePk, articlePk, commentPk) => {
    return deleteComment(moviePk, articlePk, commentPk)
      .then((response) => {
        if (response.status === 200) {
          commentMap.value[articlePk] = response.data
        }
      })
      .catch((error) => {
        console.error('Error deleting an old comment:', error)
      })
  }

  // getter
  const getCommentsByArticle = (articlePk) => {
    return commentMap.value[articlePk] || []
  }

  return {
    commentMap,
    initializeComments,
    createNewComment,
    deleteOldComment,
    getCommentsByArticle
  }
})