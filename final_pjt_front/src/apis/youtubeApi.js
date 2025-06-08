import axios from 'axios'
const baseURL = 'https://www.googleapis.com/youtube/v3/search'
const youtubeKey = import.meta.env.VITE_YOUTUBE_API_KEY

// 유튜브 공식 예고편 API
export const youtubeTrailerApi = (movieTitle) => {
  return axios
    .get(baseURL, {
      params: {
        key: youtubeKey,
        part: 'snippet',
        type: 'video',
        q: `영화 ${movieTitle} 공식 예고편`,
        maxResults: 1
      }
    })
    .then((response) => {
      if (response.data.items && response.data.items.length > 0) {
        const videoId = response.data.items[0].id.videoId
        const res = `https://www.youtube.com/embed/${videoId}?autoplay=1&mute=1`
        return res
      } else {
        window.alert('영화 예고편이 없습니다')
      }
    })
    .catch((error) => {
      console.error('서버에러:', error)
    })
}
