<template>
  <div class="course-category-view container">


    <!-- Mega Dropdown-Style Layout Container -->
    <div class="mega-style-layout glass-card">
      <!-- Left Sidebar: Categories Navigation -->
      <div class="mega-menu-sidebar">
        <button 
          v-for="cat in availableCategories" 
          :key="cat.id"
          class="mega-sidebar-item"
          :class="{ active: selectedCategory === cat.id }"
          @click="selectCategory(cat.id)"
          @mouseenter="selectCategoryHover(cat.id)"
        >
          <span class="indicator-bar"></span>
          <span>{{ cat.name }}</span>
          <span class="cat-count-badge">{{ getCategoryCount(cat.id) }}</span>
        </button>
      </div>

      <!-- Right Content: Courses Grid for regular categories -->
      <div class="mega-menu-content" v-if="selectedCategory !== 'corporate'">

        <!-- Course Cards Grid (Matching Mega Program Card Grid Style) -->
        <template v-if="filteredCourses.length > 0">
          <div class="mega-programs-grid">
            <div 
              v-for="course in paginatedCourses" 
              :key="course.id"
              class="mega-program-card"
            >
              <router-link :to="'/course/' + (course.handle || course.id)" class="mega-card-link">
                <div class="mega-school-logo">
                  <img :src="formatImageUrl(course.image, 'w800') || '/images/Square-Cover-_1.webp'" :alt="course.title" loading="lazy" decoding="async" @error="handleImageError" />
                </div>
                <div class="mega-card-info">
                  <span class="mega-school-name">{{ course.level || 'Khóa học' }}</span>
                  <h4 class="mega-program-title" :title="course.title">{{ course.title }}</h4>
                  <p class="mega-program-desc">{{ stripHtml(course.description) }}</p>
                  <div class="mega-card-footer">
                    <div class="btn-link-stretch">
                      <div class="arrow-stretch-box">
                        <span class="line-body"></span>
                        <span class="arrow-tip"></span>
                      </div>
                    </div>
                  </div>
                </div>
              </router-link>
            </div>
          </div>

          <!-- Pagination Component -->
          <Pagination 
            v-if="filteredCourses.length > pageSize"
            v-model:currentPage="currentPage"
            :totalItems="filteredCourses.length"
            :pageSize="pageSize"
            @page-change="onPageChange"
          />
        </template>

        <div v-else class="empty-state">
          <p>{{ $t('course.emptyCategory') }}</p>
        </div>
      </div>

      <!-- Corporate Menu Panel inside Mega Style Layout -->
      <div class="mega-menu-content corporate-mega-content" v-else>
        <div class="mega-content-header">
          <div>
            <span class="cat-badge-small">IN-HOUSE & TƯ VẤN</span>
            <h2 class="mega-content-title">Giải pháp Đào tạo Doanh nghiệp</h2>
          </div>
          <router-link to="/corporate/dao-tao" class="mega-view-all-link">
            Tìm hiểu chi tiết &rarr;
          </router-link>
        </div>

        <div class="corporate-menu-grid">
          <div class="corporate-menu-group">
            <div class="corporate-group-header">
              <router-link to="/corporate/dao-tao" class="corporate-group-title">
                <span class="icon-bullet">🚀</span>
                Đào tạo AI INHOUSE cho doanh nghiệp
              </router-link>
            </div>
            <ul class="corporate-sub-list">
              <li><router-link to="/corporate/dao-tao" class="corporate-sub-link">Đào tạo AI cho Cơ quan Nhà nước, UBND & Phường/Xã</router-link></li>
              <li><router-link to="/corporate/dao-tao" class="corporate-sub-link">Đào tạo AI chuyên ngành Y tế & Thẩm mỹ</router-link></li>
              <li><router-link to="/corporate/dao-tao" class="corporate-sub-link">Đào tạo AI chuyên ngành Xây dựng</router-link></li>
              <li><router-link to="/corporate/dao-tao" class="corporate-sub-link">Đào tạo AI cho Doanh nghiệp Sản xuất & Thương mại</router-link></li>
              <li><router-link to="/corporate/dao-tao" class="corporate-sub-link">Đào tạo AI cho Trường học & Cơ sở Giáo dục</router-link></li>
            </ul>
          </div>

          <div class="corporate-menu-group">
            <div class="corporate-group-header">
              <router-link to="/corporate/coe" class="corporate-group-title">
                <span class="icon-bullet">🛡️</span>
                Quản trị & Bảo mật Dữ liệu Doanh nghiệp
              </router-link>
            </div>

            <div class="corporate-group-header style-mt">
              <router-link to="/corporate/for-team" class="corporate-group-title">
                <span class="icon-bullet">📊</span>
                Xây dựng Khung năng lực & Phát triển Nhân sự
              </router-link>
            </div>
            <ul class="corporate-sub-list">
              <li><router-link to="/corporate/for-team" class="corporate-sub-link">Xây dựng Ma trận năng lực theo vị trí</router-link></li>
              <li><router-link to="/corporate/for-team" class="corporate-sub-link">Tích hợp năng lực AI & năng lực số</router-link></li>
              <li><router-link to="/corporate/for-team" class="corporate-sub-link">Xây dựng khung năng lực theo phòng ban</router-link></li>
              <li><router-link to="/corporate/for-team" class="corporate-sub-link">Xây dựng Lộ trình đào tạo toàn diện</router-link></li>
            </ul>
          </div>

          <div class="corporate-menu-group">
            <div class="corporate-group-header">
              <router-link to="/corporate/case-studies" class="corporate-group-title">
                <span class="icon-bullet">💡</span>
                Năng lực Lãnh đạo Chủ động & Hiệu quả
              </router-link>
            </div>

            <div class="corporate-group-header style-mt">
              <router-link to="/corporate/case-studies" class="corporate-group-title">
                <span class="icon-bullet">🤝</span>
                Phát triển Kỹ năng mềm Doanh nghiệp
              </router-link>
            </div>

            <div class="corporate-group-header style-mt">
              <router-link to="/corporate/case-studies" class="corporate-group-title">
                <span class="icon-bullet">🎤</span>
                Nghệ thuật Kể chuyện & Truyền cảm hứng
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useCourseStore } from '@/stores/courses';
import { stripHtml } from '@/utils/stripHtml';
import { formatImageUrl } from '@/utils/imageHelper';
import Pagination from '@/components/Pagination.vue';

const route = useRoute();
const router = useRouter();
const courseStore = useCourseStore();

const selectedCategory = ref(route.params.categorySlug || 'all');
const currentPage = ref(1);
const pageSize = ref(6);

onMounted(async () => {
  const paramSlug = route.params.categorySlug;
  if (paramSlug) {
    selectedCategory.value = paramSlug;
  }

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
});

watch(() => route.params.categorySlug, (newSlug) => {
  currentPage.value = 1;
  if (newSlug) {
    selectedCategory.value = newSlug;
  } else {
    selectedCategory.value = 'all';
  }
});

const selectCategory = (id) => {
  currentPage.value = 1;
  selectedCategory.value = id;
  if (id === 'all') {
    router.push('/courses');
  } else if (id !== 'corporate') {
    router.push(`/courses/category/${id}`);
  }
};

const selectCategoryHover = (id) => {
  if (selectedCategory.value !== id) {
    currentPage.value = 1;
  }
  selectedCategory.value = id;
};

const availableCategories = computed(() => {
  const list = [{ id: 'all', name: 'Tất cả khóa học' }];
  const cats = courseStore.categories || [];
  cats.forEach(c => {
    if (c.slug !== 'bundles') {
      list.push({ id: c.slug, name: c.name });
    }
  });
  return list;
});

const getCategoryCount = (id) => {
  if (id === 'all') return courseStore.courses.length;
  if (id === 'bundles') return courseStore.bundles ? courseStore.bundles.length : 0;
  return courseStore.getCoursesByCategory(id).length;
};



const filteredCourses = computed(() => {
  if (selectedCategory.value === 'all') {
    return courseStore.courses;
  }
  return courseStore.getCoursesByCategory(selectedCategory.value);
});

const paginatedCourses = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  return filteredCourses.value.slice(start, start + pageSize.value);
});

const onPageChange = () => {
  window.scrollTo({ top: 180, behavior: 'smooth' });
};

const formatPrice = (value) => {
  if (!value) return 'Liên hệ';
  if (typeof value === 'number') {
    return value.toLocaleString('vi-VN') + 'đ';
  }
  return value;
};

const handleImageError = (e) => {
  e.target.src = '/images/Square-Cover-_1.webp';
};
</script>

<style scoped src="@/styles/views/courses/CourseCategoryView.css"></style>
