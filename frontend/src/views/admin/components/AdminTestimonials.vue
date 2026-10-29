<template>
  <div class="tab-content animate-fade-in">
    <!-- VIEW 1: LIST TABLE -->
    <div v-if="activeView === 'list'">
      <div class="content-header flex-between">
        <div>
          <h2>Quản lý Cảm nhận & Video Feedback Học viên</h2>
          <p>Quản lý các lời nhận xét, hình ảnh thực tế và video phỏng vấn học viên trên YouTube.</p>
        </div>
        <button @click="openAddModal" class="btn btn-primary btn-sm">+ Thêm Cảm nhận mới</button>
      </div>

      <!-- Filters & Search -->
      <div class="flex-between mt-4 mb-4 gap-4" style="flex-wrap: wrap;">
        <div class="filter-tabs" style="display: flex; gap: 8px; margin: 0;">
          <button 
            @click="filterType = 'all'" 
            class="btn btn-sm"
            :class="filterType === 'all' ? 'btn-primary' : 'btn-secondary'"
          >
            Tất cả ({{ testimonials.length }})
          </button>
          <button 
            @click="filterType = 'video'" 
            class="btn btn-sm"
            :class="filterType === 'video' ? 'btn-primary' : 'btn-secondary'"
          >
            Video YouTube ({{ videoCount }})
          </button>
          <button 
            @click="filterType = 'photo'" 
            class="btn btn-sm"
            :class="filterType === 'photo' ? 'btn-primary' : 'btn-secondary'"
          >
            Ảnh & Bài viết ({{ photoCount }})
          </button>
        </div>

        <div style="position: relative; min-width: 260px;">
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="Tìm theo tên học viên, chức danh, công ty..." 
            class="admin-input-style"
            style="padding-left: 14px; background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;"
          />
        </div>
      </div>

      <!-- Testimonials Table -->
      <div class="table-responsive">
        <table class="admin-table">
          <thead>
            <tr>
              <th style="width: 50px;">ID</th>
              <th style="width: 100px;">Loại</th>
              <th>Preview</th>
              <th>Học viên & Chức danh</th>
              <th>Khóa học</th>
              <th>Nội dung / Trích dẫn</th>
              <th style="width: 110px;">Hành động</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="t in paginatedTestimonials" :key="t.id">
              <td class="font-bold text-center">#{{ t.id }}</td>
              <td>
                <span 
                  class="badge" 
                  :style="t.testimonial_type === 'video' ? 'background: #ffe4e6; color: #be123c;' : (t.testimonial_type === 'photo' ? 'background: #e0f2fe; color: #0369a1;' : 'background: #f1f5f9; color: #475569;')"
                >
                  {{ t.testimonial_type === 'video' ? 'Video' : (t.testimonial_type === 'photo' ? 'Ảnh' : 'Trích dẫn') }}
                </span>
              </td>
              <td>
                <div style="position: relative; width: 80px; height: 50px; border-radius: 8px; overflow: hidden; background: #0f172a; border: 1px solid #cbd5e1;">
                  <img 
                    :src="formatImageUrl(t.thumbnail || t.image) || 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=200&q=80'" 
                    :alt="t.name" 
                    style="width: 100%; height: 100%; object-fit: cover;" 
                    referrerpolicy="no-referrer"
                  />
                  <div v-if="t.testimonial_type === 'video'" style="position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; background: rgba(0,0,0,0.3);">
                    <span style="color: #ffffff; font-size: 16px;">▶</span>
                  </div>
                </div>
              </td>
              <td>
                <div class="font-bold" style="color: #0f172a; font-size: 15px;">{{ t.name }}</div>
                <small class="text-muted" style="display: block; margin-top: 2px; color: #475569;">
                  {{ t.role || 'Học viên' }} <span v-if="t.company">• {{ t.company }}</span>
                </small>
              </td>
              <td>
                <span v-if="t.course_name" class="badge" style="background: rgba(2, 43, 159, 0.08); color: #022b9f; font-weight: 700;">
                  {{ t.course_name }}
                </span>
                <span v-else class="text-muted" style="font-size: 12px;">(Tất cả)</span>
              </td>
              <td>
                <div style="max-width: 280px; text-overflow: ellipsis; overflow: hidden; white-space: nowrap; font-size: 13.5px; color: #334155;">
                  "{{ t.quote || t.text || '...' }}"
                </div>
                <div style="color: #f59e0b; font-size: 12px; margin-top: 2px;">
                  {{ '★'.repeat(t.rating || 5) }}
                </div>
              </td>
              <td>
                <div class="action-buttons">
                  <button @click="editTestimonial(t)" class="btn-action edit" title="Sửa đánh giá">✏️</button>
                  <button @click="deleteItem(t.id)" class="btn-action delete" title="Xóa đánh giá">🗑️</button>
                </div>
              </td>
            </tr>
            <tr v-if="filteredTestimonials.length === 0">
              <td colspan="7" class="text-center py-8 text-muted">
                Không tìm thấy cảm nhận nào phù hợp.
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination Component -->
      <Pagination 
        v-if="filteredTestimonials.length > pageSize"
        v-model:currentPage="currentPage"
        :totalItems="filteredTestimonials.length"
        :pageSize="pageSize"
      />
    </div>

    <!-- VIEW 2: FORM ADD/EDIT -->
    <div v-else-if="activeView === 'form'" class="admin-page-card" style="background: #ffffff; color: #0f172a; border-radius: 16px; padding: 28px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); border: 1px solid #e2e8f0;">
      <div class="flex-between pb-4 mb-4" style="border-bottom: 1px solid #e2e8f0;">
        <div style="display: flex; align-items: center; gap: 12px;">
          <button type="button" @click="activeView = 'list'" class="btn btn-secondary btn-sm" style="padding: 8px 16px; font-weight: 600;">
            ← Quay lại danh sách
          </button>
          <h3 style="margin: 0; color: #0f172a; font-size: 20px; font-weight: 800;">
            {{ isEditing ? 'Chỉnh sửa Cảm nhận học viên' : 'Thêm Cảm nhận & Feedback mới' }}
          </h3>
        </div>
        <button type="button" @click="activeView = 'list'" class="btn btn-secondary btn-sm">Hủy</button>
      </div>

      <form @submit.prevent="saveTestimonial" class="mt-2">
        <!-- Select Testimonial Type -->
        <div class="form-group">
          <label style="color: #1e293b; font-weight: 700;">Phân loại Feedback học viên</label>
          <div style="display: flex; gap: 16px; margin-top: 6px;">
            <label style="display: flex; align-items: center; gap: 6px; cursor: pointer; font-weight: 600;">
              <input type="radio" v-model="form.testimonialType" value="video" /> Video Feedback YouTube
            </label>
            <label style="display: flex; align-items: center; gap: 6px; cursor: pointer; font-weight: 600;">
              <input type="radio" v-model="form.testimonialType" value="photo" /> Hình ảnh & Feedback
            </label>
            <label style="display: flex; align-items: center; gap: 6px; cursor: pointer; font-weight: 600;">
              <input type="radio" v-model="form.testimonialType" value="text" /> Trích dẫn ngắn
            </label>
          </div>
        </div>

        <!-- Student Basic Info -->
        <div class="grid grid-2 gap-4 mt-4">
          <div class="form-group">
            <label style="color: #1e293b; font-weight: 600;">Họ và Tên Học viên <span style="color: #e11d48;">*</span></label>
            <input v-model="form.name" type="text" required class="admin-input-style" placeholder="Ví dụ: Nguyễn Văn Hoàng" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
          </div>

          <div class="form-group">
            <label style="color: #1e293b; font-weight: 600;">Chức danh / Vị trí</label>
            <input v-model="form.role" type="text" class="admin-input-style" placeholder="Ví dụ: Founder & CEO / Giám đốc Vận hành" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
          </div>
        </div>

        <div class="grid grid-2 gap-4 mt-4">
          <div class="form-group">
            <label style="color: #1e293b; font-weight: 600;">Công ty / Tổ chức</label>
            <input v-model="form.company" type="text" class="admin-input-style" placeholder="Ví dụ: VNG Corporation / TechVision Group" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
          </div>

          <div class="form-group">
            <label style="color: #1e293b; font-weight: 600;">Tên Khóa học tham gia</label>
            <input v-model="form.courseName" type="text" class="admin-input-style" placeholder="Ví dụ: Khóa học Generative AI trong Quản trị" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
          </div>
        </div>

        <!-- Dynamic Fields for VIDEO TYPE -->
        <div v-if="form.testimonialType === 'video'" class="mt-4 p-4" style="background: #fff1f2; border: 1px solid #fecdd3; border-radius: 12px;">
          <h4 style="margin: 0 0 12px 0; color: #be123c; font-size: 15px; font-weight: 800;">Cấu hình YouTube Video</h4>
          
          <div class="form-group">
            <label style="color: #9f1239; font-weight: 600;">Đường dẫn Video YouTube hoặc YouTube Video ID</label>
            <input 
              v-model="youtubeInput" 
              @input="onYoutubeInputChange"
              type="text" 
              class="admin-input-style" 
              placeholder="Dán link YouTube (ví dụ: https://www.youtube.com/watch?v=BC9rvc1F3dA hoặc BC9rvc1F3dA)" 
              style="background: #ffffff; color: #0f172a; border: 1px solid #fda4af;" 
            />
            <small style="color: #e11d48; display: block; margin-top: 4px;">
              Hệ thống sẽ tự động tách ID ({{ form.youtubeId || 'Chưa có' }}) và tự tạo Thumbnail YouTube chuẩn.
            </small>
          </div>

          <div class="grid grid-2 gap-4 mt-3">
            <div class="form-group">
              <label style="color: #9f1239; font-weight: 600;">Link Thumbnail Ảnh bìa Video</label>
              <div style="display: flex; gap: 8px;">
                <input v-model="form.thumbnail" type="text" class="admin-input-style" placeholder="https://img.youtube.com/vi/..." style="flex: 1; background: #ffffff; color: #0f172a; border: 1px solid #fda4af;" />
                <input type="file" ref="thumbFileRef" @change="onFileSelectForCrop($event, (url) => { form.thumbnail = url; }, 'wide', '✂ Cắt Thumbnail Video (16:9)')" style="display: none;" accept="image/*" />
                <button type="button" @click="$refs.thumbFileRef.click()" class="btn btn-secondary btn-sm">Upload</button>
              </div>
              <div v-if="form.thumbnail" style="display: flex; align-items: center; gap: 12px; margin-top: 8px;">
                <img :src="formatImageUrl(form.thumbnail)" alt="Preview Thumbnail" style="width: 120px; height: 68px; object-fit: cover; border-radius: 8px; border: 1px solid #cbd5e1;" referrerpolicy="no-referrer" />
                <button type="button" class="btn btn-sm btn-secondary" style="font-size: 12px; font-weight: 600; color: #e11d48; border-color: #fda4af;" @click="openCropper(form.thumbnail, (url) => { form.thumbnail = url; }, 'wide', '✂ Cắt Thumbnail Video (16:9)')">✂ Cắt lại ảnh</button>
              </div>
            </div>

            <div class="form-group">
              <label style="color: #9f1239; font-weight: 600;">Tựa đề / Tiêu đề Video Feedback</label>
              <textarea v-model="form.text" rows="3" class="admin-input-style" placeholder="Ví dụ: Chia sẻ từ Học viên về tính thực chiến của khóa học AI" style="background: #ffffff; color: #0f172a; border: 1px solid #fda4af;"></textarea>
            </div>
          </div>
        </div>

        <!-- Dynamic Fields for PHOTO or TEXT TYPE -->
        <div v-else class="mt-4 p-4" style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px;">
          <h4 style="margin: 0 0 12px 0; color: #022b9f; font-size: 15px; font-weight: 800;">Cấu hình Ảnh & Trích dẫn</h4>

          <div class="form-group" v-if="form.testimonialType === 'photo'">
            <label style="color: #1e293b; font-weight: 600;">Link Hình Ảnh Feedback Học viên</label>
            <div style="display: flex; gap: 8px;">
              <input v-model="form.image" type="text" class="admin-input-style" placeholder="https://... hoặc /images/..." style="flex: 1; background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
              <input type="file" ref="photoFileRef" @change="onFileSelectForCrop($event, (url) => { form.image = url; }, 'square', '✂ Cắt Ảnh Đại Diện Học Viên (1:1)')" style="display: none;" accept="image/*" />
              <button type="button" @click="$refs.photoFileRef.click()" class="btn btn-secondary btn-sm">Upload</button>
            </div>
            <div v-if="form.image" style="display: flex; align-items: center; gap: 12px; margin-top: 8px;">
              <img :src="formatImageUrl(form.image)" alt="Preview Photo" style="max-height: 80px; object-fit: cover; border-radius: 8px; border: 1px solid #cbd5e1;" referrerpolicy="no-referrer" />
              <button type="button" class="btn btn-sm btn-secondary" style="font-size: 12px; font-weight: 600; color: #0284c7; border-color: #bae6fd;" @click="openCropper(form.image, (url) => { form.image = url; }, 'square', '✂ Cắt Ảnh Đại Diện Học Viên (1:1)')">✂ Cắt lại ảnh</button>
            </div>
          </div>

          <div class="form-group mt-3">
            <label style="color: #1e293b; font-weight: 600;">Nội dung Cảm nhận / Trích dẫn chi tiết <span style="color: #e11d48;">*</span></label>
            <textarea v-model="form.quote" rows="4" required class="admin-input-style" placeholder="Viết cảm nhận thực tế của học viên..." style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;"></textarea>
          </div>
        </div>

        <!-- Rating Rating -->
        <div class="form-group mt-4">
          <label style="color: #1e293b; font-weight: 600;">Số sao Đánh giá (Rating)</label>
          <select v-model.number="form.rating" class="admin-input-style" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1; width: 160px;">
            <option :value="5">⭐⭐⭐⭐⭐ (5 sao - Xuất sắc)</option>
            <option :value="4">⭐⭐⭐⭐ (4 sao - Tốt)</option>
            <option :value="3">⭐⭐⭐ (3 sao - Khá)</option>
          </select>
        </div>

        <!-- Form Submit Actions -->
        <div class="mt-6 flex-end" style="gap: 12px; border-top: 1px solid #e2e8f0; padding-top: 20px;">
          <button type="button" @click="activeView = 'list'" class="btn btn-secondary">Hủy</button>
          <button type="submit" class="btn btn-primary" :disabled="saving">
            {{ saving ? 'Đang lưu...' : (isEditing ? 'Cập nhật Cảm nhận' : 'Thêm Cảm nhận') }}
          </button>
        </div>
      </form>
    </div>
    <!-- Image Cropper Modal -->
    <ImageCropperModal :isOpen="isCropperOpen" :imageUrl="cropTargetUrl" :aspectRatio="cropAspectRatio" :title="cropModalTitle" @close="isCropperOpen = false" @cropped="handleCroppedImage" />
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useCourseStore } from '@/stores/courses';
import Pagination from '@/components/Pagination.vue';
import { formatImageUrl } from '@/utils/imageHelper';
import ImageCropperModal from '@/components/ImageCropperModal.vue';

const courseStore = useCourseStore();

// Cropper States
const isCropperOpen = ref(false);
const cropTargetUrl = ref('');
const cropAspectRatio = ref('wide');
const cropModalTitle = ref('✂ Cắt Ảnh Testimonial');
let cropTargetCallback = null;

const openCropper = (url, callback, ratio = 'wide', title = '✂ Cắt Ảnh Testimonial') => {
  if (!url) return;
  cropTargetUrl.value = url;
  cropAspectRatio.value = ratio;
  cropModalTitle.value = title;
  cropTargetCallback = callback;
  isCropperOpen.value = true;
};

const onFileSelectForCrop = (event, callback, ratio = 'wide', title = '✂ Cắt Ảnh Testimonial') => {
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


const activeView = ref('list');
const filterType = ref('all');
const searchQuery = ref('');
const currentPage = ref(1);
const pageSize = ref(10);
const isEditing = ref(false);
const editingId = ref(null);
const saving = ref(false);
const youtubeInput = ref('');

const form = ref({
  name: '',
  role: '',
  company: '',
  text: '',
  quote: '',
  courseName: '',
  testimonialType: 'video',
  youtubeId: '',
  thumbnail: '',
  videoUrl: '',
  image: '',
  rating: 5
});

const testimonials = computed(() => courseStore.adminTestimonials || []);

const videoCount = computed(() => testimonials.value.filter(t => t.testimonial_type === 'video').length);
const photoCount = computed(() => testimonials.value.filter(t => t.testimonial_type === 'photo' || t.testimonial_type === 'text').length);

const filteredTestimonials = computed(() => {
  return testimonials.value.filter(t => {
    // Type Filter
    if (filterType.value === 'video' && t.testimonial_type !== 'video') return false;
    if (filterType.value === 'photo' && t.testimonial_type !== 'photo' && t.testimonial_type !== 'text') return false;

    // Search Query
    if (searchQuery.value.trim()) {
      const q = searchQuery.value.toLowerCase().trim();
      const matchName = t.name && t.name.toLowerCase().includes(q);
      const matchRole = t.role && t.role.toLowerCase().includes(q);
      const matchCompany = t.company && t.company.toLowerCase().includes(q);
      const matchCourse = t.course_name && t.course_name.toLowerCase().includes(q);
      return matchName || matchRole || matchCompany || matchCourse;
    }
    return true;
  });
});

const paginatedTestimonials = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  return filteredTestimonials.value.slice(start, start + pageSize.value);
});

watch([filterType, searchQuery], () => {
  currentPage.value = 1;
});

onMounted(async () => {
  try {
    await courseStore.fetchAdminTestimonials();
  } catch (err) {
    console.error("Error loading admin testimonials:", err);
  }
});

const extractYoutubeId = (url) => {
  if (!url) return '';
  if (url.length === 11 && !url.includes('/') && !url.includes('.')) {
    return url;
  }
  const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
  const match = url.match(regExp);
  return (match && match[2].length === 11) ? match[2] : '';
};

const onYoutubeInputChange = () => {
  const yid = extractYoutubeId(youtubeInput.value);
  if (yid) {
    form.value.youtubeId = yid;
    form.value.thumbnail = `https://img.youtube.com/vi/${yid}/hqdefault.jpg`;
    form.value.videoUrl = `https://www.youtube.com/embed/${yid}?autoplay=1`;
  }
};

const openAddModal = () => {
  isEditing.value = false;
  editingId.value = null;
  youtubeInput.value = '';
  form.value = {
    name: '',
    role: '',
    company: '',
    text: '',
    quote: '',
    courseName: '',
    testimonialType: 'video',
    youtubeId: '',
    thumbnail: '',
    videoUrl: '',
    image: '',
    rating: 5
  };
  activeView.value = 'form';
};

const editTestimonial = (t) => {
  isEditing.value = true;
  editingId.value = t.id;
  youtubeInput.value = t.youtube_id || t.video_url || '';
  form.value = {
    name: t.name || '',
    role: t.role || '',
    company: t.company || '',
    text: t.text || '',
    quote: t.quote || t.text || '',
    courseName: t.course_name || '',
    testimonialType: t.testimonial_type || 'text',
    youtubeId: t.youtube_id || '',
    thumbnail: t.thumbnail || '',
    videoUrl: t.video_url || '',
    image: t.image || '',
    rating: t.rating || 5
  };
  activeView.value = 'form';
};

const uploadImage = async (event, targetField) => {
  const file = event.target.files[0];
  if (!file) return;

  try {
    const url = await courseStore.uploadImage(file);
    form.value[targetField] = url;
    courseStore.showToast('Tải ảnh lên thành công!', 'success');
  } catch (err) {
    courseStore.showToast('Không thể upload ảnh: ' + err.message, 'error');
  }
};

const saveTestimonial = async () => {
  if (!form.value.name) {
    courseStore.showToast('Vui lòng nhập tên học viên', 'error');
    return;
  }

  if (form.value.testimonialType === 'video' && !form.value.youtubeId) {
    const yid = extractYoutubeId(youtubeInput.value);
    if (yid) {
      form.value.youtubeId = yid;
      form.value.thumbnail = form.value.thumbnail || `https://img.youtube.com/vi/${yid}/hqdefault.jpg`;
      form.value.videoUrl = form.value.videoUrl || `https://www.youtube.com/embed/${yid}?autoplay=1`;
    }
  }

  saving.value = true;
  try {
    const payload = {
      ...form.value,
      thumbnail: formatImageUrl(form.value.thumbnail),
      image: formatImageUrl(form.value.image)
    };
    if (isEditing.value) {
      await courseStore.updateAdminTestimonial(editingId.value, payload);
    } else {
      await courseStore.addAdminTestimonial(payload);
    }
    activeView.value = 'list';
  } catch (err) {
    console.error("Save testimonial error:", err);
  } finally {
    saving.value = false;
  }
};

const deleteItem = async (id) => {
  const isConfirmed = await courseStore.showConfirm({
    title: 'Xác nhận xóa Cảm nhận',
    message: 'Bạn có chắc chắn muốn xóa phản hồi/video feedback của học viên này?',
    confirmText: 'Đồng ý xóa',
    cancelText: 'Hủy bỏ',
    type: 'danger'
  });

  if (isConfirmed) {
    try {
      await courseStore.deleteAdminTestimonial(id);
    } catch (err) {
      console.error("Delete testimonial error:", err);
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
