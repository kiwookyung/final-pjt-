<template>
  <div class="not-found-container">
    <h1>404</h1>
    <p>죄송합니다. 찾을 수 없는 페이지입니다.</p>
    <a href="/">홈으로 돌아가기</a>
  </div>
</template>

<script setup></script>

<style>
.not-found-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #f0f0f0;
  text-align: center;
}

.not-found-container h1 {
  font-size: 10rem;
  margin: 0;
  color: #555;
}

.not-found-container p {
  font-size: 1.5rem;
  margin: 20px 0;
  color: #888;
}

.not-found-container a {
  font-size: 1rem;
  color: #00c8ff;
  text-decoration: none;
  padding: 10px 20px;
  border: 1px solid #00c8ff;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.not-found-container a:hover {
  background-color: #00c8ff;
  color: #fff;
}
</style>
