<template>
  <div class="bundle-page-container">
    <!-- 1. HERO BANNER SECTION -->
    <section class="bundle-hero-section">
      <div class="hero-backdrop-glow"></div>
      <div class="container hero-inner">
        <div class="bundle-vip-badge animate-fade-in">
          <span class="pulse-dot"></span>
          🔥 ĐẶC QUYỀN VIP BUNDLE 2026 — TIẾT KIỆM TỚI 62%
        </div>
        
        <h1 class="hero-title animate-slide-up">
          Sở Hữu Trọn Bộ <span class="gradient-blue-text">Tất Cả Khóa Học 2026</span><br/>
          Tăng 10X Hiệu Suất & Bứt Phá Sự Nghiệp
        </h1>

        <p class="hero-subtitle animate-slide-up">
          Lộ trình phát triển năng lực toàn diện từ <strong>AI Automation, Kỹ Năng Mềm</strong> đến <strong>Chuyên Môn Vận Hành & Data Analytics</strong>. Sở hữu trọn đời với đặc quyền cập nhật bài học mới miễn phí trong suốt năm 2026!
        </p>

        <!-- Hero Stats Row -->
        <div class="hero-stats-grid">
          <div class="stat-item">
            <span class="stat-num">8+</span>
            <span class="stat-desc">Khóa Học Cao Cấp</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <span class="stat-num">10,000+</span>
            <span class="stat-desc">Học Viên Tin Dùng</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <span class="stat-num">4.9 / 5.0</span>
            <span class="stat-desc">⭐ 500+ Đánh Giá Học Viên</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <span class="stat-num">Trọn Đời</span>
            <span class="stat-desc">Quyền Truy Cập & Hỗ Trợ</span>
          </div>
        </div>

        <div class="hero-cta-group">
          <a href="#bundle-packages" class="btn btn-bundle-primary">
            🚀 MUA BUNDLE 2026 GIẢM 62% NGAY
          </a>
          <a href="https://zalo.me" target="_blank" class="btn btn-bundle-secondary">
            💬 TƯ VẤN LỘ TRÌNH 1-1 QUA ZALO
          </a>
        </div>
      </div>
    </section>

    <!-- 2. BUNDLE PACKAGES SECTION -->
    <section id="bundle-packages" class="bundle-packages-section container">
      <div class="section-header text-center">
        <span class="sub-heading-tag">CÁC GÓI COMBO TỐI ƯU</span>
        <h2>Lựa Chọn <span class="highlight-blue">Gói Bundle Phù Hợp</span> Với Bạn</h2>
        <p>Tiết kiệm tối đa chi phí và sở hữu kiến thức thực chiến ứng dụng ngay vào công việc</p>
      </div>

      <div v-if="bundles.length === 0" class="empty-bundles-card text-center py-12" style="background: var(--bg-card, #ffffff); border: 1px dashed var(--border-color, #e2e8f0); border-radius: 16px; padding: 48px 24px; margin: 24px 0;">
        <div style="font-size: 48px; margin-bottom: 16px;">🎁</div>
        <h3 style="font-size: 20px; font-weight: 700; color: var(--text-color, #1e293b); margin-bottom: 8px;">Chưa có gói Combo nào được tạo</h3>
        <p style="color: var(--text-muted, #64748b); max-width: 500px; margin: 0 auto 24px; font-size: 15px; line-height: 1.6;">
          Các gói Combo khóa học với ưu đãi lớn hiện đang được ban quản trị cập nhật. Vui lòng quay lại sau hoặc tham khảo các khóa học lẻ hiện có!
        </p>
        <router-link to="/courses/ai" class="btn primary-gradient-btn" style="display: inline-block; padding: 12px 28px; text-decoration: none;">
          Khám Phá Khóa Học
        </router-link>
      </div>

      <div v-else class="packages-grid">
        <!-- DYNAMIC BACKEND BUNDLES -->
        <div 
          v-for="b in bundles" 
          :key="b.id || b.handle" 
          class="package-card"
          :class="{'featured-master-card': (b.handle && (b.handle.includes('master') || b.handle.includes('vip'))), 'standard-card': !(b.handle && b.handle.includes('master'))}"
        >
          <div v-if="b.handle && (b.handle.includes('master') || b.handle.includes('vip'))" class="popular-ribbon">🔥 BEST SELLER</div>
          <div class="card-header">
            <span class="package-tag">{{ b.handle && b.handle.includes('master') ? 'MASTER VIP ALL-IN-ONE' : 'GÓI COMBO BUNDLE' }}</span>
            <h3 class="package-title">{{ b.title }}</h3>
            <p class="package-subtitle">{{ b.description || 'Trọn bộ các khóa học tối ưu lộ trình phát triển' }}</p>
          </div>

          <div class="price-box">
            <div class="price-row">
              <span class="original-price" v-if="b.original_price || b.originalPrice">{{ formatPrice(b.original_price || b.originalPrice) }}</span>
              <span class="discount-badge" v-if="(b.original_price || b.originalPrice) > b.price">
                TIẾT KIỆM {{ Math.round((1 - b.price / (b.original_price || b.originalPrice)) * 100) }}%
              </span>
            </div>
            <div class="main-price">
              <span class="amount">{{ formatPriceNumber(b.price) }}</span><span class="currency">đ</span>
              <span class="billing-note">/ sở hữu trọn đời</span>
            </div>
          </div>

          <div class="features-list">
            <h4>📚 KHÓA HỌC BAO GỒM:</h4>
            <ul>
              <li v-for="c in (b.courses || [])" :key="c.id">
                <i class="check-icon">✓</i> <strong>{{ c.title }}</strong>
              </li>
              <li v-if="!b.courses || b.courses.length === 0">
                <i class="check-icon">✓</i> Trọn bộ khóa học chuyên sâu
              </li>
            </ul>

            <!-- BONUS GIFTS SECTION -->
            <div v-if="(b.gift_courses || b.giftCourses) && (b.gift_courses || b.giftCourses).length > 0" class="gift-courses-box mt-3" style="padding: 12px; background: rgba(245, 158, 11, 0.08); border-radius: 8px; border: 1px solid rgba(245, 158, 11, 0.25);">
              <h5 style="color: #d97706; font-size: 13px; font-weight: bold; margin-bottom: 6px;">🎁 QUÀ TẶNG ĐẶC BIỆT KÈM THEO:</h5>
              <ul style="list-style: none; padding: 0; margin: 0;">
                <li v-for="g in (b.gift_courses || b.giftCourses)" :key="g.id" style="font-size: 13px; color: #92400e; margin-bottom: 4px;">
                  ✨ Tặng miễn phí: <strong>{{ g.title }}</strong>
                </li>
              </ul>
            </div>
          </div>

          <div class="card-footer mt-4">
            <button @click="handleEnrollBundle(b)" class="btn btn-buy-now primary-gradient-btn">
              SỞ HỮU GÓI BUNDLE NGAY
            </button>
            <span class="guarantee-text" v-if="b.handle && b.handle.includes('master')">🛡️ Cam kết hoàn tiền 100% nếu không hài lòng trong 7 ngày</span>
          </div>
        </div>
      </div>
    </section>

    <!-- 4. REASONS TO CHOOSE ACC BUNDLE -->
    <section class="why-bundle-section">
      <div class="container">
        <div class="section-header text-center">
          <h2>Tại Sao Nên Chọn <span class="highlight-blue">Bundle 2026</span>?</h2>
          <p>Trải nghiệm học tập chuẩn quốc tế được xây dựng bởi đội ngũ chuyên gia hàng đầu</p>
        </div>

        <div class="reasons-grid">
          <div class="reason-card">
            <div class="reason-icon">💰</div>
            <h3>Tiết Kiệm Chi Phí Tối Đa</h3>
            <p>Sở hữu trọn bộ 8+ khóa học với chi phí ưu đãi giảm tới 62% so với đăng ký từng khóa lẻ.</p>
          </div>

          <div class="reason-card">
            <div class="reason-icon">🔄</div>
            <h3>Cập Nhật Bài Học Miễn Phí</h3>
            <p>Nhận các cập nhật kiến thức AI, công cụ mới và các khóa học mới phát hành trong năm 2026 mà không tốn thêm chi phí.</p>
          </div>

          <div class="reason-card">
            <div class="reason-icon">🤝</div>
            <h3>Hỗ Trợ Thực Hành 1-1</h3>
            <p>Giải đáp trực tiếp các vướng mắc thực tế công việc từ đội ngũ Chuyên gia Mentor thông qua nhóm Zalo VIP.</p>
          </div>

          <div class="reason-card">
            <div class="reason-icon">📜</div>
            <h3>Chứng Nhận Chuẩn Doanh Nghiệp</h3>
            <p>Cấp chứng nhận tốt nghiệp sau khi hoàn thành khóa học, giúp nâng cao uy tín trong hồ sơ năng lực.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 5. STUDENT TESTIMONIALS SECTION -->
    <section class="bundle-testimonials-section container">
      <div class="section-header text-center">
        <span class="sub-heading-tag">CÂU CHUYỆN THÀNH CÔNG</span>
        <h2>Học Viên Nói Gì Về <span class="highlight-blue">Bundle ACC Academy</span>?</h2>
      </div>

      <div class="testimonials-slider-grid">
        <div class="testimonial-card">
          <div class="rating-stars">⭐⭐⭐⭐⭐</div>
          <p class="review-text">
            "Sở hữu gói Bundle 2026 là quyết định đầu tư hời nhất năm của mình! Mình đã áp dụng ChatGPT Work Automation và Excel AI để tự động hóa toàn bộ báo cáo tuần cho ban giám đốc, giảm bớt 80% thời gian thủ công."
          </p>
          <div class="reviewer-meta">
            <div class="reviewer-avatar">LN</div>
            <div class="reviewer-info">
              <strong>Lê Nguyễn Hoàng Nam</strong>
              <span>Trưởng phòng Phân tích Dữ liệu — Vinamilk</span>
            </div>
          </div>
        </div>

        <div class="testimonial-card">
          <div class="rating-stars">⭐⭐⭐⭐⭐</div>
          <p class="review-text">
            "Khóa học AI Center of Excellence và Gen AI Studio giúp đội ngũ Marketing của công ty sản xuất hình ảnh và TVC quảng cáo nhanh gấp 5 lần mà chi phí sản xuất lại giảm hẳn một nửa!"
          </p>
          <div class="reviewer-meta">
            <div class="reviewer-avatar">TH</div>
            <div class="reviewer-info">
              <strong>Trần Hương Thảo</strong>
              <span>CMO — Sendo E-commerce</span>
            </div>
          </div>
        </div>

        <div class="testimonial-card">
          <div class="rating-stars">⭐⭐⭐⭐⭐</div>
          <p class="review-text">
            "Chất lượng video HD sắc nét, giảng viên giảng dễ hiểu và thực chiến. Nhóm Zalo VIP hỗ trợ giải đáp siêu nhanh ngay cả ngoài giờ hành chính."
          </p>
          <div class="reviewer-meta">
            <div class="reviewer-avatar">PK</div>
            <div class="reviewer-info">
              <strong>Phạm Minh Khoa</strong>
              <span>Founder & Manager — TechStartup</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 6. FAQ ACCORDION SECTION -->
    <section class="bundle-faq-section container">
      <div class="section-header text-center">
        <h2>Câu Hỏi Thường Gặp (FAQ)</h2>
      </div>

      <div class="faq-accordion-list">
        <div 
          v-for="(faq, index) in faqs" 
          :key="index" 
          class="faq-item"
          :class="{ active: openFaq === index }"
          @click="toggleFaq(index)"
        >
          <div class="faq-question">
            <span>{{ faq.q }}</span>
            <span class="faq-toggle-icon">{{ openFaq === index ? '−' : '+' }}</span>
          </div>
          <div v-if="openFaq === index" class="faq-answer">
            <p>{{ faq.a }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 7. STICKY FLOATING FOOTER BAR -->
    <div class="sticky-bundle-bar animate-slide-up" v-if="bundles.length > 0">
      <div class="container sticky-inner">
        <div class="sticky-info">
          <span class="sticky-title">🔥 {{ bundles[0].title }}</span>
          <span class="sticky-price">
            {{ formatPrice(bundles[0].price) }} 
            <small v-if="(bundles[0].original_price || bundles[0].originalPrice) > bundles[0].price">
              (Tiết kiệm {{ Math.round((1 - bundles[0].price / (bundles[0].original_price || bundles[0].originalPrice)) * 100) }}%)
            </small>
          </span>
        </div>
        <button @click="handleEnrollBundle(bundles[0])" class="btn btn-sticky-buy">
          ĐĂNG KÝ SỞ HỮU NGAY
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useCourseStore } from '@/stores/courses';

const router = useRouter();
const courseStore = useCourseStore();

const openFaq = ref(0);

const bundles = computed(() => courseStore.bundles);

const formatPrice = (val) => {
  if (!val) return '0đ';
  return val.toLocaleString('vi-VN') + 'đ';
};

const formatPriceNumber = (val) => {
  if (!val) return '0';
  return val.toLocaleString('vi-VN');
};

const toggleFaq = (idx) => {
  openFaq.value = openFaq.value === idx ? null : idx;
};

const handleEnrollBundle = async (bundleObj) => {
  if (!bundleObj) return;
  
  // If bundle has child courses, add child courses to cart
  if (bundleObj.courses && bundleObj.courses.length > 0) {
    for (const c of bundleObj.courses) {
      await courseStore.addToCart(c.id);
    }
  } else if (bundleObj.handle) {
    const course = courseStore.courses.find(c => c.handle === bundleObj.handle || c.category === 'bundles') || courseStore.courses[0];
    if (course) {
      await courseStore.addToCart(course.id);
    }
  }
  router.push('/cart');
};

const handleImageError = (e) => {
  e.target.src = 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?q=80&w=600&auto=format&fit=crop';
};

const faqs = ref([
  {
    q: 'Sau khi mua Bundle 2026 tôi có được học trọn đời không?',
    a: 'Có! Bạn sẽ sở hữu quyền truy cập trọn đời tất cả các khóa học trong gói Bundle 2026, học lại bất cứ khi nào và không bị giới hạn thời gian.'
  },
  {
    q: 'Hình thức học như thế nào?',
    a: 'Hình thức học linh hoạt kết hợp giữa Bài giảng Video HD tự học mọi lúc mọi nơi và các buổi Live Zoom trao đổi trực tiếp với Giảng viên.'
  },
  {
    q: 'ACC Academy có cấp chứng nhận sau khóa học không?',
    a: 'Có, sau khi hoàn thành xong từng khóa học và bài kiểm tra thực hành, bạn sẽ nhận được Chứng nhận Tốt nghiệp điện tử chính thức từ ACC Academy.'
  },
  {
    q: 'Doanh nghiệp của tôi có thể xuất hóa đơn VAT được không?',
    a: 'Hoàn toàn được! ACC Academy hỗ trợ xuất hóa đơn GTGT (VAT) điện tử hợp lệ cho các công ty và tổ chức.'
  }
]);

onMounted(() => {
  courseStore.fetchBundles();
  if (courseStore.courses.length === 0) {
    courseStore.fetchCourses();
  }
});
</script>

<style scoped src="@/styles/views/Bundles.css"></style>
