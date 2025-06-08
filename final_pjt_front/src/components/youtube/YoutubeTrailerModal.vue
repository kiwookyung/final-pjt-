<template>
  <div
    ref="modalRef"
    class="modal fade"
    id="youtubeTrailerModal"
    tabindex="-1"
    aria-labelledby="youtubeTrailerLabel"
    :aria-hidden="!isModalVisible"
  >
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="youtubeTrailerLabel">
            {{ movieTitle }} 공식 예고편
          </h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
            @click="stopVideo"
          ></button>
        </div>
        <div class="modal-body">
          <div
            v-if="isLoading"
            class="spinner-border text-primary"
            role="status"
          >
            <span class="visually-hidden">Loading...</span>
          </div>
          <iframe
            v-else-if="videoData"
            class="trailer-iframe"
            :src="videoData"
            frameborder="0"
            allowfullscreen
          ></iframe>
          <div v-else>
            <p>예고편을 찾을 수 없습니다.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref } from "vue";
import { youtubeTrailerApi } from "@/apis/youtubeApi";

const props = defineProps({
  movieTitle: String,
});

const videoData = ref("");
const isLoading = ref(false);
const modalRef = ref(null);
const isModalVisible = ref(false);

const stopVideo = () => {
  videoData.value = "";
};

const fetchTrailer = () => {
  isLoading.value = true;
  youtubeTrailerApi(props.movieTitle)
    .then((response) => {
      if (response) {
        videoData.value = response;
      } else {
        videoData.value = "";
      }
    })
    .catch((error) => {
      console.error("서버에러:", error);
    })
    .finally(() => {
      isLoading.value = false;
    });
};

onMounted(() => {
  if (modalRef.value) {
    modalRef.value.addEventListener("show.bs.modal", () => {
      isModalVisible.value = true;
      fetchTrailer();
    });

    modalRef.value.addEventListener("hidden.bs.modal", () => {
      isModalVisible.value = false;
    });
  }
});

onBeforeUnmount(() => {
  if (modalRef.value) {
    modalRef.value.removeEventListener("show.bs.modal", fetchTrailer);
    modalRef.value.removeEventListener("hidden.bs.modal", () => {
      isModalVisible.value = false;
    });
  }
});
</script>

<style scoped>
.modal-content {
  max-width: 820px;
}

.trailer-iframe {
  width: 720px;
  height: 450px;
  display: block;
  margin: 0 auto;
}
</style>
