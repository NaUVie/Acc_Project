<template>
  <div class="pagination-wrapper" v-if="totalPages > 1">
    <button 
      class="pagination-btn prev-btn" 
      :disabled="currentPage === 1" 
      @click="changePage(currentPage - 1)"
      title="Trang trước"
    >
      ‹ Trước
    </button>

    <div class="page-numbers">
      <button 
        v-for="(page, index) in visiblePages" 
        :key="index" 
        class="page-num-btn"
        :class="{ active: page === currentPage, ellipsis: page === '...' }"
        :disabled="page === '...'"
        @click="page !== '...' && changePage(page)"
      >
        {{ page }}
      </button>
    </div>

    <button 
      class="pagination-btn next-btn" 
      :disabled="currentPage === totalPages" 
      @click="changePage(currentPage + 1)"
      title="Trang tiếp"
    >
      Sau ›
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  currentPage: {
    type: Number,
    default: 1
  },
  totalItems: {
    type: Number,
    required: true
  },
  pageSize: {
    type: Number,
    default: 6
  }
});

const emit = defineEmits(['update:currentPage', 'page-change']);

const totalPages = computed(() => {
  return Math.ceil(props.totalItems / props.pageSize) || 1;
});

const visiblePages = computed(() => {
  const total = totalPages.value;
  const current = props.currentPage;

  if (total <= 7) {
    return Array.from({ length: total }, (_, i) => i + 1);
  }

  const pages = [];
  pages.push(1);

  if (current > 3) {
    pages.push('...');
  }

  const start = Math.max(2, current - 1);
  const end = Math.min(total - 1, current + 1);

  for (let i = start; i <= end; i++) {
    pages.push(i);
  }

  if (current < total - 2) {
    pages.push('...');
  }

  pages.push(total);
  return pages;
});

const changePage = (newPage) => {
  if (newPage >= 1 && newPage <= totalPages.value && newPage !== props.currentPage) {
    emit('update:currentPage', newPage);
    emit('page-change', newPage);
  }
};
</script>

<style scoped>
.pagination-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 40px;
  margin-bottom: 20px;
  user-select: none;
}

.pagination-btn {
  padding: 8px 16px;
  border-radius: 8px;
  border: 1px solid var(--border-color, #cbd5e1);
  background: #ffffff;
  color: #0f172a;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.pagination-btn:hover:not(:disabled) {
  border-color: var(--primary, #022b9f);
  color: var(--primary, #022b9f);
  background: rgba(2, 43, 159, 0.05);
}

.pagination-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.page-numbers {
  display: flex;
  align-items: center;
  gap: 6px;
}

.page-num-btn {
  min-width: 36px;
  height: 36px;
  padding: 0 6px;
  border-radius: 8px;
  border: 1px solid var(--border-color, #cbd5e1);
  background: #ffffff;
  color: #0f172a;
  font-size: 14px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.page-num-btn:hover:not(:disabled):not(.active) {
  border-color: var(--primary, #022b9f);
  color: var(--primary, #022b9f);
  background: rgba(2, 43, 159, 0.05);
}

.page-num-btn.active {
  background: var(--primary, #022b9f);
  color: #ffffff;
  border-color: var(--primary, #022b9f);
  box-shadow: 0 4px 10px rgba(2, 43, 159, 0.25);
}

.page-num-btn.ellipsis {
  border: none;
  background: transparent;
  cursor: default;
  color: #64748b;
}
</style>
