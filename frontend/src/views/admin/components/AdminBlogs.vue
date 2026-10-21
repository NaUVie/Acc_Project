<template>
  <div class="tab-content animate-fade-in">
    <!-- VIEW 1: LIST TABLE -->
    <div v-if="activeView === 'list'">
      <div class="content-header flex-between">
        <div>
          <h2>Quản lý Tin tức & Bài viết</h2>
          <p>Tạo, chỉnh sửa và đăng tải tin tức, kiến thức AI, chuyển đổi số và xu hướng công nghệ.</p>
        </div>
        <button @click="openAddModal" class="btn btn-primary btn-sm">+ Thêm Bài viết mới</button>
      </div>

      <!-- Filters & Search -->
      <div class="flex-between mt-4 mb-4 gap-4" style="flex-wrap: wrap;">
        <div class="filter-tabs" style="display: flex; gap: 8px; margin: 0; flex-wrap: wrap;">
          <button 
            v-for="cat in categories" 
            :key="cat"
            @click="filterCategory = cat" 
            class="btn btn-sm"
            :class="filterCategory === cat ? 'btn-primary' : 'btn-secondary'"
          >
            {{ cat === 'all' ? 'Tất cả (' + blogPosts.length + ')' : cat }}
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
            <tr v-for="b in paginatedBlogs" :key="b.id">
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
                  <button @click="editBlog(b)" class="btn-action edit" title="Sửa bài viết">✏️</button>
                  <button @click="deleteItem(b.id)" class="btn-action delete" title="Xóa bài viết">🗑️</button>
                </div>
              </td>
            </tr>
            <tr v-if="filteredBlogs.length === 0">
              <td colspan="6" class="text-center py-8 text-muted">
                Không tìm thấy bài viết nào.
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
            <label style="color: #1e293b; font-weight: 600;">Chuyên mục Bài viết <span style="color: #e11d48;">*</span></label>
            <select v-model="form.category" class="admin-input-style" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;">
              <option value="AI 2026">AI 2026</option>
              <option value="AI Automation">AI Automation</option>
              <option value="Công cụ AI">Công cụ AI</option>
              <option value="Làm việc hiệu suất">Làm việc hiệu suất</option>
              <option value="Lãnh đạo & Quản lý">Lãnh đạo & Quản lý</option>
            </select>
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
            <input type="file" ref="imageFileRef" @change="uploadImage" style="display: none;" accept="image/*" />
            <button type="button" @click="$refs.imageFileRef.click()" class="btn btn-secondary btn-sm">Upload</button>
          </div>
          <img v-if="form.image" :src="form.image" alt="Preview Image" style="margin-top: 8px; max-height: 120px; object-fit: cover; border-radius: 8px; border: 1px solid #cbd5e1;" referrerpolicy="no-referrer" />
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
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useCourseStore } from '@/stores/courses';
import RichTextEditor from '@/components/RichTextEditor.vue';
import Pagination from '@/components/Pagination.vue';

const courseStore = useCourseStore();

const activeView = ref('list'); // 'list' | 'form'
const isEditing = ref(false);
const editingId = ref(null);

const filterCategory = ref('all');
const searchQuery = ref('');
const currentPage = ref(1);
const pageSize = ref(8);
const imageFileRef = ref(null);

const categories = [
  'all',
  'AI 2026',
  'AI Automation',
  'Công cụ AI',
  'Làm việc hiệu suất',
  'Lãnh đạo & Quản lý'
];

const form = ref({
  title: '',
  handle: '',
  category: 'AI 2026',
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
    const q = searchQuery.value.toLowerCase();
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
  await courseStore.fetchAdminBlogPosts().catch(() => {});
});

const openAddModal = () => {
  isEditing.value = false;
  editingId.value = null;
  const todayStr = new Date().toLocaleDateString('vi-VN');
  form.value = {
    title: '',
    handle: '',
    category: 'AI 2026',
    image: 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=400&auto=format&fit=crop',
    excerpt: '',
    date: todayStr,
    link: '',
    content: ''
  };
  activeView.value = 'form';
};

const editBlog = (b) => {
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

const uploadImage = (e) => {
  const file = e.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (evt) => {
      form.value.image = evt.target.result;
    };
    reader.readAsDataURL(file);
  }
};

const saveBlog = async () => {
  if (!form.value.title || !form.value.handle) {
    courseStore.showToast('Vui lòng điền đầy đủ tiêu đề và slug đường dẫn tĩnh!', 'error');
    return;
  }

  if (!form.value.link) {
    form.value.link = `/blog/${form.value.handle}`;
  }

  try {
    if (isEditing.value) {
      await courseStore.updateAdminBlogPost(editingId.value, form.value);
    } else {
      await courseStore.addAdminBlogPost(form.value);
    }
    activeView.value = 'list';
  } catch (err) {
    console.error("Save blog post error:", err);
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
