<template>
  <div class="admin-view container">
    <!-- MOBILE ADMIN HEADER (Visible on screens <= 992px) -->
      <div class="admin-mobile-top-bar">
        <div class="admin-mobile-title-box">
          <span class="admin-mobile-logo">ACC ADMIN</span>
          <span class="admin-mobile-active-tag">
            <span class="tab-dot"></span>
            {{ currentTabName }}
          </span>
        </div>
        <button 
          class="admin-mobile-toggle-btn" 
          @click="isMobileMenuOpen = !isMobileMenuOpen"
        >
          <span>{{ isMobileMenuOpen ? '✕ Đóng menu' : '☰ Danh mục quản trị' }}</span>
        </button>
      </div>

      <!-- SIDEBAR NAV -->
    <div class="admin-layout glass-card animate-fade-in">
      <aside class="admin-sidebar" :class="{ 'mobile-open': isMobileMenuOpen }">
        <div class="sidebar-header">
          <span class="admin-logo-badge">ACC ADMIN</span>
          <p class="admin-subtitle">Hệ thống quản trị vận hành</p>
        </div>
        <nav class="sidebar-menu">
          <div class="menu-group">
            <button 
              class="sidebar-menu-item"
              :class="{ active: activeTab === 'overview' }"
              @click="selectTab('overview')"
            >
              <span class="menu-label">Tổng quan</span>
            </button>
          </div>

          <!-- Nhóm 1: Học viên & Tuyển sinh -->
          <div class="accordion-group">
            <button class="accordion-header" :class="{ 'has-active': studentTabs.some(t => t.id === activeTab) }" @click="toggleGroup('students')">
              <span class="accordion-title">Học viên & Tuyển sinh</span>
              <span class="accordion-arrow" :class="{ open: openGroups.students }">▾</span>
            </button>
            <div v-show="openGroups.students" class="accordion-body">
              <button 
                v-for="tab in studentTabs" 
                :key="tab.id"
                class="sidebar-menu-item sub-item"
                :class="{ active: activeTab === tab.id }"
                @click="selectTab(tab.id)"
              >
                <span class="menu-label">{{ tab.name }}</span>
              </button>
            </div>
          </div>

          <!-- Nhóm 2: Đào tạo & Khóa học -->
          <div class="accordion-group">
            <button class="accordion-header" :class="{ 'has-active': educationTabs.some(t => t.id === activeTab) }" @click="toggleGroup('education')">
              <span class="accordion-title">Đào tạo & Khóa học</span>
              <span class="accordion-arrow" :class="{ open: openGroups.education }">▾</span>
            </button>
            <div v-show="openGroups.education" class="accordion-body">
              <button 
                v-for="tab in educationTabs" 
                :key="tab.id"
                class="sidebar-menu-item sub-item"
                :class="{ active: activeTab === tab.id }"
                @click="selectTab(tab.id)"
              >
                <span class="menu-label">{{ tab.name }}</span>
              </button>
            </div>
          </div>

          <!-- Nhóm 3: Marketing & Nội dung Website -->
          <div class="accordion-group">
            <button class="accordion-header" :class="{ 'has-active': marketingTabs.some(t => t.id === activeTab) }" @click="toggleGroup('marketing')">
              <span class="accordion-title">Marketing & Nội dung</span>
              <span class="accordion-arrow" :class="{ open: openGroups.marketing }">▾</span>
            </button>
            <div v-show="openGroups.marketing" class="accordion-body">
              <button 
                v-for="tab in marketingTabs" 
                :key="tab.id"
                class="sidebar-menu-item sub-item"
                :class="{ active: activeTab === tab.id }"
                @click="selectTab(tab.id)"
              >
                <span class="menu-label">{{ tab.name }}</span>
              </button>
            </div>
          </div>

          <!-- Nhóm 4: Giao dịch & Đơn hàng (Lưu trữ) -->
          <div class="accordion-group">
            <button class="accordion-header" :class="{ 'has-active': transactionTabs.some(t => t.id === activeTab) }" @click="toggleGroup('transactions')">
              <span class="accordion-title">Đơn hàng & Giao dịch</span>
              <span class="accordion-arrow" :class="{ open: openGroups.transactions }">▾</span>
            </button>
            <div v-show="openGroups.transactions" class="accordion-body">
              <button 
                v-for="tab in transactionTabs" 
                :key="tab.id"
                class="sidebar-menu-item sub-item"
                :class="{ active: activeTab === tab.id }"
                @click="selectTab(tab.id)"
              >
                <span class="menu-label">{{ tab.name }}</span>
              </button>
            </div>
          </div>
        </nav>
        <div class="sidebar-footer">
          <router-link to="/" class="btn btn-outline btn-sm w-full text-center" @click="isMobileMenuOpen = false">
            &larr; Về Trang chủ
          </router-link>
        </div>
      </aside>

      <!-- MAIN CONTENT PANEL -->
      <main class="admin-main">
        <div v-if="isTabSwitching" class="admin-loading-bar"></div>
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
import AdminBanners from './components/AdminBanners.vue';
import AdminCoupons from './components/AdminCoupons.vue';
import AdminCommissions from './components/AdminCommissions.vue';
import AdminLecturers from './components/AdminLecturers.vue';
import AdminTestimonials from './components/AdminTestimonials.vue';
import AdminBlogs from './components/AdminBlogs.vue';
import AdminPartners from './components/AdminPartners.vue';
import AdminBoardMembers from './components/AdminBoardMembers.vue';
import AdminAdmissions from './components/AdminAdmissions.vue';

const route = useRoute();
const router = useRouter();
const courseStore = useCourseStore();

// Tab navigation phân theo nhóm logic
const studentTabs = [
  { id: 'contacts', name: 'Liên hệ tư vấn' },
  { id: 'users', name: 'Học viên & Người dùng' }
];

const educationTabs = [
  { id: 'categories', name: 'Chuyên mục' },
  { id: 'courses', name: 'Khóa học' },
  { id: 'lecturers', name: 'Giảng viên & Chuyên gia' },
  { id: 'board-members', name: 'Ban điều hành & Cố vấn' },
  { id: 'admissions', name: 'Bài viết Tuyển sinh' }
];

const marketingTabs = [
  { id: 'banners', name: 'Banner & Video Trang chủ' },
  { id: 'blogs', name: 'Tin tức & Bài viết' },
  { id: 'testimonials', name: 'Cảm nhận học viên' },
  { id: 'partners', name: 'Doanh nghiệp hợp tác' }
];

const transactionTabs = [
  { id: 'orders', name: 'Lịch sử đơn cũ' },
  { id: 'coupons', name: 'Mã giảm giá' },
];

const tabs = [
  { id: 'overview', name: 'Tổng quan' },
  ...studentTabs,
  ...educationTabs,
  ...marketingTabs,
  ...transactionTabs
];

const getInitialTab = () => {
  const queryTab = route.query.tab;
  if (queryTab && tabs.some(t => t.id === queryTab)) {
    return queryTab;
  }
  return 'overview';
};

const activeTab = ref(getInitialTab());
const isMobileMenuOpen = ref(false);

const currentTabName = computed(() => {
  const found = tabs.find(t => t.id === activeTab.value);
  return found ? found.name : 'Tổng quan';
});

const selectTab = (tabId) => {
  activeTab.value = tabId;
  isMobileMenuOpen.value = false;
};

const isTabSwitching = ref(false);
let tabSwitchTimer = null;

const openGroups = ref({
  students: studentTabs.some(t => t.id === activeTab.value),
  education: educationTabs.some(t => t.id === activeTab.value),
  marketing: marketingTabs.some(t => t.id === activeTab.value),
  transactions: transactionTabs.some(t => t.id === activeTab.value)
});

const toggleGroup = (group) => {
  openGroups.value[group] = !openGroups.value[group];
};

watch(activeTab, (newTab) => {
  if (studentTabs.some(t => t.id === newTab)) openGroups.value.students = true;
  if (educationTabs.some(t => t.id === newTab)) openGroups.value.education = true;
  if (marketingTabs.some(t => t.id === newTab)) openGroups.value.marketing = true;
  if (transactionTabs.some(t => t.id === newTab)) openGroups.value.transactions = true;
});

watch(() => route.query.tab, (newTab) => {
  if (newTab && tabs.some(t => t.id === newTab) && newTab !== activeTab.value) {
    activeTab.value = newTab;
  }
});

watch(activeTab, (newTab) => {
  isTabSwitching.value = true;
  if (tabSwitchTimer) clearTimeout(tabSwitchTimer);
  tabSwitchTimer = setTimeout(() => { isTabSwitching.value = false; }, 380);

  localStorage.setItem('acc_admin_active_tab', newTab);
  if (route.query.tab !== newTab) {
    router.replace({ query: { ...route.query, tab: newTab } });
  }
}, { immediate: true });

// Preload core metrics for Overview and Business/Customer group on arrival
onMounted(() => {
  courseStore.fetchAdminUsers().catch(() => {});
  courseStore.fetchAdminOrders().catch(() => {});
  courseStore.fetchAdminContacts().catch(() => {});
});

const currentTabComponent = computed(() => {
  switch (activeTab.value) {
    case 'overview': return AdminOverview;
    case 'partners': return AdminPartners;
    case 'blogs': return AdminBlogs;
    case 'testimonials': return AdminTestimonials;
    case 'coupons': return AdminCoupons;
    case 'commissions': return AdminCommissions;
    case 'lecturers': return AdminLecturers;
    case 'board-members': return AdminBoardMembers;
    case 'admissions': return AdminAdmissions;
    case 'banners': return AdminBanners;
    case 'categories': return AdminCategories;
    case 'courses': return AdminCourses;
            case 'orders': return AdminOrders;
    case 'users': return AdminUsers;
    case 'contacts': return AdminContacts;
    default: return AdminOverview;
  }
});
</script>

<style src="@/styles/views/AdminDashboard.css"></style>
