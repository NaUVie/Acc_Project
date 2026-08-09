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

<style scoped>
.toast-notification {
  position: fixed;
  top: 24px;
  right: 24px;
  z-index: 99999;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 20px;
  border-radius: 12px;
  background: #ffffff;
  color: #1e293b;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15), 0 2px 8px rgba(0, 0, 0, 0.08);
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  font-weight: 600;
  max-width: 400px;
  border-left: 5px solid #00f2fe;
}

.toast-success {
  border-left-color: #10b981;
}

.toast-error {
  border-left-color: #ef4444;
}

.toast-warning {
  border-left-color: #f59e0b;
}

.toast-info {
  border-left-color: #3b82f6;
}

.toast-icon {
  font-size: 18px;
}

.toast-content {
  flex: 1;
  line-height: 1.4;
}

.toast-close {
  background: none;
  border: none;
  font-size: 20px;
  color: #94a3b8;
  cursor: pointer;
  padding: 0 4px;
  line-height: 1;
  transition: color 0.2s ease;
}

.toast-close:hover {
  color: #0f172a;
}

/* Animations */
.toast-slide-enter-active,
.toast-slide-leave-active {
  transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}

.toast-slide-enter-from {
  opacity: 0;
  transform: translateY(-20px) scale(0.95);
}

.toast-slide-leave-to {
  opacity: 0;
  transform: translateX(40px);
}
</style>
