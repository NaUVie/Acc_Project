<template>
  <div class="course-category-view container">
    <!-- Header Section -->
    <div class="header-section animate-fade-in">
      <div class="badge">{{ categoryMeta.badge }}</div>
      <h1><span class="gradient-text">{{ categoryMeta.name }}</span></h1>
      <p class="subtitle">{{ categoryMeta.description }}</p>
    </div>

    <!-- Main Two-Column Layout -->
    <div class="category-main-layout">
      <!-- Left Sidebar Filters -->
      <aside class="sidebar-filter-panel glass-card">
        <!-- Section 1: Categories Navigation -->
        <div class="filter-group">
          <h3 class="filter-group-title">Danh Mục Khóa Học</h3>
          <ul class="category-nav-list">
            <li v-for="cat in availableCategories" :key="cat.slug">
              <router-link 
                :to="'/courses/category/' + cat.slug" 
                class="cat-nav-link"
                :class="{ active: currentSlug.toLowerCase() === cat.slug.toLowerCase() }"
              >
                <span>{{ cat.name }}</span>
                <span class="cat-count-badge" v-if="getCategoryCount(cat.slug)">{{ getCategoryCount(cat.slug) }}</span>
              </router-link>
            </li>
          </ul>
        </div>

        <!-- Section 2: Level Filter -->
        <div class="filter-group">
          <h3 class="filter-group-title">Trình Độ Học</h3>
          <div class="filter-options-list">
            <label class="filter-radio-option" :class="{ active: selectedLevel === '' }">
              <input type="radio" value="" v-model="selectedLevel" />
              <span>Tất cả cấp độ</span>
            </label>
            <label class="filter-radio-option" :class="{ active: selectedLevel === 'Cơ bản' }">
              <input type="radio" value="Cơ bản" v-model="selectedLevel" />
              <span>Cơ bản</span>
            </label>
            <label class="filter-radio-option" :class="{ active: selectedLevel === 'Trung cấp' }">
              <input type="radio" value="Trung cấp" v-model="selectedLevel" />
              <span>Trung cấp</span>
            </label>
            <label class="filter-radio-option" :class="{ active: selectedLevel === 'Nâng cao' }">
              <input type="radio" value="Nâng cao" v-model="selectedLevel" />
              <span>Nâng cao</span>
            </label>
          </div>
        </div>

        <!-- Section 3: Sort Options -->
        <div class="filter-group">
          <h3 class="filter-group-title">Sắp Xếp Theo</h3>
          <select v-model="sortBy" class="sidebar-select">
            <option value="default">Mới nhất</option>
            <option value="price-asc">Giá: Thấp đến Cao</option>
            <option value="price-desc">Giá: Cao đến Thấp</option>
          </select>
        </div>

        <!-- Reset Button -->
        <button 
          v-if="selectedLevel || sortBy !== 'default'" 
          class="btn-reset-filters"
          @click="resetFilters"
        >
          🔄 Xóa bộ lọc
        </button>
      </aside>

      <!-- Right Main Content Area -->
      <main class="category-content-area">
        <!-- Results Count Header -->
        <div class="category-toolbar glass-card" v-if="categoryCourses.length > 0">
          <div class="results-count">
            Hiển thị <strong>{{ displayRange }}</strong> trong <strong>{{ filteredCourses.length }}</strong> khóa học
          </div>
        </div>

        <!-- Courses Grid -->
        <div class="courses-grid-wrapper" v-if="filteredCourses.length > 0">
          <div class="courses-grid">
            <div v-for="course in paginatedCourses" :key="course.id" class="course-card glass-card animate-slide-up">
              <router-link :to="'/course/' + course.handle" class="card-image-container">
                <img :src="course.image || '/images/Square-Cover-_1.webp'" :alt="course.title" class="course-image" @error="handleImageError" />
                <div class="card-image-overlay" v-if="course.tags && course.tags.length">
                  <span v-for="tag in course.tags.slice(0, 2)" :key="tag" class="image-tag">{{ tag }}</span>
                </div>
              </router-link>
              <div class="card-body">
                <div class="card-header-meta">
                  <span class="course-badge" :class="{ 'best-seller': course.price > 3000000 }">
                    {{ course.price > 3000000 ? 'Chuyên sâu' : 'Hot' }}
                  </span>
                  <span class="level-badge">{{ course.level || 'Tổng quát' }}</span>
                </div>
                <h3>
                  <router-link :to="'/course/' + course.handle" class="course-title-link">
                    {{ course.title }}
                  </router-link>
                </h3>
                <p>{{ course.description }}</p>
                <div class="course-meta">
                  <span class="duration">⏱️ {{ course.duration || 'Linh hoạt' }}</span>
                </div>
                <div class="card-footer">
                  <div class="price-container">
                    <span class="original-price" v-if="course.originalPrice">{{ formatPrice(course.originalPrice) }}</span>
                    <span class="price">{{ formatPrice(course.price) }}</span>
                  </div>
                  <button @click.stop="handleEnroll(course.id)" class="btn btn-primary btn-sm">Đăng ký học</button>
                </div>
              </div>
            </div>
          </div>

          <!-- Pagination Component -->
          <Pagination 
            :currentPage="currentPage" 
            :totalItems="filteredCourses.length" 
            :pageSize="pageSize" 
            @update:currentPage="currentPage = $event"
          />
        </div>

        <!-- Empty State -->
        <div class="empty-category-state glass-card" v-else>
          <div class="empty-icon">📚</div>
          <h3>Chưa tìm thấy khóa học phù hợp</h3>
          <p>Không có khóa học nào khớp với bộ lọc đã chọn hoặc danh mục này đang cập nhật.</p>
          <button @click="resetFilters" class="btn btn-primary">Xóa bộ lọc</button>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useCourseStore } from '@/stores/courses';
import Pagination from '@/components/Pagination.vue';

const route = useRoute();
const router = useRouter();
const courseStore = useCourseStore();

const selectedLevel = ref('');
const sortBy = ref('default');
const currentPage = ref(1);
const pageSize = ref(6);

onMounted(async () => {
  if (courseStore.courses.length === 0) {
    await courseStore.fetchCourses();
  }
  if (courseStore.categories && courseStore.categories.length === 0) {
    await courseStore.fetchCategories();
  }
});

// Dynamic category slug from URL
const currentSlug = computed(() => {
  return route.params.categorySlug || 'ky-nang-ai';
});

watch([selectedLevel, sortBy, currentSlug], () => {
  currentPage.value = 1;
});

// Categories list for Sidebar
const availableCategories = computed(() => {
  if (courseStore.categories && courseStore.categories.length > 0) {
    return courseStore.categories;
  }
  return [
    { slug: 'ky-nang-ai', name: 'Kỹ năng AI & Tự động hóa' },
    { slug: 'ky-nang-chuyen-mon', name: 'Kỹ năng chuyên môn' },
    { slug: 'ky-nang-mem', name: 'Kỹ năng mềm' }
  ];
});

const getCategoryCount = (slug) => {
  return courseStore.getCoursesByCategory(slug).length;
};

const resetFilters = () => {
  selectedLevel.value = '';
  sortBy.value = 'default';
};

// Category Metadata presets & fallback
const categoryMeta = computed(() => {
  const slug = currentSlug.value.toLowerCase();
  const matchedCategory = courseStore.categories?.find(c => c.slug === slug);
  
  if (slug === 'ky-nang-ai' || slug === 'ai') {
    return {
      name: 'Kỹ năng Ứng dụng AI',
      badge: 'CHUYÊN ĐỀ CÔNG NGHỆ SỐ',
      description: 'Làm chủ các công cụ trí tuệ nhân tạo (ChatGPT, Claude, Copilot, Midjourney) để tối ưu hóa quy trình làm việc và đột phá năng lực bản thân.'
    };
  }
  if (slug === 'ky-nang-mem' || slug === 'mem') {
    return {
      name: 'Kỹ năng mềm',
      badge: 'PHÁT TRIỂN BẢN THÂN',
      description: 'Nâng cao tư duy phản biện, kỹ năng làm việc nhóm, quản lý thời gian và giải quyết vấn đề hiệu quả trong môi trường hiện đại.'
    };
  }
  if (slug === 'ky-nang-chuyen-mon' || slug === 'chuyen-mon') {
    return {
      name: 'Kỹ năng chuyên môn',
      badge: 'NĂNG LỰC CHUYÊN SÂU',
      description: 'Trở thành chuyên gia trong lĩnh vực tài chính, kế toán, kiểm toán và phân tích dữ liệu kinh doanh với lộ trình thực chiến.'
    };
  }

  return {
    name: matchedCategory ? matchedCategory.name : slug.replace(/-/g, ' ').toUpperCase(),
    badge: 'DANH MỤC KHÓA HỌC',
    description: 'Khám phá các khóa học chất lượng cao được thiết kế riêng cho sự nghiệp của bạn.'
  };
});

// Raw category courses from store
const categoryCourses = computed(() => {
  return courseStore.getCoursesByCategory(currentSlug.value);
});

// Filtered and Sorted courses
const filteredCourses = computed(() => {
  let list = [...categoryCourses.value];

  if (selectedLevel.value) {
    list = list.filter(c => c.level && c.level.includes(selectedLevel.value));
  }

  if (sortBy.value === 'price-asc') {
    list.sort((a, b) => a.price - b.price);
  } else if (sortBy.value === 'price-desc') {
    list.sort((a, b) => b.price - a.price);
  }

  return list;
});

// Paginated courses slice
const paginatedCourses = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  return filteredCourses.value.slice(start, start + pageSize.value);
});

const displayRange = computed(() => {
  const total = filteredCourses.value.length;
  if (total === 0) return '0';
  const start = (currentPage.value - 1) * pageSize.value + 1;
  const end = Math.min(currentPage.value * pageSize.value, total);
  return `${start}-${end}`;
});

const formatPrice = (value) => {
  if (!value) return '0đ';
  return value.toLocaleString('vi-VN') + 'đ';
};

const handleEnroll = async (courseId) => {
  if (!courseStore.token) {
    courseStore.showToast('Vui lòng đăng nhập để đăng ký khóa học!', 'warning');
    router.push('/login');
    return;
  }
  try {
    await courseStore.buyNow(courseId);
    router.push('/checkout');
  } catch (err) {
    if (err.message !== 'CANCELLED') {
      courseStore.showToast(err.message || 'Có lỗi xảy ra khi đăng ký khóa học!', 'error');
    }
  }
};

const handleImageError = (e) => {
  e.target.src = 'https://images.unsplash.com/photo-1677442136019-21780efad99a?q=80&w=600&auto=format&fit=crop';
};
</script>

<style scoped>
@import "@/styles/views/courses/AISkills.css";

.category-main-layout {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 28px;
  align-items: start;
  margin-top: 30px;
}

.sidebar-filter-panel {
  padding: 24px;
  border-radius: var(--radius-lg);
  background: #ffffff;
  border: 1px solid var(--border-color);
  position: sticky;
  top: 100px;
}

.filter-group {
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 1px solid #f1f5f9;
}

.filter-group:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.filter-group-title {
  font-size: 15px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 14px;
}

.category-nav-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.cat-nav-link {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 14px;
  border-radius: 8px;
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s ease;
}

.cat-nav-link:hover {
  background: #f8fafc;
  color: #022B9F;
}

.cat-nav-link.active {
  background: #eef2ff;
  color: #022B9F;
  font-weight: 700;
}

.cat-count-badge {
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 99px;
  background: #f1f5f9;
  color: #64748b;
}

.cat-nav-link.active .cat-count-badge {
  background: #022B9F;
  color: white;
}

.filter-options-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-radio-option {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 6px 8px;
  border-radius: 6px;
  transition: background 0.2s ease;
}

.filter-radio-option:hover {
  background: #f8fafc;
}

.filter-radio-option input {
  accent-color: #022B9F;
}

.sidebar-select {
  width: 100%;
  padding: 10px 14px;
  border-radius: 8px;
  border: 1px solid var(--border-color);
  background: white;
  font-size: 13px;
  color: var(--text-primary);
}

.btn-reset-filters {
  width: 100%;
  padding: 10px;
  margin-top: 10px;
  border-radius: 8px;
  background: #f1f5f9;
  border: none;
  color: #475569;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
}

.btn-reset-filters:hover {
  background: #e2e8f0;
}

.category-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 20px;
  margin-bottom: 24px;
  border-radius: var(--radius-lg);
}

.results-count {
  font-size: 14px;
  color: var(--text-secondary);
}

.empty-category-state {
  text-align: center;
  padding: 60px 24px;
  margin-top: 20px;
  border-radius: var(--radius-lg);
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.empty-category-state h3 {
  font-size: 22px;
  font-weight: 700;
  margin-bottom: 8px;
}

.empty-category-state p {
  color: var(--text-secondary);
  margin-bottom: 24px;
}

@media (max-width: 992px) {
  .category-main-layout {
    grid-template-columns: 1fr;
  }
  .sidebar-filter-panel {
    position: static;
  }
}
</style>
