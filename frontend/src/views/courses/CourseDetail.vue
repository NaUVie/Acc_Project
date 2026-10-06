<template>
  <div class="course-detail-view">
    <div class="detail-container">
      <!-- Breadcrumb Nav -->
      <nav class="breadcrumb-nav">
        <router-link to="/" class="breadcrumb-link">Trang chủ</router-link>
        <span class="breadcrumb-separator">&rsaquo;</span>
        <router-link :to="course ? '/courses/category/' + (course.category || 'ky-nang-ai') : '/courses/category/ky-nang-ai'" class="breadcrumb-link">{{ course ? getCategoryName(course.category) : 'Khóa học' }}</router-link>
        <span class="breadcrumb-separator">&rsaquo;</span>
        <span class="breadcrumb-current">{{ course?.title || 'Chi tiết khóa học' }}</span>
      </nav>

      <!-- Loading State -->
      <div v-if="loading" style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 80px 0;">
        <div style="width: 44px; height: 44px; border: 3px solid #cbd5e1; border-top-color: #0284c7; border-radius: 50%; animation: spin 0.8s linear infinite;"></div>
        <p style="margin-top: 16px; font-weight: 600; color: #475569;">Đang tải thông tin khóa học...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error || !course" style="background: #fef2f2; border: 1px solid #fecaca; color: #991b1b; padding: 40px; border-radius: 20px; text-align: center; max-width: 500px; margin: 60px auto;">
        <h3 style="font-size: 20px; font-weight: 800; margin-bottom: 8px;">Không tìm thấy khóa học</h3>
        <p style="font-size: 14px; margin-bottom: 24px; color: #dc2626;">{{ error || 'Khóa học bạn tìm kiếm không tồn tại hoặc đã bị gỡ bỏ.' }}</p>
        <router-link to="/" class="btn-add-cart" style="display: inline-flex; width: auto; padding: 10px 24px;">Quay về Trang chủ</router-link>
      </div>

      <!-- Main Detail View -->
      <div v-else class="detail-grid">
        
        <!-- Left Column: Hero Info & Detailed Tabs -->
        <div class="detail-main-content">
          
          <!-- Course Hero Card -->
          <div class="course-hero-card">
            <div class="course-badges-row">
              <span class="cat-badge">{{ getCategoryName(course.category) }}</span>
              <span v-if="parentProgram" class="program-parent-badge">
                🎓 thuộc {{ parentProgram.title }}
              </span>
            </div>

            <h1 class="course-main-title">{{ course.title }}</h1>

            <p class="course-main-description">
              {{ plainDescription }}
            </p>

            <!-- Stats Bar -->
            <div class="course-meta-bar">
              <div class="meta-rating">
                <span>⭐ {{ course.rating || (4.8 + ((course.id % 3) * 0.1)).toFixed(1) }}</span>
                <span class="rating-count">({{ course.ratingCount || Math.floor((course.id % 45) + 85) }} đánh giá)</span>
              </div>
              <div class="meta-item">
                <span>👥 {{ course.studentCount ? course.studentCount.toLocaleString() : ((course.id % 15 + 8) * 120 + 450).toLocaleString() }}+ Học viên</span>
              </div>
              <div class="meta-item">
                <span>🌐 Tiếng Việt</span>
              </div>
              <div class="meta-item" style="color: #94a3b8;">
                <span>🔄 Cập nhật 2026</span>
              </div>
            </div>
          </div>

          <!-- Course Tabs Card -->
          <div class="course-tabs-card">
            <!-- Tab Headers -->
            <div class="tab-headers">
              <button 
                @click="activeTab = 'overview'" 
                :class="['tab-btn', { active: activeTab === 'overview' }]"
              >
                💡 Tổng quan khóa học
              </button>
              <button 
                @click="activeTab = 'curriculum'" 
                :class="['tab-btn', { active: activeTab === 'curriculum' }]"
              >
                📚 Lộ trình học ({{ parsedCurriculum.length }} bài học)
              </button>
              <button 
                @click="activeTab = 'reviews'" 
                :class="['tab-btn', { active: activeTab === 'reviews' }]"
              >
                ⭐ Đánh giá ({{ reviews.length }})
              </button>
            </div>

            <!-- Tab Body -->
            <div class="tab-body">
              <!-- Tab 1: Overview -->
              <div v-if="activeTab === 'overview'">
                <!-- Rich Text Description Block -->
                <div v-if="course.description" class="rich-course-description mb-6" v-html="course.description"></div>

                <h3 class="section-heading">Bạn sẽ đạt được gì sau khóa học này?</h3>
                <div class="outcomes-grid">
                  <div v-for="(outcome, oIdx) in courseOutcomes" :key="oIdx" class="outcome-item">
                    <span class="check-icon">✓</span>
                    <span class="outcome-text">{{ outcome }}</span>
                  </div>
                </div>

                <div style="padding-top: 24px; border-top: 1px solid #f1f5f9; margin-top: 24px;">
                  <h3 class="section-heading">Yêu cầu & Đối tượng phù hợp</h3>
                  <ul class="requirements-list">
                    <li v-for="(req, rIdx) in courseRequirements" :key="rIdx">{{ req }}</li>
                  </ul>
                </div>
              </div>

              <!-- Tab 2: Curriculum -->
              <div v-else-if="activeTab === 'curriculum'">
                <div class="curriculum-header-row">
                  <h3 class="section-heading" style="margin: 0;">{{ course.customRoadmap ? 'Lộ trình học tập chi tiết' : 'Chi tiết các bài học' }}</h3>
                  <span v-if="!course.customRoadmap" class="lesson-badge">Tổng cộng {{ parsedCurriculum.length }} bài học</span>
                </div>

                <!-- Custom Roadmap HTML View -->
                <div v-if="course.customRoadmap" class="rich-course-description" v-html="course.customRoadmap"></div>

                <!-- Standard Curriculum Items -->
                <div v-else-if="parsedCurriculum.length === 0" style="text-align: center; padding: 40px 0; color: #64748b; font-weight: 500;">
                  Nội dung lộ trình chi tiết đang được cập nhật.
                </div>

                <div v-else class="curriculum-list">
                  <div 
                    v-for="(item, idx) in parsedCurriculum" 
                    :key="idx" 
                    class="curriculum-item"
                  >
                    <div style="display: flex; align-items: center; gap: 14px;">
                      <span class="lesson-number">{{ idx + 1 }}</span>
                      <div>
                        <h4 class="lesson-title">{{ item.title || item.name || item }}</h4>
                        <p v-if="item.duration" class="lesson-duration">⏱️ {{ item.duration }}</p>
                      </div>
                    </div>
                    <span class="hd-tag">▶ Video HD</span>
                  </div>
                </div>
              </div>

              <!-- Tab 3: Reviews -->
              <div v-else-if="activeTab === 'reviews'">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; border-bottom: 1px solid #e2e8f0; padding-bottom: 16px;">
                  <div>
                    <h3 class="section-heading" style="margin: 0;">Đánh giá từ Học viên</h3>
                    <p style="font-size: 13px; color: #64748b; margin: 4px 0 0 0;">{{ reviews.length }} nhận xét công khai từ học viên tham gia khóa học</p>
                  </div>
                  <div style="font-size: 24px; font-weight: 800; color: #d97706; display: flex; align-items: center; gap: 6px;">
                    ⭐ {{ averageRating }} / 5.0
                  </div>
                </div>

                <!-- Review Submission Box (Only for Enrolled Users or Admins) -->
                <div v-if="isAlreadyEnrolled" style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; margin-bottom: 30px;">
                  <h4 style="font-size: 15px; font-weight: 700; color: #0f172a; margin-top: 0; margin-bottom: 12px;">Viết nhận xét của bạn</h4>
                  <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
                    <span style="font-size: 13px; font-weight: 600; color: #475569;">Chọn số sao:</span>
                    <div style="display: flex; gap: 4px; cursor: pointer;">
                      <span v-for="star in 5" :key="star" @click="newReview.rating = star" style="font-size: 20px; transition: transform 0.1s;" :style="{ color: star <= newReview.rating ? '#f59e0b' : '#cbd5e1' }">★</span>
                    </div>
                  </div>
                  <textarea v-model="newReview.comment" placeholder="Chia sẻ trải nghiệm học tập của bạn về nội dung bài giảng, giảng viên..." style="width: 100%; min-height: 80px; padding: 12px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 14px; margin-bottom: 12px; box-sizing: border-box; outline: none;"></textarea>
                  <button @click="submitReview" :disabled="submittingReview" class="btn-add-cart" style="width: auto; padding: 8px 20px; font-size: 13px;">
                    {{ submittingReview ? 'Đang gửi...' : 'Gửi nhận xét' }}
                  </button>
                </div>

                <!-- Reviews List -->
                <div v-if="reviews.length === 0" style="text-align: center; padding: 40px 0; color: #64748b; font-size: 14px;">
                  Chưa có nhận xét nào. Hãy là người đầu tiên đánh giá khóa học này!
                </div>
                <div v-else style="display: flex; flex-direction: column; gap: 16px;">
                  <div v-for="rev in reviews" :key="rev.id" style="border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px; background: #fff;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                      <div style="display: flex; align-items: center; gap: 10px;">
                        <div style="width: 36px; height: 36px; border-radius: 50%; background: #0284c7; color: white; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 14px;">
                          {{ rev.user_fullname ? rev.user_fullname.charAt(0).toUpperCase() : 'H' }}
                        </div>
                        <div>
                          <div style="font-weight: 700; font-size: 14px; color: #0f172a;">{{ rev.user_fullname }}</div>
                          <div style="font-size: 11px; color: #94a3b8;">{{ formatDate(rev.created_at) }}</div>
                        </div>
                      </div>
                      <div style="color: #f59e0b; font-size: 14px;">
                        <span v-for="s in 5" :key="s">{{ s <= rev.rating ? '★' : '☆' }}</span>
                      </div>
                    </div>
                    <p style="font-size: 14px; color: #334155; margin: 0; line-height: 1.5;">{{ rev.comment }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

        </div>

        <!-- Right Column: Sticky Sidebar Card -->
        <div>
          <div class="sticky-sidebar-card">
            <!-- Thumbnail Image -->
            <div class="course-preview-box">
              <img 
                :src="course.image || '/images/default.jpg'" 
                :alt="course.title" 
                class="preview-img"
              />
              <div class="play-overlay">
                <div class="play-btn-circle">
                  <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor">
                    <polygon points="5 3 19 12 5 21 5 3"/>
                  </svg>
                </div>
              </div>
            </div>

            <!-- Price Info -->
            <div class="price-display-box">
              <div class="price-row">
                <span class="current-price">{{ formatCurrency(course.price) }}</span>
                <span v-if="course.originalPrice || course.original_price" class="old-price">
                  {{ formatCurrency(course.originalPrice || course.original_price) }}
                </span>
                <span v-if="(course.originalPrice || course.original_price) && Number(course.originalPrice || course.original_price) > Number(course.price)" class="discount-badge">
                  Giảm {{ Math.round((1 - Number(course.price) / Number(course.originalPrice || course.original_price)) * 100) }}%
                </span>
              </div>
              <p class="urgency-text">🔥 Ưu đãi có hạn - Đăng ký hôm nay tiết kiệm nhất</p>
            </div>

            <!-- Action Buttons -->
            <!-- 🎓 Đã đăng ký: Hiển thị nút Vào học ngay -->
            <div v-if="isAlreadyEnrolled" class="action-btn-group">
              <router-link :to="'/courses/' + course.handle + '/study'" class="btn-buy-now" style="text-decoration: none; display: flex; align-items: center; justify-content: center; gap: 8px;">
                ▶ Vào học ngay
              </router-link>
              <div class="enrolled-badge" style="background: #dcfce7; color: #15803d; border: 1px solid #bbf7d0; border-radius: 10px; padding: 10px 16px; text-align: center; font-size: 13px; font-weight: 600; margin-top: 8px;">
                ✅ Bạn đã đăng ký khóa học này. Chúc bạn học tốt!
              </div>
            </div>

            <!-- 🛒 Chưa đăng ký: Hiển thị nút mua -->
            <div v-else class="action-btn-group">
              <button @click="addToCart" class="btn-add-cart">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/>
                  <line x1="3" y1="6" x2="21" y2="6"/>
                  <path d="M16 10a4 4 0 0 1-8 0"/>
                </svg>
                Thêm vào giỏ hàng
              </button>
              <button @click="buyNow" class="btn-buy-now">
                ⚡ Đăng ký học ngay
              </button>
              <button @click="handleToggleWishlist" class="btn-wishlist" :style="{ background: isWishlisted ? '#fef2f2' : '#f8fafc', color: isWishlisted ? '#ef4444' : '#475569', border: '1px solid #e2e8f0', borderRadius: '12px', padding: '10px 16px', fontWeight: '600', fontSize: '13px', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '6px', width: '100%', marginTop: '8px' }">
                <span>{{ isWishlisted ? '❤️ Đã lưu vào Yêu thích' : '🤍 Thêm vào Yêu thích' }}</span>
              </button>
            </div>

            <!-- Perks List -->
            <div class="perks-box">
              <div class="perks-title">Khóa học bao gồm:</div>
              <div class="perk-item">
                <span class="perk-icon">🎥</span>
                <span>Truy cập trọn đời tất cả video HD</span>
              </div>
              <div class="perk-item">
                <span class="perk-icon">📁</span>
                <span>Tài liệu & Mẫu Prompt đính kèm đầy đủ</span>
              </div>
              <div class="perk-item">
                <span class="perk-icon">📜</span>
                <span>Cấp chứng nhận hoàn thành khóa học</span>
              </div>
              <div class="perk-item">
                <span class="perk-icon">💬</span>
                <span>Nhóm hỗ trợ học viên giải đáp 24/7</span>
              </div>
            </div>

            <!-- Lecturers / Course Instructors Box -->
            <div v-if="courseLecturers.length > 0" class="perks-box" style="margin-top: 20px;">
              <div class="perks-title" style="margin-bottom: 12px; display: flex; align-items: center; gap: 6px;">
                <span>🎓 Đội ngũ Giảng viên:</span>
              </div>
              <div v-for="lec in courseLecturers" :key="lec.id" style="display: flex; align-items: center; gap: 12px; padding: 8px 0; border-bottom: 1px dashed #e2e8f0;">
                <img :src="lec.avatar || lec.avatar_drive_link || '/images/default-avatar.jpg'" :alt="lec.name" style="width: 44px; height: 44px; border-radius: 50%; object-fit: cover; border: 2px solid #0284c7;" />
                <div>
                  <div style="font-weight: 700; color: #0f172a; font-size: 14px;">{{ lec.name }}</div>
                  <div style="font-size: 12px; color: #0284c7; font-weight: 600;">{{ lec.title }}</div>
                </div>
              </div>
            </div>

          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useCourseStore } from '@/stores/courses';
import { stripHtml } from '@/utils/stripHtml';

const route = useRoute();
const router = useRouter();
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

const courseOutcomes = computed(() => {
  if (!course.value) return [];
  if (course.value.outcomes) {
    if (Array.isArray(course.value.outcomes)) return course.value.outcomes;
    if (typeof course.value.outcomes === 'string') {
      const trimmed = course.value.outcomes.trim();
      if (trimmed.startsWith('[')) {
        try {
          const parsed = JSON.parse(trimmed);
          if (Array.isArray(parsed)) return parsed;
        } catch (e) {}
      }
      return trimmed.split('\n').map(s => s.trim()).filter(Boolean);
    }
  }
  
  const cat = course.value.category;
  if (cat === 'ky-nang-ai') {
    return [
      'Làm chủ công cụ AI & ứng dụng tự động hóa công việc thực tế',
      'Tối ưu thời gian xử lý dữ liệu và tạo nội dung x5 lần',
      'Xây dựng quy trình làm việc thông minh cho bản thân & đội ngũ',
      'Nhận chứng nhận hoàn thành khóa học từ ACC Academy'
    ];
  } else if (cat === 'ky-nang-mem') {
    return [
      'Rèn luyện tư duy giao tiếp và thuyết phục hiệu quả trong công việc',
      'Làm chủ phương pháp quản lý thời gian và giải quyết vấn đề linh hoạt',
      'Nâng cao khả năng làm việc nhóm và đàm phán chuyên nghiệp',
      'Nhận chứng nhận hoàn thành khóa học từ ACC Academy'
    ];
  } else if (cat === 'ky-nang-chuyen-mon') {
    return [
      'Thành thạo kỹ năng chuyên môn ứng dụng trực tiếp vào công việc',
      'Xây dựng quy trình làm việc chuẩn mực và đạt hiệu suất tối đa',
      'Nâng cao năng lực phân tích, quản lý và tối ưu hóa kết quả công việc',
      'Nhận chứng nhận hoàn thành khóa học từ ACC Academy'
    ];
  } else if (cat === 'bundles') {
    return [
      'Sở hữu lộ trình học tập toàn diện từ cơ bản đến chuyên sâu',
      'Tiết kiệm chi phí ưu đãi đặc biệt so với đăng ký từng khóa học lẻ',
      'Truy cập trọn đời tất cả tài liệu và video bài giảng trong gói Combo',
      'Nhận chứng nhận hoàn thành chương trình từ ACC Academy'
    ];
  }
  
  return [
    `Nắm vững kiến thức trọng tâm của khóa ${course.value.title || 'học'}`,
    'Ứng dụng thực tiễn ngay vào công việc hằng ngày',
    'Tài liệu giáo trình đính kèm và nhóm hỗ trợ 24/7',
    'Nhận chứng nhận hoàn thành khóa học từ ACC Academy'
  ];
});

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

const loadCourse = async () => {
  loading.value = true;
  error.value = null;
  const handle = route.params.handle;
  try {
    const fetched = await courseStore.fetchCourseByHandle(handle);
    course.value = fetched;
  } catch (err) {
    error.value = err.message || 'Không thể tải thông tin khóa học.';
  } finally {
    loading.value = false;
  }
};

watch(() => route.params.handle, () => {
  loadCourse().then(() => {
    loadReviews();
  });
});

const addToCart = async () => {
  if (!course.value) return;
  if (!courseStore.token) {
    courseStore.showToast('Vui lòng đăng nhập để đăng ký khóa học!', 'warning');
    router.push('/login');
    return;
  }
  try {
    await courseStore.addToCart(course.value.id);
    courseStore.showToast(`Đã thêm "${course.value.title}" vào giỏ hàng!`, 'success');
  } catch (err) {
    courseStore.showToast(err.message || 'Không thể thêm khóa học vào giỏ hàng', 'error');
  }
};

const reviews = ref([]);
const newReview = ref({ rating: 5, comment: '' });
const submittingReview = ref(false);

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
  if (!course.value) return;
  reviews.value = await courseStore.fetchCourseReviews(course.value.handle);
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

const buyNow = () => {
  if (!course.value) return;
  if (!courseStore.token) {
    courseStore.showToast('Vui lòng đăng nhập để đăng ký khóa học!', 'warning');
    router.push('/login');
    return;
  }
  courseStore.buyNow(course.value)
    .then(() => {
      router.push('/checkout');
    })
    .catch(err => {
      if (err.message !== 'CANCELLED') {
        courseStore.showToast(err.message || 'Không thể tiến hành thanh toán', 'error');
      }
    });
};

const courseLecturers = computed(() => {
  if (!course.value || !course.value.lecturerIds) return [];
  const ids = course.value.lecturerIds.split(',').map(s => s.trim()).filter(Boolean);
  return ids.map(id => courseStore.lecturers.find(l => String(l.id) === String(id))).filter(Boolean);
});

onMounted(() => {
  loadCourse().then(() => {
    loadReviews();
  });
  if (courseStore.token) {
    courseStore.fetchWishlist();
  }
  if (courseStore.programs.length === 0) {
    courseStore.fetchPrograms();
  }
  if (courseStore.lecturers.length === 0) {
    courseStore.fetchLecturers();
  }
});

</script>

<style scoped>
.rich-course-description {
  color: #334155;
  font-size: 15px;
  line-height: 1.7;
  padding-bottom: 20px;
  border-bottom: 1px solid #f1f5f9;
  margin-bottom: 24px;
}

.rich-course-description :deep(h2) {
  font-size: 20px;
  font-weight: 800;
  color: #0f172a;
  margin-top: 16px;
  margin-bottom: 10px;
}

.rich-course-description :deep(h3) {
  font-size: 17px;
  font-weight: 700;
  color: #1e293b;
  margin-top: 14px;
  margin-bottom: 8px;
}

.rich-course-description :deep(ul),
.rich-course-description :deep(ol) {
  padding-left: 24px;
  margin: 10px 0;
}

.rich-course-description :deep(li) {
  margin-bottom: 6px;
}

.rich-course-description :deep(a) {
  color: #0284c7;
  text-decoration: underline;
  font-weight: 600;
}

.rich-course-description :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 12px;
  margin: 16px 0;
  display: block;
}
</style>

<style scoped src="@/styles/views/courses/CourseDetail.css"></style>
