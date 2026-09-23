<template>
  <Teleport to="body">
    <div class="search-slideover-container" :class="{ 'active': isOpen }">
      <!-- Backdrop overlay -->
      <Transition name="fade" appear>
        <div v-if="isOpen" class="search-backdrop" @click="closeSearch"></div>
      </Transition>

      <!-- Slide-over panel -->
      <Transition name="slide" appear>
        <div v-if="isOpen" class="search-panel">
          <!-- 1. Header & Search Input -->
          <div class="search-header">
            <div class="search-title-row">
              <h2>Tìm kiếm khóa học</h2>
              <button class="close-btn" @click="closeSearch" aria-label="Đóng tìm kiếm">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="18" y1="6" x2="6" y2="18"></line>
                  <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
              </button>
            </div>

            <!-- Search input bar -->
            <div class="search-input-wrapper">
              <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="11" cy="11" r="8"/>
                <path d="M21 21l-4.35-4.35"/>
              </svg>
              <input 
                ref="searchInputRef"
                type="text" 
                v-model="searchQuery" 
                placeholder="Nhập tên khóa học, từ khóa..." 
                class="search-input"
                @keyup.esc="closeSearch"
              />
              <button v-if="searchQuery" class="clear-btn" @click="searchQuery = ''">
                &times;
              </button>
            </div>

            <!-- Quick Category Tags -->
            <div class="quick-tags">
              <button 
                class="tag-btn" 
                :class="{ active: selectedCategory === 'all' }"
                @click="selectedCategory = 'all'"
              >
                Tất cả
              </button>
              <button 
                v-for="cat in categories" 
                :key="cat.id" 
                class="tag-btn"
                :class="{ active: selectedCategory === cat.id }"
                @click="selectedCategory = cat.id"
              >
                {{ cat.name }}
              </button>
            </div>
          </div>

          <!-- 2. Search Results Body -->
          <div class="search-body">
            <!-- Popular Suggestions if query is empty -->
            <div v-if="!searchQuery.trim()" class="search-suggestions">
              <h4 class="suggestion-title">💡 Từ khóa gợi ý</h4>
              <div class="suggestion-pills">
                <button 
                  v-for="term in popularTerms" 
                  :key="term" 
                  class="pill-item"
                  @click="searchQuery = term"
                >
                  {{ term }}
                </button>
              </div>

              <!-- Top 3 Featured courses when idle -->
              <div class="featured-section">
                <h4 class="suggestion-title">🔥 Khóa học nổi bật</h4>
                <div class="results-list">
                  <div 
                    v-for="course in featuredCourses" 
                    :key="course.id" 
                    class="course-result-card"
                    @click="selectCourse(course)"
                  >
                    <img :src="course.image || '/images/default.jpg'" :alt="course.title" class="course-thumb" />
                    <div class="course-info">
                      <span class="course-category">{{ translateCategory(course.category) }}</span>
                      <h4 class="course-title">{{ course.title }}</h4>
                      <div class="course-price">
                        <span class="price-current">{{ formatCurrency(course.price) }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Search Results List (when query is typed) -->
            <div v-else-if="searchResults.length > 0" class="results-list">
              <div class="results-count">
                Tìm thấy <strong>{{ totalMatchCount }}</strong> kết quả phù hợp
              </div>

              <div 
                v-for="course in searchResults" 
                :key="course.id" 
                class="course-result-card"
                @click="selectCourse(course)"
              >
                <img :src="course.image || '/images/default.jpg'" :alt="course.title" class="course-thumb" />
                <div class="course-info">
                  <span class="course-category">{{ translateCategory(course.category) }}</span>
                  <h4 class="course-title">{{ course.title }}</h4>
                  <div class="course-price">
                    <span class="price-current">{{ formatCurrency(course.price) }}</span>
                    <span v-if="course.originalPrice && course.originalPrice > course.price" class="price-original">
                      {{ formatCurrency(course.originalPrice) }}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- No results state -->
            <div v-else class="no-results">
              <div class="empty-icon">🔍</div>
              <p>Không tìm thấy khóa học nào phù hợp với <strong>"{{ searchQuery }}"</strong></p>
              <span class="empty-hint">Thử tìm kiếm với từ khóa khác như "AI", "Doanh nghiệp", "Kỹ năng"...</span>
            </div>
          </div>
        </div>
      </Transition>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import { useCourseStore } from '@/stores/courses';
import { slugify } from '@/utils/slugify';

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['close']);
const router = useRouter();
const courseStore = useCourseStore();

const searchQuery = ref('');
const selectedCategory = ref('all');
const searchInputRef = ref(null);

const popularTerms = [
  'Đào tạo doanh nghiệp',
  'Đào tạo cá nhân',
  'Chính phủ số',
  'AI In-House'
];

const categories = [
  { id: 'dao-tao-doanh-nghiep', name: 'Đào tạo cho doanh nghiệp' },
  { id: 'dao-tao-ca-nhan', name: 'Đào tạo cho cá nhân' },
  { id: 'dao-tao-co-quan-nha-nuoc', name: 'Đào tạo cho khối cơ quan - nhà nước' }
];

watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    searchQuery.value = '';
    selectedCategory.value = 'all';
    nextTick(() => {
      if (searchInputRef.value) {
        searchInputRef.value.focus();
      }
    });
  }
});

// Featured courses displayed when input is empty (max 3 items)
const featuredCourses = computed(() => {
  return (courseStore.courses || []).slice(0, 3);
});

const filteredMatchingCourses = computed(() => {
  let list = courseStore.courses || [];
  
  if (selectedCategory.value !== 'all') {
    list = list.filter(c => c.category === selectedCategory.value);
  }

  const query = searchQuery.value.trim().toLowerCase();
  if (!query) return [];

  return list.filter(c => {
    const titleMatch = (c.title || '').toLowerCase().includes(query);
    const descMatch = (c.description || '').toLowerCase().includes(query);
    const catMatch = (c.category || '').toLowerCase().includes(query);
    return titleMatch || descMatch || catMatch;
  });
});

const totalMatchCount = computed(() => filteredMatchingCourses.value.length);

// Limit displayed search results to top 6 items to keep drawer super lightweight & fast
const searchResults = computed(() => {
  return filteredMatchingCourses.value.slice(0, 6);
});

const translateCategory = (cat) => {
  switch (cat) {
    case 'dao-tao-doanh-nghiep':
    case 'ky-nang-ai':
      return 'Đào tạo cho doanh nghiệp';
    case 'dao-tao-ca-nhan':
    case 'ky-nang-mem':
    case 'ky-nang-chuyen-mon':
      return 'Đào tạo cho cá nhân';
    case 'dao-tao-co-quan-nha-nuoc':
      return 'Đào tạo cho khối cơ quan - nhà nước';
    default:
      return cat || 'Khóa học';
  }
};

const formatCurrency = (val) => {
  return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(val || 0);
};

const closeSearch = () => {
  emit('close');
};

const selectCourse = (course) => {
  closeSearch();
  const handle = course.handle || course.slug || slugify(course.title || '');
  router.push(`/course/${handle}`);
};
</script>

<style scoped src="@/styles/components/SlideOverSearch.css"></style>
