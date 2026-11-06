<template>
  <div class="tab-content animate-fade-in admin-overview-wrapper">
    <!-- Compact Header Section -->
    <div class="content-header admin-overview-header">
      <div>
        <h2 class="overview-title">
          Tổng quan Vận hành
          <HelpTooltip 
            desc="Trung tâm điều khiển hiển thị 6 chỉ số KPI và 2 bảng tác vụ ưu tiên xử lý trong ngày." 
            impact="Phản ánh số liệu tức thì từ mọi tương tác của học viên trên website." 
          />
        </h2>
        <p class="overview-subtitle">Trung tâm kiểm soát dữ liệu: Đào tạo, Tuyển sinh, Học viên và Đánh giá học vụ.</p>
      </div>
      <div class="admin-export-actions">
        <select v-model="exportPeriod" class="admin-select export-period-select" title="Chọn khoảng thời gian thống kê & xuất dữ liệu">
          <option value="today">Hôm nay</option>
          <option value="7days">7 ngày qua</option>
          <option value="month">30 ngày qua (Tháng)</option>
          <option value="quarter">90 ngày qua (Quý)</option>
          <option value="year">365 ngày qua (Năm)</option>
          <option value="all">Tất cả thời gian</option>
        </select>
        <button type="button" @click="exportUsers" class="btn-export-action" title="Tải file CSV danh sách học viên">
          Xuất CSV Học viên
        </button>
        <button type="button" @click="exportContacts" class="btn-export-action" title="Tải file CSV yêu cầu tư vấn">
          Xuất CSV Tư vấn
        </button>
        <HelpTooltip 
          desc="Lọc dữ liệu thống kê & xuất file CSV theo các mốc thời gian: Hôm nay, 7 ngày qua, Tháng, Quý, Năm hoặc Tất cả." 
        />
        <button type="button" @click="refreshAllData" class="btn-export-action btn-refresh" :disabled="isLoading" title="Làm mới toàn bộ số liệu">
          {{ isLoading ? 'Đang tải...' : 'Làm mới' }}
        </button>
      </div>
    </div>

    <!-- 6 Uniform Compact Stats Cards (Đồng bộ, Tinh giản, Không viền màu mè) -->
    <div class="overview-stats-grid">
      <!-- 1. Yêu cầu tư vấn tuyển sinh -->
      <div class="admin-stat-card clickable-stat-card" @click="goToTab('contacts')">
        <div class="stat-top-row">
          <span class="stat-track">
            TƯ VẤN MỚI
            <HelpTooltip desc="Số yêu cầu tư vấn tuyển sinh cần gọi điện hỗ trợ." impact="Nhận từ Form tư vấn ở chân Trang chủ và trang khóa học." />
          </span>
          <span v-if="periodUnresolvedContacts.length > 0" class="badge-alert-tag">
            {{ periodUnresolvedContacts.length }} mới
          </span>
        </div>
        <div class="stat-number">
          <span v-if="isLoading && contacts.length === 0" class="stat-skeleton-pulse"></span>
          <span v-else>{{ periodUnresolvedContacts.length }}</span>
        </div>
        <div class="stat-label">Yêu cầu Tư vấn</div>
        <p class="stat-helper">
          <template v-if="exportPeriod === 'all'">Tổng {{ contacts.length }} liên hệ</template>
          <template v-else>{{ exportPeriodLabel }}: {{ periodContacts.length }} (Tổng {{ contacts.length }})</template>
        </p>
      </div>

      <!-- 2. Khóa học đào tạo -->
      <div class="admin-stat-card clickable-stat-card" @click="goToTab('courses')">
        <div class="stat-top-row">
          <span class="stat-track">
            ĐÀO TẠO
            <HelpTooltip desc="Tổng số chương trình đào tạo đang quản lý." impact="Hiển thị tại Section 6 Khóa học Tiêu biểu Trang chủ." />
          </span>
        </div>
        <div class="stat-number">
          <span v-if="isLoading && courses.length === 0" class="stat-skeleton-pulse"></span>
          <span v-else>{{ courses.length }}</span>
        </div>
        <div class="stat-label">Khóa học Đào tạo</div>
        <p class="stat-helper">{{ categories.length }} Chuyên mục</p>
      </div>

      <!-- 3. Học viên & Người dùng -->
      <div class="admin-stat-card clickable-stat-card" @click="goToTab('users')">
        <div class="stat-top-row">
          <span class="stat-track">
            HỌC VIÊN
            <HelpTooltip desc="Số tài khoản học viên đăng ký trên hệ thống." impact="Đồng bộ với cổng thông tin cá nhân /dashboard." />
          </span>
          <span v-if="exportPeriod !== 'all' && periodUsers.length > 0" class="badge-alert-tag">
            +{{ periodUsers.length }} mới
          </span>
        </div>
        <div class="stat-number">
          <span v-if="isLoading && users.length === 0" class="stat-skeleton-pulse"></span>
          <span v-else>{{ exportPeriod === 'all' ? users.length : periodUsers.length }}</span>
        </div>
        <div class="stat-label">{{ exportPeriod === 'all' ? 'Tài khoản Học viên' : 'Học viên Mới' }}</div>
        <p class="stat-helper">
          <template v-if="exportPeriod === 'all'">Thành viên hệ thống</template>
          <template v-else>{{ exportPeriodLabel }} • Tổng {{ users.length }}</template>
        </p>
      </div>

      <!-- 4. Cảm nhận học viên -->
      <div class="admin-stat-card clickable-stat-card" @click="goToTab('testimonials')">
        <div class="stat-top-row">
          <span class="stat-track">
            ĐÁNH GIÁ
            <HelpTooltip desc="Số cảm nhận đã duyệt và số bài chờ kiểm duyệt." impact="Chỉ bài đã DUYỆT mới xuất hiện tại Section 9 Trang chủ." />
          </span>
          <span v-if="periodPendingOrSpamCount > 0" class="badge-warning-tag">
            {{ periodPendingOrSpamCount }} cần xử lý
          </span>
        </div>
        <div class="stat-number">
          <span v-if="isLoading && testimonials.length === 0" class="stat-skeleton-pulse"></span>
          <span v-else>{{ periodApprovedTestimonials.length }}</span>
        </div>
        <div class="stat-label">Cảm nhận đã duyệt</div>
        <p class="stat-helper">{{ periodPendingTestimonials.length }} chờ • {{ periodSpamTestimonials.length }} spam</p>
      </div>

      <!-- 5. Tin tức & Tuyển sinh -->
      <div class="admin-stat-card clickable-stat-card" @click="goToTab('admissions')">
        <div class="stat-top-row">
          <span class="stat-track">
            BÀI VIẾT
            <HelpTooltip desc="Tổng bài viết chuyên môn và thông báo chiêu sinh." impact="Liên kết đến trang Tuyển sinh và Thư viện Cẩm nang." />
          </span>
        </div>
        <div class="stat-number">
          <span v-if="isLoading && blogs.length === 0 && admissions.length === 0" class="stat-skeleton-pulse"></span>
          <span v-else>{{ blogs.length + admissions.length }}</span>
        </div>
        <div class="stat-label">Tin tức & Tuyển sinh</div>
        <p class="stat-helper">{{ admissions.length }} tuyển sinh • {{ blogs.length }} tin</p>
      </div>

      <!-- 6. Giảng viên & Cố vấn -->
      <div class="admin-stat-card clickable-stat-card" @click="goToTab('lecturers')">
        <div class="stat-top-row">
          <span class="stat-track">
            CHUYÊN GIA
            <HelpTooltip desc="Đội ngũ giảng viên và cố vấn chiến lược." impact="Hiển thị tại Section 8 Đội ngũ Giảng viên Trang chủ." />
          </span>
        </div>
        <div class="stat-number">
          <span v-if="isLoading && lecturers.length === 0" class="stat-skeleton-pulse"></span>
          <span v-else>{{ lecturers.length + boardMembers.length }}</span>
        </div>
        <div class="stat-label">Giảng viên & Cố vấn</div>
        <p class="stat-helper">{{ lecturers.length }} GV • {{ boardMembers.length }} cố vấn</p>
      </div>
    </div>

    <!-- 2 Compact Workstation Panels Side-by-Side (Vừa vặn 1 màn hình, Không lướt nhiều) -->
    <div class="overview-workstation-grid mt-4">
      <!-- Panel 1: Yêu cầu tư vấn mới nhất -->
      <div class="workstation-panel glass-card">
        <div class="panel-header-row flex-between">
          <div class="panel-title-group">
            <h3 class="panel-title">
              Yêu cầu Tư vấn Tuyển sinh
              <HelpTooltip desc="4 khách hàng mới nhất. Nhấp 'Xử lý' để gọi điện và đổi trạng thái sang 'Đã liên hệ'." />
            </h3>
            <span class="panel-badge-count">{{ periodUnresolvedContacts.length }} chưa xử lý</span>
          </div>
          <button type="button" @click="goToTab('contacts')" class="btn-text-link">
            Xem tất cả ({{ contacts.length }}) →
          </button>
        </div>

        <div v-if="isLoading && contacts.length === 0" class="empty-compact-text">
          Đang tải yêu cầu tư vấn...
        </div>
        <div v-else-if="contacts.length === 0" class="empty-compact-text">
          Chưa có yêu cầu tư vấn nào từ học viên.
        </div>
        <div v-else class="compact-feed-list">
          <div v-for="c in recentContacts" :key="c.id" class="feed-item-card">
            <div class="feed-item-main">
              <div class="feed-item-header">
                <span class="feed-user-name">{{ c.fullname }}</span>
                <span class="feed-time">{{ formatDateShort(c.createdAt) }}</span>
              </div>
              <div class="feed-contact-line">
                <a v-if="c.phone" :href="'tel:' + c.phone" class="feed-phone-link">{{ c.phone }}</a>
                <span v-if="c.phone && c.email" class="feed-dot">•</span>
                <span v-if="c.email" class="feed-email">{{ c.email }}</span>
              </div>
              <div class="feed-topic-line">
                <span class="feed-topic-badge">{{ c.courseName || c.subject || 'Tư vấn lộ trình' }}</span>
                <span v-if="c.message" class="feed-msg-snippet">"{{ c.message }}"</span>
              </div>
            </div>
            <div class="feed-item-aside">
              <span class="status-pill" :class="c.isResolved ? 'status-resolved' : 'status-pending'">
                {{ c.isResolved ? 'Đã liên hệ' : 'Chờ tư vấn' }}
              </span>
              <button type="button" @click="goToTab('contacts')" class="btn-feed-action">
                Xử lý
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Panel 2: Đánh giá & Cảm nhận gần đây (Rõ ràng, Không bị che bên phải) -->
      <div class="workstation-panel glass-card">
        <div class="panel-header-row flex-between">
          <div class="panel-title-group">
            <h3 class="panel-title">
              Đánh giá & Cảm nhận Học viên
              <HelpTooltip desc="4 nhận xét mới nhất. Nhấp 'Kiểm duyệt' để duyệt bài hiển thị ra ngoài website." />
            </h3>
            <span v-if="periodPendingOrSpamCount > 0" class="panel-badge-warning">{{ periodPendingOrSpamCount }} cần duyệt</span>
          </div>
          <button type="button" @click="goToTab('testimonials')" class="btn-text-link">
            Xem tất cả ({{ testimonials.length }}) →
          </button>
        </div>

        <div v-if="isLoading && testimonials.length === 0" class="empty-compact-text">
          Đang tải danh sách cảm nhận...
        </div>
        <div v-else-if="testimonials.length === 0" class="empty-compact-text">
          Chưa có nhận xét hoặc cảm nhận nào.
        </div>
        <div v-else class="compact-feed-list">
          <div v-for="t in recentTestimonials" :key="t.id" class="feed-item-card">
            <div class="feed-item-main">
              <div class="feed-item-header">
                <span class="feed-user-name">{{ t.name }}</span>
                <span class="feed-rating-tag">{{ t.rating || 5 }}/5 Điểm</span>
              </div>
              <div class="feed-course-line">
                <span class="feed-course-name">{{ t.course_name || t.courseName || 'Khóa học ACC' }}</span>
                <span v-if="t.role" class="feed-dot">•</span>
                <span v-if="t.role" class="feed-user-role">{{ t.role }}</span>
              </div>
              <div class="feed-quote-text">
                "{{ t.quote || t.text || 'Nội dung nhận xét...' }}"
              </div>
            </div>
            <div class="feed-item-aside">
              <span 
                v-if="t.testimonial_type === 'spam' || t.isSpam"
                class="status-pill status-spam"
              >
                Spam
              </span>
              <span 
                v-else-if="t.isApproved || t.is_approved"
                class="status-pill status-approved"
              >
                Đã duyệt
              </span>
              <span 
                v-else
                class="status-pill status-pending"
              >
                Chờ duyệt
              </span>
              <button type="button" @click="goToTab('testimonials')" class="btn-feed-action">
                Kiểm duyệt
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useCourseStore } from '@/stores/courses';
import HelpTooltip from '@/components/common/HelpTooltip.vue';

const router = useRouter();
const route = useRoute();
const courseStore = useCourseStore();
const exportPeriod = ref('all');
const isLoading = ref(false);

// Computed store state
const users = computed(() => courseStore.adminUsers || []);
const contacts = computed(() => courseStore.adminContacts || []);
const courses = computed(() => courseStore.courses || []);
const categories = computed(() => courseStore.categories || []);
const blogs = computed(() => courseStore.adminBlogPosts || []);
const admissions = computed(() => courseStore.adminAdmissions || []);
const testimonials = computed(() => courseStore.adminTestimonials || []);
const lecturers = computed(() => courseStore.lecturers || []);
const boardMembers = computed(() => courseStore.adminBoardMembers || []);

// Period labels and date filter helper
const periodLabels = {
  today: 'Hôm nay',
  '7days': '7 ngày qua',
  month: '30 ngày qua',
  quarter: '90 ngày qua',
  year: '365 ngày qua',
  all: 'Tất cả thời gian'
};
const exportPeriodLabel = computed(() => periodLabels[exportPeriod.value] || 'Tất cả');

const isWithinPeriod = (dateVal, period) => {
  if (!period || period === 'all') return true;
  if (!dateVal) return false;
  const itemDate = new Date(dateVal).getTime();
  if (isNaN(itemDate)) return false;
  const now = new Date();
  if (period === 'today') {
    const startOfToday = new Date(now.getFullYear(), now.getMonth(), now.getDate()).getTime();
    return itemDate >= startOfToday;
  }
  if (period === '7days' || period === 'week') {
    return itemDate >= (now.getTime() - 7 * 24 * 60 * 60 * 1000);
  }
  if (period === 'month') {
    return itemDate >= (now.getTime() - 30 * 24 * 60 * 60 * 1000);
  }
  if (period === 'quarter') {
    return itemDate >= (now.getTime() - 90 * 24 * 60 * 60 * 1000);
  }
  if (period === 'year') {
    return itemDate >= (now.getTime() - 365 * 24 * 60 * 60 * 1000);
  }
  return true;
};

// Derived filtered metrics
const periodContacts = computed(() => 
  contacts.value.filter(c => isWithinPeriod(c.createdAt || c.created_at, exportPeriod.value))
);
const unresolvedContacts = computed(() => contacts.value.filter(c => !c.isResolved));
const periodUnresolvedContacts = computed(() => 
  exportPeriod.value === 'all' 
    ? unresolvedContacts.value 
    : periodContacts.value.filter(c => !c.isResolved)
);

const periodUsers = computed(() => 
  users.value.filter(u => isWithinPeriod(u.createdAt || u.created_at, exportPeriod.value))
);

const periodTestimonials = computed(() => 
  testimonials.value.filter(t => isWithinPeriod(t.createdAt || t.created_at, exportPeriod.value))
);
const approvedTestimonials = computed(() => 
  testimonials.value.filter(t => (t.isApproved || t.is_approved) && t.testimonial_type !== 'spam')
);
const periodApprovedTestimonials = computed(() => 
  exportPeriod.value === 'all'
    ? approvedTestimonials.value
    : periodTestimonials.value.filter(t => (t.isApproved || t.is_approved) && t.testimonial_type !== 'spam')
);

const pendingTestimonials = computed(() => 
  testimonials.value.filter(t => (!t.isApproved && !t.is_approved) && t.testimonial_type !== 'spam')
);
const periodPendingTestimonials = computed(() => 
  exportPeriod.value === 'all'
    ? pendingTestimonials.value
    : periodTestimonials.value.filter(t => (!t.isApproved && !t.is_approved) && t.testimonial_type !== 'spam')
);

const spamTestimonials = computed(() => 
  testimonials.value.filter(t => t.testimonial_type === 'spam' || t.isSpam)
);
const periodSpamTestimonials = computed(() => 
  exportPeriod.value === 'all'
    ? spamTestimonials.value
    : periodTestimonials.value.filter(t => t.testimonial_type === 'spam' || t.isSpam)
);

const pendingOrSpamCount = computed(() => 
  pendingTestimonials.value.length + spamTestimonials.value.length
);
const periodPendingOrSpamCount = computed(() => 
  periodPendingTestimonials.value.length + periodSpamTestimonials.value.length
);

// Recent activity slices (Compact limit of 4 items for zero scrolling)
const recentContacts = computed(() => {
  const source = exportPeriod.value !== 'all' && periodContacts.value.length > 0 
    ? periodContacts.value 
    : contacts.value;
  return source.slice(0, 4);
});
const recentTestimonials = computed(() => {
  const source = exportPeriod.value !== 'all' && periodTestimonials.value.length > 0 
    ? periodTestimonials.value 
    : testimonials.value;
  return source.slice(0, 4);
});

// Manual refresh handler
const refreshAllData = async () => {
  isLoading.value = true;
  try {
    await Promise.all([
      courseStore.fetchAdminContacts(true).catch(() => {}),
      courseStore.fetchAdminTestimonials(true).catch(() => {}),
      courseStore.fetchCourses(true).catch(() => {}),
      courseStore.fetchCategories(true).catch(() => {}),
      courseStore.fetchAdminUsers(true).catch(() => {}),
      courseStore.fetchAdminBlogPosts(true).catch(() => {}),
      courseStore.fetchAdminAdmissions(true).catch(() => {}),
      courseStore.fetchLecturers(true).catch(() => {}),
      courseStore.fetchAdminBoardMembers(true).catch(() => {})
    ]);
    courseStore.showToast('Đã làm mới dữ liệu tổng quan thành công!', 'success');
  } catch (err) {
    console.warn('Lỗi làm mới dữ liệu:', err);
  } finally {
    isLoading.value = false;
  }
};

// On mount: only fetch items that are not yet loaded to avoid lag
onMounted(async () => {
  const tasks = [];
  if (!courseStore.adminContacts?.length) tasks.push(courseStore.fetchAdminContacts().catch(() => {}));
  if (!courseStore.adminTestimonials?.length) tasks.push(courseStore.fetchAdminTestimonials().catch(() => {}));
  if (!courseStore.courses?.length) tasks.push(courseStore.fetchCourses().catch(() => {}));
  if (!courseStore.categories?.length) tasks.push(courseStore.fetchCategories().catch(() => {}));
  if (!courseStore.adminUsers?.length) tasks.push(courseStore.fetchAdminUsers().catch(() => {}));
  if (!courseStore.adminBlogPosts?.length) tasks.push(courseStore.fetchAdminBlogPosts().catch(() => {}));
  if (!courseStore.adminAdmissions?.length) tasks.push(courseStore.fetchAdminAdmissions().catch(() => {}));
  if (!courseStore.lecturers?.length) tasks.push(courseStore.fetchLecturers().catch(() => {}));
  if (!courseStore.adminBoardMembers?.length) tasks.push(courseStore.fetchAdminBoardMembers().catch(() => {}));

  if (tasks.length > 0) {
    isLoading.value = true;
    await Promise.all(tasks).finally(() => {
      isLoading.value = false;
    });
  }
});

// Navigate directly to target tab
const goToTab = (tabId) => {
  router.push({ query: { ...route.query, tab: tabId } });
};

// Export CSV handlers
const exportUsers = () => {
  courseStore.exportAdminReport('users', exportPeriod.value);
};

const exportContacts = () => {
  courseStore.exportAdminReport('contacts', exportPeriod.value);
};

// Format short date
const formatDateShort = (dateStr) => {
  if (!dateStr) return '';
  const d = new Date(dateStr);
  return `${d.getDate().toString().padStart(2, '0')}/${(d.getMonth() + 1).toString().padStart(2, '0')}/${d.getFullYear()}`;
};
</script>

<style scoped>
.admin-overview-wrapper {
  padding-bottom: 12px;
  width: 100%;
  box-sizing: border-box;
}

/* Header */
.admin-overview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 0;
  padding-bottom: 12px;
  border-bottom: 1px solid #f1f5f9;
}

.overview-title {
  font-size: 18px;
  font-weight: 800;
  color: #0f172a;
  margin: 0;
  font-family: 'Manrope', -apple-system, sans-serif;
}

.overview-subtitle {
  font-size: 12px;
  color: #64748b;
  margin: 2px 0 0 0;
}

/* Actions Header */
.admin-export-actions {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}

.export-period-select {
  padding: 6px 10px;
  font-size: 11.5px;
  border-radius: 6px;
  border: 1px solid #cbd5e1;
  background: #ffffff;
  color: #334155;
  font-weight: 500;
  cursor: pointer;
}

.btn-export-action {
  padding: 6px 11px;
  font-size: 11.5px;
  font-weight: 600;
  border-radius: 6px;
  border: 1px solid #cbd5e1;
  background: #ffffff;
  color: #334155;
  cursor: pointer;
  transition: all 0.15s ease;
  white-space: nowrap;
}

.btn-export-action:hover {
  background: #f8fafc;
  border-color: #94a3b8;
  color: #0f172a;
}

.btn-export-action.btn-refresh {
  background: #022b9f;
  border-color: #022b9f;
  color: #ffffff;
}

.btn-export-action.btn-refresh:hover {
  background: #0369a1;
  border-color: #0369a1;
}

.btn-export-action:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* ==========================================================================
   STATS CARDS GRID (1 DÒNG DUY NHẤT, GỌN GÀNG, ĐỒNG BỘ 100%)
   ========================================================================== */
.overview-stats-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 10px;
  margin-top: 14px;
  width: 100%;
}

@media (max-width: 1280px) {
  .overview-stats-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 680px) {
  .overview-stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.admin-stat-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 10px 12px;
  box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03);
  transition: all 0.15s ease;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.admin-stat-card:hover {
  border-color: #022b9f;
  background: #f8fafc;
  transform: translateY(-1px);
  box-shadow: 0 4px 10px rgba(2, 43, 159, 0.06);
}

.stat-top-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 4px;
}

.stat-track {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.5px;
  color: #64748b;
  text-transform: uppercase;
}

.badge-alert-tag {
  background: #fef2f2;
  color: #dc2626;
  border: 1px solid #fecaca;
  font-size: 9.5px;
  font-weight: 700;
  padding: 1px 4px;
  border-radius: 3px;
  white-space: nowrap;
}

.badge-warning-tag {
  background: #fffbeb;
  color: #b45309;
  border: 1px solid #fde68a;
  font-size: 9.5px;
  font-weight: 700;
  padding: 1px 4px;
  border-radius: 3px;
  white-space: nowrap;
}

.stat-number {
  font-size: 20px;
  font-weight: 800;
  color: #0f172a;
  line-height: 1.15;
  margin: 3px 0 1px 0;
  font-family: 'Manrope', -apple-system, sans-serif;
}

.stat-label {
  font-size: 11.5px;
  font-weight: 600;
  color: #334155;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.stat-helper {
  font-size: 10.5px;
  color: #94a3b8;
  margin: 1px 0 0 0;
  line-height: 1.2;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* ==========================================================================
   2 COMPACT WORKSTATION PANELS (SIDE-BY-SIDE)
   ========================================================================== */
.overview-workstation-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  width: 100%;
}

@media (max-width: 1024px) {
  .overview-workstation-grid {
    grid-template-columns: 1fr;
  }
}

.workstation-panel {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 14px 16px;
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03);
  box-sizing: border-box;
}

.panel-header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 10px;
  border-bottom: 1px solid #f1f5f9;
  margin-bottom: 10px;
  gap: 10px;
}

.panel-title-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.panel-title {
  font-size: 13.5px;
  font-weight: 700;
  color: #0f172a;
  margin: 0;
  font-family: 'Manrope', sans-serif;
}

.panel-badge-count {
  font-size: 10px;
  font-weight: 700;
  background: #eff6ff;
  color: #022b9f;
  padding: 1px 6px;
  border-radius: 4px;
  border: 1px solid #bfdbfe;
}

.panel-badge-warning {
  font-size: 10px;
  font-weight: 700;
  background: #fffbeb;
  color: #b45309;
  padding: 1px 6px;
  border-radius: 4px;
  border: 1px solid #fde68a;
}

.btn-text-link {
  background: transparent;
  border: none;
  color: #0284c7;
  font-size: 11.5px;
  font-weight: 700;
  cursor: pointer;
  padding: 0;
  text-decoration: none;
  white-space: nowrap;
}

.btn-text-link:hover {
  color: #022b9f;
}

.empty-compact-text {
  padding: 24px 12px;
  text-align: center;
  font-size: 12px;
  color: #94a3b8;
}

/* Feed List & Item Cards */
.compact-feed-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.feed-item-card {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  padding: 8px 10px;
  background: #f8fafc;
  border: 1px solid #f1f5f9;
  border-radius: 6px;
  transition: all 0.15s ease;
}

.feed-item-card:hover {
  background: #ffffff;
  border-color: #cbd5e1;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
}

.feed-item-main {
  flex: 1;
  min-width: 0;
}

.feed-item-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.feed-user-name {
  font-size: 12.5px;
  font-weight: 700;
  color: #0f172a;
}

.feed-time {
  font-size: 10.5px;
  color: #94a3b8;
}

.feed-contact-line {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11.5px;
  margin-top: 1px;
}

.feed-phone-link {
  color: #0284c7;
  font-weight: 600;
  text-decoration: none;
}

.feed-email {
  color: #64748b;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.feed-dot {
  color: #cbd5e1;
  font-size: 10px;
}

.feed-topic-line {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 3px;
  flex-wrap: wrap;
}

.feed-topic-badge {
  display: inline-block;
  padding: 1px 6px;
  background: #eff6ff;
  color: #022b9f;
  border-radius: 4px;
  font-size: 10.5px;
  font-weight: 600;
}

.feed-msg-snippet {
  font-size: 11px;
  color: #64748b;
  font-style: italic;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 240px;
}

.feed-rating-tag {
  font-size: 10.5px;
  font-weight: 700;
  background: #fef3c7;
  color: #b45309;
  padding: 1px 5px;
  border-radius: 3px;
}

.feed-course-line {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  margin-top: 1px;
}

.feed-course-name {
  font-weight: 600;
  color: #334155;
}

.feed-user-role {
  color: #64748b;
}

.feed-quote-text {
  font-size: 11.5px;
  color: #475569;
  line-height: 1.35;
  margin-top: 2px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Feed Item Aside (Status & Action) */
.feed-item-aside {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 5px;
  flex-shrink: 0;
}

.status-pill {
  display: inline-block;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 10.5px;
  font-weight: 700;
  white-space: nowrap;
}

.status-resolved {
  background: #ecfdf5;
  color: #047857;
  border: 1px solid #a7f3d0;
}

.status-pending {
  background: #fef3c7;
  color: #b45309;
  border: 1px solid #fde68a;
}

.status-spam {
  background: #fef2f2;
  color: #dc2626;
  border: 1px solid #fecaca;
}

.status-approved {
  background: #ecfdf5;
  color: #047857;
  border: 1px solid #a7f3d0;
}

.btn-feed-action {
  padding: 2px 8px;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  color: #0284c7;
  font-size: 11px;
  font-weight: 700;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.15s;
}

.btn-feed-action:hover {
  background: #eff6ff;
  border-color: #93c5fd;
  color: #022b9f;
}

.stat-skeleton-pulse {
  display: inline-block;
  width: 36px;
  height: 20px;
  background: #e2e8f0;
  border-radius: 3px;
}
</style>
