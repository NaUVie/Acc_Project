<template>
  <div class="tab-content animate-fade-in">
    <div class="content-header flex-between">
      <div>
        <h2>Quản lý Học viên</h2>
        <p>Danh sách học viên và tài khoản người dùng trên hệ thống.</p>
      </div>
      <div style="display: flex; gap: 10px; align-items: center;">
        <button @click="refreshUsers" :disabled="isRefreshing" class="btn btn-secondary btn-sm" style="display: flex; align-items: center; gap: 6px; font-weight: 600;" title="Tải lại danh sách học viên mới nhất từ máy chủ">
          <span :class="{ 'spin-icon': isRefreshing }">🔄</span>
          <span>{{ isRefreshing ? 'Đang đồng bộ...' : 'Làm mới dữ liệu' }}</span>
        </button>
        <button @click="openAddUserModal" class="btn btn-primary btn-sm">+ Thêm học viên</button>
      </div>
    </div>

    <!-- Filters & Search -->
    <div class="filter-bar mt-4">
      <input 
        v-model="userSearch" 
        type="text" 
        placeholder="Tìm theo tên, email, số điện thoại, mã giới thiệu..." 
        class="admin-search-input"
      />
      <select v-model="userFilterRole" class="admin-select">
        <option value="all">Tất cả vai trò</option>
        <option value="admin">Quản trị viên (Admin)</option>
        <option value="student">Học viên (Student)</option>
      </select>
    </div>

    <!-- Clean Compact Users Table -->
    <div class="table-responsive mt-6">
      <table class="admin-table user-compact-table">
        <thead>
          <tr>
            <th>Học viên</th>
            <th>Liên hệ</th>
            <th>Vai trò</th>
            <th>Trạng thái</th>
            <th class="text-right">Hành động</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="u in paginatedUsers" :key="u.id">
            <!-- Student Name & Avatar -->
            <td data-label="Học viên">
              <div class="user-cell-profile">
                <div class="user-avatar-badge">
                  {{ getUserInitials(u.fullname) }}
                </div>
                <div class="user-meta-info">
                  <div class="user-fullname-text">{{ u.fullname }}</div>
                  <div class="user-id-sub">Mã: #{{ u.id }}</div>
                </div>
              </div>
            </td>

            <!-- Contact Info (Email & Phone) -->
            <td data-label="Liên hệ">
              <div class="user-contact-col">
                <div class="contact-email" :title="u.email">{{ u.email }}</div>
                <div class="contact-phone text-muted" v-if="u.phone">
                  📞 {{ u.phone }}
                </div>
                <div class="contact-phone text-muted empty-phone" v-else>
                  Chưa có SĐT
                </div>
              </div>
            </td>

            <!-- Role -->
            <td data-label="Vai trò">
              <span v-if="u.role === 'admin'" class="role-admin-badge" title="Tài khoản Quản trị viên">
                🛡️ Admin
              </span>
              <select 
                v-else
                :value="u.role" 
                @change="changeUserRole(u.id, $event.target.value)"
                class="role-select role-student"
              >
                <option value="student">Student</option>
                <option value="admin">Admin</option>
              </select>
            </td>

            <!-- Status Toggle -->
            <td data-label="Trạng thái">
              <span v-if="u.role === 'admin'" class="status-admin-pill" title="Tài khoản Quản trị viên luôn hoạt động">
                🛡️ Quản trị viên
              </span>
              <button 
                v-else
                @click="toggleUserStatus(u)"
                class="status-toggle-btn"
                :class="{ active: u.isActive }"
                :title="u.isActive ? 'Nhấn để khóa tài khoản học viên' : 'Nhấn để kích hoạt lại học viên'"
              >
                {{ u.isActive ? 'Hoạt động' : 'Đã khóa' }}
              </button>
            </td>

            <!-- Actions: View Details, Edit, Delete -->
            <td data-label="Hành động" class="text-right">
              <div class="action-buttons-wrap">
                <button 
                  @click="viewUserDetails(u)" 
                  class="btn-detail-pill" 
                  title="Xem toàn bộ thông tin chi tiết học viên"
                >
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                    <circle cx="12" cy="12" r="3"></circle>
                  </svg>
                  <span>Chi tiết</span>
                </button>
                <button @click="editUserDetails(u)" class="btn-action edit" title="Chỉnh sửa thông tin / Đổi mật khẩu">✏️</button>
                <button 
                  @click="deleteUser(u.id)" 
                  class="btn-action delete" 
                  :title="u.role === 'admin' ? 'Không thể xóa tài khoản Quản trị viên' : 'Xóa học viên'"
                  :disabled="u.role === 'admin'"
                  :style="u.role === 'admin' ? 'opacity: 0.25; cursor: not-allowed;' : ''"
                >
                  🗑️
                </button>
              </div>
            </td>
          </tr>
          <tr v-if="filteredUsers.length === 0">
            <td colspan="5" class="text-center py-8 text-muted">Không tìm thấy học viên nào phù hợp với tìm kiếm.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination Component -->
    <Pagination 
      v-if="filteredUsers.length > pageSize"
      v-model:currentPage="currentPage"
      :totalItems="filteredUsers.length"
      :pageSize="pageSize"
    />

    <!-- ==================== MODAL: XEM CHI TIẾT HỌC VIÊN ==================== -->
    <div v-if="detailModalOpen && selectedUser" class="modal-overlay" @click.self="detailModalOpen = false">
      <div class="modal-content glass-card user-detail-modal animate-scale-up">
        <!-- Modal Header -->
        <div class="detail-header-card">
          <div class="detail-avatar-wrap">
            {{ getUserInitials(selectedUser.fullname) }}
          </div>
          <div class="detail-title-wrap">
            <div class="detail-user-name">{{ selectedUser.fullname }}</div>
            <div class="detail-badges-row">
              <span class="detail-id-tag">Mã học viên: #{{ selectedUser.id }}</span>
              <span class="detail-role-pill" :class="'role-' + selectedUser.role">
                {{ selectedUser.role === 'admin' ? 'Quản trị viên (Admin)' : 'Học viên (Student)' }}
              </span>
              <span class="detail-status-pill" :class="selectedUser.isActive ? 'active' : 'inactive'">
                {{ selectedUser.isActive ? 'Đang hoạt động' : 'Tài khoản đã khóa' }}
              </span>
            </div>
          </div>
          <button @click="detailModalOpen = false" class="detail-close-btn" title="Đóng">✕</button>
        </div>

        <!-- Modal Body: 2-column info grid -->
        <div class="detail-info-grid mt-4">
          <!-- Col 1: Thông tin cá nhân & liên hệ -->
          <div class="detail-info-col">
            <h4 class="detail-section-title">Thông tin liên hệ</h4>
            <div class="detail-info-row">
              <span class="detail-label">Email:</span>
              <span class="detail-value font-semibold">{{ selectedUser.email }}</span>
            </div>
            <div class="detail-info-row">
              <span class="detail-label">Số điện thoại:</span>
              <span class="detail-value">{{ selectedUser.phone || 'Chưa cập nhật' }}</span>
            </div>
            <div class="detail-info-row">
              <span class="detail-label">Ngày tham gia:</span>
              <span class="detail-value">{{ formatDate(selectedUser.createdAt) }}</span>
            </div>
          </div>

          </div>
<!-- ==================== KHÓA HỌC ĐÃ CẤP QUYỀN ==================== -->
        <div class="user-courses-section mt-5" style="border-top: 1px solid #e2e8f0; padding-top: 18px;">
          <div class="user-courses-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <div>
              <h4 class="detail-section-title" style="margin: 0; font-size: 14px; font-weight: 700; color: #0f172a;">
                📚 Quyền truy cập khóa học
                <span v-if="!loadingUserCourses" style="font-size: 12px; font-weight: 600; color: #0284c7; background: #e0f2fe; padding: 2px 8px; border-radius: 12px; margin-left: 6px;">
                  {{ userCourses.length }} khóa
                </span>
              </h4>
            </div>
            <button 
              type="button" 
              class="btn btn-sm btn-primary" 
              @click="toggleGrantForm"
              style="padding: 5px 12px; font-size: 12px; font-weight: 600; border-radius: 6px;"
            >
              {{ showGrantForm ? '✕ Đóng form' : '+ Cấp quyền khóa học' }}
            </button>
          </div>

          <!-- Form cấp quyền khóa học -->
          <div v-if="showGrantForm" class="grant-course-box mb-3 p-3" style="border: 1px dashed #38bdf8; background: #f0f9ff; border-radius: 10px;">
            <div style="font-size: 12.5px; font-weight: 700; color: #0369a1; margin-bottom: 8px;">
              Chọn khóa học cần cấp quyền vào học cho {{ selectedUser.fullname }}:
            </div>
            <div style="display: flex; gap: 8px;">
              <select v-model="selectedCourseToGrant" class="admin-input-style" style="flex: 1; font-size: 13px; background: #ffffff;">
                <option value="" disabled>-- Chọn khóa học từ danh mục --</option>
                <option 
                  v-for="c in availableCoursesToGrant" 
                  :key="c.id" 
                  :value="c.id"
                >
                  {{ c.title }}
                </option>
              </select>
              <button 
                type="button" 
                class="btn btn-sm btn-success" 
                :disabled="!selectedCourseToGrant || grantingCourse"
                @click="handleGrantCourse"
                style="padding: 6px 16px; font-size: 12.5px; font-weight: 700; white-space: nowrap; background: #16a34a; border-color: #16a34a; color: white;"
              >
                {{ grantingCourse ? 'Đang cấp...' : '✓ Xác nhận cấp' }}
              </button>
            </div>
            <p v-if="availableCoursesToGrant.length === 0" style="font-size: 12px; color: #64748b; margin: 8px 0 0 0;">
              💡 Học viên này đã được cấp tất cả các khóa học hiện có trong hệ thống!
            </p>
          </div>

          <!-- Danh sách khóa học của học viên -->
          <div class="user-courses-content">
            <div v-if="loadingUserCourses" class="text-center py-4 text-muted" style="font-size: 13px;">
              Đang tải danh sách khóa học của học viên...
            </div>
            <div v-else-if="userCourses.length === 0" class="empty-courses-alert text-center py-4" style="border: 1px dashed #cbd5e1; border-radius: 8px; background: #f8fafc; color: #64748b; font-size: 12.5px;">
              Học viên chưa được cấp quyền khóa học nào. Bấm <strong>"+ Cấp quyền khóa học"</strong> ở trên để mở quyền.
            </div>
            <div v-else class="courses-compact-scroll" style="display: flex; flex-direction: column; gap: 8px; max-height: 240px; overflow-y: auto; padding-right: 4px;">
              <div 
                v-for="enr in userCourses" 
                :key="enr.id" 
                class="enrolled-course-row" 
                style="display: flex; align-items: center; justify-content: space-between; padding: 10px 12px; border: 1px solid #e2e8f0; border-radius: 8px; background: #ffffff; transition: all 0.2s ease;"
              >
                <div style="display: flex; align-items: center; gap: 12px; min-width: 0;">
                  <img 
                    :src="enr.course?.image || '/images/Square-Cover-_1.webp'" 
                    :alt="enr.course?.title" 
                    style="width: 44px; height: 44px; border-radius: 6px; object-fit: cover; flex-shrink: 0; border: 1px solid #e2e8f0;"
                  />
                  <div style="min-width: 0;">
                    <div style="font-size: 13px; font-weight: 700; color: #1e293b; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" :title="enr.course?.title">
                      {{ enr.course?.title }}
                    </div>
                    <div style="font-size: 11.5px; color: #64748b; margin-top: 2px;">
                      Kích hoạt: {{ formatDate(enr.enrolled_at) }}
                      <span v-if="enr.order_id" style="margin-left: 6px; color: #0284c7; background: #f0f9ff; padding: 1px 6px; border-radius: 4px; font-weight: 600;">Đơn #{{ enr.order_id }}</span>
                      <span v-else style="margin-left: 6px; color: #16a34a; background: #f0fdf4; padding: 1px 6px; border-radius: 4px; font-weight: 600;">Admin cấp trực tiếp</span>
                    </div>
                  </div>
                </div>

                <div style="flex-shrink: 0; margin-left: 12px;">
                  <button 
                    type="button" 
                    class="btn btn-sm btn-danger-outline" 
                    @click="handleRevokeCourse(enr.course?.id, enr.course?.title)"
                    title="Thu hồi quyền truy cập khóa học này"
                    style="padding: 4px 10px; font-size: 11.5px; font-weight: 600; border-color: #fecdd3; color: #e11d48; border-radius: 6px;"
                  >
                    🗑️ Thu hồi quyền
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Modal Footer Actions -->
        <div class="modal-actions mt-6 flex-between">
          <div class="left-actions">
            <button 
              v-if="selectedUser.role !== 'admin'"
              @click="toggleUserStatusFromModal(selectedUser)" 
              class="btn btn-sm"
              :class="selectedUser.isActive ? 'btn-danger-outline' : 'btn-success-outline'"
            >
              {{ selectedUser.isActive ? '🔒 Khóa tài khoản' : '🔓 Mở khóa tài khoản' }}
            </button>
            <span v-else class="text-muted" style="font-size: 12.5px; font-weight: 600;">🛡️ Tài khoản Quản trị viên (Admin)</span>
          </div>
          <div class="right-actions">
            <button @click="openEditFromDetail(selectedUser)" class="btn btn-primary btn-sm">
              ✏️ Chỉnh sửa thông tin
            </button>
            <button @click="detailModalOpen = false" class="btn btn-secondary btn-sm ml-2">
              Đóng
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- ==================== MODAL: ADD/EDIT USER ==================== -->
    <div v-if="userModalOpen" class="modal-overlay" @click.self="userModalOpen = false">
      <div class="modal-content glass-card user-form-modal animate-scale-up">
        <div class="user-form-header">
          <div class="flex-align-center gap-3">
            <div class="form-modal-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>
            </div>
            <div>
              <h3 class="m-0 font-bold text-gray-900" style="font-size: 17px;">{{ isEditingUser ? 'Chỉnh sửa thông tin học viên' : 'Thêm học viên mới' }}</h3>
              <p class="text-muted text-xs m-0 mt-0.5">Vui lòng điền đầy đủ các thông tin cần thiết bên dưới</p>
            </div>
          </div>
          <button type="button" @click="userModalOpen = false" class="detail-close-btn" title="Đóng">✕</button>
        </div>

        <form @submit.prevent="saveUser">
          <div class="user-modal-grid">
            <div class="form-group">
              <label class="form-label-custom">Họ và tên <span class="text-danger">*</span></label>
              <input v-model="userForm.fullname" type="text" required class="admin-input-style" placeholder="Nguyễn Văn A" />
            </div>

            <div class="form-group">
              <label class="form-label-custom">Số điện thoại</label>
              <input v-model="userForm.phone" type="tel" class="admin-input-style" placeholder="0901234567" />
            </div>

            <div class="form-group">
              <label class="form-label-custom">Email đăng nhập <span class="text-danger">*</span></label>
              <input v-model="userForm.email" type="email" required class="admin-input-style" placeholder="example@gmail.com" :disabled="isEditingUser" />
            </div>

            <div class="form-group" v-if="!isEditingUser">
              <label class="form-label-custom">Mật khẩu khởi tạo <span class="text-danger">*</span></label>
              <input v-model="userForm.password" type="password" required class="admin-input-style" placeholder="Tối thiểu 6 ký tự" />
            </div>
            <div class="form-group" v-else>
              <label class="form-label-custom">Đặt lại mật khẩu mới</label>
              <input v-model="userForm.password" type="password" class="admin-input-style" placeholder="Để trống nếu không đổi..." />
            </div>

            <div class="form-group">
              <label class="form-label-custom">Vai trò</label>
              <select v-model="userForm.role" class="admin-input-style">
                <option value="student">Student (Học viên)</option>
                <option value="admin">Admin (Quản trị viên)</option>
              </select>
            </div>

            
          </div>

          <div class="modal-actions mt-5 pt-3 border-top">
            <button type="button" @click="userModalOpen = false" class="btn btn-secondary btn-sm px-4">Hủy</button>
            <button type="submit" class="btn btn-primary btn-sm px-5 font-semibold">Lưu thông tin</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useCourseStore } from '@/stores/courses';
import Pagination from '@/components/Pagination.vue';

const courseStore = useCourseStore();

const isRefreshing = ref(false);
const refreshUsers = async () => {
  isRefreshing.value = true;
  try {
    await courseStore.fetchAdminUsers(true);
    courseStore.showToast('Đã làm mới danh sách học viên mới nhất!', 'success');
  } catch (err) {
    courseStore.showToast('Lỗi khi làm mới: ' + (err.message || err), 'error');
  } finally {
    isRefreshing.value = false;
  }
};

const users = computed(() => courseStore.adminUsers);

onMounted(async () => {
  if (users.value.length === 0) {
    await courseStore.fetchAdminUsers().catch(err => console.warn('fetchAdminUsers failed:', err));
  }
});

const userSearch = ref('');
const userFilterRole = ref('all');
const currentPage = ref(1);
const pageSize = ref(10);

const filteredUsers = computed(() => {
  const query = (userSearch.value || '').toLowerCase().trim();
  return (users.value || []).filter(u => {
    const fullname = (u.fullname || '').toLowerCase();
    const email = (u.email || '').toLowerCase();
    const phone = (u.phone || '').toLowerCase();
    const refCode = (u.referralCode || '').toLowerCase();
    const matchesSearch = !query || fullname.includes(query) || email.includes(query) || phone.includes(query) || refCode.includes(query);
    const matchesRole = userFilterRole.value === 'all' || u.role === userFilterRole.value;
    return matchesSearch && matchesRole;
  });
});

const paginatedUsers = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  return filteredUsers.value.slice(start, start + pageSize.value);
});

watch([userSearch, userFilterRole], () => {
  currentPage.value = 1;
});

// View Details Modal States
const detailModalOpen = ref(false);
const selectedUser = ref(null);

// Student Course Access Management States
const userCourses = ref([]);
const loadingUserCourses = ref(false);
const showGrantForm = ref(false);
const selectedCourseToGrant = ref('');
const grantingCourse = ref(false);

const availableCoursesToGrant = computed(() => {
  const allCourses = courseStore.courses || [];
  const enrolledIds = new Set(userCourses.value.map(enr => String(enr.course?.id || enr.course_id)));
  return allCourses.filter(c => !enrolledIds.has(String(c.id)));
});

const loadUserCourses = async (userId) => {
  loadingUserCourses.value = true;
  try {
    userCourses.value = await courseStore.fetchAdminUserCourses(userId);
  } catch (err) {
    console.error("Failed to load user courses:", err);
    userCourses.value = [];
  } finally {
    loadingUserCourses.value = false;
  }
};

const toggleGrantForm = () => {
  showGrantForm.value = !showGrantForm.value;
  selectedCourseToGrant.value = '';
};

const handleGrantCourse = async () => {
  if (!selectedUser.value || !selectedCourseToGrant.value) return;
  grantingCourse.value = true;
  try {
    const res = await courseStore.grantAdminUserCourse(selectedUser.value.id, selectedCourseToGrant.value);
    if (res) {
      await loadUserCourses(selectedUser.value.id);
      showGrantForm.value = false;
      selectedCourseToGrant.value = '';
    }
  } catch (err) {
    // Toast already handled in action
  } finally {
    grantingCourse.value = false;
  }
};

const handleRevokeCourse = async (courseId, courseTitle) => {
  if (!selectedUser.value || !courseId) return;
  if (!window.confirm(`Bạn có chắc chắn muốn thu hồi quyền truy cập khóa học "${courseTitle || 'này'}" của học viên #${selectedUser.value.id} (${selectedUser.value.fullname})?`)) {
    return;
  }
  try {
    const ok = await courseStore.revokeAdminUserCourse(selectedUser.value.id, courseId);
    if (ok) {
      await loadUserCourses(selectedUser.value.id);
    }
  } catch (err) {
    // Toast already handled in action
  }
};

const viewUserDetails = (u) => {
  selectedUser.value = u;
  detailModalOpen.value = true;
  showGrantForm.value = false;
  selectedCourseToGrant.value = '';
  loadUserCourses(u.id);
  if (courseStore.courses.length === 0) {
    courseStore.fetchCourses();
  }
};

const openEditFromDetail = (u) => {
  detailModalOpen.value = false;
  editUserDetails(u);
};

const toggleUserStatusFromModal = async (u) => {
  await toggleUserStatus(u);
};

// CRUD User Modal States
const userModalOpen = ref(false);
const isEditingUser = ref(false);
const editingUserId = ref(null);
const userForm = ref({
  fullname: '',
  email: '',
  phone: '',
  password: '',
  role: 'student',
  referredById: null
});

const openAddUserModal = () => {
  isEditingUser.value = false;
  userForm.value = { fullname: '', email: '', phone: '', password: '', role: 'student', referredById: null };
  userModalOpen.value = true;
};

const editUserDetails = (u) => {
  isEditingUser.value = true;
  editingUserId.value = u.id;
  userForm.value = { 
    fullname: u.fullname, 
    email: u.email, 
    phone: u.phone || '', 
    role: u.role, 
    referredById: u.referredById,
    password: ''
  };
  userModalOpen.value = true;
};

const saveUser = async () => {
  try {
    if (isEditingUser.value) {
      if (userForm.value.password && userForm.value.password.trim() && userForm.value.password.trim().length < 6) {
        courseStore.showToast('Mật khẩu mới phải có tối thiểu 6 ký tự!', 'warning');
        return;
      }
      await courseStore.updateAdminUser(editingUserId.value, userForm.value);
      courseStore.showToast('Cập nhật thông tin học viên thành công!', 'success');
    } else {
      if (users.value.some(u => u.email === userForm.value.email)) {
        courseStore.showToast('Email này đã tồn tại trên hệ thống!', 'warning');
        return;
      }
      await courseStore.addAdminUser(userForm.value);
      courseStore.showToast('Thêm học viên mới thành công!', 'success');
    }
    userModalOpen.value = false;
  } catch (err) {
    courseStore.showToast(err.message || 'Không thể lưu học viên.', 'error');
  }
};

const deleteUser = async (userId) => {
  const isConfirmed = await courseStore.showConfirm({
    title: 'Xác nhận xóa học viên',
    message: 'Bạn có chắc chắn muốn xóa tài khoản học viên này khỏi hệ thống?',
    confirmText: 'Đồng ý xóa',
    cancelText: 'Hủy bỏ',
    type: 'danger'
  });

  const target = users.value.find(u => u.id === userId);
  if (target?.role === 'admin') {
    courseStore.showToast('Không thể xóa tài khoản Quản trị viên (Admin)!', 'warning');
    return;
  }

  if (isConfirmed) {
    try {
      await courseStore.deleteAdminUser(userId);
      courseStore.showToast('Đã xóa học viên thành công.', 'success');
      if (detailModalOpen.value && selectedUser.value?.id === userId) {
        detailModalOpen.value = false;
      }
    } catch (err) {
      courseStore.showToast(err.message || 'Không thể xóa học viên.', 'error');
    }
  }
};

const changeUserRole = async (userId, role) => {
  const target = users.value.find(u => u.id === userId);
  if (target?.role === 'admin' && role !== 'admin') {
    courseStore.showToast('Không thể giáng cấp tài khoản Quản trị viên (Admin)!', 'warning');
    return;
  }
  try {
    await courseStore.updateAdminUser(userId, { role });
    courseStore.showToast('Đã cập nhật vai trò người dùng thành công.', 'success');
  } catch (err) {
    courseStore.showToast(err.message || 'Không thể cập nhật vai trò.', 'error');
  }
};

const toggleUserStatus = async (u) => {
  if (u.role === 'admin') {
    courseStore.showToast('Không thể khóa tài khoản Quản trị viên (Admin)!', 'warning');
    return;
  }
  const originalStatus = u.isActive;
  // Optimistic update: UI changes immediately (0ms)
  u.isActive = !originalStatus;
  if (selectedUser.value && selectedUser.value.id === u.id) {
    selectedUser.value.isActive = u.isActive;
  }

  try {
    await courseStore.updateAdminUser(u.id, { isActive: u.isActive });
    courseStore.showToast(u.isActive ? 'Đã kích hoạt lại tài khoản học viên.' : 'Đã khóa tài khoản học viên.', 'success');
  } catch (err) {
    // Revert if API fails
    u.isActive = originalStatus;
    if (selectedUser.value && selectedUser.value.id === u.id) {
      selectedUser.value.isActive = originalStatus;
    }
    courseStore.showToast(err.message || 'Không thể thay đổi trạng thái.', 'error');
  }
};

const getReferrerName = (referredById) => {
  if (!referredById) return 'Không có';
  const parentUser = users.value.find(u => u.id === referredById);
  return parentUser ? `${parentUser.fullname} (#${parentUser.id})` : `#${referredById}`;
};

const getUserInitials = (name) => {
  if (!name) return 'U';
  const parts = name.trim().split(/\s+/);
  if (parts.length >= 2) {
    return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
  }
  return name.slice(0, 2).toUpperCase();
};

const formatDate = (isoStr) => {
  if (!isoStr) return '—';
  try {
    const d = new Date(isoStr);
    return d.toLocaleString('vi-VN', {
      hour: '2-digit',
      minute: '2-digit',
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  } catch {
    return isoStr;
  }
};

const formatCurrency = (val) => {
  return (val || 0).toLocaleString('vi-VN') + ' đ';
};

const copyReferral = (code) => {
  if (!code) return;
  navigator.clipboard.writeText(code);
  courseStore.showToast('Đã sao chép mã giới thiệu: ' + code, 'success');
};
</script>

<style scoped>
/* Compact Table Styles */
.user-compact-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
}

.user-cell-profile {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar-badge {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: linear-gradient(135deg, #022B9F 0%, #0284c7 100%);
  color: #ffffff;
  font-weight: 800;
  font-size: 13px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 2px 6px rgba(2, 43, 159, 0.2);
}

.user-meta-info {
  display: flex;
  flex-direction: column;
}

.user-fullname-text {
  font-weight: 700;
  color: #0f172a;
  font-size: 14.5px;
}

.user-id-sub {
  font-size: 12px;
  color: #64748b;
  font-weight: 500;
}

.user-contact-col {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.contact-email {
  font-size: 13.5px;
  color: #1e293b;
  font-weight: 500;
  max-width: 220px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.contact-phone {
  font-size: 12px;
}

.contact-phone.empty-phone {
  color: #94a3b8;
  font-style: italic;
}

.role-select {
  padding: 6px 10px;
  border-radius: 8px;
  font-size: 12.5px;
  font-weight: 600;
  border: 1px solid #cbd5e1;
  background: #f8fafc;
  color: #334155;
  cursor: pointer;
}

.role-select.role-admin {
  background: #eff6ff;
  border-color: #bfdbfe;
  color: #1d4ed8;
  font-weight: 700;
}

.role-select.role-student {
  background: #f1f5f9;
  border-color: #e2e8f0;
  color: #475569;
}

.role-admin-badge {
  display: inline-flex;
  align-items: center;
  padding: 5px 10px;
  border-radius: 8px;
  font-size: 12.5px;
  font-weight: 700;
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  color: #1d4ed8;
  user-select: none;
}

.status-admin-pill {
  display: inline-flex;
  align-items: center;
  padding: 5px 12px;
  border-radius: 9999px;
  font-size: 12px;
  font-weight: 700;
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  color: #15803d;
  user-select: none;
}

.action-buttons-wrap {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.btn-detail-pill {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 6px 12px;
  background: #f0f9ff;
  border: 1px solid #bae6fd;
  color: #0284c7;
  border-radius: 8px;
  font-size: 12.5px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-detail-pill:hover {
  background: #0284c7;
  color: #ffffff;
  border-color: #0284c7;
}

/* User Detail Modal Styling */
.user-detail-modal {
  max-width: 620px;
  width: 95%;
  padding: 28px;
}

.detail-header-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e2e8f0;
  position: relative;
}

.detail-avatar-wrap {
  width: 58px;
  height: 58px;
  border-radius: 50%;
  background: linear-gradient(135deg, #022B9F 0%, #0369a1 100%);
  color: #ffffff;
  font-size: 20px;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(2, 43, 159, 0.25);
  flex-shrink: 0;
}

.detail-title-wrap {
  flex: 1;
}

.detail-user-name {
  font-size: 20px;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 6px;
}

.detail-badges-row {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.detail-id-tag {
  font-size: 12px;
  color: #64748b;
  background: #f1f5f9;
  padding: 3px 8px;
  border-radius: 6px;
  font-weight: 600;
}

.detail-role-pill {
  font-size: 11.5px;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 6px;
}

.detail-role-pill.role-admin {
  background: #dbeafe;
  color: #1e40af;
}

.detail-role-pill.role-student {
  background: #f1f5f9;
  color: #475569;
}

.detail-status-pill {
  font-size: 11.5px;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 6px;
}

.detail-status-pill.active {
  background: #dcfce7;
  color: #166534;
}

.detail-status-pill.inactive {
  background: #fee2e2;
  color: #991b1b;
}

.detail-close-btn {
  background: #f1f5f9;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  font-size: 14px;
  color: #64748b;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.detail-close-btn:hover {
  background: #e2e8f0;
  color: #0f172a;
}

/* Detail Info Grid */
.detail-info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

@media (max-width: 600px) {
  .detail-info-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
}

.detail-info-col {
  background: #f8fafc;
  padding: 16px;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.detail-section-title {
  font-size: 13.5px;
  font-weight: 800;
  color: #334155;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  margin-top: 0;
  margin-bottom: 12px;
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 6px;
}

.detail-info-row {
  display: flex;
  flex-direction: column;
  margin-bottom: 10px;
  gap: 2px;
}

.detail-info-row:last-child {
  margin-bottom: 0;
}

.detail-label {
  font-size: 12px;
  color: #64748b;
  font-weight: 600;
}

.detail-value {
  font-size: 13.5px;
  color: #0f172a;
  word-break: break-word;
}

.flex-align-center {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.btn-copy-code {
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 13px;
  padding: 2px 4px;
}

.highlight-balance {
  font-weight: 800;
  color: #0284c7;
  font-size: 15px;
}

.btn-danger-outline {
  background: #fff1f2;
  border: 1px solid #fecdd3;
  color: #e11d48;
}

.btn-danger-outline:hover {
  background: #e11d48;
  color: #ffffff;
}

.btn-success-outline {
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  color: #16a34a;
}

.btn-success-outline:hover {
  background: #16a34a;
  color: #ffffff;
}

/* User Form Modal (Add/Edit) */
.user-form-modal {
  max-width: 680px;
  width: 95%;
  padding: 24px 28px;
}

.user-form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 16px;
  border-bottom: 1px solid #e2e8f0;
  margin-bottom: 20px;
}

.form-modal-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: #eff6ff;
  color: #022B9F;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}

.user-modal-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px 20px;
}

.form-label-custom {
  font-size: 13px;
  font-weight: 600;
  color: #334155;
  margin-bottom: 6px;
  display: block;
}

@media (max-width: 640px) {
  .user-modal-grid {
    grid-template-columns: 1fr;
    gap: 14px;
  }
}
</style>
