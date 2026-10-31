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
                  <img :src="course.image || '/images/Square-Cover-_1.webp'" :alt="course.title" @error="handleImageError" />
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
          <p>Chưa tìm thấy khóa học phù hợp trong danh mục này.</p>
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

<style scoped>
.course-category-view {
  padding-top: 120px;
  padding-bottom: 100px;
  min-height: 100vh;
  background-color: #f8fafc;
}

.header-section {
  text-align: center;
  max-width: 860px;
  margin-inline: auto;
  margin-bottom: 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 14px;
}

.badge {
  display: inline-block;
  font-size: 12px;
  font-weight: 800;
  color: #022b9f;
  background: rgba(2, 43, 159, 0.08);
  padding: 5px 16px;
  border-radius: 20px;
  letter-spacing: 1px;
}

.gradient-text {
  background: linear-gradient(135deg, #022b9f 0%, #2563eb 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.mega-style-layout {
  display: grid;
  grid-template-columns: 280px 1fr;
  min-height: 560px;
  background: #ffffff;
  border-radius: 20px;
  border: 1px solid #eaecf0;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.06);
  overflow: hidden;
}

@media (max-width: 992px) {
  .mega-style-layout {
    grid-template-columns: 1fr;
  }
}

/* Sidebar Column */
.mega-menu-sidebar {
  background-color: #f8fafc;
  padding: 28px 18px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  border-right: 1px solid #eaecf0;
}

.mega-sidebar-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 18px;
  background: transparent;
  border: none;
  color: #475467;
  font-size: 14.5px;
  font-weight: 600;
  text-align: left;
  border-radius: 10px;
  cursor: pointer;
  position: relative;
  transition: all 0.25s ease;
}

.mega-sidebar-item .indicator-bar {
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 0;
  background-color: #022B9F;
  transition: height 0.25s ease;
  border-radius: 0 3px 3px 0;
}

.mega-sidebar-item:hover,
.mega-sidebar-item.active {
  color: #022B9F;
  background-color: rgba(2, 43, 159, 0.06);
}

.mega-sidebar-item:hover .indicator-bar,
.mega-sidebar-item.active .indicator-bar {
  height: 60%;
}

.mega-sidebar-item.active {
  background-color: rgba(2, 43, 159, 0.09);
  font-weight: 700;
}

.cat-count-badge {
  font-size: 11px;
  padding: 3px 8px;
  border-radius: 12px;
  background: #e2e8f0;
  color: #475569;
}

.mega-sidebar-item.active .cat-count-badge {
  background: #022B9F;
  color: #ffffff;
}

/* Right Content Column */
.mega-menu-content {
  background-color: #ffffff;
  padding: 36px 40px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.mega-content-header {
  display: flex;
  flex-direction: column;
  gap: 6px;
  border-bottom: 1px solid #eaecf0;
  padding-bottom: 18px;
}

.cat-badge-small {
  font-size: 11px;
  font-weight: 800;
  color: #022b9f;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.mega-content-title {
  font-size: 24px;
  font-weight: 800;
  color: #0f172a;
  margin: 0;
}

.cat-desc-small {
  font-size: 14px;
  color: #475569;
  line-height: 1.5;
  margin: 0;
}

/* Program Card Grid */
.mega-programs-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

@media (min-width: 1200px) {
  .mega-programs-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .mega-programs-grid {
    grid-template-columns: 1fr;
  }
}

.mega-program-card {
  background-color: #ffffff;
  border: 1px solid #eaecf0;
  border-radius: 14px;
  padding: 20px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.02);
}

.mega-program-card:hover {
  transform: translateY(-4px);
  background-color: #f8fafc;
  border-color: #022B9F;
  box-shadow: 0 12px 28px rgba(2, 43, 159, 0.1);
}

.mega-card-link {
  display: flex;
  flex-direction: column;
  gap: 12px;
  text-decoration: none;
  height: 100%;
}

.mega-school-logo {
  width: 100%;
  aspect-ratio: 16 / 9;
  height: auto;
  border-radius: 10px;
  overflow: hidden;
  background-color: #ffffff;
}

.mega-school-logo img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  object-position: center center;
  transition: transform 0.4s ease;
}

.mega-program-card:hover .mega-school-logo img {
  transform: scale(1.05);
}

.mega-card-info {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  gap: 6px;
}

.mega-school-name {
  color: #022B9F;
  font-size: 11.5px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.mega-program-title {
  color: #0f172a;
  font-size: 16px;
  font-weight: 700;
  line-height: 1.4;
  margin: 0;
}

.mega-program-desc {
  font-size: 13px;
  color: #475569;
  line-height: 1.5;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.mega-card-footer {
  margin-top: auto;
  padding-top: 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  border-top: 1px dashed #e2e8f0;
}

.mega-course-price {
  display: flex;
  align-items: baseline;
  gap: 6px;
  white-space: nowrap;
  flex-shrink: 0;
}

.current-price {
  font-size: 15px;
  font-weight: 800;
  color: #022B9F;
  white-space: nowrap;
}

.original-price {
  font-size: 12px;
  color: #94a3b8;
  text-decoration: line-through;
  white-space: nowrap;
}

.btn-link-stretch {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  text-decoration: none;
  color: #022B9F;
  padding-block: 4px;
}

.arrow-stretch-box {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  margin-left: auto;
  margin-right: 0;
  width: 30px;
  max-width: 100%;
  transition: width 0.45s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.btn-link-stretch .line-body {
  width: 24px;
  height: 2px;
  background-color: currentColor;
  transition: width 0.45s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.btn-link-stretch .arrow-tip {
  border: solid currentColor;
  border-width: 0 2.5px 2.5px 0;
  display: inline-block;
  padding: 3.5px;
  transform: rotate(-45deg);
  margin-left: -6px;
  flex-shrink: 0;
}

.mega-program-card:hover .arrow-stretch-box,
.btn-link-stretch:hover .arrow-stretch-box {
  width: 90px;
}

.mega-program-card:hover .btn-link-stretch .line-body,
.btn-link-stretch:hover .line-body {
  width: 84px;
}

/* Corporate Mega Menu Panel */
.corporate-menu-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
  align-items: start;
}

@media (max-width: 992px) {
  .corporate-menu-grid {
    grid-template-columns: 1fr;
  }
}

.corporate-menu-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.corporate-group-header {
  padding-bottom: 10px;
  border-bottom: 1px solid #eaecf0;
}

.corporate-group-header.style-mt {
  margin-top: 20px;
}

.corporate-group-title {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  font-weight: 700;
  color: #0f172a;
  text-decoration: none;
  line-height: 1.35;
  transition: color 0.2s ease;
}

.corporate-group-title:hover {
  color: #022B9F;
}

.icon-bullet {
  font-size: 16px;
  flex-shrink: 0;
}

.corporate-sub-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding-left: 12px;
}

.corporate-sub-link {
  font-size: 13.5px;
  color: #475569;
  text-decoration: none;
  line-height: 1.45;
  transition: all 0.2s ease;
  display: block;
}

.corporate-sub-link:hover {
  color: #022B9F;
  font-weight: 600;
  transform: translateX(4px);
}
</style>
