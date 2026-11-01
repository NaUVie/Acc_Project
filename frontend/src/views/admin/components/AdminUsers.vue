<template>
  <div class="tab-content animate-fade-in">
    <div class="content-header flex-between">
      <div>
        <h2>Quản lý Học viên</h2>
        <p>Danh sách thông tin học viên đăng ký trên hệ thống.</p>
      </div>
      <button @click="openAddUserModal" class="btn btn-primary btn-sm">+ Thêm học viên</button>
    </div>

    <!-- Filters -->
    <div class="filter-bar mt-4">
      <input 
        v-model="userSearch" 
        type="text" 
        placeholder="Tìm theo tên, email, mã giới thiệu..." 
        class="admin-search-input"
      />
      <select v-model="userFilterRole" class="admin-select">
        <option value="all">Tất cả vai trò</option>
        <option value="admin">Quản trị viên (Admin)</option>
        <option value="student">Học viên (Student)</option>
      </select>
    </div>

    <!-- Users Table -->
    <div class="table-responsive mt-6">
      <table class="admin-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Họ và tên</th>
            <th>Email</th>
            <th>Mã giới thiệu</th>
            <th>Được giới thiệu bởi</th>
            <th>Vai trò</th>
            <th>Trạng thái</th>
            <th>Hành động</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="u in paginatedUsers" :key="u.id">
            <td class="font-bold" data-label="ID">#{{ u.id }}</td>
            <td class="font-bold" data-label="Họ và tên">{{ u.fullname }}</td>
            <td data-label="Email">{{ u.email }}</td>
            <td data-label="Mã giới thiệu"><span class="code-tag">{{ u.referralCode }}</span></td>
            <td data-label="Được giới thiệu bởi">{{ getReferrerName(u.referredById) }}</td>
            <td data-label="Vai trò">
              <select 
                :value="u.role" 
                @change="changeUserRole(u.id, $event.target.value)"
                class="role-select"
              >
                <option value="student">Student</option>
                <option value="admin">Admin</option>
              </select>
            </td>
            <td data-label="Trạng thái">
              <button 
                @click="toggleUserStatus(u)"
                class="status-toggle-btn"
                :class="{ active: u.isActive }"
              >
                {{ u.isActive ? 'Đang hoạt động' : 'Đã khóa' }}
              </button>
            </td>
            <td data-label="Hành động">
              <div class="action-buttons">
                <button @click="editUserDetails(u)" class="btn-action edit" title="Chỉnh sửa">✏️</button>
                <button @click="deleteUser(u.id)" class="btn-action delete" title="Xóa">🗑️</button>
              </div>
            </td>
          </tr>
          <tr v-if="filteredUsers.length === 0">
            <td colspan="8" class="text-center py-8 text-muted">Không tìm thấy người dùng nào phù hợp.</td>
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

    <!-- ==================== MODAL: ADD/EDIT USER ==================== -->
    <div v-if="userModalOpen" class="modal-overlay">
      <div class="modal-content glass-card">
        <h3>{{ isEditingUser ? 'Chỉnh sửa học viên' : 'Thêm học viên mới' }}</h3>
        <form @submit.prevent="saveUser" class="mt-4">
          <div class="form-group">
            <label>Họ và tên</label>
            <input v-model="userForm.fullname" type="text" required class="admin-input-style" placeholder="Nguyễn Văn A" />
          </div>
          <div class="form-group mt-3">
            <label>Email đăng nhập</label>
            <input v-model="userForm.email" type="email" required class="admin-input-style" placeholder="example@gmail.com" :disabled="isEditingUser" />
          </div>
          <div class="form-group mt-3" v-if="!isEditingUser">
            <label>Mật khẩu khởi tạo</label>
            <input v-model="userForm.password" type="password" required class="admin-input-style" placeholder="******" />
          </div>
          <div class="form-group mt-3" v-else>
            <label>Đặt lại mật khẩu mới (Để trống nếu không đổi)</label>
            <input v-model="userForm.password" type="password" class="admin-input-style" placeholder="Nhập mật khẩu mới cho học viên (tối thiểu 6 ký tự)..." />
          </div>
          <div class="form-group mt-3">
            <label>Vai trò</label>
            <select v-model="userForm.role" class="admin-input-style">
              <option value="student">Student (Học viên)</option>
              <option value="admin">Admin (Quản trị viên)</option>
            </select>
          </div>
          <div class="form-group mt-3">
            <label>Người giới thiệu (Referrer)</label>
            <select v-model="userForm.referredById" class="admin-input-style">
              <option :value="null">-- Không có --</option>
              <option v-for="u in users.filter(usr => usr.id !== editingUserId)" :key="u.id" :value="u.id">
                {{ u.fullname }} ({{ u.email }})
              </option>
            </select>
          </div>

          <div class="modal-actions mt-6">
            <button type="button" @click="userModalOpen = false" class="btn btn-secondary btn-sm">Hủy</button>
            <button type="submit" class="btn btn-primary btn-sm">Lưu lại</button>
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

onMounted(async () => {
  await courseStore.fetchAdminUsers().catch(err => console.warn('fetchAdminUsers failed:', err));
});

const users = computed(() => courseStore.adminUsers);

const userSearch = ref('');
const userFilterRole = ref('all');
const currentPage = ref(1);
const pageSize = ref(10);

const filteredUsers = computed(() => {
  const query = (userSearch.value || '').toLowerCase().trim();
  return (users.value || []).filter(u => {
    const fullname = (u.fullname || '').toLowerCase();
    const email = (u.email || '').toLowerCase();
    const refCode = (u.referralCode || '').toLowerCase();
    const matchesSearch = !query || fullname.includes(query) || email.includes(query) || refCode.includes(query);
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

// CRUD User Modal States
const userModalOpen = ref(false);
const isEditingUser = ref(false);
const editingUserId = ref(null);
const userForm = ref({
  fullname: '',
  email: '',
  password: '',
  role: 'student',
  referredById: null
});

const openAddUserModal = () => {
  isEditingUser.value = false;
  userForm.value = { fullname: '', email: '', password: '', role: 'student', referredById: null };
  userModalOpen.value = true;
};

const editUserDetails = (u) => {
  isEditingUser.value = true;
  editingUserId.value = u.id;
  userForm.value = { 
    fullname: u.fullname, 
    email: u.email, 
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

  if (isConfirmed) {
    try {
      await courseStore.deleteAdminUser(userId);
      courseStore.showToast('Đã xóa học viên thành công.', 'success');
    } catch (err) {
      courseStore.showToast(err.message || 'Không thể xóa học viên.', 'error');
    }
  }
};

const changeUserRole = async (userId, role) => {
  try {
    await courseStore.updateAdminUser(userId, { role });
    courseStore.showToast('Đã cập nhật vai trò người dùng thành công.', 'success');
  } catch (err) {
    courseStore.showToast('Không thể cập nhật vai trò.', 'error');
  }
};

const toggleUserStatus = async (u) => {
  try {
    await courseStore.updateAdminUser(u.id, { isActive: !u.isActive });
    courseStore.showToast('Đã thay đổi trạng thái hoạt động học viên.', 'success');
  } catch (err) {
    courseStore.showToast('Không thể thay đổi trạng thái.', 'error');
  }
};

const getReferrerName = (referredById) => {
  if (!referredById) return '-';
  const parentUser = users.value.find(u => u.id === referredById);
  return parentUser ? `${parentUser.fullname} (#${parentUser.id})` : '-';
};
</script>
