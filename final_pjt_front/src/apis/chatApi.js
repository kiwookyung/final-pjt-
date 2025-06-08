import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_BASE_URL

export const askChatbot = (message) => {
  return axios.post(`${BASE_URL}/movies/chatbot/`, { message })
}
