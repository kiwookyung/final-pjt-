import { ref } from 'vue'
import { defineStore } from 'pinia'
import { userProfileApi } from '@/apis/userApi'
import { useUserStore } from '@/stores/userStore'

export const usePickStore = defineStore('pick', () => {
  const pickList = ref([])

  const initializePickList = () => {
    const userStore = useUserStore()
    const userPk = userStore.userData.pk

    userProfileApi(userPk)
      .then((response) => {
        if (response && response.data) {
          pickList.value = response.data.like_movies
        }
      })
      .catch((error) => {
        console.error('Error initializing pickList:', error)
      })
  }

  const addPick = (movie) => {
    const index = pickList.value.findIndex((m) => m.id === movie.id || m.id === movie.pk)
    if (index !== -1) {
      pickList.value.splice(index, 1)
    } else {
      pickList.value.push({ id: movie.id || movie.pk, title: movie.title, isWatched: false })
    }
  }

  return {
    pickList,
    initializePickList,
    addPick
  }
})
