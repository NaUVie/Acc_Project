<template>
  <div class="course-category-view container">
    <!-- Mega Style Layout Container -->
    <div class="mega-style-layout glass-card">
      <!-- Left Sidebar: Dynamic Categories Navigation -->
      <aside class="mega-menu-sidebar" aria-label="Danh mục khóa học">
        <button 
          v-for="cat in availableCategories" 
          :key="cat.id"
          type="button"
          class="mega-sidebar-item"
          :class="{ active: selectedCategory === cat.id }"
          @click="scrollToCategory(cat.id)"
        >
          <span class="indicator-bar"></span>
          <span class="sidebar-item-label">{{ cat.name }}</span>
          <span class="cat-count-badge">{{ cat.count }}</span>
        </button>
      </aside>

      <!-- Right Content: Dynamic Category Sections with Course Cards -->
      <main class="mega-menu-content">
        <!-- Loading State -->
        <div v-if="courseStore.loading && courseStore.courses.length === 0" class="category-loading-state">
          <div class="loading-spinner"></div>
          <p>Đang tải danh sách khóa học...</p>
        </div>

        <!-- Render All Dynamic Category Sections -->
        <template v-else-if="dynamicCategories.length > 0">
          <section 
            v-for="cat in dynamicCategories" 
            :key="cat.slug" 
            :id="'category-' + cat.slug"
            class="category-group-section"
          >
            <div class="category-section-header">
              <div class="category-header-info">
                <span class="cat-badge-small">CHƯƠNG TRÌNH ĐÀO TẠO</span>
                <h3 class="category-section-title">{{ cat.name }}</h3>
              </div>
              <span class="category-count-pill">{{ cat.courses.length }} khóa học</span>
            </div>

            <!-- Course Cards Grid -->
            <div v-if="cat.courses.length > 0" class="mega-programs-grid">
              <div 
                v-for="course in cat.courses" 
                :key="course.id"
                class="mega-program-card"
              >
                <router-link :to="'/course/' + (course.handle || course.id)" class="mega-card-link">
                  <div class="mega-school-logo">
                    <img 
                      :src="formatImageUrl(course.image, 'w800') || '/images/Square-Cover-_1.webp'" 
                      :alt="course.title" 
                      loading="lazy" 
                      decoding="async" 
                      @error="handleImageError" 
                    />
                    <span class="card-status-pill" :class="'card-status-' + (course.status || 'ongoing')">
                      {{ course.status === 'upcoming' ? '⏳ Sắp diễn ra' : (course.status === 'completed' ? '🏁 Đã diễn ra' : '🟢 Đang diễn ra') }}
                    </span>
                  </div>
                  <div class="mega-card-info">
                    <span class="mega-school-name">{{ course.level || 'Khóa học' }}</span>
                    <h4 class="mega-program-title" :title="course.title">{{ course.title }}</h4>
                    <p class="mega-program-desc">{{ stripHtml(course.description) }}</p>
                    <div class="mega-card-footer">
                      <div class="arrow-container" aria-label="Xem chi tiết">
                        <svg class="block-arrow-glow" width="46" height="20" viewBox="0 0 52 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <defs>
                            <linearGradient id="catArrowBlue" x1="0%" y1="0%" x2="100%" y2="0%">
                              <stop offset="0%" stop-color="#022B9F"/>
                              <stop offset="100%" stop-color="#2563eb"/>
                            </linearGradient>
                          </defs>
                          <path d="M 2 7 L 34 7 L 34 2 L 50 12 L 34 22 L 34 17 L 2 17 Z" 
                                fill="url(#catArrowBlue)" />
                        </svg>
                      </div>
                    </div>
                  </div>
                </router-link>
              </div>
            </div>

            <!-- Empty category state if no courses exist yet in this category -->
            <div v-else class="empty-category-notice">
              <p>Chưa có khóa học nào trong danh mục này.</p>
            </div>
          </section>
        </template>

        <!-- Empty State when no courses or categories exist at all -->
        <div v-else class="empty-state">
          <p>{{ $t('course.emptyCategory') || 'Chưa có khóa học nào.' }}</p>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue';
import { useRoute } from 'vue-router';
import { useCourseStore } from '@/stores/courses';
import { stripHtml } from '@/utils/stripHtml';
import { formatImageUrl } from '@/utils/imageHelper';

const route = useRoute();
const courseStore = useCourseStore();

const selectedCategory = ref('all');
let isProgrammaticScroll = false;

// Dynamic categories with courses grouped directly from store (API / DB)
const dynamicCategories = computed(() => {
  const cats = (courseStore.categories || []).filter(c => c.slug !== 'bundles');
  const handledIds = new Set();

  const list = cats.map(c => {
    const courses = courseStore.getCoursesByCategory(c.slug) || [];
    courses.forEach(crs => handledIds.add(crs.id));
    return {
      slug: c.slug,
      name: c.name,
      courses
    };
  });

  // Any remaining courses without a matched category
  const remaining = (courseStore.courses || []).filter(c => !handledIds.has(c.id));
  if (remaining.length > 0) {
    list.push({
      slug: 'other',
      name: 'Khóa học khác',
      courses: remaining
    });
  }

  return list;
});

// Dynamic Sidebar Categories Navigation
const availableCategories = computed(() => {
  const list = [
    {
      id: 'all',
      name: 'Tất cả khóa học',
      count: courseStore.courses.length
    }
  ];

  dynamicCategories.value.forEach(cat => {
    list.push({
      id: cat.slug,
      name: cat.name,
      count: cat.courses.length
    });
  });

  return list;
});

const scrollToCategory = (id, smooth = true) => {
  selectedCategory.value = id;
  isProgrammaticScroll = true;

  if (id === 'all') {
    const layoutEl = document.querySelector('.mega-style-layout');
    if (layoutEl) {
      const headerOffset = 90;
      const targetY = layoutEl.getBoundingClientRect().top + window.pageYOffset - headerOffset;
      window.scrollTo({ top: Math.max(0, targetY), behavior: smooth ? 'smooth' : 'auto' });
    } else {
      window.scrollTo({ top: 0, behavior: smooth ? 'smooth' : 'auto' });
    }
    if (window.location.pathname !== '/courses') {
      history.replaceState(null, '', '/courses');
    }
  } else {
    const el = document.getElementById(`category-${id}`);
    if (el) {
      const headerOffset = 90;
      const targetY = el.getBoundingClientRect().top + window.pageYOffset - headerOffset;
      window.scrollTo({ top: Math.max(0, targetY), behavior: smooth ? 'smooth' : 'auto' });
    }
    history.replaceState(null, '', `/courses/category/${id}`);
  }

  setTimeout(() => {
    isProgrammaticScroll = false;
  }, 750);
};

const handleScroll = () => {
  if (isProgrammaticScroll) return;

  const sections = dynamicCategories.value;
  if (!sections.length) return;

  const headerOffset = 130;
  const scrollY = window.pageYOffset;
  const layoutEl = document.querySelector('.mega-style-layout');

  if (layoutEl) {
    const layoutTop = layoutEl.getBoundingClientRect().top + window.pageYOffset - headerOffset;
    if (scrollY < layoutTop + 40) {
      selectedCategory.value = 'all';
      return;
    }
  }

  let currentActive = 'all';
  for (const cat of sections) {
    const el = document.getElementById(`category-${cat.slug}`);
    if (el) {
      const top = el.getBoundingClientRect().top;
      if (top <= headerOffset + 40) {
        currentActive = cat.slug;
      }
    }
  }

  if (selectedCategory.value !== currentActive) {
    selectedCategory.value = currentActive;
  }
};

onMounted(async () => {
  const promises = [];
  if (courseStore.courses.length === 0) {
    promises.push(courseStore.fetchCourses());
  }
  if (courseStore.categories && courseStore.categories.length === 0) {
    promises.push(courseStore.fetchCategories());
  }
  if (promises.length > 0) {
    await Promise.all(promises).catch(() => {});
  }

  window.addEventListener('scroll', handleScroll, { passive: true });

  const paramSlug = route.params.categorySlug;
  if (paramSlug) {
    await nextTick();
    setTimeout(() => {
      scrollToCategory(paramSlug, true);
    }, 200);
  }
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
});

watch(() => route.params.categorySlug, (newSlug) => {
  if (newSlug) {
    scrollToCategory(newSlug, true);
  } else {
    scrollToCategory('all', true);
  }
});

const handleImageError = (e) => {
  e.target.src = '/images/Square-Cover-_1.webp';
};
</script>

<style scoped src="@/styles/views/courses/CourseCategoryView.css"></style>
