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
        <div class="container ecosystem-container">
          <div class="eco-left">
            <h2 class="eco-title">Kiến tạo hệ sinh thái chuyển đổi vững chắc</h2>
            <div class="eco-content">
              <p class="eco-desc">Skills Bridge thiết lập một hệ sinh thái cộng hưởng, nơi Năng lực con người được nâng tầm và Quy trình vận hành được tối ưu hóa đồng bộ.</p>
              <p class="eco-desc">Kết quả mang lại là một cấu trúc tổ chức tinh gọn, linh hoạt và sở hữu lợi thế cạnh tranh tuyệt đối trong kỷ nguyên Trí tuệ nhân tạo (AI).</p>
            </div>
            <div class="eco-counter-box">
              <div class="eco-number">{{ formatNumber(ecoCount) }}+</div>
              <div class="eco-counter-desc">Dự án & chiến lược đã thực thi thành công</div>
            </div>
          </div>

          <div class="eco-center">
            <img src="/images/Ecosystem_1.png" alt="Skills Bridge Ecosystem" class="eco-img" />
          </div>

          <div class="eco-right">
            <div class="services-list-card">
              <h3 class="services-card-title">Dịch vụ của chúng tôi</h3>
              <ul class="services-card-links">
                <li>
                  <router-link to="/courses/ai" class="service-item-link">
                    <span>Khóa học Cá nhân</span>
                    <span class="arrow-icon">&rarr;</span>
                  </router-link>
                </li>
                <li>
                  <router-link to="/corporate/dao-tao" class="service-item-link">
                    <span>Đào tạo Đội ngũ doanh nghiệp</span>
                    <span class="arrow-icon">&rarr;</span>
                  </router-link>
                </li>
                <li>
                  <router-link to="/contact" class="service-item-link">
                    <span>Tư vấn Tự động hóa</span>
                    <span class="arrow-icon">&rarr;</span>
                  </router-link>
                </li>
                <li>
                  <router-link to="/contact" class="service-item-link">
                    <span>Tư vấn Digital Marketing</span>
                    <span class="arrow-icon">&rarr;</span>
                  </router-link>
                </li>
              </ul>
              <router-link to="/contact" class="eco-cta-btn">
                <span>Kết nối với Chuyên gia</span>
                <span class="circle-arrow">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="7" y1="17" x2="17" y2="7"></line>
                    <polyline points="7 7 17 7 17 17"></polyline>
                  </svg>
                </span>
              </router-link>
            </div>
          </div>
        </div>
      </section>

      <!-- 3. Stats Section -->
      <section class="stats-section">
        <div class="container">
          <div class="stats-header">
            <h2 class="stats-title">Được tin tưởng bởi nhiều chuyên gia, lãnh đạo, và doanh nghiệp hàng đầu</h2>
            <p class="stats-subtitle">Không chỉ cung cấp giải pháp, chúng tôi tái định hình cấu trúc và hiệu suất kinh doanh để tạo ra giá trị thặng dư bền vững cho đối tác.</p>
          </div>

          <div class="stats-grid">
            <div class="stat-card-item">
              <div class="stat-num-box">{{ formatNumber(leadersCount) }}+</div>
              <div class="stat-label">Lãnh đạo và Chuyên gia</div>
              <div class="stat-desc">Đã được nâng tầm năng lực, sẵn sàng cho những vị trí then chốt</div>
            </div>
            <div class="stat-card-item">
              <div class="stat-num-box">{{ formatNumber(businessesCount) }}+</div>
              <div class="stat-label">Doanh nghiệp & Tổ chức</div>
              <div class="stat-desc">Đã chuyển đổi thành công mô hình vận hành và đào tạo</div>
            </div>
            <div class="stat-card-item">
              <div class="stat-num-box">{{ formatNumber(marketsCount) }}</div>
              <div class="stat-label">Thị trường Quốc tế</div>
              <div class="stat-desc">Minh chứng cho phương pháp luận chuẩn mực toàn cầu</div>
            </div>
            <div class="stat-card-item">
              <div class="stat-num-box">{{ formatNumber(npsCount) }}%</div>
              <div class="stat-label">NPS (Net Promoter Score)</div>
              <div class="stat-desc">Sự khẳng định tuyệt đối về chất lượng và tính ứng dụng thực tiễn từ các đối tác</div>
            </div>
          </div>
        </div>
      </section>
    </div>

    <!-- 4. Partner Logos Section -->
    <section class="partner-logos-section">
      <div class="container">
        <h3 class="partner-logos-title">70+ doanh nghiệp hàng đầu đã hợp tác</h3>
        
        <div class="partner-logos-grid" :class="{ 'reveal-active': partnerRevealActive }">
          <div 
            v-for="(logo, idx) in partnerLogos" 
            :key="idx" 
            class="partner-logo-card"
            :style="{ '--delay-idx': idx }"
          >
            <img :src="logo.src" :alt="logo.name" class="partner-logo-img" loading="lazy" />
          </div>
        </div>
      </div>
    </section>

    <!-- 5. Bento Grid Section -->
    <section class="bento-grid-section">
      <div class="container">
        <div class="bento-header">
          <h2 class="bento-title">Năng lực cốt lõi của Skills Bridge</h2>
          <p class="bento-subtitle">Các chuyên gia của chúng tôi mang đến sự kết hợp giữa kinh nghiệm thực chiến đa ngành và những góc nhìn đổi mới để khơi mào cho sự thay đổi toàn diện</p>
        </div>

        <div class="bento-grid-container">
          <!-- Card 1: Enterprise Training (Wide) -->
          <div class="bento-card card-wide bg-dark-blue">
            <img src="/images/service_card.webp" alt="Đào tạo doanh nghiệp" class="bento-card-bg" />
            <div class="bento-card-content content-center text-white">
              <h3 class="bento-card-title">Đào tạo Đội ngũ doanh nghiệp</h3>
              <p class="bento-card-desc">Xây dựng năng lực thích ứng cao cho tổ chức thông qua các lộ trình đào tạo được thiết kế riêng</p>
              <router-link to="/corporate/dao-tao" class="bento-arrow-btn btn-light">
                <span class="btn-text">Liên hệ ngay</span>
                <span class="btn-circle">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="7" y1="17" x2="17" y2="7"></line>
                    <polyline points="7 7 17 7 17 17"></polyline>
                  </svg>
                </span>
              </router-link>
            </div>
          </div>

          <!-- Card 2: Automation Consulting (Square) -->
          <div class="bento-card card-square bg-slate-gray">
            <router-link to="/contact" class="bento-card-overlay-link"></router-link>
            <picture>
              <source media="(max-width: 768px)" srcset="/images/Service_card_c75aad28-fc0e-4253-be63-ef3d2f3915d2.png" />
              <img src="/images/Service_card_dfee141b-d689-4e2c-bec9-350c9f407f84.png" alt="Tư vấn tự động hóa" class="bento-card-bg" />
            </picture>
            <div class="bento-card-content content-bottom text-white">
              <h3 class="bento-card-title">Tư vấn Tự động hóa</h3>
              <p class="bento-card-desc">Đưa AI và công nghệ tự động vào cốt lõi vận hành để tối ưu hóa nguồn lực và giảm thiểu rủi ro</p>
            </div>
          </div>

          <!-- Card 3: Digital Marketing (Square) -->
          <div class="bento-card card-square bg-slate-gray">
            <router-link to="/contact" class="bento-card-overlay-link"></router-link>
            <img src="/images/service_card_2.webp" alt="Tư vấn marketing" class="bento-card-bg" />
            <div class="bento-card-content content-bottom text-white">
              <h3 class="bento-card-title">Tư vấn Digital Marketing</h3>
              <p class="bento-card-desc">Kết nối chiến lược thương hiệu với sức mạnh số để tạo ra sự tăng trưởng doanh thu có thể đo lường được</p>
            </div>
          </div>

          <!-- Card 4: Individual Courses (Wide) -->
          <div class="bento-card card-wide bg-light-gray">
            <picture>
              <source media="(max-width: 768px)" srcset="/images/Service_card_3.png" />
              <img src="/images/Service_card_2.png" alt="Khóa học cá nhân" class="bento-card-bg" />
            </picture>
            <div class="bento-card-content content-left text-dark">
              <h3 class="bento-card-title">Khóa học Cá nhân</h3>
              <p class="bento-card-desc">Trang bị hệ thống tư duy và công cụ để mỗi cá nhân trở thành phiên bản xuất sắc nhất trong sự nghiệp của mình</p>
              <router-link to="/courses/ai" class="bento-arrow-btn btn-teal">
                <span class="btn-text">Khám phá ngay</span>
                <span class="btn-circle">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="7" y1="17" x2="17" y2="7"></line>
                    <polyline points="7 7 17 7 17 17"></polyline>
                  </svg>
                </span>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 6. Partnership Section (Autoplay Tabs) -->
    <section class="partnership-tabs-section">
      <div class="container partnership-container">
        <!-- Left Banner Card -->
        <div class="partnership-left-card">
          <img src="/images/CTA_card.png" alt="Cùng bạn mở ra khả năng mới" class="partnership-card-bg" />
          <div class="partnership-card-content text-white">
            <p class="partnership-card-tagline">Cùng bạn mở ra những khả năng mới</p>
            <router-link to="/contact" class="partnership-card-btn">
              <span>Kết nối với Chuyên gia</span>
              <span class="arrow-up-right">&nearr;</span>
            </router-link>
          </div>
        </div>

        <!-- Right Tabs Content -->
        <div class="partnership-right-content">
          <h2 class="partnership-title">Bạn đã sẵn sàng nâng tầm năng lực tổ chức?</h2>
          <p class="partnership-subtitle">Chúng tôi cung cấp các giải pháp đào tạo và tư vấn chuyên sâu, đồng hành cùng doanh nghiệp đạt hiệu quả tối ưu.</p>
          
          <!-- Tabs Navigation -->
          <div class="partnership-tabs-nav" role="tablist">
            <button 
              v-for="(tab, index) in partnershipTabs" 
              :key="index"
              class="partnership-tab-btn"
              :class="{ active: activeTab === index }"
              @click="handleTabClick(index)"
              role="tab"
              :aria-selected="activeTab === index ? 'true' : 'false'"
            >
              <span class="tab-btn-title">{{ tab.title }}</span>
              <!-- Active Progress Bar Indicator -->
              <span class="tab-progress-track">
                <span 
                  class="tab-progress-bar"
                  :style="{ width: activeTab === index ? tabProgress + '%' : '0%' }"
                ></span>
              </span>
            </button>
          </div>

          <!-- Tab Content Display -->
          <div class="partnership-tab-content-panel">
            <p class="partnership-tab-desc">
              {{ partnershipTabs[activeTab].desc }}
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- 7. Case Studies Section (Custom Follow Cursor) -->
    <section class="case-studies-section" @mousemove="handleMouseMove" @mouseenter="handleMouseEnter" @mouseleave="handleMouseLeave">
      <div class="container">
        <!-- Custom Cursor element -->
        <div 
          v-if="showCursor"
          class="custom-follow-cursor"
          :style="{ transform: `translate3d(${cursorX}px, ${cursorY}px, 0)` }"
        >
          <span class="cursor-badge-text">Đọc case study</span>
        </div>

        <div class="case-header">
          <span class="case-ui-tag">Case study</span>
          <h2 class="case-title">Hành trình của chúng tôi cùng doanh nghiệp</h2>
          <p class="case-subtitle">Những dự án thực tế giúp doanh nghiệp bứt phá hiệu năng vận hành và chất lượng nhân lực.</p>
        </div>

        <div class="cases-grid">
          <div 
            v-for="study in caseStudies" 
            :key="study.id"
            class="case-card-box"
          >
            <router-link :to="study.link" class="case-card-anchor">
              <div class="case-img-container">
                <img :src="study.image" :alt="study.title" class="case-img-photo" loading="lazy" />
                <span class="case-badge-pill">{{ study.badge }}</span>
              </div>
              <div class="case-card-body">
                <div class="case-card-meta">{{ study.meta }}</div>
                <h3 class="case-card-heading">{{ study.title }}</h3>
              </div>
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- 8. Testimonials Section -->
    <section class="testimonials-slider-section">
      <div class="container">
        <div class="testimonials-header">
          <span class="testimonials-ui-tag">Ý kiến khách hàng</span>
          <h2 class="testimonials-heading">Khách hàng cảm nhận thế nào về chúng tôi</h2>
        </div>

        <div class="testimonials-slider-wrapper">
          <div 
            class="testimonials-track"
            :style="{ transform: `translate3d(-${currentTestimonial * 100}%, 0, 0)` }"
          >
            <div 
              v-for="item in testimonials" 
              :key="item.id"
              class="testimonial-slide-item"
            >
              <div class="testimonial-bubble">
                <div class="quote-symbol">“</div>
                <p class="quote-text">{{ item.text }}</p>
                <div class="quote-author-info">
                  <h4 class="quote-author-name">{{ item.name }}</h4>
                  <p class="quote-author-role">{{ item.role }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Navigation controls -->
          <button class="slider-control prev" @click="prevTestimonial" aria-label="Previous testimonial">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M15 18l-6-6 6-6" />
            </svg>
          </button>
          <button class="slider-control next" @click="nextTestimonial" aria-label="Next testimonial">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 18l6-6-6-6" />
            </svg>
          </button>

          <!-- Slider Pagination Dots -->
          <div class="slider-indicators">
            <button 
              v-for="(item, idx) in testimonials" 
              :key="item.id"
              class="indicator-dot"
              :class="{ active: currentTestimonial === idx }"
              @click="currentTestimonial = idx"
              :aria-label="'Go to slide ' + (idx + 1)"
            ></button>
          </div>
        </div>
      </div>
    </section>

    <!-- 9. Blog posts Section -->
    <section class="blogs-section">
      <div class="container">
        <div class="blogs-header-row">
          <div class="blogs-header-left">
            <span class="blogs-ui-tag">Thư viện bài viết</span>
            <h2 class="blogs-heading">Cập nhật thông tin mới nhất cùng Skills Bridge</h2>
          </div>
          <router-link to="/library/blog" class="blogs-view-all-btn">
            Xem thêm bài viết
          </router-link>
        </div>

        <div class="blogs-grid">
          <article 
            v-for="post in blogPosts" 
            :key="post.id"
            class="blog-post-card"
          >
            <router-link :to="'/library/blog'" class="blog-image-anchor">
              <div class="blog-img-box">
                <img :src="post.image" :alt="post.title" class="blog-img-element" loading="lazy" />
              </div>
            </router-link>
            <div class="blog-body-content">
              <span class="blog-category-tag">{{ post.category }}</span>
              <h3 class="blog-post-title">
                <router-link :to="'/library/blog'">{{ post.title }}</router-link>
              </h3>
              <p class="blog-post-excerpt">{{ post.excerpt }}</p>
              <router-link :to="'/library/blog'" class="blog-read-more-link">
                <span>Xem thêm</span>
                <span class="read-more-arrow">&rarr;</span>
              </router-link>
            </div>
          </article>
        </div>
      </div>
    </section>

    <!-- 10. CTA Section -->
    <section class="cta-banner-section">
      <div class="container">
        <div class="cta-banner-box">
          <div class="cta-banner-left">
            <h2 class="cta-banner-heading">Nâng tầm lợi thế cạnh tranh cùng Skills Bridge</h2>
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
            <img src="/images/Right.png" alt="Skills Bridge Consulting Team" class="cta-right-img" loading="lazy" />
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useCourseStore } from '@/stores/courses';
import { useTestimonialStore } from '@/stores/testimonials';

const courseStore = useCourseStore();
const testimonialStore = useTestimonialStore();

// 1. Hero Carousel
const currentSlide = ref(0);
const heroSlides = [
  {
    desktopImage: '/images/CoE-Web.png',
    mobileImage: '/images/CoE-Mobile.png',
    link: '/corporate/coe',
    title: 'AI Center of Excellence'
  },
  {
    desktopImage: '/images/Website_dd1fbf97-8fbe-44ed-bfd9-1eaaa069fdb3.png',
    mobileImage: '/images/SEB_Mobile.png',
    link: '/courses/ai',
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

let heroInterval = null;
const startHeroAutoplay = () => {
  heroInterval = setInterval(() => {
    currentSlide.value = (currentSlide.value + 1) % heroSlides.length;
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
  currentSlide.value = (currentSlide.value - 1 + heroSlides.length) % heroSlides.length;
  stopHeroAutoplay();
  startHeroAutoplay();
};

const nextSlide = () => {
  currentSlide.value = (currentSlide.value + 1) % heroSlides.length;
  stopHeroAutoplay();
  startHeroAutoplay();
};

// 2. Ecosystem & Stats Counter Animation
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
        animateNumber(ecoCount, 200, 1200);
        animateNumber(leadersCount, 17000, 1800);
        animateNumber(businessesCount, 70, 1500);
        animateNumber(marketsCount, 7, 1000);
        animateNumber(npsCount, 75, 1200);
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
  { name: 'Google', src: '/images/Google.png' },
  { name: 'VNG', src: '/images/VNG.png' },
  { name: 'FPT', src: '/images/FPT.png' },
  { name: 'AXON', src: '/images/AXON.png' },
  { name: 'Shopee', src: '/images/SHOPEE.png' },
  { name: 'Lazada', src: '/images/LAZADA.png' },
  { name: 'Maybank', src: '/images/MAYBANK.png' },
  { name: 'Home Credit', src: '/images/HOMECREDIT.png' },
  { name: 'Manulife', src: '/images/MANULIFE.png' },
  { name: 'VPBank', src: '/images/VPBANK.png' },
  { name: 'MSD', src: '/images/MSD.png' },
  { name: 'ACB', src: '/images/ACB.png' },
  { name: 'Bosch', src: '/images/BOSCH.png' },
  { name: 'BUV', src: '/images/BUV.png' },
  { name: 'RMIT', src: '/images/RMIT.png' },
  { name: 'Honda', src: '/images/HONDA.png' },
  { name: 'Uniqlo', src: '/images/UNIQLO.png' },
  { name: 'Firegroup', src: '/images/FIREGROUP.png' },
  { name: 'The Home Depot', src: '/images/The_Home_Depot.png' },
  { name: 'Amway', src: '/images/Amway.png' },
  { name: 'Talentnet', src: '/images/Talentnet.png' },
  { name: 'Hoa Linh', src: '/images/Hoa_Linh.png' },
  { name: 'InteFood', src: '/images/InteFood.png' },
  { name: 'Viatris', src: '/images/Viatris.png' }
];

// 4. Partnership Autoplay Tabs
const activeTab = ref(0);
const tabsAutoplay = ref(true);
const tabProgress = ref(0);
const partnershipTabs = [
  {
    title: 'Đồng hành',
    desc: 'Làm việc sát cánh cùng đội ngũ của bạn, từ đào tạo đến triển khai thực tế, đảm bảo mọi chiến lược đều được áp dụng hiệu quả và mang lại tác động rõ ràng.'
  },
  {
    title: 'Chuyên sâu',
    desc: 'Phân tích chuyên sâu từng khía cạnh trong hoạt động kinh doanh để đưa ra giải pháp tối ưu, phù hợp với mục tiêu phát triển dài hạn.'
  },
  {
    title: 'Thiết kế riêng',
    desc: 'Mỗi giải pháp đều được thiết kế riêng biệt, phù hợp với nhu cầu cụ thể của từng đối tác, đảm bảo hiệu quả tối đa.'
  }
];

let tabProgressInterval = null;
const TAB_DURATION = 4000; // 4 seconds per tab
const startTabProgress = () => {
  if (!tabsAutoplay.value) return;
  const stepTime = 30; // ms
  const stepAmount = (stepTime / TAB_DURATION) * 100;
  
  tabProgressInterval = setInterval(() => {
    tabProgress.value += stepAmount;
    if (tabProgress.value >= 100) {
      tabProgress.value = 0;
      activeTab.value = (activeTab.value + 1) % partnershipTabs.length;
    }
  }, stepTime);
};

const stopTabProgress = () => {
  if (tabProgressInterval) {
    clearInterval(tabProgressInterval);
    tabProgressInterval = null;
  }
};

const handleTabClick = (index) => {
  tabsAutoplay.value = false;
  stopTabProgress();
  activeTab.value = index;
  tabProgress.value = 100;
};

// 5. Custom Mouse Cursor for Case Studies
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

// 8. Blog posts list from courseStore (Pinia reactive data binding)
const blogPosts = computed(() => courseStore.getBlogPosts);

onMounted(() => {
  startHeroAutoplay();
  setupCountersObserver();
  setupPartnerObserver();
  startTabProgress();
});

onUnmounted(() => {
  stopHeroAutoplay();
  stopTabProgress();
});
</script>

<style scoped>
.home-view {
  background-color: #ffffff;
  color: #101828;
  font-family: var(--font-sans);
  overflow-x: hidden;
}

/* 1. Hero Section (Carousel) */
.hero-carousel-section {
  width: 100%;
  margin-top: 80px; /* offset fixed header */
  position: relative;
}

.carousel-container {
  position: relative;
  width: 100%;
  aspect-ratio: 1920 / 720;
  overflow: hidden;
  background-color: #f4f6fa;
}

@media (max-width: 768px) {
  .carousel-container {
    aspect-ratio: 412 / 560; /* mobile aspect ratio */
  }
}

.carousel-slide {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.8s ease-in-out, visibility 0.8s ease-in-out;
  z-index: 1;
}

.carousel-slide.active {
  opacity: 1;
  visibility: visible;
  z-index: 2;
}

.slide-link {
  display: block;
  width: 100%;
  height: 100%;
}

.slide-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.carousel-arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid rgba(16, 24, 40, 0.1);
  color: #101828;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
  cursor: pointer;
  transition: all 0.3s ease;
}

.carousel-arrow:hover {
  background: #ffffff;
  color: var(--primary);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.carousel-arrow.prev {
  left: 24px;
}

.carousel-arrow.next {
  right: 24px;
}

@media (max-width: 768px) {
  .carousel-arrow {
    width: 36px;
    height: 36px;
  }
  .carousel-arrow.prev {
    left: 12px;
  }
  .carousel-arrow.next {
    right: 12px;
  }
}

.carousel-dots {
  position: absolute;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 12px;
  z-index: 10;
}

.carousel-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.5);
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
}

.carousel-dot.active {
  background: var(--primary);
  width: 24px;
  border-radius: 5px;
}

/* 2. Ecosystem Section */
.ecosystem-section {
  padding-block: 80px 60px;
  background-color: #ffffff;
}

.ecosystem-container {
  display: grid;
  grid-template-columns: 1.2fr 1fr 1fr;
  align-items: center;
  gap: 40px;
}

@media (max-width: 1024px) {
  .ecosystem-container {
    grid-template-columns: 1fr;
    gap: 48px;
  }
}

.eco-left {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.eco-title {
  font-size: 36px;
  font-weight: 800;
  line-height: 1.25;
  color: #101828;
}

@media (max-width: 768px) {
  .eco-title {
    font-size: 28px;
  }
}

.eco-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.eco-desc {
  font-size: 16px;
  line-height: 1.6;
  color: var(--text-secondary);
}

.eco-counter-box {
  margin-top: 12px;
}

.eco-number {
  font-size: 64px;
  font-weight: 900;
  color: var(--primary);
  line-height: 1.1;
  letter-spacing: -2px;
}

.eco-counter-desc {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.eco-center {
  display: flex;
  justify-content: center;
  align-items: center;
}

.eco-img {
  width: 100%;
  max-width: 320px;
  height: auto;
  object-fit: contain;
}

.eco-right {
  display: flex;
  flex-direction: column;
}

.services-list-card {
  background: #ffffff;
  border: 1px solid #eaecf0;
  border-radius: 20px;
  padding: 32px;
  box-shadow: 0 4px 20px rgba(16, 24, 40, 0.04);
}

.services-card-title {
  font-size: 20px;
  font-weight: 700;
  color: #101828;
  margin-bottom: 24px;
  border-bottom: 1px solid #f2f4f7;
  padding-bottom: 12px;
}

.services-card-links {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 24px;
}

.service-item-link {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 16px;
  background-color: #f9fafb;
  border-radius: 10px;
  font-weight: 600;
  font-size: 15px;
  color: #344054;
  transition: all 0.3s ease;
}

.service-item-link:hover {
  background-color: rgba(2, 43, 159, 0.05);
  color: var(--primary);
}

.service-item-link .arrow-icon {
  opacity: 0.6;
  transition: transform 0.3s ease;
}

.service-item-link:hover .arrow-icon {
  transform: translateX(4px);
  opacity: 1;
}

.eco-cta-btn {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: var(--primary);
  color: #ffffff !important;
  font-weight: 600;
  padding: 6px 6px 6px 20px;
  border-radius: 50px;
  font-size: 15px;
  transition: all 0.3s ease;
}

.eco-cta-btn:hover {
  background-color: #011E70;
  transform: translateY(-2px);
}

.circle-arrow {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #ffffff;
  color: var(--primary);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.4s ease;
}

.eco-cta-btn:hover .circle-arrow {
  transform: rotate(45deg);
}

/* 3. Stats Section */
.stats-section {
  padding-block: 60px 80px;
  background-color: #f9fafb;
  border-block: 1px solid #eaecf0;
}

.stats-header {
  text-align: center;
  max-width: 800px;
  margin: 0 auto 56px auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.stats-title {
  font-size: 32px;
  font-weight: 800;
  line-height: 1.3;
  color: #101828;
}

@media (max-width: 768px) {
  .stats-title {
    font-size: 24px;
  }
}

.stats-subtitle {
  font-size: 16px;
  line-height: 1.6;
  color: var(--text-secondary);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

@media (max-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 576px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
}

.stat-card-item {
  background: #ffffff;
  border: 1px solid #eaecf0;
  border-radius: 16px;
  padding: 32px 24px;
  text-align: center;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.02);
  transition: all 0.3s ease;
}

.stat-card-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(2, 43, 159, 0.06);
  border-color: rgba(2, 43, 159, 0.15);
}

.stat-num-box {
  font-size: 44px;
  font-weight: 800;
  color: var(--primary);
  margin-bottom: 12px;
  letter-spacing: -1px;
}

.stat-label {
  font-size: 16px;
  font-weight: 700;
  color: #101828;
  margin-bottom: 8px;
}

.stat-desc {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.5;
}

/* 4. Partner Logos Section */
.partner-logos-section {
  padding-block: 80px;
  background-color: #ffffff;
  border-bottom: 1px solid #eaecf0;
}

.partner-logos-title {
  text-align: center;
  font-size: 14px;
  font-weight: 700;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 1.5px;
  margin-bottom: 40px;
}

.partner-logos-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

@media (max-width: 992px) {
  .partner-logos-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (max-width: 576px) {
  .partner-logos-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
  }
}

.partner-logo-card {
  aspect-ratio: 3 / 2;
  background-color: #ffffff;
  border: 1px solid #eaecf0;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}

.partner-logos-grid.reveal-active .partner-logo-card {
  opacity: 1;
  transform: translateY(0);
}

/* Apply staggered animation delay to all cards when active */
.partner-logos-grid.reveal-active .partner-logo-card {
  transition-delay: calc(var(--delay-idx) * 45ms);
}

.partner-logo-img {
  max-width: 100%;
  max-height: 40px;
  object-fit: contain;
  filter: grayscale(100%);
  opacity: 0.6;
  transition: all 0.3s ease;
}

.partner-logo-card:hover .partner-logo-img {
  filter: grayscale(0%);
  opacity: 1;
  transform: scale(1.05);
}

/* 5. Bento Grid Section */
.bento-grid-section {
  padding-block: 80px;
  background-color: #ffffff;
}

.bento-header {
  text-align: center;
  max-width: 800px;
  margin: 0 auto 56px auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.bento-title {
  font-size: 36px;
  font-weight: 800;
  color: #101828;
}

@media (max-width: 768px) {
  .bento-title {
    font-size: 28px;
  }
}

.bento-subtitle {
  font-size: 16px;
  line-height: 1.6;
  color: var(--text-secondary);
}

.bento-grid-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

@media (max-width: 768px) {
  .bento-grid-container {
    grid-template-columns: 1fr;
  }
}

.bento-card {
  position: relative;
  border-radius: 20px;
  overflow: hidden;
  height: 380px;
  display: flex;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

@media (max-width: 768px) {
  .bento-card {
    height: 320px;
  }
}

.card-wide {
  grid-column: span 2;
}

@media (max-width: 768px) {
  .card-wide {
    grid-column: span 1;
  }
}

.bento-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 36px rgba(16, 24, 40, 0.1);
}

.bento-card-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: 1;
  transition: transform 0.6s ease;
}

.bento-card:hover .bento-card-bg {
  transform: scale(1.03);
}

.bento-card-overlay-link {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 3;
}

.bento-card-content {
  position: relative;
  z-index: 2;
  padding: 48px;
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
}

@media (max-width: 576px) {
  .bento-card-content {
    padding: 24px;
  }
}

/* Alignment Classes */
.content-center {
  justify-content: center;
  align-items: center;
  text-align: center;
}

.content-bottom {
  justify-content: flex-end;
  align-items: flex-start;
}

.content-left {
  justify-content: center;
  align-items: flex-start;
  max-width: 60%;
}

@media (max-width: 768px) {
  .content-left {
    max-width: 100%;
  }
}

/* Background Color Fallbacks */
.bg-dark-blue { background-color: #022B9F; }
.bg-slate-gray { background-color: #1d2939; }
.bg-light-gray { background-color: #f2f4f7; }

/* Text colors */
.text-white { color: #ffffff; }
.text-dark { color: #101828; }

.bento-card-title {
  font-size: 28px;
  font-weight: 800;
  margin-bottom: 12px;
}

@media (max-width: 576px) {
  .bento-card-title {
    font-size: 20px;
  }
}

.bento-card-desc {
  font-size: 15px;
  line-height: 1.5;
  margin-bottom: 24px;
  opacity: 0.9;
}

/* High Specificity Arrow button */
.bento-arrow-btn {
  display: inline-flex;
  align-items: center;
  justify-content: space-between;
  padding: 4px 4px 4px 24px;
  border-radius: 99px;
  font-size: 16px;
  font-weight: 600;
  gap: 16px;
  min-width: 200px;
  transition: all 0.3s ease;
  border: none;
}

.btn-light {
  background-color: #ffffff;
  color: #101828;
}

.btn-light .btn-circle {
  background-color: var(--primary);
  color: #ffffff;
}

.btn-teal {
  background-color: var(--primary);
  color: #ffffff;
}

.btn-teal .btn-circle {
  background-color: #ffffff;
  color: var(--primary);
}

.btn-circle {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.4s ease;
}

.bento-arrow-btn:hover {
  transform: translateY(-2px);
}

.bento-arrow-btn:hover .btn-circle svg {
  transform: rotate(45deg);
}

.btn-circle svg {
  transition: transform 0.4s ease;
}

/* 6. Partnership Section (Autoplay Tabs) */
.partnership-tabs-section {
  padding-block: 80px;
  background-color: #ffffff;
  border-block: 1px solid #eaecf0;
}

.partnership-container {
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  gap: 60px;
  align-items: center;
}

@media (max-width: 992px) {
  .partnership-container {
    grid-template-columns: 1fr;
    gap: 48px;
  }
}

.partnership-left-card {
  position: relative;
  height: 480px;
  border-radius: 24px;
  overflow: hidden;
}

@media (max-width: 576px) {
  .partnership-left-card {
    height: 360px;
  }
}

.partnership-card-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: 1;
}

.partnership-card-content {
  position: relative;
  z-index: 2;
  padding: 48px;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-sizing: border-box;
}

@media (max-width: 576px) {
  .partnership-card-content {
    padding: 32px;
  }
}

.partnership-card-tagline {
  font-size: 32px;
  font-weight: 800;
  line-height: 1.25;
}

.partnership-card-btn {
  align-self: flex-start;
  display: inline-flex;
  align-items: center;
  gap: 12px;
  background-color: #ffffff;
  color: #101828 !important;
  font-weight: 600;
  padding: 14px 28px;
  border-radius: 50px;
  font-size: 15px;
  transition: all 0.3s ease;
}

.partnership-card-btn:hover {
  background-color: #f2f4f7;
  transform: translateY(-2px);
}

.partnership-card-btn .arrow-up-right {
  font-size: 18px;
}

.partnership-right-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.partnership-title {
  font-size: 36px;
  font-weight: 800;
  color: #101828;
}

@media (max-width: 768px) {
  .partnership-title {
    font-size: 28px;
  }
}

.partnership-subtitle {
  font-size: 16px;
  line-height: 1.6;
  color: var(--text-secondary);
}

.partnership-tabs-nav {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 12px;
}

.partnership-tab-btn {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  text-align: left;
  border: none;
  background: none;
  padding: 12px 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  width: 100%;
}

.partnership-tab-btn:hover {
  background-color: #f9fafb;
}

.partnership-tab-btn.active {
  background-color: #f4f6fa;
}

.tab-btn-title {
  font-size: 18px;
  font-weight: 700;
  color: #344054;
  margin-bottom: 6px;
  transition: color 0.3s ease;
}

.partnership-tab-btn.active .tab-btn-title {
  color: var(--primary);
}

/* Tab Line Progress Indicator */
.tab-progress-track {
  width: 100%;
  height: 3px;
  background-color: #eaecf0;
  border-radius: 2px;
  overflow: hidden;
  position: relative;
}

.tab-progress-bar {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  background-color: var(--primary);
  transition: width 0.05s linear;
}

.partnership-tab-content-panel {
  margin-top: 16px;
  padding: 16px;
  background-color: #f9fafb;
  border-left: 4px solid var(--primary);
  border-radius: 0 8px 8px 0;
  min-height: 90px;
}

.partnership-tab-desc {
  font-size: 15px;
  line-height: 1.6;
  color: var(--text-secondary);
}

/* 7. Case Studies Section */
.case-studies-section {
  padding-block: 80px;
  background-color: #ffffff;
  position: relative;
}

.case-header {
  text-align: center;
  max-width: 800px;
  margin: 0 auto 56px auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.case-ui-tag {
  font-size: 12px;
  font-weight: 700;
  color: var(--primary);
  text-transform: uppercase;
  letter-spacing: 1.5px;
}

.case-title {
  font-size: 36px;
  font-weight: 800;
  color: #101828;
}

@media (max-width: 768px) {
  .case-title {
    font-size: 28px;
  }
}

.case-subtitle {
  font-size: 16px;
  line-height: 1.6;
  color: var(--text-secondary);
}

.cases-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
  max-width: 1200px;
  margin: 0 auto;
}

@media (max-width: 1024px) {
  .cases-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .cases-grid {
    grid-template-columns: 1fr;
  }
}

.case-card-box {
  background: #ffffff;
  border: 1px solid #eaecf0;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(16, 24, 40, 0.02);
  transition: all 0.3s ease;
  height: 100%;
}

.case-card-box:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 32px rgba(2, 43, 159, 0.08);
  border-color: rgba(2, 43, 159, 0.15);
}

.case-card-anchor {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.case-img-container {
  position: relative;
  aspect-ratio: 16 / 10;
  overflow: hidden;
  background-color: #f2f4f7;
}

.case-img-photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.case-card-box:hover .case-img-photo {
  transform: scale(1.04);
}

.case-badge-pill {
  position: absolute;
  top: 16px;
  left: 16px;
  background-color: #101828;
  color: #ffffff;
  font-size: 11px;
  font-weight: 700;
  padding: 6px 12px;
  border-radius: 6px;
  letter-spacing: 0.5px;
}

.case-card-body {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  flex-grow: 1;
}

.case-card-meta {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-muted);
}

.case-card-heading {
  font-size: 18px;
  font-weight: 700;
  line-height: 1.4;
  color: #101828;
  flex-grow: 1;
}

/* Custom Follow Cursor Style */
.custom-follow-cursor {
  position: absolute;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background-color: var(--primary);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 99;
  pointer-events: none;
  margin-top: -50px;
  margin-left: -50px;
  animation: scaleUp 0.2s ease-out;
  box-shadow: 0 8px 24px rgba(2, 43, 159, 0.3);
}

.cursor-badge-text {
  color: #ffffff;
  font-size: 11px;
  font-weight: 700;
  text-align: center;
  line-height: 1.2;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

@keyframes scaleUp {
  from { transform: scale(0); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

@media (max-width: 1024px) {
  /* Disable custom follower on tablets and mobile devices */
  .custom-follow-cursor {
    display: none !important;
  }
}

/* 8. Testimonials Section */
.testimonials-slider-section {
  padding-block: 80px;
  background-color: #f9fafb;
  border-block: 1px solid #eaecf0;
}

.testimonials-header {
  text-align: center;
  max-width: 800px;
  margin: 0 auto 48px auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.testimonials-ui-tag {
  font-size: 12px;
  font-weight: 700;
  color: var(--primary);
  text-transform: uppercase;
  letter-spacing: 1.5px;
}

.testimonials-heading {
  font-size: 36px;
  font-weight: 800;
  color: #101828;
}

@media (max-width: 768px) {
  .testimonials-heading {
    font-size: 28px;
  }
}

.testimonials-slider-wrapper {
  position: relative;
  max-width: 900px;
  margin: 0 auto;
  overflow: hidden;
  padding-bottom: 40px;
}

.testimonials-track {
  display: flex;
  transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  width: 100%;
}

.testimonial-slide-item {
  min-width: 100%;
  box-sizing: border-box;
  padding: 16px;
}

.testimonial-bubble {
  background-color: #ffffff;
  border: 1px solid #eaecf0;
  border-radius: 24px;
  padding: 48px;
  position: relative;
  box-shadow: 0 4px 20px rgba(16, 24, 40, 0.02);
}

@media (max-width: 576px) {
  .testimonial-bubble {
    padding: 32px 24px;
  }
}

.quote-symbol {
  font-family: Georgia, serif;
  font-size: 96px;
  line-height: 1;
  color: var(--primary);
  opacity: 0.15;
  position: absolute;
  top: 16px;
  left: 32px;
  pointer-events: none;
}

.quote-text {
  font-size: 18px;
  line-height: 1.6;
  color: #344054;
  font-style: italic;
  position: relative;
  z-index: 2;
  margin-bottom: 32px;
}

@media (max-width: 576px) {
  .quote-text {
    font-size: 16px;
  }
}

.quote-author-info {
  border-top: 1px solid #f2f4f7;
  padding-top: 24px;
}

.quote-author-name {
  font-size: 16px;
  font-weight: 700;
  color: #101828;
  margin-bottom: 4px;
}

.quote-author-role {
  font-size: 13px;
  font-weight: 600;
  color: var(--primary);
}

.slider-control {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: #ffffff;
  border: 1px solid #eaecf0;
  color: #101828;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
  cursor: pointer;
  transition: all 0.3s ease;
}

.slider-control:hover {
  background: var(--primary);
  color: #ffffff;
  border-color: var(--primary);
}

.slider-control.prev {
  left: 0;
}

.slider-control.next {
  right: 0;
}

@media (max-width: 992px) {
  .slider-control {
    display: none;
  }
}

.slider-indicators {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 8px;
}

.indicator-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #d0d5dd;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
}

.indicator-dot.active {
  background: var(--primary);
  width: 20px;
  border-radius: 4px;
}

/* 9. Blog posts Section */
.blogs-section {
  padding-block: 80px;
  background-color: #ffffff;
}

.blogs-header-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 48px;
}

@media (max-width: 768px) {
  .blogs-header-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 20px;
  }
}

.blogs-header-left {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.blogs-ui-tag {
  font-size: 12px;
  font-weight: 700;
  color: var(--primary);
  text-transform: uppercase;
  letter-spacing: 1.5px;
}

.blogs-heading {
  font-size: 36px;
  font-weight: 800;
  color: #101828;
}

@media (max-width: 768px) {
  .blogs-heading {
    font-size: 26px;
  }
}

.blogs-view-all-btn {
  display: inline-flex;
  align-items: center;
  background-color: #f2f4f7;
  color: #344054 !important;
  font-weight: 600;
  padding: 12px 24px;
  border-radius: 50px;
  font-size: 15px;
  transition: all 0.3s ease;
}

.blogs-view-all-btn:hover {
  background-color: rgba(2, 43, 159, 0.08);
  color: var(--primary) !important;
  transform: translateY(-2px);
}

.blogs-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

@media (max-width: 1024px) {
  .blogs-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 600px) {
  .blogs-grid {
    grid-template-columns: 1fr;
  }
}

.blog-post-card {
  background: #ffffff;
  border: 1px solid #eaecf0;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.01);
  display: flex;
  flex-direction: column;
  height: 100%;
  transition: all 0.3s ease;
}

.blog-post-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 32px rgba(2, 43, 159, 0.08);
  border-color: rgba(2, 43, 159, 0.15);
}

.blog-image-anchor {
  display: block;
  aspect-ratio: 16 / 10;
  overflow: hidden;
}

.blog-img-box {
  width: 100%;
  height: 100%;
  background-color: #f2f4f7;
}

.blog-img-element {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.blog-post-card:hover .blog-img-element {
  transform: scale(1.03);
}

.blog-body-content {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  flex-grow: 1;
}

.blog-category-tag {
  font-size: 11px;
  font-weight: 700;
  color: var(--primary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.blog-post-title {
  font-size: 15px;
  font-weight: 700;
  line-height: 1.4;
  color: #101828;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  height: 2.8em;
}

.blog-post-title a {
  color: #101828;
  transition: color 0.3s ease;
}

.blog-post-title a:hover {
  color: var(--primary);
}

.blog-post-excerpt {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.blog-read-more-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 700;
  color: var(--primary);
  margin-top: auto;
  align-self: flex-start;
}

.blog-read-more-link .read-more-arrow {
  transition: transform 0.3s ease;
}

.blog-read-more-link:hover .read-more-arrow {
  transform: translateX(4px);
}

/* 10. CTA Section */
.cta-banner-section {
  padding-block: 40px 80px;
  background-color: #ffffff;
}

.cta-banner-box {
  background: radial-gradient(circle at top right, rgba(2, 43, 159, 0.08), transparent 50%), #f9fafb;
  border: 1px solid #eaecf0;
  border-radius: 24px;
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  align-items: center;
  gap: 40px;
  padding: 64px;
  overflow: hidden;
}

@media (max-width: 992px) {
  .cta-banner-box {
    grid-template-columns: 1fr;
    padding: 40px;
  }
}

.cta-banner-left {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.cta-banner-heading {
  font-size: 38px;
  font-weight: 800;
  line-height: 1.2;
  color: #101828;
}

@media (max-width: 768px) {
  .cta-banner-heading {
    font-size: 28px;
  }
}

.cta-banner-desc {
  font-size: 16px;
  line-height: 1.6;
  color: var(--text-secondary);
}

.cta-benefits-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.benefit-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.check-icon {
  color: #12b76a;
  font-weight: 800;
  font-size: 18px;
}

.benefit-txt {
  font-weight: 600;
  font-size: 15px;
  color: #344054;
}

.cta-banner-btn {
  align-self: flex-start;
  background-color: var(--primary);
  color: #ffffff !important;
  font-weight: 600;
  padding: 14px 28px;
  border-radius: 50px;
  font-size: 15px;
  box-shadow: 0 4px 14px rgba(2, 43, 159, 0.3);
  transition: all 0.3s ease;
}

.cta-banner-btn:hover {
  background-color: #011E70;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(2, 43, 159, 0.4);
}

.cta-banner-right {
  display: flex;
  justify-content: center;
  align-items: center;
}

.cta-right-img {
  width: 100%;
  max-width: 440px;
  height: auto;
  object-fit: contain;
}
</style>
