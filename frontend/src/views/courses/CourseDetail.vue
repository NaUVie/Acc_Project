<template>
  <div class="course-detail-view">
    <div class="detail-container">
      <!-- Breadcrumb Nav -->
      <nav class="breadcrumb-nav">
        <router-link to="/" class="breadcrumb-link">Trang chủ</router-link>
        <span class="breadcrumb-separator">&rsaquo;</span>
        <router-link to="/courses/ai" class="breadcrumb-link">Khóa học</router-link>
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
              {{ course.description || 'Khóa học thiết kế thực chiến giúp bạn làm chủ công nghệ, x5 hiệu suất làm việc và nâng tầm sự nghiệp trong kỷ nguyên AI.' }}
            </p>

            <!-- Stats Bar -->
            <div class="course-meta-bar">
              <div class="meta-rating">
                <span>⭐ 4.9</span>
                <span class="rating-count">(128 đánh giá)</span>
              </div>
              <div class="meta-item">
                <span>👥 1,420+ Học viên</span>
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
            </div>

            <!-- Tab Body -->
            <div class="tab-body">
              <!-- Tab 1: Overview -->
              <div v-if="activeTab === 'overview'">
                <h3 class="section-heading">Bạn sẽ đạt được gì sau khóa học này?</h3>
                <div class="outcomes-grid">
                  <div class="outcome-item">
                    <span class="check-icon">✓</span>
                    <span class="outcome-text">Làm chủ công cụ AI & ứng dụng tự động hóa công việc thực tế</span>
                  </div>
                  <div class="outcome-item">
                    <span class="check-icon">✓</span>
                    <span class="outcome-text">Tối ưu thời gian xử lý dữ liệu và tạo nội dung x5 lần</span>
                  </div>
                  <div class="outcome-item">
                    <span class="check-icon">✓</span>
                    <span class="outcome-text">Xây dựng quy trình làm việc thông minh cho bản thân & đội ngũ</span>
                  </div>
                  <div class="outcome-item">
                    <span class="check-icon">✓</span>
                    <span class="outcome-text">Nhận chứng nhận hoàn thành khóa học từ ACC Academy</span>
                  </div>
                </div>

                <div style="padding-top: 24px; border-top: 1px solid #f1f5f9; margin-top: 24px;">
                  <h3 class="section-heading">Yêu cầu & Đối tượng phù hợp</h3>
                  <ul class="requirements-list">
                    <li>Dành cho Quản lý, Chuyên viên, Freelancer và bất kỳ ai muốn nâng cao năng lực thời AI.</li>
                    <li>Không yêu cầu kiến thức lập trình phức tạp – bài giảng cầm tay chỉ việc từ cơ bản đến nâng cao.</li>
                    <li>Chỉ cần máy tính kết nối Internet để tham gia học trực tuyến mọi lúc mọi nơi.</li>
                  </ul>
                </div>
              </div>

              <!-- Tab 2: Curriculum -->
              <div v-else-if="activeTab === 'curriculum'">
                <div class="curriculum-header-row">
                  <h3 class="section-heading" style="margin: 0;">Chi tiết các bài học</h3>
                  <span class="lesson-badge">Tổng cộng {{ parsedCurriculum.length }} bài học</span>
                </div>

                <div v-if="parsedCurriculum.length === 0" style="text-align: center; padding: 40px 0; color: #64748b; font-weight: 500;">
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
                <span v-if="course.originalPrice && course.originalPrice > course.price" class="discount-badge">
                  Giảm {{ Math.round((1 - course.price / course.originalPrice) * 100) }}%
                </span>
              </div>
              <p class="urgency-text">🔥 Ưu đãi có hạn - Đăng ký hôm nay tiết kiệm nhất</p>
            </div>

            <!-- Action Buttons -->
            <div class="action-btn-group">
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

const route = useRoute();
const router = useRouter();
const courseStore = useCourseStore();

const course = ref(null);
const loading = ref(true);
const error = ref(null);
const activeTab = ref('overview');

const formatCurrency = (val) => {
  if (!val && val !== 0) return '0đ';
  return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(val);
};

const getCategoryName = (cat) => {
  switch (cat) {
    case 'ky-nang-ai': return 'Kỹ năng AI';
    case 'ky-nang-mem': return 'Kỹ năng mềm';
    case 'ky-nang-chuyen-mon': return 'Kỹ năng chuyên môn';
    case 'bundles': return 'Gói Combo';
    default: return cat || 'Khóa học';
  }
};

const parentProgram = computed(() => {
  if (!course.value || !course.value.programId) return null;
  return courseStore.programs.find(p => p.id === course.value.programId);
});

const parsedCurriculum = computed(() => {
  if (!course.value || !course.value.curriculum) return [];
  try {
    if (typeof course.value.curriculum === 'string') {
      return JSON.parse(course.value.curriculum);
    }
    return course.value.curriculum;
  } catch (e) {
    return [course.value.curriculum];
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

onMounted(() => {
  loadCourse();
  if (courseStore.programs.length === 0) {
    courseStore.fetchPrograms();
  }
});

watch(() => route.params.handle, () => {
  loadCourse();
});

const addToCart = async () => {
  if (!course.value) return;
  try {
    await courseStore.addToCart(course.value.id);
    alert(`Đã thêm "${course.value.title}" vào giỏ hàng!`);
  } catch (err) {
    alert(err.message || 'Không thể thêm khóa học vào giỏ hàng');
  }
};

const buyNow = () => {
  if (!course.value) return;
  try {
    courseStore.buyNow(course.value);
    router.push('/checkout');
  } catch (err) {
    alert(err.message || 'Không thể tiến hành thanh toán');
  }
};
</script>

<style scoped src="@/styles/views/courses/CourseDetail.css"></style>
