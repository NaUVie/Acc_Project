<template>
  <div class="course-category-view container">
    <!-- Mega Style Layout Container -->
    <div class="mega-style-layout glass-card">
      <!-- Left Sidebar: Dynamic Categories Navigation -->
      <aside class="mega-menu-sidebar" aria-label="Danh mục khóa học">
        <template v-for="cat in availableCategories" :key="cat.id">
          <!-- Standard Category without Children -->
          <div v-if="cat.id !== 'dao-tao-inhouse'" class="sidebar-category-group">
            <button 
              type="button"
              class="mega-sidebar-item"
              :class="{ active: selectedCategory === cat.id }"
              @click="scrollToCategory(cat.id)"
            >
              <span class="indicator-bar"></span>
              <span class="sidebar-item-label">{{ cat.name }}</span>
            </button>
          </div>

          <!-- ĐÀO TẠO INHOUSE: Có các mục con (Hiệp hội, Doanh nghiệp, Khối cơ quan nhà nước, Khối trường học) - Mặc định sổ ra -->
          <div v-else class="sidebar-category-group is-inhouse-group">
            <div 
              class="mega-sidebar-item has-children"
              :class="{ active: selectedCategory === cat.id || isInhouseChildActive }"
              @click="selectCategory('dao-tao-inhouse')"
            >
              <span class="indicator-bar"></span>
              <span class="sidebar-item-label">{{ cat.name }}</span>
              <button 
                type="button" 
                class="submenu-toggle-btn"
                @click.stop="isInhouseExpanded = !isInhouseExpanded"
                :title="isInhouseExpanded ? 'Thu gọn danh mục con' : 'Sổ ra danh mục con'"
                aria-label="Toggle inhouse submenu"
              >
                <svg class="chevron-arrow" :class="{ 'rotate': isInhouseExpanded }" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <path d="M6 9l6 6 6-6"/>
                </svg>
              </button>
            </div>

            <!-- CÁC MỤC CON CỦA ĐÀO TẠO INHOUSE (MẶC ĐỊNH SỔ RA - KHÔNG ICON) -->
            <transition name="accordion-slide">
              <div 
                v-show="isInhouseExpanded" 
                class="sidebar-submenu"
              >
                <button 
                  v-for="sub in inhouseSubCategories" 
                  :key="sub.id"
                  type="button"
                  class="mega-sidebar-subitem"
                  :class="{ active: activeInhouseSub === sub.id && selectedCategory === sub.id }"
                  @click="selectInhouseSubCategory(sub.id)"
                >
                  <span class="subitem-dot"></span>
                  <span class="sidebar-subitem-label">{{ sub.name }}</span>
                </button>
              </div>
            </transition>
          </div>
        </template>
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
            :class="{ 'is-inhouse-section': cat.slug === 'dao-tao-inhouse' }"
          >
            <!-- CATEGORY HEADER -->
            <div class="category-section-header">
              <div class="category-header-info">
                <span class="cat-badge-small">CHƯƠNG TRÌNH ĐÀO TẠO</span>
                <h3 class="category-section-title">
                  {{ cat.name }}
                  <span v-if="cat.slug === 'dao-tao-inhouse' && activeInhouseSubName" class="sub-title-tag">
                    / {{ activeInhouseSubName }}
                  </span>
                </h3>
              </div>
              <div class="category-header-actions" v-if="cat.slug === 'dao-tao-inhouse' && activeInhouseSub !== 'all'">
                <button 
                  type="button" 
                  class="btn-reset-inhouse"
                  @click="selectCategory('dao-tao-inhouse')"
                >
                  ← Xem tất cả Inhouse
                </button>
              </div>
            </div>

            <!-- THANH LỌC NHANH CHO INHOUSE (TẤT CẢ, HIỆP HỘI, DOANH NGHIỆP, CƠ QUAN NHÀ NƯỚC, TRƯỜNG HỌC) -->
            <div v-if="cat.slug === 'dao-tao-inhouse'" class="inhouse-filter-pills">
              <button 
                type="button" 
                class="inhouse-pill-btn" 
                :class="{ active: activeInhouseSub === 'all' }"
                @click="selectCategory('dao-tao-inhouse')"
              >
                Tất cả Inhouse
              </button>
              <button 
                v-for="sub in inhouseSubCategories" 
                :key="sub.id"
                type="button" 
                class="inhouse-pill-btn" 
                :class="{ active: activeInhouseSub === sub.id }"
                @click="selectInhouseSubCategory(sub.id)"
              >
                {{ sub.name }}
              </button>
            </div>

            <!-- COURSE CARDS GRID -->
            <div v-if="displayedCoursesForCat(cat).length > 0" class="mega-programs-grid">
              <div 
                v-for="course in displayedCoursesForCat(cat)" 
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

            <!-- Empty category / subgroup state -->
            <div v-else class="empty-category-notice">
              <p>Chưa có khóa học nào trong khối này.</p>
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
const activeInhouseSub = ref('all'); // 'all' = hiển thị toàn bộ Inhouse bình thường, hoặc 'inhouse-hiep-hoi', 'inhouse-doanh-nghiep', etc.
const isInhouseExpanded = ref(true); // Mặc định sổ ra theo yêu cầu người dùng
let isProgrammaticScroll = false;

// Hàm phân loại các khóa học Inhouse vào 4 khối con
const classifyInhouseCourse = (course) => {
  const text = `${course.title || ''} ${course.description || ''} ${course.category || ''} ${course.category_slug || ''}`.toLowerCase();
  
  // 1. Hiệp hội
  if (text.includes('saca') || text.includes('hiệp hội') || text.includes('hiep hoi') || text.includes('hiep-hoi') || text.includes('association')) {
    return 'inhouse-hiep-hoi';
  }
  // 2. Khối trường học
  if (text.includes('giáo dục') || text.includes('giao duc') || text.includes('trường học') || text.includes('truong hoc') || text.includes('truong-hoc') || text.includes('school') || text.includes('đại học')) {
    return 'inhouse-truong-hoc';
  }
  // 3. Khối cơ quan nhà nước
  if (text.includes('nhà nước') || text.includes('nha nuoc') || text.includes('cơ quan') || text.includes('co quan') || text.includes('ubnd') || text.includes('phường') || text.includes('xã') || text.includes('quận') || text.includes('chính phủ')) {
    return 'inhouse-co-quan-nha-nuoc';
  }
  // 4. Doanh nghiệp (mặc định cho inhouse)
  return 'inhouse-doanh-nghiep';
};

// 4 mục con của Đào tạo INHOUSE (Hiệp hội, Doanh nghiệp, Khối cơ quan nhà nước, Khối trường học) - KHÔNG icon emoji
const inhouseSubCategories = computed(() => {
  const inhouseCourses = courseStore.getCoursesByCategory('dao-tao-inhouse') || [];
  
  const hiephoiCourses = inhouseCourses.filter(c => classifyInhouseCourse(c) === 'inhouse-hiep-hoi');
  const doanhnghiepCourses = inhouseCourses.filter(c => classifyInhouseCourse(c) === 'inhouse-doanh-nghiep');
  const nhanuocCourses = inhouseCourses.filter(c => classifyInhouseCourse(c) === 'inhouse-co-quan-nha-nuoc');
  const truonghocCourses = inhouseCourses.filter(c => classifyInhouseCourse(c) === 'inhouse-truong-hoc');

  return [
    { 
      id: 'inhouse-hiep-hoi', 
      name: 'Hiệp hội', 
      count: hiephoiCourses.length, 
      courses: hiephoiCourses 
    },
    { 
      id: 'inhouse-doanh-nghiep', 
      name: 'Doanh nghiệp', 
      count: doanhnghiepCourses.length, 
      courses: doanhnghiepCourses 
    },
    { 
      id: 'inhouse-co-quan-nha-nuoc', 
      name: 'Khối cơ quan nhà nước', 
      count: nhanuocCourses.length, 
      courses: nhanuocCourses 
    },
    { 
      id: 'inhouse-truong-hoc', 
      name: 'Khối trường học', 
      count: truonghocCourses.length, 
      courses: truonghocCourses 
    }
  ];
});

// Tên khối con Inhouse đang chọn
const activeInhouseSubName = computed(() => {
  if (activeInhouseSub.value === 'all') return '';
  const sub = inhouseSubCategories.value.find(s => s.id === activeInhouseSub.value);
  return sub ? sub.name : '';
});

// Kiểm tra xem một trong các mục con của Inhouse có đang active không
const isInhouseChildActive = computed(() => {
  return inhouseSubCategories.value.some(sub => sub.id === selectedCategory.value);
});

// Danh sách khóa học hiển thị cho từng chuyên mục
const displayedCoursesForCat = (cat) => {
  if (cat.slug === 'dao-tao-inhouse') {
    if (activeInhouseSub.value && activeInhouseSub.value !== 'all') {
      return cat.courses.filter(c => classifyInhouseCourse(c) === activeInhouseSub.value);
    }
    return cat.courses; // Ấn vào inhouse hiển thị toàn bộ bình thường
  }
  return cat.courses;
};

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

// Khi ấn vào danh mục cha (Inhouse -> hiển thị toàn bộ bình thường)
const selectCategory = (id) => {
  if (id === 'dao-tao-inhouse') {
    activeInhouseSub.value = 'all'; // Hiển thị toàn bộ inhouse bình thường
  }
  scrollToCategory(id);
};

// Khi ấn riêng từng khối con của Inhouse -> mới lọc riêng khối đó
const selectInhouseSubCategory = (subId) => {
  activeInhouseSub.value = subId;
  selectedCategory.value = subId;
  isInhouseExpanded.value = true;
  scrollToCategory('dao-tao-inhouse');
};

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
    const targetAnchor = id.startsWith('inhouse-') ? 'dao-tao-inhouse' : id;
    const el = document.getElementById(`category-${targetAnchor}`);
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

  const sections = dynamicCategories.value;
  if (!sections.length) return;

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

  if (currentActive !== 'dao-tao-inhouse' || activeInhouseSub.value === 'all') {
    if (selectedCategory.value !== currentActive) {
      selectedCategory.value = currentActive;
    }
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
    const ALIAS_MAP = {
      'hiep-hoi': 'inhouse-hiep-hoi',
      'doanh-nghiep': 'inhouse-doanh-nghiep',
      'co-quan-nha-nuoc': 'inhouse-co-quan-nha-nuoc',
      'nha-nuoc': 'inhouse-co-quan-nha-nuoc',
      'truong-hoc': 'inhouse-truong-hoc',
      'inhouse': 'dao-tao-inhouse'
    };
    const target = ALIAS_MAP[paramSlug] || paramSlug;
    await nextTick();
    setTimeout(() => {
      if (target.startsWith('inhouse-')) {
        selectInhouseSubCategory(target);
      } else {
        scrollToCategory(target, true);
      }
    }, 200);
  }
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
});

watch(() => route.params.categorySlug, (newSlug) => {
  if (newSlug) {
    const ALIAS_MAP = {
      'hiep-hoi': 'inhouse-hiep-hoi',
      'doanh-nghiep': 'inhouse-doanh-nghiep',
      'co-quan-nha-nuoc': 'inhouse-co-quan-nha-nuoc',
      'nha-nuoc': 'inhouse-co-quan-nha-nuoc',
      'truong-hoc': 'inhouse-truong-hoc',
      'inhouse': 'dao-tao-inhouse'
    };
    const target = ALIAS_MAP[newSlug] || newSlug;
    if (target.startsWith('inhouse-')) {
      selectInhouseSubCategory(target);
    } else {
      selectCategory(target);
    }
  } else {
    selectCategory('all');
  }
});

const handleImageError = (e) => {
  e.target.src = '/images/Square-Cover-_1.webp';
};
</script>

<style scoped src="@/styles/views/courses/CourseCategoryView.css"></style>