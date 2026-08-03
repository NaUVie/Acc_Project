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
          <tr v-for="u in filteredUsers" :key="u.id">
            <td class="font-bold">#{{ u.id }}</td>
            <td class="font-bold">{{ u.fullname }}</td>
            <td>{{ u.email }}</td>
            <td><span class="code-tag">{{ u.referralCode }}</span></td>
            <td>{{ getReferrerName(u.referredById) }}</td>
            <td>
              <select 
                :value="u.role" 
                @change="changeUserRole(u.id, $event.target.value)"
                class="role-select"
              >
                <option value="student">Student</option>
                <option value="admin">Admin</option>
              </select>
            </td>
            <td>
              <button 
                @click="toggleUserStatus(u)"
                class="status-toggle-btn"
                :class="{ active: u.isActive }"
              >
                {{ u.isActive ? 'Đang hoạt động' : 'Đã khóa' }}
              </button>
            </td>
            <td>
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
import { ref, computed } from 'vue';
import { useCourseStore } from '@/stores/courses';

const courseStore = useCourseStore();

const users = computed(() => courseStore.adminUsers);

const userSearch = ref('');
const userFilterRole = ref('all');

const filteredUsers = computed(() => {
  return users.value.filter(u => {
    const matchesSearch = u.fullname.toLowerCase().includes(userSearch.value.toLowerCase()) || 
                          u.email.toLowerCase().includes(userSearch.value.toLowerCase()) ||
                          u.referralCode.toLowerCase().includes(userSearch.value.toLowerCase());
    const matchesRole = userFilterRole.value === 'all' || u.role === userFilterRole.value;
    return matchesSearch && matchesRole;
  });
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
    referredById: u.referredById 
  };
  userModalOpen.value = true;
};

const saveUser = async () => {
  try {
    if (isEditingUser.value) {
      await courseStore.updateAdminUser(editingUserId.value, userForm.value);
      alert('Cập nhật thông tin học viên thành công!');
    } else {
      if (users.value.some(u => u.email === userForm.value.email)) {
        alert('Email này đã tồn tại trên hệ thống!');
        return;
      }
      await courseStore.addAdminUser(userForm.value);
      alert('Thêm học viên mới thành công!');
    }
    userModalOpen.value = false;
  } catch (err) {
    alert(err.message || 'Không thể lưu học viên.');
  }
};

const deleteUser = async (userId) => {
  if (confirm('Bạn có chắc chắn muốn xóa học viên này khỏi hệ thống?')) {
    try {
      await courseStore.deleteAdminUser(userId);
      alert('Đã xóa học viên thành công.');
    } catch (err) {
      alert(err.message || 'Không thể xóa học viên.');
    }
  }
};

const changeUserRole = async (userId, role) => {
  try {
    await courseStore.updateAdminUser(userId, { role });
    alert('Đã cập nhật vai trò người dùng thành công.');
  } catch (err) {
    alert('Không thể cập nhật vai trò.');
  }
};

const toggleUserStatus = async (u) => {
  try {
    await courseStore.updateAdminUser(u.id, { isActive: !u.isActive });
    alert('Đã thay đổi trạng thái hoạt động học viên.');
  } catch (err) {
    alert('Không thể thay đổi trạng thái.');
  }
};

const getReferrerName = (referredById) => {
  if (!referredById) return '-';
  const parentUser = users.value.find(u => u.id === referredById);
  return parentUser ? `${parentUser.fullname} (#${parentUser.id})` : '-';
};
</script>
