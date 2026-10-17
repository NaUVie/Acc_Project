<template>
  <div class="tab-content animate-fade-in">
    <!-- VIEW 1: LECTURERS LIST TABLE -->
    <div v-if="activeView === 'list'">
      <div class="content-header flex-between">
        <div>
          <h2>Quản lý Đội ngũ Giảng viên</h2>
          <p>Danh sách các chuyên gia, giảng viên, cố vấn và quản lý các chuyên ngành đào tạo.</p>
        </div>
        <div style="display: flex; gap: 10px;">
          <button @click="openMajorsModal" class="btn btn-secondary btn-sm" style="font-weight: 600;">🏷️ Quản lý Chuyên ngành</button>
          <button @click="openAddLecturerModal" class="btn btn-primary btn-sm">+ Thêm giảng viên mới</button>
        </div>
      </div>

      <!-- Search & Page Size Bar -->
      <div class="filter-bar mt-4" style="display: flex; gap: 12px; align-items: center; justify-content: space-between; flex-wrap: wrap;">
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="Tìm theo tên, chức danh, chuyên ngành..." 
          class="admin-search-input"
          style="flex: 1; min-width: 200px;"
        />
        <div style="display: flex; align-items: center; gap: 8px; font-size: 13px; color: #475569; font-weight: 600;">
          <span>Hiển thị:</span>
          <select v-model="pageSize" class="admin-input-style" style="padding: 6px 12px; border-radius: 8px; border: 1px solid #cbd5e1; background: #ffffff; color: #0f172a; cursor: pointer;">
            <option :value="8">8 / trang</option>
            <option :value="20">20 / trang</option>
            <option :value="999">Tất cả (Dễ kéo thả sắp xếp)</option>
          </select>
        </div>
      </div>

      <!-- Table with Drag & Drop -->
      <div class="table-responsive mt-6">
        <table class="admin-table">
          <thead>
            <tr>
              <th style="width: 50px; text-align: center;">Thứ tự</th>
              <th>Avatar</th>
              <th>Mã ID</th>
              <th>Họ & Tên</th>
              <th>Chức danh / Vị trí</th>
              <th>Chuyên ngành</th>
              <th>Trang chủ (Max 4)</th>
              <th>Hành động</th>
            </tr>
          </thead>
          <tbody>
            <tr 
              v-for="(l, idx) in paginatedLecturers" 
              :key="l.id"
              draggable="true"
              @dragstart="onDragStart($event, idx)"
              @dragover.prevent="onDragOver($event, idx)"
              @drop="onDrop($event, idx)"
              :style="{ cursor: 'grab', background: dragOverIndex === ((currentPage - 1) * pageSize + idx) ? '#e0f2fe' : '' }"
            >
              <td style="text-align: center;">
                <span class="drag-handle" style="cursor: grab; font-size: 16px; color: #94a3b8; user-select: none;" title="Kéo thả để đổi thứ tự">☰ {{ (currentPage - 1) * pageSize + idx + 1 }}</span>
              </td>
              <td>
                <img :src="formatImageUrl(l.avatar || l.avatar_drive_link || '/images/default-avatar.jpg')" :alt="l.name" style="width: 44px; height: 44px; border-radius: 50%; object-fit: cover; border: 2px solid #0284c7;" />
              </td>
              <td class="font-bold text-xs" style="color: #64748b;">{{ l.id }}</td>
              <td class="font-bold" style="color: #0f172a;">{{ l.name }}</td>
              <td>
                <span class="badge badge-primary" style="background: #e0f2fe; color: #0369a1; border: 1px solid #bae6fd;">{{ l.title }}</span>
              </td>
              <td>
                <div style="display: flex; gap: 4px; flex-wrap: wrap;">
                  <span 
                    v-for="mId in (l.majorIds && l.majorIds.length > 0 ? l.majorIds : (l.majorId ? [l.majorId] : []))" 
                    :key="mId" 
                    class="badge badge-info" 
                    style="background: #e0f2fe; color: #0284c7; border: 1px solid #bae6fd; font-size: 11px; padding: 3px 8px;"
                  >
                    {{ getMajorNameById(mId) }}
                  </span>
                  <span v-if="!l.majorIds || l.majorIds.length === 0" style="color: #94a3b8; font-size: 12px;">-- Chưa chọn --</span>
                </div>
              </td>
              <td>
                <button 
                  type="button" 
                  @click="toggleFeatured(l)" 
                  class="btn btn-xs" 
                  :style="{
                    background: l.is_featured ? '#fef3c7' : '#f1f5f9',
                    color: l.is_featured ? '#b45309' : '#64748b',
                    border: l.is_featured ? '1px solid #fde68a' : '1px solid #cbd5e1',
                    borderRadius: '20px',
                    padding: '4px 12px',
                    fontWeight: '700',
                    cursor: 'pointer'
                  }"
                >
                  {{ l.is_featured ? '⭐ Đã chọn (' + featuredCount + '/4)' : '☆ Nổi bật' }}
                </button>
              </td>
              <td>
                <div class="action-buttons">
                  <button @click="editLecturer(l)" class="btn-action edit" title="Sửa thông tin">✏️</button>
                  <button @click="deleteLecturer(l)" class="btn-action delete" title="Xóa">🗑️</button>
                </div>
              </td>
            </tr>
            <tr v-if="filteredLecturers.length === 0">
              <td colspan="8" class="text-center py-8 text-muted">Không tìm thấy giảng viên nào.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination Component -->
      <Pagination 
        :currentPage="currentPage" 
        :totalItems="filteredLecturers.length" 
        :pageSize="pageSize" 
        @update:currentPage="currentPage = $event"
      />
    </div>

    <!-- VIEW 2: LECTURER ADD/EDIT FORM -->
    <div v-else-if="activeView === 'form'" class="admin-page-card" style="background: #ffffff; color: #0f172a; border-radius: 16px; padding: 28px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); border: 1px solid #e2e8f0;">
      <div class="flex-between pb-4 mb-4" style="border-bottom: 1px solid #e2e8f0;">
        <div style="display: flex; align-items: center; gap: 12px;">
          <button type="button" @click="activeView = 'list'" class="btn btn-secondary btn-sm" style="padding: 8px 16px; font-weight: 600;">
            ← Quay lại danh sách
          </button>
          <h3 style="margin: 0; color: #0f172a; font-size: 20px; font-weight: 800;">
            {{ isEditing ? 'Chỉnh sửa thông tin giảng viên' : 'Thêm giảng viên mới' }}
          </h3>
        </div>
        <button type="button" @click="activeView = 'list'" class="btn btn-secondary btn-sm">Hủy</button>
      </div>

      <form @submit.prevent="saveLecturer">
        <div class="grid-2">
          <div class="form-group">
            <label style="color: #1e293b; font-weight: 600;">Mã định danh (ID Slug)</label>
            <input v-model="lecturerForm.id" :disabled="isEditing" type="text" required class="admin-input-style" placeholder="ví dụ: le-quang-trieu" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
            <small v-if="!isEditing" class="text-muted">Mã ID duy nhất không dấu, ví dụ: le-van-a</small>
          </div>
          <div class="form-group">
            <label style="color: #1e293b; font-weight: 600;">Họ và Tên Giảng viên</label>
            <input v-model="lecturerForm.name" @input="onNameInput" type="text" required class="admin-input-style" placeholder="ví dụ: Lê Quang Triều" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
          </div>
        </div>

        <div class="form-group mt-3">
          <label style="color: #1e293b; font-weight: 600;">Chức danh / Vị trí công tác</label>
          <input v-model="lecturerForm.title" type="text" required class="admin-input-style" placeholder="ví dụ: Chuyên gia Khai phá Dữ liệu & AI Agent" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
        </div>

        <div class="form-group mt-3">
          <label style="color: #1e293b; font-weight: 600;">Chuyên ngành đào tạo (Có thể tích chọn nhiều chuyên ngành)</label>
          <div style="display: flex; gap: 12px 20px; flex-wrap: wrap; margin-top: 6px; background: #f8fafc; padding: 14px 18px; border-radius: 10px; border: 1px solid #cbd5e1;">
            <label 
              v-for="m in lecturerMajors" 
              :key="m.id" 
              style="display: inline-flex; align-items: center; gap: 8px; font-size: 13.5px; font-weight: 600; color: #334155; cursor: pointer; user-select: none;"
            >
              <input 
                type="checkbox" 
                :value="m.id" 
                v-model="lecturerForm.majorIds" 
                style="width: 17px; height: 17px; cursor: pointer; accent-color: #0284c7;" 
              />
              <span>{{ m.name }}</span>
            </label>
          </div>
        </div>

        <div class="form-group mt-3">
          <label style="color: #1e293b; font-weight: 600;">Hình ảnh Avatar (Tải từ máy hoặc dán URL)</label>
          <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
            <input v-model="lecturerForm.avatar" type="text" required class="admin-input-style" placeholder="/images/default-avatar.jpg hoặc URL Cloudinary" style="flex: 1; min-width: 240px; background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
            <label class="btn btn-primary btn-sm" style="padding: 10px 16px; cursor: pointer; display: inline-flex; align-items: center; gap: 6px; white-space: nowrap; margin: 0; font-weight: 600;">
              <span>Tải ảnh từ máy</span>
              <input type="file" accept="image/*" @change="uploadAvatar" style="display: none;" />
            </label>
          </div>
          <div v-if="uploadingAvatar" style="font-size: 12px; color: #0284c7; margin-top: 4px; font-weight: 600;">
            Đang tải ảnh lên Cloudinary...
          </div>
          <div v-if="lecturerForm.avatar" class="mt-2">
            <img :src="formatImageUrl(lecturerForm.avatar)" alt="Preview" style="width: 80px; height: 80px; border-radius: 50%; object-fit: cover; border: 2px solid #0284c7;" />
          </div>
        </div>

        <div class="form-group mt-3">
          <label style="color: #1e293b; font-weight: 600;">Tiêu đề ngắn / Tagline</label>
          <input v-model="lecturerForm.tagline" type="text" class="admin-input-style" placeholder="ví dụ: 10+ năm kinh nghiệm cố vấn Chuyển đổi số doanh nghiệp" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
        </div>

        <div class="form-group mt-3" style="display: flex; align-items: center; gap: 8px;">
          <input type="checkbox" id="is_featured_chk" v-model="lecturerForm.is_featured" style="width: 18px; height: 18px; cursor: pointer;" />
          <label for="is_featured_chk" style="color: #1e293b; font-weight: 600; cursor: pointer; margin: 0;">Hiển thị nổi bật ngoài Trang chủ (Tối đa 4 người)</label>
        </div>

        <div class="form-group mt-3">
          <label style="color: #1e293b; font-weight: 600;">Giới thiệu tóm tắt (Bio Short)</label>
          <textarea v-model="lecturerForm.bioShort" rows="3" class="admin-input-style" placeholder="Đoạn mô tả tóm tắt quá trình công tác, thành tựu..." style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;"></textarea>
        </div>

        <div class="flex-between mt-6 pt-4" style="border-top: 1px solid #e2e8f0;">
          <button type="button" @click="activeView = 'list'" class="btn btn-secondary btn-sm" style="padding: 10px 24px;">Hủy bỏ</button>
          <button type="submit" class="btn btn-primary btn-sm" style="padding: 10px 32px; font-weight: 700;">Lưu thông tin giảng viên</button>
        </div>
      </form>
    </div>

    <!-- MODAL LECTURER MAJORS CRUD -->
    <div v-if="showMajorsModal" class="modal-overlay" @click.self="closeMajorsModal">
      <div class="modal-content animate-fade-in" style="max-width: 700px;">
        <div class="modal-header">
          <h3>🏷️ Quản lý Chuyên ngành Giảng viên (Database)</h3>
          <button class="close-btn" @click="closeMajorsModal">&times;</button>
        </div>

        <div class="modal-body" style="padding: 16px 0;">
          <!-- Form Create / Edit Major -->
          <form @submit.prevent="saveMajor" style="background: #f8fafc; padding: 16px; border-radius: 12px; margin-bottom: 20px; border: 1px solid #e2e8f0;">
            <h4 style="margin-top: 0; margin-bottom: 12px; font-size: 15px; color: #0f172a; font-weight: 700;">
              {{ isEditingMajor ? '✏️ Chỉnh sửa chuyên ngành' : '➕ Thêm chuyên ngành mới' }}
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
                  <td colspan="5" class="text-center py-4 text-muted">Chưa có chuyên ngành nào trong Database.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="modal-footer" style="display: flex; justify-content: flex-end;">
          <button type="button" class="btn btn-secondary" @click="closeMajorsModal">Đóng</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useCourseStore } from '@/stores/courses';
import { slugify } from '@/utils/slugify';
import { formatImageUrl } from '@/utils/imageHelper';
import Pagination from '@/components/Pagination.vue';

const courseStore = useCourseStore();

const lecturers = computed(() => courseStore.lecturers || []);
const lecturerMajors = computed(() => courseStore.lecturerMajors || []);

const localLecturers = ref([]);

watch(lecturers, (newList) => {
  localLecturers.value = [...newList];
}, { immediate: true });

const featuredCount = computed(() => {
  return lecturers.value.filter(l => l.is_featured).length;
});

const getMajorNameById = (id) => {
  if (!id) return 'Chuyên gia';
  const match = lecturerMajors.value.find(m => m.id === id);
  return match ? match.name : id;
};

const getMajorLecturersCount = (majorId) => {
  return lecturers.value.filter(l => l.majorId === majorId).length;
};

// Drag and drop state & handlers
const draggedIndex = ref(null);
const dragOverIndex = ref(null);

const onDragStart = (e, index) => {
  const globalIndex = (currentPage.value - 1) * pageSize.value + index;
  draggedIndex.value = globalIndex;
  e.dataTransfer.effectAllowed = 'move';
};

const onDragOver = (e, index) => {
  const globalIndex = (currentPage.value - 1) * pageSize.value + index;
  dragOverIndex.value = globalIndex;
};

const onDrop = async (e, targetIndex) => {
  const globalTargetIndex = (currentPage.value - 1) * pageSize.value + targetIndex;
  if (draggedIndex.value === null || draggedIndex.value === globalTargetIndex) {
    draggedIndex.value = null;
    dragOverIndex.value = null;
    return;
  }

  const list = [...localLecturers.value];
  const [draggedItem] = list.splice(draggedIndex.value, 1);
  list.splice(globalTargetIndex, 0, draggedItem);
  localLecturers.value = list;

  draggedIndex.value = null;
  dragOverIndex.value = null;

  try {
    await courseStore.reorderLecturers(localLecturers.value);
    courseStore.showToast('Đã cập nhật thứ tự hiển thị giảng viên!', 'success');
  } catch (err) {
    courseStore.showToast('Không thể cập nhật thứ tự.', 'error');
  }
};

const toggleFeatured = async (l) => {
  try {
    const updated = await courseStore.toggleLecturerFeatured(l.id);
    const isNowFeatured = updated ? updated.is_featured : !l.is_featured;
    courseStore.showToast(isNowFeatured ? `Đã gắn mác Nổi bật Trang chủ cho ${l.name}` : `Đã bỏ Nổi bật đối với ${l.name}`, 'info');
  } catch (err) {
    courseStore.showToast(err.message || 'Không thể thay đổi trạng thái nổi bật.', 'error');
  }
};

const searchQuery = ref('');
const currentPage = ref(1);
const pageSize = ref(8);

watch([searchQuery, pageSize], () => {
  currentPage.value = 1;
});

const filteredLecturers = computed(() => {
  return localLecturers.value.filter(l => {
    const q = searchQuery.value.toLowerCase();
    const mName = (l.majorName || getMajorNameById(l.majorId)).toLowerCase();
    return l.name.toLowerCase().includes(q) || 
           l.title.toLowerCase().includes(q) ||
           mName.includes(q) ||
           (l.id && l.id.toLowerCase().includes(q));
  });
});

const paginatedLecturers = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  return filteredLecturers.value.slice(start, start + pageSize.value);
});

const activeView = ref('list'); // 'list' | 'form'
const isEditing = ref(false);
const uploadingAvatar = ref(false);

const lecturerForm = ref({
  id: '',
  name: '',
  title: '',
  tagline: '',
  avatar: '',
  avatarDriveLink: '',
  driveProfile: '',
  bioShort: '',
  detailsHtml: '',
  majorId: '',
  majorIds: [],
  is_featured: false
});

const onNameInput = () => {
  if (!isEditing.value) {
    lecturerForm.value.id = slugify(lecturerForm.value.name);
  }
};

onMounted(async () => {
  await Promise.all([
    courseStore.fetchLecturerMajors(),
    courseStore.fetchLecturers()
  ]);
});

const openAddLecturerModal = () => {
  isEditing.value = false;
  lecturerForm.value = {
    id: '',
    name: '',
    title: '',
    tagline: '',
    avatar: '/images/default-avatar.jpg',
    avatarDriveLink: '',
    driveProfile: '',
    bioShort: '',
    detailsHtml: '',
    majorId: lecturerMajors.value.length > 0 ? lecturerMajors.value[0].id : '',
    majorIds: lecturerMajors.value.length > 0 ? [lecturerMajors.value[0].id] : [],
    is_featured: false
  };
  activeView.value = 'form';
};

const editLecturer = (l) => {
  isEditing.value = true;
  const initialMajorIds = l.majorIds && l.majorIds.length > 0 ? [...l.majorIds] : (l.majorId ? [l.majorId] : []);
  lecturerForm.value = {
    id: l.id,
    name: l.name,
    title: l.title,
    tagline: l.tagline || '',
    avatar: l.avatar || l.avatar_drive_link || '/images/default-avatar.jpg',
    avatarDriveLink: l.avatar_drive_link || '',
    driveProfile: l.drive_profile || '',
    bioShort: l.bio_short || '',
    detailsHtml: l.details_html || '',
    majorId: l.majorId || '',
    majorIds: initialMajorIds,
    is_featured: l.is_featured || false
  };
  activeView.value = 'form';
};

const uploadAvatar = async (e) => {
  const file = e.target.files[0];
  if (!file) return;
  uploadingAvatar.value = true;
  try {
    const url = await courseStore.uploadImage(file);
    lecturerForm.value.avatar = url;
    courseStore.showToast('Tải ảnh đại diện thành công!', 'success');
  } catch (err) {
    courseStore.showToast('Lỗi khi tải ảnh: ' + err.message, 'error');
  } finally {
    uploadingAvatar.value = false;
  }
};

const saveLecturer = async () => {
  try {
    if (!lecturerForm.value.id.trim()) {
      courseStore.showToast('Vui lòng nhập mã ID duy nhất!', 'warning');
      return;
    }
    const payload = {
      ...lecturerForm.value,
      avatar: formatImageUrl(lecturerForm.value.avatar)
    };
    if (isEditing.value) {
      await courseStore.updateAdminLecturer(payload.id, payload);
      courseStore.showToast('Cập nhật giảng viên thành công!', 'success');
    } else {
      if (lecturers.value.some(l => l.id === payload.id)) {
        courseStore.showToast('Mã ID này đã được sử dụng!', 'warning');
        return;
      }
      await courseStore.addAdminLecturer(payload);
      courseStore.showToast('Thêm giảng viên mới thành công!', 'success');
    }
    activeView.value = 'list';
  } catch (err) {
    courseStore.showToast(err.message || 'Không thể lưu giảng viên.', 'error');
  }
};

const deleteLecturer = async (l) => {
  const isConfirmed = await courseStore.showConfirm({
    title: 'Xác nhận xóa giảng viên',
    message: `Bạn có chắc chắn muốn xóa giảng viên "${l.name}" khỏi hệ thống?`,
    confirmText: 'Đồng ý xóa',
    cancelText: 'Hủy bỏ',
    type: 'danger'
  });

  if (isConfirmed) {
    try {
      await courseStore.deleteAdminLecturer(l.id);
      courseStore.showToast(`Đã xóa giảng viên "${l.name}" thành công.`, 'success');
    } catch (err) {
      courseStore.showToast(err.message || 'Không thể xóa giảng viên.', 'error');
    }
  }
};

// --- LECTURER MAJORS CRUD MODAL STATE & ACTIONS ---
const showMajorsModal = ref(false);
const isEditingMajor = ref(false);
const majorForm = ref({
  id: '',
  name: '',
  icon: '🎓',
  badge: '',
  description: '',
  position: 0
});

const openMajorsModal = () => {
  resetMajorForm();
  showMajorsModal.value = true;
};

const closeMajorsModal = () => {
  showMajorsModal.value = false;
};

const resetMajorForm = () => {
  isEditingMajor.value = false;
  majorForm.value = {
    id: '',
    name: '',
    icon: '🎓',
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
    icon: m.icon || '🎓',
    badge: m.badge || m.name.toUpperCase(),
    description: m.description || '',
    position: m.position || 0
  };
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
  } catch (err) {
    courseStore.showToast(err.message || 'Lỗi khi lưu chuyên ngành.', 'error');
  }
};

const deleteMajor = async (m) => {
  const count = getMajorLecturersCount(m.id);
  let msg = `Bạn có chắc chắn muốn xóa chuyên ngành "${m.name}"?`;
  if (count > 0) {
    msg += `\n\n⚠️ Đang có ${count} giảng viên thuộc chuyên ngành này. Sau khi xóa, các giảng viên sẽ trở về trạng thái chưa thuộc chuyên ngành.`;
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
    } catch (err) {
      courseStore.showToast(err.message || 'Lỗi khi xóa chuyên ngành.', 'error');
    }
  }
};
</script>