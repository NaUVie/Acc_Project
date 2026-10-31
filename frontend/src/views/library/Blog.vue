<template>
  <div class="blog-page">
    <div class="container">
      <!-- Hero Section đồng bộ phong cách ACC Academy -->
      <div class="blog-hero">
        <h1 class="hero-title">Tin tức, Kiến thức </h1>
      

        <!-- Search Box -->
        <div class="search-filter-wrapper">
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

      <!-- Category Filter Tabs -->
      <div class="category-tabs">
        <button 
          v-for="cat in availableCategories" 
          :key="cat"
          class="cat-tab-btn"
          :class="{ active: selectedCategory === cat }"
          @click="changeCategory(cat)"
        >
          {{ cat === 'All posts' ? 'Tất cả bài viết' : cat }}
        </button>
      </div>

      <!-- Result Counter (nếu có tìm kiếm hoặc lọc) -->
      <div class="results-header" v-if="filteredPosts.length > 0">
        <span class="results-count">
          Hiển thị <strong>{{ paginatedPosts.length }}</strong> trên tổng số <strong>{{ filteredPosts.length }}</strong> bài viết
        </span>
      </div>

      <!-- Loading Skeleton Cards -->
      <div class="blog-grid" v-if="isLoading && posts.length === 0">
        <article v-for="n in 6" :key="n" class="blog-card skeleton-card">
          <div class="card-image-wrapper skeleton-img-box"></div>
          <div class="card-body">
            <div class="skeleton-shimmer skeleton-date"></div>
            <div class="skeleton-shimmer skeleton-title"></div>
            <div class="skeleton-shimmer skeleton-desc"></div>
            <div class="skeleton-shimmer skeleton-btn"></div>
          </div>
        </article>
      </div>

      <!-- Blog Grid -->
      <div class="blog-grid" v-else-if="filteredPosts.length > 0" ref="blogGridRef">
        <article 
          v-for="post in paginatedPosts" 
          :key="post.id" 
          class="blog-card"
        >
          <router-link :to="post.link || '/blog/' + post.handle" class="card-image-link">
            <div class="card-image-wrapper">
              <img 
                :src="post.image || 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=800&auto=format&fit=crop'" 
                :alt="post.title"
                class="card-image"
                loading="lazy"
                decoding="async"
              />
              <span class="category-badge">{{ post.category }}</span>
            </div>
          </router-link>

          <div class="card-body">
            <div class="card-meta">
              <span class="meta-date">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                  <line x1="16" y1="2" x2="16" y2="6"></line>
                  <line x1="8" y1="2" x2="8" y2="6"></line>
                  <line x1="3" y1="10" x2="21" y2="10"></line>
                </svg>
                {{ post.date || 'Mới cập nhật' }}
              </span>
              <span class="meta-author">ACC Editorial</span>
            </div>

            <h3 class="card-title">
              <router-link :to="post.link || '/blog/' + post.handle" class="title-link">
                {{ post.title }}
              </router-link>
            </h3>

            <p class="card-excerpt">{{ post.excerpt }}</p>

            <div class="card-footer">
              <router-link :to="post.link || '/blog/' + post.handle" class="btn-read-more">
                <span>Đọc bài viết</span>
                <span class="arrow">&rarr;</span>
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
        <p class="empty-desc">Thử tìm kiếm với từ khóa khác hoặc chuyển danh mục hiển thị.</p>
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

const courseStore = useCourseStore();
const blogGridRef = ref(null);
const isLoading = ref(courseStore.blogPosts.length === 0);

onMounted(async () => {
  courseStore.fetchBlogCategories().catch(() => {});
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

const selectedCategory = ref('All posts');
const searchQuery = ref('');
const currentPage = ref(1);
const pageSize = ref(6); // 6 bài viết mỗi trang (chia đều lưới 2 hoặc 3 cột)

const posts = computed(() => courseStore.getBlogPosts || []);

// Tự động nạp động các danh mục từ DB & danh sách bài viết thực tế
const availableCategories = computed(() => {
  const cats = ['All posts'];
  if (courseStore.blogCategories && courseStore.blogCategories.length > 0) {
    courseStore.blogCategories.forEach(c => {
      if (c.name && !cats.includes(c.name)) cats.push(c.name);
    });
  }
  posts.value.forEach(p => {
    if (p.category && !cats.includes(p.category)) {
      cats.push(p.category);
    }
  });
  return cats;
});

const filteredPosts = computed(() => {
  return posts.value.filter(post => {
    const matchesCategory = selectedCategory.value === 'All posts' || post.category === selectedCategory.value;
    const q = searchQuery.value.toLowerCase().trim();
    const matchesSearch = !q || 
      (post.title && post.title.toLowerCase().includes(q)) || 
      (post.excerpt && post.excerpt.toLowerCase().includes(q)) ||
      (post.category && post.category.toLowerCase().includes(q));
    return matchesCategory && matchesSearch;
  });
});

// Danh sách bài viết được cắt theo trang hiện tại
const paginatedPosts = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  const end = start + pageSize.value;
  return filteredPosts.value.slice(start, end);
});

// Reset về trang 1 khi người dùng đổi từ khóa hoặc đổi danh mục
watch([searchQuery, selectedCategory], () => {
  currentPage.value = 1;
});

const changeCategory = (cat) => {
  selectedCategory.value = cat;
  currentPage.value = 1;
};

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
  selectedCategory.value = 'All posts';
  searchQuery.value = '';
  currentPage.value = 1;
};
</script>

<style scoped src="@/styles/views/library/Blog.css"></style>
