import { ref } from 'vue'
import { defineStore } from 'pinia'
import {
  fetchMovieArticles,
  createMovieArticle,
  deleteMovieArticle,
  updateMovieArticle
} from '@/apis/movieApi'

export const useArticleStore = defineStore('article', () => {
  const articles = ref([])

  const initializeArticles = (moviePk, sort = 'popular') => {
    fetchMovieArticles(moviePk, sort)
      .then((response) => {
        if (response && response.data) {
          articles.value = response.data
        }
      })
      .catch((error) => {
        console.error('Error initializing articles:', error)
      })
  }

  const addArticle = (moviePk, newArticle) => {
    return createMovieArticle(moviePk, newArticle)
      .then((response) => {
        if (response.status === 201) {
          articles.value.push(response.data)
          window.alert('성공적으로 글이 작성됐습니다!')
        }
      })
      .catch((error) => {
        console.error(error)
        throw error
      })
  }

  const deleteArticle = (moviePk, articlePk) => {
    return deleteMovieArticle(moviePk, articlePk)
      .then((response) => {
        if (response.status === 200) {
          const index = articles.value.findIndex((article) => article.pk === articlePk)
          if (index !== -1) {
            articles.value.splice(index, 1)
          }
          return response
        } else {
          window.alert('서버 오류')
        }
      })
      .catch((error) => {
        console.error(error)
        throw error
      })
  }

  const updateArticle = (moviePk, articlePk, newContent) => {
    return updateMovieArticle(moviePk, articlePk, newContent)
      .then((response) => {
        if (response.status === 200) {
          const article = articles.value.find((article) => article.pk === articlePk)
          if (article) {
            article.content = newContent
          }
          return response
        } else {
          window.alert('서버 오류')
        }
      })
      .catch((error) => {
        console.error(error)
      })
  }

  return {
    articles,
    initializeArticles,
    addArticle,
    deleteArticle,
    updateArticle
  }
})
