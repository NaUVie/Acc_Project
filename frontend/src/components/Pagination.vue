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

<style scoped src="@/styles/components/Pagination.css"></style>
