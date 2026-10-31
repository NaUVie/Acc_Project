<template>
  <Teleport to="body">
    <transition name="confirm-fade">
      <div v-if="confirmState.show" class="confirm-backdrop" @click.self="cancel">
        <div class="confirm-modal-card glass-card">
          <div class="confirm-header">
            <div class="confirm-icon-wrapper" :class="confirmState.type">
              <span v-if="confirmState.type === 'danger'">🗑️</span>
              <span v-else-if="confirmState.type === 'warning'">⚠️</span>
              <span v-else>❓</span>
            </div>
            <h3 class="confirm-title">{{ confirmState.title }}</h3>
          </div>

          <div class="confirm-body">
            <p class="confirm-message">{{ confirmState.message }}</p>
          </div>

          <div class="confirm-footer">
            <button type="button" @click="cancel" class="btn btn-secondary btn-sm confirm-btn-cancel">
              {{ confirmState.cancelText }}
            </button>
            <button 
              type="button" 
              @click="confirm" 
              class="btn btn-sm confirm-btn-action"
              :class="confirmState.type === 'danger' ? 'btn-danger-gradient' : 'btn-primary'"
            >
              {{ confirmState.confirmText }}
            </button>
          </div>
        </div>
      </div>
    </transition>
  </Teleport>
</template>

<script setup>
import { computed } from 'vue';
import { useCourseStore } from '@/stores/courses';

const courseStore = useCourseStore();
const confirmState = computed(() => courseStore.confirmModal);

const confirm = () => {
  courseStore.handleConfirmResult(true);
};

const cancel = () => {
  courseStore.handleConfirmResult(false);
};
</script>

<style scoped src="@/styles/components/ConfirmModal.css"></style>
