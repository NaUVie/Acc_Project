<template>
  <transition name="toast-slide">
    <div v-if="toast.show" :class="['toast-notification', `toast-${toast.type}`]">
      <div class="toast-icon">
        <span v-if="toast.type === 'success'">✅</span>
        <span v-else-if="toast.type === 'error'">❌</span>
        <span v-else-if="toast.type === 'warning'">⚠️</span>
        <span v-else>ℹ️</span>
      </div>
      <div class="toast-content">
        {{ toast.message }}
      </div>
      <button class="toast-close" @click="hideToast">&times;</button>
    </div>
  </transition>
</template>

<script setup>
import { computed } from 'vue';
import { useCourseStore } from '@/stores/courses';

const courseStore = useCourseStore();
const toast = computed(() => courseStore.toast);

const hideToast = () => {
  courseStore.hideToast();
};
</script>

<style scoped src="@/styles/components/ToastNotification.css"></style>
