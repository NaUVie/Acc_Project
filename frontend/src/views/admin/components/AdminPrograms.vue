<template>
  <div class="tab-content animate-fade-in">
    <!-- VIEW 1: LIST TABLE -->
    <div v-if="activeView === 'list'">
      <div class="content-header flex-between">
        <div>
          <h2>Quản lý Chương trình Đào tạo (Programs)</h2>
          <p>Tạo các chương trình đào tạo tổng thể và gộp nhiều khóa học làm con của chương trình đó.</p>
        </div>
        <button @click="openAddModal" class="btn btn-primary btn-sm">+ Thêm chương trình mới</button>
      </div>

      <!-- Programs Grid / Table -->
      <div class="table-responsive mt-6">
        <table class="admin-table">
          <thead>
            <tr>
              <th>Hình ảnh</th>
              <th>Tên chương trình</th>
              <th>Mô tả</th>
              <th>Khóa học con (Child Courses)</th>
              <th>Hành động</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in programs" :key="p.id">
              <td>
                <img :src="p.image || '/images/default.jpg'" :alt="p.title" class="admin-course-thumb" />
              </td>
              <td class="font-bold">
                <div>{{ p.title }}</div>
                <small class="text-muted">Slug: {{ p.slug }}</small>
              </td>
              <td style="max-width: 240px;">
                <div class="line-clamp-2 text-sm text-secondary" style="display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;" :title="p.description">
                  {{ p.description }}
                </div>
              </td>
              <td style="max-width: 260px;">
                <div class="child-courses-tags">
                  <template v-if="getChildCourses(p.id).length > 0">
                    <span 
                      v-for="c in getChildCourses(p.id).slice(0, 2)" 
                      :key="c.id" 
                      class="badge badge-info mr-1 mb-1"
                      style="display: inline-block; max-width: 220px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; vertical-align: middle;"
                    >
                      🎓 {{ c.title }}
                    </span>
                    <span 
                      v-if="getChildCourses(p.id).length > 2"
                      class="badge" 
                      style="background: #e2e8f0; color: #334155; font-weight: 700; font-size: 11px; cursor: pointer; display: inline-block; margin-bottom: 4px; padding: 4px 8px; border-radius: 6px;"
                      :title="getChildCourses(p.id).map(x => x.title).join('\n')"
                    >
                      +{{ getChildCourses(p.id).length - 2 }} khóa học khác
                    </span>
                  </template>
                  <span v-else class="text-muted text-xs">
                    (Chưa có khóa học con)
                  </span>
                </div>
              </td>
              <td>
                <div class="action-buttons">
                  <button @click="editProgram(p)" class="btn-action edit" title="Sửa chương trình">✏️</button>
                  <button @click="deleteProgram(p.id)" class="btn-action delete" title="Xóa chương trình">🗑️</button>
                </div>
              </td>
            </tr>
            <tr v-if="programs.length === 0">
              <td colspan="5" class="text-center py-8 text-muted">Chưa có chương trình đào tạo nào. Hãy nhấn "+ Thêm chương trình mới".</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- VIEW 2: SUB-PAGE FORM: ADD/EDIT PROGRAM -->
    <div v-else-if="activeView === 'form'" class="admin-page-card" style="background: #ffffff; color: #0f172a; border-radius: 16px; padding: 28px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); border: 1px solid #e2e8f0;">
      <div class="flex-between pb-4 mb-4" style="border-bottom: 1px solid #e2e8f0;">
        <div style="display: flex; align-items: center; gap: 12px;">
          <button type="button" @click="activeView = 'list'" class="btn btn-secondary btn-sm" style="padding: 8px 16px; font-weight: 600;">
            ← Quay lại danh sách
          </button>
          <h3 style="margin: 0; color: #0f172a; font-size: 20px; font-weight: 800;">
            {{ isEditing ? 'Chỉnh sửa chương trình đào tạo' : 'Thêm chương trình đào tạo mới' }}
          </h3>
        </div>
        <button type="button" @click="activeView = 'list'" class="btn btn-secondary btn-sm">Hủy</button>
      </div>

      <form @submit.prevent="saveProgram" class="mt-2">
        <div class="form-group">
          <label style="color: #1e293b; font-weight: 600;">Tên chương trình đào tạo</label>
          <input v-model="form.title" @input="onTitleInput" type="text" required class="admin-input-style" placeholder="Ví dụ: Chương Trình Đào Tạo Chuyên Gia AI 2026" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
        </div>

        <div class="form-group mt-3">
          <label style="color: #1e293b; font-weight: 600;">Slug (Đường dẫn tĩnh - Tự động tạo)</label>
          <input v-model="form.slug" type="text" required class="admin-input-style" placeholder="chuong-trinh-chuyen-gia-ai-2026" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
        </div>

        <div class="form-group mt-3">
          <label style="color: #1e293b; font-weight: 600;">Hình ảnh đại diện (Tải ảnh từ máy lên Cloudinary hoặc dán URL)</label>
          <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
            <input v-model="form.image" type="text" class="admin-input-style" placeholder="/images/default.jpg hoặc URL Cloudinary" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1; flex: 1; min-width: 240px;" />
            <label class="btn btn-primary btn-sm" style="padding: 10px 16px; cursor: pointer; display: inline-flex; align-items: center; gap: 6px; white-space: nowrap; margin: 0; font-weight: 600;">
              <span>Tải ảnh từ máy</span>
              <input type="file" accept="image/*" @change="uploadProgramImage" style="display: none;" />
            </label>
          </div>
          <div v-if="uploadingProgramImage" style="font-size: 12px; color: #0284c7; margin-top: 4px; font-weight: 600;">
            Đang tải ảnh lên Cloudinary (Thư mục Acc Demo)...
          </div>
          <div v-if="form.image" class="mt-2">
            <img :src="form.image" alt="Preview" style="max-height: 100px; border-radius: 8px; border: 1px solid #cbd5e1; object-fit: cover;" />
          </div>
        </div>

        <!-- Select Child Courses for this Program -->
        <div class="form-group mt-4" style="padding: 18px; background: #f0fdf4; border-radius: 12px; border: 1px solid #bbf7d0;">
          <label class="font-bold mb-2" style="font-size: 15px; display: block; color: #15803d;">
            Chọn các khóa học thuộc Chương trình đào tạo này:
          </label>
          <div class="courses-checkbox-grid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 12px; max-height: 240px; overflow-y: auto; padding-right: 8px;">
            <label 
              v-for="c in courses" 
              :key="c.id"
              style="display: flex; align-items: center; gap: 10px; font-size: 13px; cursor: pointer; background: #ffffff; padding: 10px 14px; border-radius: 8px; border: 1px solid #cbd5e1; color: #0f172a; box-shadow: 0 1px 2px rgba(0,0,0,0.03);"
            >
              <input 
                type="checkbox" 
                :value="c.id" 
                v-model="form.courseIds"
                style="width: 18px; height: 18px; accent-color: #16a34a;"
              />
              <span style="flex: 1; font-weight: 600; color: #0f172a;">{{ c.title }}</span>
            </label>
          </div>
        </div>

        <div class="form-group mt-3">
          <label style="color: #1e293b; font-weight: 600;">Mô tả chi tiết chương trình</label>
          <textarea v-model="form.description" rows="4" class="admin-input-style" placeholder="Mô tả mục tiêu và lộ trình đào tạo tổng thể..." style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;"></textarea>
        </div>

        <div class="flex-between mt-6 pt-4" style="border-top: 1px solid #e2e8f0;">
          <button type="button" @click="activeView = 'list'" class="btn btn-secondary btn-sm" style="padding: 10px 24px;">Hủy bỏ</button>
          <button type="submit" class="btn btn-primary btn-sm" style="padding: 10px 32px; font-weight: 700;">Lưu chương trình</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useCourseStore } from '@/stores/courses';
import { slugify } from '@/utils/slugify';

const courseStore = useCourseStore();

const programs = computed(() => courseStore.programs);
const courses = computed(() => courseStore.courses);

const uploadingProgramImage = ref(false);

const uploadProgramImage = async (e) => {
  const file = e.target.files[0];
  if (!file) return;
  uploadingProgramImage.value = true;
  try {
    const url = await courseStore.uploadImage(file);
    form.value.image = url;
  } catch (err) {
    alert('Lỗi khi tải ảnh lên Cloudinary: ' + err.message);
  } finally {
    uploadingProgramImage.value = false;
  }
};

const onTitleInput = () => {
  if (!isEditing.value || !form.value.slug) {
    form.value.slug = slugify(form.value.title);
  }
};

const getChildCourses = (progId) => {
  return courses.value.filter(c => c.programId === progId);
};

// Active View State ('list' | 'form')
const activeView = ref('list');
const isEditing = ref(false);
const editingId = ref(null);
const form = ref({
  title: '',
  slug: '',
  image: '/images/default.jpg',
  description: '',
  courseIds: []
});

onMounted(() => {
  courseStore.fetchPrograms();
  if (courseStore.courses.length === 0) {
    courseStore.fetchCourses();
  }
});

const openAddModal = () => {
  isEditing.value = false;
  editingId.value = null;
  form.value = {
    title: '',
    slug: '',
    image: '/images/default.jpg',
    description: '',
    courseIds: []
  };
  activeView.value = 'form';
};

const editProgram = (p) => {
  isEditing.value = true;
  editingId.value = p.id;
  const childIds = getChildCourses(p.id).map(c => c.id);
  form.value = {
    title: p.title,
    slug: p.slug,
    image: p.image || '/images/default.jpg',
    description: p.description || '',
    courseIds: childIds
  };
  activeView.value = 'form';
};

const saveProgram = async () => {
  try {
    if (isEditing.value) {
      await courseStore.updateAdminProgram(editingId.value, form.value);
      alert('Cập nhật chương trình đào tạo thành công!');
    } else {
      await courseStore.addAdminProgram(form.value);
      alert('Thêm chương trình đào tạo mới thành công!');
    }
    activeView.value = 'list';
  } catch (err) {
    alert(err.message || 'Không thể lưu chương trình đào tạo.');
  }
};

const deleteProgram = async (id) => {
  if (confirm('Bạn có chắc chắn muốn xóa chương trình đào tạo này?')) {
    try {
      await courseStore.deleteAdminProgram(id);
      alert('Đã xóa chương trình đào tạo.');
    } catch (err) {
      alert(err.message || 'Không thể xóa chương trình.');
    }
  }
};
</script>
