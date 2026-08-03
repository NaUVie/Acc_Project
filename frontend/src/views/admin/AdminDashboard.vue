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
import { ref, computed, onMounted } from 'vue';
import { useCourseStore } from '@/stores/courses';

// Import modular tab components
import AdminOverview from './components/AdminOverview.vue';
import AdminOrders from './components/AdminOrders.vue';
import AdminUsers from './components/AdminUsers.vue';
import AdminContacts from './components/AdminContacts.vue';
import AdminCourses from './components/AdminCourses.vue';

const courseStore = useCourseStore();

onMounted(async () => {
  await Promise.all([
    courseStore.fetchAdminUsers(),
    courseStore.fetchAdminOrders(),
    courseStore.fetchAdminContacts(),
    courseStore.fetchCourses()
  ]);
});

// Setup Tab navigation
const tabs = [
  { id: 'overview', name: 'Tổng quan', icon: '📊' },
  { id: 'orders', name: 'Đơn hàng', icon: '📦' },
  { id: 'users', name: 'Học viên', icon: '👥' },
  { id: 'contacts', name: 'Liên hệ', icon: '✉️' },
  { id: 'courses', name: 'Khóa học', icon: '📚' }
];

const activeTab = ref('overview');

const currentTabComponent = computed(() => {
  switch (activeTab.value) {
    case 'overview': return AdminOverview;
    case 'orders': return AdminOrders;
    case 'users': return AdminUsers;
    case 'contacts': return AdminContacts;
    case 'courses': return AdminCourses;
    default: return AdminOverview;
  }
});
</script>

<style src="@/styles/views/AdminDashboard.css"></style>
