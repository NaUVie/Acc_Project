<template>
  <div class="course-detail-view">
    <div class="detail-container">
      <!-- Breadcrumb Nav -->
      <nav class="breadcrumb-nav" style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
        <button 
          type="button" 
          @click="goBack" 
          class="btn-detail-back" 
          style="background: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 6px; padding: 4px 10px; font-size: 13px; font-weight: 600; color: #334155; cursor: pointer; display: inline-flex; align-items: center; gap: 4px;"
          title="Quay lại vị trí trước"
        >
          <span>← Quay lại</span>
        </button>
        <span class="breadcrumb-separator" style="color: #cbd5e1;">|</span>
        <router-link to="/" class="breadcrumb-link">{{ $t('nav.home') }}</router-link>
        <span class="breadcrumb-separator">&rsaquo;</span>
        <router-link :to="course ? '/courses/category/' + (course.category || 'dao-tao-ca-nhan') : '/courses'" class="breadcrumb-link">{{ course ? getCategoryName(course.category) : 'Khóa học' }}</router-link>
        <span class="breadcrumb-separator">&rsaquo;</span>
        <span class="breadcrumb-current">{{ course?.title || 'Chi tiết khóa học' }}</span>
      </nav>

      <!-- Loading State -->
      <div v-if="loading" class="detail-loading-box">
        <div class="detail-loading-spinner"></div>
        <p class="detail-loading-text">{{ $t('common.loading') }}</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error || !course" class="detail-error-box">
        <h3>Không tìm thấy nội dung khóa học</h3>
        <p>{{ error || 'Khóa học bạn tìm kiếm không tồn tại hoặc đã bị gỡ bỏ.' }}</p>
        <router-link to="/courses" class="btn-back-courses">Xem tất cả khóa học</router-link>
      </div>

      <!-- Main Article & Registration Layout -->
      <div v-else class="course-article-grid">
        
        <!-- Left Column: Article Style Content -->
        <article class="course-article-main">
          <!-- Article Header -->
          <header class="article-header-box">
            <div class="article-badges" style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap;">
              <span 
                class="status-badge-pill" 
                :class="'badge-status-' + (course.status || 'ongoing')"
              >
                {{ course.status === 'upcoming' ? '⏳ Sắp diễn ra' : (course.status === 'completed' ? '🏁 Đã diễn ra' : '🟢 Đang diễn ra') }}
              </span>
              <span v-if="parentProgram" class="program-badge-pill">🎓 {{ parentProgram.title }}</span>
            </div>
            
            <h1 class="article-main-title">{{ course.title }}</h1>
            
            <p class="article-lead-text" v-if="plainDescription">
              {{ plainDescription }}
            </p>
<!-- 
            <div class="article-meta-row">
              <span class="meta-item">⭐ {{ course.rating || '4.9' }} ({{ course.ratingCount || 120 }} đánh giá)</span>
              <span class="meta-item">👥 {{ course.studentCount ? course.studentCount.toLocaleString() : '1,200' }}+ Học viên</span>
              <span class="meta-item">🔄 Cập nhật mới nhất</span>
            </div> -->
          </header>

          <!-- Featured Cover Image -->
          <div class="article-cover-box" v-if="course.coverImage || course.image">
            <img :src="formatImageUrl(course.coverImage || course.image, 'w1600')" :alt="course.title" class="article-cover-img" />
          </div>

          <!-- Main Article Content Body -->
          <div class="article-content-body">
            <!-- Full Description / Content -->
            <div v-if="course.description" class="rich-article-html" v-html="sanitizeHtml(course.description)"></div>

            <!-- Detailed Roadmap / Curriculum if exists -->
            <div v-if="course.customRoadmap" class="article-section-block">
              <h3 class="article-sub-heading">Lộ trình đào tạo chi tiết</h3>
              <div class="rich-article-html" v-html="sanitizeHtml(course.customRoadmap)"></div>
            </div>

            <div v-else-if="parsedCurriculum.length > 0" class="article-section-block">
              <h3 class="article-sub-heading">Nội dung bài giảng</h3>
              <div class="article-curriculum-list">
                <div v-for="(item, idx) in parsedCurriculum" :key="idx" class="article-curriculum-item">
                  <span class="item-num">{{ idx + 1 }}</span>
                  <div class="item-info">
                    <h4 class="item-title">{{ item.title || item.name || item }}</h4>
                    <span v-if="item.duration" class="item-dur">⏱️ {{ item.duration }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Requirements & Target Audience -->
            <div v-if="courseRequirements.length > 0" class="article-section-block">
              <h3 class="article-sub-heading">Đối tượng & Yêu cầu tham gia</h3>
              <ul class="article-req-list">
                <li v-for="(req, rIdx) in courseRequirements" :key="rIdx">{{ req }}</li>
              </ul>
            </div>

            <!-- Instructor Info -->
            <div v-if="courseLecturers.length > 0" class="article-section-block">
              <h3 class="article-sub-heading">{{ $t('course.lecturersHeading') }}</h3>
              <div class="article-lecturers-grid">
                <div v-for="lec in courseLecturers" :key="lec.id" class="article-lecturer-card">
                  <img :src="lec.avatar || '/images/default-avatar.jpg'" :alt="lec.name" class="lec-avatar" />
                  <div>
                    <h4 class="lec-name">{{ lec.name }}</h4>
                    <p class="lec-title">{{ lec.title }}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- End of Article Resource Action Buttons Bar (Lấy học liệu, Lấy link ảnh, Link Youtube) -->
            <div class="article-section-block course-resource-actions-wrapper">
              <h4 class="resource-block-title">Tài nguyên & Học liệu khóa học</h4>
              <p class="resource-block-desc">Sau khi đọc và tìm hiểu nội dung khóa học, học viên có thể tải học liệu, xem kho ảnh hoạt động và video bài giảng bên dưới:</p>
              <div class="course-resource-actions-bar">
                <button 
                  type="button" 
                  class="btn-course-resource btn-resource-materials" 
                  @click="handleOpenResource(course.materialsLink, 'học liệu')"
                  title="Nhấp để mở hoặc tải tài liệu học tập của khóa học"
                >
                  Lấy học liệu
                </button>

                <button 
                  type="button" 
                  class="btn-course-resource btn-resource-photos" 
                  @click="handleOpenResource(course.photosLink, 'kho ảnh')"
                  title="Nhấp để xem album / kho ảnh hoạt động của khóa học"
                >
                  Lấy link ảnh
                </button>

                <button 
                  type="button" 
                  class="btn-course-resource btn-resource-youtube" 
                  @click="handleOpenResource(course.youtubeLink, 'video YouTube')"
                  title="Nhấp để xem video bài giảng / giới thiệu trên YouTube"
                >
                  Link YouTube
                </button>
              </div>
            </div>

            <!-- Student Reviews & Testimonials Section (Nhận xét học viên - Không cần đăng nhập) -->
            <div class="article-section-block course-reviews-section">
              <div class="reviews-header flex-between" style="display: flex; justify-content: space-between; align-items: flex-start; gap: 16px; flex-wrap: wrap;">
                <div>
                  <h3 class="article-sub-heading" style="margin-bottom: 4px;">💬 Chia sẻ & Cảm nhận từ Học viên</h3>
                  <p class="text-muted" style="font-size: 14px; margin: 0;">Đánh giá thực tế từ học viên sau khi hoàn thành khóa học tại ACC Academy.</p>
                </div>
                <button 
                  type="button" 
                  class="btn btn-primary btn-sm" 
                  @click="showReviewForm = !showReviewForm"
                  style="font-weight: 700; border-radius: 8px; padding: 8px 16px; white-space: nowrap;"
                >
                  {{ showReviewForm ? '✕ Đóng form' : '✍️ Viết nhận xét' }}
                </button>
              </div>

              <!-- Form gửi cảm nhận (KHÔNG CẦN ĐĂNG NHẬP) -->
              <div v-if="showReviewForm" class="review-submit-box mt-4 animate-fade-in" style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 14px; padding: 22px;">
                <h4 style="font-size: 15px; font-weight: 700; color: #0f172a; margin: 0 0 14px 0;">Gửi cảm nhận của bạn về khóa học (Không cần đăng nhập)</h4>
                <form @submit.prevent="submitReviewNoAuth">
                  <div class="grid grid-2 gap-3" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px;">
                    <div class="form-group" style="margin: 0;">
                      <label style="font-size: 13px; font-weight: 600; color: #334155;">Họ và tên học viên <span style="color: #ef4444;">*</span></label>
                      <input v-model="studentReviewForm.name" type="text" required placeholder="Ví dụ: Nguyễn Văn An" class="admin-input-style" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
                    </div>
                    <div class="form-group" style="margin: 0;">
                      <label style="font-size: 13px; font-weight: 600; color: #334155;">Chức vụ / Đơn vị công tác (Tùy chọn)</label>
                      <input v-model="studentReviewForm.role" type="text" placeholder="Ví dụ: Trưởng phòng Vận hành • Công ty XYZ" class="admin-input-style" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
                    </div>
                  </div>

                  <div class="form-group mt-3" style="margin-top: 12px;">
                    <label style="font-size: 13px; font-weight: 600; color: #334155; display: block; margin-bottom: 4px;">Đánh giá chất lượng khóa học</label>
                    <div class="star-rating-selector" style="display: flex; gap: 6px; font-size: 26px; cursor: pointer; align-items: center;">
                      <span v-for="star in 5" :key="star" @click="studentReviewForm.rating = star" :style="{ color: star <= studentReviewForm.rating ? '#f59e0b' : '#cbd5e1' }">★</span>
                      <span style="font-size: 13px; color: #64748b; font-weight: 600; margin-left: 8px;">({{ studentReviewForm.rating }} sao)</span>
                    </div>
                  </div>

                  <div class="form-group mt-3" style="margin-top: 12px;">
                    <label style="font-size: 13px; font-weight: 600; color: #334155; display: block; margin-bottom: 4px;">Nội dung nhận xét / chia sẻ trải nghiệm <span style="color: #ef4444;">*</span></label>
                    <textarea v-model="studentReviewForm.text" rows="4" required placeholder="Chia sẻ cảm nhận của bạn về giảng viên, nội dung bài giảng, ứng dụng vào công việc thực tế..." class="admin-input-style" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;"></textarea>
                  </div>

                  <div style="display: flex; gap: 10px; align-items: center; justify-content: flex-end; margin-top: 14px;">
                    <button type="button" class="btn btn-secondary btn-sm" @click="showReviewForm = false">Hủy</button>
                    <button type="submit" class="btn btn-primary btn-sm" :disabled="submittingReview" style="padding: 8px 24px; font-weight: 700;">
                      {{ submittingReview ? 'Đang gửi...' : 'Gửi nhận xét ngay' }}
                    </button>
                  </div>
                </form>
              </div>

              <!-- Danh sách nhận xét đã được duyệt của khóa học -->
              <div class="course-reviews-list mt-4" style="margin-top: 16px;">
                <div v-if="courseTestimonials.length > 0" class="reviews-grid">
                  <div v-for="t in courseTestimonials" :key="t.id" class="review-card-item" style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 18px 20px; margin-bottom: 14px; box-shadow: 0 2px 8px rgba(0,0,0,0.03);">
                    <div class="review-card-header" style="display: flex; align-items: center; gap: 12px; margin-bottom: 10px;">
                      <img :src="formatImageUrl(t.image || t.avatar) || '/images/default-avatar.jpg'" :alt="t.name" style="width: 44px; height: 44px; border-radius: 50%; object-fit: cover; border: 1px solid #cbd5e1;" />
                      <div>
                        <h4 style="margin: 0; font-size: 15px; font-weight: 700; color: #0f172a;">{{ t.name }}</h4>
                        <p v-if="t.role || t.company" style="margin: 2px 0 0; font-size: 12.5px; color: #64748b;">{{ t.role }} <span v-if="t.company">• {{ t.company }}</span></p>
                      </div>
                      <div style="color: #f59e0b; font-size: 14px; margin-left: auto;">
                        {{ '★'.repeat(t.rating || 5) }}
                      </div>
                    </div>
                    <p style="font-size: 14px; line-height: 1.6; color: #334155; margin: 0; font-style: italic;">"{{ t.text || t.quote }}"</p>
                    <div v-if="t.createdAt" style="margin-top: 8px; font-size: 12px; color: #94a3b8;">
                      📅 {{ formatDate(t.createdAt) }}
                    </div>
                  </div>
                </div>

                <div v-else class="empty-reviews-box" style="padding: 28px; text-align: center; background: #f8fafc; border-radius: 12px; border: 1px dashed #cbd5e1;">
                  <p style="color: #64748b; margin: 0; font-size: 14px;">Chưa có nhận xét nào được hiển thị cho khóa học này. Hãy là người đầu tiên gửi chia sẻ của bạn!</p>
                </div>
              </div>
            </div>
          </div>

        </article>

        <!-- Right Side: Sticky Registration Sidebar -->
        <aside class="course-article-sidebar">
          <div class="sticky-register-card">
            <!-- Nếu đã sở hữu: Hiển thị nút Vào học ngay -->
            <router-link 
              v-if="isAlreadyEnrolled"
              :to="'/courses/' + (course.handle || course.id) + '/study'"
              class="sidebar-register-btn enrolled-study-btn" 
              style="width: 100%; box-sizing: border-box; display: flex; align-items: center; justify-content: center; gap: 8px; text-decoration: none; background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: #ffffff; font-weight: 700; margin-bottom: 12px;"
            >
              <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                <polygon points="5 3 19 12 5 21 5 3"></polygon>
              </svg>
              <span>Vào Học Ngay</span>
            </router-link>

            <!-- Nếu chưa sở hữu: Nút Đăng ký (Zalo) và Nút Liên hệ (Form liên hệ) -->
            <template v-else>
              <a 
                href="https://zalo.me/0938566700" 
                target="_blank" 
                rel="noopener noreferrer" 
                class="sidebar-register-btn sidebar-zalo-btn" 
                style="width: 100%; box-sizing: border-box; text-decoration: none; display: flex; align-items: center; justify-content: center; font-family: var(--font-sans); margin-bottom: 10px;"
              >
                Đăng Ký
              </a>

              <button 
                type="button" 
                class="sidebar-contact-btn" 
                @click="showConsultationModal = true"
                style="width: 100%; box-sizing: border-box; cursor: pointer; font-family: var(--font-sans); margin-bottom: 10px;"
              >
                Liên Hệ
              </button>
            </template>

            <a href="tel:0938566700" class="sidebar-hotline-btn">
              Hotline: 0938 566 700
            </a>

            <!-- Sidebar Related Articles Widget (Bài viết liên quan) -->
            <div v-if="relatedBlogs.length > 0" class="sidebar-related-courses-box">
              <div class="sidebar-related-header">
                <span class="related-badge">BÀI VIẾT</span>
                <h3 class="sidebar-related-title">Bài viết liên quan</h3>
              </div>

              <div class="sidebar-related-list">
                <div 
                  v-for="blog in relatedBlogs" 
                  :key="blog.id" 
                  class="sidebar-related-item"
                >
                  <router-link :to="'/blog/' + blog.handle" class="sidebar-rel-thumb-link">
                    <img 
                      :src="blog.image || '/images/Square-Cover-_1.webp'" 
                      :alt="blog.title" 
                      class="sidebar-rel-thumb" 
                      loading="lazy" 
                    />
                  </router-link>
                  <div class="sidebar-rel-info">
                    <span class="sidebar-rel-cat">{{ blog.category }}</span>
                    <h4 class="sidebar-rel-name">
                      <router-link :to="'/blog/' + blog.handle">
                        {{ blog.title }}
                      </router-link>
                    </h4>
                    <div class="sidebar-rel-price-row" v-if="blog.date">
                      <span class="text-xs text-muted" style="font-size: 12px; color: #64748b;">📅 {{ blog.date }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <router-link to="/library/blog" class="sidebar-related-more-btn" style="display: flex; align-items: center; justify-content: center; gap: 8px;">
                <span>Xem tất cả bài viết</span>
                <svg class="block-arrow-glow" width="36" height="16" viewBox="0 0 52 24" fill="none">
                  <path d="M 2 7 L 34 7 L 34 2 L 50 12 L 34 22 L 34 17 L 2 17 Z" fill="#022B9F" />
                </svg>
              </router-link>
            </div>
          </div>
        </aside>

      </div>
    </div>

    <!-- Consultation Registration Modal -->
    <Transition name="fade">
      <div v-if="showConsultationModal" class="consultation-modal-overlay" @click.self="showConsultationModal = false">
        <div class="consultation-modal-card">
          <div class="modal-card-header">
            <div>
              <h3 class="modal-card-title">Liên Hệ Tư Vấn Khóa Học</h3>
              <p class="modal-card-subtitle" v-if="course">{{ course.title }}</p>
            </div>
            <button type="button" class="modal-close-btn" @click="showConsultationModal = false" aria-label="Đóng">&times;</button>
          </div>

          <form @submit.prevent="submitConsultationForm" class="modal-card-body">
            <div class="form-group" style="margin-bottom: 14px;">
              <label style="font-size: 13px; font-weight: 600; color: #334155; display: block; margin-bottom: 4px;">Họ và tên học viên <span style="color: #ef4444;">*</span></label>
              <input v-model="consultationForm.fullname" type="text" required placeholder="Ví dụ: Nguyễn Văn An" class="admin-input-style" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1; width: 100%;" />
            </div>

            <div class="grid grid-2 gap-3" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; margin-bottom: 14px;">
              <div class="form-group" style="margin: 0;">
                <label style="font-size: 13px; font-weight: 600; color: #334155; display: block; margin-bottom: 4px;">Số điện thoại <span style="color: #ef4444;">*</span></label>
                <input v-model="consultationForm.phone" type="tel" required placeholder="Ví dụ: 0912 345 678" class="admin-input-style" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1; width: 100%;" />
              </div>
              <div class="form-group" style="margin: 0;">
                <label style="font-size: 13px; font-weight: 600; color: #334155; display: block; margin-bottom: 4px;">Email liên hệ <span style="color: #ef4444;">*</span></label>
                <input v-model="consultationForm.email" type="email" required placeholder="Ví dụ: email@gmail.com" class="admin-input-style" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1; width: 100%;" />
              </div>
            </div>

            <div class="form-group" style="margin-bottom: 16px;">
              <label style="font-size: 13px; font-weight: 600; color: #334155; display: block; margin-bottom: 4px;">Nhu cầu tư vấn / Lời nhắn</label>
              <textarea v-model="consultationForm.message" rows="3" placeholder="Ví dụ: Tôi muốn tìm hiểu chi tiết lịch học, chính sách ưu đãi..." class="admin-input-style" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1; width: 100%;"></textarea>
            </div>

            <div class="modal-actions-row" style="display: flex; gap: 10px; justify-content: flex-end; align-items: center;">
              <button type="button" class="btn btn-secondary btn-sm" @click="showConsultationModal = false">Hủy</button>
              <button type="submit" class="btn btn-primary btn-sm" :disabled="submittingConsultation" style="font-weight: 700; padding: 9px 24px;">
                {{ submittingConsultation ? 'Đang gửi...' : 'Gửi thông tin liên hệ' }}
              </button>
            </div>

            <div class="modal-support-footer" style="margin-top: 16px; padding-top: 12px; border-top: 1px solid #e2e8f0; text-align: center; font-size: 13px; color: #64748b;">
              Hoặc kết nối trực tiếp Hotline: <a href="tel:0938566700" style="color: #022B9F; font-weight: 700;">0938 566 700</a> • <a href="https://zalo.me/0938566700" target="_blank" rel="noopener" style="color: #022B9F; font-weight: 600;">Zalo</a>
            </div>
          </form>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useCourseStore } from '@/stores/courses';
import { useTestimonialStore } from '@/stores/testimonials';
import { stripHtml } from '@/utils/stripHtml';
import { sanitizeHtml } from '@/utils/sanitize';
import { formatImageUrl } from '@/utils/imageHelper';

const route = useRoute();
const router = useRouter();

const goBack = () => {
  if (window.history.length > 1) {
    router.back();
  } else {
    router.push('/');
  }
};
const courseStore = useCourseStore();

const course = ref(null);
const loading = ref(true);

const plainDescription = computed(() => {
  if (!course.value || !course.value.description) {
    return 'Khóa học thiết kế thực chiến giúp bạn làm chủ công nghệ, x5 hiệu suất làm việc và nâng tầm sự nghiệp trong kỷ nguyên AI.';
  }
  const clean = stripHtml(course.value.description);
  return clean.length > 220 ? clean.substring(0, 220) + '...' : clean;
});

// Check if current user already enrolled in this course
const isAlreadyEnrolled = computed(() => {
  if (!course.value || !courseStore.token) return false;
  return courseStore.isEnrolled(course.value.handle) || courseStore.isEnrolled(course.value.id);
});
const error = ref(null);
const activeTab = ref('overview');

const hasDiscount = (c) => {
  if (!c) return false;
  const orig = Number(c.originalPrice || c.original_price || 0);
  const cur = Number(c.price || 0);
  return orig > cur;
};

const formatCurrency = (val) => {
  if (!val && val !== 0) return '0đ';
  return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(val);
};

const getCategoryName = (cat) => {
  if (!cat) return 'Khóa học';
  const found = courseStore.categories.find(c => c.slug === cat || c.name === cat);
  if (found) return found.name;
  switch (cat) {
    case 'dao-tao-doanh-nghiep':
    case 'ky-nang-ai':
      return 'Đào tạo cho doanh nghiệp';
    case 'dao-tao-ca-nhan':
    case 'ky-nang-mem':
    case 'ky-nang-chuyen-mon':
      return 'Đào tạo cho cá nhân';
    case 'dao-tao-co-quan-nha-nuoc':
      return 'Đào tạo cho khối cơ quan - nhà nước';
    case 'bundles':
      return 'Gói Combo';
    default:
      return cat;
  }
};

const courseRequirements = computed(() => {
  if (!course.value) return [];
  if (course.value.requirements) {
    if (Array.isArray(course.value.requirements)) return course.value.requirements;
    if (typeof course.value.requirements === 'string') {
      const trimmed = course.value.requirements.trim();
      if (trimmed.startsWith('[')) {
        try {
          const parsed = JSON.parse(trimmed);
          if (Array.isArray(parsed)) return parsed;
        } catch (e) {}
      }
      return trimmed.split('\n').map(s => s.trim()).filter(Boolean);
    }
  }

  return [
    'Dành cho Quản lý, Chuyên viên, Freelancer và bất kỳ ai muốn nâng cao năng lực thời AI.',
    'Không yêu cầu kiến thức lập trình phức tạp – bài giảng cầm tay chỉ việc từ cơ bản đến nâng cao.',
    'Chỉ cần máy tính kết nối Internet để tham gia học trực tuyến mọi lúc mọi nơi.'
  ];
});

const parentProgram = computed(() => {
  if (!course.value || !course.value.programId) return null;
  return courseStore.programs.find(p => p.id === course.value.programId);
});

const parsedCurriculum = computed(() => {
  if (!course.value) return [];
  const curr = course.value.curriculumData || course.value.curriculum;
  if (!curr) return [];
  try {
    if (typeof curr === 'string') {
      return JSON.parse(curr);
    }
    return curr;
  } catch (e) {
    return [curr];
  }
});

const showConsultationModal = ref(false);
const submittingConsultation = ref(false);
const consultationForm = ref({
  fullname: '',
  phone: '',
  email: '',
  message: ''
});

// Auto-fill user contact info if logged in
watch(() => courseStore.userMe, (u) => {
  if (u) {
    if (!consultationForm.value.fullname) consultationForm.value.fullname = u.fullname || '';
    if (!consultationForm.value.email) consultationForm.value.email = u.email || '';
    if (!consultationForm.value.phone) consultationForm.value.phone = u.phone || '';
  }
}, { immediate: true });

const submitConsultationForm = async () => {
  if (!consultationForm.value.fullname || !consultationForm.value.phone || !consultationForm.value.email) {
    courseStore.showToast('Vui lòng điền đầy đủ các thông tin bắt buộc (*)', 'warning');
    return;
  }
  submittingConsultation.value = true;
  try {
    const nameParts = consultationForm.value.fullname.trim().split(' ');
    const lastName = nameParts.length > 0 ? nameParts[nameParts.length - 1] : '';
    const firstName = nameParts.length > 1 ? nameParts[0] : consultationForm.value.fullname.trim();
    const middleName = nameParts.length > 2 ? nameParts.slice(1, -1).join(' ') : '';

    await courseStore.sendContact(
      firstName,
      middleName,
      lastName,
      consultationForm.value.email,
      consultationForm.value.phone,
      course.value?.handle || 'course-register',
      consultationForm.value.message || `Đăng ký tư vấn cho khóa học: ${course.value?.title || ''}`
    );
    courseStore.showToast('Cảm ơn bạn! Thông tin liên hệ đã được gửi thành công.', 'success');
    showConsultationModal.value = false;
    consultationForm.value.message = '';
  } catch (err) {
    courseStore.showToast(err.message || 'Gửi thông tin thất bại. Vui lòng liên hệ Hotline 0938 566 700!', 'error');
  } finally {
    submittingConsultation.value = false;
  }
};

const loadCourse = async () => {
  const handle = route.params.handle;
  if (!handle) {
    loading.value = false;
    return;
  }

  // 1. Kiểm tra ngay trong cache của Pinia store -> nếu có thì hiển thị tức thì (0ms delay)
  const cached = courseStore.courses.find(c => c.handle === handle || c.slug === handle || String(c.id) === String(handle));
  if (cached) {
    course.value = cached;
    loading.value = false;
  } else {
    loading.value = true;
  }

  error.value = null;
  try {
    const fetched = await courseStore.fetchCourseByHandle(handle);
    course.value = fetched;
  } catch (err) {
    if (!course.value) {
      error.value = err.message || 'Không thể tải thông tin khóa học.';
    }
  } finally {
    loading.value = false;
  }
};

watch(() => route.params.handle, () => {
  loadCourse().then(() => {
    loadReviews();
    loadCourseTestimonials();
  });
});



const testimonialStore = useTestimonialStore();
const courseTestimonials = ref([]);
const showReviewForm = ref(false);
const submittingReview = ref(false);

const studentReviewForm = ref({
  name: '',
  role: '',
  rating: 5,
  text: ''
});

const loadCourseTestimonials = async () => {
  if (!course.value || !course.value.id) return;
  courseTestimonials.value = await testimonialStore.fetchCourseTestimonials(course.value.id);
};

const handleOpenResource = (url, label) => {
  if (url && url.trim()) {
    window.open(url.trim(), '_blank', 'noopener,noreferrer');
  } else {
    courseStore.showToast(`Liên kết ${label} của khóa học này đang được chuẩn bị và sẽ cập nhật sớm!`, 'info');
  }
};

const submitReviewNoAuth = async () => {
  if (!studentReviewForm.value.name.trim() || !studentReviewForm.value.text.trim()) {
    courseStore.showToast('Vui lòng nhập đầy đủ họ tên và nội dung cảm nhận!', 'warning');
    return;
  }
  submittingReview.value = true;
  try {
    await testimonialStore.submitPublicTestimonial({
      name: studentReviewForm.value.name.trim(),
      role: studentReviewForm.value.role.trim(),
      rating: studentReviewForm.value.rating,
      text: studentReviewForm.value.text.trim(),
      courseId: course.value.id,
      courseName: course.value.title
    });
    courseStore.showToast('Cảm ơn bạn! Cảm nhận đã được gửi thành công và sẽ hiển thị sau khi Ban quản trị kiểm duyệt.', 'success');
    studentReviewForm.value = { name: '', role: '', rating: 5, text: '' };
    showReviewForm.value = false;
  } catch (err) {
    courseStore.showToast(err.message || 'Không thể gửi cảm nhận. Vui lòng thử lại!', 'error');
  } finally {
    submittingReview.value = false;
  }
};

const reviews = ref([]);
const newReview = ref({ rating: 5, comment: '' });

const isWishlisted = computed(() => {
  if (!course.value || !courseStore.wishlist) return false;
  return courseStore.wishlist.some(w => w.course && (w.course.id === course.value.id || w.course.handle === course.value.handle));
});

const averageRating = computed(() => {
  if (reviews.value.length === 0) return (4.8 + ((course.value?.id || 1) % 3) * 0.1).toFixed(1);
  const sum = reviews.value.reduce((acc, r) => acc + r.rating, 0);
  return (sum / reviews.value.length).toFixed(1);
});

const formatDate = (iso) => {
  if (!iso) return '';
  const d = new Date(iso);
  return d.toLocaleDateString('vi-VN');
};

const handleToggleWishlist = async () => {
  if (!course.value) return;
  await courseStore.toggleWishlist(course.value.id);
};

const loadReviews = async () => {
  const handle = course.value?.handle || route.params.handle;
  if (!handle) return;
  reviews.value = await courseStore.fetchCourseReviews(handle);
};

const submitReview = async () => {
  if (!newReview.value.comment.trim()) {
    courseStore.showToast('Vui lòng viết lời nhận xét trước khi gửi!', 'warning');
    return;
  }
  submittingReview.value = true;
  try {
    const rev = await courseStore.addCourseReview(course.value.handle, {
      rating: newReview.value.rating,
      comment: newReview.value.comment
    });
    reviews.value.unshift(rev);
    newReview.value.comment = '';
  } catch (err) {
    // handled by store toast
  } finally {
    submittingReview.value = false;
  }
};



const courseLecturers = computed(() => {
  if (!course.value || !course.value.lecturerIds) return [];
  const ids = course.value.lecturerIds.split(',').map(s => s.trim()).filter(Boolean);
  return ids.map(id => courseStore.lecturers.find(l => String(l.id) === String(id))).filter(Boolean);
});

// Bài viết liên quan: CHỈ hiển thị những bài viết được gán đúng khóa học này (qua course_id)
const relatedBlogs = computed(() => {
  if (!course.value || !courseStore.blogPosts || courseStore.blogPosts.length === 0) return [];
  const currentCourseId = Number(course.value.id);

  return courseStore.blogPosts.filter(b => b.course_id && Number(b.course_id) === currentCourseId);
});

onMounted(() => {
  loadCourse().then(() => {
    loadCourseTestimonials();
  });
  loadReviews();
  if (courseStore.courses.length === 0) {
    courseStore.fetchCourses();
  }
  if (courseStore.blogPosts.length === 0) {
    courseStore.fetchBlogs().catch(() => {});
  }
  if (courseStore.token) {
    courseStore.fetchWishlist();
    if (!courseStore.enrollments || courseStore.enrollments.length === 0) {
      courseStore.fetchEnrollments().catch(() => {});
    }
  }
  if (courseStore.programs.length === 0) {
    courseStore.fetchPrograms();
  }
  if (courseStore.lecturers.length === 0) {
    courseStore.fetchLecturers();
  }
});

</script>



<style scoped src="@/styles/views/courses/CourseDetail.css"></style>
