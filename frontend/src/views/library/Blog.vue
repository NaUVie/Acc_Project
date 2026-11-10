<template>
  <div class="blog-page">
    <!-- Hero Section đồng bộ phong cách ACC Academy với nền xanh navy gradient nhạt dần -->
    <section class="blog-hero-section">
      <div class="hero-backdrop-glow"></div>
      <div class="container hero-inner">
        <h1 class="hero-title animate-fade-in">Tin tức, Kiến thức</h1>

        <!-- Search Box -->
        <div class="search-filter-wrapper animate-fade-in">
          <div class="search-input-container">
            <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8"></circle>
              <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
            <input 
              type="text" 
              v-model="searchQuery" 
              placeholder="Tìm kiếm bài viết theo từ khóa, chủ đề..." 
              class="search-input"
            />
            <button v-if="searchQuery" class="clear-search-btn" @click="searchQuery = ''" title="Xóa tìm kiếm">
              &times;
            </button>
          </div>
        </div>
      </div>
    </section>

    <div class="container blog-content-container">
      <!-- Result Counter (nếu có tìm kiếm) -->
      <div class="results-header" v-if="searchQuery && filteredPosts.length > 0">
        <span class="results-count">
          Hiển thị <strong>{{ paginatedPosts.length }}</strong> trên tổng số <strong>{{ filteredPosts.length }}</strong> bài viết tìm thấy
        </span>
      </div>

      <!-- Loading Skeleton Strips -->
      <div class="blog-list-wrapper" v-if="isLoading && posts.length === 0">
        <article v-for="n in 5" :key="n" class="blog-strip-item skeleton-strip">
          <div class="strip-image-link skeleton-img-box"></div>
          <div class="strip-content">
            <div class="skeleton-shimmer skeleton-date"></div>
            <div class="skeleton-shimmer skeleton-title"></div>
            <div class="skeleton-shimmer skeleton-desc"></div>
            <div class="skeleton-shimmer skeleton-btn"></div>
          </div>
        </article>
      </div>

      <!-- Blog List (Kiểu ngang từng thanh) -->
      <div class="blog-list-wrapper" v-else-if="filteredPosts.length > 0" ref="blogGridRef">
        <article 
          v-for="post in paginatedPosts" 
          :key="post.id" 
          class="blog-strip-item"
        >
          <router-link :to="post.link || '/blog/' + post.handle" class="strip-image-link">
            <div class="strip-image-wrapper">
              <img 
                :src="formatImageUrl(post.image, 'w800') || 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=800&auto=format&fit=crop'" 
                :alt="post.title"
                class="strip-image"
                loading="lazy"
                decoding="async"
              />
              <span class="category-badge" v-if="post.category">{{ post.category }}</span>
            </div>
          </router-link>

          <div class="strip-content">
            <div class="strip-meta">
              <span class="meta-date">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                  <line x1="16" y1="2" x2="16" y2="6"></line>
                  <line x1="8" y1="2" x2="8" y2="6"></line>
                  <line x1="3" y1="10" x2="21" y2="10"></line>
                </svg>
                {{ formatDate(post.date || post.created_at || post.createdAt) }}
              </span>
              <span class="meta-dot">•</span>
              <span class="meta-author">ACC Editorial</span>
              <span v-if="getLinkedCourseTitle(post.course_id)" class="linked-course-pill">
                {{ getLinkedCourseTitle(post.course_id) }}
              </span>
            </div>

            <h2 class="strip-title">
              <router-link :to="post.link || '/blog/' + post.handle">
                {{ post.title }}
              </router-link>
            </h2>

            <p class="strip-desc" v-if="post.excerpt || post.description">
              {{ post.excerpt || post.description }}
            </p>

            <div class="strip-footer">
              <router-link :to="post.link || '/blog/' + post.handle" class="arrow-container" aria-label="Đọc bài viết">
                <svg class="block-arrow-glow" width="46" height="20" viewBox="0 0 52 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M 2 7 L 34 7 L 34 2 L 50 12 L 34 22 L 34 17 L 2 17 Z" fill="#022B9F" />
                </svg>
              </router-link>
            </div>
          </div>
        </article>
      </div>

      <!-- Pagination Component -->
      <Pagination 
        v-if="filteredPosts.length > pageSize"
        v-model:currentPage="currentPage"
        :totalItems="filteredPosts.length"
        :pageSize="pageSize"
        @page-change="onPageChange"
      />

      <!-- Empty State -->
      <div v-else-if="!isLoading && filteredPosts.length === 0" class="empty-state">
        <h3 class="empty-title">Không tìm thấy bài viết phù hợp</h3>
        <p class="empty-desc">Thử tìm kiếm với từ khóa khác.</p>
        <button @click="resetFilters" class="btn-reset">
          Xem tất cả bài viết
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, nextTick } from 'vue';
import { useCourseStore } from '@/stores/courses';
import Pagination from '@/components/Pagination.vue';
import { formatImageUrl } from '@/utils/imageHelper';

const courseStore = useCourseStore();
const blogGridRef = ref(null);
const isLoading = ref(courseStore.blogPosts.length === 0);

onMounted(async () => {
  if (!courseStore.blogPosts || courseStore.blogPosts.length === 0) {
    isLoading.value = true;
    try {
      await courseStore.fetchBlogs();
    } finally {
      isLoading.value = false;
    }
  } else {
    isLoading.value = false;
    courseStore.fetchBlogs().catch(() => {});
  }
});

const searchQuery = ref('');
const currentPage = ref(1);
const pageSize = ref(8); // 8 bài viết mỗi trang dạng danh sách ngang

const formatDate = (dateStr) => {
  if (!dateStr) return 'Mới cập nhật';
  try {
    const d = new Date(dateStr);
    if (isNaN(d.getTime())) return dateStr;
    return d.toLocaleDateString('vi-VN', { day: '2-digit', month: '2-digit', year: 'numeric' });
  } catch (e) {
    return dateStr;
  }
};

const getLinkedCourseTitle = (courseId) => {
  if (!courseId) return null;
  const c = courseStore.courses.find(item => item.id === courseId);
  return c ? c.title : null;
};

const posts = computed(() => courseStore.getBlogPosts || []);

const filteredPosts = computed(() => {
  const q = searchQuery.value.toLowerCase().trim();
  if (!q) return posts.value;
  return posts.value.filter(post => {
    return (post.title && post.title.toLowerCase().includes(q)) || 
      (post.excerpt && post.excerpt.toLowerCase().includes(q)) ||
      (post.category && post.category.toLowerCase().includes(q));
  });
});

// Danh sách bài viết được cắt theo trang hiện tại
const paginatedPosts = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  const end = start + pageSize.value;
  return filteredPosts.value.slice(start, end);
});

// Reset về trang 1 khi người dùng đổi từ khóa
watch(searchQuery, () => {
  currentPage.value = 1;
});

const onPageChange = () => {
  nextTick(() => {
    if (blogGridRef.value) {
      const topOffset = blogGridRef.value.getBoundingClientRect().top + window.scrollY - 100;
      window.scrollTo({
        top: topOffset,
        behavior: 'smooth'
      });
    }
  });
};

const resetFilters = () => {
  searchQuery.value = '';
  currentPage.value = 1;
};
</script>

<style scoped src="@/styles/views/library/Blog.css"></style>