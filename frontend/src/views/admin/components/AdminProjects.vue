<template>
  <div class="tab-content animate-fade-in">
    <!-- SUB-NAV: PROJECTS VS REVIEWS -->
    <div class="sub-nav mb-6" style="display: flex; gap: 10px; border-bottom: 2px solid #e2e8f0; padding-bottom: 12px;">
      <button 
        type="button" 
        @click="subTab = 'projects'" 
        class="btn btn-sm"
        :class="subTab === 'projects' ? 'btn-primary' : 'btn-secondary'"
        style="font-weight: 700; padding: 8px 18px;"
      >
        📂 Quản lý Dự án & Case Study
      </button>

      <button 
        type="button" 
        @click="subTab = 'reviews'" 
        class="btn btn-sm"
        :class="subTab === 'reviews' ? 'btn-primary' : 'btn-secondary'"
        style="font-weight: 700; padding: 8px 18px; display: inline-flex; align-items: center; gap: 6px;"
      >
        <span>⭐ Đánh giá từ Học viên</span>
        <span 
          v-if="pendingReviewsCount > 0" 
          class="badge" 
          style="background: #e11d48; color: #ffffff; font-size: 11px; padding: 2px 7px; border-radius: 10px;"
        >
          {{ pendingReviewsCount }}
        </span>
      </button>
    </div>

    <!-- VIEW 1: PROJECTS MANAGEMENT -->
    <div v-if="subTab === 'projects'">
      <!-- LIST VIEW -->
      <div v-if="activeView === 'list'">
        <div class="content-header flex-between">
          <div>
            <h2>Quản lý Dự án & Case Study Thực tế</h2>
            <p>Danh sách các dự án AI tiêu biểu cho khối Doanh nghiệp, Cá nhân và Cơ quan Nhà nước.</p>
          </div>
          <button @click="openAddModal" class="btn btn-primary btn-sm">+ Thêm Dự án mới</button>
        </div>

        <!-- Filter Bar -->
        <div class="filter-bar flex-between mt-4 mb-4 gap-4" style="flex-wrap: wrap;">
          <div class="filter-tabs" style="display: flex; gap: 8px; margin: 0;">
            <button 
              @click="filterCategory = 'all'" 
              class="btn btn-sm" 
              :class="filterCategory === 'all' ? 'btn-primary' : 'btn-secondary'"
            >
              Tất cả ({{ projects.length }})
            </button>
            <button 
              @click="filterCategory = 'du-an-doanh-nghiep'" 
              class="btn btn-sm" 
              :class="filterCategory === 'du-an-doanh-nghiep' ? 'btn-primary' : 'btn-secondary'"
            >
              Doanh nghiệp ({{ corporateCount }})
            </button>
            <button 
              @click="filterCategory = 'du-an-ca-nhan'" 
              class="btn btn-sm" 
              :class="filterCategory === 'du-an-ca-nhan' ? 'btn-primary' : 'btn-secondary'"
            >
              Cá nhân ({{ personalCount }})
            </button>
            <button 
              @click="filterCategory = 'du-an-nha-nuoc'" 
              class="btn btn-sm" 
              :class="filterCategory === 'du-an-nha-nuoc' ? 'btn-primary' : 'btn-secondary'"
            >
              Cơ quan Nhà nước ({{ govCount }})
            </button>
          </div>

          <div style="min-width: 280px; flex: 1; max-width: 350px;">
            <input 
              v-model="searchQuery" 
              type="text" 
              placeholder="Tìm theo tiêu đề, khách hàng hoặc ID..." 
              class="admin-search-input"
              style="width: 100%;"
            />
          </div>
        </div>

        <!-- Table -->
        <div class="table-responsive">
          <table class="admin-table">
            <thead>
              <tr>
                <th style="width: 60px;">Ảnh</th>
                <th>Tiêu đề & Chuyên mục</th>
                <th>Khách hàng / Tác giả</th>
                <th>Thời gian</th>
                <th style="text-align: right; width: 140px;">Hành động</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="p in paginatedProjects" :key="p.id">
                <td>
                  <img 
                    :src="p.image || '/images/default.png'" 
                    alt="thumb" 
                    style="width: 54px; height: 38px; object-fit: cover; border-radius: 6px; border: 1px solid #cbd5e1;"
                    referrerpolicy="no-referrer"
                  />
                </td>
                <td>
                  <div class="font-bold" style="color: #0f172a; font-size: 14px;">{{ p.title }}</div>
                  <div style="display: flex; gap: 8px; align-items: center; margin-top: 4px;">
                    <span class="badge badge-info" style="font-size: 11.5px;">{{ p.category_name || p.category }}</span>
                    <span class="text-xs text-muted" style="font-size: 11.5px;">ID: {{ p.id }}</span>
                    <router-link :to="'/du-an/' + p.id" target="_blank" style="font-size: 11.5px; color: #0284c7; text-decoration: underline;">
                      Xem chi tiết ↗
                    </router-link>
                  </div>
                </td>
                <td>
                  <div style="font-size: 13.5px; color: #334155;">{{ p.client || 'Chưa cập nhật' }}</div>
                </td>
                <td>
                  <div style="font-size: 13.5px; color: #64748b;">{{ p.date || '--' }}</div>
                </td>
                <td style="text-align: right;">
                  <div class="action-buttons" style="justify-content: flex-end;">
                    <button @click="editProject(p)" class="btn-action edit" title="Sửa">✏️</button>
                    <button @click="deleteItem(p.id)" class="btn-action delete" title="Xóa">🗑️</button>
                  </div>
                </td>
              </tr>
              <tr v-if="filteredProjects.length === 0">
                <td colspan="5" class="text-center py-8 text-muted">Không có dự án nào phù hợp với bộ lọc.</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <Pagination 
          :currentPage="projectsPage" 
          :totalItems="filteredProjects.length" 
          :pageSize="projectsPageSize" 
          @update:currentPage="projectsPage = $event"
          @page-change="projectsPage = $event"
        />
      </div>

      <!-- VIEW 2: FORM ADD/EDIT (Extracted Component) -->
      <ProjectFormView 
        v-else-if="activeView === 'form'"
        :initialData="editingProject"
        @cancel="activeView = 'list'"
        @saved="onProjectSaved"
      />
    </div>

    <!-- VIEW 2: PROJECT REVIEWS MODERATION (Extracted Component) -->
    <ProjectReviewsSection 
      v-else-if="subTab === 'reviews'"
      :projects="projects"
      @update-counts="onReviewsCountsUpdate"
    />
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useCourseStore } from '@/stores/courses';
import Pagination from '@/components/Pagination.vue';
import ProjectFormView from '../modals/ProjectFormView.vue';
import ProjectReviewsSection from '../modals/ProjectReviewsSection.vue';

const courseStore = useCourseStore();

const subTab = ref('projects');
const activeView = ref('list');
const editingProject = ref(null);

const filterCategory = ref('all');
const searchQuery = ref('');
const projectsPage = ref(1);
const projectsPageSize = ref(10);
const pendingReviewsCount = ref(0);

const projects = computed(() => courseStore.adminProjects || []);
const corporateCount = computed(() => projects.value.filter(p => p.category === 'du-an-doanh-nghiep').length);
const personalCount = computed(() => projects.value.filter(p => p.category === 'du-an-ca-nhan').length);
const govCount = computed(() => projects.value.filter(p => p.category === 'du-an-nha-nuoc').length);

const filteredProjects = computed(() => {
  return projects.value.filter(p => {
    if (filterCategory.value !== 'all' && p.category !== filterCategory.value) return false;
    if (searchQuery.value.trim()) {
      const q = searchQuery.value.toLowerCase().trim();
      const matchTitle = p.title && p.title.toLowerCase().includes(q);
      const matchClient = p.client && p.client.toLowerCase().includes(q);
      const matchId = p.id && p.id.toLowerCase().includes(q);
      return matchTitle || matchClient || matchId;
    }
    return true;
  });
});

const paginatedProjects = computed(() => {
  const start = (projectsPage.value - 1) * projectsPageSize.value;
  return filteredProjects.value.slice(start, start + projectsPageSize.value);
});

watch([filterCategory, searchQuery], () => {
  projectsPage.value = 1;
});

const openAddModal = () => {
  editingProject.value = null;
  activeView.value = 'form';
};

const editProject = (p) => {
  editingProject.value = p;
  activeView.value = 'form';
};

const onProjectSaved = () => {
  activeView.value = 'list';
  courseStore.fetchAdminProjects();
};

const deleteItem = async (id) => {
  const isConfirmed = await courseStore.showConfirm({
    title: 'Xác nhận xóa Dự án',
    message: 'Bạn có chắc chắn muốn xóa Case study / Dự án này?',
    confirmText: 'Đồng ý xóa',
    cancelText: 'Hủy bỏ',
    type: 'danger'
  });

  if (isConfirmed) {
    try {
      await courseStore.deleteAdminProject(id);
    } catch (err) {
      console.error("Delete project error:", err);
    }
  }
};

const onReviewsCountsUpdate = (counts) => {
  pendingReviewsCount.value = counts.pending;
};

onMounted(async () => {
  try {
    await courseStore.fetchAdminProjects();
  } catch (err) {
    console.error("Error loading admin projects:", err);
  }
});
</script>

<style scoped src="@/styles/views/admin/AdminProjects.css"></style>
