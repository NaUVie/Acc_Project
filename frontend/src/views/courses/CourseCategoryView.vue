<template>
  <div class="course-category-view container">
    <!-- Header Section -->
    <div class="header-section animate-fade-in">
      <div class="badge">{{ categoryMeta.badge }}</div>
      <h1><span class="gradient-text">{{ categoryMeta.name }}</span></h1>
      <p class="subtitle">{{ categoryMeta.description }}</p>
    </div>

    <!-- Filter & Sort Bar (Dynamic) -->
    <div class="category-toolbar glass-card" v-if="categoryCourses.length > 0">
      <div class="results-count">
        Hiển thị <strong>{{ displayRange }}</strong> trong <strong>{{ filteredCourses.length }}</strong> khóa học
      </div>
      <div class="toolbar-actions">
        <!-- Level Filter -->
        <select v-model="selectedLevel" class="filter-select">
          <option value="">Tất cả cấp độ</option>
          <option value="Cơ bản">Cơ bản</option>
          <option value="Trung cấp">Trung cấp</option>
          <option value="Nâng cao">Nâng cao</option>
        </select>
        <!-- Sort Option -->
        <select v-model="sortBy" class="filter-select">
          <option value="default">Mới nhất</option>
          <option value="price-asc">Giá: Thấp đến Cao</option>
          <option value="price-desc">Giá: Cao đến Thấp</option>
        </select>
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
      <h3>Chưa có khóa học nào</h3>
      <p>Danh mục này đang được cập nhật thêm các khóa học mới. Vui lòng quay lại sau!</p>
      <router-link to="/" class="btn btn-primary">Về trang chủ</router-link>
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

// Category Metadata presets & fallback
const categoryMeta = computed(() => {
  const slug = currentSlug.value.toLowerCase();
  
  // Custom store category check
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

.category-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  margin-bottom: 30px;
  border-radius: var(--radius-lg);
}

.results-count {
  font-size: 14px;
  color: var(--text-secondary);
}

.toolbar-actions {
  display: flex;
  gap: 12px;
}

.filter-select {
  padding: 8px 16px;
  border-radius: 8px;
  border: 1px solid var(--border-color);
  background: white;
  color: var(--text-primary);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
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
</style>
