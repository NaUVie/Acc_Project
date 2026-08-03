<template>
  <div class="course-category-view">
    <!-- 1. Custom Course Announcement Banner -->
    <div class="custom-course-announcement">
      <img src="/images/collection-thumb-2.webp" alt="Tối Ưu Năng Suất & Quản Trị Vận Hành" class="cca-bg-image" />
      <div class="cca-overlay"></div>
      <div class="cca-container">
        <div class="cca-text-wrap">
          <h1 class="cca-heading animate-fade-in">Tối Ưu Năng Suất & Quản Trị Vận Hành</h1>
          <p class="cca-subheading animate-fade-in">Nâng cấp kỹ năng cá nhân và dẫn dắt doanh nghiệp ứng dụng AI hiệu quả với bộ đôi khóa học mới nhất.</p>
        </div>
        <div class="cca-card-container">
          <router-link 
            v-for="course in promoCourses" 
            :key="course.id" 
            :to="`/contact?course=${course.handle}`" 
            class="cca-card"
          >
            <span class="cca-badge">Khóa học mới</span>
            <img :src="course.image" :alt="course.title" class="cca-card-image" />
            <div class="cca-card-content">
              <h3 class="cca-card-title">{{ course.title }}</h3>
              <div class="cca-card-prices">
                <span class="cca-card-price">{{ formatPrice(course.price) }}</span>
                <span v-if="course.originalPrice" class="cca-card-compare">{{ formatPrice(course.originalPrice) }}</span>
              </div>
            </div>
          </router-link>
        </div>
      </div>
    </div>

    <!-- 2. Collection List Section -->
    <div class="collection-list-section">
      <div class="container">
        <h2 class="section-title">Học theo chủ đề</h2>
        <div class="collection-list-grid-wrapper">
          <div class="collection-list-grid">
            <router-link 
              v-for="cat in categories" 
              :key="cat.name" 
              :to="cat.link" 
              class="collection-card"
              :class="{ 'active': cat.isActive }"
            >
              <div class="collection-card__image-wrapper">
                <img :src="cat.image" :alt="cat.name" class="collection-card__image" />
                <div class="collection-card__overlay"></div>
              </div>
              <span class="collection-card__title">{{ cat.name }}</span>
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- 3. Main Catalog Section -->
    <div class="main-catalog-section container">
      <div class="collection-layout">
        
        <!-- Desktop Sidebar Filters -->
        <aside class="collection__sidebar-filters">
          <div class="filters-widget">
            <div class="widget-header">
              <h3 class="widget-title">Bộ lọc</h3>
              <button @click="resetFilters" class="clear-filters-link" v-if="hasActiveFilters">
                Xóa tất cả
              </button>
            </div>
            
            <!-- Level Filter -->
            <div class="filter-group">
              <h4 class="filter-group-title">Cấp độ</h4>
              <div class="filter-options">
                <label v-for="level in levels" :key="level" class="filter-checkbox-label">
                  <input type="checkbox" :value="level" v-model="selectedLevels" />
                  <span class="checkbox-text">{{ level }}</span>
                </label>
              </div>
            </div>

            <!-- Product Type Filter -->
            <div class="filter-group">
              <h4 class="filter-group-title">Loại sản phẩm</h4>
              <div class="filter-options">
                <label v-for="type in types" :key="type" class="filter-checkbox-label">
                  <input type="checkbox" :value="type" v-model="selectedTypes" />
                  <span class="checkbox-text">{{ type }}</span>
                </label>
              </div>
            </div>

            <!-- Price Filter -->
            <div class="filter-group">
              <h4 class="filter-group-title">Học phí</h4>
              <div class="price-range-inputs">
                <div class="price-input-wrapper">
                  <input type="number" placeholder="Từ" v-model.number="minPrice" />
                  <span class="currency-label">₫</span>
                </div>
                <span class="price-separator">-</span>
                <div class="price-input-wrapper">
                  <input type="number" placeholder="Đến" v-model.number="maxPrice" />
                  <span class="currency-label">₫</span>
                </div>
              </div>
            </div>
          </div>
        </aside>

        <!-- Right Side Results Area -->
        <div class="collection__results">
          
          <!-- Top Toolbar -->
          <div class="collection-toolbar">
            <div class="toolbar-left">
              <button @click="isMobileFiltersOpen = true" class="mobile-filter-trigger">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="4" y1="21" x2="4" y2="14" />
                  <line x1="4" y1="10" x2="4" y2="3" />
                  <line x1="12" y1="21" x2="12" y2="12" />
                  <line x1="12" y1="8" x2="12" y2="3" />
                  <line x1="20" y1="21" x2="20" y2="16" />
                  <line x1="20" y1="12" x2="20" y2="3" />
                  <line x1="1" y1="14" x2="7" y2="14" />
                  <line x1="9" y1="8" x2="15" y2="8" />
                  <line x1="17" y1="16" x2="23" y2="16" />
                </svg>
                <span>Bộ lọc</span>
                <span v-if="activeFilterCount > 0" class="mobile-filter-badge">
                  {{ activeFilterCount }}
                </span>
              </button>
              <span class="results-count">{{ filteredCourses.length }} khóa học</span>
            </div>
            <div class="toolbar-right">
              <div class="sort-selector">
                <span class="sort-label">Sắp xếp theo:</span>
                <select v-model="sortBy" class="sort-select">
                  <option value="best-selling">Mua nhiều nhất</option>
                  <option value="created-descending">Mới nhất</option>
                  <option value="price-ascending">Giá: Thấp đến Cao</option>
                  <option value="price-descending">Giá: Cao đến Thấp</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Product Grid -->
          <div v-if="filteredCourses.length > 0" class="collection-products-grid">
            <div v-for="course in filteredCourses" :key="course.id" class="product-grid-item">
              <ProductCard :course="course" />
            </div>
          </div>
          
          <!-- Empty State -->
          <div v-else class="empty-state">
            <svg class="empty-icon" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <circle cx="11" cy="11" r="8" />
              <line x1="21" y1="21" x2="16.65" y2="16.65" />
            </svg>
            <h3>Không tìm thấy khóa học nào</h3>
            <p>Vui lòng điều chỉnh lại bộ lọc của bạn để tìm kiếm khóa học phù hợp.</p>
            <button @click="resetFilters" class="clear-filters-btn">Xóa bộ lọc</button>
          </div>
        </div>

      </div>
    </div>

    <!-- 4. Mobile Filter Drawer -->
    <div class="mobile-filters-drawer" :class="{ 'open': isMobileFiltersOpen }">
      <div class="drawer-backdrop" @click="isMobileFiltersOpen = false"></div>
      <div class="drawer-content">
        <div class="drawer-header">
          <h3>Bộ lọc</h3>
          <button @click="isMobileFiltersOpen = false" class="close-drawer-btn" aria-label="Đóng">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
          </button>
        </div>
        
        <div class="drawer-body">
          <!-- Level Filter -->
          <div class="filter-group">
            <h4 class="filter-group-title">Cấp độ</h4>
            <div class="filter-options">
              <label v-for="level in levels" :key="level" class="filter-checkbox-label">
                <input type="checkbox" :value="level" v-model="selectedLevels" />
                <span class="checkbox-text">{{ level }}</span>
              </label>
            </div>
          </div>

          <!-- Product Type Filter -->
          <div class="filter-group">
            <h4 class="filter-group-title">Loại sản phẩm</h4>
            <div class="filter-options">
              <label v-for="type in types" :key="type" class="filter-checkbox-label">
                <input type="checkbox" :value="type" v-model="selectedTypes" />
                <span class="checkbox-text">{{ type }}</span>
              </label>
            </div>
          </div>

          <!-- Price Filter -->
          <div class="filter-group">
            <h4 class="filter-group-title">Học phí</h4>
            <div class="price-range-inputs">
              <div class="price-input-wrapper">
                <input type="number" placeholder="Từ" v-model.number="minPrice" />
                <span class="currency-label">₫</span>
              </div>
              <span class="price-separator">-</span>
              <div class="price-input-wrapper">
                <input type="number" placeholder="Đến" v-model.number="maxPrice" />
                <span class="currency-label">₫</span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="drawer-footer">
          <button @click="resetFilters" class="btn btn-secondary" :disabled="!hasActiveFilters">Xóa tất cả</button>
          <button @click="isMobileFiltersOpen = false" class="btn btn-primary">Xem kết quả</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useCourseStore } from '@/stores/courses';
import ProductCard from '@/components/ProductCard.vue';

const courseStore = useCourseStore();

// Promo courses shown in announcement banner
const promoCourses = computed(() => {
  return [
    courseStore.getCourseByHandle('chatgpt-work-automation'),
    courseStore.getCourseByHandle('ai-center-of-excellence')
  ].filter(Boolean);
});

// Categories list
const categories = [
  { name: 'Tạo bộ khóa học', link: '/bundles', image: '/images/16_ee7b342a-17d9-4648-9808-e23a54db946b.png', isActive: false },
  { name: 'Kỹ năng AI', link: '/courses/ai', image: '/images/12.png', isActive: false },
  { name: 'Combo khóa học', link: '/bundles', image: '/images/15_8e9187c9-89f2-46e6-ac3f-ff8f4fc77625.png', isActive: false },
  { name: 'Kỹ năng chuyên môn', link: '/courses/chuyen-mon', image: '/images/14_ec52e092-8d4b-44b4-b80b-43c971eaa575.png', isActive: true },
  { name: 'Kỹ năng mềm', link: '/courses/mem', image: '/images/13_6a38fcf7-4c61-40a3-85b5-4f796feef710.png', isActive: false }
];

// Filters options
const levels = ['Cơ bản', 'Trung cấp', 'Mọi cấp độ'];
const types = ['Quản lý dữ liệu', 'Xây dựng dashboard'];

// Filters states
const selectedLevels = ref([]);
const selectedTypes = ref([]);
const minPrice = ref(null);
const maxPrice = ref(null);
const sortBy = ref('best-selling');
const isMobileFiltersOpen = ref(false);

const resetFilters = () => {
  selectedLevels.value = [];
  selectedTypes.value = [];
  minPrice.value = null;
  maxPrice.value = null;
};

const hasActiveFilters = computed(() => {
  return (
    selectedLevels.value.length > 0 ||
    selectedTypes.value.length > 0 ||
    minPrice.value !== null ||
    maxPrice.value !== null
  );
});

const activeFilterCount = computed(() => {
  let count = 0;
  if (selectedLevels.value.length > 0) count += selectedLevels.value.length;
  if (selectedTypes.value.length > 0) count += selectedTypes.value.length;
  if (minPrice.value !== null) count += 1;
  if (maxPrice.value !== null) count += 1;
  return count;
});

// Specialist Courses logic
const specialistCourses = computed(() => {
  return courseStore.getCoursesByCategory('ky-nang-chuyen-mon');
});

// Dynamic filtering & sorting
const filteredCourses = computed(() => {
  let list = [...specialistCourses.value];

  // Filter by level
  if (selectedLevels.value.length > 0) {
    list = list.filter(course => selectedLevels.value.includes(course.level));
  }

  // Filter by product type
  if (selectedTypes.value.length > 0) {
    list = list.filter(course => {
      return selectedTypes.value.some(type => {
        if (type === 'Quản lý dữ liệu') {
          return course.handle === 'excel-ai';
        }
        if (type === 'Xây dựng dashboard') {
          return course.handle !== 'excel-ai';
        }
        return true;
      });
    });
  }

  // Filter by price
  if (minPrice.value !== null) {
    list = list.filter(course => course.price >= minPrice.value);
  }
  if (maxPrice.value !== null) {
    list = list.filter(course => course.price <= maxPrice.value);
  }

  // Sorting
  if (sortBy.value === 'price-ascending') {
    list.sort((a, b) => a.price - b.price);
  } else if (sortBy.value === 'price-descending') {
    list.sort((a, b) => b.price - a.price);
  } else if (sortBy.value === 'created-descending') {
    list.sort((a, b) => b.id - a.id);
  } else {
    // default/best-selling: preserve store ordering
  }

  return list;
});

const formatPrice = (value) => {
  return value.toLocaleString('vi-VN') + '₫';
};
</script>

<style scoped src="@/styles/views/courses/ProfessionalSkills.css"></style>
