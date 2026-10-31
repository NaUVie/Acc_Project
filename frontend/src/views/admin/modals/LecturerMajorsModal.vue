<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content animate-fade-in" style="max-width: 700px;">
      <div class="modal-header">
        <h3>Quản lý Chuyên ngành Giảng viên (Database)</h3>
        <button class="close-btn" @click="$emit('close')">&times;</button>
      </div>

      <div class="modal-body" style="padding: 16px 0;">
        <!-- Form Create / Edit Major -->
        <form @submit.prevent="saveMajor" style="background: #f8fafc; padding: 16px; border-radius: 12px; margin-bottom: 20px; border: 1px solid #e2e8f0;">
          <h4 style="margin-top: 0; margin-bottom: 12px; font-size: 15px; color: #0f172a; font-weight: 700;">
            {{ isEditingMajor ? 'Chỉnh sửa chuyên ngành' : 'Thêm chuyên ngành mới' }}
          </h4>
          
          <div class="grid-2">
            <div class="form-group">
              <label style="font-size: 12px; font-weight: 600; color: #475569;">Mã ID chuyên ngành (Slug)</label>
              <input 
                v-model="majorForm.id" 
                :disabled="isEditingMajor" 
                type="text" 
                required 
                class="admin-input-style" 
                placeholder="tai-chinh-lanh-dao" 
                style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1; font-size: 13px;"
              />
            </div>
            <div class="form-group">
              <label style="font-size: 12px; font-weight: 600; color: #475569;">Tên chuyên ngành</label>
              <input 
                v-model="majorForm.name" 
                @input="onMajorNameInput" 
                type="text" 
                required 
                class="admin-input-style" 
                placeholder="QUẢN TRỊ - TÀI CHÍNH" 
                style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1; font-size: 13px;"
              />
            </div>
          </div>

          <div class="grid-2 mt-2">
            <div class="form-group">
              <label style="font-size: 12px; font-weight: 600; color: #475569;">Nhãn Badge Header</label>
              <input 
                v-model="majorForm.badge" 
                type="text" 
                class="admin-input-style" 
                placeholder="QUẢN TRỊ - TÀI CHÍNH" 
                style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1; font-size: 13px;"
              />
            </div>
            <div class="form-group">
              <label style="font-size: 12px; font-weight: 600; color: #475569;">Mô tả ngắn chuyên ngành</label>
              <input 
                v-model="majorForm.description" 
                type="text" 
                class="admin-input-style" 
                placeholder="Đội ngũ chuyên gia chuyên sâu thuộc..." 
                style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1; font-size: 13px;"
              />
            </div>
          </div>

          <div class="mt-3" style="display: flex; gap: 8px; justify-content: flex-end;">
            <button v-if="isEditingMajor" type="button" class="btn btn-secondary btn-xs" @click="resetMajorForm">Hủy sửa</button>
            <button type="submit" class="btn btn-primary btn-xs" style="padding: 6px 16px; font-weight: 700;">
              {{ isEditingMajor ? 'Cập nhật chuyên ngành' : 'Tạo mới' }}
            </button>
          </div>
        </form>

        <!-- Majors List Table -->
        <div class="table-responsive">
          <table class="admin-table" style="font-size: 13px;">
            <thead>
              <tr>
                <th>ID Slug</th>
                <th>Tên Chuyên ngành</th>
                <th>Số Giảng viên</th>
                <th class="text-right">Hành động</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="m in lecturerMajors" :key="m.id">
                <td><code style="background: #f1f5f9; padding: 2px 6px; border-radius: 4px; color: #0284c7;">{{ m.id }}</code></td>
                <td><strong>{{ m.name }}</strong></td>
                <td><span class="badge badge-info">{{ getMajorLecturersCount(m.id) }} người</span></td>
                <td class="text-right">
                  <div class="action-buttons" style="justify-content: flex-end;">
                    <button @click="editMajor(m)" class="btn-action edit" title="Sửa">✏️</button>
                    <button @click="deleteMajor(m)" class="btn-action delete" title="Xóa">🗑️</button>
                  </div>
                </td>
              </tr>
              <tr v-if="lecturerMajors.length === 0">
                <td colspan="4" class="text-center py-4 text-muted">Chưa có chuyên ngành nào trong Database.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="modal-footer" style="display: flex; justify-content: flex-end;">
        <button type="button" class="btn btn-secondary" @click="$emit('close')">Đóng</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useCourseStore } from '@/stores/courses';
import { slugify } from '@/utils/slugify';

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  lecturers: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits(['close', 'updated']);

const courseStore = useCourseStore();
const lecturerMajors = computed(() => courseStore.lecturerMajors || []);

const isEditingMajor = ref(false);
const majorForm = ref({
  id: '',
  name: '',
  icon: '',
  badge: '',
  description: '',
  position: 0
});

const resetMajorForm = () => {
  isEditingMajor.value = false;
  majorForm.value = {
    id: '',
    name: '',
    icon: '',
    badge: '',
    description: '',
    position: 0
  };
};

const onMajorNameInput = () => {
  if (!isEditingMajor.value) {
    majorForm.value.id = slugify(majorForm.value.name);
    majorForm.value.badge = majorForm.value.name.toUpperCase();
  }
};

const editMajor = (m) => {
  isEditingMajor.value = true;
  majorForm.value = {
    id: m.id,
    name: m.name,
    icon: m.icon || '',
    badge: m.badge || m.name.toUpperCase(),
    description: m.description || '',
    position: m.position || 0
  };
};

const getMajorLecturersCount = (majorId) => {
  return props.lecturers.filter(l => {
    const ids = l.majorIds && l.majorIds.length > 0 ? l.majorIds : (l.majorId ? [l.majorId] : []);
    return ids.includes(majorId);
  }).length;
};

const saveMajor = async () => {
  try {
    if (!majorForm.value.id.trim() || !majorForm.value.name.trim()) {
      courseStore.showToast('Vui lòng nhập tên và mã chuyên ngành!', 'warning');
      return;
    }
    if (isEditingMajor.value) {
      await courseStore.updateAdminLecturerMajor(majorForm.value.id, majorForm.value);
      courseStore.showToast('Cập nhật chuyên ngành thành công!', 'success');
    } else {
      if (lecturerMajors.value.some(m => m.id === majorForm.value.id)) {
        courseStore.showToast('Mã ID chuyên ngành này đã tồn tại!', 'warning');
        return;
      }
      await courseStore.addAdminLecturerMajor(majorForm.value);
      courseStore.showToast('Thêm chuyên ngành mới thành công!', 'success');
    }
    resetMajorForm();
    emit('updated');
  } catch (err) {
    courseStore.showToast(err.message || 'Lỗi khi lưu chuyên ngành.', 'error');
  }
};

const deleteMajor = async (m) => {
  const count = getMajorLecturersCount(m.id);
  let msg = `Bạn có chắc chắn muốn xóa chuyên ngành "${m.name}"?`;
  if (count > 0) {
    msg += `\n\nĐang có ${count} giảng viên thuộc chuyên ngành này. Sau khi xóa, các giảng viên sẽ trở về trạng thái chưa thuộc chuyên ngành.`;
  }
  const isConfirmed = await courseStore.showConfirm({
    title: 'Xác nhận xóa chuyên ngành giảng viên',
    message: msg,
    confirmText: 'Đồng ý xóa',
    cancelText: 'Hủy bỏ',
    type: 'danger'
  });

  if (isConfirmed) {
    try {
      await courseStore.deleteAdminLecturerMajor(m.id);
      courseStore.showToast(`Đã xóa chuyên ngành "${m.name}".`, 'success');
      emit('updated');
    } catch (err) {
      courseStore.showToast(err.message || 'Lỗi khi xóa chuyên ngành.', 'error');
    }
  }
};
</script>

