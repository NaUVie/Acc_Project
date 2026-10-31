<template>
  <div class="admin-page-card" style="background: #ffffff; color: #0f172a; border-radius: 16px; padding: 28px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); border: 1px solid #e2e8f0;">
    <div class="flex-between pb-4 mb-4" style="border-bottom: 1px solid #e2e8f0;">
      <div style="display: flex; align-items: center; gap: 12px;">
        <button type="button" @click="$emit('cancel')" class="btn btn-secondary btn-sm" style="padding: 8px 16px; font-weight: 600;">
          ← Quay lại danh sách
        </button>
        <h3 style="margin: 0; color: #0f172a; font-size: 20px; font-weight: 800;">
          {{ isEditingCourse ? 'Chỉnh sửa thông tin khóa học' : 'Thêm khóa học mới' }}
        </h3>
      </div>
      <button type="button" @click="$emit('cancel')" class="btn btn-secondary btn-sm">Hủy</button>
    </div>

    <form @submit.prevent="saveCourse">
      <div class="form-group">
        <label style="color: #1e293b; font-weight: 600;">Tên khóa học</label>
        <input v-model="courseForm.title" @input="onTitleInput" type="text" required class="admin-input-style" placeholder="Ví dụ: ChatGPT thực chiến nâng cao" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
      </div>

      <div class="form-group mt-3">
        <label style="color: #1e293b; font-weight: 600;">Đường dẫn tĩnh (Slug / Handle - Tự động tạo)</label>
        <input v-model="courseForm.handle" type="text" required class="admin-input-style" placeholder="chatgpt-nang-cao" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
      </div>

      <div class="grid-2 mt-3">
        <div class="form-group">
          <label style="color: #1e293b; font-weight: 600;">Chuyên mục</label>
          <select v-model="courseForm.category" class="admin-input-style" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;">
            <option v-for="cat in categories" :key="cat.slug" :value="cat.slug">{{ cat.name }} ({{ cat.slug }})</option>
            <option value="custom">+ Nhập chuyên mục tùy chỉnh mới...</option>
          </select>
          <div v-if="courseForm.category === 'custom'" class="mt-2">
            <input v-model="customCategorySlug" type="text" placeholder="Nhập mã slug chuyên mục mới (ví dụ: marketing-ai)" class="admin-input-style" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
          </div>
        </div>
      </div>

      <div class="grid-2 mt-3">
        <div class="form-group">
          <label style="color: #1e293b; font-weight: 600;">Ảnh Thumbnail / Danh sách (Card)</label>
          <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
            <input v-model="courseForm.image" type="text" required class="admin-input-style" placeholder="/images/default.jpg hoặc URL Cloudinary" style="flex: 1; min-width: 200px; background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
            <label class="btn btn-primary btn-sm" style="padding: 10px 14px; cursor: pointer; display: inline-flex; align-items: center; gap: 6px; white-space: nowrap; margin: 0; font-weight: 600;">
              <span>Tải ảnh</span>
              <input type="file" accept="image/*" @change="onFileSelectForCrop($event, (url) => { courseForm.image = url; }, 'square', '✂ Cắt Thumbnail Khóa Học (1:1)')" style="display: none;" />
            </label>
          </div>
          <div v-if="uploadingCourseImage" style="font-size: 12px; color: #0284c7; margin-top: 4px; font-weight: 600;">
            Đang tải ảnh thumbnail lên Cloudinary...
          </div>
          <div v-if="courseForm.image" class="mt-2" style="display: flex; align-items: center; gap: 12px;">
            <img :src="courseForm.image" alt="Thumbnail Preview" style="max-height: 80px; border-radius: 8px; border: 1px solid #cbd5e1; object-fit: contain; background: #ffffff;" />
            <button type="button" class="btn btn-sm btn-secondary" style="font-size: 12px; font-weight: 600; color: #0284c7; border-color: #bae6fd;" @click="openCropper(courseForm.image, (url) => { courseForm.image = url; }, 'square', '✂ Cắt Thumbnail Khóa Học (1:1)')">✂ Cắt lại ảnh</button>
          </div>
        </div>

        <div class="form-group">
          <label style="color: #1e293b; font-weight: 600;">Ảnh Bìa hiển thị trang chi tiết (Cover Image)</label>
          <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
            <input v-model="courseForm.coverImage" type="text" class="admin-input-style" placeholder="Để trống sẽ dùng chung ảnh Thumbnail" style="flex: 1; min-width: 200px; background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
            <label class="btn btn-primary btn-sm" style="padding: 10px 14px; cursor: pointer; display: inline-flex; align-items: center; gap: 6px; white-space: nowrap; margin: 0; font-weight: 600; background: #475569;">
              <span>Tải ảnh</span>
              <input type="file" accept="image/*" @change="onFileSelectForCrop($event, (url) => { courseForm.coverImage = url; }, 'wide', '✂ Cắt Cover Khóa Học (16:9)')" style="display: none;" />
            </label>
          </div>
          <div v-if="uploadingCoverImage" style="font-size: 12px; color: #0284c7; margin-top: 4px; font-weight: 600;">
            Đang tải ảnh bìa chi tiết lên Cloudinary...
          </div>
          <div v-if="courseForm.coverImage" class="mt-2" style="display: flex; align-items: center; gap: 12px;">
            <img :src="courseForm.coverImage" alt="Cover Preview" style="max-height: 80px; border-radius: 8px; border: 1px solid #cbd5e1; object-fit: contain; background: #ffffff;" />
            <button type="button" class="btn btn-sm btn-secondary" style="font-size: 12px; font-weight: 600; color: #0284c7; border-color: #bae6fd;" @click="openCropper(courseForm.coverImage, (url) => { courseForm.coverImage = url; }, 'wide', '✂ Cắt Cover Khóa Học (16:9)')">✂ Cắt lại ảnh</button>
          </div>
        </div>
      </div>

      <div class="grid-2 mt-3">
        <div class="form-group">
          <label style="color: #1e293b; font-weight: 600;">Giá bán (VNĐ)</label>
          <input v-model.number="courseForm.price" type="number" required class="admin-input-style" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1; font-weight: bold;" />
        </div>
        <div class="form-group">
          <label style="color: #1e293b; font-weight: 600;">Giá gốc niêm yết (VNĐ)</label>
          <input v-model.number="courseForm.originalPrice" type="number" required class="admin-input-style" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
        </div>
      </div>

      <div class="grid-2 mt-3">
        <div class="form-group">
          <label style="color: #1e293b; font-weight: 600;">Thời lượng</label>
          <input v-model="courseForm.duration" type="text" required class="admin-input-style" placeholder="12 tuần, 24 giờ học..." style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
        </div>
        <div class="form-group">
          <label style="color: #1e293b; font-weight: 600;">Trình độ</label>
          <input v-model="courseForm.level" type="text" required class="admin-input-style" placeholder="Cơ bản, Trung cấp, Nâng cao" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
        </div>
      </div>

      <div class="form-group mt-3">
        <label style="color: #1e293b; font-weight: 600;">Mô tả chi tiết & Tổng quan khóa học (Soạn thảo văn bản)</label>
        <RichTextEditor v-model="courseForm.description" placeholder="Soạn thảo mô tả chi tiết, tổng quan nội dung khóa học..." />
      </div>

      <div class="form-group mt-3">
        <label style="color: #1e293b; font-weight: 600;">Lộ trình khóa học tùy chỉnh (Giai đoạn 1, 2, 3...)</label>
        <RichTextEditor v-model="courseForm.customRoadmap" placeholder="Ví dụ:&#10;Giai đoạn 1 – AI Foundation | 2 ngày&#10;Xây dựng nền tảng sử dụng AI...&#10;Giai đoạn 2 – AI Agent Operating System | 2 ngày&#10;Thực hành xây dựng ứng dụng..." />
        <small class="text-muted" style="display: block; margin-top: 4px;">Soạn thảo chi tiết các giai đoạn lộ trình học (Nếu để trống sẽ hiển thị bài giảng từ mục Giáo trình).</small>
      </div>

      <div class="form-group mt-3">
        <label style="color: #1e293b; font-weight: 600;">Đội ngũ Giảng viên / Người thực hiện khóa học</label>
        <div style="display: flex; flex-direction: column; gap: 8px;">
          <select v-model="selectedLecturerToAdd" @change="addLecturerToCourse" class="admin-input-style" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;">
            <option value="">-- Chọn Giảng viên để thêm vào khóa học --</option>
            <option v-for="l in lecturers" :key="l.id" :value="l.id">{{ l.name }} ({{ l.title }})</option>
          </select>
          <div v-if="selectedLecturersList.length > 0" style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 4px;">
            <span v-for="lec in selectedLecturersList" :key="lec.id" style="background: #e0f2fe; color: #0369a1; border: 1px solid #bae6fd; padding: 6px 12px; border-radius: 20px; font-size: 13px; font-weight: 600; display: inline-flex; align-items: center; gap: 8px;">
              <span>{{ lec.name }} - {{ lec.title }}</span>
              <button type="button" @click="removeLecturerFromCourse(lec.id)" style="background: none; border: none; color: #ef4444; font-weight: 800; cursor: pointer; padding: 0 4px; font-size: 14px;">✕</button>
            </span>
          </div>
        </div>
      </div>

      <div class="form-group mt-3">
        <label style="color: #1e293b; font-weight: 600;">Bạn sẽ đạt được gì sau khóa học này? (Mỗi mục 1 dòng)</label>
        <textarea v-model="courseForm.outcomes" rows="4" class="admin-input-style" placeholder="Ví dụ:&#10;Rèn luyện tư duy giao tiếp và thuyết phục hiệu quả trong công việc&#10;Làm chủ phương pháp quản lý thời gian và giải quyết vấn đề linh hoạt&#10;Nâng cao khả năng làm việc nhóm và đàm phán chuyên nghiệp" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;"></textarea>
        <small class="text-muted" style="display: block; margin-top: 4px;">Nhập từng kết quả đạt được trên một dòng riêng biệt.</small>
      </div>

      <div class="form-group mt-3">
        <label style="color: #1e293b; font-weight: 600;">Yêu cầu & Đối tượng phù hợp (Mỗi mục 1 dòng)</label>
        <textarea v-model="courseForm.requirements" rows="4" class="admin-input-style" placeholder="Ví dụ:&#10;Dành cho Quản lý, Chuyên viên, Freelancer và bất kỳ ai muốn nâng cao năng lực thời AI.&#10;Không yêu cầu kiến thức lập trình phức tạp – bài giảng cầm tay chỉ việc.&#10;Chỉ cần máy tính kết nối Internet để tham gia học trực tuyến." style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;"></textarea>
        <small class="text-muted" style="display: block; margin-top: 4px;">Nhập từng yêu cầu hoặc đối tượng trên một dòng riêng biệt.</small>
      </div>

      <div class="flex-between mt-6 pt-4" style="border-top: 1px solid #e2e8f0;">
        <button type="button" @click="$emit('cancel')" class="btn btn-secondary btn-sm" style="padding: 10px 24px;">Hủy bỏ</button>
        <button type="submit" class="btn btn-primary btn-sm" style="padding: 10px 32px; font-weight: 700;">Lưu thông tin khóa học</button>
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
import RichTextEditor from '@/components/RichTextEditor.vue';
import ImageCropperModal from '@/components/ImageCropperModal.vue';

const props = defineProps({
  initialData: {
    type: Object,
    default: null
  },
  categories: {
    type: Array,
    default: () => []
  },
  lecturers: {
    type: Array,
    default: () => []
  },
  courses: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits(['cancel', 'saved']);
const courseStore = useCourseStore();

const isEditingCourse = computed(() => !!(props.initialData && props.initialData.id));
const customCategorySlug = ref('');
const selectedLecturerToAdd = ref('');
const uploadingCourseImage = ref(false);
const uploadingCoverImage = ref(false);

// Cropper States
const isCropperOpen = ref(false);
const cropTargetUrl = ref('');
const cropAspectRatio = ref('square');
const cropModalTitle = ref('✂ Cắt & Căn Chỉnh Hình Ảnh Khóa Học');
let cropTargetCallback = null;

const courseForm = ref({
  title: '',
  handle: '',
  category: 'dao-tao-doanh-nghiep',
  programId: null,
  image: '',
  coverImage: '',
  price: 0,
  originalPrice: 0,
  duration: '12 tuần',
  level: 'Trung cấp',
  description: '',
  outcomes: '',
  requirements: '',
  customRoadmap: '',
  lecturerIds: ''
});

onMounted(() => {
  if (props.initialData) {
    const c = props.initialData;
    let formattedOutcomes = c.outcomes || '';
    if (Array.isArray(formattedOutcomes)) {
      formattedOutcomes = formattedOutcomes.join('\n');
    } else if (typeof formattedOutcomes === 'string') {
      try {
        const parsed = JSON.parse(formattedOutcomes);
        if (Array.isArray(parsed)) formattedOutcomes = parsed.join('\n');
      } catch (e) {}
    }

    let formattedRequirements = c.requirements || '';
    if (Array.isArray(formattedRequirements)) {
      formattedRequirements = formattedRequirements.join('\n');
    } else if (typeof formattedRequirements === 'string') {
      try {
        const parsed = JSON.parse(formattedRequirements);
        if (Array.isArray(parsed)) formattedRequirements = parsed.join('\n');
      } catch (e) {}
    }

    courseForm.value = {
      title: c.title,
      handle: c.handle,
      category: c.category,
      programId: c.programId || null,
      image: c.image,
      coverImage: c.coverImage || '',
      price: c.price,
      originalPrice: c.originalPrice,
      duration: c.duration,
      level: c.level,
      description: c.description,
      outcomes: formattedOutcomes,
      requirements: formattedRequirements,
      customRoadmap: c.customRoadmap || '',
      lecturerIds: c.lecturerIds || ''
    };
  } else {
    courseForm.value = {
      title: '',
      handle: '',
      category: 'dao-tao-doanh-nghiep',
      programId: null,
      image: '/images/default.jpg',
      coverImage: '',
      price: 9800000,
      originalPrice: 12000000,
      duration: '12 tuần',
      level: 'Trung cấp',
      description: '',
      outcomes: '',
      requirements: '',
      customRoadmap: '',
      lecturerIds: ''
    };
  }
});

const onTitleInput = () => {
  if (!isEditingCourse.value) {
    courseForm.value.handle = slugify(courseForm.value.title);
  }
};

const selectedLecturersList = computed(() => {
  if (!courseForm.value.lecturerIds) return [];
  const ids = courseForm.value.lecturerIds.split(',').map(id => id.trim()).filter(Boolean);
  return ids.map(id => {
    const lec = props.lecturers.find(l => l.id === id);
    return lec || { id, name: id, title: 'Giảng viên' };
  });
});

const addLecturerToCourse = () => {
  if (!selectedLecturerToAdd.value) return;
  const currentIds = courseForm.value.lecturerIds ? courseForm.value.lecturerIds.split(',').map(s => s.trim()).filter(Boolean) : [];
  if (!currentIds.includes(selectedLecturerToAdd.value)) {
    currentIds.push(selectedLecturerToAdd.value);
    courseForm.value.lecturerIds = currentIds.join(',');
  }
  selectedLecturerToAdd.value = '';
};

const removeLecturerFromCourse = (id) => {
  const currentIds = courseForm.value.lecturerIds ? courseForm.value.lecturerIds.split(',').map(s => s.trim()).filter(Boolean) : [];
  courseForm.value.lecturerIds = currentIds.filter(i => i !== id).join(',');
};

const openCropper = (url, callback, ratio = 'square', title = '✂ Cắt & Căn Chỉnh Hình Ảnh Khóa Học') => {
  if (!url) return;
  cropTargetUrl.value = url;
  cropAspectRatio.value = ratio;
  cropModalTitle.value = title;
  cropTargetCallback = callback;
  isCropperOpen.value = true;
};

const onFileSelectForCrop = (event, callback, ratio = 'square', title = '✂ Cắt & Căn Chỉnh Hình Ảnh Khóa Học') => {
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

const saveCourse = async () => {
  try {
    const payload = { 
      ...courseForm.value,
      image: formatImageUrl(courseForm.value.image),
      coverImage: courseForm.value.coverImage ? formatImageUrl(courseForm.value.coverImage) : null
    };
    if (payload.category === 'custom') {
      if (!customCategorySlug.value.trim()) {
        courseStore.showToast('Vui lòng nhập mã slug cho chuyên mục mới!', 'warning');
        return;
      }
      payload.category = customCategorySlug.value.trim();
    }
    if (isEditingCourse.value) {
      await courseStore.updateAdminCourse(props.initialData.id, payload);
      courseStore.showToast('Cập nhật khóa học thành công!', 'success');
    } else {
      if (props.courses.some(c => c.handle === payload.handle)) {
        courseStore.showToast('Đường dẫn tĩnh (Slug) này đã tồn tại!', 'warning');
        return;
      }
      await courseStore.addAdminCourse(payload);
      courseStore.showToast('Thêm khóa học mới thành công!', 'success');
    }
    emit('saved');
  } catch (err) {
    courseStore.showToast(err.message || 'Không thể lưu khóa học.', 'error');
  }
};
</script>

