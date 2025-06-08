const API_URL = 'http://127.0.0.1:8000'
const TMDB_URL = 'https://api.themoviedb.org/3/movie/top_rated?language=ko-KR&page=1'
const weatherApiKey = import.meta.env.VITE_WEATHER_API_KEY
const TMDB_KEY = import.meta.env.VITE_TMDB_API_KEY

// Top Rated 영화 API
import axios from 'axios'

export function getTopRatedMoviesFromDB() {
  return axios.get('http://localhost:8000/movies/top-rated/')
}

// 최신 영화 섹션
export function getLatestMovies() {
  return axios.get(`${API_URL}/movies/?sort=release_date`)
}

// 누적 인기 영화 섹션
export function getMostWatchedMovies() {
  return axios.get(`${API_URL}/movies/?sort=vote_count`)
}

// 장르 목록
export function getGenres() {
  return axios.get(`${API_URL}/movies/genres/`)
}

// 특정 장르의 영화 최대 20개
export function getMoviesByGenre(genreId, limit = 20) {
  return axios.get(`${API_URL}/movies/genres/${genreId}/movies/?limit=${limit}`)
}


// 영화 List 조회 API
export const getMoviesList = (page = 1) => {
  return axios.get(`${API_URL}/movies/?page=${page}`)
}

// 각 영화 상세 조회 API
export const getMovieDetail = (moviePk) => {
  return axios.get(`${API_URL}/movies/${moviePk}/`)
}

// 날씨 기반 추천을 위한 현재 서울 날씨 조회 API
export const fetchWeather = () => {
  const url = `http://api.openweathermap.org/data/2.5/weather?q=Seoul&appid=${weatherApiKey}`
  return axios.get(url).then((response) => response.data.weather[0].main)
}

// 날씨 기반 추천 장르 알고리즘
export const selectGenreByWeather = (weather) => {
  switch (weather) {
    case 'Rain':
      return 27 // 공포
    case 'Snow':
      return 28 // 액션
    case 'Clear':
      return 12 // 모험
    case 'Clouds':
      return 35 // 코미디
    default:
      return 35 // Comedy
  }
}

// 날씨 기반 추천
export const getRecommendedMovies = (genrePk, limit = 10) => {
  return axios.get(`${API_URL}/movies/recommended/${genrePk}/`)
    .then((res) => res.data.slice(0, limit))
}


// 사용자의 영화 Pick API
export const addListMovie = (moviePk) => {
  const token = window.localStorage.getItem('token')

  return axios.post(
    `${API_URL}/movies/${moviePk}/addlist/`,
    {},
    {
      headers: {
        Authorization: `Token ${token}`
      }
    }
  )
}

// 영화 article List 조회
export const fetchMovieArticles = (moviePk, sort = 'popular') => {
  return axios
    .get(`${API_URL}/movies/${moviePk}/articles/?sort=${sort}`)
    .then((response) => {
      return response
    })
    .catch((error) => {
      console.error('API 요청 중 에러가 발생했습니다:', error)
      throw error
    })
}

// 사용자의 영화 평론 작성 API
export const createMovieArticle = (moviePk, payload) => {
  const token = window.localStorage.getItem('token')
  return axios
    .post(`${API_URL}/movies/${moviePk}/articles/`, payload, {
      headers: {
        Authorization: `Token ${token}`
      }
    })
    .then((response) => {
      return response
    })
    .catch((error) => {
      console.error('API 요청 중 에러가 발생했습니다:', error)
      throw error
    })
}

// 사용자의 영화 평론 삭제 API
export const deleteMovieArticle = (moviePk, articlePk) => {
  const token = window.localStorage.getItem('token')
  return axios
    .delete(`${API_URL}/movies/${moviePk}/articles/${articlePk}`, {
      headers: {
        Authorization: `Token ${token}`
      }
    })
    .then((response) => {
      return response
    })
    .catch((error) => {
      console.error('API 요청 중 에러가 발생했습니다:', error)
      throw error
    })
}

// 사용자의 영화 평론 수정 API
export const updateMovieArticle = (moviePk, articlePk, payload) => {
  const token = window.localStorage.getItem('token')
  return axios
    .put(`${API_URL}/movies/${moviePk}/articles/${articlePk}/`, payload, {
      headers: {
        Authorization: `Token ${token}`
      }
    })
    .then((response) => {
      return response
    })
    .catch((error) => {
      console.error('API 요청 중 에러가 발생했습니다:', error)
      throw error
    })
}

// 영화 comment List 조회
export const getCommentList = (moviePk, articlePk) => {
  return axios
    .get(`${API_URL}/movies/${moviePk}/articles/${articlePk}/comments/`)
    .then((response) => {
      return response
    })
    .catch((error) => {
      console.error('API 요청 중 에러가 발생했습니다:', error)
      throw error
    })
}

// 사용자의 comment 작성 API
export const createNewCommentAPI = (moviePk, articlePk, payload) => {
  const token = window.localStorage.getItem('token')
  return axios
    .post(`${API_URL}/movies/${moviePk}/articles/${articlePk}/comments/`, payload, {
      headers: {
        Authorization: `Token ${token}`
      }
    })
    .then((response) => {
      return response
    })
    .catch((error) => {
      console.error('API 요청 중 에러가 발생했습니다:', error)
      throw error
    })
}

// 사용자의 comment 삭제 API
export const deleteComment = (moviePk, articlePk, commentPk) => {
  const token = window.localStorage.getItem('token')
  return axios
    .delete(`${API_URL}/movies/${moviePk}/articles/${articlePk}/comments/${commentPk}`, {
      headers: {
        Authorization: `Token ${token}`
      }
    })
    .then((response) => {
      return response
    })
    .catch((error) => {
      console.error('API 요청 중 에러가 발생했습니다:', error)
      throw error
    })
}

// 사용자의 article 좋아요 API
export const likeArticleApi = (moviePk, articlePk) => {
  const token = window.localStorage.getItem('token')
  return axios
    .post(
      `${API_URL}/movies/${moviePk}/articles/${articlePk}/comments/like/`,
      {},
      {
        headers: {
          Authorization: `Token ${token}`
        }
      }
    )
    .then((response) => {
      return response
    })
    .catch((error) => {
      console.error('API 요청 중 에러가 발생했습니다:', error)
      throw error
    })
}

// 전체 검색
export const getAllMovies = () => {
  return axios.get(`${API_URL}/movies/all/`)
}
