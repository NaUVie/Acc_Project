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

<style scoped>
.course-category-view {
  padding-top: 80px; /* Offset fixed header */
  background-color: var(--bg-primary, #f9fafb);
}

/* 1. Custom Announcement Banner */
.custom-course-announcement {
  position: relative;
  padding-block: 60px;
  background-color: #111111;
  color: #ffffff;
  overflow: hidden;
  display: flex;
  align-items: center;
}

@media (min-width: 768px) {
  .custom-course-announcement {
    padding-block: 80px;
  }
}

.cca-bg-image {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: 0;
  opacity: 0.8;
}

.cca-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to right, rgba(0, 0, 0, 0.85) 0%, rgba(0, 0, 0, 0.4) 100%);
  z-index: 1;
}

.cca-container {
  position: relative;
  z-index: 2;
  max-width: 1600px;
  width: 100%;
  margin-inline: auto;
  padding-inline: 24px;
  display: grid;
  grid-template-columns: 1fr;
  gap: 40px;
  align-items: center;
}

@media (min-width: 992px) {
  .cca-container {
    grid-template-columns: 1.2fr 1fr;
    gap: 60px;
  }
}

.cca-text-wrap {
  max-width: 700px;
}

.cca-heading {
  font-family: var(--font-sans);
  font-size: 32px;
  line-height: 1.2;
  font-weight: 700;
  color: #ffffff;
  margin: 0 0 16px 0;
  letter-spacing: -0.02em;
}

@media (min-width: 768px) {
  .cca-heading {
    font-size: 46px;
  }
}

.cca-subheading {
  font-size: 15px;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.85);
  margin: 0;
}

@media (min-width: 768px) {
  .cca-subheading {
    font-size: 17px;
  }
}

.cca-card-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  align-items: center;
  width: 100%;
}

@media (min-width: 992px) {
  .cca-card-container {
    align-items: flex-end;
  }
}

.cca-card {
  position: relative;
  display: flex;
  align-items: center;
  gap: 16px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  padding: 16px;
  text-decoration: none;
  max-width: 480px;
  width: 100%;
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  transition: transform 0.3s ease, background 0.3s ease, border-color 0.3s ease;
}

.cca-card:hover {
  transform: translateY(-4px);
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.3);
}

.cca-badge {
  position: absolute;
  top: -12px;
  right: 20px;
  background-color: var(--primary, #20869a);
  color: #ffffff;
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 700;
  line-height: 1.2;
  z-index: 3;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
  text-transform: uppercase;
}

.cca-card-image {
  width: 90px;
  height: 90px;
  flex-shrink: 0;
  border-radius: 8px;
  object-fit: cover;
  background-color: rgba(0, 0, 0, 0.2);
}

.cca-card-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
}

.cca-card-title {
  font-size: 13px;
  font-weight: 600;
  color: #ffffff;
  line-height: 1.4;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

@media (min-width: 480px) {
  .cca-card-title {
    font-size: 14px;
  }
}

.cca-card-prices {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.cca-card-price {
  font-size: 15px;
  font-weight: 700;
  color: #ffffff;
}

.cca-card-compare {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.5);
  text-decoration: line-through;
}

/* 2. Collection List Section */
.collection-list-section {
  padding-block: 40px;
  background-color: var(--bg-secondary, #ffffff);
  border-bottom: 1px solid var(--border-color, rgba(16, 24, 40, 0.08));
}

.section-title {
  font-family: var(--font-sans);
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary-color, #101828);
  margin-bottom: 24px;
}

.collection-list-grid-wrapper {
  overflow-x: auto;
  padding-bottom: 10px;
  margin-inline: -24px;
  padding-inline: 24px;
  scrollbar-width: none;
}

.collection-list-grid-wrapper::-webkit-scrollbar {
  display: none;
}

.collection-list-grid {
  display: flex;
  gap: 16px;
  width: max-content;
}

@media (min-width: 1024px) {
  .collection-list-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    width: 100%;
  }
}

.collection-card {
  display: flex;
  flex-direction: column;
  gap: 12px;
  text-decoration: none;
  width: 160px;
  transition: transform 0.3s ease;
}

@media (min-width: 1024px) {
  .collection-card {
    width: 100%;
  }
}

.collection-card:hover {
  transform: translateY(-4px);
}

.collection-card__image-wrapper {
  position: relative;
  aspect-ratio: 16 / 9;
  border-radius: 8px;
  overflow: hidden;
  border: 2px solid transparent;
  transition: border-color 0.3s ease;
}

.collection-card.active .collection-card__image-wrapper {
  border-color: var(--primary, #20869a);
}

.collection-card__image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.collection-card:hover .collection-card__image {
  transform: scale(1.05);
}

.collection-card__overlay {
  position: absolute;
  inset: 0;
  background-color: rgba(16, 24, 40, 0.1);
  transition: background-color 0.3s ease;
}

.collection-card:hover .collection-card__overlay {
  background-color: rgba(16, 24, 40, 0);
}

.collection-card__title {
  font-size: 13px;
  font-weight: 600;
  text-align: center;
  color: var(--text-secondary, #475467);
  transition: color 0.3s ease;
}

.collection-card.active .collection-card__title,
.collection-card:hover .collection-card__title {
  color: var(--primary, #20869a);
}

/* 3. Main Catalog Section */
.main-catalog-section {
  padding-block: 40px 80px;
}

.collection-layout {
  display: grid;
  grid-template-columns: 1fr;
  gap: 40px;
}

@media (min-width: 1000px) {
  .collection-layout {
    grid-template-columns: 280px 1fr;
  }
}

/* Sidebar Filters */
.collection__sidebar-filters {
  display: none;
}

@media (min-width: 1000px) {
  .collection__sidebar-filters {
    display: block;
  }
}

.filters-widget {
  position: sticky;
  top: 100px;
  background: var(--bg-secondary, #ffffff);
  border: 1px solid var(--border-color, rgba(16, 24, 40, 0.08));
  border-radius: 12px;
  padding: 24px;
}

.widget-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  border-bottom: 1px solid var(--border-color, rgba(16, 24, 40, 0.08));
  padding-bottom: 12px;
}

.widget-title {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary-color, #101828);
}

.clear-filters-link {
  font-size: 12px;
  color: var(--primary, #20869a);
  background: none;
  border: none;
  font-weight: 600;
  cursor: pointer;
  padding: 0;
}

.clear-filters-link:hover {
  text-decoration: underline;
}

.filter-group {
  margin-bottom: 24px;
}

.filter-group:last-child {
  margin-bottom: 0;
}

.filter-group-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary-color, #101828);
  margin-bottom: 14px;
}

.filter-options {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.filter-checkbox-label {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  font-size: 13px;
  color: var(--text-secondary, #475467);
}

.filter-checkbox-label input {
  accent-color: var(--primary, #20869a);
  width: 16px;
  height: 16px;
  border-radius: 4px;
}

.price-range-inputs {
  display: flex;
  align-items: center;
  gap: 8px;
}

.price-input-wrapper {
  position: relative;
  flex: 1;
}

.price-input-wrapper input {
  width: 100%;
  padding: 8px 24px 8px 12px;
  border: 1px solid var(--border-color, rgba(16, 24, 40, 0.12));
  border-radius: 6px;
  font-size: 13px;
  outline: none;
  background-color: var(--bg-primary, #f9fafb);
  -moz-appearance: textfield;
}

.price-input-wrapper input::-webkit-outer-spin-button,
.price-input-wrapper input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.currency-label {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 12px;
  color: var(--text-muted, #667085);
  pointer-events: none;
}

.price-separator {
  color: var(--text-muted, #667085);
  font-size: 14px;
}

/* Results Content */
.collection__results {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.collection-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--border-color, rgba(16, 24, 40, 0.08));
  padding-bottom: 16px;
}

.toolbar-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.mobile-filter-trigger {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background-color: var(--bg-secondary, #ffffff);
  border: 1px solid var(--border-color, rgba(16, 24, 40, 0.12));
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary-color, #101828);
  cursor: pointer;
}

.mobile-filter-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background-color: var(--primary, #20869a);
  color: white;
  font-size: 10px;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  font-weight: 700;
}

@media (min-width: 1000px) {
  .mobile-filter-trigger {
    display: none;
  }
}

.results-count {
  font-size: 13px;
  color: var(--text-muted, #667085);
}

.sort-selector {
  display: flex;
  align-items: center;
  gap: 8px;
}

.sort-label {
  font-size: 13px;
  color: var(--text-muted, #667085);
  display: none;
}

@media (min-width: 480px) {
  .sort-label {
    display: inline;
  }
}

.sort-select {
  padding: 8px 12px;
  border: 1px solid var(--border-color, rgba(16, 24, 40, 0.12));
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary-color, #101828);
  outline: none;
  background-color: var(--bg-secondary, #ffffff);
  cursor: pointer;
}

/* Products Grid */
.collection-products-grid {
  display: grid;
  grid-template-columns: repeat(var(--product-list-items-per-row, 1), minmax(0, 1fr));
  gap: 24px;
}

.product-grid-item {
  height: 100%;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 60px 24px;
  background: var(--bg-secondary, #ffffff);
  border: 1px solid var(--border-color, rgba(16, 24, 40, 0.08));
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.empty-icon {
  color: var(--text-muted, #667085);
}

.empty-state h3 {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary-color, #101828);
}

.empty-state p {
  font-size: 14px;
  color: var(--text-secondary, #475467);
  max-width: 400px;
  line-height: 1.6;
}

.clear-filters-btn {
  background: var(--primary-gradient);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: var(--rounded-button);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(32, 134, 154, 0.3);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.clear-filters-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(32, 134, 154, 0.4);
}

/* 4. Mobile Drawer */
.mobile-filters-drawer {
  position: fixed;
  inset: 0;
  z-index: 1000;
  visibility: hidden;
  transition: visibility 0.3s ease;
}

.mobile-filters-drawer.open {
  visibility: visible;
}

.drawer-backdrop {
  position: absolute;
  inset: 0;
  background-color: rgba(16, 24, 40, 0.4);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.mobile-filters-drawer.open .drawer-backdrop {
  opacity: 1;
}

.drawer-content {
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  width: 85%;
  max-width: 340px;
  background-color: var(--bg-secondary, #ffffff);
  transform: translateX(-100%);
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  display: flex;
  flex-direction: column;
  box-shadow: 10px 0 30px rgba(16, 24, 40, 0.15);
}

.mobile-filters-drawer.open .drawer-content {
  transform: translateX(0);
}

.drawer-header {
  padding: 16px 20px;
  border-bottom: 1px solid var(--border-color, rgba(16, 24, 40, 0.08));
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.drawer-header h3 {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary-color, #101828);
}

.close-drawer-btn {
  background: none;
  border: none;
  color: var(--text-secondary, #475467);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.drawer-body {
  padding: 24px 20px;
  overflow-y: auto;
  flex-grow: 1;
}

.drawer-footer {
  padding: 16px 20px;
  border-top: 1px solid var(--border-color, rgba(16, 24, 40, 0.08));
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  gap: 12px;
}

.drawer-footer .btn {
  padding-block: 10px;
  font-size: 13px;
  width: 100%;
}
</style>
