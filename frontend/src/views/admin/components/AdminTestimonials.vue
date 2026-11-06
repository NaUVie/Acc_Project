<template>
  <div class="tab-content animate-fade-in">
    <!-- VIEW 1: LIST TABLE -->
    <div v-if="activeView === 'list'">
      <div class="content-header flex-between">
        <div>
          <h2>Quản lý Cảm nhận & Video Feedback Học viên</h2>
          <p>Quản lý các lời nhận xét, hình ảnh thực tế và video phỏng vấn học viên trên YouTube.</p>
        </div>
        <div style="display: flex; gap: 10px; align-items: center;">
          <button @click="refreshTestimonials" :disabled="isRefreshing" class="btn btn-secondary btn-sm" style="display: flex; align-items: center; gap: 6px; font-weight: 600;" title="Tải lại danh sách cảm nhận mới nhất">
            <span :class="{ 'spin-icon': isRefreshing }">🔄</span>
            <span>{{ isRefreshing ? 'Đang đồng bộ...' : 'Làm mới dữ liệu' }}</span>
          </button>
          <button @click="openAddModal" class="btn btn-primary btn-sm" style="white-space: nowrap; flex-shrink: 0;">+ Thêm Cảm nhận mới</button>
        </div>
      </div>

      <!-- Filters & Search -->
      <div class="flex-between mt-4 mb-4 gap-4" style="flex-wrap: wrap;">
        <div class="filter-tabs" style="display: flex; gap: 8px; margin: 0; flex-wrap: wrap;">
          <button 
            @click="filterType = 'all'" 
            class="btn btn-sm"
            :class="filterType === 'all' ? 'btn-primary' : 'btn-secondary'"
          >
            Tất cả ({{ testimonials.length }})
          </button>
          <button 
            @click="filterType = 'pending'" 
            class="btn btn-sm"
            :class="filterType === 'pending' ? 'btn-warning-active' : 'btn-secondary'"
            style="font-weight: 700;"
          >
            ⏳ Chờ duyệt ({{ pendingCount }})
          </button>
          <button 
            @click="filterType = 'approved'" 
            class="btn btn-sm"
            :class="filterType === 'approved' ? 'btn-success-active' : 'btn-secondary'"
            style="font-weight: 700;"
          >
            🟢 Đã duyệt ({{ approvedCount }})
          </button>
          <button 
            @click="filterType = 'spam'" 
            class="btn btn-sm"
            :class="filterType === 'spam' ? 'btn-danger' : 'btn-secondary'"
            style="font-weight: 700;"
            :style="filterType !== 'spam' && spamCount > 0 ? 'color: #dc2626; border-color: #fca5a5; background: #fff1f2;' : ''"
          >
            ⚠️ Nghi ngờ spam ({{ spamCount }})
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
            Ảnh & Trích dẫn ({{ photoCount }})
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

      <!-- Spam Notice & Cleanup Action Banner -->
      <div v-if="filterType === 'spam'" class="mb-4 p-3 flex-between" style="background: #fef2f2; border: 1px solid #fecaca; border-radius: 10px; flex-wrap: wrap; gap: 12px; align-items: center;">
        <div style="font-size: 13.5px; color: #991b1b; display: flex; align-items: center; gap: 8px;">
          <span style="font-size: 18px;">ℹ️</span>
          <span>Hệ thống có cơ chế tự động xóa vĩnh viễn các nhận xét rác sau <strong>30 ngày</strong>. Bạn cũng có thể chủ động dọn dẹp ngay bây giờ.</span>
        </div>
        <button 
          v-if="spamCount > 0"
          type="button" 
          class="btn btn-danger btn-sm" 
          @click="handlePurgeAllSpam" 
          :disabled="isPurgingSpam"
          style="font-weight: 700; white-space: nowrap; padding: 6px 14px;"
        >
          <span>{{ isPurgingSpam ? 'Đang dọn dẹp...' : '🗑️ Dọn sạch tất cả nhận xét rác' }}</span>
        </button>
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
              <th>Trạng thái</th>
              <th>Nội dung / Trích dẫn</th>
              <th style="width: 110px;">Hành động</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="t in paginatedTestimonials" :key="t.id">
              <td class="font-bold text-center" data-label="ID">#{{ t.id }}</td>
              <td data-label="Loại">
                <span 
                  class="badge" 
                  :style="t.testimonial_type === 'video' ? 'background: #ffe4e6; color: #be123c;' : (t.testimonial_type === 'photo' ? 'background: #e0f2fe; color: #0369a1;' : 'background: #f1f5f9; color: #475569;')"
                >
                  {{ t.testimonial_type === 'video' ? 'Video' : (t.testimonial_type === 'photo' ? 'Ảnh' : 'Trích dẫn') }}
                </span>
              </td>
              <td data-label="Preview">
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
              <td class="wrap-cell" data-label="Học viên & Chức danh">
                <div class="font-bold" style="color: #0f172a; font-size: 15px;">{{ t.name }}</div>
                <small class="text-muted" style="display: block; margin-top: 2px; color: #475569;">
                  {{ t.role || 'Học viên' }} <span v-if="t.company">• {{ t.company }}</span>
                </small>
              </td>
              <td class="wrap-cell" data-label="Khóa học">
                <span v-if="t.course_name || t.courseName" class="badge" style="background: rgba(2, 43, 159, 0.08); color: #022b9f; font-weight: 700;">
                  📚 {{ t.course_name || t.courseName }}
                </span>
                <span v-else class="text-muted" style="font-size: 12px;">(Tất cả)</span>
              </td>
              <td data-label="Trạng thái">
                <div v-if="t.testimonial_type === 'spam' || t.isSpam" style="display: flex; flex-direction: column; gap: 4px; align-items: flex-start;">
                  <span class="badge" style="background: #fef2f2; color: #dc2626; border: 1px solid #fecaca; font-weight: 800; font-size: 11.5px;">
                    ⚠️ Nghi ngờ spam
                  </span>
                  <div style="display: flex; gap: 4px; margin-top: 2px;">
                    <button 
                      type="button" 
                      @click="setStatus(t, 'approved')" 
                      class="btn btn-xs" 
                      style="padding: 2px 7px; font-size: 11px; background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; border-radius: 4px; font-weight: 600; cursor: pointer;"
                      title="Duyệt hiển thị (Không phải spam)"
                    >
                      Duyệt
                    </button>
                    <button 
                      type="button" 
                      @click="setStatus(t, 'pending')" 
                      class="btn btn-xs" 
                      style="padding: 2px 7px; font-size: 11px; background: #fef3c7; color: #b45309; border: 1px solid #fde68a; border-radius: 4px; font-weight: 600; cursor: pointer;"
                      title="Bỏ nhãn spam, chuyển sang chờ duyệt"
                    >
                      Chờ duyệt
                    </button>
                  </div>
                </div>

                <div v-else style="display: flex; align-items: center; gap: 6px; flex-wrap: wrap;">
                  <button 
                    type="button" 
                    class="badge" 
                    :style="t.isApproved ? 'background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; cursor: pointer;' : 'background: #fef3c7; color: #b45309; border: 1px solid #fde68a; cursor: pointer; font-weight: 800;'"
                    @click="toggleApproval(t)"
                    :title="t.isApproved ? 'Nhấp để ẩn cảm nhận này' : 'Nhấp để duyệt hiển thị công khai cảm nhận này'"
                  >
                    {{ t.isApproved ? '🟢 Đã duyệt' : '⏳ Chờ duyệt' }}
                  </button>
                  <button 
                    type="button" 
                    @click="setStatus(t, 'spam')" 
                    style="background: #fff1f2; border: 1px solid #fecdd3; border-radius: 4px; cursor: pointer; color: #e11d48; font-size: 11px; padding: 2px 6px; font-weight: 700;"
                    title="Đánh dấu nghi ngờ spam"
                  >
                    🚩 Spam
                  </button>
                </div>
              </td>
              <td class="wrap-cell" data-label="Nội dung / Trích dẫn">
                <div style="max-width: 280px; text-overflow: ellipsis; overflow: hidden; white-space: nowrap; font-size: 13.5px; color: #334155;">
                  "{{ t.quote || t.text || '...' }}"
                </div>
                <div style="color: #f59e0b; font-size: 12px; margin-top: 2px;">
                  {{ '★'.repeat(t.rating || 5) }}
                </div>
              </td>
              <td data-label="Hành động">
                <div class="action-buttons">
                  <button @click="editTestimonial(t)" class="btn-action edit" title="Sửa đánh giá">✏️</button>
                  <button @click="deleteItem(t.id)" class="btn-action delete" title="Xóa đánh giá">🗑️</button>
                </div>
              </td>
            </tr>
            <tr v-if="filteredTestimonials.length === 0">
              <td colspan="8" class="text-center py-8 text-muted">
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
            <label style="color: #1e293b; font-weight: 600;">Khóa học tham gia</label>
            <select v-model="form.courseId" @change="onCourseSelectChange" class="admin-input-style" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;">
              <option :value="null">-- Không gán khóa học cụ thể / Cảm nhận chung --</option>
              <option v-for="c in coursesList" :key="c.id" :value="c.id">
                {{ c.title }}
              </option>
            </select>
          </div>
        </div>

        <div class="grid grid-2 gap-4 mt-3">
          <div class="form-group">
            <label style="color: #1e293b; font-weight: 600;">Trạng thái kiểm duyệt</label>
            <select v-model="form.statusMode" class="admin-input-style" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1; font-weight: 600;">
              <option value="approved">🟢 Đã duyệt (Hiển thị công khai)</option>
              <option value="pending">⏳ Chờ duyệt (Tạm ẩn)</option>
              <option value="spam">⚠️ Nghi ngờ spam (Gắn cờ cảnh báo & Ẩn)</option>
            </select>
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

const isRefreshing = ref(false);
const refreshTestimonials = async () => {
  isRefreshing.value = true;
  try {
    await courseStore.fetchAdminTestimonials(true);
    courseStore.showToast('Đã làm mới danh sách cảm nhận học viên!', 'success');
  } catch (err) {
    courseStore.showToast('Lỗi khi làm mới: ' + (err.message || err), 'error');
  } finally {
    isRefreshing.value = false;
  }
};

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

const coursesList = computed(() => courseStore.courses || []);

const onCourseSelectChange = () => {
  if (!form.value.courseId) {
    form.value.courseName = '';
  } else {
    const found = coursesList.value.find(c => Number(c.id) === Number(form.value.courseId));
    form.value.courseName = found ? found.title : '';
  }
};

const setStatus = async (item, status) => {
  try {
    let payload = { ...item };
    if (status === 'approved') {
      payload.isApproved = true;
      payload.testimonialType = item.image ? 'photo' : (item.youtube_id || item.youtubeId ? 'video' : 'text');
    } else if (status === 'pending') {
      payload.isApproved = false;
      payload.testimonialType = item.image ? 'photo' : (item.youtube_id || item.youtubeId ? 'video' : 'text');
    } else if (status === 'spam') {
      payload.isApproved = false;
      payload.testimonialType = 'spam';
    }

    payload.courseId = item.course_id || item.courseId || null;
    payload.courseName = item.course_name || item.courseName || '';

    await courseStore.updateAdminTestimonial(item.id, payload);
    item.isApproved = payload.isApproved;
    item.testimonial_type = payload.testimonialType;
    item.testimonialType = payload.testimonialType;
    item.isSpam = payload.testimonialType === 'spam';

    const msg = status === 'approved' 
      ? 'Đã duyệt hiển thị' 
      : (status === 'spam' ? 'Đã đánh dấu nghi ngờ spam' : 'Đã chuyển về chờ duyệt');
    courseStore.showToast(`${msg} cho nhận xét của ${item.name}!`, 'success');
  } catch (err) {
    courseStore.showToast('Lỗi khi đổi trạng thái: ' + (err.message || err), 'error');
  }
};

const toggleApproval = async (item) => {
  await setStatus(item, item.isApproved ? 'pending' : 'approved');
};

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
  courseId: null,
  isApproved: true,
  statusMode: 'approved',
  testimonialType: 'video',
  youtubeId: '',
  thumbnail: '',
  videoUrl: '',
  image: '',
  rating: 5
});

const testimonials = computed(() => courseStore.adminTestimonials || []);

const spamCount = computed(() => testimonials.value.filter(t => t.testimonial_type === 'spam' || t.isSpam).length);
const videoCount = computed(() => testimonials.value.filter(t => t.testimonial_type === 'video').length);
const photoCount = computed(() => testimonials.value.filter(t => t.testimonial_type === 'photo' || t.testimonial_type === 'text').length);
const pendingCount = computed(() => testimonials.value.filter(t => t.isApproved === false && t.testimonial_type !== 'spam' && !t.isSpam).length);
const approvedCount = computed(() => testimonials.value.filter(t => t.isApproved !== false && t.testimonial_type !== 'spam' && !t.isSpam).length);

const filteredTestimonials = computed(() => {
  return testimonials.value.filter(t => {
    const isSpam = t.testimonial_type === 'spam' || t.isSpam;

    // Filter by Spam / Approval / Type
    if (filterType.value === 'spam') {
      if (!isSpam) return false;
    } else if (filterType.value === 'pending') {
      if (t.isApproved !== false || isSpam) return false;
    } else if (filterType.value === 'approved') {
      if (!t.isApproved || isSpam) return false;
    } else if (filterType.value === 'video') {
      if (t.testimonial_type !== 'video') return false;
    } else if (filterType.value === 'photo') {
      if (t.testimonial_type !== 'photo' && t.testimonial_type !== 'text') return false;
    }

    // Search Query
    if (searchQuery.value.trim()) {
      const q = searchQuery.value.toLowerCase().trim();
      const matchName = t.name && t.name.toLowerCase().includes(q);
      const matchRole = t.role && t.role.toLowerCase().includes(q);
      const matchCompany = t.company && t.company.toLowerCase().includes(q);
      const matchCourse = (t.course_name || t.courseName) && (t.course_name || t.courseName).toLowerCase().includes(q);
      const matchText = (t.quote || t.text) && (t.quote || t.text).toLowerCase().includes(q);
      return matchName || matchRole || matchCompany || matchCourse || matchText;
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
    courseId: null,
    isApproved: true,
    statusMode: 'approved',
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
  const isSpam = t.testimonial_type === 'spam' || t.isSpam;
  const statusMode = isSpam ? 'spam' : (t.isApproved ? 'approved' : 'pending');

  form.value = {
    name: t.name || '',
    role: t.role || '',
    company: t.company || '',
    text: t.text || '',
    quote: t.quote || t.text || '',
    courseName: t.course_name || t.courseName || '',
    courseId: t.course_id || t.courseId || null,
    isApproved: t.isApproved !== undefined ? t.isApproved : (t.is_approved !== false),
    statusMode,
    testimonialType: isSpam ? (t.image ? 'photo' : 'text') : (t.testimonial_type || 'text'),
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
    let resolvedType = form.value.testimonialType;
    let resolvedApproved = form.value.statusMode === 'approved';
    if (form.value.statusMode === 'spam') {
      resolvedType = 'spam';
      resolvedApproved = false;
    } else if (resolvedType === 'spam') {
      resolvedType = form.value.image ? 'photo' : (form.value.youtubeId ? 'video' : 'text');
    }

    const payload = {
      ...form.value,
      isApproved: resolvedApproved,
      testimonialType: resolvedType,
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

const isPurgingSpam = ref(false);

const handlePurgeAllSpam = async () => {
  if (spamCount.value === 0) return;
  const isConfirmed = await courseStore.showConfirm({
    title: 'Xác nhận dọn dẹp nhận xét rác',
    message: `Bạn có chắc chắn muốn xóa vĩnh viễn toàn bộ ${spamCount.value} nhận xét rác/spam đang có trong hệ thống? Thao tác này sẽ xóa hoàn toàn và không thể khôi phục.`,
    confirmText: 'Đồng ý dọn sạch',
    cancelText: 'Hủy bỏ',
    type: 'danger'
  });

  if (isConfirmed) {
    isPurgingSpam.value = true;
    try {
      await courseStore.cleanupSpamTestimonials(0);
    } catch (err) {
      console.error("Purge spam error:", err);
    } finally {
      isPurgingSpam.value = false;
    }
  }
};
</script>
