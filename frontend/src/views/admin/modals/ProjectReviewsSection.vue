<template>
  <div>
    <div class="content-header flex-between mb-4">
      <div>
        <h2 style="font-size: 20px; font-weight: 800; color: #022b9f; margin-bottom: 4px;">
          Quản lý Đánh giá & Nhận xét Dự án
        </h2>
        <p style="color: #64748b; font-size: 13.5px; margin: 0;">
          Phê duyệt, kiểm duyệt và quản lý các phản hồi thực tế từ học viên cho các Case Study / Dự án.
        </p>
      </div>
      <button @click="loadAdminReviews" class="btn btn-secondary btn-sm" :disabled="loadingReviews">
        <span>🔄 Làm mới</span>
      </button>
    </div>

    <!-- Review Filter Controls -->
    <div class="filter-bar flex-between mb-4" style="gap: 12px; flex-wrap: wrap;">
      <div style="display: flex; gap: 8px;">
        <button 
          @click="reviewStatusFilter = 'all'" 
          class="btn btn-sm" 
          :class="reviewStatusFilter === 'all' ? 'btn-primary' : 'btn-secondary'"
        >
          Tất cả ({{ allProjectReviews.length }})
        </button>
        <button 
          @click="reviewStatusFilter = 'pending'" 
          class="btn btn-sm" 
          :class="reviewStatusFilter === 'pending' ? 'btn-primary' : 'btn-secondary'"
        >
          Chờ duyệt ({{ pendingReviewsCount }})
        </button>
        <button 
          @click="reviewStatusFilter = 'approved'" 
          class="btn btn-sm" 
          :class="reviewStatusFilter === 'approved' ? 'btn-primary' : 'btn-secondary'"
        >
          Đã duyệt ({{ approvedReviewsCount }})
        </button>
      </div>

      <div style="min-width: 260px;">
        <select v-model="reviewProjectFilter" class="admin-input-style" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;">
          <option value="all">-- Lọc theo tất cả dự án --</option>
          <option v-for="p in projects" :key="p.id" :value="p.id">
            {{ p.title }}
          </option>
        </select>
      </div>
    </div>

    <!-- Reviews Table -->
    <div class="table-responsive">
      <table class="admin-table">
        <thead>
          <tr>
            <th style="width: 160px;">Học viên</th>
            <th style="width: 200px;">Dự án</th>
            <th style="width: 90px;">Đánh giá</th>
            <th>Nội dung nhận xét</th>
            <th style="width: 130px;">Trạng thái</th>
            <th style="width: 140px;">Hành động</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="rev in paginatedAdminReviews" :key="rev.id">
            <td>
              <div class="font-bold" style="color: #0f172a;">{{ rev.author_name }}</div>
              <small class="text-muted" style="display: block; font-size: 11.5px; color: #64748b;">
                {{ rev.author_email || 'Không có email' }}
              </small>
              <small class="text-muted" style="display: block; font-size: 11px; margin-top: 2px;">
                {{ formatReviewDate(rev.created_at) }}
              </small>
            </td>
            <td>
              <span class="font-bold" style="color: #022b9f; font-size: 13.5px; display: block;">
                {{ getProjectTitle(rev.project_id) }}
              </span>
              <router-link :to="'/du-an/' + rev.project_id" target="_blank" style="font-size: 12px; color: #0284c7; text-decoration: underline;">
                Xem trang dự án
              </router-link>
            </td>
            <td>
              <span style="color: #f59e0b; font-weight: 700;">
                ★ {{ rev.rating }}/5
              </span>
            </td>
            <td>
              <div class="admin-review-comment-box">
                <p class="admin-review-comment-excerpt">
                  {{ rev.comment }}
                </p>
                <button 
                  type="button" 
                  @click="selectedReviewDetail = rev" 
                  class="btn-view-review-detail"
                >
                  Xem chi tiết
                </button>
              </div>
            </td>
            <td>
              <span 
                class="badge" 
                :style="rev.is_approved ? 'background: #d1fae5; color: #065f46; font-weight: 700;' : 'background: #fef3c7; color: #92400e; font-weight: 700;'"
              >
                {{ rev.is_approved ? 'Đã hiển thị' : 'Chờ phê duyệt' }}
              </span>
            </td>
            <td>
              <div class="action-buttons" style="gap: 6px;">
                <button 
                  @click="handleToggleApproval(rev)" 
                  class="btn btn-sm"
                  :class="rev.is_approved ? 'btn-secondary' : 'btn-primary'"
                  style="padding: 4px 10px; font-size: 12px;"
                  :title="rev.is_approved ? 'Bấm để ẩn nhận xét' : 'Bấm để duyệt hiển thị nhận xét'"
                >
                  {{ rev.is_approved ? 'Ẩn' : 'Duyệt' }}
                </button>
                <button 
                  @click="handleDeleteReview(rev.id)" 
                  class="btn btn-sm" 
                  style="padding: 4px 8px; font-size: 12px; background: #fee2e2; color: #b91c1c;"
                  title="Xóa nhận xét"
                >
                  Xóa
                </button>
              </div>
            </td>
          </tr>
          <tr v-if="filteredProjectReviews.length === 0">
            <td colspan="6" class="text-center py-8 text-muted">
              {{ loadingReviews ? 'Đang tải danh sách nhận xét...' : 'Không có nhận xét nào phù hợp bộ lọc.' }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination for Admin Reviews -->
    <div class="mt-6 flex-between" style="flex-wrap: wrap; gap: 14px;" v-if="filteredProjectReviews.length > 0">
      <span style="font-size: 13px; color: #64748b;">
        Hiển thị {{ paginatedAdminReviews.length }} / {{ filteredProjectReviews.length }} nhận xét (Trang {{ adminReviewsPage }})
      </span>
      <Pagination 
        :currentPage="adminReviewsPage" 
        :totalItems="filteredProjectReviews.length" 
        :pageSize="adminReviewsPageSize" 
        @update:currentPage="adminReviewsPage = $event"
        @page-change="adminReviewsPage = $event"
      />
    </div>

    <!-- Review Detail Modal in Admin -->
    <div v-if="selectedReviewDetail" class="admin-modal-overlay animate-fade-in" @click.self="selectedReviewDetail = null">
      <div class="admin-modal-box">
        <div class="admin-modal-header">
          <h3>Chi tiết nhận xét của học viên</h3>
          <button @click="selectedReviewDetail = null" class="btn-modal-close">✕</button>
        </div>
        <div class="admin-modal-body">
          <div class="review-detail-meta-grid">
            <div>
              <span class="meta-label">Người gửi:</span>
              <strong>{{ selectedReviewDetail.author_name }}</strong>
            </div>
            <div>
              <span class="meta-label">Email:</span>
              <span>{{ selectedReviewDetail.author_email || 'Chưa cung cấp' }}</span>
            </div>
            <div>
              <span class="meta-label">Dự án:</span>
              <strong style="color: #022b9f;">{{ getProjectTitle(selectedReviewDetail.project_id) }}</strong>
            </div>
            <div>
              <span class="meta-label">Thời gian:</span>
              <span>{{ formatReviewDate(selectedReviewDetail.created_at) }}</span>
            </div>
            <div>
              <span class="meta-label">Đánh giá sao:</span>
              <span style="color: #f59e0b; font-weight: 700; font-size: 15px;">
                ★ {{ selectedReviewDetail.rating }}/5 Sao
              </span>
            </div>
            <div>
              <span class="meta-label">Trạng thái:</span>
              <span 
                class="badge" 
                :style="selectedReviewDetail.is_approved ? 'background: #d1fae5; color: #065f46; font-weight: 700;' : 'background: #fef3c7; color: #92400e; font-weight: 700;'"
              >
                {{ selectedReviewDetail.is_approved ? 'Đã hiển thị công khai' : 'Đang chờ phê duyệt' }}
              </span>
            </div>
          </div>

          <div class="review-detail-content-section mt-4">
            <span class="meta-label" style="display: block; margin-bottom: 6px;">Nội dung nhận xét đầy đủ:</span>
            <div class="review-detail-comment-full">
              {{ selectedReviewDetail.comment }}
            </div>
          </div>
        </div>
        <div class="admin-modal-footer">
          <button 
            type="button" 
            @click="handleToggleApproval(selectedReviewDetail)" 
            class="btn"
            :class="selectedReviewDetail.is_approved ? 'btn-secondary' : 'btn-primary'"
          >
            {{ selectedReviewDetail.is_approved ? 'Chuyển về Chờ duyệt' : 'Duyệt & Đăng công khai' }}
          </button>
          <button 
            type="button" 
            @click="handleDeleteReview(selectedReviewDetail.id); selectedReviewDetail = null;" 
            class="btn btn-secondary" 
            style="color: #b91c1c; border-color: #fca5a5;"
          >
            Xóa nhận xét này
          </button>
          <button type="button" @click="selectedReviewDetail = null" class="btn btn-secondary">
            Đóng
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useCourseStore } from '@/stores/courses';
import Pagination from '@/components/Pagination.vue';

const props = defineProps({
  projects: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits(['update-counts']);

const courseStore = useCourseStore();

const allProjectReviews = ref([]);
const loadingReviews = ref(false);
const reviewStatusFilter = ref('all');
const reviewProjectFilter = ref('all');
const adminReviewsPage = ref(1);
const adminReviewsPageSize = ref(10);
const selectedReviewDetail = ref(null);

const pendingReviewsCount = computed(() => {
  return allProjectReviews.value.filter(r => !r.is_approved).length;
});

const approvedReviewsCount = computed(() => {
  return allProjectReviews.value.filter(r => r.is_approved).length;
});

watch([pendingReviewsCount, approvedReviewsCount], () => {
  emit('update-counts', {
    pending: pendingReviewsCount.value,
    approved: approvedReviewsCount.value,
    total: allProjectReviews.value.length
  });
});

const filteredProjectReviews = computed(() => {
  return allProjectReviews.value.filter(r => {
    if (reviewStatusFilter.value === 'pending' && r.is_approved) return false;
    if (reviewStatusFilter.value === 'approved' && !r.is_approved) return false;
    if (reviewProjectFilter.value !== 'all' && r.project_id !== reviewProjectFilter.value) return false;
    return true;
  });
});

const paginatedAdminReviews = computed(() => {
  const start = (adminReviewsPage.value - 1) * adminReviewsPageSize.value;
  return filteredProjectReviews.value.slice(start, start + adminReviewsPageSize.value);
});

watch([reviewStatusFilter, reviewProjectFilter], () => {
  adminReviewsPage.value = 1;
});

const getProjectTitle = (projectId) => {
  const p = props.projects.find(item => item.id === projectId);
  return p ? p.title : projectId;
};

const formatReviewDate = (dateStr) => {
  if (!dateStr) return '';
  try {
    const d = new Date(dateStr);
    return d.toLocaleString('vi-VN', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  } catch (e) {
    return dateStr;
  }
};

const loadAdminReviews = async () => {
  loadingReviews.value = true;
  try {
    const data = await courseStore.fetchProjectReviewsAdmin();
    allProjectReviews.value = Array.isArray(data) ? data : [];
    adminReviewsPage.value = 1;
  } catch (err) {
    console.error("Error loading project reviews:", err);
  } finally {
    loadingReviews.value = false;
  }
};

const handleToggleApproval = async (review) => {
  try {
    const updated = await courseStore.toggleProjectReviewApproval(review.id);
    if (updated) {
      review.is_approved = updated.is_approved;
    }
  } catch (e) {
    console.error("Toggle approval error:", e);
  }
};

const handleDeleteReview = async (reviewId) => {
  const isConfirmed = await courseStore.showConfirm({
    title: 'Xác nhận xóa nhận xét',
    message: 'Bạn có chắc chắn muốn xóa vĩnh viễn nhận xét này của học viên?',
    confirmText: 'Đồng ý xóa',
    cancelText: 'Hủy bỏ',
    type: 'danger'
  });

  if (isConfirmed) {
    try {
      const ok = await courseStore.deleteProjectReviewAdmin(reviewId);
      if (ok) {
        allProjectReviews.value = allProjectReviews.value.filter(r => r.id !== reviewId);
      }
    } catch (e) {
      console.error("Delete review error:", e);
    }
  }
};

onMounted(() => {
  loadAdminReviews();
});

defineExpose({
  loadAdminReviews,
  pendingReviewsCount
});
</script>

