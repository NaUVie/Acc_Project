<template>
  <div class="project-detail-page" v-if="project">
    <div class="container">
      <!-- Breadcrumb -->
      <div class="breadcrumb">
        <router-link to="/">Trang chủ</router-link>
        <span class="sep">&rsaquo;</span>
        <router-link to="/projects">Dự án Đào tạo & Tư vấn</router-link>
        <span class="sep">&rsaquo;</span>
        <span class="current">{{ project.title }}</span>
      </div>

      <!-- Main Grid Layout (Article Content + Sidebar) -->
      <div class="project-layout-grid">
        <!-- Main Content Column -->
        <main class="project-main-column">
          <!-- Article Header -->
          <div class="article-header">
            <div class="header-badges">
              <span class="category-badge" :class="project.category">
                {{ project.categoryName }}
              </span>
              <span class="publish-date">Đăng ngày {{ project.date }}</span>
              <span v-if="project.client" class="client-tag">{{ project.client }}</span>
            </div>
            <h1 class="article-title">{{ project.title }}</h1>
            <p class="article-lead">{{ project.summary }}</p>
          </div>

          <!-- Cover Image -->
          <div class="cover-wrapper" v-if="project.image">
            <img :src="project.image" :alt="project.title" class="cover-image" referrerpolicy="no-referrer" />
          </div>

          <!-- Article Content -->
          <div class="article-body">
            <div v-if="typeof project.content === 'string'" class="content-html-wrapper" v-html="sanitizeHtml(project.content)"></div>
            <template v-else-if="Array.isArray(project.content)">
              <div 
                v-for="(block, idx) in project.content" 
                :key="idx"
                class="content-block"
              >
                <div v-if="block.type === 'html'" class="content-html-wrapper" v-html="sanitizeHtml(block.text)"></div>
                <h2 v-else-if="block.type === 'heading'" class="block-heading">{{ block.text }}</h2>
                <p v-else-if="block.type === 'paragraph'" class="block-paragraph">{{ block.text }}</p>
                <ul v-else-if="block.type === 'bullets'" class="block-bullets">
                  <li v-for="(item, bIdx) in block.items" :key="bIdx">{{ item }}</li>
                </ul>
              </div>
            </template>

            <!-- Drive Profile Link Button -->
            <div v-if="project.driveProfile" class="drive-banner-box">
              <div class="drive-info">
                <h4 class="drive-title">Tài liệu & Hồ sơ Dự án (Google Drive)</h4>
                <p class="drive-desc">Bấm vào nút dưới đây để mở tài liệu chi tiết hoặc bài giới thiệu đầy đủ của dự án trên Google Drive.</p>
              </div>
              <a :href="project.driveProfile" target="_blank" rel="noopener noreferrer" class="btn-drive-full">
                <span>XEM TRÊN GOOGLE DRIVE</span>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                  <polyline points="15 3 21 3 21 9"></polyline>
                  <line x1="10" y1="14" x2="21" y2="3"></line>
                </svg>
              </a>
            </div>
          </div>

          <!-- PROJECT REVIEWS / COMMENTS SECTION -->
          <section class="project-reviews-section">
            <div class="reviews-header-block">
              <div class="reviews-header-left">
                <h3 class="reviews-heading">Nhận xét & Đánh giá của Học viên</h3>
                <p class="reviews-subheading">Chia sẻ ý kiến và trải nghiệm của bạn về dự án đào tạo này. Mọi nhận xét sẽ được hiển thị công khai sau khi được Quản trị viên duyệt.</p>
              </div>
              <div class="reviews-stat-badge" v-if="approvedReviews.length > 0">
                <span class="stat-star">★</span>
                <span class="stat-number">{{ averageRating }}</span>
                <span class="stat-count">({{ approvedReviews.length }} đánh giá)</span>
              </div>
            </div>

            <!-- Review submission form (Collapsible / Expandable) -->
            <div class="review-form-card" :class="{ 'is-expanded': isReviewFormOpen }">
              <!-- Compact collapsed state -->
              <div v-if="!isReviewFormOpen" class="review-form-trigger" @click="isReviewFormOpen = true">
                <div class="trigger-left">
                  <div class="trigger-text-wrap">
                    <span class="trigger-title">Viết nhận xét hoặc chia sẻ cảm nhận của bạn...</span>
                  </div>
                </div>
                <button type="button" class="btn-open-form">
                  <span>Viết nhận xét</span>
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                    <polyline points="6 9 12 15 18 9"></polyline>
                  </svg>
                </button>
              </div>

              <!-- Expanded full form state -->
              <div v-else class="review-form-expanded animate-fade-in">
                <div class="form-card-header">
                  <div>
                    <h4 class="form-title">Gửi nhận xét về dự án</h4>
                    <p class="form-desc">
                      Nhận xét của bạn sẽ được gửi tới Quản trị viên kiểm duyệt trước khi hiển thị trên trang.
                    </p>
                  </div>
                  <button type="button" @click="isReviewFormOpen = false" class="btn-close-form" title="Thu gọn">
                    Thu gọn
                  </button>
                </div>

                <!-- Notice after submission -->
                <div v-if="submittedSuccess" class="submission-notice-banner animate-fade-in">
                  <div>
                    <strong>Cảm ơn bạn đã gửi nhận xét!</strong>
                    <p>Ý kiến của bạn đã được ghi nhận thành công và đang chờ Quản trị viên phê duyệt để xuất hiện công khai.</p>
                  </div>
                </div>

                <form @submit.prevent="handleSubmitReview" class="review-form">
                  <div class="form-row-grid">
                    <div class="form-group">
                      <label class="form-label">Họ và tên học viên <span class="required">*</span></label>
                      <input 
                        v-model="reviewForm.authorName" 
                        type="text" 
                        class="form-control-input"
                        placeholder="VD: Nguyễn Văn A"
                        required
                      />
                    </div>
                    <div class="form-group">
                      <label class="form-label">Email liên hệ <small>(không bắt buộc)</small></label>
                      <input 
                        v-model="reviewForm.authorEmail" 
                        type="email" 
                        class="form-control-input"
                        placeholder="VD: hocvien@email.com"
                      />
                    </div>
                  </div>

                  <!-- Star Rating selector -->
                  <div class="form-group rating-select-group">
                    <label class="form-label">Đánh giá mức độ hài lòng:</label>
                    <div class="star-rating-picker">
                      <button 
                        type="button" 
                        v-for="s in 5" 
                        :key="s" 
                        class="star-btn"
                        :class="{ active: s <= reviewForm.rating }"
                        @click="reviewForm.rating = s"
                        :title="s + ' sao'"
                      >
                        ★
                      </button>
                      <span class="rating-label-text">
                        {{ ratingLabels[reviewForm.rating] || 'Tuyệt vời' }}
                      </span>
                    </div>
                  </div>

                  <div class="form-group">
                    <div style="display: flex; justify-content: space-between; align-items: baseline;">
                      <label class="form-label">Nội dung nhận xét, cảm nhận <span class="required">*</span></label>
                      <div class="char-word-counter" :class="{ 'has-error': commentWordCount < 10 && commentWordCount > 0 || commentWordCount > 300 }">
                        <span>{{ commentWordCount }}/300 từ</span>
                        <span class="sep">•</span>
                        <span>{{ commentCharCount }}/1500 ký tự</span>
                      </div>
                    </div>
                    <textarea 
                      v-model="reviewForm.comment" 
                      rows="4" 
                      maxlength="1500"
                      class="form-control-textarea"
                      placeholder="Hãy chia sẻ cảm nhận, kết quả đạt được hoặc góp ý của bạn về dự án này (Tối thiểu 10 từ, tối đa 300 từ)..."
                      required
                    ></textarea>
                    <div v-if="commentWordCount > 0 && commentWordCount < 10" class="input-hint-error">
                      Cần thêm ít nhất {{ 10 - commentWordCount }} từ nữa (hiện tại: {{ commentWordCount }}/10 từ).
                    </div>
                  </div>

                  <div class="form-actions-row">
                    <div class="status-note">
                      <span class="status-dot"></span>
                      <span>Chế độ kiểm duyệt: Đang bật</span>
                    </div>
                    <div style="display: flex; gap: 10px; align-items: center;">
                      <button type="button" @click="isReviewFormOpen = false" class="btn-cancel-form">
                        Hủy
                      </button>
                      <button type="submit" class="btn-submit-review" :disabled="submittingReview">
                        <span v-if="submittingReview" class="spinner-small"></span>
                        <span>{{ submittingReview ? 'Đang gửi...' : 'Gửi nhận xét' }}</span>
                      </button>
                    </div>
                  </div>
                </form>
              </div>
            </div>

            <!-- List of Approved Reviews -->
            <div class="reviews-list-container">
              <div v-if="loadingReviews" class="reviews-loading">
                <div class="loading-spinner-small"></div>
                <span>Đang tải nhận xét...</span>
              </div>

              <div v-else-if="approvedReviews.length === 0" class="empty-reviews-box">
                <h4>Chưa có nhận xét nào được hiển thị</h4>
                <p>Hãy là học viên đầu tiên gửi nhận xét và cảm nhận về dự án này.</p>
              </div>

              <div v-else class="reviews-cards-list">
                <article v-for="rev in paginatedReviews" :key="rev.id" class="review-item-card">
                  <div class="review-author-meta">
                    <div class="review-avatar">
                      {{ getInitials(rev.author_name) }}
                    </div>
                    <div class="review-author-info">
                      <div class="author-name-row">
                        <strong class="author-fullname">{{ rev.author_name }}</strong>
                        <span class="approved-badge">Đã xác thực</span>
                      </div>
                      <div class="review-stars-date">
                        <div class="review-stars">
                          <span v-for="s in 5" :key="s" class="star" :class="{ filled: s <= rev.rating }">★</span>
                        </div>
                        <span class="review-date">{{ formatDate(rev.created_at) }}</span>
                      </div>
                    </div>
                  </div>

                  <!-- Truncated/Expanded comment body -->
                  <div class="review-body-text" :class="{ 'is-collapsed': !expandedReviews[rev.id] && isCommentLong(rev.comment) }">
                    {{ rev.comment }}
                  </div>

                  <!-- Toggle show more / show less button if long -->
                  <div v-if="isCommentLong(rev.comment)" class="toggle-readmore-row">
                    <button type="button" @click="toggleExpandReview(rev.id)" class="btn-toggle-readmore">
                      {{ expandedReviews[rev.id] ? 'Thu gọn nhận xét' : 'Xem đầy đủ nhận xét' }}
                    </button>
                  </div>
                </article>


                <!-- Reviews Pagination -->
                <div class="mt-6 flex-center" v-if="approvedReviews.length > reviewsPageSize">
                  <Pagination 
                    :currentPage="reviewsPage" 
                    :totalItems="approvedReviews.length" 
                    :pageSize="reviewsPageSize" 
                    @update:currentPage="reviewsPage = $event"
                    @page-change="reviewsPage = $event"
                  />
                </div>
              </div>
            </div>
          </section>
        </main>


        <!-- Sidebar (Right Side: Related Projects) -->
        <aside class="project-sidebar" v-if="relatedProjects.length > 0">
          <div class="sidebar-sticky-box">
            <div class="related-sidebar-card">
              <h3 class="sidebar-title">Dự án khác</h3>
              <div class="sidebar-related-list">
                <article v-for="rel in relatedProjects" :key="rel.id" class="sidebar-related-item">
                  <router-link :to="'/projects/' + rel.id" class="sidebar-rel-link">
                    <div class="sidebar-rel-img" v-if="rel.image">
                      <img :src="rel.image" :alt="rel.title" referrerpolicy="no-referrer" />
                    </div>
                    <div class="sidebar-rel-info">
                      <span class="sidebar-rel-cat">{{ rel.categoryName }}</span>
                      <h4 class="sidebar-rel-title">{{ rel.title }}</h4>
                      <span class="sidebar-rel-date">{{ rel.date }}</span>
                    </div>
                  </router-link>
                </article>
              </div>
            </div>
          </div>
        </aside>
      </div>
    </div>
  </div>

  <div class="not-found-container" v-else>
    <div class="container text-center">
      <h2>Không tìm thấy bài viết dự án</h2>
      <p>Bài viết dự án bạn đang tìm kiếm không tồn tại hoặc đã thay đổi đường dẫn.</p>
      <router-link to="/projects" class="btn-back">Quay lại danh sách dự án</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useCourseStore } from '@/stores/courses';
import Pagination from '@/components/Pagination.vue';
import { sanitizeHtml } from '@/utils/sanitize';

const route = useRoute();
const courseStore = useCourseStore();

const project = computed(() => {
  return courseStore.projects.find(p => p.id === route.params.id);
});

const relatedProjects = computed(() => {
  if (!project.value) return [];
  return courseStore.projects
    .filter(p => p.id !== project.value.id)
    .slice(0, 3);
});

// Reviews State
const approvedReviews = ref([]);
const loadingReviews = ref(false);
const submittingReview = ref(false);
const submittedSuccess = ref(false);
const isReviewFormOpen = ref(false);

// Pagination & Truncation for User Reviews
const reviewsPage = ref(1);
const reviewsPageSize = ref(5);
const expandedReviews = ref({}); // { [id]: boolean }

const paginatedReviews = computed(() => {
  const start = (reviewsPage.value - 1) * reviewsPageSize.value;
  return approvedReviews.value.slice(start, start + reviewsPageSize.value);
});

const isCommentLong = (comment) => {
  if (!comment) return false;
  // Consider long if > 150 chars or has more than 3 line breaks
  return comment.length > 150 || (comment.match(/\n/g) || []).length >= 3;
};

const toggleExpandReview = (id) => {
  expandedReviews.value = {
    ...expandedReviews.value,
    [id]: !expandedReviews.value[id]
  };
};

const reviewForm = ref({
  authorName: '',
  authorEmail: '',
  rating: 5,
  comment: ''
});

const ratingLabels = {
  5: 'Xuất sắc ⭐⭐⭐⭐⭐',
  4: 'Rất tốt ⭐⭐⭐⭐',
  3: 'Hài lòng ⭐⭐⭐',
  2: 'Tạm được ⭐⭐',
  1: 'Cần cải thiện ⭐'
};

const averageRating = computed(() => {
  if (approvedReviews.value.length === 0) return '5.0';
  const total = approvedReviews.value.reduce((acc, r) => acc + (r.rating || 5), 0);
  return (total / approvedReviews.value.length).toFixed(1);
});

const loadReviews = async () => {
  if (!route.params.id) return;
  loadingReviews.value = true;
  try {
    const list = await courseStore.fetchProjectReviews(route.params.id);
    approvedReviews.value = Array.isArray(list) ? list : [];
  } catch (e) {
    console.error('Error fetching reviews:', e);
  } finally {
    loadingReviews.value = false;
  }
};

const commentCharCount = computed(() => {
  return (reviewForm.value.comment || '').length;
});

const commentWordCount = computed(() => {
  const text = (reviewForm.value.comment || '').trim();
  if (!text) return 0;
  return text.split(/\s+/).length;
});

const handleSubmitReview = async () => {
  const authorName = reviewForm.value.authorName.trim();
  const comment = reviewForm.value.comment.trim();

  if (!authorName) {
    courseStore.showToast('Vui lòng điền họ tên của bạn!', 'warning');
    return;
  }

  if (!comment) {
    courseStore.showToast('Vui lòng điền nội dung nhận xét!', 'warning');
    return;
  }

  if (comment.length > 1500) {
    courseStore.showToast(`Nhận xét không được vượt quá 1500 ký tự (hiện tại: ${comment.length})!`, 'warning');
    return;
  }

  const words = comment.split(/\s+/).length;
  if (words < 10) {
    courseStore.showToast(`Nhận xét cần tối thiểu 10 từ (hiện tại: ${words} từ)!`, 'warning');
    return;
  }

  if (words > 300) {
    courseStore.showToast(`Nhận xét không được vượt quá 300 từ (hiện tại: ${words} từ)!`, 'warning');
    return;
  }

  submittingReview.value = true;
  try {
    await courseStore.submitProjectReview(route.params.id, {
      author_name: authorName,
      author_email: reviewForm.value.authorEmail?.trim() || null,
      rating: reviewForm.value.rating,
      comment: comment
    });

    submittedSuccess.value = true;
    reviewForm.value.comment = '';
    reviewForm.value.rating = 5;

    // Reset success banner after 8 seconds
    setTimeout(() => {
      submittedSuccess.value = false;
    }, 8000);
  } catch (err) {
    // Error notification handled by store
  } finally {
    submittingReview.value = false;
  }
};

const getInitials = (name) => {
  if (!name) return 'HV';
  const parts = name.trim().split(' ');
  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
};

const formatDate = (dateStr) => {
  if (!dateStr) return '';
  try {
    const d = new Date(dateStr);
    return d.toLocaleDateString('vi-VN', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  } catch (e) {
    return dateStr;
  }
};

const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

onMounted(() => {
  scrollToTop();
  if (courseStore.projects.length === 0) {
    courseStore.fetchProjects();
  }
  loadReviews();
  if (courseStore.user) {
    if (!reviewForm.value.authorName) reviewForm.value.authorName = courseStore.user.fullname || '';
    if (!reviewForm.value.authorEmail) reviewForm.value.authorEmail = courseStore.user.email || '';
  }
});

watch(() => route.params.id, () => {
  scrollToTop();
  submittedSuccess.value = false;
  reviewsPage.value = 1;
  expandedReviews.value = {};
  loadReviews();
});
</script>

<style scoped src="@/styles/views/ProjectDetail.css"></style>


