<template>
  <Teleport to="body">
    <div v-if="isOpen" class="modal-overlay" @click.self="$emit('close')" style="position: fixed; inset: 0; width: 100%; height: 100%; background: rgba(15, 23, 42, 0.6); display: flex; align-items: center; justify-content: center; z-index: 99999; padding: 20px;">
      <div class="modal-content animate-fade-in" style="background: #ffffff; border-radius: 16px; width: 100%; max-width: 600px; max-height: 90vh; display: flex; flex-direction: column; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2); border: 1px solid #e2e8f0; overflow: hidden;">
      <div class="modal-header" style="display: flex; justify-content: space-between; align-items: center; padding: 18px 24px; border-bottom: 1px solid #e2e8f0; background: #f8fafc;">
        <div>
          <h3 style="margin: 0; font-size: 18px; font-weight: 800; color: #0f172a;">🏷️ Quản lý Chuyên mục Bài viết</h3>
          <p style="margin: 4px 0 0; font-size: 13px; color: #64748b;">Chủ động thêm mới, đổi tên hoặc xóa các chuyên mục bài viết</p>
        </div>
        <button class="close-btn" @click="$emit('close')" style="background: none; border: none; font-size: 24px; cursor: pointer; color: #94a3b8;">&times;</button>
      </div>

      <div class="modal-body" style="padding: 20px 24px; overflow-y: auto;">
        <!-- Form Thêm / Sửa Chuyên mục -->
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px; margin-bottom: 20px;">
          <h4 style="margin: 0 0 12px 0; font-size: 14px; font-weight: 700; color: #022b9f;">
            {{ editingCatId ? '✏️ Cập nhật tên Chuyên mục' : '➕ Thêm Chuyên mục Mới' }}
          </h4>
          <div style="display: flex; gap: 8px; flex-wrap: wrap;">
            <input 
              v-model="catForm.name" 
              type="text" 
              placeholder="Tên chuyên mục (VD: Trí tuệ nhân tạo, Tự động hóa...)" 
              class="admin-input-style"
              style="flex: 2; min-width: 200px; background: #ffffff;"
              @keydown.enter.prevent="handleSaveCategory"
            />
            <button 
              type="button" 
              @click="handleSaveCategory" 
              class="btn btn-primary btn-sm"
              :disabled="!catForm.name.trim() || isSubmittingCat"
              style="white-space: nowrap; font-weight: 600;"
            >
              {{ isSubmittingCat ? 'Đang lưu...' : (editingCatId ? 'Cập nhật' : 'Thêm mới') }}
            </button>
            <button 
              v-if="editingCatId" 
              type="button" 
              @click="cancelEditCat" 
              class="btn btn-secondary btn-sm"
            >
              Hủy
            </button>
          </div>
          <small v-if="editingCatId" style="display: block; margin-top: 6px; color: #0284c7; font-size: 12px;">
            💡 Lưu ý: Khi đổi tên, toàn bộ bài viết đang thuộc chuyên mục này sẽ được tự động đồng bộ sang tên mới!
          </small>
        </div>

        <!-- Danh sách chuyên mục hiện có -->
        <div style="border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden;">
          <table class="admin-table" style="margin: 0; width: 100%;">
            <thead>
              <tr style="background: #f1f5f9;">
                <th>Tên chuyên mục</th>
                <th style="width: 120px; text-align: center;">Số bài viết</th>
                <th style="width: 100px; text-align: right;">Hành động</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="categories.length === 0">
                <td colspan="3" class="text-center py-4 text-muted">Chưa có chuyên mục nào.</td>
              </tr>
              <tr v-for="cat in categories" :key="cat.id || cat.name">
                <td>
                  <div style="font-weight: 700; color: #0f172a; font-size: 14px;">{{ cat.name }}</div>
                  <code style="font-size: 11px; color: #64748b;">{{ cat.slug }}</code>
                </td>
                <td style="text-align: center;">
                  <span class="badge" style="background: rgba(2, 43, 159, 0.08); color: #022b9f; font-weight: 700; padding: 4px 10px; border-radius: 9999px;">
                    {{ cat.post_count || 0 }} bài
                  </span>
                </td>
                <td style="text-align: right;">
                  <div class="action-buttons" style="justify-content: flex-end;">
                    <button @click="startEditCat(cat)" class="btn-action edit" title="Sửa tên chuyên mục">✏️</button>
                    <button @click="handleDeleteCat(cat)" class="btn-action delete" title="Xóa chuyên mục">🗑️</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="modal-footer" style="padding: 14px 24px; border-top: 1px solid #e2e8f0; display: flex; justify-content: flex-end; background: #f8fafc;">
        <button type="button" @click="$emit('close')" class="btn btn-secondary">Đóng</button>
      </div>
    </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref } from 'vue';
import { useCourseStore } from '@/stores/courses';

defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  categories: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits(['close', 'updated']);
const courseStore = useCourseStore();

const isSubmittingCat = ref(false);
const editingCatId = ref(null);
const catForm = ref({ name: '', slug: '', description: '' });

const startEditCat = (cat) => {
  editingCatId.value = cat.id;
  catForm.value = { name: cat.name, slug: cat.slug, description: cat.description || '' };
};

const cancelEditCat = () => {
  editingCatId.value = null;
  catForm.value = { name: '', slug: '', description: '' };
};

const handleSaveCategory = async () => {
  const name = catForm.value.name.trim();
  if (!name) return;
  isSubmittingCat.value = true;
  try {
    if (editingCatId.value) {
      await courseStore.updateBlogCategory(editingCatId.value, { name });
    } else {
      await courseStore.addBlogCategory({ name });
    }
    cancelEditCat();
    await courseStore.fetchBlogCategories(true);
    emit('updated');
  } catch (err) {
    // Toast handled in store
  } finally {
    isSubmittingCat.value = false;
  }
};

const handleDeleteCat = async (cat) => {
  if (cat.post_count > 0) {
    courseStore.showToast?.(`Không thể xóa chuyên mục "${cat.name}" vì đang có ${cat.post_count} bài viết! Hãy chuyển hoặc sửa bài viết trước.`, 'warning');
    return;
  }
  const confirmed = await courseStore.showConfirm?.({
    title: 'Xóa chuyên mục bài viết',
    message: `Bạn có chắc muốn xóa chuyên mục "${cat.name}" không?`,
    confirmText: 'Xóa chuyên mục',
    cancelText: 'Hủy'
  });
  if (confirmed) {
    await courseStore.deleteBlogCategory(cat.id);
    await courseStore.fetchBlogCategories(true);
    emit('updated');
  }
};
</script>

