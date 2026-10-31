<template>
  <div class="tab-content animate-fade-in">
    <!-- SUB-NAV: HERO BANNERS VS HOME VIDEO & INTRO -->
    <div class="mb-4" style="display: flex; gap: 10px; border-bottom: 2px solid #e2e8f0; padding-bottom: 12px;">
      <button 
        type="button" 
        @click="subTab = 'banners'" 
        class="btn btn-sm"
        :class="subTab === 'banners' ? 'btn-primary' : 'btn-secondary'"
        style="font-weight: 700; border-radius: 8px;"
      >
        Banner Hero ({{ banners.length }})
      </button>
      <button 
        type="button" 
        @click="openHomeIntroTab" 
        class="btn btn-sm"
        :class="subTab === 'home_intro' ? 'btn-primary' : 'btn-secondary'"
        style="font-weight: 700; border-radius: 8px;"
      >
        Video & Giới thiệu Kiến tạo năng lực
      </button>
    </div>

    <!-- TAB 1: BANNERS CAROUSEL -->
    <div v-if="subTab === 'banners'">
      <!-- VIEW 1: LIST TABLE -->
      <div v-if="activeView === 'list'">
        <div class="content-header flex-between">
          <div>
            <h2>Quản lý Banner (Hero Carousel)</h2>
            <p>Tùy chỉnh các banner quảng cáo và hình ảnh trình chiếu trên trang chủ.</p>
          </div>
          <button @click="openAddModal" class="btn btn-primary btn-sm">+ Thêm Banner mới</button>
        </div>

        <!-- Banners Table -->
        <div class="table-responsive mt-6">
        <table class="admin-table">
          <thead>
            <tr>
              <th style="width: 60px;">Vị trí</th>
              <th>Preview Banner</th>
              <th>Tiêu đề & Link</th>
              <th>Loại Link</th>
              <th>Trạng thái</th>
              <th>Hành động</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="b in banners" :key="b.id">
              <td class="font-bold text-center">
                <span class="badge" style="background: #e0f2fe; color: #0369a1; font-weight: 700; padding: 4px 10px; border-radius: 6px;">
                  #{{ b.position }}
                </span>
              </td>
              <td>
                <div style="display: flex; gap: 8px; align-items: center;">
                  <img :src="b.desktop_image" :alt="b.title" class="admin-course-thumb" style="width: 120px; height: 60px; object-fit: cover; border-radius: 8px; border: 1px solid #cbd5e1;" />
                  <img v-if="b.mobile_image" :src="b.mobile_image" alt="Mobile" class="admin-course-thumb" style="width: 35px; height: 60px; object-fit: cover; border-radius: 8px; border: 1px solid #cbd5e1;" title="Mobile Image" />
                </div>
              </td>
              <td>
                <div class="font-bold" style="color: #0f172a; font-size: 15px;">{{ b.title }}</div>
                <small class="text-muted" style="word-break: break-all; display: block; margin-top: 2px;">
                  {{ b.link || '(Không có)' }}
                </small>
              </td>
              <td>
                <span class="badge" :style="b.is_external ? 'background: #fef3c7; color: #b45309;' : 'background: #f1f5f9; color: #475569;'">
                  {{ b.is_external ? 'Ngoại bộ' : 'Nội bộ' }}
                </span>
              </td>
              <td>
                <button 
                  @click="toggleActive(b)" 
                  class="badge" 
                  :style="b.is_active ? 'background: #dcfce7; color: #15803d; border: none; cursor: pointer; padding: 6px 12px;' : 'background: #fee2e2; color: #b91c1c; border: none; cursor: pointer; padding: 6px 12px;'"
                  title="Nhấn để đổi trạng thái"
                >
                  {{ b.is_active ? 'Đang hiển thị' : 'Đã ẩn' }}
                </button>
              </td>
              <td>
                <div class="action-buttons">
                  <button @click="openCropper(b.desktop_image, async (url) => { await courseStore.updateBanner(b.id, { desktop_image: url }); b.desktop_image = url; courseStore.showToast('Đã cắt và cập nhật banner!', 'success'); }, 'wide', '✂ Cắt Banner: ' + b.title)" class="btn-action edit" title="Cắt lại ảnh Banner" style="color: #0284c7;">✂️</button>
                  <button @click="editBanner(b)" class="btn-action edit" title="Sửa Banner">✏️</button>
                  <button @click="deleteBannerItem(b.id)" class="btn-action delete" title="Xóa Banner">🗑️</button>
                </div>
              </td>
            </tr>
            <tr v-if="banners.length === 0">
              <td colspan="6" class="text-center py-8 text-muted">Chưa có banner nào. Hãy nhấn "+ Thêm Banner mới".</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- VIEW 2: FORM ADD/EDIT -->
    <div v-else-if="activeView === 'form'" class="admin-page-card" style="background: #ffffff; color: #0f172a; border-radius: 16px; padding: 28px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); border: 1px solid #e2e8f0;">
      <div class="flex-between pb-4 mb-4" style="border-bottom: 1px solid #e2e8f0;">
        <div style="display: flex; align-items: center; gap: 12px;">
          <button type="button" @click="activeView = 'list'" class="btn btn-secondary btn-sm" style="padding: 8px 16px; font-weight: 600;">
            ← Quay lại danh sách
          </button>
          <h3 style="margin: 0; color: #0f172a; font-size: 20px; font-weight: 800;">
            {{ isEditing ? 'Chỉnh sửa Banner' : 'Thêm Banner mới' }}
          </h3>
        </div>
        <button type="button" @click="activeView = 'list'" class="btn btn-secondary btn-sm">Hủy</button>
      </div>

      <form @submit.prevent="saveBanner" class="mt-2">
        <div class="form-group">
          <label style="color: #1e293b; font-weight: 600;">Tiêu đề Banner</label>
          <input v-model="form.title" type="text" required class="admin-input-style" placeholder="Ví dụ: AI Center of Excellence" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
        </div>

        <div class="grid grid-2 gap-4 mt-4">
          <div class="form-group">
            <label style="color: #1e293b; font-weight: 600;">Ảnh Desktop (Yêu cầu)</label>
            <div style="display: flex; gap: 8px; margin-top: 4px;">
              <input v-model="form.desktop_image" type="text" required class="admin-input-style" placeholder="/images/CoE-Web.png hoặc URL" style="flex: 1; background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
              <input type="file" ref="desktopFileRef" @change="onFileSelectForCrop($event, (url) => { form.desktop_image = url; }, 'wide', '✂ Cắt Banner Desktop (16:9)')" style="display: none;" accept="image/*" />
              <button type="button" @click="$refs.desktopFileRef.click()" class="btn btn-secondary btn-sm">Upload</button>
            </div>
            <div v-if="form.desktop_image" style="display: flex; align-items: center; gap: 12px; margin-top: 8px;">
              <img :src="form.desktop_image" alt="Preview Desktop" style="max-height: 80px; border-radius: 8px; border: 1px solid #e2e8f0; object-fit: cover;" />
              <button type="button" class="btn btn-sm btn-secondary" style="font-size: 12px; font-weight: 600; color: #0284c7; border-color: #bae6fd;" @click="openCropper(form.desktop_image, (url) => { form.desktop_image = url; }, 'wide', '✂ Cắt Banner Desktop (16:9)')">✂ Cắt lại ảnh</button>
            </div>
          </div>

          <div class="form-group">
            <label style="color: #1e293b; font-weight: 600;">Ảnh Mobile (Tùy chọn)</label>
            <div style="display: flex; gap: 8px; margin-top: 4px;">
              <input v-model="form.mobile_image" type="text" class="admin-input-style" placeholder="/images/CoE-Mobile.png hoặc URL" style="flex: 1; background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
              <input type="file" ref="mobileFileRef" @change="onFileSelectForCrop($event, (url) => { form.mobile_image = url; }, 'free', '✂ Cắt Banner Mobile')" style="display: none;" accept="image/*" />
              <button type="button" @click="$refs.mobileFileRef.click()" class="btn btn-secondary btn-sm">Upload</button>
            </div>
            <div v-if="form.mobile_image" style="display: flex; align-items: center; gap: 12px; margin-top: 8px;">
              <img :src="form.mobile_image" alt="Preview Mobile" style="max-height: 80px; border-radius: 8px; border: 1px solid #e2e8f0; object-fit: cover;" />
              <button type="button" class="btn btn-sm btn-secondary" style="font-size: 12px; font-weight: 600; color: #0284c7; border-color: #bae6fd;" @click="openCropper(form.mobile_image, (url) => { form.mobile_image = url; }, 'free', '✂ Cắt Banner Mobile')">✂ Cắt lại ảnh</button>
            </div>
          </div>
        </div>

        <div class="grid grid-2 gap-4 mt-4">
          <div class="form-group">
            <label style="color: #1e293b; font-weight: 600;">Đường dẫn Liên kết (Link)</label>
            <input v-model="form.link" type="text" class="admin-input-style" placeholder="Ví dụ: /corporate/coe hoặc https://..." style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
          </div>

          <div class="form-group">
            <label style="color: #1e293b; font-weight: 600;">Thứ tự hiển thị (Position)</label>
            <input v-model.number="form.position" type="number" min="0" class="admin-input-style" placeholder="1, 2, 3..." style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
          </div>
        </div>

        <div class="grid grid-2 gap-4 mt-4" style="background: #f8fafc; padding: 16px; border-radius: 10px; border: 1px solid #e2e8f0;">
          <div class="form-group" style="display: flex; align-items: center; gap: 10px; margin: 0;">
            <input v-model="form.is_external" type="checkbox" id="is_external" style="width: 18px; height: 18px; cursor: pointer;" />
            <label for="is_external" style="color: #1e293b; font-weight: 600; cursor: pointer; margin: 0;">
              Mở link trong tab mới (Trang ngoài / External Link)
            </label>
          </div>

          <div class="form-group" style="display: flex; align-items: center; gap: 10px; margin: 0;">
            <input v-model="form.is_active" type="checkbox" id="is_active" style="width: 18px; height: 18px; cursor: pointer;" />
            <label for="is_active" style="color: #1e293b; font-weight: 600; cursor: pointer; margin: 0;">
              Hiển thị Banner này trên trang chủ (Active)
            </label>
          </div>
        </div>

        <div class="mt-6 flex-end" style="gap: 12px; border-top: 1px solid #e2e8f0; padding-top: 20px;">
          <button type="button" @click="activeView = 'list'" class="btn btn-secondary">Hủy</button>
          <button type="submit" class="btn btn-primary" :disabled="saving">
            {{ saving ? 'Đang lưu...' : (isEditing ? 'Cập nhật Banner' : 'Tạo Banner') }}
          </button>
        </div>
      </form>
    </div>
    </div> <!-- END TAB 1: BANNERS -->

    <!-- TAB 2: HOME INTRO & VIDEO CONFIGURATION -->
    <div v-else-if="subTab === 'home_intro'" class="admin-page-card" style="background: #ffffff; color: #0f172a; border-radius: 16px; padding: 28px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); border: 1px solid #e2e8f0;">
      <div class="content-header flex-between pb-4 mb-4" style="border-bottom: 1px solid #e2e8f0;">
        <div>
          <h2 style="font-size: 20px; font-weight: 800; color: #0f172a; margin: 0 0 6px 0;">Cấu hình Phần "Kiến tạo năng lực — Dẫn dắt chuyển đổi bền vững" & Video</h2>
          <p style="color: #64748b; margin: 0; font-size: 13.5px;">Tùy chỉnh tiêu đề, hai đoạn văn giới thiệu, số liệu bộ đếm, đường dẫn video giới thiệu và ảnh bìa hiển thị trên trang chủ.</p>
        </div>
        <button type="button" @click="loadHomeIntroSettings" class="btn btn-secondary btn-sm" :disabled="loadingIntro">
          {{ loadingIntro ? 'Đang tải...' : 'Tải lại' }}
        </button>
      </div>

      <form @submit.prevent="saveHomeIntro">
        <div class="form-group mb-4">
          <label style="color: #1e293b; font-weight: 700; font-size: 14px;">Tiêu đề chính (Hiệu ứng chữ từng từ) <span style="color: #e11d48;">*</span></label>
          <input 
            v-model="introForm.title" 
            type="text" 
            required 
            class="admin-input-style" 
            placeholder="Kiến tạo năng lực – Dẫn dắt chuyển đổi bền vững" 
            style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1; font-weight: 600;" 
          />
          <small class="text-muted" style="display: block; margin-top: 4px;">Mỗi từ trong câu tiêu đề này sẽ tự động chạy hiệu ứng xuất hiện trên trang chủ.</small>
        </div>

        <div class="grid grid-2 gap-4 mb-4">
          <div class="form-group">
            <label style="color: #1e293b; font-weight: 700; font-size: 14px;">Đoạn giới thiệu 1 <span style="color: #e11d48;">*</span></label>
            <textarea 
              v-model="introForm.desc1" 
              rows="4" 
              required 
              class="admin-input-style" 
              placeholder="ACC Academy đồng hành cùng cá nhân, doanh nghiệp và tổ chức..." 
              style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;"
            ></textarea>
          </div>

          <div class="form-group">
            <label style="color: #1e293b; font-weight: 700; font-size: 14px;">Đoạn giới thiệu 2 <span style="color: #e11d48;">*</span></label>
            <textarea 
              v-model="introForm.desc2" 
              rows="4" 
              required 
              class="admin-input-style" 
              placeholder="Chúng tôi kết hợp Đào tạo – Tư vấn – Công nghệ – Chiến lược..." 
              style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;"
            ></textarea>
          </div>
        </div>

        <div class="grid grid-2 gap-4 mb-4" style="background: #f8fafc; padding: 18px; border-radius: 12px; border: 1px solid #e2e8f0;">
          <div class="form-group">
            <label style="color: #1e293b; font-weight: 700; font-size: 14px;">Số đếm hiển thị (Counter number)</label>
            <input 
              v-model.number="introForm.counter_number" 
              type="number" 
              min="0" 
              class="admin-input-style" 
              placeholder="500" 
              style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1; font-weight: 700;" 
            />
            <small class="text-muted" style="display: block; margin-top: 4px;">Hệ thống sẽ tự động thêm dấu "+" và chạy hiệu ứng tăng số (Ví dụ: 500+).</small>
          </div>

          <div class="form-group">
            <label style="color: #1e293b; font-weight: 700; font-size: 14px;">Mô tả dưới số đếm</label>
            <input 
              v-model="introForm.counter_label" 
              type="text" 
              class="admin-input-style" 
              placeholder="CHƯƠNG TRÌNH & DỰ ÁN ĐÀO TẠO – TƯ VẤN ĐÃ TRIỂN KHAI" 
              style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" 
            />
          </div>
        </div>

        <!-- Video Configuration Section -->
        <div class="p-4 mb-4" style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 12px;">
          <h4 style="margin: 0 0 12px 0; color: #166534; font-size: 15px; font-weight: 800;">Cấu hình Video Giới thiệu Trang chủ</h4>

          <div class="form-group mb-3">
            <label style="color: #14532d; font-weight: 700; font-size: 13.5px;">Đường dẫn Video (Hỗ trợ Link YouTube, Google Drive, Direct MP4 hoặc Upload file) <span style="color: #e11d48;">*</span></label>
            <div style="display: flex; gap: 8px;">
              <input 
                v-model="introForm.video_url" 
                type="text" 
                required 
                class="admin-input-style" 
                placeholder="Dán link YouTube, Google Drive (drive.google.com/file/d/...) hoặc URL .mp4" 
                style="flex: 1; background: #ffffff; color: #0f172a; border: 1px solid #86efac;" 
              />
              <input type="file" ref="videoFileRef" @change="uploadVideoFile" style="display: none;" accept="video/*" />
              <button type="button" @click="$refs.videoFileRef.click()" class="btn btn-secondary btn-sm" :disabled="uploadingVideo">
                {{ uploadingVideo ? 'Đang tải...' : 'Upload Video' }}
              </button>
            </div>
            <small style="display: block; margin-top: 4px; color: #15803d;">
              <strong>Hệ thống hỗ trợ đa dạng:</strong> Dán link YouTube (thường / Shorts), link chia sẻ Google Drive (ví dụ link của bạn: <code>https://drive.google.com/file/d/.../view</code>), file video trực tiếp (.mp4) hoặc bấm "Upload Video".
            </small>
          </div>

          <div class="grid grid-2 gap-4">
            <div class="form-group">
              <label style="color: #14532d; font-weight: 700; font-size: 13.5px;">Ảnh bìa Video (Poster Thumbnail)</label>
              <div style="display: flex; gap: 8px;">
                <input 
                  v-model="introForm.poster_url" 
                  type="text" 
                  class="admin-input-style" 
                  placeholder="/images/CoE-Thumb.png hoặc link ảnh" 
                  style="flex: 1; background: #ffffff; color: #0f172a; border: 1px solid #86efac;" 
                />
                <input type="file" ref="posterFileRef" @change="onFileSelectForCrop($event, (url) => { introForm.poster_url = url; }, 'wide', '✂ Cắt Poster Video (16:9)')" style="display: none;" accept="image/*" />
                <button type="button" @click="$refs.posterFileRef.click()" class="btn btn-secondary btn-sm">
                  Upload Ảnh
                </button>
              </div>
              <div v-if="introForm.poster_url" style="display: flex; align-items: center; gap: 12px; margin-top: 8px;">
                <img :src="introForm.poster_url" alt="Poster Preview" style="max-height: 80px; object-fit: cover; border-radius: 8px; border: 1px solid #86efac;" referrerpolicy="no-referrer" />
                <button type="button" class="btn btn-sm btn-secondary" style="font-size: 12px; font-weight: 600; color: #166534; border-color: #86efac;" @click="openCropper(introForm.poster_url, (url) => { introForm.poster_url = url; }, 'wide', '✂ Cắt Poster Video (16:9)')">✂ Cắt lại ảnh</button>
              </div>
            </div>

            <div class="form-group">
              <label style="color: #14532d; font-weight: 700; font-size: 13.5px;">Chữ nút phát trên ảnh bìa</label>
              <input 
                v-model="introForm.btn_label" 
                type="text" 
                class="admin-input-style" 
                placeholder="XEM VIDEO GIỚI THIỆU ACC ACADEMY" 
                style="background: #ffffff; color: #0f172a; border: 1px solid #86efac;" 
              />
            </div>
          </div>
        </div>

        <div class="flex-end" style="gap: 12px; border-top: 1px solid #e2e8f0; padding-top: 20px;">
          <button type="submit" class="btn btn-primary" :disabled="savingIntro" style="padding: 10px 24px; font-weight: 700;">
            {{ savingIntro ? 'Đang lưu cài đặt...' : 'Lưu Thay Đổi Trang Chủ' }}
          </button>
        </div>
      </form>
    </div>
    <!-- Image Cropper Modal -->
    <ImageCropperModal :isOpen="isCropperOpen" :imageUrl="cropTargetUrl" :aspectRatio="cropAspectRatio" :title="cropModalTitle" @close="isCropperOpen = false" @cropped="handleCroppedImage" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useCourseStore } from '@/stores/courses';
import { formatImageUrl } from '@/utils/imageHelper';
import ImageCropperModal from '@/components/ImageCropperModal.vue';

const courseStore = useCourseStore();

// Cropper States
const isCropperOpen = ref(false);
const cropTargetUrl = ref('');
const cropAspectRatio = ref('wide');
const cropModalTitle = ref('✂ Cắt & Căn Chỉnh Hình Ảnh');
let cropTargetCallback = null;

const openCropper = (url, callback, ratio = 'wide', title = '✂ Cắt & Căn Chỉnh Hình Ảnh') => {
  if (!url) return;
  cropTargetUrl.value = url;
  cropAspectRatio.value = ratio;
  cropModalTitle.value = title;
  cropTargetCallback = callback;
  isCropperOpen.value = true;
};

const onFileSelectForCrop = (event, callback, ratio = 'wide', title = '✂ Cắt & Căn Chỉnh Hình Ảnh') => {
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


const subTab = ref('banners'); // 'banners' or 'home_intro'

const activeView = ref('list');
const isEditing = ref(false);
const editingId = ref(null);
const saving = ref(false);

const form = ref({
  title: '',
  desktop_image: '',
  mobile_image: '',
  link: '',
  is_external: false,
  position: 1,
  is_active: true
});

// Home Intro & Video Config States
const loadingIntro = ref(false);
const savingIntro = ref(false);
const uploadingVideo = ref(false);
const introForm = ref({
  title: 'Kiến tạo năng lực – Dẫn dắt chuyển đổi bền vững',
  desc1: 'ACC Academy đồng hành cùng cá nhân, doanh nghiệp và tổ chức trong hành trình nâng cao năng lực, ứng dụng AI và chuyển đổi số vào thực tiễn.',
  desc2: 'Chúng tôi kết hợp Đào tạo – Tư vấn – Công nghệ – Chiến lược, giúp đội ngũ không chỉ hiểu công nghệ mà còn biết cách ứng dụng hiệu quả vào công việc, tối ưu quy trình và tạo ra giá trị tăng trưởng bền vững.',
  counter_number: 500,
  counter_label: 'CHƯƠNG TRÌNH & DỰ ÁN ĐÀO TẠO – TƯ VẤN ĐÃ TRIỂN KHAI',
  video_url: '/videos/intro.mp4',
  poster_url: '/images/CoE-Thumb.png',
  btn_label: 'XEM VIDEO GIỚI THIỆU ACC ACADEMY'
});

const banners = computed(() => courseStore.adminBanners);

onMounted(async () => {
  try {
    await courseStore.fetchAdminBanners();
  } catch (err) {
    console.error("Error loading admin banners:", err);
  }
});

const openAddModal = () => {
  isEditing.value = false;
  editingId.value = null;
  form.value = {
    title: '',
    desktop_image: '',
    mobile_image: '',
    link: '',
    is_external: false,
    position: (banners.value.length || 0) + 1,
    is_active: true
  };
  activeView.value = 'form';
};

const editBanner = (b) => {
  isEditing.value = true;
  editingId.value = b.id;
  form.value = {
    title: b.title,
    desktop_image: b.desktop_image,
    mobile_image: b.mobile_image || '',
    link: b.link || '',
    is_external: !!b.is_external,
    position: b.position || 1,
    is_active: !!b.is_active
  };
  activeView.value = 'form';
};

const toggleActive = async (b) => {
  try {
    await courseStore.updateBanner(b.id, { is_active: !b.is_active });
    courseStore.showToast(`Đã ${!b.is_active ? 'bật' : 'tắt'} hiển thị banner "${b.title}"`, 'success');
  } catch (err) {
    courseStore.showToast("Lỗi khi cập nhật trạng thái banner: " + err.message, 'error');
  }
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

const saveBanner = async () => {
  saving.value = true;
  try {
    const payload = {
      ...form.value,
      desktop_image: formatImageUrl(form.value.desktop_image),
      mobile_image: form.value.mobile_image ? formatImageUrl(form.value.mobile_image) : ''
    };
    if (isEditing.value) {
      await courseStore.updateBanner(editingId.value, payload);
      courseStore.showToast('Cập nhật banner thành công!', 'success');
    } else {
      await courseStore.createBanner(payload);
      courseStore.showToast('Tạo banner mới thành công!', 'success');
    }
    activeView.value = 'list';
  } catch (err) {
    courseStore.showToast("Có lỗi xảy ra: " + (err.message || err), 'error');
  } finally {
    saving.value = false;
  }
};

const deleteBannerItem = async (id) => {
  const isConfirmed = await courseStore.showConfirm({
    title: 'Xác nhận xóa Banner',
    message: 'Bạn có chắc chắn muốn xóa banner trình chiếu này khỏi trang chủ?',
    confirmText: 'Đồng ý xóa',
    cancelText: 'Hủy bỏ',
    type: 'danger'
  });

  if (isConfirmed) {
    try {
      await courseStore.deleteBanner(id);
      courseStore.showToast('Đã xóa banner thành công!', 'success');
    } catch (err) {
      courseStore.showToast("Lỗi khi xóa banner: " + err.message, 'error');
    }
  }
};

// Home Intro Methods
const openHomeIntroTab = async () => {
  subTab.value = 'home_intro';
  await loadHomeIntroSettings();
};

const loadHomeIntroSettings = async () => {
  loadingIntro.value = true;
  try {
    const res = await courseStore.fetchHomeIntroSettings();
    if (res) {
      introForm.value = {
        title: res.title || 'Kiến tạo năng lực – Dẫn dắt chuyển đổi bền vững',
        desc1: res.desc1 || '',
        desc2: res.desc2 || '',
        counter_number: res.counter_number ?? 500,
        counter_label: res.counter_label || 'CHƯƠNG TRÌNH & DỰ ÁN ĐÀO TẠO – TƯ VẤN ĐÃ TRIỂN KHAI',
        video_url: res.video_url || '/videos/intro.mp4',
        poster_url: res.poster_url || '/images/CoE-Thumb.png',
        btn_label: res.btn_label || 'XEM VIDEO GIỚI THIỆU ACC ACADEMY'
      };
    }
  } catch (err) {
    console.error("Error loading home intro settings:", err);
  } finally {
    loadingIntro.value = false;
  }
};

const uploadPosterFile = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  try {
    const url = await courseStore.uploadImage(file);
    introForm.value.poster_url = url;
    courseStore.showToast('Tải ảnh bìa video thành công!', 'success');
  } catch (err) {
    courseStore.showToast('Không thể upload ảnh bìa: ' + err.message, 'error');
  }
};

const uploadVideoFile = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  uploadingVideo.value = true;
  const formData = new FormData();
  formData.append('file', file);

  try {
    const res = await fetch('/api/upload', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${courseStore.token}`
      },
      body: formData
    });
    if (!res.ok) throw new Error('Upload video thất bại');
    const data = await res.json();
    introForm.value.video_url = data.url;
    courseStore.showToast('Tải video thành công!', 'success');
  } catch (err) {
    courseStore.showToast('Không thể upload video: ' + err.message, 'error');
  } finally {
    uploadingVideo.value = false;
  }
};

const saveHomeIntro = async () => {
  savingIntro.value = true;
  try {
    const payload = {
      ...introForm.value,
      poster_url: formatImageUrl(introForm.value.poster_url)
    };
    await courseStore.updateHomeIntroSettings(payload);
    courseStore.showToast('Đã lưu cấu hình phần giới thiệu & video trang chủ thành công!', 'success');
  } catch (err) {
    courseStore.showToast('Lỗi khi lưu cài đặt: ' + (err.message || err), 'error');
  } finally {
    savingIntro.value = false;
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
