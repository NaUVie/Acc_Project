<template>
  <div class="tab-content animate-fade-in">
    <!-- VIEW 1: BLOGS LIST TABLE -->
    <div v-if="activeView === 'list'">
      <div class="content-header flex-between">
        <div>
          <h2>Quản lý Tin tức & Bài viết</h2>
          <p>Danh sách các bài viết chia sẻ, kiến thức AI và cập nhật xu hướng công nghệ trên toàn hệ thống.</p>
        </div>
        <div style="display: flex; gap: 8px;">
          <button @click="showCatManagerModal = true" class="btn btn-secondary btn-sm" type="button" style="display: inline-flex; align-items: center; gap: 6px;">
            <span>🏷️ Quản lý Chuyên mục</span>
          </button>
          <button @click="openAddModal" class="btn btn-primary btn-sm">+ Thêm Bài viết mới</button>
        </div>
      </div>

      <!-- Filters -->
      <div class="filter-bar flex-between mt-4 mb-4 gap-4" style="flex-wrap: wrap;">
        <div style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap;">
          <span style="font-size: 13.5px; font-weight: 600; color: #475569;">Lọc chuyên mục:</span>
          <select v-model="filterCategory" class="admin-input-style" style="min-width: 180px; padding: 6px 12px; font-size: 13.5px;">
            <option value="all">Tất cả chuyên mục ({{ blogPosts.length }})</option>
            <option v-for="cat in availableCategories" :key="cat.id || cat.name" :value="cat.name">
              {{ cat.name }} ({{ getCategoryPostCount(cat.name) }})
            </option>
          </select>
        </div>

        <div style="min-width: 280px; flex: 1; max-width: 350px;">
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="Tìm theo tiêu đề, slug hoặc chuyên mục..." 
            class="admin-search-input"
            style="width: 100%;"
          />
        </div>
      </div>

      <!-- Table -->
      <div class="table-responsive">
        <table class="admin-table">
          <thead>
            <tr>
              <th style="width: 60px;">Ảnh</th>
              <th>Tiêu đề Bài viết</th>
              <th>Chuyên mục</th>
              <th>Ngày đăng</th>
              <th style="text-align: right; width: 140px;">Hành động</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="b in paginatedBlogs" :key="b.id">
              <td>
                <img 
                  :src="b.image || '/images/default.jpg'" 
                  alt="thumb" 
                  style="width: 54px; height: 38px; object-fit: cover; border-radius: 6px; border: 1px solid #cbd5e1;"
                  referrerpolicy="no-referrer"
                />
              </td>
              <td>
                <div class="font-bold" style="color: #0f172a; font-size: 14px;">{{ b.title }}</div>
                <div style="display: flex; gap: 8px; align-items: center; margin-top: 4px;">
                  <span class="text-xs text-muted" style="font-size: 11.5px;">Slug: /blog/{{ b.handle || b.id }}</span>
                  <router-link :to="'/blog/' + (b.handle || b.id)" target="_blank" style="font-size: 11.5px; color: #0284c7; text-decoration: underline;">
                    Xem bài viết ↗
                  </router-link>
                </div>
              </td>
              <td>
                <span class="badge badge-info" style="font-size: 11.5px;">{{ b.category || 'Chung' }}</span>
              </td>
              <td>
                <div style="font-size: 13.5px; color: #64748b;">{{ b.date || '--' }}</div>
              </td>
              <td style="text-align: right;">
                <div class="action-buttons" style="justify-content: flex-end;">
                  <button @click="openQuickCropper(b)" class="btn-action edit" title="Cắt lại ảnh đại diện" style="color: #0284c7;">✂️</button>
                  <button @click="editBlog(b)" class="btn-action edit" title="Sửa">✏️</button>
                  <button @click="deleteItem(b.id)" class="btn-action delete" title="Xóa">🗑️</button>
                </div>
              </td>
            </tr>
            <tr v-if="isLoadingBlogs && filteredBlogs.length === 0">
              <td colspan="5">
                <div class="admin-center-loader" style="padding: 40px 0; min-height: 160px;">
                  <div class="admin-spinner"></div>
                  <p class="admin-loader-text">Đang nạp danh sách tin tức & bài viết...</p>
                </div>
              </td>
            </tr>
            <tr v-else-if="filteredBlogs.length === 0">
              <td colspan="5" class="text-center py-8 text-muted">Không có bài viết nào phù hợp với bộ lọc.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <Pagination 
        :currentPage="currentPage" 
        :totalItems="filteredBlogs.length" 
        :pageSize="pageSize" 
        @update:currentPage="currentPage = $event"
      />
    </div>

    <!-- VIEW 2: FORM ADD/EDIT (Extracted Component) -->
    <BlogFormView 
      v-else-if="activeView === 'form'"
      :initialData="editingBlog"
      :availableCategories="availableCategories"
      @cancel="activeView = 'list'"
      @saved="onBlogSaved"
      @open-category-modal="showCatManagerModal = true"
    />

    <!-- Blog Categories Manager Modal (Extracted Component) -->
    <BlogCategoryModal 
      :isOpen="showCatManagerModal"
      :categories="availableCategories"
      @close="showCatManagerModal = false"
      @updated="courseStore.fetchBlogCategories(true)"
    />

    <!-- Quick Image Cropper Modal for table row -->
    <ImageCropperModal 
      :isOpen="isCropperOpen" 
      :imageUrl="cropTargetUrl" 
      :aspectRatio="'wide'" 
      :title="cropModalTitle" 
      @close="isCropperOpen = false" 
      @cropped="handleQuickCropped" 
    />
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useCourseStore } from '@/stores/courses';
import Pagination from '@/components/Pagination.vue';
import ImageCropperModal from '@/components/ImageCropperModal.vue';
import BlogCategoryModal from '../modals/BlogCategoryModal.vue';
import BlogFormView from '../modals/BlogFormView.vue';

const courseStore = useCourseStore();

const activeView = ref('list');
const editingBlog = ref(null);
const showCatManagerModal = ref(false);

const filterCategory = ref('all');
const searchQuery = ref('');
const currentPage = ref(1);
const pageSize = ref(8);
const isLoadingBlogs = ref(courseStore.adminBlogPosts.length === 0 && courseStore.blogPosts.length === 0);

// Quick Cropper for Table
const isCropperOpen = ref(false);
const cropTargetUrl = ref('');
const cropModalTitle = ref('✂ Cắt Thumbnail Bài Viết');
let quickCropTargetBlog = null;

const blogPosts = computed(() => {
  return courseStore.adminBlogPosts.length > 0 ? courseStore.adminBlogPosts : courseStore.blogPosts;
});

const availableCategories = computed(() => {
  const storeCats = courseStore.blogCategories || [];
  if (storeCats.length > 0) return storeCats;
  
  const distinctNames = new Set();
  blogPosts.value.forEach(b => {
    if (b.category) distinctNames.add(b.category);
  });
  if (distinctNames.size === 0) {
    ['AI 2026', 'AI Automation', 'Công cụ AI', 'Làm việc hiệu suất', 'Lãnh đạo & Quản lý'].forEach(n => distinctNames.add(n));
  }
  return Array.from(distinctNames).map((name, idx) => ({ id: idx + 1, name, slug: name.toLowerCase().replace(/\s+/g, '-'), post_count: 0 }));
});

const getCategoryPostCount = (catName) => {
  return blogPosts.value.filter(b => b.category === catName).length;
};

const filteredBlogs = computed(() => {
  return blogPosts.value.filter(b => {
    if (filterCategory.value !== 'all' && b.category !== filterCategory.value) return false;
    if (searchQuery.value.trim()) {
      const q = searchQuery.value.toLowerCase().trim();
      const matchTitle = b.title && b.title.toLowerCase().includes(q);
      const matchCategory = b.category && b.category.toLowerCase().includes(q);
      const matchSlug = (b.handle || b.id) && (b.handle || b.id).toLowerCase().includes(q);
      return matchTitle || matchCategory || matchSlug;
    }
    return true;
  });
});

const paginatedBlogs = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  return filteredBlogs.value.slice(start, start + pageSize.value);
});

watch([filterCategory, searchQuery], () => {
  currentPage.value = 1;
});

const openAddModal = () => {
  editingBlog.value = null;
  activeView.value = 'form';
};

const editBlog = (b) => {
  editingBlog.value = b;
  activeView.value = 'form';
};

const onBlogSaved = () => {
  activeView.value = 'list';
  courseStore.fetchAdminBlogPosts();
};

const openQuickCropper = (b) => {
  quickCropTargetBlog = b;
  cropTargetUrl.value = b.image || '/images/default.jpg';
  cropModalTitle.value = `✂ Cắt Thumbnail: ${b.title}`;
  isCropperOpen.value = true;
};

const handleQuickCropped = async (newUrl) => {
  isCropperOpen.value = false;
  if (quickCropTargetBlog) {
    await courseStore.updateAdminBlogPost(quickCropTargetBlog.id, {
      ...quickCropTargetBlog,
      image: newUrl
    });
    quickCropTargetBlog.image = newUrl;
    courseStore.showToast('Đã cắt và cập nhật ảnh đại diện bài viết!', 'success');
    quickCropTargetBlog = null;
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

onMounted(async () => {
  try {
    await Promise.all([
      courseStore.fetchAdminBlogPosts(),
      courseStore.fetchBlogCategories()
    ]);
  } catch (err) {
    console.error("Error loading blog posts:", err);
  } finally {
    isLoadingBlogs.value = false;
  }
});
</script>
