import axios from 'axios'

const API_URL = 'http://localhost:8000/api/v1/community/'

// 토큰이 필요한 요청에 Authorization 헤더 추가
const getAuthHeaders = () => {
  const token = window.localStorage.getItem('token')
  return {
    headers: {
      Authorization: `Token ${token}`
    }
  }
}

// ✅ 1. 전체 커뮤니티 글 가져오기
export const fetchCommunityPosts = () => {
  return axios.get(API_URL)
}

// ✅ 2. 커뮤니티 글 작성
export const createCommunityPost = (newPost) => {
  return axios.post(API_URL, newPost, getAuthHeaders())
}

// ✅ 3. 커뮤니티 글 삭제
export const deleteCommunityPost = (postPk) => {
  return axios.delete(`${API_URL}${postPk}/`, getAuthHeaders())
}

// ✅ 4. 커뮤니티 글 수정
export const updateCommunityPost = (postPk, updatedData) => {
  return axios.put(`${API_URL}${postPk}/`, updatedData, getAuthHeaders())
}

// ✅ 5. 단일 게시글 상세 조회 (선택사항)
export const fetchCommunityPost = (postPk) => {
  return axios.get(`${API_URL}${postPk}/`)
}