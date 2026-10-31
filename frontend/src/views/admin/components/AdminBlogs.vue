<template>
  <div class="tab-content animate-fade-in">
    <!-- VIEW 1: LIST TABLE -->
    <div v-if="activeView === 'list'">
      <div class="content-header flex-between">
        <div>
          <h2>Quản lý Tin tức & Bài viết</h2>
          <p>Tạo, chỉnh sửa và đăng tải tin tức, kiến thức AI, chuyển đổi số và xu hướng công nghệ.</p>
        </div>
        <div style="display: flex; gap: 10px;">
          <button @click="openCategoryModal" class="btn btn-secondary btn-sm" type="button" style="display: inline-flex; align-items: center; gap: 6px;">
            🏷️ Quản lý Chuyên mục
          </button>
          <button @click="openAddModal" class="btn btn-primary btn-sm">+ Thêm Bài viết mới</button>
        </div>
      </div>

      <!-- Filters & Search -->
      <div class="flex-between mt-4 mb-4 gap-4" style="flex-wrap: wrap;">
        <div class="filter-tabs" style="display: flex; gap: 8px; margin: 0; flex-wrap: wrap;">
          <button 
            @click="filterCategory = 'all'" 
            class="btn btn-sm"
            :class="filterCategory === 'all' ? 'btn-primary' : 'btn-secondary'"
          >
            Tất cả ({{ blogPosts.length }})
          </button>
          <button 
            v-for="cat in availableCategories" 
            :key="cat.id || cat.name"
            @click="filterCategory = cat.name" 
            class="btn btn-sm"
            :class="filterCategory === cat.name ? 'btn-primary' : 'btn-secondary'"
          >
            {{ cat.name }}
            <span v-if="cat.post_count !== undefined" style="opacity: 0.7; font-size: 11px; margin-left: 2px;">({{ cat.post_count }})</span>
          </button>
        </div>

        <div style="position: relative; min-width: 260px;">
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="Tìm bài viết, tiêu đề..." 
            class="admin-input-style"
            style="padding-left: 14px; background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;"
          />
        </div>
      </div>

      <!-- Blogs Table -->
      <div class="table-responsive">
        <table class="admin-table">
          <thead>
            <tr>
              <th style="width: 100px;">Ảnh bìa</th>
              <th>Tiêu đề bài viết</th>
              <th>Chuyên mục</th>
              <th>Ngày đăng</th>
              <th>Đường dẫn tĩnh (Slug)</th>
              <th style="width: 110px;">Hành động</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="isLoadingBlogs && filteredBlogs.length === 0">
              <td colspan="6">
                <div class="admin-center-loader" style="padding: 40px 0; min-height: 160px;">
                  <div class="admin-spinner"></div>
                  <p class="admin-loader-text">Đang nạp danh sách bài viết...</p>
                </div>
              </td>
            </tr>
            <tr v-else-if="filteredBlogs.length === 0 && !isLoadingBlogs">
              <td colspan="6" class="text-center py-8 text-muted">
                Không tìm thấy bài viết nào.
              </td>
            </tr>
            <tr v-else v-for="b in paginatedBlogs" :key="b.id">
              <td>
                <img 
                  :src="b.image || 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=400&auto=format&fit=crop'" 
                  :alt="b.title" 
                  style="width: 90px; height: 55px; object-fit: cover; border-radius: 8px; border: 1px solid #cbd5e1;" 
                  referrerpolicy="no-referrer"
                />
              </td>
              <td>
                <div class="font-bold" style="color: #0f172a; font-size: 15px;">{{ b.title }}</div>
                <small class="text-muted" style="display: block; margin-top: 2px; color: #64748b; font-size: 12px;">
                  {{ b.excerpt ? (b.excerpt.substring(0, 75) + '...') : '' }}
                </small>
              </td>
              <td>
                <span class="badge" style="background: rgba(2, 43, 159, 0.08); color: #022b9f; font-weight: 700;">
                  {{ b.category }}
                </span>
              </td>
              <td>
                <span class="text-muted" style="font-weight: 600; font-size: 13px;">{{ b.date || 'N/A' }}</span>
              </td>
              <td>
                <code style="font-size: 12px; color: #0284c7; background: #f0f9ff; padding: 2px 6px; border-radius: 4px;">{{ b.handle }}</code>
              </td>
              <td>
                <div class="action-buttons">
                  <button @click="openCropper(b.image, async (url) => { await courseStore.updateBlog(b.id, { image: url }); b.image = url; courseStore.showToast('Đã cắt và cập nhật ảnh bài viết!', 'success'); }, 'wide', '✂ Cắt Thumbnail: ' + b.title)" class="btn-action edit" title="Cắt lại ảnh Thumbnail" style="color: #0284c7;">✂️</button>
                  <button @click="editBlog(b)" class="btn-action edit" title="Sửa bài viết">✏️</button>
                  <button @click="deleteItem(b.id)" class="btn-action delete" title="Xóa bài viết">🗑️</button>
                </div>
              </td>
            </tr>

          </tbody>
        </table>
      </div>

      <!-- Pagination Component -->
      <Pagination 
        v-if="filteredBlogs.length > pageSize"
        v-model:currentPage="currentPage"
        :totalItems="filteredBlogs.length"
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
            {{ isEditing ? 'Chỉnh sửa Tin tức / Bài viết' : 'Thêm Tin tức / Bài viết mới' }}
          </h3>
        </div>
        <button type="button" @click="activeView = 'list'" class="btn btn-secondary btn-sm">Hủy</button>
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
                @click="openCategoryModal" 
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
          <button type="button" @click="activeView = 'list'" class="btn btn-secondary" style="padding: 10px 24px;">Hủy bỏ</button>
          <button type="submit" class="btn btn-primary" style="padding: 10px 24px; font-weight: 700;">
            {{ isEditing ? 'Cập nhật Bài viết' : 'Tạo Bài viết mới' }}
          </button>
        </div>
      </form>
    </div>

    <!-- Blog Categories Manager Modal -->
    <div v-if="showCatManagerModal" class="modal-overlay" @click.self="showCatManagerModal = false" style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(15, 23, 42, 0.6); display: flex; align-items: center; justify-content: center; z-index: 1050; padding: 20px;">
      <div class="modal-content animate-fade-in" style="background: #ffffff; border-radius: 16px; width: 100%; max-width: 600px; max-height: 90vh; display: flex; flex-direction: column; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2); border: 1px solid #e2e8f0; overflow: hidden;">
        <div class="modal-header" style="display: flex; justify-content: space-between; align-items: center; padding: 18px 24px; border-bottom: 1px solid #e2e8f0; background: #f8fafc;">
          <div>
            <h3 style="margin: 0; font-size: 18px; font-weight: 800; color: #0f172a;">🏷️ Quản lý Chuyên mục Bài viết</h3>
            <p style="margin: 4px 0 0; font-size: 13px; color: #64748b;">Chủ động thêm mới, đổi tên hoặc xóa các chuyên mục bài viết</p>
          </div>
          <button class="close-btn" @click="showCatManagerModal = false" style="background: none; border: none; font-size: 24px; cursor: pointer; color: #94a3b8;">&times;</button>
        </div>

        <div class="modal-body" style="padding: 20px 24px; overflow-y: auto;">
          <!-- Form Thêm / Sửa Chuyên mục -->
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px; margin-bottom: 20px;">
            <h4 style="margin: 0 0 12px 0; font-size: 14px; font-weight: 700; color: #022b9f;">
              {{ editingCatId ? '✏️ Cập nhật tên Chuyên mục' : '➕ Thêm Chuyên mục Mới' }}
            </h4>
            <div style="display: flex; gap: 8px; flex-wrap: wrap;">
              <input 
                v-model="catForm.name" 
                type="text" 
                placeholder="Tên chuyên mục (VD: Trí tuệ nhân tạo, Tự động hóa...)" 
                class="admin-input-style"
                style="flex: 2; min-width: 200px; background: #ffffff;"
                @keydown.enter.prevent="handleSaveCategory"
              />
              <button 
                type="button" 
                @click="handleSaveCategory" 
                class="btn btn-primary btn-sm"
                :disabled="!catForm.name.trim() || isSubmittingCat"
                style="white-space: nowrap; font-weight: 600;"
              >
                {{ isSubmittingCat ? 'Đang lưu...' : (editingCatId ? 'Cập nhật' : 'Thêm mới') }}
              </button>
              <button 
                v-if="editingCatId" 
                type="button" 
                @click="cancelEditCat" 
                class="btn btn-secondary btn-sm"
              >
                Hủy
              </button>
            </div>
            <small v-if="editingCatId" style="display: block; margin-top: 6px; color: #0284c7; font-size: 12px;">
              💡 Lưu ý: Khi đổi tên, toàn bộ bài viết đang thuộc chuyên mục này sẽ được tự động đồng bộ sang tên mới!
            </small>
          </div>

          <!-- Danh sách chuyên mục hiện có -->
          <div style="border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden;">
            <table class="admin-table" style="margin: 0; width: 100%;">
              <thead>
                <tr style="background: #f1f5f9;">
                  <th>Tên chuyên mục</th>
                  <th style="width: 120px; text-align: center;">Số bài viết</th>
                  <th style="width: 100px; text-align: right;">Hành động</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="availableCategories.length === 0">
                  <td colspan="3" class="text-center py-4 text-muted">Chưa có chuyên mục nào.</td>
                </tr>
                <tr v-for="cat in availableCategories" :key="cat.id || cat.name">
                  <td>
                    <div style="font-weight: 700; color: #0f172a; font-size: 14px;">{{ cat.name }}</div>
                    <code style="font-size: 11px; color: #64748b;">{{ cat.slug }}</code>
                  </td>
                  <td style="text-align: center;">
                    <span class="badge" style="background: rgba(2, 43, 159, 0.08); color: #022b9f; font-weight: 700; padding: 4px 10px; border-radius: 9999px;">
                      {{ cat.post_count || 0 }} bài
                    </span>
                  </td>
                  <td style="text-align: right;">
                    <div class="action-buttons" style="justify-content: flex-end;">
                      <button @click="startEditCat(cat)" class="btn-action edit" title="Sửa tên chuyên mục">✏️</button>
                      <button @click="handleDeleteCat(cat)" class="btn-action delete" title="Xóa chuyên mục">🗑️</button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="modal-footer" style="padding: 14px 24px; border-top: 1px solid #e2e8f0; display: flex; justify-content: flex-end; background: #f8fafc;">
          <button type="button" @click="showCatManagerModal = false" class="btn btn-secondary">Đóng</button>
        </div>
      </div>
    </div>

    <!-- Image Cropper Modal -->
    <ImageCropperModal :isOpen="isCropperOpen" :imageUrl="cropTargetUrl" :aspectRatio="cropAspectRatio" :title="cropModalTitle" @close="isCropperOpen = false" @cropped="handleCroppedImage" />
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useCourseStore } from '@/stores/courses';
import RichTextEditor from '@/components/RichTextEditor.vue';
import Pagination from '@/components/Pagination.vue';
import ImageCropperModal from '@/components/ImageCropperModal.vue';

const courseStore = useCourseStore();

// Cropper States
const isCropperOpen = ref(false);
const cropTargetUrl = ref('');
const cropAspectRatio = ref('wide');
const cropModalTitle = ref('✂ Cắt Thumbnail Bài Viết');
let cropTargetCallback = null;

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


const activeView = ref('list'); // 'list' | 'form'
const isEditing = ref(false);
const editingId = ref(null);

const filterCategory = ref('all');
const searchQuery = ref('');
const currentPage = ref(1);
const pageSize = ref(8);
const imageFileRef = ref(null);
const uploadingImage = ref(false);
const savingBlog = ref(false);
const isLoadingBlogs = ref(courseStore.adminBlogPosts.length === 0 && courseStore.blogPosts.length === 0);

// Blog Categories Management
const showCatManagerModal = ref(false);
const showQuickAddCat = ref(false);
const quickCatName = ref('');
const isSubmittingCat = ref(false);
const editingCatId = ref(null);
const catForm = ref({ name: '', slug: '', description: '' });

// Dynamically compute available categories combining store + existing posts
const availableCategories = computed(() => {
  const storeCats = courseStore.blogCategories || [];
  if (storeCats.length > 0) return storeCats;
  
  // Fallback to distinct categories in blog posts if store hasn't populated yet
  const distinctNames = new Set();
  blogPosts.value.forEach(b => {
    if (b.category) distinctNames.add(b.category);
  });
  if (distinctNames.size === 0) {
    ['AI 2026', 'AI Automation', 'Công cụ AI', 'Làm việc hiệu suất', 'Lãnh đạo & Quản lý'].forEach(n => distinctNames.add(n));
  }
  return Array.from(distinctNames).map((name, idx) => ({ id: idx + 1, name, slug: name.toLowerCase().replace(/\s+/g, '-'), post_count: 0 }));
});

const openCategoryModal = () => {
  editingCatId.value = null;
  catForm.value = { name: '', slug: '', description: '' };
  showCatManagerModal.value = true;
};

const startEditCat = (cat) => {
  editingCatId.value = cat.id;
  catForm.value = { name: cat.name, slug: cat.slug, description: cat.description || '' };
};

const cancelEditCat = () => {
  editingCatId.value = null;
  catForm.value = { name: '', slug: '', description: '' };
};

const handleSaveCategory = async () => {
  const name = catForm.value.name.trim();
  if (!name) return;
  isSubmittingCat.value = true;
  try {
    if (editingCatId.value) {
      await courseStore.updateBlogCategory(editingCatId.value, { name });
    } else {
      await courseStore.addBlogCategory({ name });
    }
    cancelEditCat();
    await courseStore.fetchBlogCategories(true);
  } catch (err) {
    // Toast handled in store
  } finally {
    isSubmittingCat.value = false;
  }
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

const handleDeleteCat = async (cat) => {
  if (cat.post_count > 0) {
    courseStore.showToast?.(`Không thể xóa chuyên mục "${cat.name}" vì đang có ${cat.post_count} bài viết! Hãy chuyển hoặc sửa bài viết trước.`, 'warning');
    return;
  }
  const confirmed = await courseStore.showConfirm?.({
    title: 'Xóa chuyên mục bài viết',
    message: `Bạn có chắc muốn xóa chuyên mục "${cat.name}" không?`,
    confirmText: 'Xóa chuyên mục',
    cancelText: 'Hủy'
  });
  if (confirmed) {
    await courseStore.deleteBlogCategory(cat.id);
    await courseStore.fetchBlogCategories(true);
  }
};

const form = ref({
  title: '',
  handle: '',
  category: '',
  image: '',
  excerpt: '',
  date: '',
  link: '',
  content: ''
});

const blogPosts = computed(() => courseStore.adminBlogPosts.length > 0 ? courseStore.adminBlogPosts : courseStore.blogPosts);

const filteredBlogs = computed(() => {
  return blogPosts.value.filter(b => {
    const matchCategory = filterCategory.value === 'all' || b.category === filterCategory.value;
    const q = (searchQuery.value || '').toLowerCase().trim();
    const matchQuery = !q || (b.title && b.title.toLowerCase().includes(q)) || 
                       (b.excerpt && b.excerpt.toLowerCase().includes(q)) ||
                       (b.handle && b.handle.toLowerCase().includes(q));
    return matchCategory && matchQuery;
  });
});

const paginatedBlogs = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  return filteredBlogs.value.slice(start, start + pageSize.value);
});

watch([filterCategory, searchQuery], () => {
  currentPage.value = 1;
});

onMounted(async () => {
  if (blogPosts.value.length === 0) {
    isLoadingBlogs.value = true;
  }
  try {
    await Promise.allSettled([
      courseStore.fetchAdminBlogPosts(),
      courseStore.fetchBlogCategories()
    ]);
  } finally {
    isLoadingBlogs.value = false;
  }
});

const openAddModal = () => {
  isEditing.value = false;
  editingId.value = null;
  const todayStr = new Date().toLocaleDateString('vi-VN');
  const defaultCat = availableCategories.value[0]?.name || 'AI 2026';
  form.value = {
    title: '',
    handle: '',
    category: defaultCat,
    image: 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=400&auto=format&fit=crop',
    excerpt: '',
    date: todayStr,
    link: '',
    content: ''
  };
  activeView.value = 'form';
};

const editBlog = async (b) => {
  isEditing.value = true;
  editingId.value = b.id;
  form.value = {
    title: b.title || '',
    handle: b.handle || '',
    category: b.category || 'AI 2026',
    image: b.image || '',
    excerpt: b.excerpt || '',
    date: b.date || '',
    link: b.link || '',
    content: b.content || ''
  };
  activeView.value = 'form';
  // Nếu content chưa có (do API list tối ưu không trả full text), kéo nội dung chi tiết
  if (!b.content) {
    try {
      const full = await courseStore.apiRequest(`/blogs/${b.id}`);
      if (full && full.content) {
        form.value.content = full.content;
        b.content = full.content;
      }
    } catch (e) {
      console.warn("Could not fetch full blog content:", e);
    }
  }
};

const generateSlug = () => {
  if (isEditing.value && form.value.handle) return;
  if (!form.value.title) {
    form.value.handle = '';
    return;
  }
  let slug = form.value.title.toLowerCase();
  slug = slug.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  slug = slug.replace(/[đĐ]/g, 'd');
  slug = slug.replace(/([^0-9a-z-\s])/g, '');
  slug = slug.replace(/(\s+)/g, '-');
  slug = slug.replace(/-+/g, '-');
  slug = slug.replace(/^-+|-+$/g, '');
  form.value.handle = slug;
  if (!form.value.link) {
    form.value.link = `/blog/${slug}`;
  }
};

const uploadImage = async (e) => {
  const file = e.target.files[0];
  if (!file) return;

  uploadingImage.value = true;
  try {
    const url = await courseStore.uploadImage(file);
    form.value.image = url;
    courseStore.showToast('Tải ảnh đại diện thành công!', 'success');
  } catch (err) {
    console.error("Upload blog image error:", err);
    // Fallback: nếu lỗi upload server thì dùng base64
    const reader = new FileReader();
    reader.onload = (evt) => {
      form.value.image = evt.target.result;
    };
    reader.readAsDataURL(file);
    courseStore.showToast('Không thể tải ảnh lên máy chủ, đã lưu dạng base64: ' + err.message, 'warning');
  } finally {
    uploadingImage.value = false;
    e.target.value = '';
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
      await courseStore.updateAdminBlogPost(editingId.value, form.value);
    } else {
      await courseStore.addAdminBlogPost(form.value);
    }
    activeView.value = 'list';
  } catch (err) {
    console.error("Save blog post error:", err);
  } finally {
    savingBlog.value = false;
  }
};

const deleteItem = async (id) => {
  const confirmed = await courseStore.showConfirm({
    title: 'Xóa bài viết / tin tức',
    message: 'Bạn có chắc chắn muốn xóa bài viết này không? Hành động này không thể hoàn tác.',
    confirmText: 'Xóa bài viết',
    cancelText: 'Hủy'
  });
  if (confirmed) {
    await courseStore.deleteAdminBlogPost(id);
  }
};
</script>

<style scoped>
.admin-input-style {
  width: 100%;
  padding: 10px 14px;
  border-radius: 8px;
  border: 1px solid #cbd5e1;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
}
.admin-input-style:focus {
  border-color: #022b9f;
  box-shadow: 0 0 0 3px rgba(2, 43, 159, 0.1);
}
.action-buttons {
  display: flex;
  gap: 6px;
}
.btn-action {
  background: #f1f5f9;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  padding: 6px 10px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}
.btn-action:hover {
  background: #e2e8f0;
}
.btn-action.delete:hover {
  background: #ffe4e6;
  border-color: #fda4af;
}
</style>
