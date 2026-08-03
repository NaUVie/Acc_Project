<template>
  <div class="tab-content animate-fade-in">
    <div class="content-header">
      <h2>Quản lý Lời nhắn Liên hệ</h2>
      <p>Danh sách các yêu cầu hỗ trợ và tư vấn lộ trình học của học viên tiềm năng.</p>
    </div>

    <!-- Contact Info Settings Panel -->
    <div class="glass-card mb-6" style="padding: 20px; border-radius: 12px; background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1);">
      <h3 class="font-bold mb-2 text-lg">Cấu hình thông tin liên hệ</h3>
      <p class="text-muted mb-4" style="font-size: 13px;">Các thông tin hiển thị tại trang Liên hệ (Địa chỉ, Email, Hotline, Zalo, Viber...).</p>
      
      <form @submit.prevent="saveSettings" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px;">
        <div class="form-group">
          <label style="display: block; font-weight: 500; margin-bottom: 5px; font-size: 13px;">Địa chỉ trụ sở chính</label>
          <input v-model="settingsData.address" type="text" class="form-control" placeholder="123 Điện Biên Phủ..." required style="width: 100%; padding: 8px 12px; border-radius: 6px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); color: #fff;">
        </div>
        
        <div class="form-group">
          <label style="display: block; font-weight: 500; margin-bottom: 5px; font-size: 13px;">Hotline điện thoại</label>
          <input v-model="settingsData.hotline" type="text" class="form-control" placeholder="090 ..." required style="width: 100%; padding: 8px 12px; border-radius: 6px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); color: #fff;">
        </div>
        
        <div class="form-group">
          <label style="display: block; font-weight: 500; margin-bottom: 5px; font-size: 13px;">Email liên hệ</label>
          <input v-model="settingsData.email" type="email" class="form-control" placeholder="support@..." required style="width: 100%; padding: 8px 12px; border-radius: 6px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); color: #fff;">
        </div>

        <div class="form-group">
          <label style="display: block; font-weight: 500; margin-bottom: 5px; font-size: 13px;">Zalo Link</label>
          <input v-model="settingsData.zalo" type="text" class="form-control" placeholder="https://zalo.me/..." style="width: 100%; padding: 8px 12px; border-radius: 6px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); color: #fff;">
        </div>

        <div class="form-group">
          <label style="display: block; font-weight: 500; margin-bottom: 5px; font-size: 13px;">Viber Link</label>
          <input v-model="settingsData.viber" type="text" class="form-control" placeholder="https://viber.click/..." style="width: 100%; padding: 8px 12px; border-radius: 6px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); color: #fff;">
        </div>

        <div style="grid-column: 1 / -1; text-align: right; margin-top: 10px;">
          <button type="submit" class="btn btn-primary" :disabled="savingSettings" style="padding: 8px 20px; font-size: 13px;">
            {{ savingSettings ? 'Đang lưu...' : 'Lưu cấu hình' }}
          </button>
        </div>
      </form>
    </div>

    <div class="filter-bar mt-4">
      <input 
        v-model="contactSearch" 
        type="text" 
        placeholder="Tìm theo tên, email, nội dung lời nhắn..." 
        class="admin-search-input"
      />
    </div>

    <!-- Contacts List -->
    <div class="contacts-list mt-6">
      <div 
        v-for="c in filteredContacts" 
        :key="c.id" 
        class="contact-message-card glass-card mb-4"
        :class="{ resolved: c.isResolved }"
      >
        <div class="contact-card-header">
          <div>
            <h4 class="font-bold">{{ c.lastName }} {{ c.middleName }} {{ c.firstName }}</h4>
            <small class="text-muted">✉️ Email: {{ c.email }} | 📞 SĐT: {{ c.phone }} | Dịch vụ quan tâm: <span class="badge badge-info">{{ translateCourseHandle(c.courseHandle) }}</span></small>
          </div>
          <div style="display: flex; gap: 8px;">
            <button 
              @click="toggleContactStatus(c.id)" 
              class="btn btn-sm"
              :class="c.isResolved ? 'btn-secondary' : 'btn-success'"
            >
              {{ c.isResolved ? 'Mở lại yêu cầu' : 'Đánh dấu đã xử lý' }}
            </button>
            <button @click="deleteContact(c.id)" class="btn btn-sm btn-danger">Xóa tin nhắn</button>
          </div>
        </div>
        <div class="contact-card-body mt-3">
          <p>{{ c.message }}</p>
          <small class="text-muted mt-2 block">Gửi lúc: {{ formatDate(c.createdAt) }}</small>
        </div>
      </div>
      <div v-if="filteredContacts.length === 0" class="text-center py-12 text-muted">
        Không có lời nhắn nào được tìm thấy.
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useCourseStore } from '@/stores/courses';

const courseStore = useCourseStore();

const settingsData = ref({
  address: '',
  hotline: '',
  email: '',
  zalo: '',
  viber: ''
});

const savingSettings = ref(false);

onMounted(async () => {
  await courseStore.fetchContactSettings();
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
    alert('Đã cập nhật cấu hình thông tin liên hệ thành công!');
  } catch (err) {
    alert('Lỗi khi lưu cấu hình: ' + err.message);
  } finally {
    savingSettings.value = false;
  }
};

const contacts = computed(() => courseStore.adminContacts);

const contactSearch = ref('');

const filteredContacts = computed(() => {
  return contacts.value.filter(c => {
    const searchVal = contactSearch.value.toLowerCase();
    const fullName = `${c.lastName} ${c.middleName} ${c.firstName}`.toLowerCase();
    return fullName.includes(searchVal) || 
           c.email.toLowerCase().includes(searchVal) ||
           c.phone.toLowerCase().includes(searchVal) ||
           c.message.toLowerCase().includes(searchVal);
  });
});

const toggleContactStatus = async (contactId) => {
  try {
    await courseStore.toggleContactResolved(contactId);
    alert('Đã cập nhật trạng thái liên hệ.');
  } catch (err) {
    alert(err.message || 'Không thể cập nhật liên hệ.');
  }
};

const deleteContact = async (contactId) => {
  if (confirm('Bạn có chắc chắn muốn xóa tin nhắn liên hệ này?')) {
    try {
      await courseStore.deleteAdminContact(contactId);
      alert('Đã xóa tin nhắn liên hệ thành công.');
    } catch (err) {
      alert(err.message || 'Không thể xóa liên hệ.');
    }
  }
};

// Helpers
const formatDate = (dateStr) => {
  if (!dateStr) return '';
  const d = new Date(dateStr);
  return d.toLocaleString('vi-VN');
};

const translateCourseHandle = (handle) => {
  switch (handle) {
    case 'chatgpt-work-automation': return 'ChatGPT & AI Automation';
    case 'ai-center-of-excellence': return 'AI Center of Excellence';
    default: return handle;
  }
};
</script>
