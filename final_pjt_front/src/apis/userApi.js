// src/apis/userApi.js
import axios from "axios";
import Swal from "sweetalert2";

const API_URL = "http://127.0.0.1:8000";

// 에러 메시지 번역 함수
const translateMessage = (message) => {
  const translations = {
    "User with this username already exists.": "이미 존재하는 아이디입니다.",
    "This password is too common.": "비밀번호가 너무 단순합니다.",
  };
  return translations[message] || "";
};

// 회원가입 API
export const signUpApi = (payload) => {
  return axios
    .post(`${API_URL}/accounts/signup/`, payload)
    .then((response) => response)
    .catch((error) => {
      if (error.response && error.response.data) {
        const errorData = error.response.data;
        let errorMessage = "";

        Object.values(errorData).forEach((messages) => {
          const translatedMessages = messages
            .map(translateMessage)
            .filter(Boolean);
          errorMessage += `${translatedMessages.join(", ")}<br>`;
        });

        if (errorMessage) {
          Swal.fire({
            title: "회원가입 에러",
            html: errorMessage,
            icon: "error",
            confirmButtonColor: "#682cd48c",
            confirmButtonText: "확인",
          });
        }
      } else {
        console.error("알 수 없는 에러가 발생했습니다.", error);
      }
    });
};

// 로그인 API
export const loginApi = (payload) => {
  return axios
    .post(`${API_URL}/accounts/login/`, payload)
    .then((response) => response)
    .catch((error) => {
      console.error("API 요청 중 에러가 발생했습니다:", error);
      throw error;
    });
};

// 로그아웃 API
export const logoutApi = () => {
  return axios
    .post(`${API_URL}/accounts/logout/`)
    .then((response) => response)
    .catch((error) => {
      console.error("API 요청 중 에러가 발생했습니다:", error);
      throw error;
    });
};

// 유저 프로필 조회 API
export const userProfileApi = (userPk) => {
  return axios
    .get(`${API_URL}/profile/${userPk}/`)
    .then((response) => response)
    .catch((error) => {
      console.error("API 요청 중 에러가 발생했습니다:", error);
      throw error;
    });
};

// 현재 로그인한 유저 정보 조회 API
export const fetchCurrentUserApi = (token) => {
  return axios
    .get(`${API_URL}/accounts/user/`, {
      headers: {
        Authorization: `Token ${token}`,
      },
    })
    .then((response) => response)
    .catch((error) => {
      console.error("API 요청 중 에러가 발생했습니다:", error);
      throw error;
    });
};

// 팔로우 상태 확인 API
export const checkFollowingApi = (token, userPk) => {
  return axios
    .get(`${API_URL}/profile/${userPk}/follow/status/`, {
      headers: {
        Authorization: `Token ${token}`,
      },
    })
    .then((response) => response)
    .catch((error) => {
      console.error("API 요청 중 에러가 발생했습니다:", error);
      throw error;
    });
};

// 팔로우 API
// 팔로우 API
export const followApi = (token, userPk) => {
  return axios.post(
    `${API_URL}/profile/${userPk}/follow/`,
    {},
    { headers: { Authorization: `Token ${token}` } }
  )
}

// 언팔로우 API (DELETE 대신 POST /unfollow/)
export const unfollowApi = (token, userPk) => {
  return axios.post(
    `${API_URL}/profile/${userPk}/follow/`,
    {},
    { headers: { Authorization: `Token ${token}` } }
  )
};

// 프로필 사진 변경 API
export const profilePicEdit = (userPk, payload) => {
  const token = window.localStorage.getItem("token");

  return axios
    .put(`${API_URL}/profile/${userPk}/update/`, payload, {
      headers: {
        "Content-Type": "multipart/form-data",
        Authorization: `Token ${token}`,
      },
    })
    .then((response) => response)
    .catch((error) => {
      console.error("API 요청 중 에러가 발생했습니다:", error);
      throw error;
    });
};

export const deleteUserApi = (token, userId) => {
  return axios.delete(`${API_URL}/profile/${userId}/delete/`, {
    headers: {
      Authorization: `Token ${token}`,
    },
  });
};

// 회원정보 수정 API
export const updateUserProfileApi = (token, userId, formData) => {
  return axios.put(`${API_URL}/profile/${userId}/update/`, formData, {
    headers: {
      Authorization: `Token ${token}`,
      'Content-Type': 'multipart/form-data',
    },
  })
  .then(response => response)
  .catch(error => {
    console.error("API 요청 중 에러가 발생했습니다:", error.response?.data || error);
    throw error;
  });
};


//비밀번호 변경
// userApi.js 예시
export const changePasswordApi = (token, payload) => {
  return axios.put('http://127.0.0.1:8000/profile/change-password/', payload, {
    headers: {
      Authorization: `Token ${token}`,
      'Content-Type': 'application/json'
    }
  })
}