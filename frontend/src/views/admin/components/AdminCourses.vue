<template>
  <div class="tab-content animate-fade-in">
    <!-- VIEW 1: COURSES LIST TABLE -->
    <div v-if="activeView === 'list'">
      <div class="content-header flex-between">
        <div>
          <h2>Quản lý Khóa học & Giáo trình</h2>
          <p>Danh sách các khóa học đào tạo, bài giảng và giáo trình trên toàn hệ thống.</p>
        </div>
        <div style="display: flex; gap: 10px; align-items: center;">
          <button @click="refreshCourses" :disabled="isRefreshing" class="btn btn-secondary btn-sm" style="display: flex; align-items: center; gap: 6px; font-weight: 600;" title="Tải lại danh sách mới nhất từ máy chủ">
            <span :class="{ 'spin-icon': isRefreshing }">🔄</span>
            <span>{{ isRefreshing ? 'Đang đồng bộ...' : 'Làm mới dữ liệu' }}</span>
          </button>
          <button @click="openAddCourse" class="btn btn-primary btn-sm">+ Thêm khóa học mới</button>
        </div>
      </div>

      <!-- Search & Category Filter Bar -->
      <div class="filter-bar mt-4" style="display: flex; gap: 12px; align-items: center; justify-content: space-between; flex-wrap: wrap;">
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="Tìm theo tên khóa học, mã đường dẫn tĩnh..." 
          class="admin-search-input"
          style="flex: 1; min-width: 240px;"
        />
        
        <!-- Filter by Category -->
        <div style="display: flex; align-items: center; gap: 8px; font-size: 13px; color: #475569; font-weight: 600;">
          <span>Chuyên mục:</span>
          <select v-model="selectedCategoryFilter" class="admin-input-style" style="padding: 6px 12px; border-radius: 8px; border: 1px solid #cbd5e1; background: #ffffff; color: #0f172a; cursor: pointer; max-width: 250px;">
            <option value="all">Tất cả chuyên mục ({{ courses.length }})</option>
            <option v-for="cat in categories" :key="cat.slug" :value="cat.slug">
              {{ cat.name }} ({{ getCategoryCoursesCount(cat.slug) }})
            </option>
          </select>
        </div>
      </div>

      <!-- Filter by Event Status (Sắp diễn ra / Đang diễn ra / Đã diễn ra) -->
      <div class="status-tabs-container mt-3" style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap;">
        <span style="font-size: 13px; font-weight: 700; color: #475569; margin-right: 4px;">Trạng thái:</span>
        <button 
          type="button" 
          class="btn btn-sm" 
          :class="selectedStatusFilter === 'all' ? 'btn-primary' : 'btn-secondary'"
          @click="selectedStatusFilter = 'all'"
          style="font-weight: 600; border-radius: 20px; padding: 5px 14px;"
        >
          Tất cả ({{ courses.length }})
        </button>
        <button 
          type="button" 
          class="btn btn-sm" 
          :class="selectedStatusFilter === 'upcoming' ? 'btn-status-filter-upcoming-active' : 'btn-secondary'"
          @click="selectedStatusFilter = 'upcoming'"
          style="font-weight: 600; border-radius: 20px; padding: 5px 14px;"
        >
          ⏳ Sắp diễn ra ({{ countByStatus('upcoming') }})
        </button>
        <button 
          type="button" 
          class="btn btn-sm" 
          :class="selectedStatusFilter === 'ongoing' ? 'btn-status-filter-ongoing-active' : 'btn-secondary'"
          @click="selectedStatusFilter = 'ongoing'"
          style="font-weight: 600; border-radius: 20px; padding: 5px 14px;"
        >
          🟢 Đang diễn ra ({{ countByStatus('ongoing') }})
        </button>
        <button 
          type="button" 
          class="btn btn-sm" 
          :class="selectedStatusFilter === 'completed' ? 'btn-status-filter-completed-active' : 'btn-secondary'"
          @click="selectedStatusFilter = 'completed'"
          style="font-weight: 600; border-radius: 20px; padding: 5px 14px;"
        >
          🏁 Đã diễn ra ({{ countByStatus('completed') }})
        </button>
      </div>

      <div class="table-responsive mt-6">
        <table class="admin-table">
          <thead>
            <tr>
              <th style="width: 60px;">Ảnh</th>
              <th>Tên khóa học</th>
              <th>Chuyên mục</th>
              <th>Trạng thái</th>
              <th>Thời lượng</th>
              <th>Hành động</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="c in paginatedCourses" :key="c.id">
              <td data-label="Ảnh">
                <img :src="c.image || '/images/default.jpg'" :alt="c.title" style="width: 48px; height: 36px; border-radius: 4px; object-fit: cover;" />
              </td>
              <td data-label="Tên khóa học">
                <div class="font-bold" style="color: #0f172a;">{{ c.title }}</div>
                <div class="text-xs text-muted">/khoa-hoc/{{ c.handle }}</div>
              </td>
              <td data-label="Chuyên mục">
                <span class="badge badge-info">{{ getCategoryName(c.category) }}</span>
              </td>
              <td data-label="Trạng thái">
                <select 
                  :value="c.status || 'ongoing'" 
                  @change="handleQuickStatusChange(c, $event.target.value)"
                  class="admin-course-status-select"
                  :class="'select-status-' + (c.status || 'ongoing')"
                  title="Nhấp để chuyển trực tiếp trạng thái của khóa học"
                >
                  <option value="upcoming">⏳ Sắp diễn ra</option>
                  <option value="ongoing">🟢 Đang diễn ra</option>
                  <option value="completed">🏁 Đã diễn ra</option>
                </select>
              </td>
              <td data-label="Thời lượng">{{ c.duration || 'N/A' }}</td>
              <td data-label="Hành động">
                <div class="action-buttons">
                  <button @click="editCourse(c)" class="btn-action edit" title="Sửa thông tin">✏️</button>
                  <button @click="deleteCourse(c.id)" class="btn-action delete" title="Xóa">🗑️</button>
                </div>
              </td>
            </tr>
            <tr v-if="isLoadingCourses && filteredCourses.length === 0">
              <td colspan="6">
                <div class="admin-center-loader" style="padding: 40px 0; min-height: 160px;">
                  <div class="admin-spinner"></div>
                  <p class="admin-loader-text">Đang nạp danh sách khóa học...</p>
                </div>
              </td>
            </tr>
            <tr v-else-if="filteredCourses.length === 0">
              <td colspan="6" class="text-center py-8 text-muted">Không tìm thấy khóa học nào phù hợp.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination Component -->
      <Pagination 
        :currentPage="currentPage" 
        :totalItems="filteredCourses.length" 
        :pageSize="pageSize" 
        @update:currentPage="currentPage = $event"
      />
    </div>

    <!-- VIEW 2: COURSE ADD/EDIT FORM (Extracted Component) -->
    <CourseFormView 
      v-else-if="activeView === 'course_form'"
      :initialData="editingCourse"
      :categories="categories"
      :lecturers="lecturers"
      :courses="courses"
      @cancel="activeView = 'list'"
      @saved="onCourseSaved"
    />

    <!-- VIEW 3: CURRICULUM FORM (Extracted Component) -->
    <CourseCurriculumView 
      v-else-if="activeView === 'curriculum_form'"
      :course="selectedCourseForCurriculum"
      @cancel="activeView = 'list'"
      @saved="activeView = 'list'"
    />
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useCourseStore } from '@/stores/courses';
import Pagination from '@/components/Pagination.vue';
import CourseFormView from '../modals/CourseFormView.vue';
import CourseCurriculumView from '../modals/CourseCurriculumView.vue';

const courseStore = useCourseStore();
const isLoadingCourses = ref(courseStore.courses.length === 0);
const isRefreshing = ref(false);

const refreshCourses = async () => {
  isRefreshing.value = true;
  try {
    await courseStore.fetchCourses(true);
    await courseStore.fetchCategories(true);
    courseStore.showToast('Đã làm mới và đồng bộ dữ liệu khóa học mới nhất từ máy chủ!', 'success');
  } catch (err) {
    courseStore.showToast('Lỗi khi làm mới dữ liệu: ' + err.message, 'error');
  } finally {
    isRefreshing.value = false;
  }
};

const activeView = ref('list');
const editingCourse = ref(null);
const selectedCourseForCurriculum = ref(null);

const searchQuery = ref('');
const selectedCategoryFilter = ref('all');
const selectedStatusFilter = ref('all');
const currentPage = ref(1);

const countByStatus = (st) => {
  return courses.value.filter(c => (c.status || 'ongoing') === st).length;
};

const getStatusLabel = (st) => {
  if (st === 'upcoming') return 'Sắp diễn ra';
  if (st === 'completed') return 'Đã diễn ra';
  return 'Đang diễn ra';
};

const handleQuickStatusChange = async (course, newStatus) => {
  try {
    await courseStore.updateAdminCourse(course.id, {
      ...course,
      status: newStatus
    });
    course.status = newStatus;
    courseStore.showToast(`Đã chuyển khóa học sang "${getStatusLabel(newStatus)}"`, 'success');
  } catch (err) {
    courseStore.showToast('Lỗi khi đổi trạng thái: ' + (err.message || err), 'error');
  }
};
const pageSize = ref(8);

const courses = computed(() => courseStore.courses || []);
const categories = computed(() => courseStore.categories || []);
const lecturers = computed(() => courseStore.lecturers || []);

const formatCurrency = (val) => {
  if (!val) return '0 ₫';
  return Number(val).toLocaleString('vi-VN') + ' ₫';
};

const getCategoryName = (catSlug) => {
  const cat = categories.value.find(c => c.slug === catSlug);
  return cat ? cat.name : catSlug;
};

const getCategoryCoursesCount = (slug) => {
  return courses.value.filter(c => c.category === slug).length;
};

const filteredCourses = computed(() => {
  let list = courses.value;
  if (selectedCategoryFilter.value !== 'all') {
    list = list.filter(c => c.category === selectedCategoryFilter.value);
  }
  if (selectedStatusFilter.value !== 'all') {
    list = list.filter(c => (c.status || 'ongoing') === selectedStatusFilter.value);
  }
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase().trim();
    list = list.filter(c => 
      c.title.toLowerCase().includes(q) || 
      (c.handle && c.handle.toLowerCase().includes(q))
    );
  }
  return list;
});

const paginatedCourses = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  return filteredCourses.value.slice(start, start + pageSize.value);
});

watch([selectedCategoryFilter, selectedStatusFilter, searchQuery], () => {
  currentPage.value = 1;
});

const openAddCourse = () => {
  editingCourse.value = null;
  activeView.value = 'course_form';
};

const editCourse = (c) => {
  editingCourse.value = c;
  activeView.value = 'course_form';
};

const openCurriculum = (c) => {
  selectedCourseForCurriculum.value = c;
  activeView.value = 'curriculum_form';
};

const onCourseSaved = () => {
  activeView.value = 'list';
};

const deleteCourse = async (courseId) => {
  const c = courses.value.find(item => item.id === courseId);
  const title = c ? c.title : '';

  const isConfirmed = await courseStore.showConfirm({
    title: 'Xác nhận xóa khóa học',
    message: `Bạn có chắc chắn muốn xóa khóa học "${title}" khỏi hệ thống?\n\nHệ thống sẽ đồng thời dọn dẹp các dữ liệu liên quan (học viên, đánh giá, ghi chú, giỏ hàng...).`,
    confirmText: 'Đồng ý xóa',
    cancelText: 'Hủy bỏ',
    type: 'danger'
  });

  if (isConfirmed) {
    try {
      await courseStore.deleteAdminCourse(courseId);
      courseStore.showToast(`Đã xóa khóa học "${title}" thành công.`, 'success');
    } catch (err) {
      courseStore.showToast(err.message || 'Không thể xóa khóa học.', 'error');
    }
  }
};

onMounted(async () => {
  try {
    const promises = [];
    if (courses.value.length === 0) promises.push(courseStore.fetchCourses());
    if (categories.value.length === 0) promises.push(courseStore.fetchCategories());
    if (lecturers.value.length === 0) promises.push(courseStore.fetchLecturers());
    if (promises.length > 0) await Promise.all(promises);
  } finally {
    isLoadingCourses.value = false;
  }
});
</script>

<style scoped>
.spin-icon {
  display: inline-block;
  animation: spinCourse 0.8s linear infinite;
}
@keyframes spinCourse {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Status Tabs & Select Styles */
.btn-status-filter-upcoming-active {
  background: #f59e0b !important;
  color: #ffffff !important;
  border-color: #d97706 !important;
  box-shadow: 0 2px 6px rgba(245, 158, 11, 0.35);
}
.btn-status-filter-ongoing-active {
  background: #10b981 !important;
  color: #ffffff !important;
  border-color: #059669 !important;
  box-shadow: 0 2px 6px rgba(16, 185, 129, 0.35);
}
.btn-status-filter-completed-active {
  background: #64748b !important;
  color: #ffffff !important;
  border-color: #475569 !important;
  box-shadow: 0 2px 6px rgba(100, 116, 139, 0.35);
}

.admin-course-status-select {
  padding: 5px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  border: 1px solid #cbd5e1;
  outline: none;
  transition: all 0.2s ease;
  white-space: nowrap;
}
.admin-course-status-select:hover {
  filter: brightness(0.95);
}
.admin-course-status-select.select-status-upcoming {
  background: #fef3c7;
  color: #b45309;
  border-color: #fcd34d;
}
.admin-course-status-select.select-status-ongoing {
  background: #ecfdf5;
  color: #047857;
  border-color: #6ee7b7;
}
.admin-course-status-select.select-status-completed {
  background: #f1f5f9;
  color: #475569;
  border-color: #cbd5e1;
}

</style>
