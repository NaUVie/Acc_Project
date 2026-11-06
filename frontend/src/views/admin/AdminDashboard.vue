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
              <HelpTooltip 
                desc="Trung tâm điều khiển: 6 chỉ số KPI và 2 bảng tác vụ ưu tiên trong ngày." 
                impact="Phản ánh số liệu thời gian thực từ mọi tương tác của học viên trên website." 
                position="right"
              />
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
                <HelpTooltip 
                  v-if="tab.desc" 
                  :desc="tab.desc" 
                  :impact="tab.impact"
                  position="right"
                />
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
                <HelpTooltip 
                  v-if="tab.desc" 
                  :desc="tab.desc" 
                  :impact="tab.impact"
                  position="right"
                />
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
                <HelpTooltip 
                  v-if="tab.desc" 
                  :desc="tab.desc" 
                  :impact="tab.impact"
                  position="right"
                />
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
import HelpTooltip from '@/components/common/HelpTooltip.vue';

const route = useRoute();
const router = useRouter();
const courseStore = useCourseStore();

// Tab navigation phân theo nhóm logic kèm giải thích công dụng
const studentTabs = [
  { 
    id: 'contacts', 
    name: 'Liên hệ tư vấn',
    desc: 'Tiếp nhận và gọi điện tư vấn cho các học viên để lại thông tin.',
    impact: 'Kết nối trực tiếp với Form tư vấn ở chân Trang chủ và trang khóa học.'
  },
  { 
    id: 'users', 
    name: 'Học viên & Người dùng',
    desc: 'Quản lý tài khoản học viên, đổi mật khẩu và cấp quyền khóa học.',
    impact: 'Đồng bộ với Cổng học viên cá nhân /dashboard.'
  }
];

const educationTabs = [
  { 
    id: 'categories', 
    name: 'Chuyên mục',
    desc: 'Quản lý các nhóm chuyên đề đào tạo (Doanh nghiệp, Cá nhân, Nhà nước).',
    impact: 'Hiển thị trên Mega Menu Header và Tabs lọc khóa học Trang chủ.'
  },
  { 
    id: 'courses', 
    name: 'Khóa học',
    desc: 'Quản lý danh sách khóa học nhận tư vấn, lộ trình và đề cương bài giảng.',
    impact: 'Hiển thị tại Section 6 Khóa học Tiêu biểu Trang chủ.'
  },
  { 
    id: 'lecturers', 
    name: 'Giảng viên & Chuyên gia',
    desc: 'Quản lý hồ sơ giảng viên, học hàm học vị, chức danh và tiểu sử.',
    impact: 'Hiển thị tại Section 8 Đội ngũ Giảng viên Trang chủ.'
  },
  { 
    id: 'board-members', 
    name: 'Ban điều hành & Cố vấn',
    desc: 'Quản lý thành viên hội đồng cố vấn chiến lược và ban lãnh đạo.',
    impact: 'Hiển thị tại trang Giới thiệu / Về chúng tôi.'
  },
  { 
    id: 'admissions', 
    name: 'Bài viết Tuyển sinh',
    desc: 'Đăng các thông báo chiêu sinh, lịch khai giảng và học bổng mới.',
    impact: 'Liên kết tới nút Tuyển sinh trên Header và trang /admissions.'
  }
];

const marketingTabs = [
  { 
    id: 'banners', 
    name: 'Banner & Video Trang chủ',
    desc: 'Quản lý slide ảnh bìa, câu slogan, nút CTA và video YouTube.',
    impact: 'Hiển thị tại Section 1 & Section 3 trên Trang chủ.'
  },
  { 
    id: 'blogs', 
    name: 'Tin tức & Bài viết',
    desc: 'Soạn thảo bài viết chuyên môn, cẩm nang quản trị tăng SEO.',
    impact: 'Hiển thị tại Thư viện Cẩm nang tri thức /library/blog.'
  },
  { 
    id: 'testimonials', 
    name: 'Cảm nhận học viên',
    desc: 'Kiểm duyệt nhận xét, phê duyệt hoặc đánh dấu spam.',
    impact: 'Chỉ bài ĐÃ DUYỆT mới xuất hiện tại Section 9 Trang chủ.'
  },
  { 
    id: 'partners', 
    name: 'Doanh nghiệp hợp tác',
    desc: 'Quản lý logo đối tác doanh nghiệp (chạy marquee hoặc cố định).',
    impact: 'Hiển thị tại Section 4 ngay dưới banner Trang chủ.'
  }
];

const tabs = [
  { id: 'overview', name: 'Tổng quan' },
  ...studentTabs,
  ...educationTabs,
  ...marketingTabs
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
  marketing: marketingTabs.some(t => t.id === activeTab.value)
});

const toggleGroup = (group) => {
  openGroups.value[group] = !openGroups.value[group];
};

watch(activeTab, (newTab) => {
  if (studentTabs.some(t => t.id === newTab)) openGroups.value.students = true;
  if (educationTabs.some(t => t.id === newTab)) openGroups.value.education = true;
  if (marketingTabs.some(t => t.id === newTab)) openGroups.value.marketing = true;
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
