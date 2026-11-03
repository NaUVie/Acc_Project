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
            <div class="article-badges">
              <!-- <span class="cat-badge-pill">{{ getCategoryName(course.category) }}</span> -->
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

            <!-- Outcomes / Highlights -->
            <div v-if="courseOutcomes.length > 0" class="article-section-block">
              <h3 class="article-sub-heading">Giá trị cốt lõi & Mục tiêu đạt được</h3>
              <div class="article-outcomes-grid">
                <div v-for="(outcome, oIdx) in courseOutcomes" :key="oIdx" class="article-outcome-card">
                  <span class="check-icon">✓</span>
                  <span>{{ outcome }}</span>
                </div>
              </div>
            </div>

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
          </div>

        </article>

        <!-- Right Side: Sticky Registration Sidebar -->
        <aside class="course-article-sidebar">
          <div class="sticky-register-card">
            <div class="sidebar-price-header">
              <span class="price-label">{{ hasDiscount(course) ? $t('course.discountTuition') : $t('course.tuition') }}</span>
              <div class="price-val-row">
                <span class="price-current">{{ formatCurrency(course.price) }}</span>
                <span v-if="hasDiscount(course)" class="price-old">
                  {{ formatCurrency(course.originalPrice || course.original_price) }}
                </span>
              </div>
              <div class="vat-badge-text" style="font-size: 11.5px; color: #16a34a; font-weight: 600; margin-top: 4px;">
                ✓ Đã bao gồm thuế GTGT (VAT)
              </div>
            </div>

            <div class="sidebar-perks-list">
              <div class="sidebar-perk-item">{{ $t('course.perk1') }}</div>
              <div class="sidebar-perk-item">{{ $t('course.perk2') }}</div>
              <div class="sidebar-perk-item">{{ $t('course.perk3') }}</div>
              <div class="sidebar-perk-item">{{ $t('course.perk4') }}</div>
            </div>

            <!-- Nếu đã sở hữu: Hiển thị nút Vào học ngay -->
            <router-link 
              v-if="isAlreadyEnrolled"
              :to="'/courses/' + (course.handle || course.id) + '/study'"
              class="sidebar-register-btn enrolled-study-btn" 
              style="width: 100%; box-sizing: border-box; display: flex; align-items: center; justify-content: center; gap: 8px; text-decoration: none; background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: #ffffff; font-weight: 700;"
            >
              <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                <polygon points="5 3 19 12 5 21 5 3"></polygon>
              </svg>
              <span>Vào Học Ngay</span>
            </router-link>

            <!-- Nếu chưa sở hữu: Hiển thị nút Đăng ký -->
            <button 
              v-else
              type="button" 
              class="sidebar-register-btn" 
              style="width: 100%; box-sizing: border-box; cursor: pointer; border: none; font-family: var(--font-sans);" 
              @click="buyNow"
            >
              Đăng Ký
            </button>

            <a href="tel:0938566700" class="sidebar-hotline-btn">
             Hotline: 0938 566 700
            </a>

            <!-- Sidebar Related Courses Widget (Cùng nằm trong sidebar container, cuộn tự nhiên) -->
            <div v-if="relatedCourses.length > 0" class="sidebar-related-courses-box">
              <div class="sidebar-related-header">
                <span class="related-badge">{{ $t('course.relatedBadge') }}</span>
                <h3 class="sidebar-related-title">{{ $t('course.relatedTitle') }}</h3>
              </div>

              <div class="sidebar-related-list">
                <div 
                  v-for="relCourse in relatedCourses" 
                  :key="relCourse.id" 
                  class="sidebar-related-item"
                >
                  <router-link :to="'/course/' + (relCourse.handle || relCourse.id)" class="sidebar-rel-thumb-link">
                    <img 
                      :src="relCourse.image || '/images/Square-Cover-_1.webp'" 
                      :alt="relCourse.title" 
                      class="sidebar-rel-thumb" 
                      loading="lazy" 
                    />
                  </router-link>
                  <div class="sidebar-rel-info">
                    <span class="sidebar-rel-cat">{{ getCategoryName(relCourse.category) }}</span>
                    <h4 class="sidebar-rel-name">
                      <router-link :to="'/course/' + (relCourse.handle || relCourse.id)">
                        {{ relCourse.title }}
                      </router-link>
                    </h4>
                    <div class="sidebar-rel-price-row">
                      <span class="sidebar-rel-price">{{ formatCurrency(relCourse.price) }}</span>
                      <span v-if="hasDiscount(relCourse)" class="sidebar-rel-price-old">
                        {{ formatCurrency(relCourse.originalPrice || relCourse.original_price) }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              <router-link :to="course?.category ? '/courses/category/' + course.category : '/courses'" class="sidebar-related-more-btn">
                Xem tất cả khóa học &rarr;
              </router-link>
            </div>
          </div>
        </aside>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useCourseStore } from '@/stores/courses';
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

const registerForm = ref({
  fullname: '',
  phone: '',
  email: '',
  message: ''
});
const submittingRegister = ref(false);

const scrollToRegister = () => {
  const el = document.getElementById('course-register-form');
  if (el) {
    el.scrollIntoView({ behavior: 'smooth' });
  }
};

const handleBottomRegister = async () => {
  if (!registerForm.value.fullname || !registerForm.value.phone || !registerForm.value.email) {
    courseStore.showToast('Vui lòng điền đầy đủ các thông tin bắt buộc (*)', 'warning');
    return;
  }

  submittingRegister.value = true;
  try {
    const nameParts = registerForm.value.fullname.trim().split(' ');
    const lastName = nameParts.length > 0 ? nameParts[nameParts.length - 1] : '';
    const firstName = nameParts.length > 1 ? nameParts[0] : registerForm.value.fullname.trim();
    const middleName = nameParts.length > 2 ? nameParts.slice(1, -1).join(' ') : '';

    await courseStore.sendContact(
      firstName,
      middleName,
      lastName,
      registerForm.value.email,
      registerForm.value.phone,
      course.value?.handle || 'course-detail-register',
      registerForm.value.message || `Đăng ký tư vấn cho khóa học: ${course.value?.title || ''}`
    );

    courseStore.showToast('Cảm ơn bạn! Đã gửi thông tin đăng ký tư vấn thành công.', 'success');
    registerForm.value = { fullname: '', phone: '', email: '', message: '' };
  } catch (err) {
    courseStore.showToast(err.message || 'Gửi thông tin thất bại. Vui lòng thử lại!', 'error');
  } finally {
    submittingRegister.value = false;
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

const buyNow = () => {
  if (!course.value) return;
  if (!courseStore.token) {
    courseStore.showToast('Vui lòng đăng nhập để đăng ký khóa học!', 'warning');
    router.push('/login');
    return;
  }
  if (isAlreadyEnrolled.value) {
    courseStore.showToast('Bạn đã sở hữu khóa học này rồi! Đang chuyển đến phòng học...', 'info');
    router.push('/courses/' + (course.value.handle || course.value.id) + '/study');
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

// Khóa học liên quan: cùng category hoặc cùng programId, loại trừ chính khóa học hiện tại
const relatedCourses = computed(() => {
  if (!course.value || !courseStore.courses || courseStore.courses.length === 0) return [];
  const currentId = course.value.id;
  const currentHandle = course.value.handle;
  const currentCategory = course.value.category;
  const currentProgramId = course.value.programId;

  // 1. Ưu tiên khóa học cùng chuyên mục (category) hoặc cùng chương trình (program)
  let sameCategory = courseStore.courses.filter(c => {
    if (c.id === currentId || c.handle === currentHandle) return false;
    return (currentCategory && c.category === currentCategory) || 
           (currentProgramId && c.programId === currentProgramId);
  });

  // 2. Nếu không đủ 4 khóa học, lấy thêm các khóa học khác để gợi ý đủ tối đa 4 khóa
  if (sameCategory.length < 4) {
    const others = courseStore.courses.filter(c => {
      if (c.id === currentId || c.handle === currentHandle) return false;
      return !sameCategory.some(sc => sc.id === c.id);
    });
    sameCategory = [...sameCategory, ...others];
  }

  return sameCategory.slice(0, 4);
});

onMounted(() => {
  loadCourse();
  loadReviews();
  if (courseStore.courses.length === 0) {
    courseStore.fetchCourses();
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
