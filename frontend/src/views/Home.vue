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

          <div class="eco-center">
            <img src="/images/Ecosystem_1.png" alt="ACC Academy Ecosystem" class="eco-img" />
          </div>

          <div class="eco-right">
            <div class="services-list-card">
              <h3 class="services-card-title">Dịch vụ của chúng tôi</h3>
              <ul class="services-card-links">
                <li>
                  <router-link to="/corporate/dao-tao" class="service-item-link">
                    <span>Đào tạo In-house cho Doanh nghiệp</span>
                    <span class="arrow-icon">&rarr;</span>
                  </router-link>
                </li>
                <li>
                  <router-link to="/courses/category/ky-nang-chuyen-mon" class="service-item-link">
                    <span>Tuyển sinh các chương trình sau đại học</span>
                    <span class="arrow-icon">&rarr;</span>
                  </router-link>
                </li>
                <li>
                  <router-link to="/corporate/coe" class="service-item-link">
                    <span>Tư vấn Ứng dụng AI & Tự động hóa</span>
                    <span class="arrow-icon">&rarr;</span>
                  </router-link>
                </li>
                <li>
                  <router-link to="/contact" class="service-item-link">
                    <span>Tư vấn Marketing & Chuyển đổi số</span>
                    <span class="arrow-icon">&rarr;</span>
                  </router-link>
                </li>
                <li>
                  <router-link to="/courses/category/ky-nang-ai" class="service-item-link">
                    <span>Đào tạo dành cho Cá nhân</span>
                    <span class="arrow-icon">&rarr;</span>
                  </router-link>
                </li>
              </ul>
              <router-link to="/contact" class="eco-cta-btn">
                <span>Liên hệ tư vấn</span>
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
      <div class="container">
        <h3 class="partner-logos-title">130+ doanh nghiệp hàng đầu đã hợp tác</h3>
        
        <div class="partner-logos-grid" :class="{ 'reveal-active': partnerRevealActive }">
          <div 
            v-for="(logo, idx) in partnerLogos" 
            :key="idx" 
            class="partner-logo-card"
            :style="{ '--delay-idx': idx }"
          >
            <img :src="logo.src" :alt="logo.name" class="partner-logo-img" referrerpolicy="no-referrer" />
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

          <!-- Card 2: Enterprise Training (Square) -->
          <div class="bento-card card-square bg-slate-gray">
            <router-link to="/corporate/dao-tao" class="bento-card-overlay-link"></router-link>
            <div class="bento-card-content content-top text-white">
              <h3 class="bento-card-title">Đào tạo doanh nghiệp</h3>
              <p class="bento-card-desc">Chương trình Inhouse may đo và các Khóa đào tạo cá nhân - chuyển hóa kiến thức quốc tế thành hành vi và hiệu suất trong tổ chức của bạn.</p>
            </div>
            <div class="bento-card-bottom-mockup">
              <img src="/images/Service_card_dfee141b-d689-4e2c-bec9-350c9f407f84.png" alt="Đào tạo doanh nghiệp" class="bento-mockup-img" />
            </div>
          </div>

          <!-- Card 3: Exclusive Andrews Admission (Square) -->
          <div class="bento-card card-square bg-slate-gray">
            <router-link to="/courses/category/ky-nang-chuyen-mon" class="bento-card-overlay-link"></router-link>
            <img src="/images/service_card_2.webp" alt="Tuyển sinh độc quyền Andrews" class="bento-card-bg bento-bg-tint" />
            <div class="bento-card-content content-top text-white">
              <h3 class="bento-card-title">Tuyển sinh độc quyền Andrews</h3>
              <p class="bento-card-desc">Thạc sĩ MBA Andrews tại Việt Nam và GEI - Hội thảo Lãnh đạo cấp cao tại Michigan, Hoa Kỳ. ACC là đại diện duy nhất tại Việt Nam.</p>
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
              <router-link to="/courses/category/ky-nang-ai" class="bento-arrow-btn btn-teal">
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

    <!-- 7. Comprehensive Training Solutions (Courses Grid Section) -->
    <section class="courses-section">
      <div class="container">
        <div class="courses-header">
          <span class="courses-ui-tag">Giải pháp đào tạo</span>
          <h2 class="courses-title">Giải pháp đào tạo phát triển năng lực toàn diện</h2>
          <p class="courses-subtitle">ACC cung cấp các chương trình đào tạo được thiết kế theo từng cấp độ, chức năng và nhu cầu của tổ chức, giúp chuyển hóa kiến thức thành năng lực thực tiễn và hiệu quả công việc.</p>
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
                <span class="home-course-level-tag">{{ course.level || 'Tất cả cấp độ' }}</span>
              </div>
            </router-link>
            
            <div class="home-course-body">
              <h3 class="home-course-heading">
                <router-link :to="'/course/' + (course.handle || course.id)">{{ course.title }}</router-link>
              </h3>
              <p class="home-course-desc">{{ course.description }}</p>
              
              <div class="home-course-footer">
                <div class="home-course-price">
                  <span class="price-orig" v-if="course.originalPrice">{{ formatPrice(course.originalPrice) }}</span>
                  <span class="price-val">{{ formatPrice(course.price) }}</span>
                </div>
                <router-link :to="'/course/' + (course.handle || course.id)" class="home-course-btn">
                  <span>Chi tiết</span>
                  <span class="arrow">&rarr;</span>
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
  { name: 'Đối tác 131', src: 'https://drive.google.com/thumbnail?id=1lyu7z2iak8pq6tK4AQ1XexIdPBt_uLG6&sz=w400' }
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

// 8. Dynamic Courses Data from courseStore
const homeCourses = computed(() => {
  if (courseStore.courses && courseStore.courses.length > 0) {
    return courseStore.courses;
  }
  return [
    {
      id: 1,
      title: 'ChatGPT & AI Work Automation',
      description: 'Làm chủ ChatGPT và các công cụ GenAI để tự động hóa 70% công việc văn phòng hằng ngày.',
      handle: 'chatgpt-work-automation',
      price: 1950000,
      originalPrice: 3500000,
      image: '/images/AIP_AIProductivity_SQR.png',
      level: 'Mọi cấp độ'
    },
    {
      id: 2,
      title: 'AI Center of Excellence (CoE)',
      description: 'Xây dựng trung tâm năng lực AI cốt lõi và lộ trình chuyển đổi số toàn diện cho doanh nghiệp.',
      handle: 'ai-center-of-excellence',
      price: 4800000,
      originalPrice: 7500000,
      image: '/images/CoE-Thumb.png',
      level: 'Chuyên sâu'
    },
    {
      id: 3,
      title: 'Phân tích dữ liệu & Dashboard với Looker Studio',
      description: 'Chuyển hóa dữ liệu thô thành báo cáo trực quan sinh động hỗ trợ ra quyết định kinh doanh tức thì.',
      handle: 'looker-studio-data-analysis',
      price: 2450000,
      originalPrice: 4200000,
      image: '/images/LS_Looker_Studio_for_Everyone_SQR.png',
      level: 'Trung cấp'
    },
    {
      id: 4,
      title: 'Ứng dụng Claude AI & Midjourney nâng cao',
      description: 'Khai phá sức mạnh xử lý ngôn ngữ tự nhiên phức tạp và tạo tác phẩm hình ảnh truyền thông đỉnh cao.',
      handle: 'claude-ai-midjourney-mastery',
      price: 2950000,
      originalPrice: 4800000,
      image: '/images/Claude_Productivity.png',
      level: 'Nâng cao'
    },
    {
      id: 5,
      title: 'Kỹ năng Giao tiếp & Thuyết phục Lãnh đạo',
      description: 'Phát triển năng lực truyền tải thông điệp tạo tác động cao cho các cấp quản lý và lãnh đạo.',
      handle: 'leadership-communication-skills',
      price: 3200000,
      originalPrice: 5000000,
      image: '/images/Frame_1707482601.png',
      level: 'Trung cấp'
    },
    {
      id: 6,
      title: 'Xây dựng Quy trình Tự động hóa với Make & n8n',
      description: 'Thiết lập luồng tự động hóa tích hợp đa ứng dụng doanh nghiệp mà không cần lập trình chuyên sâu.',
      handle: 'workflow-automation-make-n8n',
      price: 2750000,
      originalPrice: 4500000,
      image: '/images/AI_Workflow_Automation_8decdc78-096c-4924-9bf9-128ca34359a4.png',
      level: 'Trung cấp'
    },
    {
      id: 7,
      title: 'Chiến lược Marketing Dựa trên Dữ liệu (Data-Driven)',
      description: 'Tối ưu hiệu quả các chiến dịch tiếp thị số thông qua phân tích hành vi khách hàng và đo lường ROI.',
      handle: 'data-driven-marketing-strategy',
      price: 3500000,
      originalPrice: 5500000,
      image: '/images/Data_Bootcamp.png',
      level: 'Nâng cao'
    },
    {
      id: 8,
      title: 'Google Gemini & Copilot for Microsoft 365',
      description: 'Đột phá hiệu suất văn phòng với bộ đôi công cụ trợ lý ảo thông minh hàng đầu hiện nay.',
      handle: 'gemini-copilot-m365-mastery',
      price: 1850000,
      originalPrice: 3200000,
      image: '/images/Gemini_Productivity.png',
      level: 'Cơ bản'
    },
    {
      id: 9,
      title: 'Tư duy Quản trị & Ra quyết định với AI',
      description: 'Trang bị khung tư duy ứng dụng AI cho các nhà quản lý để tối ưu hóa nguồn lực và ra quyết định chuẩn xác.',
      handle: 'ai-decision-making-for-leaders',
      price: 4200000,
      originalPrice: 6500000,
      image: '/images/AID_AI_for_Decision_Making_SQR.png',
      level: 'Quản lý'
    },
    {
      id: 10,
      title: 'Kỹ năng Excel Chuyên sâu & VBA Tự động hóa',
      description: 'Nâng cấp kỹ năng xử lý bảng tính phức tạp, tạo báo cáo tự động và viết mã lệnh VBA cơ bản.',
      handle: 'advanced-excel-vba-automation',
      price: 2150000,
      originalPrice: 3800000,
      image: '/images/Excell_skill_e9651cdc-6ff9-48ed-9e96-d4e0b6419a41.png',
      level: 'Trung cấp'
    },
    {
      id: 11,
      title: 'Quản trị Dự án Chuyển đổi Số',
      description: 'Phương pháp luận và bộ công cụ thực chiến quản trị các dự án công nghệ số trong tổ chức.',
      handle: 'digital-transformation-project-management',
      price: 3900000,
      originalPrice: 6000000,
      image: '/images/DataFlow_Automation.png',
      level: 'Nâng cao'
    },
    {
      id: 12,
      title: 'Sáng tạo Nội dung Multi-channel với Generative AI',
      description: 'Tạo hàng loạt nội dung hình ảnh, video và văn bản đa kênh chất lượng cao chuẩn thương hiệu.',
      handle: 'multichannel-content-generative-ai',
      price: 2600000,
      originalPrice: 4200000,
      image: '/images/AI_Content_Mastery.png',
      level: 'Mọi cấp độ'
    }
  ];
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

// 9. Blog posts list from courseStore
const blogPosts = computed(() => courseStore.getBlogPosts);

onMounted(() => {
  startHeroAutoplay();
  setupEcoTitleObserver();
  setupCountersObserver();
  setupPartnerObserver();
  startTabProgress();
  if (courseStore.courses.length === 0) {
    courseStore.fetchCourses();
  }
});

onUnmounted(() => {
  stopHeroAutoplay();
  stopTabProgress();
});
</script>

<style scoped src="@/styles/views/Home.css"></style>
