<template>
  <div class="admin-page-card" style="background: #ffffff; color: #0f172a; border-radius: 16px; padding: 28px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); border: 1px solid #e2e8f0;">
    <div class="flex-between pb-4 mb-4" style="border-bottom: 1px solid #e2e8f0;">
      <div style="display: flex; align-items: center; gap: 12px;">
        <button type="button" @click="$emit('cancel')" class="btn btn-secondary btn-sm" style="padding: 8px 16px; font-weight: 600;">
          ← Quay lại danh sách
        </button>
        <h3 style="margin: 0; color: #0f172a; font-size: 20px; font-weight: 800;">
          {{ isEditing ? 'Chỉnh sửa thông tin giảng viên' : 'Thêm giảng viên mới' }}
        </h3>
      </div>
      <button type="button" @click="$emit('cancel')" class="btn btn-secondary btn-sm">Hủy</button>
    </div>

    <form @submit.prevent="saveLecturer">
      <div class="grid-2">
        <div class="form-group">
          <label style="color: #1e293b; font-weight: 600;">Họ và Tên Giảng viên</label>
          <input v-model="lecturerForm.name" @input="onNameInput" type="text" required class="admin-input-style" placeholder="ví dụ: Lê Quang Triều" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
        </div>
        <div class="form-group">
          <label style="color: #1e293b; font-weight: 600;">Chức danh / Vị trí công tác</label>
          <input v-model="lecturerForm.title" type="text" required class="admin-input-style" placeholder="ví dụ: Chuyên gia Khai phá Dữ liệu & AI Agent" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
        </div>
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
            <input type="file" accept="image/*" @change="onFileSelectForCrop($event, (url) => { lecturerForm.avatar = url; lecturerForm.avatarDriveLink = ''; }, 'square', '✂ Cắt Avatar Giảng Viên (1:1)')" style="display: none;" />
          </label>
        </div>
        <div v-if="uploadingAvatar" style="font-size: 12px; color: #0284c7; margin-top: 4px; font-weight: 600;">
          Đang tải ảnh lên Cloudinary...
        </div>
        <div v-if="lecturerForm.avatar" class="mt-2" style="display: flex; align-items: center; gap: 12px;">
          <img :src="formatImageUrl(lecturerForm.avatar)" alt="Preview" style="width: 70px; height: 70px; border-radius: 50%; object-fit: cover; border: 2px solid #0284c7;" />
          <button type="button" class="btn btn-sm btn-secondary" style="font-size: 12px; font-weight: 600; color: #0284c7; border-color: #bae6fd;" @click="openCropper(lecturerForm.avatar, (url) => { lecturerForm.avatar = url; lecturerForm.avatarDriveLink = ''; }, 'square', '✂ Cắt Avatar Giảng Viên (1:1)')">✂ Cắt lại ảnh</button>
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

      <div class="form-group mt-3" style="display: flex; align-items: center; gap: 8px;">
        <input type="checkbox" id="show_detail_btn_chk" v-model="lecturerForm.show_detail_btn" style="width: 18px; height: 18px; cursor: pointer;" />
        <label for="show_detail_btn_chk" style="color: #1e293b; font-weight: 600; cursor: pointer; margin: 0;">👁️ Hiển thị nút "Xem chi tiết giới thiệu" ở thẻ Giảng viên (Mặc định tắt)</label>
      </div>

      <div class="form-group mt-3">
        <label style="color: #1e293b; font-weight: 600;">Giới thiệu tóm tắt (Bio Short)</label>
        <textarea v-model="lecturerForm.bioShort" rows="3" class="admin-input-style" placeholder="Đoạn mô tả ngắn tóm tắt quá trình công tác, thành tựu..." style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;"></textarea>
      </div>

      <!-- Detailed Content Editor (Rich Text) -->
      <div class="form-group mt-4 p-4" style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; flex-wrap: wrap; gap: 6px;">
          <label style="color: #0f172a; font-weight: 700; font-size: 14.5px; margin: 0;">
            📝 Nội dung Giới thiệu chi tiết (Soạn thảo văn bản, Chèn ảnh, Xuống hàng, Định dạng)
          </label>
          <span style="font-size: 12px; color: #64748b;">Hỗ trợ chèn ảnh, đề mục H2/H3, in đậm, danh sách...</span>
        </div>
        <RichTextEditor 
          v-model="lecturerForm.detailsHtml" 
          placeholder="Nhập nội dung chi tiết về quá trình công tác, thành tựu, hình ảnh hoạt động đào tạo của giảng viên (nội dung này sẽ hiển thị ở trang Chi tiết Giảng viên)..." 
        />
      </div>

      <!-- Position Settings -->
      <div class="form-group mt-3" style="background: #f8fafc; padding: 16px; border-radius: 12px; border: 1px solid #e2e8f0;">
        <h4 style="margin: 0 0 12px 0; font-size: 14px; font-weight: 700; color: #0f172a;">
          🔢 Cài đặt Thứ tự hiển thị
        </h4>
        <div class="grid-2">
          <div class="form-group">
            <label style="color: #1e293b; font-weight: 600; font-size: 13px;">Thứ tự chung (Trang Tất cả chuyên ngành)</label>
            <input 
              v-model.number="lecturerForm.position" 
              type="number" 
              min="1" 
              class="admin-input-style" 
              placeholder="1, 2, 3..." 
              style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" 
            />
            <small class="text-muted">Vị trí hiển thị tại danh sách Tất cả.</small>
          </div>
        </div>

        <div v-if="lecturerForm.majorIds && lecturerForm.majorIds.length > 0" class="mt-3">
          <label style="color: #1e293b; font-weight: 600; font-size: 13px; margin-bottom: 6px; display: block;">
            Thứ tự riêng theo từng chuyên ngành đã chọn:
          </label>
          <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 12px;">
            <div 
              v-for="mId in lecturerForm.majorIds" 
              :key="mId"
              style="background: #ffffff; padding: 10px 14px; border-radius: 8px; border: 1px solid #cbd5e1; display: flex; align-items: center; justify-content: space-between; gap: 10px;"
            >
              <span style="font-size: 12.5px; font-weight: 600; color: #334155;">{{ getMajorNameById(mId) }}</span>
              <div style="display: flex; align-items: center; gap: 6px;">
                <span style="font-size: 12px; color: #64748b;">Số:</span>
                <input 
                  type="number" 
                  min="1" 
                  :value="lecturerForm.major_positions ? lecturerForm.major_positions[mId] : ''"
                  @input="updateFormMajorPos(mId, $event.target.value)"
                  class="admin-input-style" 
                  placeholder="Mặc định"
                  style="width: 75px; text-align: center; padding: 4px 8px; font-size: 13px; font-weight: 700; color: #0284c7;"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="flex-between mt-6 pt-4" style="border-top: 1px solid #e2e8f0;">
        <button type="button" @click="$emit('cancel')" class="btn btn-secondary btn-sm" style="padding: 10px 24px;">Hủy bỏ</button>
        <button 
          type="submit" 
          class="btn btn-primary btn-sm" 
          :disabled="uploadingAvatar || savingLecturer" 
          style="padding: 10px 32px; font-weight: 700; display: inline-flex; align-items: center; gap: 8px;"
        >
          <span v-if="savingLecturer" style="width: 14px; height: 14px; border: 2px solid #ffffff; border-top-color: transparent; border-radius: 50%; display: inline-block; animation: spin 0.8s linear infinite;"></span>
          <span>{{ savingLecturer ? 'Đang lưu giảng viên...' : (uploadingAvatar ? 'Đang tải ảnh...' : 'Lưu thông tin giảng viên') }}</span>
        </button>
      </div>
    </form>

    <!-- Image Cropper Modal -->
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
import { slugify } from '@/utils/slugify';
import { formatImageUrl } from '@/utils/imageHelper';
import ImageCropperModal from '@/components/ImageCropperModal.vue';
import RichTextEditor from '@/components/RichTextEditor.vue';

const props = defineProps({
  initialData: {
    type: Object,
    default: null
  },
  lecturers: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits(['cancel', 'saved']);

const courseStore = useCourseStore();
const lecturerMajors = computed(() => courseStore.lecturerMajors || []);
const isEditing = computed(() => !!(props.initialData && props.initialData.id));

const savingLecturer = ref(false);
const uploadingAvatar = ref(false);
const pendingDeleteImages = ref([]);

// Cropper States
const isCropperOpen = ref(false);
const cropTargetUrl = ref('');
const cropAspectRatio = ref('square');
const cropModalTitle = ref('✂ Cắt & Căn Chỉnh Avatar Giảng Viên');
let cropTargetCallback = null;

const lecturerForm = ref({
  id: '',
  name: '',
  title: '',
  tagline: '',
  avatar: '/images/default-avatar.jpg',
  avatarDriveLink: '',
  driveProfile: '',
  bioShort: '',
  detailsHtml: '',
  majorId: '',
  majorIds: [],
  position: 1,
  major_positions: {},
  is_featured: false,
  show_detail_btn: false
});

onMounted(() => {
  if (props.initialData) {
    const l = props.initialData;
    const initialMajorIds = l.majorIds && l.majorIds.length > 0 ? [...l.majorIds] : (l.majorId ? [l.majorId] : []);
    lecturerForm.value = {
      id: l.id,
      name: l.name,
      title: l.title,
      tagline: l.tagline || '',
      avatar: l.avatar || l.avatar_drive_link || '/images/default-avatar.jpg',
      avatarDriveLink: l.avatar_drive_link || '',
      driveProfile: l.drive_profile || '',
      bioShort: l.bio_short || l.bioShort || '',
      detailsHtml: l.details_html || l.detailsHtml || '',
      majorId: l.majorId || '',
      majorIds: initialMajorIds,
      position: l.position ?? 1,
      major_positions: l.major_positions ? { ...l.major_positions } : {},
      is_featured: l.is_featured || false,
      show_detail_btn: !!(l.show_detail_btn ?? l.showDetailBtn ?? false)
    };

    if (!l.details_html && !l.detailsHtml && l.id) {
      courseStore.apiRequest(`/lecturers/${l.id}`).then(full => {
        if (full && full.details_html && isEditing.value) {
          lecturerForm.value.detailsHtml = full.details_html;
          l.details_html = full.details_html;
        }
      }).catch(() => {});
    }
  } else {
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
      position: (props.lecturers.length || 0) + 1,
      major_positions: {},
      is_featured: false,
      show_detail_btn: false
    };
  }
});

const onNameInput = () => {
  // auto slugify placeholder or handle in save
};

const getMajorNameById = (id) => {
  if (!id) return 'Chuyên gia';
  const match = lecturerMajors.value.find(m => m.id === id);
  return match ? match.name : id;
};

const updateFormMajorPos = (mId, val) => {
  if (!lecturerForm.value.major_positions) {
    lecturerForm.value.major_positions = {};
  }
  const num = parseInt(val);
  if (!isNaN(num) && num > 0) {
    lecturerForm.value.major_positions[mId] = num;
  } else {
    delete lecturerForm.value.major_positions[mId];
  }
};

const openCropper = (url, callback, ratio = 'square', title = '✂ Cắt & Căn Chỉnh Avatar Giảng Viên') => {
  if (!url) return;
  cropTargetUrl.value = url;
  cropAspectRatio.value = ratio;
  cropModalTitle.value = title;
  cropTargetCallback = callback;
  isCropperOpen.value = true;
};

const onFileSelectForCrop = (event, callback, ratio = 'square', title = '✂ Cắt & Căn Chỉnh Avatar Giảng Viên') => {
  const file = event.target?.files?.[0];
  if (!file) return;
  if (isEditing.value && lecturerForm.value.avatar && lecturerForm.value.avatar.includes('cloudinary.com')) {
    if (!pendingDeleteImages.value.includes(lecturerForm.value.avatar)) {
      pendingDeleteImages.value.push(lecturerForm.value.avatar);
    }
  }
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

const saveLecturer = async () => {
  if (uploadingAvatar.value || savingLecturer.value) {
    if (uploadingAvatar.value) courseStore.showToast('Ảnh đang tải lên, vui lòng đợi trong giây lát...', 'warning');
    return;
  }
  try {
    if (!lecturerForm.value.name.trim()) {
      courseStore.showToast('Vui lòng nhập họ và tên giảng viên!', 'warning');
      return;
    }

    savingLecturer.value = true;

    let baseId = (lecturerForm.value.id || slugify(lecturerForm.value.name)).trim();
    if (!baseId) {
      baseId = 'gv-' + Date.now().toString(36);
    }

    let finalId = baseId;
    if (!isEditing.value) {
      let counter = 2;
      while (props.lecturers.some(l => l.id === finalId)) {
        finalId = `${baseId}-${counter}`;
        counter++;
      }
    }
    lecturerForm.value.id = finalId;

    const cleanAvatar = (lecturerForm.value.avatar || '').trim();
    let finalAvatar = formatImageUrl(cleanAvatar);
    let finalDriveLink = lecturerForm.value.avatarDriveLink || '';

    if (cleanAvatar.includes('drive.google.com')) {
      finalDriveLink = cleanAvatar;
    } else if (cleanAvatar.startsWith('http') && !cleanAvatar.includes('drive.google.com')) {
      finalDriveLink = '';
    }

    const payload = {
      ...lecturerForm.value,
      id: finalId,
      avatar: finalAvatar,
      avatarDriveLink: finalDriveLink,
      detailsHtml: lecturerForm.value.detailsHtml || '',
      show_detail_btn: !!lecturerForm.value.show_detail_btn
    };

    if (isEditing.value) {
      await courseStore.updateAdminLecturer(payload.id, payload);
      courseStore.showToast('Cập nhật giảng viên thành công!', 'success');
    } else {
      await courseStore.addAdminLecturer(payload);
      courseStore.showToast('Thêm giảng viên mới thành công!', 'success');
    }

    if (pendingDeleteImages.value.length > 0) {
      for (const oldImg of pendingDeleteImages.value) {
        courseStore.deleteImage(oldImg);
      }
      pendingDeleteImages.value = [];
    }

    emit('saved');
  } catch (err) {
    courseStore.showToast(err.message || 'Không thể lưu giảng viên.', 'error');
  } finally {
    savingLecturer.value = false;
  }
};
</script>

