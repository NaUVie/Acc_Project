<template>
  <div class="tab-content animate-fade-in">
    <!-- VIEW 1: LIST TABLE -->
    <div v-if="activeView === 'list'">
      <div class="content-header flex-between">
        <div>
          <h2>Quản lý Ban Điều Hành & Cố Vấn ({{ boardMembers.length }})</h2>
          <p>
            Quản lý danh sách và thứ tự hiển thị của ban lãnh đạo, sáng lập và cố vấn trên trang <strong>Về chúng tôi</strong>.
          </p>
        </div>
        <div style="display: flex; gap: 10px; align-items: center;">
          <button @click="refreshBoardMembers" :disabled="isRefreshing" class="btn btn-secondary btn-sm" style="display: flex; align-items: center; gap: 6px; font-weight: 600;" title="Tải lại danh sách mới nhất">
            <span :class="{ 'spin-icon': isRefreshing }">🔄</span>
            <span>{{ isRefreshing ? 'Đang đồng bộ...' : 'Làm mới' }}</span>
          </button>
          <button @click="openAddModal" class="btn btn-primary btn-sm">+ Thêm Thành viên mới</button>
        </div>
      </div>

      <!-- SEARCH & FILTER BAR -->
      <div class="table-search-bar mt-4 mb-4" style="display: flex; gap: 12px; align-items: center; flex-wrap: wrap;">
        <input 
          v-model="searchQuery" 
          type="text" 
          class="admin-input-style" 
          placeholder="Tìm theo họ tên, chức vụ..." 
          style="max-width: 320px; padding: 8px 14px; font-size: 14px; background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1; border-radius: 8px;"
        />
        <select 
          v-model="filterStatus" 
          class="admin-input-style"
          style="max-width: 170px; padding: 8px 12px; font-size: 14px; background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1; border-radius: 8px;"
        >
          <option value="all">Tất cả trạng thái</option>
          <option value="active">Đang hiển thị</option>
          <option value="hidden">Đã ẩn</option>
        </select>
        <span class="text-muted" style="font-size: 13.5px; margin-left: auto;">
          Hiển thị <strong>{{ filteredMembers.length }}</strong> / {{ boardMembers.length }} thành viên (sắp xếp theo thứ tự hiển thị)
        </span>
      </div>

      <!-- Members Table -->
      <div class="table-responsive mt-2">
        <table class="admin-table">
          <thead>
            <tr>
              <th style="width: 130px; text-align: center;">Thứ tự hiển thị</th>
              <th style="width: 90px; text-align: center;">Ảnh đại diện</th>
              <th style="width: 220px;">Họ và tên</th>
              <th style="width: 250px;">Chức vụ hiển thị</th>
              <th>Tiểu sử / Thành tích</th>
              <th style="width: 120px; text-align: center;">Trạng thái</th>
              <th style="width: 110px; text-align: center;">Hành động</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="filteredMembers.length === 0">
              <td colspan="7" class="text-center" style="padding: 36px; color: #64748b;">
                Không tìm thấy thành viên nào phù hợp.
              </td>
            </tr>
            <tr v-for="(member, idx) in filteredMembers" :key="member.id">
              <!-- CỘT THỨ TỰ CÓ NÚT LÊN/XUỐNG VÀ INPUT NHANH -->
              <td style="text-align: center;">
                <div style="display: flex; align-items: center; justify-content: center; gap: 4px;">
                  <button 
                    type="button" 
                    @click="moveOrder(member, 'up')" 
                    :disabled="idx === 0"
                    class="order-btn"
                    title="Đưa lên trên"
                  >
                    ▲
                  </button>
                  <input 
                    type="number" 
                    :value="member.position"
                    @change="onPositionChange(member, $event.target.value)"
                    min="1"
                    style="width: 46px; text-align: center; font-weight: 700; color: #0f172a; border: 1px solid #cbd5e1; border-radius: 6px; padding: 3px 2px; font-size: 13px;"
                    title="Nhập số thứ tự và nhấn Enter để đổi"
                  />
                  <button 
                    type="button" 
                    @click="moveOrder(member, 'down')" 
                    :disabled="idx === filteredMembers.length - 1"
                    class="order-btn"
                    title="Đưa xuống dưới"
                  >
                    ▼
                  </button>
                </div>
              </td>
              <!-- CỘT ẢNH CÓ NÚT CẮT ẢNH NHANH -->
              <td style="text-align: center;">
                <div style="position: relative; display: inline-block; width: 54px; height: 54px;">
                  <div style="width: 100%; height: 100%; border-radius: 10px; overflow: hidden; background: #f1f5f9; display: flex; align-items: center; justify-content: center; border: 1px solid #e2e8f0;">
                    <img 
                      v-if="member.avatar" 
                      :src="member.avatar" 
                      :alt="member.name"
                      style="width: 100%; height: 100%; object-fit: cover;"
                      @error="(e) => e.target.src = '/images/1_6.png'"
                    />
                    <span v-else style="font-size: 22px;">👤</span>
                  </div>
                  <button 
                    v-if="member.avatar"
                    type="button"
                    class="crop-mini-btn"
                    title="✂ Cắt & căn chỉnh ảnh chân dung"
                    @click="openCropper(member.avatar, async (url) => { await courseStore.updateBoardMember(member.id, { avatar: url }); }, 'square', `✂ Cắt Ảnh: ${member.name}`)"
                  >
                    ✂
                  </button>
                </div>
              </td>
              <td>
                <div style="font-weight: 700; color: #0f172a; font-size: 14.5px;">{{ member.name }}</div>
              </td>
              <td>
                <div style="color: #0369a1; font-weight: 600; font-size: 13px; line-height: 1.4;">{{ member.main_role }}</div>
              </td>
              <td>
                <ul style="margin: 0; padding-left: 18px; font-size: 12.5px; color: #475569; line-height: 1.45;">
                  <li v-for="(bio, bIdx) in getBioLines(member)" :key="bIdx">
                    {{ bio }}
                  </li>
                </ul>
              </td>
              <td style="text-align: center;">
                <button 
                  type="button" 
                  @click="toggleActive(member)"
                  class="btn btn-sm"
                  :style="member.is_active 
                    ? 'background: #dcfce7; color: #15803d; border: 1px solid #bbf7d0; font-weight: 600; font-size: 12px; padding: 4px 10px; border-radius: 6px;' 
                    : 'background: #fee2e2; color: #b91c1c; border: 1px solid #fecaca; font-weight: 600; font-size: 12px; padding: 4px 10px; border-radius: 6px;'"
                  title="Nhấn để đổi trạng thái"
                >
                  {{ member.is_active ? '✓ Hiển thị' : '✕ Đang ẩn' }}
                </button>
              </td>
              <td data-label="Hành động">
                <div class="action-buttons" style="justify-content: center;">
                  <button @click="openEditModal(member)" class="btn-action edit" title="Sửa thông tin">✏️</button>
                  <button @click="confirmDelete(member)" class="btn-action delete" title="Xóa">🗑️</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- VIEW 2: ADD / EDIT MODAL (COMPACT 2-COLUMN, NO SCROLL) -->
    <Teleport to="body">
      <div v-if="isModalOpen" class="admin-modal-overlay" @click.self="closeModal">
      <div class="admin-modal-card" style="max-width: 820px; width: 95%; padding: 20px 24px;">
        <div class="modal-header flex-between" style="border-bottom: 1px solid #e2e8f0; padding-bottom: 12px; margin-bottom: 16px;">
          <h3 style="font-size: 17px; font-weight: 700; color: #0f172a; margin: 0;">
            {{ isEditing ? '✏️ Chỉnh sửa Thành viên Ban Điều Hành & Cố Vấn' : '➕ Thêm Thành viên mới' }}
          </h3>
          <button @click="closeModal" class="btn btn-sm btn-secondary" style="border: none; background: transparent; font-size: 18px; cursor: pointer; padding: 0 4px;">✕</button>
        </div>

        <form @submit.prevent="saveMember">
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; align-items: stretch;">
            <!-- CỘT TRÁI: THÔNG TIN CHÍNH & ẢNH -->
            <div style="display: flex; flex-direction: column; gap: 12px;">
              <!-- Avatar + Tên + Thứ tự -->
              <div style="display: flex; gap: 14px; align-items: flex-start;">
                <!-- Avatar Box kết hợp Cắt ảnh -->
                <div style="display: flex; flex-direction: column; align-items: center; gap: 5px;">
                  <div 
                    @click="$refs.avatarFileRef.click()"
                    style="width: 76px; height: 76px; border-radius: 12px; overflow: hidden; background: #f8fafc; border: 2px dashed #cbd5e1; cursor: pointer; display: flex; align-items: center; justify-content: center; position: relative; transition: all 0.2s;"
                    title="Nhấn để chọn ảnh chân dung & cắt ảnh"
                  >
                    <img 
                      v-if="form.avatar" 
                      :src="form.avatar" 
                      alt="Avatar" 
                      style="width: 100%; height: 100%; object-fit: cover;" 
                      @error="(e) => e.target.src = '/images/1_6.png'" 
                    />
                    <div v-else style="text-align: center; color: #64748b; font-size: 11px;">
                      <div style="font-size: 20px;">📷</div>
                      <span>Chọn ảnh</span>
                    </div>
                  </div>
                  
                  <input 
                    type="file" 
                    ref="avatarFileRef" 
                    @change="onFileSelectForCrop($event, (url) => { form.avatar = url; }, 'square', '✂ Cắt & Căn Chỉnh Ảnh Chân Dung')" 
                    style="display: none;" 
                    accept="image/*" 
                  />
                  
                  <div style="display: flex; gap: 4px; align-items: center;">
                    <button 
                      type="button" 
                      @click="$refs.avatarFileRef.click()" 
                      class="btn btn-secondary btn-sm" 
                      style="font-size: 10.5px; padding: 2px 7px; border-radius: 5px;"
                    >
                      {{ form.avatar ? 'Đổi ảnh' : 'Tải lên' }}
                    </button>
                    <button 
                      v-if="form.avatar" 
                      type="button" 
                      class="btn btn-sm btn-secondary" 
                      style="font-size: 10.5px; padding: 2px 7px; border-radius: 5px; color: #0284c7; border-color: #bae6fd;" 
                      title="Mở trình cắt ảnh"
                      @click="openCropper(form.avatar, (url) => { form.avatar = url; }, 'square', '✂ Cắt & Căn Chỉnh Ảnh Chân Dung')"
                    >
                      ✂ Cắt ảnh
                    </button>
                  </div>
                </div>

                <!-- Tên & Thứ tự -->
                <div style="flex: 1; display: flex; flex-direction: column; gap: 8px;">
                  <div>
                    <label style="display: block; font-weight: 600; font-size: 13px; color: #1e293b; margin-bottom: 3px;">Họ và tên *</label>
                    <input 
                      v-model="form.name" 
                      type="text" 
                      required 
                      class="admin-input-style" 
                      placeholder="VD: TS. Nguyễn Tấn Bình" 
                      style="width: 100%; padding: 7px 10px; font-size: 13.5px; border: 1px solid #cbd5e1; border-radius: 6px;"
                    />
                  </div>
                  <div>
                    <label style="display: block; font-weight: 600; font-size: 13px; color: #1e293b; margin-bottom: 3px;">Thứ tự hiển thị *</label>
                    <input 
                      v-model.number="form.position" 
                      type="number" 
                      min="1"
                      required
                      class="admin-input-style" 
                      placeholder="1, 2, 3..." 
                      style="width: 100%; padding: 7px 10px; font-size: 13.5px; border: 1px solid #cbd5e1; border-radius: 6px;"
                    />
                  </div>
                </div>
              </div>

              <!-- Chức vụ hiển thị -->
              <div>
                <label style="display: block; font-weight: 600; font-size: 13px; color: #1e293b; margin-bottom: 3px;">Chức vụ hiển thị *</label>
                <input 
                  v-model="form.main_role" 
                  type="text" 
                  required 
                  class="admin-input-style" 
                  placeholder="VD: Chủ tịch HĐQT / Cố vấn Cao cấp..." 
                  style="width: 100%; padding: 7px 10px; font-size: 13.5px; border: 1px solid #cbd5e1; border-radius: 6px;"
                />
              </div>

              <!-- URL Ảnh (phụ) -->
              <div>
                <label style="display: block; font-weight: 600; font-size: 12px; color: #64748b; margin-bottom: 3px;">Đường dẫn ảnh trực tiếp (tùy chọn)</label>
                <input 
                  v-model="form.avatar" 
                  type="text" 
                  class="admin-input-style" 
                  placeholder="/images/... hoặc https://..." 
                  style="width: 100%; padding: 6px 10px; font-size: 12px; border: 1px solid #e2e8f0; border-radius: 6px;"
                />
              </div>

              <!-- Trạng thái hiển thị -->
              <label style="display: flex; align-items: center; gap: 8px; cursor: pointer; font-size: 13px; font-weight: 600; color: #1e293b; margin-top: 2px;">
                <input v-model="form.is_active" type="checkbox" style="width: 16px; height: 16px; accent-color: #2563eb;" />
                <span>Hiển thị công khai trên website</span>
              </label>
            </div>

            <!-- CỘT PHẢI: TIỂU SỬ / THÀNH TỰU -->
            <div style="display: flex; flex-direction: column;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                <label style="font-weight: 600; font-size: 13px; color: #1e293b; margin: 0;">Tiểu sử & Thành tựu (mỗi dòng 1 ý)</label>
                <span style="font-size: 11px; color: #64748b;">(Mỗi dòng = 1 gạch đầu dòng)</span>
              </div>
              <textarea 
                v-model="form.bio_text" 
                rows="8"
                class="admin-input-style" 
                placeholder="CEO Sadaco Tas&#10;Chủ tịch HĐQT CTY CP Tập đoàn Sài Gòn Tiến Đoàn&#10;Thạc sĩ QTKD Đại học Andrews (Hoa Kỳ)" 
                style="flex: 1; min-height: 195px; width: 100%; padding: 8px 12px; font-size: 13px; border: 1px solid #cbd5e1; border-radius: 6px; line-height: 1.5; resize: none;"
              ></textarea>
            </div>
          </div>

          <!-- Footer -->
          <div class="modal-footer" style="display: flex; justify-content: flex-end; gap: 10px; margin-top: 16px; border-top: 1px solid #e2e8f0; padding-top: 12px;">
            <button type="button" @click="closeModal" class="btn btn-secondary btn-sm" style="padding: 6px 14px;">Hủy bỏ</button>
            <button type="submit" class="btn btn-primary btn-sm" :disabled="saving" style="padding: 6px 18px; font-weight: 600;">
              {{ saving ? 'Đang lưu...' : (isEditing ? 'Lưu thay đổi' : 'Thêm thành viên') }}
            </button>
          </div>
        </form>
      </div>
    </div>
    </Teleport>

    <!-- Image Cropper Modal (Hỗ trợ Vuông 1:1, Tự do, Thu phóng, Căn chỉnh khuôn mặt) -->
    <ImageCropperModal 
      :isOpen="isCropperOpen" 
      :imageUrl="cropTargetUrl" 
      :aspectRatio="cropAspectRatio" 
      :title="cropModalTitle" 
      @close="isCropperOpen = false" 
      @cropped="handleCroppedImage" 
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useCourseStore } from '@/stores/courses';
import ImageCropperModal from '@/components/ImageCropperModal.vue';

const courseStore = useCourseStore();

const activeView = ref('list');
const isRefreshing = ref(false);
const isModalOpen = ref(false);
const isEditing = ref(false);
const editingId = ref(null);
const saving = ref(false);
const avatarFileRef = ref(null);

// Cropper States
const isCropperOpen = ref(false);
const cropTargetUrl = ref('');
const cropAspectRatio = ref('square');
const cropModalTitle = ref('✂ Cắt & Căn Chỉnh Ảnh Chân Dung');
let cropTargetCallback = null;

const openCropper = (url, callback, ratio = 'square', title = '✂ Cắt & Căn Chỉnh Ảnh Chân Dung') => {
  if (!url) return;
  cropTargetUrl.value = url;
  cropAspectRatio.value = ratio;
  cropModalTitle.value = title;
  cropTargetCallback = callback;
  isCropperOpen.value = true;
};

const onFileSelectForCrop = (event, callback, ratio = 'square', title = '✂ Cắt & Căn Chỉnh Ảnh Chân Dung') => {
  const file = event.target?.files?.[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = (e) => {
    openCropper(e.target.result, callback, ratio, title);
  };
  reader.readAsDataURL(file);
  event.target.value = '';
};

const handleCroppedImage = async (newUrl) => {
  isCropperOpen.value = false;
  if (cropTargetCallback) {
    await cropTargetCallback(newUrl);
  }
};

const searchQuery = ref('');
const filterStatus = ref('all');

const form = ref({
  name: '',
  main_role: '',
  avatar: '',
  position: 1,
  is_active: true,
  bio_text: ''
});

// Always sort by position ascending
const boardMembers = computed(() => {
  const list = [...(courseStore.adminBoardMembers || [])];
  return list.sort((a, b) => (Number(a.position) || 0) - (Number(b.position) || 0));
});

const filteredMembers = computed(() => {
  return boardMembers.value.filter(m => {
    // Status filter
    if (filterStatus.value === 'active' && !m.is_active) return false;
    if (filterStatus.value === 'hidden' && m.is_active) return false;
    // Search query
    if (searchQuery.value.trim()) {
      const q = searchQuery.value.toLowerCase();
      const matchName = m.name?.toLowerCase().includes(q);
      const matchRole = m.main_role?.toLowerCase().includes(q);
      if (!matchName && !matchRole) return false;
    }
    return true;
  });
});

const getBioLines = (member) => {
  if (Array.isArray(member.bio_list)) return member.bio_list;
  if (typeof member.bio_list === 'string') {
    try {
      const parsed = JSON.parse(member.bio_list);
      if (Array.isArray(parsed)) return parsed;
    } catch {
      return member.bio_list.split('\n').map(s => s.trim()).filter(Boolean);
    }
  }
  return [];
};

const refreshBoardMembers = async () => {
  isRefreshing.value = true;
  try {
    await courseStore.fetchAdminBoardMembers(true);
  } catch (err) {
    console.error('Error refreshing board members:', err);
  } finally {
    isRefreshing.value = false;
  }
};

const openAddModal = () => {
  isEditing.value = false;
  editingId.value = null;
  const maxPos = boardMembers.value.reduce((max, m) => Math.max(max, Number(m.position) || 0), 0);
  form.value = {
    name: '',
    main_role: '',
    avatar: '',
    position: maxPos + 1,
    is_active: true,
    bio_text: ''
  };
  isModalOpen.value = true;
};

const openEditModal = (member) => {
  isEditing.value = true;
  editingId.value = member.id;
  const bioLines = getBioLines(member);
  form.value = {
    name: member.name || '',
    main_role: member.main_role || '',
    avatar: member.avatar || '',
    position: member.position || 1,
    is_active: member.is_active !== undefined ? member.is_active : true,
    bio_text: bioLines.join('\n')
  };
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
};

// Swap order with adjacent member
const moveOrder = async (member, direction) => {
  const list = [...filteredMembers.value];
  const idx = list.findIndex(m => m.id === member.id);
  const targetIdx = direction === 'up' ? idx - 1 : idx + 1;
  if (targetIdx < 0 || targetIdx >= list.length) return;

  const targetMember = list[targetIdx];
  const oldPos = Number(member.position) || 1;
  const targetPos = Number(targetMember.position) || 1;

  let newCurrentPos = targetPos;
  let newTargetPos = oldPos;
  if (newCurrentPos === newTargetPos) {
    newCurrentPos = direction === 'up' ? targetPos - 1 : targetPos + 1;
  }

  try {
    await Promise.all([
      courseStore.updateBoardMember(member.id, { position: newCurrentPos }),
      courseStore.updateBoardMember(targetMember.id, { position: newTargetPos })
    ]);
  } catch (err) {
    console.error('Failed to change order:', err);
  }
};

// Direct inline position input change
const onPositionChange = async (member, val) => {
  const newPos = parseInt(val, 10);
  if (isNaN(newPos) || newPos < 1 || newPos === member.position) return;
  try {
    await courseStore.updateBoardMember(member.id, { position: newPos });
  } catch (err) {
    console.error('Failed to update position:', err);
  }
};

const toggleActive = async (member) => {
  try {
    await courseStore.updateBoardMember(member.id, {
      is_active: !member.is_active
    });
  } catch (err) {
    console.error('Toggle active failed:', err);
  }
};

const confirmDelete = (member) => {
  if (confirm(`Bạn có chắc chắn muốn xóa thành viên "${member.name}" khỏi danh sách?`)) {
    courseStore.deleteBoardMember(member.id).catch(err => {
      console.error('Delete failed:', err);
    });
  }
};

const saveMember = async () => {
  saving.value = true;
  try {
    const bioArray = form.value.bio_text
      .split('\n')
      .map(l => l.trim())
      .filter(l => l.length > 0);

    const payload = {
      name: form.value.name.trim(),
      main_role: form.value.main_role.trim(),
      avatar: form.value.avatar.trim() || null,
      position: Number(form.value.position) || 1,
      is_active: Boolean(form.value.is_active),
      bio_list: JSON.stringify(bioArray)
    };

    if (isEditing.value && editingId.value) {
      await courseStore.updateBoardMember(editingId.value, payload);
    } else {
      await courseStore.createBoardMember(payload);
    }
    closeModal();
  } catch (err) {
    console.error('Save failed:', err);
    courseStore.showToast('Lỗi khi lưu thông tin thành viên!', 'error');
  } finally {
    saving.value = false;
  }
};

onMounted(() => {
  courseStore.fetchAdminBoardMembers().catch(() => {});
});
</script>

<style scoped>
.order-btn {
  background: #f1f5f9;
  border: 1px solid #cbd5e1;
  color: #475569;
  border-radius: 6px;
  width: 26px;
  height: 26px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 11px;
  transition: all 0.15s ease;
}
.order-btn:hover:not(:disabled) {
  background: #2563eb;
  color: #ffffff;
  border-color: #2563eb;
}
.order-btn:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}

.crop-mini-btn {
  position: absolute;
  bottom: -4px;
  right: -4px;
  background: #0284c7;
  color: #ffffff;
  border: 2px solid #ffffff;
  border-radius: 50%;
  width: 22px;
  height: 22px;
  font-size: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
  transition: all 0.15s ease;
}
.crop-mini-btn:hover {
  background: #0369a1;
  transform: scale(1.15);
}

.admin-modal-overlay {
  position: fixed;
  inset: 0;
  width: 100%;
  height: 100%;
  background: rgba(15, 23, 42, 0.65);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 99999;
  padding: 16px;
  box-sizing: border-box;
}

.admin-modal-card {
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.spin-icon {
  display: inline-block;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  100% {
    transform: rotate(360deg);
  }
}
</style>
