<template>
  <div class="tab-content animate-fade-in">
    <!-- VIEW 1: ADMISSIONS LIST TABLE -->
    <div v-if="activeView === 'list'">
      <div class="content-header flex-between">
        <div>
          <h2>Quản lý Bài viết Tuyển sinh ({{ admissions.length }})</h2>
          <p>
            Quản lý các chương trình và bài viết tuyển sinh (MBA, GEI, Mini MBA...) hiển thị trên trang <strong>Tuyển sinh</strong> và trang chi tiết.
          </p>
        </div>
        <div style="display: flex; gap: 10px; align-items: center;">
          <button @click="refreshAdmissions" :disabled="isRefreshing" class="btn btn-secondary btn-sm" style="display: flex; align-items: center; gap: 6px; font-weight: 600;" title="Tải lại danh sách mới nhất">
            <span :class="{ 'spin-icon': isRefreshing }">🔄</span>
            <span>{{ isRefreshing ? 'Đang đồng bộ...' : 'Làm mới' }}</span>
          </button>
          <button @click="openAddModal" class="btn btn-primary btn-sm">+ Thêm Bài viết Tuyển sinh mới</button>
        </div>
      </div>

      <!-- SEARCH & FILTER BAR -->
      <div class="table-search-bar mt-4 mb-4" style="display: flex; gap: 12px; align-items: center; flex-wrap: wrap;">
        <input 
          v-model="searchQuery" 
          type="text" 
          class="admin-input-style" 
          placeholder="Tìm theo tiêu đề, slug, chuyên mục hoặc tag..." 
          style="max-width: 340px; padding: 8px 14px; font-size: 14px; background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1; border-radius: 8px;"
        />
        <select 
          v-model="filterStatus" 
          class="admin-input-style"
          style="max-width: 170px; padding: 8px 12px; font-size: 14px; background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1; border-radius: 8px;"
        >
          <option value="all">Tất cả trạng thái</option>
          <option value="active">Đang hiển thị</option>
          <option value="hidden">Đã ẩn</option>
        </select>
        <span class="text-muted" style="font-size: 13.5px; margin-left: auto;">
          Hiển thị <strong>{{ filteredAdmissions.length }}</strong> / {{ admissions.length }} bài viết
        </span>
      </div>

      <!-- Table -->
      <div class="table-responsive mt-2">
        <table class="admin-table">
          <thead>
            <tr>
              <th style="width: 120px; text-align: center;">Thứ tự</th>
              <th style="width: 110px;">Ảnh bìa</th>
              <th style="min-width: 240px;">Tiêu đề Bài viết</th>
              <th style="width: 180px;">Chuyên mục / Tag</th>
              <th style="min-width: 200px;">Điểm nổi bật</th>
              <th style="width: 120px; text-align: center;">Trạng thái</th>
              <th style="width: 110px; text-align: center;">Hành động</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="filteredAdmissions.length === 0">
              <td colspan="7" class="text-center" style="padding: 36px; color: #64748b;">
                Không tìm thấy bài viết tuyển sinh nào phù hợp.
              </td>
            </tr>
            <tr v-for="(post, idx) in filteredAdmissions" :key="post.id">
              <!-- CỘT THỨ TỰ -->
              <td style="text-align: center;">
                <div style="display: flex; align-items: center; justify-content: center; gap: 4px;">
                  <button 
                    type="button" 
                    @click="moveOrder(post, 'up')" 
                    :disabled="idx === 0"
                    class="order-btn"
                    title="Đưa lên trên"
                  >
                    ▲
                  </button>
                  <input 
                    type="number" 
                    :value="post.position"
                    @change="onPositionChange(post, $event.target.value)"
                    min="1"
                    style="width: 44px; text-align: center; font-weight: 700; color: #0f172a; border: 1px solid #cbd5e1; border-radius: 6px; padding: 3px 2px; font-size: 13px;"
                    title="Nhập số thứ tự và nhấn Enter để đổi"
                  />
                  <button 
                    type="button" 
                    @click="moveOrder(post, 'down')" 
                    :disabled="idx === filteredAdmissions.length - 1"
                    class="order-btn"
                    title="Đưa xuống dưới"
                  >
                    ▼
                  </button>
                </div>
              </td>

              <!-- ẢNH BÌA -->
              <td>
                <div style="position: relative; display: inline-block; width: 90px; height: 56px;">
                  <div style="width: 100%; height: 100%; border-radius: 8px; overflow: hidden; background: #f1f5f9; border: 1px solid #e2e8f0;">
                    <img 
                      v-if="post.image" 
                      :src="post.image" 
                      :alt="post.title"
                      style="width: 100%; height: 100%; object-fit: cover;"
                      @error="(e) => e.target.src = '/images/andrew.jpg'"
                    />
                    <div v-else style="display: flex; align-items: center; justify-content: center; height: 100%; font-size: 20px;">🎓</div>
                  </div>
                  <button 
                    v-if="post.image"
                    type="button"
                    class="crop-mini-btn"
                    title="✂ Cắt & căn chỉnh ảnh bìa"
                    @click="openCropper(post.image, async (url) => { await courseStore.updateAdmissionPost(post.id, { image: url }); }, 'wide', `✂ Cắt Ảnh: ${post.title}`)"
                  >
                    ✂
                  </button>
                </div>
              </td>

              <!-- TIÊU ĐỀ & SLUG -->
              <td>
                <div style="font-weight: 700; color: #0f172a; font-size: 14.5px; line-height: 1.4; margin-bottom: 4px;">
                  {{ post.title }}
                </div>
                <div style="display: flex; gap: 8px; align-items: center; font-size: 12.5px;">
                  <span style="color: #64748b; font-family: monospace;">/admissions/detail/{{ post.slug }}</span>
                  <router-link :to="`/admissions/detail/${post.slug}`" target="_blank" style="color: #0284c7; text-decoration: none; font-size: 12px; font-weight: 600;">
                    Xem trang ↗
                  </router-link>
                </div>
              </td>

              <!-- CHUYÊN MỤC & TAG -->
              <td>
                <div v-if="post.category" style="margin-bottom: 4px;">
                  <span class="badge" style="background: #e0f2fe; color: #0369a1; border: 1px solid #bae6fd; font-size: 11.5px; font-weight: 700;">
                    {{ post.category }}
                  </span>
                </div>
                <div v-if="post.tag">
                  <span class="badge" style="background: #fef3c7; color: #b45309; border: 1px solid #fde68a; font-size: 11px; font-weight: 600;">
                    {{ post.tag }}
                  </span>
                </div>
              </td>

              <!-- ĐIỂM NỔI BẬT -->
              <td>
                <ul style="margin: 0; padding-left: 16px; font-size: 12px; color: #475569; line-height: 1.4;">
                  <li v-for="(h, hIdx) in getHighlightsList(post)" :key="hIdx">
                    {{ h }}
                  </li>
                </ul>
              </td>

              <!-- TRẠNG THÁI -->
              <td style="text-align: center;">
                <button 
                  type="button" 
                  @click="toggleActive(post)"
                  class="btn btn-sm"
                  :style="post.is_active 
                    ? 'background: #dcfce7; color: #15803d; border: 1px solid #bbf7d0; font-weight: 600; font-size: 12px; padding: 4px 10px; border-radius: 6px;' 
                    : 'background: #fee2e2; color: #b91c1c; border: 1px solid #fecaca; font-weight: 600; font-size: 12px; padding: 4px 10px; border-radius: 6px;'"
                  title="Nhấn để đổi trạng thái"
                >
                  {{ post.is_active ? '✓ Hiển thị' : '✕ Đang ẩn' }}
                </button>
              </td>

              <!-- HÀNH ĐỘNG -->
              <td data-label="Hành động">
                <div class="action-buttons" style="justify-content: center;">
                  <button @click="openEditModal(post)" class="btn-action edit" title="Sửa bài viết">✏️</button>
                  <button @click="confirmDelete(post)" class="btn-action delete" title="Xóa bài viết">🗑️</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- VIEW 2: ADD / EDIT MODAL (CLEAN 2-COLUMN LAYOUT) -->
    <div v-if="isModalOpen" class="admin-modal-overlay" @click.self="closeModal">
      <div class="admin-modal-card" style="max-width: 900px; width: 95%; max-height: 92vh; overflow-y: auto; padding: 22px 26px;">
        <div class="modal-header flex-between" style="border-bottom: 1px solid #e2e8f0; padding-bottom: 12px; margin-bottom: 16px;">
          <h3 style="font-size: 18px; font-weight: 700; color: #0f172a; margin: 0;">
            {{ isEditing ? '✏️ Chỉnh sửa Bài viết Tuyển sinh' : '➕ Thêm Bài viết Tuyển sinh mới' }}
          </h3>
          <button @click="closeModal" class="btn btn-sm btn-secondary" style="border: none; background: transparent; font-size: 18px; cursor: pointer; padding: 0 4px;">✕</button>
        </div>

        <form @submit.prevent="savePost">
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 18px;">
            <!-- CỘT TRÁI: THÔNG TIN BÀI VIẾT -->
            <div style="display: flex; flex-direction: column; gap: 12px;">
              <!-- TIÊU ĐỀ -->
              <div>
                <label style="display: block; font-weight: 600; font-size: 13px; color: #1e293b; margin-bottom: 3px;">Tiêu đề Bài viết Tuyển sinh *</label>
                <input 
                  v-model="form.title" 
                  @input="onTitleInput"
                  type="text" 
                  required 
                  class="admin-input-style" 
                  placeholder="VD: MBA Andrews Hoa Kỳ: Học quản trị theo chuẩn Mỹ..." 
                  style="width: 100%; padding: 8px 10px; font-size: 13.5px; border: 1px solid #cbd5e1; border-radius: 6px;"
                />
              </div>

              <!-- SLUG & THỨ TỰ -->
              <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 10px;">
                <div>
                  <label style="display: block; font-weight: 600; font-size: 13px; color: #1e293b; margin-bottom: 3px;">Đường dẫn tĩnh (Slug) *</label>
                  <input 
                    v-model="form.slug" 
                    type="text" 
                    required 
                    class="admin-input-style" 
                    placeholder="VD: mba, mini-mba, gei..." 
                    style="width: 100%; padding: 8px 10px; font-size: 13px; font-family: monospace; border: 1px solid #cbd5e1; border-radius: 6px;"
                  />
                </div>
                <div>
                  <label style="display: block; font-weight: 600; font-size: 13px; color: #1e293b; margin-bottom: 3px;">Thứ tự *</label>
                  <input 
                    v-model.number="form.position" 
                    type="number" 
                    min="1"
                    required 
                    class="admin-input-style" 
                    style="width: 100%; padding: 8px 10px; font-size: 13.5px; border: 1px solid #cbd5e1; border-radius: 6px;"
                  />
                </div>
              </div>

              <!-- CHUYÊN MỤC & NHÃN TAG -->
              <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <div>
                  <label style="display: block; font-weight: 600; font-size: 13px; color: #1e293b; margin-bottom: 3px;">Chuyên mục tuyển sinh</label>
                  <input 
                    v-model="form.category" 
                    type="text" 
                    class="admin-input-style" 
                    placeholder="VD: BẰNG QUỐC TẾ HOA KỲ" 
                    style="width: 100%; padding: 8px 10px; font-size: 13px; border: 1px solid #cbd5e1; border-radius: 6px;"
                  />
                </div>
                <div>
                  <label style="display: block; font-weight: 600; font-size: 13px; color: #1e293b; margin-bottom: 3px;">Nhãn Badge (Tag)</label>
                  <input 
                    v-model="form.tag" 
                    type="text" 
                    class="admin-input-style" 
                    placeholder="VD: Đại học Andrews Hoa Kỳ" 
                    style="width: 100%; padding: 8px 10px; font-size: 13px; border: 1px solid #cbd5e1; border-radius: 6px;"
                  />
                </div>
              </div>

              <!-- ẢNH BÌA & CẮT ẢNH -->
              <div>
                <label style="display: block; font-weight: 600; font-size: 13px; color: #1e293b; margin-bottom: 4px;">Ảnh bìa bài viết</label>
                <div style="display: flex; gap: 10px; align-items: center;">
                  <div 
                    @click="$refs.coverFileRef.click()"
                    style="width: 80px; height: 50px; border-radius: 6px; overflow: hidden; background: #f8fafc; border: 1px dashed #cbd5e1; cursor: pointer; display: flex; align-items: center; justify-content: center; flex-shrink: 0;"
                    title="Nhấn để chọn và cắt ảnh"
                  >
                    <img v-if="form.image" :src="form.image" alt="Preview" style="width: 100%; height: 100%; object-fit: cover;" @error="(e) => e.target.src = '/images/andrew.jpg'" />
                    <span v-else style="font-size: 16px;">📷</span>
                  </div>
                  <input type="file" ref="coverFileRef" @change="onFileSelectForCrop($event, (url) => { form.image = url; }, 'wide', '✂ Cắt & Căn Chỉnh Ảnh Bìa Tuyển Sinh')" style="display: none;" accept="image/*" />
                  <input 
                    v-model="form.image" 
                    type="text" 
                    class="admin-input-style" 
                    placeholder="/images/... hoặc URL ảnh" 
                    style="flex: 1; padding: 7px 10px; font-size: 12.5px; border: 1px solid #cbd5e1; border-radius: 6px;"
                  />
                  <button type="button" @click="$refs.coverFileRef.click()" class="btn btn-secondary btn-sm" style="font-size: 11px; padding: 6px 10px; white-space: nowrap;">
                    Tải lên
                  </button>
                  <button 
                    v-if="form.image"
                    type="button" 
                    @click="openCropper(form.image, (url) => { form.image = url; }, 'wide', '✂ Cắt & Căn Chỉnh Ảnh Bìa')"
                    class="btn btn-secondary btn-sm" 
                    style="font-size: 11px; padding: 6px 10px; color: #0284c7; border-color: #bae6fd; white-space: nowrap;"
                  >
                    ✂ Cắt
                  </button>
                </div>
              </div>

              <!-- MÔ TẢ PHỤ ĐỀ -->
              <div>
                <label style="display: block; font-weight: 600; font-size: 13px; color: #1e293b; margin-bottom: 3px;">Mô tả ngắn / Phụ đề</label>
                <textarea 
                  v-model="form.subtitle" 
                  rows="3" 
                  class="admin-input-style" 
                  placeholder="Mô tả tóm tắt chương trình hiển thị ở thẻ danh sách..." 
                  style="width: 100%; padding: 8px 10px; font-size: 13px; border: 1px solid #cbd5e1; border-radius: 6px; line-height: 1.45;"
                ></textarea>
              </div>

              <!-- ĐIỂM NỔI BẬT (HIGHLIGHTS) -->
              <div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 3px;">
                  <label style="font-weight: 600; font-size: 13px; color: #1e293b; margin: 0;">Điểm nổi bật (mỗi dòng 1 gạch đầu dòng)</label>
                  <span style="font-size: 11px; color: #64748b;">(Hiển thị ở card danh sách)</span>
                </div>
                <textarea 
                  v-model="form.highlights_text" 
                  rows="3" 
                  class="admin-input-style" 
                  placeholder="Bằng Thạc sĩ do ĐH Andrews (Hoa Kỳ) trực tiếp cấp&#10;Được Bộ Giáo dục & Đào tạo Việt Nam công nhận&#10;Lịch học cuối tuần linh hoạt" 
                  style="width: 100%; padding: 8px 10px; font-size: 12.5px; border: 1px solid #cbd5e1; border-radius: 6px; line-height: 1.45;"
                ></textarea>
              </div>

              <!-- KÍCH HOẠT HIỂN THỊ -->
              <label style="display: flex; align-items: center; gap: 8px; cursor: pointer; font-size: 13px; font-weight: 600; color: #1e293b;">
                <input v-model="form.is_active" type="checkbox" style="width: 16px; height: 16px; accent-color: #2563eb;" />
                <span>Hiển thị công khai bài viết trên trang Tuyển sinh</span>
              </label>
            </div>

            <!-- CỘT PHẢI: NỘI DUNG CHI TIẾT BÀI VIẾT (HTML) -->
            <div style="display: flex; flex-direction: column;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                <label style="font-weight: 600; font-size: 13px; color: #1e293b; margin: 0;">Nội dung chi tiết bài viết (HTML)</label>
                <span style="font-size: 11.5px; color: #64748b;">Hỗ trợ thẻ &lt;h2&gt;, &lt;p&gt;, &lt;ul&gt;&lt;li&gt;</span>
              </div>
              <textarea 
                v-model="form.content" 
                rows="18" 
                class="admin-input-style" 
                placeholder="<h2>1. Giới thiệu chương trình</h2>&#10;<p>Nội dung chi tiết giới thiệu về chương trình tuyển sinh...</p>&#10;&#10;<h2>2. Điều kiện tuyển sinh</h2>&#10;<ul>&#10;  <li>Tốt nghiệp Đại học</li>&#10;  <li>Tiếng Anh tương đương IELTS 5.5</li>&#10;</ul>" 
                style="flex: 1; min-height: 380px; width: 100%; padding: 10px 12px; font-size: 13px; font-family: Consolas, monospace; border: 1px solid #cbd5e1; border-radius: 6px; line-height: 1.5; resize: none;"
              ></textarea>
            </div>
          </div>

          <!-- Footer -->
          <div class="modal-footer" style="display: flex; justify-content: flex-end; gap: 10px; margin-top: 18px; border-top: 1px solid #e2e8f0; padding-top: 14px;">
            <button type="button" @click="closeModal" class="btn btn-secondary btn-sm" style="padding: 7px 16px;">Hủy bỏ</button>
            <button type="submit" class="btn btn-primary btn-sm" :disabled="saving" style="padding: 7px 20px; font-weight: 600;">
              {{ saving ? 'Đang lưu...' : (isEditing ? 'Lưu thay đổi' : 'Thêm bài viết') }}
            </button>
          </div>
        </form>
      </div>
    </div>

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
import ImageCropperModal from '@/components/ImageCropperModal.vue';

const courseStore = useCourseStore();

const activeView = ref('list');
const isRefreshing = ref(false);
const isModalOpen = ref(false);
const isEditing = ref(false);
const editingId = ref(null);
const saving = ref(false);
const coverFileRef = ref(null);

// Cropper States
const isCropperOpen = ref(false);
const cropTargetUrl = ref('');
const cropAspectRatio = ref('wide');
const cropModalTitle = ref('✂ Cắt & Căn Chỉnh Ảnh Bìa Tuyển Sinh');
let cropTargetCallback = null;

const openCropper = (url, callback, ratio = 'wide', title = '✂ Cắt & Căn Chỉnh Ảnh Bìa Tuyển Sinh') => {
  if (!url) return;
  cropTargetUrl.value = url;
  cropAspectRatio.value = ratio;
  cropModalTitle.value = title;
  cropTargetCallback = callback;
  isCropperOpen.value = true;
};

const onFileSelectForCrop = (event, callback, ratio = 'wide', title = '✂ Cắt & Căn Chỉnh Ảnh Bìa Tuyển Sinh') => {
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

const searchQuery = ref('');
const filterStatus = ref('all');

const form = ref({
  title: '',
  slug: '',
  subtitle: '',
  category: '',
  tag: '',
  image: '',
  position: 1,
  is_active: true,
  highlights_text: '',
  content: ''
});

// Always sort by position ascending
const admissions = computed(() => {
  const list = [...(courseStore.adminAdmissions || [])];
  return list.sort((a, b) => (Number(a.position) || 0) - (Number(b.position) || 0));
});

const filteredAdmissions = computed(() => {
  return admissions.value.filter(p => {
    // Status filter
    if (filterStatus.value === 'active' && !p.is_active) return false;
    if (filterStatus.value === 'hidden' && p.is_active) return false;
    // Search query
    if (searchQuery.value.trim()) {
      const q = searchQuery.value.toLowerCase();
      const matchTitle = p.title?.toLowerCase().includes(q);
      const matchSlug = p.slug?.toLowerCase().includes(q);
      const matchCat = p.category?.toLowerCase().includes(q);
      const matchTag = p.tag?.toLowerCase().includes(q);
      if (!matchTitle && !matchSlug && !matchCat && !matchTag) return false;
    }
    return true;
  });
});

const getHighlightsList = (post) => {
  if (Array.isArray(post.highlights)) return post.highlights;
  if (typeof post.highlights === 'string') {
    try {
      const parsed = JSON.parse(post.highlights);
      if (Array.isArray(parsed)) return parsed;
    } catch {
      return post.highlights.split('\n').map(s => s.trim()).filter(Boolean);
    }
  }
  return [];
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

const onTitleInput = () => {
  if (!isEditing.value && !form.value.slug) {
    form.value.slug = slugify(form.value.title);
  }
};

const refreshAdmissions = async () => {
  isRefreshing.value = true;
  try {
    await courseStore.fetchAdminAdmissions(true);
  } catch (err) {
    console.error('Error refreshing admissions:', err);
  } finally {
    isRefreshing.value = false;
  }
};

const openAddModal = () => {
  isEditing.value = false;
  editingId.value = null;
  const maxPos = admissions.value.reduce((max, p) => Math.max(max, Number(p.position) || 0), 0);
  form.value = {
    title: '',
    slug: '',
    subtitle: '',
    category: '',
    tag: '',
    image: '',
    position: maxPos + 1,
    is_active: true,
    highlights_text: '',
    content: ''
  };
  isModalOpen.value = true;
};

const openEditModal = (post) => {
  isEditing.value = true;
  editingId.value = post.id;
  const hlList = getHighlightsList(post);
  form.value = {
    title: post.title || '',
    slug: post.slug || '',
    subtitle: post.subtitle || '',
    category: post.category || '',
    tag: post.tag || '',
    image: post.image || '',
    position: post.position || 1,
    is_active: post.is_active !== undefined ? post.is_active : true,
    highlights_text: hlList.join('\n'),
    content: post.content || ''
  };
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
};

// Swap order with adjacent post
const moveOrder = async (post, direction) => {
  const list = [...filteredAdmissions.value];
  const idx = list.findIndex(p => p.id === post.id);
  const targetIdx = direction === 'up' ? idx - 1 : idx + 1;
  if (targetIdx < 0 || targetIdx >= list.length) return;

  const targetPost = list[targetIdx];
  const oldPos = Number(post.position) || 1;
  const targetPos = Number(targetPost.position) || 1;

  let newCurrentPos = targetPos;
  let newTargetPos = oldPos;
  if (newCurrentPos === newTargetPos) {
    newCurrentPos = direction === 'up' ? targetPos - 1 : targetPos + 1;
  }

  try {
    await Promise.all([
      courseStore.updateAdmissionPost(post.id, { position: newCurrentPos }),
      courseStore.updateAdmissionPost(targetPost.id, { position: newTargetPos })
    ]);
  } catch (err) {
    console.error('Failed to change order:', err);
  }
};

// Direct inline position input change
const onPositionChange = async (post, val) => {
  const newPos = parseInt(val, 10);
  if (isNaN(newPos) || newPos < 1 || newPos === post.position) return;
  try {
    await courseStore.updateAdmissionPost(post.id, { position: newPos });
  } catch (err) {
    console.error('Failed to update position:', err);
  }
};

const toggleActive = async (post) => {
  try {
    await courseStore.updateAdmissionPost(post.id, {
      is_active: !post.is_active
    });
  } catch (err) {
    console.error('Toggle active failed:', err);
  }
};

const confirmDelete = (post) => {
  if (confirm(`Bạn có chắc chắn muốn xóa bài viết tuyển sinh "${post.title}"?`)) {
    courseStore.deleteAdmissionPost(post.id).catch(err => {
      console.error('Delete failed:', err);
    });
  }
};

const savePost = async () => {
  saving.value = true;
  try {
    const hlArray = form.value.highlights_text
      .split('\n')
      .map(l => l.trim())
      .filter(l => l.length > 0);

    const payload = {
      title: form.value.title.trim(),
      slug: form.value.slug.trim(),
      subtitle: form.value.subtitle.trim() || null,
      category: form.value.category.trim() || null,
      tag: form.value.tag.trim() || null,
      image: form.value.image.trim() || null,
      position: Number(form.value.position) || 1,
      is_active: Boolean(form.value.is_active),
      highlights: JSON.stringify(hlArray),
      content: form.value.content || ''
    };

    if (isEditing.value && editingId.value) {
      await courseStore.updateAdmissionPost(editingId.value, payload);
    } else {
      await courseStore.createAdmissionPost(payload);
    }
    closeModal();
  } catch (err) {
    console.error('Save failed:', err);
    courseStore.showToast('Lỗi khi lưu bài viết tuyển sinh!', 'error');
  } finally {
    saving.value = false;
  }
};

onMounted(() => {
  courseStore.fetchAdminAdmissions().catch(() => {});
});
</script>

<style scoped>
.order-btn {
  background: #f1f5f9;
  border: 1px solid #cbd5e1;
  color: #475569;
  border-radius: 6px;
  width: 26px;
  height: 26px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 11px;
  transition: all 0.15s ease;
}
.order-btn:hover:not(:disabled) {
  background: #2563eb;
  color: #ffffff;
  border-color: #2563eb;
}
.order-btn:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}

.crop-mini-btn {
  position: absolute;
  bottom: -4px;
  right: -4px;
  background: #0284c7;
  color: #ffffff;
  border: 2px solid #ffffff;
  border-radius: 50%;
  width: 22px;
  height: 22px;
  font-size: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
  transition: all 0.15s ease;
}
.crop-mini-btn:hover {
  background: #0369a1;
  transform: scale(1.15);
}

.admin-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(15, 23, 42, 0.65);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 16px;
}

.admin-modal-card {
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.spin-icon {
  display: inline-block;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  100% {
    transform: rotate(360deg);
  }
}
</style>

