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
              <p class="eco-desc">ACC Academy thiết lập một hệ sinh thái cộng hưởng, nơi Năng lực con người được nâng tầm và Quy trình vận hành được tối ưu hóa đồng bộ.</p>
              <p class="eco-desc">Kết quả mang lại là một cấu trúc tổ chức tinh gọn, linh hoạt và sở hữu lợi thế cạnh tranh tuyệt đối trong kỷ nguyên Trí tuệ nhân tạo (AI).</p>
            </div>
            <div class="eco-counter-box">
              <div class="eco-number">{{ formatNumber(ecoCount) }}+</div>
              <div class="eco-counter-desc">Dự án & chiến lược đã thực thi thành công</div>
            </div>
          </div>

          <div class="eco-center">
            <img src="/images/Ecosystem_1.png" alt="ACC Academy Ecosystem" class="eco-img" />
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
          <h2 class="bento-title">Năng lực cốt lõi của ACC Academy</h2>
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

    <!-- 8. Testimonials Section (Doanh nhân & Influencers) -->
    <StudentTestimonials />

    <!-- 9. Blog posts Section -->
    <section class="blogs-section">
      <div class="container">
        <div class="blogs-header-row">
          <div class="blogs-header-left">
            <span class="blogs-ui-tag">Thư viện bài viết</span>
            <h2 class="blogs-heading">Cập nhật thông tin mới nhất cùng ACC Academy</h2>
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
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useCourseStore } from '@/stores/courses';
import { useTestimonialStore } from '@/stores/testimonials';
import StudentTestimonials from '@/components/StudentTestimonials.vue';

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

<style scoped src="@/styles/views/Home.css"></style>
