<template>
  <div class="tab-content animate-fade-in">
    <!-- VIEW 1: LECTURERS LIST TABLE -->
    <div v-if="activeView === 'list'">
      <div class="content-header flex-between">
        <div>
          <h2>Quản lý Đội ngũ Giảng viên</h2>
          <p>Danh sách các chuyên gia, giảng viên, cố vấn và quản lý các chuyên ngành đào tạo.</p>
        </div>
        <div style="display: flex; gap: 8px; align-items: center; flex-shrink: 0; flex-wrap: wrap;">
          <button 
            @click="isReorderMode = !isReorderMode" 
            class="btn btn-sm"
            :style="{
              background: isReorderMode ? '#0284c7' : '#f1f5f9',
              color: isReorderMode ? '#ffffff' : '#334155',
              border: isReorderMode ? '1px solid #0284c7' : '1px solid #cbd5e1',
              fontWeight: '700',
              padding: '6px 12px',
              fontSize: '13px'
            }"
          >
            {{ isReorderMode ? '✓ Xong' : '↕ Sắp Xếp' }}
          </button>
          <button @click="refreshLecturers" :disabled="isRefreshing" class="btn btn-secondary btn-sm" style="display: flex; align-items: center; gap: 6px; font-weight: 600; padding: 6px 12px; font-size: 13px;" title="Tải lại danh sách giảng viên mới nhất từ máy chủ">
            <span :class="{ 'spin-icon': isRefreshing }">🔄</span>
            <span>{{ isRefreshing ? 'Đang đồng bộ...' : 'Làm mới' }}</span>
          </button>
          <button @click="showMajorsModal = true" class="btn btn-secondary btn-sm" style="font-weight: 600; padding: 6px 12px; font-size: 13px;">QL Chuyên Ngành</button>
          <button @click="openAddLecturer" class="btn btn-primary btn-sm" style="font-weight: 600; padding: 6px 14px; font-size: 13px;">+ Thêm</button>
        </div>
      </div>

      <!-- Search & Major Filter Bar -->
      <div class="filter-bar mt-4" style="display: flex; gap: 12px; align-items: center; justify-content: space-between; flex-wrap: wrap;">
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="Tìm theo tên, chức danh, chuyên ngành..." 
          class="admin-search-input"
          style="flex: 1; min-width: 200px;"
        />
        
        <!-- Filter by Major -->
        <div style="display: flex; align-items: center; gap: 8px; font-size: 13px; color: #475569; font-weight: 600;">
          <span>Lọc chuyên ngành:</span>
          <select v-model="selectedMajorFilter" class="admin-input-style" style="padding: 6px 12px; border-radius: 8px; border: 1px solid #cbd5e1; background: #ffffff; color: #0f172a; cursor: pointer; max-width: 230px;">
            <option value="all">Tất cả chuyên ngành ({{ lecturers.length }})</option>
            <option v-for="m in lecturerMajors" :key="m.id" :value="m.id">
              {{ m.name }} ({{ getMajorLecturersCount(m.id) }})
            </option>
          </select>
        </div>

        <div style="display: flex; align-items: center; gap: 8px; font-size: 13px; color: #475569; font-weight: 600;">
          <span>Hiển thị:</span>
          <select v-model="pageSize" class="admin-input-style" style="padding: 6px 12px; border-radius: 8px; border: 1px solid #cbd5e1; background: #ffffff; color: #0f172a; cursor: pointer;">
            <option :value="8">8 / trang</option>
            <option :value="20">20 / trang</option>
            <option :value="999">Tất cả (Dễ kéo thả sắp xếp)</option>
          </select>
        </div>
      </div>

      <!-- Table with Up / Down Order Buttons -->
      <div class="table-responsive mt-6">
        <table class="admin-table">
          <thead>
            <tr>
              <th style="width: 50px; text-align: center;">STT</th>
              <th style="width: 56px;">Avatar</th>
              <th style="min-width: 150px;">Họ & Tên</th>
              <th style="max-width: 200px;">Chức danh / Vị trí</th>
              <th style="max-width: 220px;">Chuyên ngành</th>
              <th style="width: 105px; text-align: center;">Trang chủ</th>
              <th style="width: 110px; text-align: center;">Nút chi tiết</th>
              <th style="width: 90px; text-align: center;">Hành động</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="isLoadingLecturers && filteredLecturers.length === 0">
              <td colspan="8">
                <div class="admin-center-loader" style="padding: 40px 0; min-height: 160px;">
                  <div class="admin-spinner"></div>
                  <p class="admin-loader-text">Đang nạp danh sách giảng viên...</p>
                </div>
              </td>
            </tr>
            <tr v-else-if="filteredLecturers.length === 0 && !isLoadingLecturers">
              <td colspan="8" class="text-center py-8 text-muted">Không tìm thấy giảng viên nào phù hợp.</td>
            </tr>
            <tr 
              v-else
              v-for="(l, idx) in paginatedLecturers" 
              :key="l.id"
            >
              <td style="text-align: center; width: 80px;" data-label="STT">
                <div v-if="isReorderMode" style="display: inline-flex; align-items: center; justify-content: center; gap: 3px; background: #f0f9ff; padding: 2px 6px; border-radius: 6px; border: 1px solid #bae6fd;">
                  <button 
                    type="button"
                    @click="moveLecturer(l, 'up')"
                    :disabled="isFirstInList(l)"
                    class="btn-arrow"
                    title="Di chuyển lên trên"
                    :style="{
                      opacity: isFirstInList(l) ? '0.3' : '1',
                      cursor: isFirstInList(l) ? 'not-allowed' : 'pointer'
                    }"
                  >
                    ▲
                  </button>
                  <span style="font-weight: 800; font-size: 13px; color: #0284c7; min-width: 20px; text-align: center;">
                    {{ (currentPage - 1) * pageSize + idx + 1 }}
                  </span>
                  <button 
                    type="button"
                    @click="moveLecturer(l, 'down')"
                    :disabled="isLastInList(l)"
                    class="btn-arrow"
                    title="Di chuyển xuống dưới"
                    :style="{
                      opacity: isLastInList(l) ? '0.3' : '1',
                      cursor: isLastInList(l) ? 'not-allowed' : 'pointer'
                    }"
                  >
                    ▼
                  </button>
                </div>
                <span v-else style="font-weight: 700; font-size: 13px; color: #64748b;">
                  {{ (currentPage - 1) * pageSize + idx + 1 }}
                </span>
              </td>
              <td data-label="Avatar">
                <img :src="formatImageUrl(l.avatar || l.avatar_drive_link || '/images/default-avatar.jpg')" :alt="l.name" style="width: 40px; height: 40px; border-radius: 50%; object-fit: cover; border: 2px solid #0284c7;" />
              </td>
              <td class="wrap-cell" data-label="Họ & Tên">
                <div class="font-bold" style="color: #0f172a; font-size: 14px;">{{ l.name }}</div>
                <div class="text-xs" style="color: #94a3b8; font-size: 11px;">ID: {{ l.id }}</div>
              </td>
              <td class="wrap-cell" style="max-width: 200px;" data-label="Chức danh / Vị trí">
                <span 
                  class="badge badge-primary truncate-text" 
                  :title="l.title"
                  style="background: #e0f2fe; color: #0369a1; border: 1px solid #bae6fd; font-size: 12px; display: inline-block; max-width: 100%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; vertical-align: middle;"
                >
                  {{ l.title }}
                </span>
              </td>
              <td class="wrap-cell" style="max-width: 220px;" data-label="Chuyên ngành">
                <div style="display: flex; gap: 4px; flex-wrap: wrap;">
                  <span 
                    v-for="mId in (l.majorIds && l.majorIds.length > 0 ? l.majorIds : (l.majorId ? [l.majorId] : []))" 
                    :key="mId" 
                    class="badge badge-info" 
                    :title="getMajorNameById(mId)"
                    style="background: #f1f5f9; color: #334155; border: 1px solid #cbd5e1; font-size: 11px; padding: 2px 7px; border-radius: 6px; max-width: 210px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;"
                  >
                    {{ getMajorNameById(mId) }}
                  </span>
                  <span v-if="!l.majorIds || l.majorIds.length === 0" style="color: #94a3b8; font-size: 12px;">-- Chưa chọn --</span>
                </div>
              </td>
              <td style="text-align: center;" data-label="Trang chủ">
                <button 
                  type="button" 
                  @click="toggleFeatured(l)" 
                  class="btn btn-xs" 
                  :style="{
                    background: l.is_featured ? '#fef3c7' : '#f1f5f9',
                    color: l.is_featured ? '#b45309' : '#64748b',
                    border: l.is_featured ? '1px solid #fde68a' : '1px solid #cbd5e1',
                    borderRadius: '20px',
                    padding: '3px 10px',
                    fontWeight: '700',
                    cursor: 'pointer',
                    fontSize: '11px',
                    whiteSpace: 'nowrap'
                  }"
                >
                  {{ l.is_featured ? '⭐ Nổi bật' : '☆ Thường' }}
                </button>
              </td>
              <td style="text-align: center;" data-label="Nút chi tiết">
                <button 
                  type="button" 
                  @click="toggleShowDetail(l)" 
                  class="btn btn-xs" 
                  :style="{
                    background: (l.show_detail_btn || l.showDetailBtn) ? '#ecfdf5' : '#f8fafc',
                    color: (l.show_detail_btn || l.showDetailBtn) ? '#059669' : '#94a3b8',
                    border: (l.show_detail_btn || l.showDetailBtn) ? '1px solid #a7f3d0' : '1px solid #cbd5e1',
                    borderRadius: '20px',
                    padding: '3px 10px',
                    fontWeight: '700',
                    cursor: 'pointer',
                    fontSize: '11px',
                    whiteSpace: 'nowrap'
                  }"
                  :title="(l.show_detail_btn || l.showDetailBtn) ? 'Đang BẬT nút xem chi tiết ở danh sách giảng viên' : 'Đang TẮT nút xem chi tiết (mặc định)'"
                >
                  {{ (l.show_detail_btn || l.showDetailBtn) ? '👁️ Hiện nút' : '🚫 Ẩn nút' }}
                </button>
              </td>
              <td style="text-align: center;" data-label="Hành động">
                <div class="action-buttons" style="justify-content: center; gap: 6px;">
                  <button @click="openQuickCropper(l)" class="btn-action edit" title="Cắt lại Avatar (1:1)" style="color: #0284c7;">✂️</button>
                  <button @click="editLecturer(l)" class="btn-action edit" title="Sửa thông tin">✏️</button>
                  <button @click="deleteLecturer(l)" class="btn-action delete" title="Xóa">🗑️</button>
                </div>
              </td>
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

    <!-- VIEW 2: LECTURER ADD/EDIT FORM (Extracted Component) -->
    <LecturerFormView 
      v-else-if="activeView === 'form'"
      :initialData="editingLecturer"
      :lecturers="lecturers"
      @cancel="activeView = 'list'"
      @saved="onLecturerSaved"
    />

    <!-- MODAL LECTURER MAJORS CRUD (Extracted Component) -->
    <LecturerMajorsModal 
      :isOpen="showMajorsModal"
      :lecturers="lecturers"
      @close="showMajorsModal = false"
      @updated="courseStore.fetchLecturers()"
    />

    <!-- Quick Table Image Cropper Modal -->
    <ImageCropperModal 
      :isOpen="isCropperOpen" 
      :imageUrl="cropTargetUrl" 
      :aspectRatio="'square'" 
      :title="cropModalTitle" 
      @close="isCropperOpen = false" 
      @cropped="handleQuickCropped" 
    />
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useCourseStore } from '@/stores/courses';
import { formatImageUrl } from '@/utils/imageHelper';
import Pagination from '@/components/Pagination.vue';
import ImageCropperModal from '@/components/ImageCropperModal.vue';
import LecturerMajorsModal from '../modals/LecturerMajorsModal.vue';
import LecturerFormView from '../modals/LecturerFormView.vue';

const courseStore = useCourseStore();
const isLoadingLecturers = ref(courseStore.lecturers.length === 0);
const isRefreshing = ref(false);

const refreshLecturers = async () => {
  isRefreshing.value = true;
  try {
    await Promise.all([
      courseStore.fetchLecturers(true),
      courseStore.fetchLecturerMajors(true)
    ]);
    courseStore.showToast('Đã làm mới danh sách giảng viên mới nhất!', 'success');
  } catch (err) {
    courseStore.showToast('Lỗi khi làm mới: ' + (err.message || err), 'error');
  } finally {
    isRefreshing.value = false;
  }
};

// View navigation
const activeView = ref('list');
const editingLecturer = ref(null);
const showMajorsModal = ref(false);

// Cropper States for quick edit in table
const isCropperOpen = ref(false);
const cropTargetUrl = ref('');
const cropModalTitle = ref('✂ Cắt Avatar Giảng Viên');
let quickCropperTargetLecturer = null;

const isReorderMode = ref(false);
const searchQuery = ref('');
const selectedMajorFilter = ref('all');
const currentPage = ref(1);
const pageSize = ref(8);

const lecturers = computed(() => courseStore.lecturers || []);
const lecturerMajors = computed(() => courseStore.lecturerMajors || []);
const localLecturers = ref([]);

watch(lecturers, (newList) => {
  localLecturers.value = [...newList];
}, { immediate: true });

const getMajorNameById = (id) => {
  if (!id) return 'Chuyên gia';
  const match = lecturerMajors.value.find(m => m.id === id);
  return match ? match.name : id;
};

const getMajorLecturersCount = (majorId) => {
  return lecturers.value.filter(l => {
    const ids = l.majorIds && l.majorIds.length > 0 ? l.majorIds : (l.majorId ? [l.majorId] : []);
    return ids.includes(majorId);
  }).length;
};

const filteredLecturers = computed(() => {
  let list = [...localLecturers.value];

  if (selectedMajorFilter.value !== 'all') {
    list = list.filter(l => {
      const ids = l.majorIds && l.majorIds.length > 0 ? l.majorIds : (l.majorId ? [l.majorId] : []);
      return ids.includes(selectedMajorFilter.value);
    });
  }

  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase().trim();
    list = list.filter(l => {
      const nameMatch = (l.name || '').toLowerCase().includes(q);
      const titleMatch = (l.title || '').toLowerCase().includes(q);
      const majorMatch = (l.majorIds || []).some(id => getMajorNameById(id).toLowerCase().includes(q));
      return nameMatch || titleMatch || majorMatch;
    });
  }

  return list;
});

const paginatedLecturers = computed(() => {
  if (pageSize.value === 999) return filteredLecturers.value;
  const start = (currentPage.value - 1) * pageSize.value;
  return filteredLecturers.value.slice(start, start + pageSize.value);
});

const isFirstInList = (l) => {
  const list = filteredLecturers.value;
  return list.length > 0 && list[0].id === l.id;
};

const isLastInList = (l) => {
  const list = filteredLecturers.value;
  return list.length > 0 && list[list.length - 1].id === l.id;
};

const moveLecturer = async (l, direction) => {
  const list = [...filteredLecturers.value];
  const currentIndex = list.findIndex(item => item.id === l.id);
  if (currentIndex === -1) return;

  const targetIndex = direction === 'up' ? currentIndex - 1 : currentIndex + 1;
  if (targetIndex < 0 || targetIndex >= list.length) return;

  const temp = list[currentIndex];
  list[currentIndex] = list[targetIndex];
  list[targetIndex] = temp;

  localLecturers.value = list;

  try {
    const isFiltered = selectedMajorFilter.value !== 'all';
    const reorderedPayload = list.map((item, index) => {
      const pos = index + 1;
      if (isFiltered) {
        const majorPos = item.major_positions ? { ...item.major_positions } : {};
        majorPos[selectedMajorFilter.value] = pos;
        return { id: item.id, major_positions: majorPos };
      }
      return { id: item.id, position: pos };
    });

    await courseStore.reorderAdminLecturers(reorderedPayload);
  } catch (err) {
    courseStore.showToast(err.message || 'Lỗi khi lưu vị trí giảng viên.', 'error');
  }
};

const openQuickCropper = (l) => {
  quickCropperTargetLecturer = l;
  cropTargetUrl.value = l.avatar || l.avatar_drive_link || '/images/default-avatar.jpg';
  cropModalTitle.value = `✂ Cắt Avatar Giảng Viên: ${l.name}`;
  isCropperOpen.value = true;
};

const handleQuickCropped = async (newUrl) => {
  isCropperOpen.value = false;
  if (quickCropperTargetLecturer) {
    await courseStore.updateAdminLecturer(quickCropperTargetLecturer.id, {
      ...quickCropperTargetLecturer,
      avatar: newUrl,
      avatar_drive_link: ''
    });
    quickCropperTargetLecturer.avatar = newUrl;
    quickCropperTargetLecturer.avatar_drive_link = '';
    courseStore.showToast('Đã cắt và cập nhật ảnh giảng viên!', 'success');
    quickCropperTargetLecturer = null;
  }
};

const openAddLecturer = () => {
  editingLecturer.value = null;
  activeView.value = 'form';
};

const editLecturer = (l) => {
  editingLecturer.value = l;
  activeView.value = 'form';
};

const onLecturerSaved = () => {
  activeView.value = 'list';
  courseStore.fetchLecturers();
};

const toggleFeatured = async (l) => {
  try {
    const newStatus = !l.is_featured;
    await courseStore.updateAdminLecturer(l.id, { ...l, is_featured: newStatus });
    l.is_featured = newStatus;
    courseStore.showToast(`Đã ${newStatus ? 'đặt làm nổi bật' : 'bỏ nổi bật'} giảng viên ${l.name}`, 'success');
  } catch (err) {
    courseStore.showToast(err.message || 'Lỗi khi đổi trạng thái nổi bật.', 'error');
  }
};

const toggleShowDetail = async (l) => {
  try {
    const currentStatus = !!(l.show_detail_btn || l.showDetailBtn);
    const newStatus = !currentStatus;
    await courseStore.updateAdminLecturer(l.id, { ...l, show_detail_btn: newStatus });
    l.show_detail_btn = newStatus;
    l.showDetailBtn = newStatus;
    courseStore.showToast(`Đã ${newStatus ? 'bật' : 'tắt'} nút xem chi tiết cho ${l.name}`, 'success');
  } catch (err) {
    courseStore.showToast(err.message || 'Lỗi khi đổi cài đặt nút chi tiết.', 'error');
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
      if (l.avatar && l.avatar.includes('cloudinary.com')) {
        courseStore.deleteImage(l.avatar);
      }
      courseStore.showToast(`Đã xóa giảng viên "${l.name}" thành công.`, 'success');
    } catch (err) {
      courseStore.showToast(err.message || 'Không thể xóa giảng viên.', 'error');
    }
  }
};

onMounted(async () => {
  try {
    await Promise.all([
      courseStore.fetchLecturerMajors(),
      courseStore.fetchLecturers()
    ]);
  } finally {
    isLoadingLecturers.value = false;
  }
});
</script>
