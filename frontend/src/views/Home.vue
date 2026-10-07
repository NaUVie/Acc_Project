<template>
  <div class="home-view">
    <!-- 1. Hero Section (Carousel) -->
    <section class="hero-carousel-section" aria-label="Hero carousel banner">
      <div class="carousel-container">
        <div 
          v-for="(slide, index) in heroSlides" 
          :key="index"
          class="carousel-slide"
          :class="{ active: currentSlide === index }"
        >
          <a v-if="slide.isExternal" :href="slide.link" target="_blank" rel="noopener" class="slide-link">
            <picture>
              <source media="(max-width: 768px)" :srcset="slide.mobileImage" />
              <img :src="slide.desktopImage" :alt="slide.title" class="slide-image" />
            </picture>
          </a>
          <router-link v-else :to="slide.link" class="slide-link">
            <picture>
              <source media="(max-width: 768px)" :srcset="slide.mobileImage" />
              <img :src="slide.desktopImage" :alt="slide.title" class="slide-image" />
            </picture>
          </router-link>
        </div>

        <!-- Slider Arrows -->
        <button class="carousel-arrow prev" @click="prevSlide" aria-label="Previous slide">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M15 18l-6-6 6-6" />
          </svg>
        </button>
        <button class="carousel-arrow next" @click="nextSlide" aria-label="Next slide">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 18l6-6-6-6" />
          </svg>
        </button>

        <!-- Slider Dots -->
        <div class="carousel-dots">
          <button 
            v-for="(slide, index) in heroSlides" 
            :key="index"
            class="carousel-dot"
            :class="{ active: currentSlide === index }"
            @click="setSlide(index)"
            :aria-label="'Go to slide ' + (index + 1)"
          ></button>
        </div>
      </div>
    </section>

    <!-- Stats Trigger Zone (Wrapper for Ecosystem and Stats Grid for counter trigger) -->
    <div class="stats-trigger-zone">
      <!-- 2. Ecosystem Section -->
      <section class="ecosystem-section">
        <div class="container">
          <!-- Top Centered Header with Word-by-Word Animation -->
          <div class="eco-header">
            <h2 class="eco-main-title" :class="{ 'animated': ecoTitleAnimated }">
              <span 
                v-for="(word, idx) in ecoTitleWords" 
                :key="idx" 
                class="word-span"
                :style="{ '--word-delay': `${idx * 0.1}s` }"
              >{{ word }}&nbsp;</span>
            </h2>
          </div>

          <div class="ecosystem-container">
            <div class="eco-left">
              <div class="eco-content">
                <p class="eco-desc">ACC Academy đồng hành cùng cá nhân, doanh nghiệp và tổ chức trong hành trình nâng cao năng lực, ứng dụng AI và chuyển đổi số vào thực tiễn.</p>
                <p class="eco-desc">Chúng tôi kết hợp Đào tạo – Tư vấn – Công nghệ – Chiến lược, giúp đội ngũ không chỉ hiểu công nghệ mà còn biết cách ứng dụng hiệu quả vào công việc, tối ưu quy trình và tạo ra giá trị tăng trưởng bền vững.</p>
              </div>
              <div class="eco-counter-box">
                <div class="eco-number">{{ formatNumber(ecoCount) }}+</div>
                <div class="eco-counter-desc">CHƯƠNG TRÌNH & DỰ ÁN ĐÀO TẠO – TƯ VẤN ĐÃ TRIỂN KHAI</div>
              </div>
            </div>

            <!-- Video Player Section (Replaces eco-center image & eco-right services list) -->
            <div class="eco-video-wrapper">
              <div class="eco-video-card" :class="{ 'is-playing': isVideoPlaying }">
                <video 
                  ref="ecoVideoRef" 
                  class="eco-video-element" 
                  poster="/images/CoE-Thumb.png"
                  controls
                  playsinline
                  :src="videoUrl"
                  @play="isVideoPlaying = true"
                  @pause="isVideoPlaying = false"
                  @ended="isVideoPlaying = false"
                ></video>
                <div v-if="!isVideoPlaying" class="video-play-overlay" @click="handlePlayVideo">
                  <div class="play-pulse-ring"></div>
                  <button class="play-btn-circle" aria-label="Phát video">
                    <svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor">
                      <polygon points="5 3 19 12 5 21 5 3"></polygon>
                    </svg>
                  </button>
                  <span class="play-btn-label">XEM VIDEO GIỚI THIỆU ACC ACADEMY</span>
                </div>
              </div>
            </div>
          </div>
      </div>
    </section>

      <!-- 3. Stats Section -->
      <section class="stats-section">
        <div class="container">
          <div class="stats-header">
            <h2 class="stats-title">Năng lực & Giá trị thực tiễn</h2>
            <p class="stats-subtitle">Mỗi chương trình đào tạo và tư vấn của ACC Academy được thiết kế dựa trên nhu cầu thực tế, hướng đến khả năng ứng dụng ngay và tạo ra giá trị bền vững cho cá nhân, doanh nghiệp và tổ chức.</p>
          </div>

          <div class="stats-grid">
            <div class="stat-card-item">
              <div class="stat-num-box">{{ formatNumber(leadersCount) }}+</div>
              <div class="stat-label">Học viên & Nhà quản lý</div>
              <div class="stat-desc">Đã tham gia các chương trình đào tạo, nâng cao năng lực và ứng dụng AI.</div>
            </div>
            <div class="stat-card-item">
              <div class="stat-num-box">{{ formatNumber(businessesCount) }}+</div>
              <div class="stat-label">Doanh nghiệp & Tổ chức</div>
              <div class="stat-desc">Đã đồng hành triển khai các chương trình đào tạo và tư vấn chuyên biệt.</div>
            </div>
            <div class="stat-card-item">
              <div class="stat-num-box">{{ formatNumber(marketsCount) }}+</div>
              <div class="stat-label">Thị trường Quốc tế</div>
              <div class="stat-desc">Mở rộng hoạt động đào tạo và kết nối chuyên gia tại nhiều thị trường.</div>
            </div>
            <div class="stat-card-item">
              <div class="stat-num-box">{{ formatNumber(npsCount) }}+</div>
              <div class="stat-label">NPS - Chỉ số Khuyến nghị Khách hàng</div>
              <div class="stat-desc">Phản ánh mức độ hài lòng và sẵn sàng giới thiệu ACC Academy đến đối tác khác.</div>
            </div>
          </div>
        </div>
      </section>
    </div>

    <!-- 4. Partner Logos Section -->
    <section class="partner-logos-section">
      <div class="partner-logos-header container">
        <h3 class="partner-logos-title">130+ doanh nghiệp hàng đầu đã hợp tác</h3>
      </div>
      
      <div class="partner-marquee-container">
        <!-- Row 1: Scroll Left -->
        <div class="partner-marquee-track partner-track-left">
          <div 
            v-for="(logo, idx) in partnerRow1" 
            :key="'r1-a-' + idx" 
            class="partner-logo-card"
          >
            <img :src="logo.src" :alt="logo.name" class="partner-logo-img" loading="lazy" referrerpolicy="no-referrer" />
          </div>
          <div 
            v-for="(logo, idx) in partnerRow1" 
            :key="'r1-b-' + idx" 
            class="partner-logo-card"
          >
            <img :src="logo.src" :alt="logo.name" class="partner-logo-img" loading="lazy" referrerpolicy="no-referrer" />
          </div>
        </div>

        <!-- Row 2: Scroll Right -->
        <div class="partner-marquee-track partner-track-right">
          <div 
            v-for="(logo, idx) in partnerRow2" 
            :key="'r2-a-' + idx" 
            class="partner-logo-card"
          >
            <img :src="logo.src" :alt="logo.name" class="partner-logo-img" loading="lazy" referrerpolicy="no-referrer" />
          </div>
          <div 
            v-for="(logo, idx) in partnerRow2" 
            :key="'r2-b-' + idx" 
            class="partner-logo-card"
          >
            <img :src="logo.src" :alt="logo.name" class="partner-logo-img" loading="lazy" referrerpolicy="no-referrer" />
          </div>
        </div>

        <!-- Row 3: Scroll Left -->
        <div class="partner-marquee-track partner-track-left-alt">
          <div 
            v-for="(logo, idx) in partnerRow3" 
            :key="'r3-a-' + idx" 
            class="partner-logo-card"
          >
            <img :src="logo.src" :alt="logo.name" class="partner-logo-img" loading="lazy" referrerpolicy="no-referrer" />
          </div>
          <div 
            v-for="(logo, idx) in partnerRow3" 
            :key="'r3-b-' + idx" 
            class="partner-logo-card"
          >
            <img :src="logo.src" :alt="logo.name" class="partner-logo-img" loading="lazy" referrerpolicy="no-referrer" />
          </div>
        </div>
      </div>
    </section>

    <!-- 5. Bento Grid Section -->
    <section class="bento-grid-section">
      <div class="container">
        <div class="bento-header">
          <h2 class="bento-title">Năng lực cốt lõi của ACC Academy</h2>
          <p class="bento-subtitle">
            ACC — Học viện Cổ phần Kết nối Tri thức — là đơn vị giáo dục chuyên biệt dành cho cá nhân và doanh nghiệp, được bảo chứng học thuật bởi Đại học Andrews (Hoa Kỳ).<br />
            <strong>Chúng tôi không bán khóa học.</strong><br />
            Chúng tôi kiến tạo năng lực có thể đo lường, đi cùng tổ chức của bạn đến kết quả thực
          </p>
        </div>

        <div class="bento-grid-container">
          <div 
            v-for="(card, index) in bentoCards" 
            :key="card.id"
            class="bento-card"
            :class="[index === 0 ? 'card-wide' : 'card-square', card.bgClass]"
          >
            <router-link v-if="card.link" :to="card.link" class="bento-card-overlay-link"></router-link>
            
            <img v-if="card.bgImage" :src="card.bgImage" :alt="card.title" class="bento-card-bg" :class="card.bgImgClass" />
            
            <div class="bento-card-content" :class="card.contentClass">
              <h3 class="bento-card-title">{{ card.title }}</h3>
              <p class="bento-card-desc">{{ card.desc }}</p>
            </div>

            <div v-if="card.mockupImage" class="bento-card-bottom-mockup">
              <img :src="card.mockupImage" :alt="card.title" class="bento-mockup-img" />
            </div>
          </div>
        </div>
      </div>
    </section>


    <!-- 7. Comprehensive Training Solutions (Courses Grid Section) -->
    <section class="courses-section">
      <div class="container">
        <div class="courses-header">
          <h2 class="courses-title">Lịch đào tạo</h2>
          <!-- Filter Tabs / Navbar (All, Inhouse, Individual) -->
          <div class="course-filter-tabs">
            <button 
              class="tab-btn" 
              :class="{ active: currentCourseCategory === 'all' }"
              @click="currentCourseCategory = 'all'"
            >
              Tất cả
            </button>
            <button 
              class="tab-btn" 
              :class="{ active: currentCourseCategory === 'dao-tao-doanh-nghiep' }"
              @click="currentCourseCategory = 'dao-tao-doanh-nghiep'"
            >
               Đào tạo Inhouse
            </button>
            <button 
              class="tab-btn" 
              :class="{ active: currentCourseCategory === 'dao-tao-ca-nhan' }"
              @click="currentCourseCategory = 'dao-tao-ca-nhan'"
            >
               Đào tạo Cá nhân
            </button>
          </div>
        </div>

        <div class="home-courses-grid">
          <div 
            v-for="course in displayedCourses" 
            :key="course.id"
            class="home-course-card"
          >
            <router-link :to="'/course/' + (course.handle || course.id)" class="home-course-img-link">
              <div class="home-course-img-box">
                <img :src="course.image || '/images/Square-Cover-_1.webp'" :alt="course.title" class="home-course-img" loading="lazy" />
              </div>
            </router-link>
            
            <div class="home-course-body">
              <h3 class="home-course-heading">
                <router-link :to="'/course/' + (course.handle || course.id)">{{ course.title }}</router-link>
              </h3>
              <!-- <p class="home-course-desc">{{ stripHtml(course.description) }}</p> -->
              
              <div class="home-course-footer">
                <router-link :to="'/course/' + (course.handle || course.id)" class="btn-link-stretch" aria-label="Xem chi tiết khóa học">
                  <div class="arrow-stretch-box">
                    <span class="line-body"></span>
                    <span class="arrow-tip"></span>
                  </div>
                </router-link>
              </div>
            </div>
          </div>
        </div>

        <!-- Load More Button -->
        <div class="load-more-courses-container" v-if="hasMoreCourses">
          <button @click="loadMoreCourses" class="btn-load-more-courses">
            <span>Xem thêm khóa học</span>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M6 9l6 6 6-6"/>
            </svg>
          </button>
        </div>
      </div>
    </section>

    <!-- 8. Featured Lecturers Section -->
    <section class="featured-lecturers-section">
      <div class="container">
        <div class="blogs-header-row">
          <div class="blogs-header-left">
            <h2 class="blogs-heading">Đội ngũ Giảng viên & Chuyên gia Thực chiến</h2>
          </div>
          <router-link to="/doi-ngu-giang-vien" class="header-link-with-arrow" aria-label="Xem tất cả giảng viên">
            <span class="header-link-text">Xem tất cả</span>
            <div class="btn-link-stretch">
              <div class="arrow-stretch-box">
                <span class="line-body"></span>
                <span class="arrow-tip"></span>
              </div>
            </div>
          </router-link>
        </div>

        <div class="home-lecturers-grid">
          <div 
            v-for="l in featuredLecturers" 
            :key="l.id" 
            class="home-lecturer-card-item"
          >
            <router-link :to="'/giang-vien/' + l.id" class="team-card-wrapper group">
              <div class="team-card-image-box">
                <img 
                  :src="l.avatar" 
                  :alt="l.name" 
                  class="team-card-img" 
                  @error="(e) => e.target.src = '/images/1_6.png'"
                  referrerpolicy="no-referrer" 
                />
                <!-- Dark Gradient Overlay -->
                <div class="team-card-gradient"></div>
                
                <!-- Bottom Info Box -->
                <div class="team-card-info-box">
                  <h3 class="team-card-name">{{ l.name }}</h3>
                  <div class="team-card-role-row">
                    <span class="accent-line"></span>
                    <span class="team-card-role">{{ l.title }}</span>
                  </div>
                </div>
              </div>
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- 9. Student Shared Feedback Section (Replaces Blog Section) -->
    <section class="student-feedback-section">
      <div class="container">
        <div class="blogs-header-row">
          <div class="blogs-header-left">
            <h2 class="blogs-heading">Cảm nhận từ Học viên ACC</h2>
          </div>
          <router-link to="/chia-se-hoc-vien" class="header-link-with-arrow" aria-label="Xem thêm chia sẻ học viên">
            <span class="header-link-text">Xem thêm</span>
            <div class="btn-link-stretch">
              <div class="arrow-stretch-box">
                <span class="line-body"></span>
                <span class="arrow-tip"></span>
              </div>
            </div>
          </router-link>
        </div>

        <div class="home-feedback-grid">
          <div 
            v-for="p in homeStudentFeedbacks" 
            :key="p.id" 
            class="home-feedback-card"
          >
            <div class="home-feedback-img-box" v-if="p.image">
              <img :src="p.image" :alt="p.name" class="home-feedback-img" referrerpolicy="no-referrer" />
            </div>
            <div class="home-feedback-body">
              <div class="home-student-profile">
                <img :src="p.avatar" :alt="p.name" class="home-profile-avatar" referrerpolicy="no-referrer" />
                <div>
                  <h4 class="home-profile-name">{{ p.name }}</h4>
                  <p class="home-profile-role">{{ p.role }} • {{ p.company }}</p>
                </div>
              </div>
              <div class="home-stars">★★★★★</div>
              <p class="home-quote-text">"{{ p.quote }}"</p>
              <!-- <span class="home-course-tag">{{ p.courseName }}</span> -->
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 10. CTA Section
    <section class="cta-banner-section">
      <div class="container">
        <div class="cta-banner-box">
          <div class="cta-banner-left">
            <h2 class="cta-banner-heading">Nâng tầm lợi thế cạnh tranh cùng ACC Academy</h2>
            <p class="cta-banner-desc">Nhận lộ trình tư vấn chi tiết từ chuyên gia của chúng tôi và thiết lập nền tảng chuyển đổi số bền vững cho cá nhân & doanh nghiệp của bạn.</p>
            <div class="cta-benefits-list">
              <div class="benefit-item">
                <span class="check-icon">✓</span>
                <span class="benefit-txt">Hệ sinh thái học tập đa chiều</span>
              </div>
              <div class="benefit-item">
                <span class="check-icon">✓</span>
                <span class="benefit-txt">Công cụ và Tư duy thực chiến</span>
              </div>
              <div class="benefit-item">
                <span class="check-icon">✓</span>
                <span class="benefit-txt">Cập nhật nội dung liên tục</span>
              </div>
            </div>
            <router-link to="/contact" class="cta-banner-btn">
              Kết nối với Chuyên gia
            </router-link>
          </div>
          <div class="cta-banner-right">
            <img src="/images/Right.png" alt="ACC Academy Consulting Team" class="cta-right-img" loading="lazy" />
          </div>
        </div>
      </div>
    </section> -->
  </div>

  <!-- Auto Pop-up Consultation Modal (Horizontal Name Card Style) -->
  <Transition name="modal-fade">
    <div v-if="isContactModalOpen" class="consult-modal-overlay" @click.self="closeContactModal">
      <div class="consult-card-visit-horizontal" role="dialog" aria-modal="true" aria-labelledby="consult-modal-title">
        <button class="consult-modal-close" @click="closeContactModal" aria-label="Đóng cửa sổ">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>

        <!-- Left Side: ACC Logo & Brand Identity -->
        <div class="card-visit-left">
          <div class="card-logo-box">
            <img src="/images/logo3.png" alt="ACC Academy Logo" class="card-acc-logo" />
            <h2 class="card-acc-brand">ACC ACADEMY</h2>
            <p class="card-acc-slogan">Kiến tạo năng lực — Dẫn dắt chuyển đổi bền vững</p>
          </div>
          <div class="card-decoration-pattern"></div>
        </div>

        <!-- Right Side: Compact Form -->
        <div class="card-visit-right">
          <div class="card-visit-header">
            <h3 id="consult-modal-title" class="card-visit-title">Đăng Ký Tư Vấn</h3>
            <p class="card-visit-desc">Nhận tư vấn trực tiếp từ chuyên gia</p>
          </div>

          <form @submit.prevent="submitContactModal" class="card-visit-form">
            <div class="card-input-wrap">
              <input 
                v-model="contactForm.fullname" 
                type="text" 
                class="card-input" 
                placeholder="Họ và tên *" 
                required 
              />
            </div>

            <div class="card-input-wrap">
              <input 
                v-model="contactForm.phone" 
                type="tel" 
                class="card-input" 
                placeholder="Số điện thoại *" 
                required 
              />
            </div>

            <div class="card-input-wrap">
              <input 
                v-model="contactForm.email" 
                type="email" 
                class="card-input" 
                placeholder="Email *" 
                required 
              />
            </div>

            <button type="submit" class="card-submit-btn" :disabled="isSubmittingContact">
              <span v-if="!isSubmittingContact">Đăng Ký Ngay &rarr;</span>
              <span v-else>Đang gửi...</span>
            </button>
          </form>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useCourseStore } from '@/stores/courses';
import { useTestimonialStore } from '@/stores/testimonials';
import { lecturersData } from '@/data/lecturers';
import { photoTestimonialsData } from '@/data/testimonials';
import { stripHtml } from '@/utils/stripHtml';

const courseStore = useCourseStore();
const testimonialStore = useTestimonialStore();

// Ecosystem Video Player
const ecoVideoRef = ref(null);
const isVideoPlaying = ref(false);
const videoUrl = ref('/videos/intro.mp4');

const handlePlayVideo = () => {
  if (ecoVideoRef.value) {
    ecoVideoRef.value.play();
    isVideoPlaying.value = true;
  }
};

// 1. Hero Carousel
const currentSlide = ref(0);
const heroSlides = computed(() => {
  if (courseStore.banners && courseStore.banners.length > 0) {
    return courseStore.banners.map(b => ({
      desktopImage: b.desktop_image,
      mobileImage: b.mobile_image || b.desktop_image,
      link: b.link || '/',
      title: b.title,
      isExternal: !!b.is_external
    }));
  }
  return [
    {
      desktopImage: '/images/CoE-Web.png',
      mobileImage: '/images/CoE-Mobile.png',
      link: '/corporate/coe',
      title: 'AI Center of Excellence'
    },
    {
      desktopImage: '/images/Website_dd1fbf97-8fbe-44ed-bfd9-1eaaa069fdb3.png',
      mobileImage: '/images/SEB_Mobile.png',
      link: '/courses/category/ky-nang-ai',
      title: 'ChatGPT Work Automation'
    },
    {
      desktopImage: '/images/website_bbadf8f3-a076-4351-ba9e-f9f077fd6271.webp',
      mobileImage: '/images/mobile_34381454-0cf6-416c-9487-9a341853b38f.webp',
      link: 'https://teamlacquan.vn/',
      title: 'teamlacquan.vn',
      isExternal: true
    }
  ];
});

let heroInterval = null;
const startHeroAutoplay = () => {
  heroInterval = setInterval(() => {
    const len = heroSlides.value.length || 1;
    currentSlide.value = (currentSlide.value + 1) % len;
  }, 5000);
};

const stopHeroAutoplay = () => {
  if (heroInterval) clearInterval(heroInterval);
};

const setSlide = (index) => {
  currentSlide.value = index;
  stopHeroAutoplay();
  startHeroAutoplay();
};

const prevSlide = () => {
  const len = heroSlides.value.length || 1;
  currentSlide.value = (currentSlide.value - 1 + len) % len;
  stopHeroAutoplay();
  startHeroAutoplay();
};

const nextSlide = () => {
  const len = heroSlides.value.length || 1;
  currentSlide.value = (currentSlide.value + 1) % len;
  stopHeroAutoplay();
  startHeroAutoplay();
};

// 2. Ecosystem & Stats Counter Animation
const ecoTitleWords = ['Kiến', 'tạo', 'năng', 'lực', '–', 'Dẫn', 'dắt', 'chuyển', 'đổi', 'bền', 'vững'];
const ecoTitleAnimated = ref(false);

const setupEcoTitleObserver = () => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        ecoTitleAnimated.value = true;
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });

  const target = document.querySelector('.eco-main-title');
  if (target) observer.observe(target);
};

const ecoCount = ref(0);
const leadersCount = ref(0);
const businessesCount = ref(0);
const marketsCount = ref(0);
const npsCount = ref(0);
const countersAnimated = ref(false);

const animateNumber = (refVar, target, duration = 1500) => {
  let start = null;
  const step = (timestamp) => {
    if (!start) start = timestamp;
    const progress = Math.min((timestamp - start) / duration, 1);
    refVar.value = Math.floor(progress * target);
    if (progress < 1) {
      window.requestAnimationFrame(step);
    } else {
      refVar.value = target;
    }
  };
  window.requestAnimationFrame(step);
};

const setupCountersObserver = () => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !countersAnimated.value) {
        countersAnimated.value = true;
        animateNumber(ecoCount, 500, 1200);
        animateNumber(leadersCount, 17000, 1800);
        animateNumber(businessesCount, 70, 1500);
        animateNumber(marketsCount, 7, 1000);
        animateNumber(npsCount, 85, 1200);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  const target = document.querySelector('.stats-trigger-zone');
  if (target) observer.observe(target);
};

const formatNumber = (value) => {
  return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
};

const formatPrice = (value) => {
  if (!value) return 'Liên hệ';
  if (typeof value === 'number') {
    return value.toLocaleString('vi-VN') + 'đ';
  }
  return value;
};

// 3. Partner Logo Stagger Reveal
const partnerRevealActive = ref(false);
const setupPartnerObserver = () => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        partnerRevealActive.value = true;
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.05 });

  const target = document.querySelector('.partner-logos-section');
  if (target) observer.observe(target);
};

const partnerLogos = [
  { name: 'Đối tác 1', src: 'https://drive.google.com/thumbnail?id=120WyoSixRMCuWCMFeNjFKxsDzt74filf&sz=w400' },
  { name: 'Đối tác 2', src: 'https://drive.google.com/thumbnail?id=1ZININwRW94lavoqqoJ3eAArE5v6vsyZ5&sz=w400' },
  { name: 'Đối tác 3', src: 'https://drive.google.com/thumbnail?id=1CU6Pq9-wx_l2DPlb7uigkGIvCtcl921E&sz=w400' },
  { name: 'Đối tác 4', src: 'https://drive.google.com/thumbnail?id=1miKA4icyQ_nAgwQe5vQge3bqg2W_f8zg&sz=w400' },
  { name: 'Đối tác 5', src: 'https://drive.google.com/thumbnail?id=1Dlbfhcst3Ql0nali2mMLnNSxFZXBR6fK&sz=w400' },
  { name: 'Đối tác 6', src: 'https://drive.google.com/thumbnail?id=1sGiCe18WnDNjwH_m6c3kwrdgQ5uSRUYA&sz=w400' },
  { name: 'Đối tác 7', src: 'https://drive.google.com/thumbnail?id=1aH1uD_pYe3TZRO-5HBo9ceAajh5IGKgy&sz=w400' },
  { name: 'Đối tác 8', src: 'https://drive.google.com/thumbnail?id=1jbZBxZePFiI7jO9z6WNtPp-ZG3whJH4v&sz=w400' },
  { name: 'Đối tác 9', src: 'https://drive.google.com/thumbnail?id=1sXKJCb-T7Js1ecD7f4_eKt9kAwx0F9eq&sz=w400' },
  { name: 'Đối tác 10', src: 'https://drive.google.com/thumbnail?id=1OKzXpaMCHfs4jB11rDbnpCcng6lEYfP7&sz=w400' },
  { name: 'Đối tác 11', src: 'https://drive.google.com/thumbnail?id=190mmLyYwA8nbyMM0vGs89E8j99EiXlCa&sz=w400' },
  { name: 'Đối tác 12', src: 'https://drive.google.com/thumbnail?id=12cvA0WcM4Fd6dQGAWTAc3SoJ3LaDOVuT&sz=w400' },
  { name: 'Đối tác 13', src: 'https://drive.google.com/thumbnail?id=1rgdDL5_RoP2A9UzeVP9sD0y8CrGWNA5y&sz=w400' },
  { name: 'Đối tác 14', src: 'https://drive.google.com/thumbnail?id=1lO81tFi07weL_E_FhVsDPRWf5pEJx8p3&sz=w400' },
  { name: 'Đối tác 15', src: 'https://drive.google.com/thumbnail?id=10cZRoXLI_WX6i-ck4JChUdeY1A5n19FI&sz=w400' },
  { name: 'Đối tác 16', src: 'https://drive.google.com/thumbnail?id=1ufMAQWi_tXQUdZsgTYf6-7UqqOPR8a7J&sz=w400' },
  { name: 'Đối tác 17', src: 'https://drive.google.com/thumbnail?id=1NQ-BN6gjTxEeHmktJMY3Nkig8ZnnqbF3&sz=w400' },
  { name: 'Đối tác 18', src: 'https://drive.google.com/thumbnail?id=15feRjlmeVcexzArlgwdsqxJ27SKRW5TU&sz=w400' },
  { name: 'Đối tác 19', src: 'https://drive.google.com/thumbnail?id=1WQWx_KXalgYMWRsOXOmo5ZOCamzf3kNn&sz=w400' },
  { name: 'Đối tác 20', src: 'https://drive.google.com/thumbnail?id=1_dQ3mr_uemCfvtRN863gzoymg1E8FSsk&sz=w400' },
  { name: 'Đối tác 21', src: 'https://drive.google.com/thumbnail?id=14CcrokSyvboMCfX7WnHY5QrirIJ3ocvR&sz=w400' },
  { name: 'Đối tác 22', src: 'https://drive.google.com/thumbnail?id=1PjAMuLct4GxI_9dI1kZByeZSCWdE_6T3&sz=w400' },
  { name: 'Đối tác 23', src: 'https://drive.google.com/thumbnail?id=1-7Wt7l-M20TIktuhoyAhwdzBzIxT-JUK&sz=w400' },
  { name: 'Đối tác 24', src: 'https://drive.google.com/thumbnail?id=1jN-yv_tRoxpZmDz8l1OF7mUxQHeeaqLY&sz=w400' },
  { name: 'Đối tác 25', src: 'https://drive.google.com/thumbnail?id=1Z95HJjP0kbyi-ZX4zOabhIXrdeiaCZjm&sz=w400' },
  { name: 'Đối tác 26', src: 'https://drive.google.com/thumbnail?id=1ZHO-C-hRijrD8I0hcJ8lDKw0lGugyMSZ&sz=w400' },
  { name: 'Đối tác 27', src: 'https://drive.google.com/thumbnail?id=1SUnrjvYW-qpBXVIYr0I-NjrgDdc6zdUS&sz=w400' },
  { name: 'Đối tác 28', src: 'https://drive.google.com/thumbnail?id=1T6B2Q7d1x4ZWvAiAJiazhzyTQbxJBx8h&sz=w400' },
  { name: 'Đối tác 29', src: 'https://drive.google.com/thumbnail?id=1s41ADCnm6LrZ4IOJWu-nF2sv9JfjTHph&sz=w400' },
  { name: 'Đối tác 30', src: 'https://drive.google.com/thumbnail?id=1GCtdR5NBW2NjUufCYjFFvZ8XbGuGXc75&sz=w400' },
  { name: 'Đối tác 31', src: 'https://drive.google.com/thumbnail?id=1uJ51n-lVSm7aTcsrPOuTarojMCAZbNlE&sz=w400' },
  { name: 'Đối tác 32', src: 'https://drive.google.com/thumbnail?id=1Cu0Couaqnm93r6GKM1FTTW330lzqna-e&sz=w400' },
  { name: 'Đối tác 33', src: 'https://drive.google.com/thumbnail?id=1WECHK_RnEAWubBw0eHRkCHb8z71212wG&sz=w400' },
  { name: 'Đối tác 34', src: 'https://drive.google.com/thumbnail?id=1MevpznNHCUU2GQmYIe6quFIR5cGfG1sz&sz=w400' },
  { name: 'Đối tác 35', src: 'https://drive.google.com/thumbnail?id=17IIf8l_Anaqp9ILV4h396PdWQQLdaVoY&sz=w400' },
  { name: 'Đối tác 36', src: 'https://drive.google.com/thumbnail?id=1XzfK-Oeq2HeNF7iwoA9js3_rEwhZh0Ji&sz=w400' },
  { name: 'Đối tác 37', src: 'https://drive.google.com/thumbnail?id=14_Avx4km9PtHFkTImKtWH1esW9poG7um&sz=w400' },
  { name: 'Đối tác 38', src: 'https://drive.google.com/thumbnail?id=1pWx9GEZNdXvlRIdCRbkqPUsqYRO5jyqa&sz=w400' },
  { name: 'Đối tác 39', src: 'https://drive.google.com/thumbnail?id=16TV8qMAx40306O142bH_sL6owU5UoO1_&sz=w400' },
  { name: 'Đối tác 40', src: 'https://drive.google.com/thumbnail?id=1BMmqenc3pFBjqyp_WS0pnoJ1lbwcPrrU&sz=w400' },
  { name: 'Đối tác 41', src: 'https://drive.google.com/thumbnail?id=1ax6Rmhz1aL3MUIwIyNo0-HlaqudDYakP&sz=w400' },
  { name: 'Đối tác 42', src: 'https://drive.google.com/thumbnail?id=1pymUpQFy1j1PrXnJlty8yDEVws21IhSy&sz=w400' },
  { name: 'Đối tác 43', src: 'https://drive.google.com/thumbnail?id=1SAc5tUjOP5m3aprac8wmA4c6k4m5hO-e&sz=w400' },
  { name: 'Đối tác 44', src: 'https://drive.google.com/thumbnail?id=1G0mudSS745i6_J2_Rs-NNU8CxXH68HIJ&sz=w400' },
  { name: 'Đối tác 45', src: 'https://drive.google.com/thumbnail?id=1wye7-s1fqNwKETYM8vLAIqZOGW-gjl1H&sz=w400' },
  { name: 'Đối tác 46', src: 'https://drive.google.com/thumbnail?id=1CFeSldwnd5CpM7tz-bgGIEwxTOS2KUdK&sz=w400' },
  { name: 'Đối tác 47', src: 'https://drive.google.com/thumbnail?id=1ggXZxHVSV4hHkPCWKJCIWFcXhfHlZudG&sz=w400' },
  { name: 'Đối tác 48', src: 'https://drive.google.com/thumbnail?id=12AbVpU4bOpv7PIsqo-eOvicHtFbfHWHt&sz=w400' },
  { name: 'Đối tác 49', src: 'https://drive.google.com/thumbnail?id=1kNJjeM4tUnyeDlCoC6auso9SaTSeFIWL&sz=w400' },
  { name: 'Đối tác 50', src: 'https://drive.google.com/thumbnail?id=1MSd3Ktvxb304WArrc1rhxpPoAuAkJnSH&sz=w400' },
  { name: 'Đối tác 51', src: 'https://drive.google.com/thumbnail?id=1_tEAHiG3uPfY4Y0DS_8rtz0b92-a1Fo4&sz=w400' },
  { name: 'Đối tác 52', src: 'https://drive.google.com/thumbnail?id=15kjfiY7U4pZKyT4HawZEP9yob288R-0l&sz=w400' },
  { name: 'Đối tác 53', src: 'https://drive.google.com/thumbnail?id=1XwfM6mUdCqS2-76GP4oll1m4GWhO_BxF&sz=w400' },
  { name: 'Đối tác 54', src: 'https://drive.google.com/thumbnail?id=1SPLTzaigKzWmIEkISM2qk7bTI8aEeXMX&sz=w400' },
  { name: 'Đối tác 55', src: 'https://drive.google.com/thumbnail?id=1ZArWUKL0haz3lYY296uztgrMo1eVJWO_&sz=w400' },
  { name: 'Đối tác 56', src: 'https://drive.google.com/thumbnail?id=1eMdG6BEA3eqfKwMAXe9GejuagJ4Gn6Vv&sz=w400' },
  { name: 'Đối tác 57', src: 'https://drive.google.com/thumbnail?id=12ayrz-9fIeLzqbiOlkObcvtp-lItir_L&sz=w400' },
  { name: 'Đối tác 58', src: 'https://drive.google.com/thumbnail?id=1lLQQXfg8ls5VDy6WpPMcf1Bp6IM3gHgQ&sz=w400' },
  { name: 'Đối tác 59', src: 'https://drive.google.com/thumbnail?id=1j-Kf5Uyi1RdLiFdX-GvwxdfzxpBhH7QA&sz=w400' },
  { name: 'Đối tác 60', src: 'https://drive.google.com/thumbnail?id=1KrQqyWkFC6FAVDGMGiFFRCIr67ANR-Ea&sz=w400' },
  { name: 'Đối tác 61', src: 'https://drive.google.com/thumbnail?id=1qThDrr6Hz1BmaM83eaeskWgT5LgW0MqZ&sz=w400' },
  { name: 'Đối tác 62', src: 'https://drive.google.com/thumbnail?id=1yKn61_xXJ_h55nnu9vyALSw3rmGyh9ot&sz=w400' },
  { name: 'Đối tác 63', src: 'https://drive.google.com/thumbnail?id=1rwY5qoFRf2-aYzNVe8pPO8HTjRAKSsrR&sz=w400' },
  { name: 'Đối tác 64', src: 'https://drive.google.com/thumbnail?id=1Z-D8WamdM1bzigBeULCw3KnCCch-ttO6&sz=w400' },
  { name: 'Đối tác 65', src: 'https://drive.google.com/thumbnail?id=18FNKsF6wO-LRzNePn5jjhFtB8O7wS9WE&sz=w400' },
  { name: 'Đối tác 66', src: 'https://drive.google.com/thumbnail?id=1LAZO3KMSDkXyoT_88DndMmWF0iMopnLr&sz=w400' },
  { name: 'Đối tác 67', src: 'https://drive.google.com/thumbnail?id=1dmBuMPOqwce4FRw3ZCmGHorXDSAArVvF&sz=w400' },
  { name: 'Đối tác 68', src: 'https://drive.google.com/thumbnail?id=1wUgmS8qzZBTe6RLj9sf4OOcjch0ZJqPi&sz=w400' },
  { name: 'Đối tác 69', src: 'https://drive.google.com/thumbnail?id=18HGT3Yx-9QoYBvB3ClJ245tcNTMgPOlF&sz=w400' },
  { name: 'Đối tác 70', src: 'https://drive.google.com/thumbnail?id=1mEvwIxggXua93bOY6jWGch6iyIE10MR2&sz=w400' },
  { name: 'Đối tác 71', src: 'https://drive.google.com/thumbnail?id=1Y2gLhTFBMNk1oa6aJ2_S4IKbvjTJU5dN&sz=w400' },
  { name: 'Đối tác 72', src: 'https://drive.google.com/thumbnail?id=1EVY71WOK_hI6phsI8AiOVcLAXJHNmM4a&sz=w400' },
  { name: 'Đối tác 73', src: 'https://drive.google.com/thumbnail?id=1G4L_6qylDTCSQikUtRILWDNQ41NU3deg&sz=w400' },
  { name: 'Đối tác 74', src: 'https://drive.google.com/thumbnail?id=1bW2n8z-7XyWMeijcPcsojfMspeuY7WjW&sz=w400' },
  { name: 'Đối tác 75', src: 'https://drive.google.com/thumbnail?id=1DlZsj7-rZWsfK0rQvfAGEhLXscKRl37t&sz=w400' },
  { name: 'Đối tác 76', src: 'https://drive.google.com/thumbnail?id=1rtWXl0N-hj4pqZhfv2cOT9hQn3OpQCF_&sz=w400' },
  { name: 'Đối tác 77', src: 'https://drive.google.com/thumbnail?id=1oN8m3U0QMaQQQ3i1QQlZB-H4uF6fU7ZL&sz=w400' },
  { name: 'Đối tác 78', src: 'https://drive.google.com/thumbnail?id=1DiXzp1Lwo4OwKUJ-PbZWhtixZp1aykYU&sz=w400' },
  { name: 'Đối tác 79', src: 'https://drive.google.com/thumbnail?id=1ItAfJWV5DOvYrbW4K7w7-o-kSHi_OL41&sz=w400' },
  { name: 'Đối tác 80', src: 'https://drive.google.com/thumbnail?id=1kKYwfJovi6c7m-z48C_OcUkjltAOID8G&sz=w400' },
  { name: 'Đối tác 81', src: 'https://drive.google.com/thumbnail?id=1hoIlb72TV0b0Yk386S07NE7jZsLshbWr&sz=w400' },
  { name: 'Đối tác 82', src: 'https://drive.google.com/thumbnail?id=1SPKg-rBYS9kzNc01R3Y-xkK07Yapazo1&sz=w400' },
  { name: 'Đối tác 83', src: 'https://drive.google.com/thumbnail?id=1CkiWy5x2h6ms_-bAfq8U0CBMbfXjFhgR&sz=w400' },
  { name: 'Đối tác 84', src: 'https://drive.google.com/thumbnail?id=1-aCY9bbKYCZvLKAS7g2hTbeYAahxn9ce&sz=w400' },
  { name: 'Đối tác 85', src: 'https://drive.google.com/thumbnail?id=1MoJWz3nLn6_SRqQo8Y91dHm85na83ThN&sz=w400' },
  { name: 'Đối tác 86', src: 'https://drive.google.com/thumbnail?id=1QscZSgKo5jrQ0SM_i5JUC9EbecmkerQy&sz=w400' },
  { name: 'Đối tác 87', src: 'https://drive.google.com/thumbnail?id=1cru7AvS7-KTYBdy8Dpts1nmTb_i_J-D2&sz=w400' },
  { name: 'Đối tác 88', src: 'https://drive.google.com/thumbnail?id=1eakztvwxkhX9M_J854nUVIQJ36ZFp8u9&sz=w400' },
  { name: 'Đối tác 89', src: 'https://drive.google.com/thumbnail?id=1GolYmzQQeTksxLZ9OzNh9E4lzO0qkaGy&sz=w400' },
  { name: 'Đối tác 90', src: 'https://drive.google.com/thumbnail?id=1IqjHOM8cK_hKkAcjvXClVBdSj48u1cvY&sz=w400' },
  { name: 'Đối tác 91', src: 'https://drive.google.com/thumbnail?id=1VK0j8htIsmmWkRlyuQQIWf8VVjmjYvSZ&sz=w400' },
  { name: 'Đối tác 92', src: 'https://drive.google.com/thumbnail?id=1GnuUNQ9vHzjcidL2R94DmMNlQ151hw8c&sz=w400' },
  { name: 'Đối tác 93', src: 'https://drive.google.com/thumbnail?id=1rZrJpu1jP5bVb4n8kbLZWzBkCXzNtF0p&sz=w400' },
  { name: 'Đối tác 94', src: 'https://drive.google.com/thumbnail?id=14_mhAywmIgu0Yt0O456gdExBh3BUaLph&sz=w400' },
  { name: 'Đối tác 95', src: 'https://drive.google.com/thumbnail?id=1olDnKoLEABJxmZts5dDoP91hvI_y73v-&sz=w400' },
  { name: 'Đối tác 96', src: 'https://drive.google.com/thumbnail?id=1JTonvCg0TMv3NMavsYbJY30EDSvVs5Yp&sz=w400' },
  { name: 'Đối tác 97', src: 'https://drive.google.com/thumbnail?id=1YkhMOYnE4hoRb3a-_7fiMJfyqUzOlCzL&sz=w400' },
  { name: 'Đối tác 98', src: 'https://drive.google.com/thumbnail?id=1jd1XGMjSn7U9fk-IFOG9J48toAiZGNaZ&sz=w400' },
  { name: 'Đối tác 99', src: 'https://drive.google.com/thumbnail?id=1G_q036b7RdiKHggbjS7gQtNw2DCJRCUl&sz=w400' },
  { name: 'Đối tác 100', src: 'https://drive.google.com/thumbnail?id=1cfVieLJImP_b1Uf0MSQeD2N-CERiP5Ej&sz=w400' },
  { name: 'Đối tác 101', src: 'https://drive.google.com/thumbnail?id=18Z1TSXdqx3GcF3DqW-MkBDtgEwqIXSYd&sz=w400' },
  { name: 'Đối tác 102', src: 'https://drive.google.com/thumbnail?id=1wbxM_eVd5W4ETIxHC7W4l_bQ4PQDXCo4&sz=w400' },
  { name: 'Đối tác 103', src: 'https://drive.google.com/thumbnail?id=1jqFA2iW2lAnz3L-bDe1F_xBJB1jOlWl7&sz=w400' },
  { name: 'Đối tác 104', src: 'https://drive.google.com/thumbnail?id=134RVvEMjtfL5pEaxNxUvESL2Hkh6HbeN&sz=w400' },
  { name: 'Đối tác 105', src: 'https://drive.google.com/thumbnail?id=1t4rzDivHNDBip6ZSGRJeETgjXMp2ARhx&sz=w400' },
  { name: 'Đối tác 106', src: 'https://drive.google.com/thumbnail?id=1Hq9Gqyv40xtkar1nJmnv7fie_XUoZ9qh&sz=w400' },
  { name: 'Đối tác 107', src: 'https://drive.google.com/thumbnail?id=1TeU8oPmm0qsCqVhR4RkGBwbUnW2BkXzm&sz=w400' },
  { name: 'Đối tác 108', src: 'https://drive.google.com/thumbnail?id=13kNJHBWeNLTOB2aEKxfMkU6MUk0cW5Ag&sz=w400' },
  { name: 'Đối tác 109', src: 'https://drive.google.com/thumbnail?id=1vrBq25UFeuV2GTonOv_PxnYkTr9knfDW&sz=w400' },
  { name: 'Đối tác 110', src: 'https://drive.google.com/thumbnail?id=14bApJyne-usxK1cgegdLG7Mh_cHHndTS&sz=w400' },
  { name: 'Đối tác 111', src: 'https://drive.google.com/thumbnail?id=113Z7Rhwou8NH7ktpOAzIyJo6-AFbf5DX&sz=w400' },
  { name: 'Đối tác 112', src: 'https://drive.google.com/thumbnail?id=1--RSOj--DkiqgKMVZMCnyFFf6CvcBqxZ&sz=w400' },
  { name: 'Đối tác 113', src: 'https://drive.google.com/thumbnail?id=1rPTrZCgUr3p3ZGWW-vHNBDfWFg_BxaRJ&sz=w400' },
  { name: 'Đối tác 114', src: 'https://drive.google.com/thumbnail?id=1L4kNcsIoC8FAThFVbTO9V0kz2DKgP3Kx&sz=w400' },
  { name: 'Đối tác 115', src: 'https://drive.google.com/thumbnail?id=19YbU4gVAgFHKQU-Q-Waqy62Rm9DxF3Gi&sz=w400' },
  { name: 'Đối tác 116', src: 'https://drive.google.com/thumbnail?id=10yZ0dwh6oUdiwPxTiLGfBifWsEP2aIiq&sz=w400' },
  { name: 'Đối tác 117', src: 'https://drive.google.com/thumbnail?id=1RiMMhUYKNW-awv4LnQEq9ziQStyZlhut&sz=w400' },
  { name: 'Đối tác 118', src: 'https://drive.google.com/thumbnail?id=1FlFxPmo9_WvJ-FU0lAvLCbgG1SYlFB9B&sz=w400' },
  { name: 'Đối tác 119', src: 'https://drive.google.com/thumbnail?id=1DLWQyZAuA6prn0bVC8TzqeW5ZwYMWOYz&sz=w400' },
  { name: 'Đối tác 120', src: 'https://drive.google.com/thumbnail?id=1JPEBwQkkmFQFp8atFazirUz5k6KpE3Bt&sz=w400' },
  { name: 'Đối tác 121', src: 'https://drive.google.com/thumbnail?id=16xTXzwT8VEkgl_hc-c62w0ycgFf8C0vt&sz=w400' },
  { name: 'Đối tác 122', src: 'https://drive.google.com/thumbnail?id=1HwD_TH5B-fSOkMxSw7yvYjmFtA7exRqY&sz=w400' },
  { name: 'Đối tác 123', src: 'https://drive.google.com/thumbnail?id=1AhC7cTV92uqmwfXHz3S6njdZqdAkSVD-&sz=w400' },
  { name: 'Đối tác 124', src: 'https://drive.google.com/thumbnail?id=1VXV97IzU7D_Vlje4XKrkXGWRdGvYlROe&sz=w400' },
  { name: 'Đối tác 125', src: 'https://drive.google.com/thumbnail?id=1GTBbDFTzxy7NPL6AOmMehQFv15q1nxz7&sz=w400' },
  { name: 'Đối tác 126', src: 'https://drive.google.com/thumbnail?id=10xIEWTXBtKNTUmaTv1b6PZrPvMcqRdD0&sz=w400' },
  { name: 'Đối tác 127', src: 'https://drive.google.com/thumbnail?id=15zFUBkGZeYH6fEaAPI_QvDic9sCPJp1x&sz=w400' },
  { name: 'Đối tác 128', src: 'https://drive.google.com/thumbnail?id=1ts89H4WhBhMNfA2ArvYPuXZHTf3toHl3&sz=w400' },
  { name: 'Đối tác 129', src: 'https://drive.google.com/thumbnail?id=1EmG0OdZy9KfpgnEc0EL4ia_1JNtp750o&sz=w400' },
  { name: 'Đối tác 130', src: 'https://drive.google.com/thumbnail?id=1I9Z2zEeb0C8BJ3mB3l5RXI9swyDR1xTe&sz=w400' },
  { name: 'Đối tác 131', src: 'https://drive.google.com/thumbnail?id=1lyu7z2iak8pq6tK4AQ1XexIdPBt_uLG6&sz=w400' },
  { name: 'Đối tác 132', src: 'https://drive.google.com/thumbnail?id=1_JzbTSatd8x1OPLFptfg1DT_xuEO4Hjp&sz=w400' },
  { name: 'Đối tác 133', src: 'https://drive.google.com/thumbnail?id=1b378GpCnLUDWuoX5etKg4OLBDljqVWxM&sz=w400' },
  { name: 'Đối tác 134', src: 'https://drive.google.com/thumbnail?id=1PnL8NkivKXEpboIpoDeXlHE4XpOBqNDW&sz=w400' },
  { name: 'Đối tác 135', src: 'https://drive.google.com/thumbnail?id=1e1C6X22UTcaDxevVzbYmdBYVi5n2PEt-&sz=w400' },
  { name: 'Đối tác 136', src: 'https://drive.google.com/thumbnail?id=1dqAgR97sr5vt_i7cyEdlirnLJC8B_q5f&sz=w400' },
  { name: 'Đối tác 137', src: 'https://drive.google.com/thumbnail?id=1jGVMxysKJ3c33LgrKnCayADykl5u-mkY&sz=w400' },
  { name: 'Đối tác 138', src: 'https://drive.google.com/thumbnail?id=1sI8f54M4LH2UmXZKWs9vNkBsYxZPnLeV&sz=w400' }
];

const thirdPart = Math.ceil(partnerLogos.length / 3);
const partnerRow1 = computed(() => partnerLogos.slice(0, thirdPart));
const partnerRow2 = computed(() => partnerLogos.slice(thirdPart, thirdPart * 2));
const partnerRow3 = computed(() => partnerLogos.slice(thirdPart * 2));


// Bento Grid Cards Data with F5 Rotation
const rawBentoCards = [
  {
    id: 'ca-nhan',
    title: 'Đào tạo cho cá nhân',
    desc: 'Trang bị hệ thống tư duy và công cụ để mỗi cá nhân trở thành phiên bản xuất sắc nhất trong sự nghiệp của mình',
    bgClass: 'bg-dark-blue',
    contentClass: 'content-center text-white',
    bgImage: '/images/service_card.webp',
    link: '/courses/category/dao-tao-ca-nhan'
  },
  {
    id: 'inhouse',
    title: 'Đào tạo Inhouse',
    desc: 'Xây dựng năng lực thích ứng cao cho tổ chức thông qua các lộ trình đào tạo được thiết kế riêng',
    bgClass: 'bg-slate-gray',
    contentClass: 'content-top text-white',
    mockupImage: '/images/Service_card_dfee141b-d689-4e2c-bec9-350c9f407f84.png',
    link: '/courses/category/dao-tao-doanh-nghiep'
  },
  {
    id: 'andrews',
    title: 'Tuyển sinh đại học Andrews',
    desc: 'Thạc sĩ MBA Andrews tại Việt Nam và GEI - Hội thảo Lãnh đạo cấp cao tại Michigan, Hoa Kỳ.',
    bgClass: 'bg-slate-gray',
    contentClass: 'content-top text-white',
    bgImage: '/images/service_card_2.webp',
    bgImgClass: 'bento-bg-tint',
    link: '/tuyen-sinh'
  }
];

const bentoCardsOffset = ref(0);

const getBentoRotationOffset = () => {
  if (typeof window !== 'undefined' && window.sessionStorage) {
    let currentIdx = parseInt(sessionStorage.getItem('acc_bento_rotate_idx') || '0', 10);
    const nextIdx = (currentIdx + 1) % rawBentoCards.length;
    sessionStorage.setItem('acc_bento_rotate_idx', nextIdx.toString());
    return currentIdx;
  }
  return 0;
};

const bentoCards = computed(() => {
  const offset = bentoCardsOffset.value;
  const len = rawBentoCards.length;
  const rotated = [];
  for (let i = 0; i < len; i++) {
    rotated.push(rawBentoCards[(i + offset) % len]);
  }
  return rotated;
});
const showCursor = ref(false);
const cursorX = ref(0);
const cursorY = ref(0);

const handleMouseMove = (e) => {
  const rect = e.currentTarget.getBoundingClientRect();
  cursorX.value = e.clientX - rect.left;
  cursorY.value = e.clientY - rect.top;
};
const handleMouseEnter = () => {
  showCursor.value = true;
};
const handleMouseLeave = () => {
  showCursor.value = false;
};

// 6. Case Studies data
const caseStudies = [
  {
    id: 1,
    title: 'Giao tiếp tạo tác động cao cho lãnh đạo Chuỗi cung ứng và Sản xuất',
    badge: 'Kỹ năng mềm',
    image: '/images/Frame_1707482601.png',
    meta: 'Lĩnh vực: Ngành may mặc và chuỗi cung ứng • Việt Nam',
    link: '/corporate/case-studies'
  },
  {
    id: 2,
    title: 'Đẩy mạnh ứng dụng AI trong sáng tạo nội dung (Amway)',
    badge: 'Kỹ năng AI',
    image: '/images/Frame_1707482602.png',
    meta: 'Lĩnh vực: Bán hàng trực tiếp / Hàng tiêu dùng • Việt Nam',
    link: '/corporate/case-studies'
  },
  {
    id: 3,
    title: 'Nâng cao năng suất làm việc với Copilot trong Phân tích Dữ liệu',
    badge: 'Kỹ năng AI',
    image: '/images/Frame_1707482600.png',
    meta: 'Lĩnh vực: Bán hàng trực tiếp / Hàng tiêu dùng • Việt Nam',
    link: '/corporate/case-studies'
  }
];

// 7. Testimonials Slider
const currentTestimonial = ref(0);
const testimonials = computed(() => testimonialStore.testimonials);
const prevTestimonial = () => {
  currentTestimonial.value = (currentTestimonial.value - 1 + testimonials.value.length) % testimonials.value.length;
};
const nextTestimonial = () => {
  currentTestimonial.value = (currentTestimonial.value + 1) % testimonials.value.length;
};

// 8. Dynamic Courses Data from courseStore
const currentCourseCategory = ref('all');

const homeCourses = computed(() => {
  const list = courseStore.courses || [];
  if (currentCourseCategory.value === 'all') {
    return list;
  }
  return courseStore.getCoursesByCategory(currentCourseCategory.value);
});

// Load 8 courses initially, then load 8 more on button click
const visibleCourseCount = ref(8);

const displayedCourses = computed(() => {
  return homeCourses.value.slice(0, visibleCourseCount.value);
});

const hasMoreCourses = computed(() => {
  return visibleCourseCount.value < homeCourses.value.length;
});

const loadMoreCourses = () => {
  visibleCourseCount.value += 8;
};

// 9. Featured Lecturers (Dynamically fetched, max 4 featured or fallback to top 4)
const featuredLecturers = computed(() => {
  if (courseStore.lecturers && courseStore.lecturers.length > 0) {
    const featured = courseStore.lecturers.filter(l => l.is_featured);
    if (featured.length > 0) {
      return featured.slice(0, 4);
    }
    return courseStore.lecturers.slice(0, 4);
  }
  const featuredLecturerIds = ['nguyen-vu-huy-hoang', 'nguyen-tan-binh', 'bui-huynh-thuong', 'helen-lam-hien'];
  return lecturersData.filter(l => featuredLecturerIds.includes(l.id));
});

// 10. Student Shared Feedbacks photos for Home
const homeStudentFeedbacks = computed(() => {
  return photoTestimonialsData.slice(0, 3);
});

// 11. Consultation Auto Pop-up Modal State & Handler
const isContactModalOpen = ref(false);
const isSubmittingContact = ref(false);
const contactForm = ref({
  fullname: '',
  phone: '',
  email: '',
  courseHandle: '',
  message: ''
});

const closeContactModal = () => {
  isContactModalOpen.value = false;
};

const submitContactModal = async () => {
  if (!contactForm.value.fullname || !contactForm.value.phone || !contactForm.value.email) {
    courseStore.showToast('Vui lòng điền đầy đủ các thông tin bắt buộc (*)', 'warning');
    return;
  }

  isSubmittingContact.value = true;
  try {
    const nameParts = contactForm.value.fullname.trim().split(' ');
    const lastName = nameParts.length > 0 ? nameParts[nameParts.length - 1] : '';
    const firstName = nameParts.length > 1 ? nameParts[0] : contactForm.value.fullname.trim();
    const middleName = nameParts.length > 2 ? nameParts.slice(1, -1).join(' ') : '';

    await courseStore.sendContact(
      firstName,
      middleName,
      lastName,
      contactForm.value.email,
      contactForm.value.phone,
      contactForm.value.courseHandle || 'consultation-popup',
      contactForm.value.message || 'Đăng ký tư vấn từ Popup Trang Chủ'
    );

    courseStore.showToast('Cảm ơn bạn! Thông tin đăng ký tư vấn đã được gửi thành công.', 'success');
    closeContactModal();
    contactForm.value = {
      fullname: '',
      phone: '',
      email: '',
      courseHandle: '',
      message: ''
    };
  } catch (err) {
    courseStore.showToast(err.message || 'Gửi thông tin thất bại. Vui lòng thử lại sau!', 'error');
  } finally {
    isSubmittingContact.value = false;
  }
};

onMounted(() => {
  bentoCardsOffset.value = getBentoRotationOffset();
  startHeroAutoplay();
  setupEcoTitleObserver();
  setupCountersObserver();
  setupPartnerObserver();

  // Auto pop-up consultation modal on mount (with short delay for smooth entrance)
  setTimeout(() => {
    isContactModalOpen.value = true;
  }, 600);

  if (courseStore.courses.length === 0) {
    courseStore.fetchCourses();
  }
  if (courseStore.lecturers.length === 0) {
    courseStore.fetchLecturers();
  }
});

onUnmounted(() => {
  stopHeroAutoplay();
});
</script>

<style scoped src="@/styles/views/Home.css"></style>
