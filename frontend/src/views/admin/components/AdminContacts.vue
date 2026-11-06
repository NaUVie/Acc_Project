<template>
  <div class="tab-content animate-fade-in">
    <!-- Header Section -->
    <div class="content-header flex-between" style="flex-wrap: wrap; gap: 12px; margin-bottom: 20px;">
      <div>
        <h2>Quản lý Lời nhắn Liên hệ</h2>
        <p>Danh sách các yêu cầu hỗ trợ và tư vấn lộ trình học của học viên tiềm năng.</p>
      </div>
      <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
        <!-- Toggle Contact Settings Button -->
        <button 
          @click="isSettingsOpen = !isSettingsOpen" 
          class="btn btn-sm"
          :style="isSettingsOpen ? 'background: #022B9F; color: #ffffff; border: 1.5px solid #022B9F;' : 'background: #ffffff; color: #022B9F; border: 1.5px solid #bfdbfe;'"
          style="display: flex; align-items: center; gap: 6px; font-weight: 700; padding: 8px 16px; border-radius: 8px; transition: all 0.2s;"
          title="Ẩn / Hiện khung cấu hình thông tin liên hệ website"
        >
          <span>⚙️</span>
          <span>{{ isSettingsOpen ? 'Thu gọn cấu hình ▲' : 'Cấu hình thông tin liên hệ ▼' }}</span>
        </button>

        <!-- Refresh Button -->
        <button 
          @click="refreshContacts" 
          :disabled="isRefreshing" 
          class="btn btn-secondary btn-sm" 
          style="display: flex; align-items: center; gap: 6px; font-weight: 600; padding: 8px 16px;" 
          title="Tải lại danh sách liên hệ mới nhất từ máy chủ"
        >
          <span :class="{ 'spin-icon': isRefreshing }">🔄</span>
          <span>{{ isRefreshing ? 'Đang đồng bộ...' : 'Làm mới dữ liệu' }}</span>
        </button>
      </div>
    </div>

    <!-- Quick Info Strip when Collapsed -->
    <div v-if="!isSettingsOpen" class="quick-settings-strip glass-card mb-5">
      <div class="quick-settings-info">
        <span class="info-item">📍 <strong>Trụ sở:</strong> {{ settingsData.address || 'Chưa thiết lập' }}</span>
        <span class="info-item">📞 <strong>Hotline:</strong> {{ settingsData.hotline || 'Chưa thiết lập' }}</span>
        <span class="info-item">✉️ <strong>Email:</strong> {{ settingsData.email || 'Chưa thiết lập' }}</span>
      </div>
      <button type="button" @click="isSettingsOpen = true" class="btn-quick-edit">
        ✏️ Chỉnh sửa thông tin liên hệ
      </button>
    </div>

    <!-- Contact Info Settings Panel (Collapsible) -->
    <Transition name="fade-slide">
      <div 
        v-if="isSettingsOpen" 
        class="glass-card mb-6 settings-panel-box"
      >
        <div class="settings-panel-header">
          <div>
            <h3 class="font-bold text-lg" style="color: #0f172a; margin: 0 0 4px 0;">Cấu hình thông tin liên hệ Website</h3>
            <p style="font-size: 13px; color: #64748b; margin: 0;">Các thông tin hiển thị tại trang Liên hệ, Chân trang (Footer) & Nút hỗ trợ nhanh.</p>
          </div>
          <button type="button" @click="isSettingsOpen = false" class="btn-close-settings" title="Thu gọn">
            &times;
          </button>
        </div>
        
        <form @submit.prevent="saveSettings" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; margin-top: 18px;">
          <div class="form-group">
            <label class="form-label">Địa chỉ trụ sở chính *</label>
            <input v-model="settingsData.address" type="text" class="admin-input-style" placeholder="156 Nam Kỳ Khởi Nghĩa..." required>
          </div>
          
          <div class="form-group">
            <label class="form-label">Hotline điện thoại *</label>
            <input v-model="settingsData.hotline" type="text" class="admin-input-style" placeholder="0938 566 700" required>
          </div>
          
          <div class="form-group">
            <label class="form-label">Email liên hệ *</label>
            <input v-model="settingsData.email" type="email" class="admin-input-style" placeholder="info@acc-edu.vn" required>
          </div>

          <div class="form-group">
            <label class="form-label">Liên kết Zalo (URL)</label>
            <input v-model="settingsData.zalo" type="text" class="admin-input-style" placeholder="https://zalo.me/0938566700">
          </div>

          <div class="form-group">
            <label class="form-label">Liên kết Viber (URL)</label>
            <input v-model="settingsData.viber" type="text" class="admin-input-style" placeholder="https://viber.click/0938566700">
          </div>

          <div class="settings-actions-bar">
            <button type="button" @click="isSettingsOpen = false" class="btn btn-secondary btn-sm" style="padding: 10px 18px; font-weight: 600;">
              Thu gọn
            </button>
            <button type="submit" class="btn btn-primary" :disabled="savingSettings" style="padding: 10px 24px; font-size: 14px; font-weight: 700;">
              {{ savingSettings ? 'Đang lưu...' : 'Lưu cấu hình' }}
            </button>
          </div>
        </form>
      </div>
    </Transition>

    <!-- Filter Bar: Search + Status Tabs -->
    <div class="contacts-toolbar glass-card mb-5">
      <!-- Status Pills -->
      <div class="filter-pills-row">
        <button 
          type="button"
          class="filter-pill-btn"
          :class="{ active: contactFilterStatus === 'all' }"
          @click="contactFilterStatus = 'all'"
        >
          Tất cả <span class="pill-badge">{{ contacts.length }}</span>
        </button>
        <button 
          type="button"
          class="filter-pill-btn pill-pending"
          :class="{ active: contactFilterStatus === 'pending' }"
          @click="contactFilterStatus = 'pending'"
        >
          Chưa xử lý <span class="pill-badge pending">{{ unresolvedCount }}</span>
        </button>
        <button 
          type="button"
          class="filter-pill-btn pill-resolved"
          :class="{ active: contactFilterStatus === 'resolved' }"
          @click="contactFilterStatus = 'resolved'"
        >
          Đã xử lý <span class="pill-badge resolved">{{ resolvedCount }}</span>
        </button>
      </div>

      <!-- Search Input -->
      <div class="search-input-wrap">
        <input 
          v-model="contactSearch" 
          type="text" 
          placeholder="Tìm theo tên, email, SĐT, nội dung..." 
          class="admin-search-input"
        />
        <button v-if="contactSearch" @click="contactSearch = ''" class="btn-clear-search" title="Xóa tìm kiếm">&times;</button>
      </div>
    </div>

    <!-- Contacts List -->
    <div class="contacts-list">
      <div 
        v-for="c in paginatedContacts" 
        :key="c.id" 
        class="contact-message-card glass-card mb-4"
        :class="{ resolved: c.isResolved }"
      >
        <div class="contact-card-header">
          <div>
            <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap; margin-bottom: 4px;">
              <h4 class="font-bold" style="font-size: 16px; margin: 0; color: #0f172a;">
                {{ c.lastName }} {{ c.middleName }} {{ c.firstName }}
              </h4>
              <span class="status-chip" :class="c.isResolved ? 'chip-success' : 'chip-warning'">
                {{ c.isResolved ? '✓ Đã xử lý' : '⏳ Chờ xử lý' }}
              </span>
            </div>
            <div class="contact-sub-details">
              <span>✉️ <a :href="'mailto:' + c.email">{{ c.email }}</a></span>
              <span>📞 <a :href="'tel:' + c.phone" style="font-weight: 700;">{{ c.phone }}</a></span>
              <span>🎓 Dịch vụ quan tâm: <strong class="badge-topic">{{ translateCourseHandle(c.courseHandle) }}</strong></span>
            </div>
          </div>
          <div class="contact-card-actions">
            <button 
              @click="toggleContactStatus(c.id)" 
              class="btn btn-sm"
              :class="c.isResolved ? 'btn-secondary' : 'btn-success'"
              style="font-weight: 600;"
            >
              {{ c.isResolved ? 'Mở lại yêu cầu' : 'Đánh dấu đã xử lý' }}
            </button>
            <button @click="deleteContact(c.id)" class="btn btn-sm btn-danger" style="font-weight: 600;">
              Xóa
            </button>
          </div>
        </div>
        <div class="contact-card-body mt-3">
          <p class="contact-msg-text">{{ c.message }}</p>
          <small class="text-muted mt-2 block" style="font-size: 12.5px;">🕒 Gửi lúc: {{ formatDate(c.createdAt) }}</small>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="filteredContacts.length === 0" class="text-center py-12 text-muted glass-card" style="padding: 40px; border-radius: 12px; background: #fff;">
        <span style="font-size: 32px; display: block; margin-bottom: 8px;">📭</span>
        <p style="font-size: 15px; margin: 0;">Không tìm thấy lời nhắn liên hệ nào phù hợp với bộ lọc.</p>
      </div>
    </div>

    <!-- Pagination & Page Size Control Footer -->
    <div class="pagination-footer-wrapper glass-card mt-6">
      <div class="pagination-stats text-muted">
        Hiển thị <strong>{{ startItemIndex }}</strong> - <strong>{{ endItemIndex }}</strong> trên tổng số <strong>{{ filteredContacts.length }}</strong> liên hệ
        <span v-if="totalPages > 1"> (Trang {{ currentPage }}/{{ totalPages }})</span>
      </div>

      <div class="pagination-controls-group">
        <!-- Page size selector -->
        <div class="page-size-selector">
          <span>Hiển thị:</span>
          <select v-model.number="pageSize" class="page-size-select">
            <option :value="5">5 / trang</option>
            <option :value="10">10 / trang</option>
            <option :value="20">20 / trang</option>
            <option :value="50">50 / trang</option>
          </select>
        </div>

        <!-- Pagination Component -->
        <Pagination 
          v-if="filteredContacts.length > pageSize"
          v-model:currentPage="currentPage"
          :totalItems="filteredContacts.length"
          :pageSize="pageSize"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useCourseStore } from '@/stores/courses';
import Pagination from '@/components/Pagination.vue';

const courseStore = useCourseStore();

// Contact Settings Panel State
const isSettingsOpen = ref(false);
const savingSettings = ref(false);
const isRefreshing = ref(false);

const settingsData = ref({
  address: '',
  hotline: '',
  email: '',
  zalo: '',
  viber: ''
});

// Refresh Handler
const refreshContacts = async () => {
  isRefreshing.value = true;
  try {
    await Promise.all([
      courseStore.fetchAdminContacts(true),
      courseStore.fetchContactSettings(true)
    ]);
    courseStore.showToast('Đã đồng bộ danh sách liên hệ mới nhất!', 'success');
  } catch (err) {
    courseStore.showToast('Lỗi khi làm mới: ' + (err.message || err), 'error');
  } finally {
    isRefreshing.value = false;
  }
};

onMounted(async () => {
  await Promise.all([
    courseStore.fetchContactSettings(),
    courseStore.fetchAdminContacts()
  ]);
  if (courseStore.contactSettings) {
    settingsData.value = {
      address: courseStore.contactSettings.address || '',
      hotline: courseStore.contactSettings.hotline || '',
      email: courseStore.contactSettings.email || '',
      zalo: courseStore.contactSettings.zalo || '',
      viber: courseStore.contactSettings.viber || ''
    };
  }
});

const saveSettings = async () => {
  savingSettings.value = true;
  try {
    await courseStore.updateContactSettings(settingsData.value);
    courseStore.showToast('Đã cập nhật cấu hình thông tin liên hệ thành công!', 'success');
  } catch (err) {
    courseStore.showToast('Lỗi khi lưu cấu hình: ' + err.message, 'error');
  } finally {
    savingSettings.value = false;
  }
};

// Contacts List & Filtering
const contacts = computed(() => courseStore.adminContacts || []);

const contactSearch = ref('');
const contactFilterStatus = ref('all'); // 'all' | 'pending' | 'resolved'
const currentPage = ref(1);
const pageSize = ref(10);

const unresolvedCount = computed(() => {
  return contacts.value.filter(c => !c.isResolved).length;
});

const resolvedCount = computed(() => {
  return contacts.value.filter(c => c.isResolved).length;
});

const filteredContacts = computed(() => {
  const searchVal = (contactSearch.value || '').toLowerCase().trim();
  const statusFilter = contactFilterStatus.value;

  return contacts.value.filter(c => {
    // Status filter
    if (statusFilter === 'pending' && c.isResolved) return false;
    if (statusFilter === 'resolved' && !c.isResolved) return false;

    // Search filter
    if (!searchVal) return true;
    const fullName = [c.lastName, c.middleName, c.firstName].filter(Boolean).join(' ').toLowerCase();
    const email = (c.email || '').toLowerCase();
    const phone = (c.phone || '').toLowerCase();
    const message = (c.message || '').toLowerCase();
    const courseHandle = (c.courseHandle || '').toLowerCase();
    return fullName.includes(searchVal) || 
           email.includes(searchVal) || 
           phone.includes(searchVal) || 
           message.includes(searchVal) ||
           courseHandle.includes(searchVal);
  });
});

const totalPages = computed(() => {
  return Math.ceil(filteredContacts.value.length / pageSize.value) || 1;
});

const startItemIndex = computed(() => {
  if (filteredContacts.value.length === 0) return 0;
  return (currentPage.value - 1) * pageSize.value + 1;
});

const endItemIndex = computed(() => {
  return Math.min(currentPage.value * pageSize.value, filteredContacts.value.length);
});

const paginatedContacts = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  return filteredContacts.value.slice(start, start + pageSize.value);
});

watch([contactSearch, contactFilterStatus, pageSize], () => {
  currentPage.value = 1;
});

const toggleContactStatus = async (contactId) => {
  try {
    await courseStore.toggleContactResolved(contactId);
    courseStore.showToast('Đã cập nhật trạng thái liên hệ.', 'success');
  } catch (err) {
    courseStore.showToast(err.message || 'Không thể cập nhật liên hệ.', 'error');
  }
};

const deleteContact = async (contactId) => {
  const isConfirmed = await courseStore.showConfirm({
    title: 'Xác nhận xóa liên hệ',
    message: 'Bạn có chắc chắn muốn xóa lời nhắn liên hệ này khỏi hệ thống?',
    confirmText: 'Đồng ý xóa',
    cancelText: 'Hủy bỏ',
    type: 'danger'
  });

  if (isConfirmed) {
    try {
      await courseStore.deleteAdminContact(contactId);
      courseStore.showToast('Đã xóa tin nhắn liên hệ thành công.', 'success');
    } catch (err) {
      courseStore.showToast(err.message || 'Không thể xóa liên hệ.', 'error');
    }
  }
};

// Formatting helpers
const formatDate = (dateStr) => {
  if (!dateStr) return '';
  const d = new Date(dateStr);
  return d.toLocaleString('vi-VN');
};

const translateCourseHandle = (handle) => {
  if (!handle) return 'Tư vấn thông tin chung';
  const clean = handle.trim().toLowerCase();
  const map = {
    'individual': 'Đào tạo cho cá nhân',
    'corporate': 'Đào tạo cho doanh nghiệp',
    'postgraduate': 'Tuyển sinh sau đại học',
    'consultation-popup': 'Popup Tư vấn Trang Chủ',
    'course-register': 'Đăng ký tư vấn khóa học',
    'lien-he': 'Liên hệ chung',
    'chatgpt-work-automation': 'ChatGPT & AI Automation',
    'ai-center-of-excellence': 'AI Center of Excellence'
  };
  return map[clean] || handle;
};
</script>

<style scoped>
.quick-settings-strip {
  padding: 12px 18px;
  border-radius: 10px;
  background: #f8fafc;
  border: 1px dashed #cbd5e1;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
}
.quick-settings-info {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  font-size: 13px;
  color: #475569;
}
.btn-quick-edit {
  background: transparent;
  border: none;
  color: #022B9F;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  text-decoration: underline;
  padding: 0;
}
.btn-quick-edit:hover {
  color: #0284c7;
}

.settings-panel-box {
  padding: 22px 24px;
  border-radius: 12px;
  background: #ffffff;
  border: 1.5px solid #bfdbfe;
  box-shadow: 0 4px 16px rgba(2, 43, 159, 0.06);
}
.settings-panel-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  border-bottom: 1px solid #f1f5f9;
  padding-bottom: 12px;
}
.btn-close-settings {
  background: transparent;
  border: none;
  font-size: 24px;
  color: #94a3b8;
  cursor: pointer;
  padding: 0 4px;
  line-height: 1;
}
.btn-close-settings:hover {
  color: #0f172a;
}
.form-label {
  display: block;
  font-weight: 600;
  margin-bottom: 6px;
  font-size: 13px;
  color: #1e293b;
}
.settings-actions-bar {
  grid-column: 1 / -1;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 10px;
  padding-top: 12px;
  border-top: 1px solid #f1f5f9;
}

.contacts-toolbar {
  padding: 14px 18px;
  border-radius: 12px;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 14px;
}
.filter-pills-row {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap;
}
.filter-pill-btn {
  padding: 6px 14px;
  border-radius: 20px;
  border: 1px solid #cbd5e1;
  background: #ffffff;
  color: #475569;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s ease;
}
.filter-pill-btn:hover {
  background: #f8fafc;
  border-color: #94a3b8;
}
.filter-pill-btn.active {
  background: #022B9F;
  color: #ffffff;
  border-color: #022B9F;
}
.pill-badge {
  padding: 1px 7px;
  border-radius: 10px;
  font-size: 11.5px;
  font-weight: 700;
  background: #e2e8f0;
  color: #334155;
}
.filter-pill-btn.active .pill-badge {
  background: rgba(255, 255, 255, 0.25);
  color: #ffffff;
}
.pill-badge.pending {
  background: #fef3c7;
  color: #b45309;
}
.pill-badge.resolved {
  background: #dcfce7;
  color: #15803d;
}

.search-input-wrap {
  position: relative;
  display: flex;
  align-items: center;
  flex: 1;
  min-width: 260px;
  max-width: 420px;
}
.search-input-wrap .admin-search-input {
  width: 100%;
  padding-right: 30px;
}
.btn-clear-search {
  position: absolute;
  right: 10px;
  background: transparent;
  border: none;
  color: #94a3b8;
  font-size: 18px;
  cursor: pointer;
}

.status-chip {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 12px;
  font-size: 11.5px;
  font-weight: 700;
}
.chip-success {
  background: #dcfce7;
  color: #15803d;
  border: 1px solid #bbf7d0;
}
.chip-warning {
  background: #fef3c7;
  color: #b45309;
  border: 1px solid #fde68a;
}

.contact-sub-details {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
  font-size: 13px;
  color: #64748b;
  margin-top: 4px;
}
.contact-sub-details a {
  color: #022B9F;
  text-decoration: none;
}
.contact-sub-details a:hover {
  text-decoration: underline;
}
.badge-topic {
  background: #eff6ff;
  color: #022B9F;
  padding: 2px 8px;
  border-radius: 6px;
  font-size: 12px;
  border: 1px solid #bfdbfe;
}
.contact-msg-text {
  font-size: 14px;
  line-height: 1.6;
  color: #1e293b;
  background: #f8fafc;
  padding: 12px 16px;
  border-radius: 8px;
  border-left: 3px solid #022B9F;
  margin: 0;
  white-space: pre-wrap;
}

.pagination-footer-wrapper {
  padding: 14px 20px;
  border-radius: 12px;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 15px;
}
.pagination-controls-group {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}
.page-size-selector {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #475569;
}
.page-size-select {
  padding: 5px 10px;
  border-radius: 6px;
  border: 1.5px solid #cbd5e1;
  background: #ffffff;
  font-size: 13px;
  font-weight: 600;
  color: #0f172a;
  cursor: pointer;
}
.page-size-select:focus {
  outline: none;
  border-color: #022B9F;
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.25s ease-out;
}
.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
