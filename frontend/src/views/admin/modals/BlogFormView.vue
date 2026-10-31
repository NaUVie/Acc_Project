<template>
  <div class="admin-page-card" style="background: #ffffff; color: #0f172a; border-radius: 16px; padding: 28px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); border: 1px solid #e2e8f0;">
    <div class="flex-between pb-4 mb-4" style="border-bottom: 1px solid #e2e8f0;">
      <div style="display: flex; align-items: center; gap: 12px;">
        <button type="button" @click="$emit('cancel')" class="btn btn-secondary btn-sm" style="padding: 8px 16px; font-weight: 600;">
          ← Quay lại danh sách
        </button>
        <h3 style="margin: 0; color: #0f172a; font-size: 20px; font-weight: 800;">
          {{ isEditing ? 'Chỉnh sửa Tin tức / Bài viết' : 'Thêm Tin tức / Bài viết mới' }}
        </h3>
      </div>
      <button type="button" @click="$emit('cancel')" class="btn btn-secondary btn-sm">Hủy</button>
    </div>

    <form @submit.prevent="saveBlog" class="mt-2">
      <div class="form-group mb-4">
        <label style="color: #1e293b; font-weight: 600;">Tiêu đề Bài viết <span style="color: #e11d48;">*</span></label>
        <input 
          v-model="form.title" 
          @input="generateSlug" 
          type="text" 
          required 
          class="admin-input-style" 
          placeholder="Ví dụ: Top 10 Công cụ AI hỗ trợ tự động hóa doanh nghiệp năm 2026" 
          style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" 
        />
      </div>

      <div class="grid grid-2 gap-4">
        <div class="form-group">
          <label style="color: #1e293b; font-weight: 600;">Đường dẫn tĩnh Slug (Handle) <span style="color: #e11d48;">*</span></label>
          <input 
            v-model="form.handle" 
            type="text" 
            required 
            class="admin-input-style" 
            placeholder="top-10-cong-cu-ai-2026" 
            style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" 
          />
          <small class="text-muted" style="display: block; margin-top: 2px;">Dùng làm URL bài viết, ví dụ: /blog/top-10-cong-cu-ai-2026</small>
        </div>

        <div class="form-group">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
            <label style="color: #1e293b; font-weight: 600; margin: 0;">Chuyên mục Bài viết <span style="color: #e11d48;">*</span></label>
            <button 
              type="button" 
              @click="$emit('open-category-modal')" 
              style="font-size: 12px; color: #0284c7; background: none; border: none; cursor: pointer; font-weight: 600; padding: 0; text-decoration: underline;"
            >
              ⚙️ Quản lý Chuyên mục
            </button>
          </div>
          <div style="display: flex; gap: 8px;">
            <select 
              v-model="form.category" 
              class="admin-input-style" 
              required
              style="flex: 1; background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;"
            >
              <option value="" disabled>-- Chọn chuyên mục bài viết --</option>
              <option v-for="cat in availableCategories" :key="cat.id || cat.name" :value="cat.name">
                {{ cat.name }}
              </option>
            </select>
            <button 
              type="button" 
              class="btn btn-secondary btn-sm" 
              @click="showQuickAddCat = !showQuickAddCat"
              title="Tạo nhanh một chuyên mục mới ngay tại đây"
              style="white-space: nowrap; font-weight: 600;"
            >
              {{ showQuickAddCat ? 'Đóng' : '+ Thêm mới' }}
            </button>
          </div>

          <!-- Quick Add Category inline box -->
          <div v-if="showQuickAddCat" class="quick-add-cat-box mt-2" style="display: flex; gap: 8px; background: #f0fdf4; padding: 10px; border-radius: 8px; border: 1px solid #bbf7d0; align-items: center;">
            <input 
              v-model="quickCatName" 
              type="text" 
              placeholder="Nhập tên chuyên mục mới (VD: Case Study AI)..." 
              class="admin-input-style"
              style="flex: 1; background: #ffffff; border: 1px solid #86efac; font-size: 13px; padding: 8px 12px;"
              @keydown.enter.prevent="handleQuickAddCategory"
            />
            <button 
              type="button" 
              @click="handleQuickAddCategory" 
              class="btn btn-primary btn-sm"
              :disabled="!quickCatName.trim() || isSubmittingCat"
            >
              {{ isSubmittingCat ? 'Đang tạo...' : 'Tạo & Chọn' }}
            </button>
            <button 
              type="button" 
              @click="showQuickAddCat = false; quickCatName = ''" 
              class="btn btn-secondary btn-sm"
            >
              Hủy
            </button>
          </div>
        </div>
      </div>

      <div class="grid grid-2 gap-4 mt-4">
        <div class="form-group">
          <label style="color: #1e293b; font-weight: 600;">Ngày hiển thị (Hiển thị công khai)</label>
          <input v-model="form.date" type="text" class="admin-input-style" placeholder="Ví dụ: 15/08/2026" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
        </div>

        <div class="form-group">
          <label style="color: #1e293b; font-weight: 600;">Link liên kết ngoài (Tùy chọn)</label>
          <input v-model="form.link" type="text" class="admin-input-style" placeholder="/blog/... hoặc URL ngoài" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
        </div>
      </div>

      <div class="form-group mt-4">
        <label style="color: #1e293b; font-weight: 600;">Ảnh đại diện Bài viết (Thumbnail URL)</label>
        <div style="display: flex; gap: 8px;">
          <input v-model="form.image" type="text" class="admin-input-style" placeholder="https://... hoặc URL ảnh" style="flex: 1; background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
          <input type="file" ref="imageFileRef" @change="onFileSelectForCrop($event, (url) => { form.image = url; }, 'wide', '✂ Cắt Thumbnail Bài Viết (16:9)')" style="display: none;" accept="image/*" />
          <button type="button" @click="$refs.imageFileRef.click()" class="btn btn-secondary btn-sm" :disabled="uploadingImage">
            {{ uploadingImage ? 'Đang tải...' : 'Upload' }}
          </button>
        </div>
        <div v-if="form.image" style="display: flex; align-items: center; gap: 12px; margin-top: 8px;">
          <img :src="form.image" alt="Preview Image" style="max-height: 80px; object-fit: cover; border-radius: 8px; border: 1px solid #cbd5e1;" referrerpolicy="no-referrer" />
          <button type="button" class="btn btn-sm btn-secondary" style="font-size: 12px; font-weight: 600; color: #0284c7; border-color: #bae6fd;" @click="openCropper(form.image, (url) => { form.image = url; }, 'wide', '✂ Cắt Thumbnail Bài Viết (16:9)')">✂ Cắt lại ảnh</button>
        </div>
      </div>

      <div class="form-group mt-4">
        <label style="color: #1e293b; font-weight: 600;">Tóm tắt ngắn Bài viết (Excerpt)</label>
        <textarea v-model="form.excerpt" rows="3" class="admin-input-style" placeholder="Tóm tắt 2-3 câu ngắn gọn hiển thị trên trang danh sách tin tức..." style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;"></textarea>
      </div>

      <!-- Detailed Content Editor (Rich Text) -->
      <div class="mt-6 p-4" style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px;">
        <h4 style="margin: 0 0 12px 0; color: #022b9f; font-size: 16px; font-weight: 800;">Nội dung chi tiết Bài viết (WYSIWYG Soạn thảo văn bản)</h4>
        <RichTextEditor 
          v-model="form.content" 
          placeholder="Soạn thảo nội dung bài viết tin tức đầy đủ (In đậm, In nghiêng, H2, H3, Danh sách, Link, Chèn bảng/ảnh)..." 
        />
      </div>

      <div class="flex-end gap-3 mt-6 pt-4" style="border-top: 1px solid #e2e8f0;">
        <button type="button" @click="$emit('cancel')" class="btn btn-secondary" style="padding: 10px 24px;">Hủy bỏ</button>
        <button type="submit" class="btn btn-primary" :disabled="savingBlog" style="padding: 10px 24px; font-weight: 700;">
          {{ savingBlog ? 'Đang lưu...' : (isEditing ? 'Cập nhật Bài viết' : 'Tạo Bài viết mới') }}
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
  },
  availableCategories: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits(['cancel', 'saved', 'open-category-modal']);
const courseStore = useCourseStore();

const isEditing = computed(() => !!(props.initialData && props.initialData.id));
const savingBlog = ref(false);
const uploadingImage = ref(false);
const imageFileRef = ref(null);

const showQuickAddCat = ref(false);
const quickCatName = ref('');
const isSubmittingCat = ref(false);

// Cropper States
const isCropperOpen = ref(false);
const cropTargetUrl = ref('');
const cropAspectRatio = ref('wide');
const cropModalTitle = ref('✂ Cắt Thumbnail Bài Viết');
let cropTargetCallback = null;

const form = ref({
  id: '',
  title: '',
  handle: '',
  category: '',
  date: '',
  image: '',
  excerpt: '',
  content: '',
  link: ''
});

onMounted(() => {
  if (props.initialData) {
    const p = props.initialData;
    form.value = {
      id: p.id,
      title: p.title || '',
      handle: p.handle || '',
      category: p.category || '',
      date: p.date || '',
      image: p.image || '',
      excerpt: p.excerpt || '',
      content: p.content || '',
      link: p.link || ''
    };
  } else {
    form.value = {
      id: '',
      title: '',
      handle: '',
      category: props.availableCategories.length > 0 ? props.availableCategories[0].name : 'AI 2026',
      date: new Date().toLocaleDateString('vi-VN', { day: '2-digit', month: '2-digit', year: 'numeric' }),
      image: '',
      excerpt: '',
      content: '',
      link: ''
    };
  }
});

const generateSlug = () => {
  if (isEditing.value) return;
  if (!form.value.title) {
    form.value.handle = '';
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
  form.value.handle = slug.substring(0, 70);
};

const handleQuickAddCategory = async () => {
  const name = quickCatName.value.trim();
  if (!name) return;
  isSubmittingCat.value = true;
  try {
    const created = await courseStore.addBlogCategory({ name });
    if (created) {
      form.value.category = created.name;
      quickCatName.value = '';
      showQuickAddCat.value = false;
      await courseStore.fetchBlogCategories(true);
    }
  } catch (err) {
    // Toast handled in store
  } finally {
    isSubmittingCat.value = false;
  }
};

const openCropper = (url, callback, ratio = 'wide', title = '✂ Cắt Thumbnail Bài Viết') => {
  if (!url) return;
  cropTargetUrl.value = url;
  cropAspectRatio.value = ratio;
  cropModalTitle.value = title;
  cropTargetCallback = callback;
  isCropperOpen.value = true;
};

const onFileSelectForCrop = (event, callback, ratio = 'wide', title = '✂ Cắt Thumbnail Bài Viết') => {
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

const saveBlog = async () => {
  if (savingBlog.value) return;
  if (!form.value.title || !form.value.handle) {
    courseStore.showToast('Vui lòng điền đầy đủ tiêu đề và slug đường dẫn tĩnh!', 'error');
    return;
  }

  if (!form.value.link) {
    form.value.link = `/blog/${form.value.handle}`;
  }

  savingBlog.value = true;
  try {
    if (isEditing.value) {
      await courseStore.updateAdminBlogPost(props.initialData.id, form.value);
    } else {
      await courseStore.addAdminBlogPost(form.value);
    }
    emit('saved');
  } catch (err) {
    console.error("Save blog post error:", err);
  } finally {
    savingBlog.value = false;
  }
};
</script>

