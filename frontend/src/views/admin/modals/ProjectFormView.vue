<template>
  <div class="admin-page-card" style="background: #ffffff; color: #0f172a; border-radius: 16px; padding: 28px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); border: 1px solid #e2e8f0;">
    <div class="flex-between pb-4 mb-4" style="border-bottom: 1px solid #e2e8f0;">
      <div style="display: flex; align-items: center; gap: 12px;">
        <button type="button" @click="$emit('cancel')" class="btn btn-secondary btn-sm" style="padding: 8px 16px; font-weight: 600;">
          ← Quay lại danh sách
        </button>
        <h3 style="margin: 0; color: #0f172a; font-size: 20px; font-weight: 800;">
          {{ isEditing ? 'Chỉnh sửa Dự án / Case Study' : 'Thêm Dự án / Case Study mới' }}
        </h3>
      </div>
      <button type="button" @click="$emit('cancel')" class="btn btn-secondary btn-sm">Hủy</button>
    </div>

    <form @submit.prevent="saveProject" class="mt-2">
      <div class="grid grid-2 gap-4">
        <div class="form-group">
          <label style="color: #1e293b; font-weight: 600;">Mã định danh Slug (ID) <span style="color: #e11d48;">*</span></label>
          <input 
            v-model="form.id" 
            :disabled="isEditing" 
            type="text" 
            required 
            class="admin-input-style" 
            placeholder="dao-tao-ai-acb" 
            style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" 
          />
          <small class="text-muted" style="display: block; margin-top: 2px;">Chuỗi không dấu dùng làm đường dẫn URL xem chi tiết dự án.</small>
        </div>

        <div class="form-group">
          <label style="color: #1e293b; font-weight: 600;">Chuyên mục Dự án <span style="color: #e11d48;">*</span></label>
          <select v-model="form.category" @change="onCategoryChange" class="admin-input-style" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;">
            <option value="du-an-doanh-nghiep">Dự án Doanh nghiệp</option>
            <option value="du-an-ca-nhan">Dự án Cá nhân</option>
            <option value="du-an-nha-nuoc">Dự án Khối Cơ quan - Nhà nước</option>
          </select>
        </div>
      </div>

      <div class="form-group mt-4">
        <label style="color: #1e293b; font-weight: 600;">Tên / Tiêu đề Dự án <span style="color: #e11d48;">*</span></label>
        <input 
          v-model="form.title" 
          @input="generateSlug" 
          type="text" 
          required 
          class="admin-input-style" 
          placeholder="Ví dụ: Đào tạo ứng dụng Generative AI cho 150+ nhân sự quản lý Tập đoàn ACB" 
          style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" 
        />
      </div>

      <div class="grid grid-2 gap-4 mt-4">
        <div class="form-group">
          <label style="color: #1e293b; font-weight: 600;">Tên Khách hàng / Tác giả</label>
          <input v-model="form.client" type="text" class="admin-input-style" placeholder="Ví dụ: Tập đoàn Tài chính ACB / Bosch Việt Nam" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
        </div>

        <div class="form-group">
          <label style="color: #1e293b; font-weight: 600;">Thời gian thực hiện</label>
          <input v-model="form.date" type="text" class="admin-input-style" placeholder="Ví dụ: 15/08/2026 hoặc Tháng 09/2026" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
        </div>
      </div>

      <div class="grid grid-2 gap-4 mt-4">
        <div class="form-group">
          <label style="color: #1e293b; font-weight: 600;">Ảnh đại diện Dự án (Thumbnail URL)</label>
          <div style="display: flex; gap: 8px;">
            <input v-model="form.image" type="text" class="admin-input-style" placeholder="https://... hoặc URL ảnh" style="flex: 1; background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
            <input type="file" ref="imageFileRef" @change="onFileSelectForCrop($event, (url) => { form.image = url; }, 'wide', '✂ Cắt Ảnh Đại Diện Dự Án (16:9)')" style="display: none;" accept="image/*" />
            <button type="button" @click="$refs.imageFileRef.click()" class="btn btn-secondary btn-sm">Upload</button>
          </div>
          <div v-if="form.image" style="display: flex; align-items: center; gap: 12px; margin-top: 8px;">
            <img :src="form.image" alt="Preview Image" style="max-height: 80px; object-fit: cover; border-radius: 8px; border: 1px solid #cbd5e1;" referrerpolicy="no-referrer" />
            <button type="button" class="btn btn-sm btn-secondary" style="font-size: 12px; font-weight: 600; color: #0284c7; border-color: #bae6fd;" @click="openCropper(form.image, (url) => { form.image = url; }, 'wide', '✂ Cắt Ảnh Đại Diện Dự Án (16:9)')">✂ Cắt lại ảnh</button>
          </div>
        </div>

        <div class="form-group">
          <label style="color: #1e293b; font-weight: 600;">Link Hồ sơ năng lực / Google Drive Profile</label>
          <input v-model="form.driveProfile" type="text" class="admin-input-style" placeholder="https://drive.google.com/file/d/..." style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
        </div>
      </div>

      <div class="form-group mt-4">
        <label style="color: #1e293b; font-weight: 600;">Mô tả / Tóm tắt ngắn Dự án</label>
        <textarea v-model="form.summary" rows="3" class="admin-input-style" placeholder="Nêu vắn tắt mục tiêu và kết quả cốt lõi của dự án..." style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;"></textarea>
      </div>

      <!-- Detailed Content Editor (Rich Text vs Blocks) -->
      <div class="mt-6 p-4" style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px;">
        <div class="flex-between mb-3" style="flex-wrap: wrap; gap: 10px;">
          <h4 style="margin: 0; color: #022b9f; font-size: 16px; font-weight: 800;">Nội dung chi tiết Bài viết Case Study</h4>
          
          <div style="display: flex; gap: 8px;">
            <button 
              type="button" 
              @click="editorMode = 'rich'" 
              class="btn btn-sm" 
              :class="editorMode === 'rich' ? 'btn-primary' : 'btn-secondary'"
            >
              Trình soạn thảo văn bản
            </button>
            <button 
              type="button" 
              @click="editorMode = 'blocks'" 
              class="btn btn-sm" 
              :class="editorMode === 'blocks' ? 'btn-primary' : 'btn-secondary'"
            >
              Dạng Khối Cấu trúc
            </button>
          </div>
        </div>

        <!-- Mode 1: WYSIWYG Rich Text Editor -->
        <div v-if="editorMode === 'rich'" class="mt-2">
          <RichTextEditor 
            v-model="richHtmlContent" 
            placeholder="Soạn thảo bài viết dự án trực quan (In đậm, In nghiêng, H2, H3, Danh sách, Link...)..." 
          />
        </div>

        <!-- Mode 2: Content Blocks Builder -->
        <div v-else-if="editorMode === 'blocks'" class="mt-2">
          <div class="flex-between mb-2">
            <span style="font-size: 13px; font-weight: 600; color: #475569;">Quản lý các khối văn bản chuẩn:</span>
            <button type="button" @click="addContentBlock('paragraph')" class="btn btn-secondary btn-sm">+ Thêm Khối văn bản mới</button>
          </div>

          <div v-for="(block, bIdx) in contentBlocks" :key="bIdx" class="mb-3 p-3" style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px;">
            <div class="flex-between mb-2">
              <div style="display: flex; gap: 8px; align-items: center;">
                <select v-model="block.type" class="admin-input-style" style="width: 150px; padding: 4px 8px; font-size: 13px;">
                  <option value="paragraph">Đoạn văn (Paragraph)</option>
                  <option value="heading">Tiêu đề phụ (Heading)</option>
                  <option value="bullets">Danh sách chấm tròn (Bullets)</option>
                </select>
                <span class="font-bold text-muted" style="font-size: 12px;">Khối {{ bIdx + 1 }}</span>
              </div>
              <button type="button" @click="removeContentBlock(bIdx)" class="btn btn-sm" style="padding: 2px 6px; font-size: 12px; background: #fee2e2; color: #b91c1c;" title="Xóa khối">Xóa</button>
            </div>

            <div v-if="block.type === 'bullets'">
              <label style="font-size: 12px; font-weight: 600; color: #475569;">Các ý chấm tròn (Mỗi ý 1 dòng):</label>
              <textarea v-model="block.bulletText" rows="3" class="admin-input-style" placeholder="Ý 1&#10;Ý 2&#10;Ý 3" style="font-size: 13.5px;"></textarea>
            </div>
            <div v-else>
              <textarea v-model="block.text" rows="2" class="admin-input-style" placeholder="Nhập nội dung văn bản..." style="font-size: 13.5px;"></textarea>
            </div>
          </div>

          <div v-if="contentBlocks.length === 0" class="text-center py-4 text-muted" style="font-size: 13px;">
            Chưa có khối nội dung nào. Nhấn "+ Thêm Khối văn bản mới" để bổ sung chi tiết bài viết.
          </div>
        </div>
      </div>

      <!-- Form Submit Actions -->
      <div class="mt-6 flex-end" style="gap: 12px; border-top: 1px solid #e2e8f0; padding-top: 20px;">
        <button type="button" @click="$emit('cancel')" class="btn btn-secondary">Hủy</button>
        <button type="submit" class="btn btn-primary" :disabled="saving">
          {{ saving ? 'Đang lưu...' : (isEditing ? 'Cập nhật Dự án' : 'Tạo Dự án') }}
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
import RichTextEditor from '@/components/RichTextEditor.vue';
import ImageCropperModal from '@/components/ImageCropperModal.vue';

const props = defineProps({
  initialData: {
    type: Object,
    default: null
  }
});

const emit = defineEmits(['cancel', 'saved']);

const courseStore = useCourseStore();
const isEditing = computed(() => !!(props.initialData && props.initialData.id));

const saving = ref(false);
const editorMode = ref('rich');
const richHtmlContent = ref('');
const contentBlocks = ref([]);
const imageFileRef = ref(null);

// Cropper States
const isCropperOpen = ref(false);
const cropTargetUrl = ref('');
const cropAspectRatio = ref('wide');
const cropModalTitle = ref('✂ Cắt Ảnh Dự Án');
let cropTargetCallback = null;

const form = ref({
  id: '',
  title: '',
  category: 'du-an-doanh-nghiep',
  categoryName: 'Dự án Doanh nghiệp',
  summary: '',
  image: '',
  date: '',
  client: '',
  driveProfile: ''
});

onMounted(() => {
  if (props.initialData) {
    const p = props.initialData;
    form.value = {
      id: p.id,
      title: p.title || '',
      category: p.category || 'du-an-doanh-nghiep',
      categoryName: p.category_name || 'Dự án Doanh nghiệp',
      summary: p.summary || '',
      image: p.image || '',
      date: p.date || '',
      client: p.client || '',
      driveProfile: p.drive_profile || ''
    };

    let rawContent = p.content;
    let parsedBlocks = [];
    let isHtmlString = false;

    if (typeof rawContent === 'string') {
      try {
        const parsed = JSON.parse(rawContent);
        if (Array.isArray(parsed)) {
          parsedBlocks = parsed;
        } else {
          isHtmlString = true;
        }
      } catch (err) {
        isHtmlString = true;
      }
    } else if (Array.isArray(rawContent)) {
      parsedBlocks = rawContent;
    }

    if (isHtmlString) {
      editorMode.value = 'rich';
      richHtmlContent.value = rawContent || '';
    } else {
      editorMode.value = 'rich';
      let htmlResult = '';
      parsedBlocks.forEach(b => {
        if (b.type === 'heading') htmlResult += `<h2>${b.text || ''}</h2>`;
        else if (b.type === 'paragraph') htmlResult += `<p>${b.text || ''}</p>`;
        else if (b.type === 'bullets' && Array.isArray(b.items)) {
          htmlResult += `<ul>${b.items.map(i => `<li>${i}</li>`).join('')}</ul>`;
        } else if (b.type === 'html') {
          htmlResult += b.text || '';
        }
      });
      richHtmlContent.value = htmlResult;

      contentBlocks.value = parsedBlocks.map(b => ({
        type: b.type || 'paragraph',
        text: b.text || '',
        bulletText: Array.isArray(b.items) ? b.items.join('\n') : (b.text || '')
      }));
    }
  } else {
    editorMode.value = 'rich';
    richHtmlContent.value = '';
    form.value = {
      id: '',
      title: '',
      category: 'du-an-doanh-nghiep',
      categoryName: 'Dự án Doanh nghiệp',
      summary: '',
      image: '',
      date: '',
      client: '',
      driveProfile: ''
    };
    contentBlocks.value = [{ type: 'paragraph', text: '' }];
  }
});

const onCategoryChange = () => {
  if (form.value.category === 'du-an-doanh-nghiep') form.value.categoryName = 'Dự án Doanh nghiệp';
  else if (form.value.category === 'du-an-ca-nhan') form.value.categoryName = 'Dự án Cá nhân';
  else if (form.value.category === 'du-an-nha-nuoc') form.value.categoryName = 'Dự án Khối Cơ quan - Nhà nước';
};

const generateSlug = () => {
  if (isEditing.value) return;
  if (!form.value.title) {
    form.value.id = '';
    return;
  }
  let slug = form.value.title.toLowerCase();
  slug = slug.replace(/á|à|ả|ã|ạ|ă|ắ|ằ|ẳ|ẵ|ặ|â|ấ|ầ|ẩ|ẫ|ậ/g, 'a');
  slug = slug.replace(/é|è|ẻ|ẽ|ẹ|ê|ế|ề|ể|ễ|ệ/g, 'e');
  slug = slug.replace(/i|í|ì|ỉ|ĩ|ị/g, 'i');
  slug = slug.replace(/ó|ò|ỏ|õ|ọ|ô|ố|ồ|ổ|ỗ|ộ|ơ|ớ|ờ|ở|ỡ|ợ/g, 'o');
  slug = slug.replace(/ú|ù|ủ|ũ|ụ|ư|ứ|ừ|ử|ữ|ự/g, 'u');
  slug = slug.replace(/ý|ỳ|ỷ|ỹ|ỵ/g, 'y');
  slug = slug.replace(/đ/g, 'd');
  slug = slug.replace(/[^a-z0-9\s-]/g, '');
  slug = slug.replace(/\s+/g, '-').replace(/-+/g, '-');
  form.value.id = slug.substring(0, 60);
};

const addContentBlock = (type = 'paragraph') => {
  contentBlocks.value.push({ type, text: '', bulletText: '' });
};

const removeContentBlock = (idx) => {
  contentBlocks.value.splice(idx, 1);
};

const openCropper = (url, callback, ratio = 'wide', title = '✂ Cắt Ảnh Dự Án (16:9)') => {
  if (!url) return;
  cropTargetUrl.value = url;
  cropAspectRatio.value = ratio;
  cropModalTitle.value = title;
  cropTargetCallback = callback;
  isCropperOpen.value = true;
};

const onFileSelectForCrop = (event, callback, ratio = 'wide', title = '✂ Cắt Ảnh Dự Án (16:9)') => {
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

const saveProject = async () => {
  if (!form.value.id || !form.value.title) {
    courseStore.showToast('Vui lòng nhập ID và Tiêu đề dự án', 'error');
    return;
  }

  let finalContent;
  if (editorMode.value === 'rich') {
    finalContent = richHtmlContent.value || '';
  } else {
    finalContent = contentBlocks.value.map(b => {
      if (b.type === 'bullets') {
        const items = (b.bulletText || '').split('\n').map(s => s.trim()).filter(Boolean);
        return { type: 'bullets', items };
      }
      return { type: b.type || 'paragraph', text: b.text || '' };
    });
  }

  const payload = {
    ...form.value,
    content: finalContent
  };

  saving.value = true;
  try {
    if (isEditing.value) {
      await courseStore.updateAdminProject(form.value.id, payload);
    } else {
      await courseStore.addAdminProject(payload);
    }
    emit('saved');
  } catch (err) {
    console.error("Save project error:", err);
  } finally {
    saving.value = false;
  }
};
</script>

