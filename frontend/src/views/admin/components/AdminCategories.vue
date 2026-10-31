<template>
  <div class="admin-categories-tab">
    <div class="admin-header-actions mb-4">
      <div>
        <h2 class="admin-title">Quản lý Chuyên mục Khóa học</h2>
        <p class="admin-subtitle">Thêm, sửa, xóa các chuyên mục phân loại khóa học (Kỹ năng AI, Kỹ năng mềm, Marketing, etc.)</p>
      </div>
      <button class="btn btn-primary" @click="openAddModal">
        <span>+ Thêm chuyên mục mới</span>
      </button>
    </div>

    <!-- SUMMARY CARDS -->
    <div class="admin-summary-grid mb-4">
      <div class="summary-card">
        <div class="summary-info">
          <span class="summary-label">Tổng chuyên mục</span>
          <span class="summary-value">{{ categories.length }}</span>
        </div>
      </div>
    </div>

    <!-- CATEGORIES TABLE -->
    <div class="admin-table-container">
      <table class="admin-table">
        <thead>
          <tr>
            <th>Mã Slug</th>
            <th>Tên Chuyên mục</th>
            <th>Số khóa học đang có</th>
            <th class="text-right">Hành động</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="categories.length === 0">
            <td colspan="4" class="text-center py-4" style="color: #64748b;">
              Chưa có chuyên mục nào. Nhấn nút "+ Thêm chuyên mục mới" để tạo.
            </td>
          </tr>
          <tr v-for="cat in categories" :key="cat.slug">
            <td>
              <span class="badge badge-secondary" style="font-family: monospace; font-size: 13px;">{{ cat.slug }}</span>
            </td>
            <td>
              <strong style="color: #0f172a; font-size: 15px;">{{ cat.name }}</strong>
            </td>
            <td>
              <span class="badge badge-info">{{ getCourseCount(cat.slug) }} khóa học</span>
            </td>
            <td class="text-right">
              <div class="admin-actions-cell" style="justify-content: flex-end;">
                <button class="btn-action edit" title="Sửa tên chuyên mục" @click="editCategory(cat)">
                  ✏️
                </button>
                <button class="btn-action delete" title="Xóa chuyên mục" @click="confirmDelete(cat)">
                  🗑️
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- MODAL ADD / EDIT CATEGORY -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content animate-fade-in" style="max-width: 500px;">
        <div class="modal-header">
          <h3>{{ isEditing ? 'Sửa Tên Chuyên Mục' : 'Thêm Chuyên Mục Mới' }}</h3>
          <button class="close-btn" @click="closeModal">&times;</button>
        </div>
        
        <form @submit.prevent="saveCategory">
          <div class="form-group mb-3">
            <label style="color: #1e293b; font-weight: 600;">Tên chuyên mục</label>
            <input 
              v-model="catForm.name" 
              @input="onNameInput"
              type="text" 
              required 
              class="admin-input-style" 
              placeholder="Ví dụ: Kỹ năng Quản trị & Lãnh đạo" 
              style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" 
            />
          </div>

          <div class="form-group mb-4">
            <label style="color: #1e293b; font-weight: 600;">Đường dẫn tĩnh (Slug)</label>
            <input 
              v-model="catForm.slug" 
              :readonly="isEditing"
              type="text" 
              required 
              class="admin-input-style" 
              placeholder="ky-nang-quan-tri" 
              style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" 
            />
            <small v-if="isEditing" style="color: #64748b; margin-top: 4px; display: block;">Mã slug không thể sửa sau khi khởi tạo để giữ liên kết khóa học.</small>
          </div>

          <div class="modal-footer" style="display: flex; gap: 10px; justify-content: flex-end;">
            <button type="button" class="btn btn-outline" @click="closeModal">Hủy</button>
            <button type="submit" class="btn btn-primary" :disabled="submitting">
              {{ submitting ? 'Đang lưu...' : (isEditing ? 'Cập nhật' : 'Tạo mới') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useCourseStore } from '@/stores/courses';

const courseStore = useCourseStore();

onMounted(async () => {
  await courseStore.fetchCategories().catch(err => console.warn('fetchCategories failed:', err));
  if (courseStore.courses.length === 0) {
    courseStore.fetchCourses().catch(err => console.warn('fetchCourses failed:', err));
  }
});

const categories = computed(() => courseStore.categories || []);
const showModal = ref(false);
const isEditing = ref(false);
const submitting = ref(false);

const catForm = ref({
  name: '',
  slug: ''
});

const getCourseCount = (slug) => {
  return courseStore.courses.filter(c => c.category === slug || c.category_slug === slug).length;
};

const slugify = (text) => {
  return text
    .toString()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9 -]/g, '')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-');
};

const onNameInput = () => {
  if (!isEditing.value) {
    catForm.value.slug = slugify(catForm.value.name);
  }
};

const openAddModal = () => {
  isEditing.value = false;
  catForm.value = { name: '', slug: '' };
  showModal.value = true;
};

const editCategory = (cat) => {
  isEditing.value = true;
  catForm.value = { name: cat.name, slug: cat.slug };
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

const saveCategory = async () => {
  submitting.value = true;
  try {
    if (isEditing.value) {
      await courseStore.updateCategory(catForm.value.slug, catForm.value.name);
    } else {
      await courseStore.createCategory(catForm.value);
    }
    closeModal();
  } catch (err) {
    console.error(err);
  } finally {
    submitting.value = false;
  }
};

const confirmDelete = async (cat) => {
  const count = getCourseCount(cat.slug);
  let msg = `Bạn có chắc chắn muốn xóa chuyên mục "${cat.name}"?`;
  if (count > 0) {
    msg += `\n\nHiện tại đang có ${count} khóa học thuộc chuyên mục này. Vui lòng di chuyển hoặc xóa các khóa học trước khi xóa chuyên mục!`;
  }
  const isConfirmed = await courseStore.showConfirm({
    title: 'Xác nhận xóa chuyên mục',
    message: msg,
    confirmText: 'Đồng ý xóa',
    cancelText: 'Hủy bỏ',
    type: 'danger'
  });

  if (isConfirmed) {
    await courseStore.deleteCategory(cat.slug);
  }
};
</script>
