<template>
  <div class="admin-view container">
    <div class="admin-layout glass-card animate-fade-in">
      
      <!-- SIDEBAR NAV -->
      <aside class="admin-sidebar">
        <div class="sidebar-header">
          <span class="admin-logo-badge">👑 ACC ADMIN</span>
          <p class="admin-subtitle">Hệ thống quản trị vận hành</p>
        </div>
        <nav class="sidebar-menu">
          <button 
            v-for="tab in tabs" 
            :key="tab.id"
            class="sidebar-menu-item"
            :class="{ active: activeTab === tab.id }"
            @click="activeTab = tab.id"
          >
            <span class="menu-icon">{{ tab.icon }}</span>
            <span class="menu-label">{{ tab.name }}</span>
          </button>
        </nav>
        <div class="sidebar-footer">
          <router-link to="/" class="btn btn-outline btn-sm w-full text-center">
            &larr; Về Trang chủ
          </router-link>
        </div>
      </aside>

      <!-- MAIN CONTENT PANEL -->
      <main class="admin-main">
        <component :is="currentTabComponent" />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useCourseStore } from '@/stores/courses';

// Import modular tab components
import AdminOverview from './components/AdminOverview.vue';
import AdminOrders from './components/AdminOrders.vue';
import AdminUsers from './components/AdminUsers.vue';
import AdminContacts from './components/AdminContacts.vue';
import AdminCourses from './components/AdminCourses.vue';
import AdminCategories from './components/AdminCategories.vue';
import AdminPrograms from './components/AdminPrograms.vue';
import AdminBundles from './components/AdminBundles.vue';
import AdminBanners from './components/AdminBanners.vue';
import AdminCoupons from './components/AdminCoupons.vue';
import AdminCommissions from './components/AdminCommissions.vue';
import AdminLecturers from './components/AdminLecturers.vue';
import AdminTestimonials from './components/AdminTestimonials.vue';
import AdminProjects from './components/AdminProjects.vue';
import AdminBlogs from './components/AdminBlogs.vue';

const route = useRoute();
const router = useRouter();
const courseStore = useCourseStore();

// Setup Tab navigation
const tabs = [
  { id: 'overview', name: 'Tổng quan', icon: '📊' },
  { id: 'blogs', name: 'Tin tức & Bài viết', icon: '📰' },
  { id: 'projects', name: 'Dự án Case Study', icon: '💼' },
  { id: 'testimonials', name: 'Cảm nhận học viên', icon: '💬' },
  { id: 'coupons', name: 'Mã giảm giá', icon: '🎟️' },
  { id: 'commissions', name: 'Hoa hồng Affiliate', icon: '🤝' },
  { id: 'lecturers', name: 'Giảng viên', icon: '👨‍🏫' },
  { id: 'banners', name: 'Banner Hero', icon: '🖼️' },
  { id: 'categories', name: 'Chuyên mục', icon: '🏷️' },
  { id: 'courses', name: 'Khóa học', icon: '📚' },
  { id: 'programs', name: 'Chương trình', icon: '🎓' },
  { id: 'bundles', name: 'Gói Combo', icon: '📦' },
  { id: 'orders', name: 'Đơn hàng', icon: '🛍️' },
  { id: 'users', name: 'Học viên', icon: '👥' },
  { id: 'contacts', name: 'Liên hệ', icon: '✉️' }
];

const getInitialTab = () => {
  const queryTab = route.query.tab;
  if (queryTab && tabs.some(t => t.id === queryTab)) {
    return queryTab;
  }
  const savedTab = localStorage.getItem('acc_admin_active_tab');
  if (savedTab && tabs.some(t => t.id === savedTab)) {
    return savedTab;
  }
  return 'overview';
};

const activeTab = ref(getInitialTab());

watch(activeTab, (newTab) => {
  localStorage.setItem('acc_admin_active_tab', newTab);
  if (route.query.tab !== newTab) {
    router.replace({ query: { ...route.query, tab: newTab } });
  }
}, { immediate: true });

onMounted(async () => {
  await Promise.all([
    courseStore.fetchAdminUsers(),
    courseStore.fetchAdminOrders(),
    courseStore.fetchAdminContacts(),
    courseStore.fetchCourses(),
    courseStore.fetchCategories().catch(() => {}),
    courseStore.fetchPrograms(),
    courseStore.fetchBundles(),
    courseStore.fetchLecturers().catch(() => {}),
    courseStore.fetchAdminBanners().catch(() => {}),
    courseStore.fetchAdminTestimonials().catch(() => {}),
    courseStore.fetchAdminProjects().catch(() => {}),
    courseStore.fetchAdminBlogPosts().catch(() => {})
  ]);
});

const currentTabComponent = computed(() => {
  switch (activeTab.value) {
    case 'overview': return AdminOverview;
    case 'blogs': return AdminBlogs;
    case 'projects': return AdminProjects;
    case 'testimonials': return AdminTestimonials;
    case 'coupons': return AdminCoupons;
    case 'commissions': return AdminCommissions;
    case 'lecturers': return AdminLecturers;
    case 'banners': return AdminBanners;
    case 'categories': return AdminCategories;
    case 'courses': return AdminCourses;
    case 'programs': return AdminPrograms;
    case 'bundles': return AdminBundles;
    case 'orders': return AdminOrders;
    case 'users': return AdminUsers;
    case 'contacts': return AdminContacts;
    default: return AdminOverview;
  }
});
</script>

<style src="@/styles/views/AdminDashboard.css"></style>
