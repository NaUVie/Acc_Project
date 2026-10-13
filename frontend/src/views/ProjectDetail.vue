<template>
  <div class="project-detail-page" v-if="project">
    <div class="container">
      <!-- Breadcrumb -->
      <div class="breadcrumb">
        <router-link to="/">Trang chủ</router-link>
        <span class="sep">&rsaquo;</span>
        <router-link to="/du-an">Dự án Đào tạo & Tư vấn</router-link>
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
            <div v-if="typeof project.content === 'string'" class="content-html-wrapper" v-html="project.content"></div>
            <template v-else-if="Array.isArray(project.content)">
              <div 
                v-for="(block, idx) in project.content" 
                :key="idx"
                class="content-block"
              >
                <div v-if="block.type === 'html'" class="content-html-wrapper" v-html="block.text"></div>
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
                  <router-link :to="'/du-an/' + rel.id" class="sidebar-rel-link">
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
      <router-link to="/du-an" class="btn-back">Quay lại danh sách dự án</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useCourseStore } from '@/stores/courses';
import Pagination from '@/components/Pagination.vue';

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

<style scoped>
.project-detail-page {
  padding-top: 120px;
  padding-bottom: 100px;
  background-color: #ffffff;
  min-height: 100vh;
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13.5px;
  color: #64748b;
  margin-bottom: 32px;
  flex-wrap: wrap;
}

.breadcrumb a {
  color: #022b9f;
  text-decoration: none;
  font-weight: 600;
}

.breadcrumb .sep {
  color: #94a3b8;
}

.breadcrumb .current {
  color: #1e293b;
  font-weight: 600;
}

.project-layout-grid {
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 40px;
  align-items: start;
}

@media (max-width: 992px) {
  .project-layout-grid {
    grid-template-columns: 1fr;
    gap: 32px;
  }
}

.project-main-column {
  min-width: 0;
}

.article-header {
  margin-bottom: 32px;
}

.header-badges {
  display: flex;
  align-items: center;
  gap: 14px;
  flex-wrap: wrap;
  margin-bottom: 16px;
}

.category-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 800;
  color: #ffffff;
  text-transform: uppercase;
}

.category-badge.du-an-doanh-nghiep {
  background: #022b9f;
}

.category-badge.du-an-ca-nhan {
  background: #0284c7;
}

.category-badge.du-an-nha-nuoc {
  background: #059669;
}

.publish-date, .client-tag {
  font-size: 13px;
  font-weight: 600;
  color: #64748b;
}

.article-title {
  font-size: clamp(26px, 3.5vw, 38px);
  font-weight: 800;
  color: #0f172a;
  line-height: 1.3;
  margin: 0 0 16px 0;
}

.article-lead {
  font-size: 17px;
  line-height: 1.6;
  color: #475569;
  font-weight: 500;
  margin: 0;
}

.cover-wrapper {
  width: 100%;
  max-height: 440px;
  border-radius: 16px;
  overflow: hidden;
  margin-bottom: 36px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.06);
}

.cover-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.article-body {
  width: 100%;
  margin-bottom: 40px;
}

.content-block {
  margin-bottom: 24px;
}

.block-heading {
  font-size: 22px;
  font-weight: 800;
  color: #0f172a;
  margin: 32px 0 16px 0;
  padding-bottom: 8px;
  border-bottom: 2px solid #f1f5f9;
}

.block-paragraph {
  font-size: 16px;
  line-height: 1.8;
  color: #334155;
  margin: 0;
}

.block-bullets {
  padding-left: 24px;
  margin: 0;
}

.block-bullets li {
  font-size: 16px;
  line-height: 1.8;
  color: #334155;
  margin-bottom: 8px;
}

.content-html-wrapper :deep(h2) {
  font-size: 22px;
  font-weight: 800;
  color: #0f172a;
  margin: 32px 0 16px 0;
  padding-bottom: 8px;
  border-bottom: 2px solid #f1f5f9;
}
.content-html-wrapper :deep(h3) {
  font-size: 19px;
  font-weight: 700;
  color: #0f172a;
  margin: 24px 0 12px 0;
}
.content-html-wrapper :deep(p) {
  font-size: 16px;
  line-height: 1.8;
  color: #334155;
  margin-bottom: 16px;
}
.content-html-wrapper :deep(ul), .content-html-wrapper :deep(ol) {
  padding-left: 24px;
  margin-bottom: 20px;
}
.content-html-wrapper :deep(li) {
  font-size: 16px;
  line-height: 1.8;
  color: #334155;
  margin-bottom: 8px;
}
.content-html-wrapper :deep(a) {
  color: #022b9f;
  text-decoration: underline;
  font-weight: 600;
}

.drive-banner-box {
  margin-top: 40px;
  padding: 24px;
  background: linear-gradient(135deg, #f0f4ff 0%, #e0e7ff 100%);
  border: 1.5px solid #c7d2fe;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  flex-wrap: wrap;
}

.drive-title {
  font-size: 17px;
  font-weight: 800;
  color: #1e1b4b;
  margin: 0 0 6px 0;
}

.drive-desc {
  font-size: 14px;
  color: #3730a3;
  margin: 0;
}

.btn-drive-full {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 12px 24px;
  background: #022b9f;
  color: #ffffff;
  font-weight: 700;
  font-size: 13.5px;
  border-radius: 10px;
  text-decoration: none;
  transition: background 0.2s ease;
  white-space: nowrap;
}

.btn-drive-full:hover {
  background: #1e40af;
}

/* Sidebar Styles */
.project-sidebar {
  width: 100%;
}

.sidebar-sticky-box {
  position: sticky;
  top: 100px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.related-sidebar-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 22px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
}

.sidebar-title {
  font-size: 18px;
  font-weight: 800;
  color: #0f172a;
  margin: 0 0 16px 0;
  padding-bottom: 12px;
  border-bottom: 2px solid #f1f5f9;
}

.sidebar-related-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.sidebar-related-item {
  border-bottom: 1px solid #f1f5f9;
  padding-bottom: 14px;
}

.sidebar-related-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.sidebar-rel-link {
  display: flex;
  gap: 12px;
  text-decoration: none;
  align-items: flex-start;
  transition: transform 0.2s ease;
}

.sidebar-rel-link:hover {
  transform: translateX(2px);
}

.sidebar-rel-img {
  width: 76px;
  height: 58px;
  border-radius: 8px;
  overflow: hidden;
  flex-shrink: 0;
  background: #f1f5f9;
}

.sidebar-rel-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.sidebar-rel-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
}

.sidebar-rel-cat {
  font-size: 11px;
  font-weight: 700;
  color: #022b9f;
  text-transform: uppercase;
}

.sidebar-rel-title {
  font-size: 13.5px;
  font-weight: 700;
  color: #1e293b;
  line-height: 1.35;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  transition: color 0.2s ease;
}

.sidebar-rel-link:hover .sidebar-rel-title {
  color: #022b9f;
}

.sidebar-rel-date {
  font-size: 11.5px;
  color: #94a3b8;
  font-weight: 500;
}

.not-found-container {
  padding-top: 160px;
  padding-bottom: 120px;
}

.btn-back {
  display: inline-block;
  margin-top: 20px;
  padding: 12px 24px;
  background: #022b9f;
  color: #ffffff;
  border-radius: 10px;
  text-decoration: none;
  font-weight: 700;
}

/* ==================== PROJECT REVIEWS STYLES ==================== */
.project-reviews-section {
  margin-top: 50px;
  padding-top: 36px;
  border-top: 2px solid #f1f5f9;
}

.reviews-header-block {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
  margin-bottom: 28px;
  flex-wrap: wrap;
}

.reviews-header-left {
  flex: 1;
  min-width: 280px;
}

.reviews-heading {
  font-size: 24px;
  font-weight: 800;
  color: #0f172a;
  margin: 0 0 8px 0;
}

.reviews-subheading {
  font-size: 14px;
  color: #64748b;
  line-height: 1.6;
  margin: 0;
}

.reviews-stat-badge {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 8px 16px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.stat-star {
  font-size: 18px;
}

.stat-number {
  font-size: 18px;
  font-weight: 800;
  color: #0f172a;
}

.stat-count {
  font-size: 13px;
  color: #64748b;
  font-weight: 600;
}

/* Form Card (Collapsible) */
.review-form-card {
  background: #f8fafc;
  border: 1.5px dashed #cbd5e1;
  border-radius: 16px;
  padding: 16px 20px;
  margin-bottom: 36px;
  transition: all 0.25s ease;
}

.review-form-card.is-expanded {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-style: solid;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
}

/* Collapsed Trigger Button Bar */
.review-form-trigger {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  cursor: pointer;
  user-select: none;
}

.trigger-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.trigger-avatar {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: #e0e7ff;
  color: #022b9f;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}

.trigger-text-wrap {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.trigger-title {
  font-size: 14.5px;
  font-weight: 700;
  color: #1e293b;
}

.trigger-subtitle {
  font-size: 12.5px;
  color: #64748b;
}

.btn-open-form {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: #022b9f;
  color: #ffffff;
  font-size: 13px;
  font-weight: 700;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  white-space: nowrap;
  transition: background 0.2s, transform 0.1s;
}

.btn-open-form:hover {
  background: #1e40af;
  transform: translateY(-1px);
}

/* Expanded Card Header */
.form-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 20px;
}

.btn-close-form {
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  color: #64748b;
  font-size: 12.5px;
  font-weight: 600;
  padding: 6px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
  white-space: nowrap;
}

.btn-close-form:hover {
  background: #e2e8f0;
  color: #0f172a;
}

.btn-cancel-form {
  background: #ffffff;
  border: 1px solid #cbd5e1;
  color: #64748b;
  font-size: 13px;
  font-weight: 600;
  padding: 9px 18px;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-cancel-form:hover {
  background: #f1f5f9;
  color: #0f172a;
}

.form-title {
  font-size: 17px;
  font-weight: 800;
  color: #0f172a;
  margin: 0 0 4px 0;
}

.form-desc {
  font-size: 13.5px;
  color: #64748b;
  margin: 0;
}

.submission-notice-banner {
  background: #ecfdf5;
  border: 1.5px solid #a7f3d0;
  border-radius: 12px;
  padding: 14px 18px;
  margin-bottom: 20px;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  color: #065f46;
}

.notice-icon {
  font-size: 22px;
  line-height: 1;
}

.submission-notice-banner strong {
  display: block;
  font-size: 14.5px;
  margin-bottom: 2px;
}

.submission-notice-banner p {
  margin: 0;
  font-size: 13px;
  line-height: 1.5;
}

.review-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-row-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

@media (max-width: 640px) {
  .form-row-grid {
    grid-template-columns: 1fr;
  }
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-label {
  font-size: 13px;
  font-weight: 700;
  color: #334155;
}

.form-label .required {
  color: #ef4444;
}

.form-label small {
  color: #94a3b8;
  font-weight: 400;
}

.form-control-input,
.form-control-textarea {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  background: #ffffff;
  color: #0f172a;
  font-size: 14px;
  transition: border-color 0.2s, box-shadow 0.2s;
  box-sizing: border-box;
  font-family: inherit;
}

.form-control-input:focus,
.form-control-textarea:focus {
  outline: none;
  border-color: #022b9f;
  box-shadow: 0 0 0 3px rgba(2, 43, 159, 0.1);
}

.char-word-counter {
  font-size: 12px;
  color: #64748b;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
}

.char-word-counter .sep {
  color: #cbd5e1;
}

.char-word-counter.has-error {
  color: #e11d48;
}

.input-hint-error {
  font-size: 12px;
  color: #e11d48;
  font-weight: 600;
  margin-top: 2px;
}

.rating-select-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.star-rating-picker {
  display: flex;
  align-items: center;
  gap: 6px;
}

.star-btn {
  background: none;
  border: none;
  font-size: 26px;
  color: #cbd5e1;
  cursor: pointer;
  line-height: 1;
  padding: 0 2px;
  transition: transform 0.1s, color 0.15s;
}

.star-btn:hover {
  transform: scale(1.15);
}

.star-btn.active {
  color: #f59e0b;
}

.rating-label-text {
  font-size: 13px;
  font-weight: 700;
  color: #475569;
  margin-left: 8px;
}

.form-actions-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 6px;
  flex-wrap: wrap;
  gap: 12px;
}

.status-note {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 12.5px;
  color: #64748b;
  font-weight: 500;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #10b981;
}

.btn-submit-review {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 22px;
  background: #022b9f;
  color: #ffffff;
  font-size: 13.5px;
  font-weight: 700;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: background 0.2s, transform 0.1s;
}

.btn-submit-review:hover:not(:disabled) {
  background: #1e40af;
  transform: translateY(-1px);
}

.btn-submit-review:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

/* Reviews List */
.reviews-list-container {
  margin-top: 24px;
}

.reviews-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 30px;
  color: #64748b;
  font-size: 14px;
}

.empty-reviews-box {
  text-align: center;
  padding: 36px 20px;
  background: #ffffff;
  border: 1px dashed #cbd5e1;
  border-radius: 14px;
}

.empty-icon {
  font-size: 32px;
  display: block;
  margin-bottom: 8px;
}

.empty-reviews-box h4 {
  font-size: 16px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 6px 0;
}

.empty-reviews-box p {
  font-size: 13.5px;
  color: #64748b;
  margin: 0;
}

.reviews-cards-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.review-item-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  padding: 20px;
  transition: box-shadow 0.2s;
}

.review-item-card:hover {
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.04);
}

.review-author-meta {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 12px;
}

.review-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: linear-gradient(135deg, #022b9f 0%, #3b82f6 100%);
  color: #ffffff;
  font-weight: 800;
  font-size: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.review-author-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.author-name-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.author-fullname {
  font-size: 14.5px;
  font-weight: 700;
  color: #0f172a;
}

.approved-badge {
  font-size: 11px;
  font-weight: 700;
  color: #059669;
  background: #d1fae5;
  padding: 2px 8px;
  border-radius: 10px;
}

.review-stars-date {
  display: flex;
  align-items: center;
  gap: 10px;
}

.review-stars {
  display: flex;
  gap: 2px;
}

.review-stars .star {
  font-size: 14px;
  color: #cbd5e1;
}

.review-stars .star.filled {
  color: #f59e0b;
}

.review-date {
  font-size: 12px;
  color: #94a3b8;
}

.review-body-text {
  font-size: 14.5px;
  line-height: 1.7;
  color: #334155;
  white-space: pre-line;
  word-break: break-word;
  transition: max-height 0.3s ease;
}

.review-body-text.is-collapsed {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.toggle-readmore-row {
  margin-top: 8px;
}

.btn-toggle-readmore {
  background: none;
  border: none;
  padding: 0;
  font-size: 13px;
  font-weight: 700;
  color: #022b9f;
  cursor: pointer;
  transition: color 0.15s;
}

.btn-toggle-readmore:hover {
  text-decoration: underline;
  color: #1e40af;
}

.flex-center {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>


