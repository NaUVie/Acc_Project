<template>
  <div class="tab-content animate-fade-in">
    <!-- VIEW 1: LIST TABLE -->
    <div v-if="activeView === 'list'">
      <div class="content-header flex-between">
        <div>
          <h2>Quản lý Banner (Hero Carousel)</h2>
          <p>Tùy chỉnh các banner quảng cáo và hình ảnh trình chiếu trên trang chủ.</p>
        </div>
        <button @click="openAddModal" class="btn btn-primary btn-sm">+ Thêm Banner mới</button>
      </div>

      <!-- Banners Table -->
      <div class="table-responsive mt-6">
        <table class="admin-table">
          <thead>
            <tr>
              <th style="width: 60px;">Vị trí</th>
              <th>Preview Banner</th>
              <th>Tiêu đề & Link</th>
              <th>Loại Link</th>
              <th>Trạng thái</th>
              <th>Hành động</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="b in banners" :key="b.id">
              <td class="font-bold text-center">
                <span class="badge" style="background: #e0f2fe; color: #0369a1; font-weight: 700; padding: 4px 10px; border-radius: 6px;">
                  #{{ b.position }}
                </span>
              </td>
              <td>
                <div style="display: flex; gap: 8px; align-items: center;">
                  <img :src="b.desktop_image" :alt="b.title" class="admin-course-thumb" style="width: 120px; height: 60px; object-fit: cover; border-radius: 8px; border: 1px solid #cbd5e1;" />
                  <img v-if="b.mobile_image" :src="b.mobile_image" alt="Mobile" class="admin-course-thumb" style="width: 35px; height: 60px; object-fit: cover; border-radius: 8px; border: 1px solid #cbd5e1;" title="Mobile Image" />
                </div>
              </td>
              <td>
                <div class="font-bold" style="color: #0f172a; font-size: 15px;">{{ b.title }}</div>
                <small class="text-muted" style="word-break: break-all; display: block; margin-top: 2px;">
                  🔗 {{ b.link || '(Không có)' }}
                </small>
              </td>
              <td>
                <span class="badge" :style="b.is_external ? 'background: #fef3c7; color: #b45309;' : 'background: #f1f5f9; color: #475569;'">
                  {{ b.is_external ? '🌐 Ngoại bộ' : '🏠 Nội bộ' }}
                </span>
              </td>
              <td>
                <button 
                  @click="toggleActive(b)" 
                  class="badge" 
                  :style="b.is_active ? 'background: #dcfce7; color: #15803d; border: none; cursor: pointer; padding: 6px 12px;' : 'background: #fee2e2; color: #b91c1c; border: none; cursor: pointer; padding: 6px 12px;'"
                  title="Nhấn để đổi trạng thái"
                >
                  {{ b.is_active ? '🟢 Đang hiển thị' : '🔴 Đã ẩn' }}
                </button>
              </td>
              <td>
                <div class="action-buttons">
                  <button @click="editBanner(b)" class="btn-action edit" title="Sửa Banner">✏️</button>
                  <button @click="deleteBannerItem(b.id)" class="btn-action delete" title="Xóa Banner">🗑️</button>
                </div>
              </td>
            </tr>
            <tr v-if="banners.length === 0">
              <td colspan="6" class="text-center py-8 text-muted">Chưa có banner nào. Hãy nhấn "+ Thêm Banner mới".</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- VIEW 2: FORM ADD/EDIT -->
    <div v-else-if="activeView === 'form'" class="admin-page-card" style="background: #ffffff; color: #0f172a; border-radius: 16px; padding: 28px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); border: 1px solid #e2e8f0;">
      <div class="flex-between pb-4 mb-4" style="border-bottom: 1px solid #e2e8f0;">
        <div style="display: flex; align-items: center; gap: 12px;">
          <button type="button" @click="activeView = 'list'" class="btn btn-secondary btn-sm" style="padding: 8px 16px; font-weight: 600;">
            ← Quay lại danh sách
          </button>
          <h3 style="margin: 0; color: #0f172a; font-size: 20px; font-weight: 800;">
            {{ isEditing ? 'Chỉnh sửa Banner' : 'Thêm Banner mới' }}
          </h3>
        </div>
        <button type="button" @click="activeView = 'list'" class="btn btn-secondary btn-sm">Hủy</button>
      </div>

      <form @submit.prevent="saveBanner" class="mt-2">
        <div class="form-group">
          <label style="color: #1e293b; font-weight: 600;">Tiêu đề Banner</label>
          <input v-model="form.title" type="text" required class="admin-input-style" placeholder="Ví dụ: AI Center of Excellence" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
        </div>

        <div class="grid grid-2 gap-4 mt-4">
          <div class="form-group">
            <label style="color: #1e293b; font-weight: 600;">Ảnh Desktop (Yêu cầu)</label>
            <div style="display: flex; gap: 8px; margin-top: 4px;">
              <input v-model="form.desktop_image" type="text" required class="admin-input-style" placeholder="/images/CoE-Web.png hoặc URL" style="flex: 1; background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
              <input type="file" ref="desktopFileRef" @change="uploadImage($event, 'desktop_image')" style="display: none;" accept="image/*" />
              <button type="button" @click="$refs.desktopFileRef.click()" class="btn btn-secondary btn-sm">Upload</button>
            </div>
            <img v-if="form.desktop_image" :src="form.desktop_image" alt="Preview Desktop" style="margin-top: 8px; max-height: 100px; border-radius: 8px; border: 1px solid #e2e8f0; object-fit: cover;" />
          </div>

          <div class="form-group">
            <label style="color: #1e293b; font-weight: 600;">Ảnh Mobile (Tùy chọn)</label>
            <div style="display: flex; gap: 8px; margin-top: 4px;">
              <input v-model="form.mobile_image" type="text" class="admin-input-style" placeholder="/images/CoE-Mobile.png hoặc URL" style="flex: 1; background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
              <input type="file" ref="mobileFileRef" @change="uploadImage($event, 'mobile_image')" style="display: none;" accept="image/*" />
              <button type="button" @click="$refs.mobileFileRef.click()" class="btn btn-secondary btn-sm">Upload</button>
            </div>
            <img v-if="form.mobile_image" :src="form.mobile_image" alt="Preview Mobile" style="margin-top: 8px; max-height: 100px; border-radius: 8px; border: 1px solid #e2e8f0; object-fit: cover;" />
          </div>
        </div>

        <div class="grid grid-2 gap-4 mt-4">
          <div class="form-group">
            <label style="color: #1e293b; font-weight: 600;">Đường dẫn Liên kết (Link)</label>
            <input v-model="form.link" type="text" class="admin-input-style" placeholder="Ví dụ: /corporate/coe hoặc https://..." style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
          </div>

          <div class="form-group">
            <label style="color: #1e293b; font-weight: 600;">Thứ tự hiển thị (Position)</label>
            <input v-model.number="form.position" type="number" min="0" class="admin-input-style" placeholder="1, 2, 3..." style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
          </div>
        </div>

        <div class="grid grid-2 gap-4 mt-4" style="background: #f8fafc; padding: 16px; border-radius: 10px; border: 1px solid #e2e8f0;">
          <div class="form-group" style="display: flex; align-items: center; gap: 10px; margin: 0;">
            <input v-model="form.is_external" type="checkbox" id="is_external" style="width: 18px; height: 18px; cursor: pointer;" />
            <label for="is_external" style="color: #1e293b; font-weight: 600; cursor: pointer; margin: 0;">
              Mở link trong tab mới (Trang ngoài / External Link)
            </label>
          </div>

          <div class="form-group" style="display: flex; align-items: center; gap: 10px; margin: 0;">
            <input v-model="form.is_active" type="checkbox" id="is_active" style="width: 18px; height: 18px; cursor: pointer;" />
            <label for="is_active" style="color: #1e293b; font-weight: 600; cursor: pointer; margin: 0;">
              Hiển thị Banner này trên trang chủ (Active)
            </label>
          </div>
        </div>

        <div class="mt-6 flex-end" style="gap: 12px; border-top: 1px solid #e2e8f0; padding-top: 20px;">
          <button type="button" @click="activeView = 'list'" class="btn btn-secondary">Hủy</button>
          <button type="submit" class="btn btn-primary" :disabled="saving">
            {{ saving ? 'Đang lưu...' : (isEditing ? 'Cập nhật Banner' : 'Tạo Banner') }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useCourseStore } from '@/stores/courses';

const courseStore = useCourseStore();

const activeView = ref('list');
const isEditing = ref(false);
const editingId = ref(null);
const saving = ref(false);

const form = ref({
  title: '',
  desktop_image: '',
  mobile_image: '',
  link: '',
  is_external: false,
  position: 1,
  is_active: true
});

const banners = computed(() => courseStore.adminBanners);

onMounted(async () => {
  try {
    await courseStore.fetchAdminBanners();
  } catch (err) {
    console.error("Error loading admin banners:", err);
  }
});

const openAddModal = () => {
  isEditing.value = false;
  editingId.value = null;
  form.value = {
    title: '',
    desktop_image: '',
    mobile_image: '',
    link: '',
    is_external: false,
    position: (banners.value.length || 0) + 1,
    is_active: true
  };
  activeView.value = 'form';
};

const editBanner = (b) => {
  isEditing.value = true;
  editingId.value = b.id;
  form.value = {
    title: b.title,
    desktop_image: b.desktop_image,
    mobile_image: b.mobile_image || '',
    link: b.link || '',
    is_external: !!b.is_external,
    position: b.position || 1,
    is_active: !!b.is_active
  };
  activeView.value = 'form';
};

const toggleActive = async (b) => {
  try {
    await courseStore.updateBanner(b.id, { is_active: !b.is_active });
    courseStore.showToast(`Đã ${!b.is_active ? 'bật' : 'tắt'} hiển thị banner "${b.title}"`, 'success');
  } catch (err) {
    courseStore.showToast("Lỗi khi cập nhật trạng thái banner: " + err.message, 'error');
  }
};

const uploadImage = async (event, targetField) => {
  const file = event.target.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append('file', file);

  try {
    const res = await fetch('/api/upload', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${courseStore.token}`
      },
      body: formData
    });
    if (!res.ok) throw new Error('Upload thất bại');
    const data = await res.json();
    form.value[targetField] = data.url;
    courseStore.showToast('Tải ảnh lên thành công!', 'success');
  } catch (err) {
    courseStore.showToast('Không thể upload ảnh: ' + err.message, 'error');
  }
};

const saveBanner = async () => {
  saving.value = true;
  try {
    if (isEditing.value) {
      await courseStore.updateBanner(editingId.value, form.value);
      courseStore.showToast('Cập nhật banner thành công!', 'success');
    } else {
      await courseStore.createBanner(form.value);
      courseStore.showToast('Tạo banner mới thành công!', 'success');
    }
    activeView.value = 'list';
  } catch (err) {
    courseStore.showToast("Có lỗi xảy ra: " + (err.message || err), 'error');
  } finally {
    saving.value = false;
  }
};

const deleteBannerItem = async (id) => {
  const isConfirmed = await courseStore.showConfirm({
    title: 'Xác nhận xóa Banner',
    message: 'Bạn có chắc chắn muốn xóa banner trình chiếu này khỏi trang chủ?',
    confirmText: 'Đồng ý xóa',
    cancelText: 'Hủy bỏ',
    type: 'danger'
  });

  if (isConfirmed) {
    try {
      await courseStore.deleteBanner(id);
      courseStore.showToast('Đã xóa banner thành công!', 'success');
    } catch (err) {
      courseStore.showToast("Lỗi khi xóa banner: " + err.message, 'error');
    }
  }
};
</script>

<style scoped>
.admin-input-style {
  width: 100%;
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 14px;
}
</style>
