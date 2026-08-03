<template>
  <div class="blog-page">
    <header class="blog-banner bg-secondary">
      <div class="container">
        <div class="blog-banner-content v-stack gap-10 text-center justify-items-center">
          <div class="v-stack gap-5 sm:gap-8">
            <h1 class="h0">Bài viết mới nhất</h1>
          </div>
        </div>
        
        <!-- Category Filter Tab List -->
        <div class="scroll-area bleed sm:unbleed justify-items-center">
          <div class="nav-categories">
            <ul class="h-stack bold text-base" role="tablist">
              <li 
                v-for="cat in categories" 
                :key="cat"
                role="tab" 
                :aria-selected="selectedCategory === cat ? 'true' : 'false'"
              >
                <a 
                  href="#" 
                  :class="{ selected: selectedCategory === cat }"
                  @click.prevent="selectedCategory = cat"
                >
                  {{ cat }}
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </header>

    <div class="blog-posts__container container">
      <!-- Search Box for premium interaction -->
      <div class="search-filter-wrapper">
        <div class="search-input-container">
          <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="Tìm kiếm bài viết..." 
            class="search-input"
          />
        </div>
      </div>

      <!-- Blog Grid -->
      <div class="blog-posts" v-if="filteredPosts.length > 0">
        <article 
          v-for="post in filteredPosts" 
          :key="post.id" 
          class="blog-post-card snap-center group"
        >
          <a :href="post.link" class="blog-post-card__figure rounded">
            <span class="badge badge--primary">{{ post.category }}</span>
            <img 
              :src="post.image" 
              :alt="post.title"
              class="w-full h-full object-cover zoom-image"
              loading="lazy"
            />
          </a>
          <div class="blog-post-card__info">
            <div class="v-stack gap-4 sm:gap-5">
              <div class="v-stack gap-3 sm:gap-4">
                <p class="h3">
                  <a :href="post.link">{{ post.title }}</a>
                </p>
                <p>{{ post.excerpt }}</p>
              </div>
              <div class="blog-post-card__meta">
                <div class="text-with-icon link-faded">
                  <svg role="presentation" fill="none" focusable="false" stroke-width="1.5" width="16" height="16" class="icon icon-blog-date" viewBox="0 0 16 16">
                    <path d="M5.372 1v2.877M10.455 1v2.877" stroke="currentColor" stroke-linecap="round"></path>
                    <path d="M14.338 7.632H1.497l.179-4.57 6.164-.448 6.497.448v4.57Z" fill="currentColor" fill-opacity=".12"></path>
                    <path d="M1.224 12.073c.183 1.631 1.508 2.925 3.147 3.004a73.18 73.18 0 0 0 3.546.083c1.256 0 2.413-.028 3.546-.083 1.639-.079 2.964-1.374 3.146-3.004.124-1.099.225-2.224.225-3.37 0-1.147-.102-2.273-.225-3.371-.182-1.631-1.507-2.925-3.146-3.004a73.22 73.22 0 0 0-3.546-.083 73.22 73.22 0 0 0-3.546.083c-1.639.079-2.964 1.374-3.147 3.004C1.101 6.43 1 7.556 1 8.703c0 1.146.102 2.272.224 3.37ZM1.331 7.202h13.24" stroke="currentColor"></path>
                  </svg>
                  <span class="text-sm">{{ post.date }}</span>
                </div>
              </div>
            </div>
          </div>
        </article>
      </div>

      <!-- Empty State -->
      <div v-else class="empty-results">
        <p>Không tìm thấy bài viết phù hợp.</p>
        <button @click="resetFilters" class="reset-btn">Xem tất cả bài viết</button>
      </div>

      <!-- Pagination -->
      <nav class="pagination" role="navigation" aria-label="Pagination navigation" v-if="filteredPosts.length > 0">
        <span class="pagination__item pagination__item--disabled">
          <span class="animated-arrow animated-arrow--reverse"></span>
        </span>
        <span class="pagination__current">1  /  1</span>
        <span class="pagination__item pagination__item--disabled">
          <span class="animated-arrow"></span>
        </span>
      </nav>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useCourseStore } from '@/stores/courses';

const courseStore = useCourseStore();

const categories = [
  'All posts',
  'AI 2026',
  'AI Automation',
  'Công cụ AI',
  'Làm việc hiệu suất',
  'Lãnh đạo & Quản lý'
];

const selectedCategory = ref('All posts');
const searchQuery = ref('');

const posts = computed(() => courseStore.getBlogPosts);

const filteredPosts = computed(() => {
  return posts.value.filter(post => {
    const matchesCategory = selectedCategory.value === 'All posts' || post.category === selectedCategory.value;
    const matchesSearch = post.title.toLowerCase().includes(searchQuery.value.toLowerCase()) || 
                          post.excerpt.toLowerCase().includes(searchQuery.value.toLowerCase());
    return matchesCategory && matchesSearch;
  });
});

const resetFilters = () => {
  selectedCategory.value = 'All posts';
  searchQuery.value = '';
};
</script>

<style scoped src="@/styles/views/library/Blog.css"></style>
