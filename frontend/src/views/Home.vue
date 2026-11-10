<template>
  <div class="home-view">
    <!-- 1. Hero Section (Carousel) -->
    <section v-if="courseStore.bannersLoading || heroSlides.length > 0" class="hero-carousel-section" aria-label="Hero carousel banner">
      <div class="carousel-container">
        <!-- Skeleton Loading State -->
        <div v-if="courseStore.bannersLoading" class="carousel-skeleton">
          <div class="skeleton-shimmer"></div>
        </div>

        <!-- Slides -->
        <template v-else>
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

          <!-- Slider Arrows (only if more than 1 slide) -->
          <button v-if="heroSlides.length > 1" class="carousel-arrow prev" @click="prevSlide" aria-label="Previous slide">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M15 18l-6-6 6-6" />
            </svg>
          </button>
          <button v-if="heroSlides.length > 1" class="carousel-arrow next" @click="nextSlide" aria-label="Next slide">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 18l6-6-6-6" />
            </svg>
          </button>

          <!-- Slider Dots (only if more than 1 slide) -->
          <div v-if="heroSlides.length > 1" class="carousel-dots">
            <button 
              v-for="(slide, index) in heroSlides" 
              :key="index"
              class="carousel-dot"
              :class="{ active: currentSlide === index }"
              @click="setSlide(index)"
              :aria-label="'Go to slide ' + (index + 1)"
            ></button>
          </div>
        </template>
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
                <p class="eco-desc">{{ homeIntroData.desc1 }}</p>
                <p class="eco-desc">{{ homeIntroData.desc2 }}</p>
              </div>
              <div class="eco-counter-box">
                <div class="eco-number">{{ formatNumber(ecoCount) }}+</div>
                <div class="eco-counter-desc">{{ homeIntroData.counter_label }}</div>
              </div>
            </div>

            <!-- Video Player Section (Replaces eco-center image & eco-right services list) -->
            <div 
              class="eco-video-wrapper"
              @mouseenter="hasVideo && handleWarmup()"
              @touchstart.passive="hasVideo && handleWarmup()"
            >
              <div class="eco-video-card" :class="{ 'is-playing': isVideoPlaying, 'is-image-only': !hasVideo }">
                <!-- 1. Video Mode -->
                <template v-if="hasVideo">
                  <!-- Iframe Embed (YouTube / Google Drive) -->
                  <iframe 
                    v-if="videoEmbedUrl && isVideoPlaying"
                    :src="videoEmbedUrl"
                    class="eco-video-element eco-video-iframe"
                    :title="$t('home.introVideoTitle')"
                    frameborder="0"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                    allowfullscreen
                    loading="eager"
                  ></iframe>

                  <!-- HTML5 Video (Direct .mp4 / local file) -->
                  <video 
                    v-else-if="!videoEmbedUrl && isVideoPlaying"
                    ref="ecoVideoRef" 
                    class="eco-video-element" 
                    :poster="formatImageUrl(homeIntroData.poster_url)"
                    controls
                    playsinline
                    muted
                    preload="metadata"
                    :src="homeIntroData.video_url"
                    @play="isVideoPlaying = true"
                    @pause="isVideoPlaying = false"
                    @ended="isVideoPlaying = false"
                  ></video>

                  <!-- Poster Image (when not playing yet) -->
                  <img 
                    v-if="!isVideoPlaying" 
                    :src="formatImageUrl(homeIntroData.poster_url, 'w1200') || '/images/CoE-Thumb.png'" 
                    alt="Video Poster" 
                    class="eco-video-element" 
                    loading="eager"
                    fetchpriority="high"
                    decoding="async"
                  />

                  <!-- Play Overlay Button -->
                  <div v-if="!isVideoPlaying" class="video-play-overlay" @click="handlePlayVideo">
                    <div class="play-pulse-ring"></div>
                    <button class="play-btn-circle" :aria-label="$t('home.playVideo')">
                      <svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor">
                        <polygon points="5 3 19 12 5 21 5 3"></polygon>
                      </svg>
                    </button>
                    <span class="play-btn-label">{{ homeIntroData.btn_label }}</span>
                  </div>
                </template>

                <!-- 2. Pure Image Mode (Khi để trống link video) -->
                <template v-else>
                  <img 
                    :src="formatImageUrl(homeIntroData.poster_url, 'w1200') || '/images/CoE-Thumb.png'" 
                    alt="ACC Academy" 
                    class="eco-video-element" 
                    loading="eager"
                    fetchpriority="high"
                    decoding="async"
                  />
                </template>
              </div>
            </div>
          </div>
      </div>
    </section>

      <!-- 3. Stats Section -->
      <section class="stats-section">
        <div class="container">
          <div class="stats-header">
            <h2 class="stats-title">{{ $t('home.statsTitle') }}</h2>
            <p class="stats-subtitle">
              <span class="stats-line-1">{{ $t('home.statsSubtitle1') }}</span>
              <span class="stats-line-2">{{ $t('home.statsSubtitle2') }}</span>
            </p>
          </div>

          <div class="stats-grid">
            <div class="stat-card-item">
              <div class="stat-num-box">{{ formatNumber(leadersCount) }}+</div>
              <div class="stat-label">{{ $t('home.statsLearners') }}</div>
              <div class="stat-desc">{{ $t('home.statsLearnersDesc') }}</div>
            </div>
            <div class="stat-card-item">
              <div class="stat-num-box">{{ formatNumber(businessesCount) }}+</div>
              <div class="stat-label">{{ $t('home.statsEnterprises') }}</div>
              <div class="stat-desc">{{ $t('home.statsEnterprisesDesc') }}</div>
            </div>
            <div class="stat-card-item">
              <div class="stat-num-box">{{ formatNumber(marketsCount) }}+</div>
              <div class="stat-label">{{ $t('home.statsMarkets') }}</div>
              <div class="stat-desc">{{ $t('home.statsMarketsDesc') }}</div>
            </div>
            <div class="stat-card-item">
              <div class="stat-num-box">{{ formatNumber(npsCount) }}+</div>
              <div class="stat-label">{{ $t('home.statsNps') }}</div>
              <div class="stat-desc">{{ $t('home.statsNpsDesc') }}</div>
            </div>
          </div>
        </div>
      </section>
    </div>

    <!-- 4. Partner Logos Section -->
    <section class="partner-logos-section" v-show="partnerLogos.length > 0">
      <div class="partner-logos-header container">
        <h3 class="partner-logos-title">{{ $t('home.partnerEnterpriseTitle') }}</h3>
      </div>
      
      <div class="partner-display-wrapper">
        <!-- Row 1: Fixed Top (6 đối tác cố định) -->
        <div class="partner-fixed-row-container container">
          <div class="partner-fixed-grid">
            <component
              :is="logo.link ? 'a' : 'div'"
              v-for="(logo, idx) in partnerTopFixed" 
              :key="'fixed-top-' + idx" 
              :href="logo.link || undefined"
              :target="logo.link ? '_blank' : undefined"
              :rel="logo.link ? 'noopener noreferrer' : undefined"
              class="partner-logo-card"
              :title="logo.name"
            >
              <img :src="formatImageUrl(logo.src, 's320')" :alt="logo.name" class="partner-logo-img" loading="eager" decoding="async" referrerpolicy="no-referrer" @load="handleLogoLoad" @error="handleLogoError" />
            </component>
          </div>
        </div>

        <!-- Row 2: Running Marquee (Hàng giữa chạy vô tận) -->
        <div class="partner-marquee-container">
          <div class="partner-marquee-track partner-track-left">
            <component
              :is="logo.link ? 'a' : 'div'"
              v-for="(logo, idx) in partnerMarqueeList" 
              :key="'marquee-a-' + idx" 
              :href="logo.link || undefined"
              :target="logo.link ? '_blank' : undefined"
              :rel="logo.link ? 'noopener noreferrer' : undefined"
              class="partner-logo-card"
              :title="logo.name"
            >
              <img :src="formatImageUrl(logo.src, 's320')" :alt="logo.name" class="partner-logo-img" loading="eager" decoding="async" referrerpolicy="no-referrer" @load="handleLogoLoad" @error="handleLogoError" />
            </component>
            <component
              :is="logo.link ? 'a' : 'div'"
              v-for="(logo, idx) in partnerMarqueeList" 
              :key="'marquee-b-' + idx" 
              :href="logo.link || undefined"
              :target="logo.link ? '_blank' : undefined"
              :rel="logo.link ? 'noopener noreferrer' : undefined"
              class="partner-logo-card"
              :title="logo.name"
            >
              <img :src="formatImageUrl(logo.src, 's320')" :alt="logo.name" class="partner-logo-img" loading="lazy" decoding="async" referrerpolicy="no-referrer" @load="handleLogoLoad" @error="handleLogoError" />
            </component>
          </div>
        </div>

        <!-- Row 3: Fixed Bottom (6 đối tác cố định) -->
        <div class="partner-fixed-row-container container">
          <div class="partner-fixed-grid">
            <component
              :is="logo.link ? 'a' : 'div'"
              v-for="(logo, idx) in partnerBottomFixed" 
              :key="'fixed-bottom-' + idx" 
              :href="logo.link || undefined"
              :target="logo.link ? '_blank' : undefined"
              :rel="logo.link ? 'noopener noreferrer' : undefined"
              class="partner-logo-card"
              :title="logo.name"
            >
              <img :src="formatImageUrl(logo.src, 's320')" :alt="logo.name" class="partner-logo-img" loading="eager" decoding="async" referrerpolicy="no-referrer" @load="handleLogoLoad" @error="handleLogoError" />
            </component>
          </div>
        </div>
      </div>
    </section>

    <!-- 5. Bento Grid Section -->
    <section class="bento-grid-section">
      <div class="container">
        <div class="bento-header">
          <h2 class="bento-title">{{ bentoHeaderData.title }}</h2>
          <p class="bento-subtitle">
            <span class="bento-line-1">{{ bentoHeaderData.line1 }}</span>
            <span class="bento-line-2">{{ bentoHeaderData.line2 }}</span><br />
            <strong>{{ bentoHeaderData.strong }}</strong><br />
            {{ bentoHeaderData.line3 }}
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
          <h2 class="courses-title">{{ $t('home.trainingSchedule') }}</h2>
          <!-- Filter Tabs / Navbar (All, Inhouse, Individual) -->
          <div class="course-filter-tabs">
            <button 
              class="tab-btn" 
              :class="{ active: currentCourseCategory === 'all' }"
              @click="currentCourseCategory = 'all'"
            >
              {{ $t('home.all') }}
            </button>
            <button 
              v-for="cat in homeCategories" 
              :key="cat.slug"
              class="tab-btn" 
              :class="{ active: currentCourseCategory === cat.slug }"
              @click="currentCourseCategory = cat.slug"
            >
               {{ cat.name }}
            </button>
          </div>
        </div>

        <!-- Skeleton Loading State when loading without cached courses -->
        <div class="home-courses-grid" v-if="courseStore.loading && displayedCourses.length === 0">
          <div v-for="n in 4" :key="'skeleton-course-' + n" class="home-course-card course-skeleton-card">
            <div class="home-course-img-link course-skeleton-img">
              <div class="skeleton-shimmer"></div>
            </div>
            <div class="home-course-body">
              <div class="course-skeleton-title">
                <div class="skeleton-shimmer"></div>
              </div>
              <div class="course-skeleton-sub">
                <div class="skeleton-shimmer"></div>
              </div>
            </div>
          </div>
        </div>

        <div class="home-courses-grid" v-else>
          <div 
            v-for="course in displayedCourses" 
            :key="course.id"
            class="home-course-card"
          >
            <router-link :to="'/course/' + (course.handle || course.id)" class="home-course-img-link">
              <div class="home-course-img-box">
                <img :src="formatImageUrl(course.image, 'w800') || '/images/Square-Cover-_1.webp'" :alt="course.title" class="home-course-img" loading="lazy" decoding="async" />
                <span class="card-status-pill" :class="'card-status-' + (course.status || 'ongoing')">
                  {{ course.status === 'upcoming' ? '⏳ Sắp diễn ra' : (course.status === 'completed' ? '🏁 Đã diễn ra' : '🟢 Đang diễn ra') }}
                </span>
              </div>
            </router-link>
            
            <div class="home-course-body">
              <h3 class="home-course-heading">
                <router-link :to="'/course/' + (course.handle || course.id)">{{ course.title }}</router-link>
              </h3>
              <!-- <p class="home-course-desc">{{ stripHtml(course.description) }}</p> -->
              
              <div class="home-course-footer">
                <router-link :to="'/course/' + (course.handle || course.id)" class="arrow-container" :aria-label="$t('common.viewDetails')">
                  <svg class="block-arrow-glow" width="46" height="20" viewBox="0 0 52 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <defs>
                      <linearGradient id="homeArrowBlue" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stop-color="#022B9F"/>
                        <stop offset="100%" stop-color="#2563eb"/>
                      </linearGradient>
                    </defs>
                    <path d="M 2 7 L 34 7 L 34 2 L 50 12 L 34 22 L 34 17 L 2 17 Z" 
                          fill="url(#homeArrowBlue)" />
                  </svg>
                </router-link>
              </div>
            </div>
          </div>
        </div>

        <!-- Load More Button -->
        <div class="load-more-courses-container" v-if="hasMoreCourses">
          <button @click="loadMoreCourses" class="btn-load-more-courses">
            <span>{{ $t('home.loadMoreCourses') }}</span>
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
            <h2 class="blogs-heading">{{ $t('home.lecturersSectionTitle') }}</h2>
          </div>
          <router-link to="/lecturers" class="header-link-with-arrow" aria-label="Xem tất cả giảng viên">
            <span class="header-link-text">{{ $t('common.seeAll') }}</span>
            <svg class="block-arrow-glow" width="40" height="18" viewBox="0 0 52 24" fill="none">
              <path d="M 2 7 L 34 7 L 34 2 L 50 12 L 34 22 L 34 17 L 2 17 Z" fill="#022B9F" />
            </svg>
          </router-link>
        </div>

        <div class="home-lecturers-grid">
          <!-- Skeleton Loading when fetching real lecturers -->
          <template v-if="courseStore.lecturersLoading && featuredLecturers.length === 0">
            <div v-for="n in 4" :key="n" class="home-lecturer-card-item">
              <div class="team-card-wrapper" style="height: 380px; border-radius: 20px; background: linear-gradient(90deg, #f1f5f9 25%, #e2e8f0 37%, #f1f5f9 63%); background-size: 400% 100%; animation: skeletonShimmer 1.4s ease infinite;"></div>
            </div>
          </template>

          <template v-else>
            <div 
              v-for="l in featuredLecturers" 
              :key="l.id" 
              class="home-lecturer-card-item"
            >
              <router-link :to="'/lecturers/' + l.id" class="team-card-wrapper group">
                <div class="team-card-image-box">
                  <img 
                    :src="formatImageUrl(l.avatar, 's500')" 
                    :alt="l.name" 
                    class="team-card-img" 
                    loading="lazy"
                    decoding="async"
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
          </template>
        </div>
      </div>
    </section>

    <!-- 9. Student Shared Feedback Section (Replaces Blog Section) -->
    <section class="student-feedback-section">
      <div class="container">
        <div class="blogs-header-row">
          <div class="blogs-header-left">
            <h2 class="blogs-heading">{{ $t('home.feedbackHeading') }}</h2>
          </div>
          <router-link to="/testimonials" class="header-link-with-arrow" :aria-label="$t('common.seeMore')">
            <span class="header-link-text">{{ $t('common.seeMore') }}</span>
            <svg class="block-arrow-glow" width="40" height="18" viewBox="0 0 52 24" fill="none">
              <path d="M 2 7 L 34 7 L 34 2 L 50 12 L 34 22 L 34 17 L 2 17 Z" fill="#022B9F" />
            </svg>
          </router-link>
        </div>

        <div class="home-feedback-grid">
          <div 
            v-for="p in homeStudentFeedbacks" 
            :key="p.id" 
            class="home-feedback-card"
          >
            <div class="home-feedback-img-box" v-if="p.image">
              <img :src="formatImageUrl(p.image)" :alt="p.name" class="home-feedback-img" referrerpolicy="no-referrer" />
            </div>
            <div class="home-feedback-body">
              <div class="home-student-profile">
                <img :src="formatImageUrl(p.avatar)" :alt="p.name" class="home-profile-avatar" referrerpolicy="no-referrer" />
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

    <!-- Auto Pop-up Consultation Modal (Horizontal Name Card Style) -->
    <Transition name="modal-fade">
    <div v-if="isContactModalOpen" class="consult-modal-overlay" @click.self="closeContactModal">
      <div class="consult-card-visit-horizontal" role="dialog" aria-modal="true" aria-labelledby="consult-modal-title">
        <button class="consult-modal-close" @click="closeContactModal" :aria-label="$t('home.popupClose')">
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
            <p class="card-acc-slogan">{{ $t('home.popupSlogan') }}</p>
          </div>
          <div class="card-decoration-pattern"></div>
        </div>

        <!-- Right Side: Compact Form -->
        <div class="card-visit-right">
          <div class="card-visit-header">
            <h3 id="consult-modal-title" class="card-visit-title">{{ $t('home.popupTitle') }}</h3>
            <p class="card-visit-desc">{{ $t('home.popupDesc') }}</p>
          </div>

          <form @submit.prevent="submitContactModal" class="card-visit-form">
            <div class="card-input-wrap">
              <input 
                v-model="contactForm.fullname" 
                type="text" 
                class="card-input" 
                :placeholder="$t('home.popupNamePlaceholder')" 
                required 
              />
            </div>

            <div class="card-input-wrap" :class="{ 'has-error': homePhoneError }">
              <input 
                v-model="contactForm.phone" 
                type="tel" 
                class="card-input" 
                :placeholder="$t('home.popupPhonePlaceholder')" 
                required 
                @blur="validateHomePhone"
                @input="homePhoneError = ''"
              />
              <span v-if="homePhoneError" class="modal-field-error">{{ homePhoneError }}</span>
            </div>

            <div class="card-input-wrap" :class="{ 'has-error': homeEmailError }">
              <input 
                v-model="contactForm.email" 
                type="email" 
                class="card-input" 
                :placeholder="$t('home.popupEmailPlaceholder')" 
                required 
                @blur="validateHomeEmail"
                @input="homeEmailError = ''"
              />
              <span v-if="homeEmailError" class="modal-field-error">{{ homeEmailError }}</span>
            </div>

            <!-- Anti-spam Honeypot field (hidden from real users, bots will auto-fill) -->
            <div class="ohnohoney" aria-hidden="true">
              <label for="fax_number_modal">Do not fill this</label>
              <input type="text" id="fax_number_modal" v-model="homeHoneypotValue" autocomplete="off" tabindex="-1" />
            </div>

            <button type="submit" class="card-submit-btn" :disabled="isSubmittingContact || homeCooldown > 0">
              <span v-if="homeCooldown > 0">Đã gửi (Đợi {{ homeCooldown }}s)</span>
              <span v-else-if="!isSubmittingContact" style="display: inline-flex; align-items: center; justify-content: center; gap: 8px;">
                <span>{{ $t('home.popupSubmit') }}</span>
                <svg class="block-arrow-glow" width="34" height="15" viewBox="0 0 52 24" fill="none">
                  <path d="M 2 7 L 34 7 L 34 2 L 50 12 L 34 22 L 34 17 L 2 17 Z" fill="#ffffff" />
                </svg>
              </span>
              <span v-else>{{ $t('home.popupSubmitting') }}</span>
            </button>
          </form>
        </div>
      </div>
    </div>
  </Transition>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, onActivated, onDeactivated } from 'vue';
import { onBeforeRouteLeave } from 'vue-router';

defineOptions({
  name: 'Home'
});
import { useI18n } from 'vue-i18n';
import { useCourseStore } from '@/stores/courses';
import { useTestimonialStore } from '@/stores/testimonials';
import { stripHtml } from '@/utils/stripHtml';
import { formatImageUrl } from '@/utils/imageHelper';
import { validateVietnamesePhone, validateEmail } from '@/utils/validation';

const courseStore = useCourseStore();
const testimonialStore = useTestimonialStore();
const { t, locale } = useI18n();

// Ecosystem Video Player & Dynamic Home Intro
const ecoVideoRef = ref(null);
const isVideoPlaying = ref(false);

const defaultHomeIntro = computed(() => ({
  title: t('home.introTitle'),
  desc1: t('home.introDesc1'),
  desc2: t('home.introDesc2'),
  counter_number: 500,
  counter_label: t('home.introCounterLabel'),
  video_url: '',
  poster_url: '/images/CoE-Thumb.png',
  btn_label: t('home.introBtnLabel')
}));

const homeIntroData = computed(() => {
  const admin = courseStore.homeIntroSettings;
  if (!admin) return defaultHomeIntro.value;
  if (locale.value === 'vi') return admin;
  // English: keep admin-configured media/counter, only swap the text
  const d = defaultHomeIntro.value;
  return {
    ...admin,
    title: d.title,
    desc1: d.desc1,
    desc2: d.desc2,
    counter_label: d.counter_label,
    btn_label: d.btn_label
  };
});

const bentoHeaderData = computed(() => {
  const admin = courseStore.homeIntroSettings;
  if (locale.value === 'vi' && admin) {
    return {
      title: admin.bento_title || t('home.bentoTitle'),
      line1: admin.bento_line1 || t('home.bentoLine1'),
      line2: admin.bento_line2 || t('home.bentoLine2'),
      strong: admin.bento_strong || t('home.bentoStrong'),
      line3: admin.bento_line3 || t('home.bentoLine3')
    };
  }
  return {
    title: t('home.bentoTitle'),
    line1: t('home.bentoLine1'),
    line2: t('home.bentoLine2'),
    strong: t('home.bentoStrong'),
    line3: t('home.bentoLine3')
  };
});

// Helper to convert YouTube / Google Drive URLs to embeddable URLs
const convertToEmbedUrl = (url) => {
  if (!url) return null;
  const cleanUrl = url.trim();

  // 1. YouTube
  // Matches: youtube.com/watch?v=ID, youtu.be/ID, youtube.com/embed/ID, youtube.com/shorts/ID
  const ytMatch = cleanUrl.match(/(?:youtube\.com\/(?:watch\?.*v=|embed\/|shorts\/)|youtu\.be\/)([a-zA-Z0-9_-]{11})/i);
  if (ytMatch && ytMatch[1]) {
    // youtube-nocookie: Loads faster (less tracking overhead)
    // mute=1: Muted by default as requested & bypasses browser autoplay restrictions for instant start
    return `https://www.youtube-nocookie.com/embed/${ytMatch[1]}?autoplay=1&mute=1&rel=0&playsinline=1&modestbranding=1&enablejsapi=1`;
  }

  // 2. Google Drive
  // Matches: drive.google.com/file/d/FILE_ID/view, drive.google.com/open?id=FILE_ID
  const driveMatch = cleanUrl.match(/drive\.google\.com\/(?:file\/d\/([a-zA-Z0-9_-]+)|open\?id=([a-zA-Z0-9_-]+))/i);
  if (driveMatch) {
    const fileId = driveMatch[1] || driveMatch[2];
    if (fileId) {
      return `https://drive.google.com/file/d/${fileId}/preview?autoplay=1`;
    }
  }

  return null;
};

const videoEmbedUrl = computed(() => {
  const url = homeIntroData.value?.video_url;
  return convertToEmbedUrl(url);
});

const hasVideo = computed(() => {
  const url = homeIntroData.value?.video_url;
  return Boolean(url && typeof url === 'string' && url.trim().length > 0);
});

const isWarmedUp = ref(false);
const handleWarmup = () => {
  if (isWarmedUp.value) return;
  isWarmedUp.value = true;
  if (videoEmbedUrl.value) {
    // Prefetch YouTube player document ahead of time for instant playback
    const existing = document.querySelector('link[data-warmup-video]');
    if (!existing) {
      const link = document.createElement('link');
      link.rel = 'prefetch';
      link.as = 'document';
      link.href = videoEmbedUrl.value;
      link.setAttribute('data-warmup-video', 'true');
      document.head.appendChild(link);
    }
  } else if (ecoVideoRef.value) {
    ecoVideoRef.value.preload = 'auto';
  }
};

const setupVideoWarmupObserver = () => {
  if (typeof window === 'undefined') return;
  const ecoWrapper = document.querySelector('.eco-video-wrapper');
  if (ecoWrapper && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      if (entries[0] && entries[0].isIntersecting) {
        handleWarmup();
        observer.disconnect();
      }
    }, { rootMargin: '300px' });
    observer.observe(ecoWrapper);
  }
};

const handlePlayVideo = () => {
  isVideoPlaying.value = true;
  if (!videoEmbedUrl.value && ecoVideoRef.value) {
    ecoVideoRef.value.muted = true;
    ecoVideoRef.value.play().catch(() => {});
  }
};

// 1. Hero Carousel
const currentSlide = ref(0);
const heroSlides = computed(() => {
  if (courseStore.banners && courseStore.banners.length > 0) {
    return courseStore.banners.map(b => {
      const link = (b.link || '/').trim();
      const isHttp = /^https?:\/\//i.test(link) || link.startsWith('//');
      return {
        desktopImage: formatImageUrl(b.desktop_image, 's1920'),
        mobileImage: formatImageUrl(b.mobile_image || b.desktop_image, 's1080'),
        link: link || '/',
        title: b.title,
        isExternal: Boolean(b.is_external || isHttp)
      };
    });
  }
  return [];
});

let heroInterval = null;
const startHeroAutoplay = () => {
  stopHeroAutoplay();
  if (heroSlides.value.length <= 1) return;
  heroInterval = setInterval(() => {
    const len = heroSlides.value.length;
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

watch(heroSlides, (newSlides) => {
  if (currentSlide.value >= newSlides.length) {
    currentSlide.value = 0;
  }
  startHeroAutoplay();
});

// 2. Ecosystem & Stats Counter Animation
const ecoTitleWords = computed(() => {
  const title = (homeIntroData.value && homeIntroData.value.title) || 'Kiến tạo năng lực – Dẫn dắt chuyển đổi bền vững';
  return title.trim().split(/\s+/);
});
const ecoTitleAnimated = ref(false);

let ecoObserver = null;
let countersObserver = null;
let partnerObserver = null;
let animRafIds = [];

const setupEcoTitleObserver = () => {
  if (ecoObserver) {
    ecoObserver.disconnect();
  }
  ecoObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        ecoTitleAnimated.value = true;
        ecoObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });

  const target = document.querySelector('.eco-main-title');
  if (target) ecoObserver.observe(target);
};

const ecoCount = ref(0);
const leadersCount = ref(0);
const businessesCount = ref(0);
const marketsCount = ref(0);
const npsCount = ref(0);
const countersAnimated = ref(false);

const animateNumber = (refVar, target, duration = 1500) => {
  let start = null;
  let rafId = null;
  const step = (timestamp) => {
    if (!start) start = timestamp;
    const progress = Math.min((timestamp - start) / duration, 1);
    refVar.value = Math.floor(progress * target);
    if (progress < 1) {
      rafId = window.requestAnimationFrame(step);
      animRafIds.push(rafId);
    } else {
      refVar.value = target;
    }
  };
  rafId = window.requestAnimationFrame(step);
  animRafIds.push(rafId);
};

const setupCountersObserver = () => {
  if (countersObserver) {
    countersObserver.disconnect();
  }
  countersObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !countersAnimated.value) {
        countersAnimated.value = true;
        const targetEco = (homeIntroData.value && homeIntroData.value.counter_number) || 500;
        animateNumber(ecoCount, targetEco, 1200);
        animateNumber(leadersCount, 17000, 1800);
        animateNumber(businessesCount, 70, 1500);
        animateNumber(marketsCount, 7, 1000);
        animateNumber(npsCount, 85, 1200);
        countersObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  const target = document.querySelector('.stats-trigger-zone');
  if (target) countersObserver.observe(target);
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

// 3. Partner Logos Setup & Preloading
const partnerLogos = computed(() => {
  return courseStore.partners || [];
});

const partnerTopFixed = computed(() => {
  return partnerLogos.value.filter(p => p.row_type === 'top_fixed').slice(0, 6);
});

const partnerBottomFixed = computed(() => {
  return partnerLogos.value.filter(p => p.row_type === 'bottom_fixed').slice(0, 6);
});

const partnerMarqueeList = computed(() => {
  return partnerLogos.value.filter(p => !p.row_type || p.row_type === 'marquee');
});

const isPartnersReady = ref(true);

const handleLogoError = (e) => {
  const img = e.target;
  if (!img || img.dataset.retried) return;
  img.dataset.retried = 'true';
  const m = img.src.match(/(?:d\/|[?&]id=)([a-zA-Z0-9_-]+)/);
  if (m && m[1]) {
    const fileId = m[1];
    if (img.src.includes('lh3.googleusercontent.com')) {
      img.src = `https://drive.google.com/thumbnail?id=${fileId}&sz=w320`;
    } else {
      img.src = `https://lh3.googleusercontent.com/d/${fileId}=s320`;
    }
  }
};

const handleLogoLoad = (e) => {
  const img = e.target;
  if (!img || !img.naturalWidth || !img.naturalHeight) return;
  const ratio = img.naturalWidth / img.naturalHeight;
  // If logo is square or vertical (ratio < 1.35), scale up to balance visual area with wide horizontal logos
  if (ratio < 1.35) {
    img.style.setProperty('--logo-scale', '1.2');
  } else if (ratio < 1.85) {
    img.style.setProperty('--logo-scale', '1.1');
  } else {
    img.style.setProperty('--logo-scale', '1');
  }
};

const preloadPartnerLogos = (partners) => {
  if (!partners || partners.length === 0) return;

  // Non-blocking background image warm-up
  const topImages = partners.filter(p => p.row_type === 'top_fixed').slice(0, 6).map(p => p.src);
  const marqueeFirstImages = partners.filter(p => !p.row_type || p.row_type === 'marquee').slice(0, 10).map(p => p.src);
  const bottomImages = partners.filter(p => p.row_type === 'bottom_fixed').slice(0, 6).map(p => p.src);

  const initialImagesToLoad = [...new Set([...topImages, ...marqueeFirstImages, ...bottomImages])].filter(Boolean);
  initialImagesToLoad.forEach(src => {
    const img = new Image();
    img.referrerPolicy = 'no-referrer';
    img.src = formatImageUrl(src, 's320');
  });
};

watch(partnerLogos, (newPartners) => {
  if (newPartners && newPartners.length > 0) {
    preloadPartnerLogos(newPartners);
  }
}, { immediate: true });

// Partner Logo Reveal Observer
const partnerRevealActive = ref(false);
const setupPartnerObserver = () => {
  if (partnerObserver) {
    partnerObserver.disconnect();
  }
  partnerObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        partnerRevealActive.value = true;
        partnerObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.05 });

  const target = document.querySelector('.partner-logos-section');
  if (target) partnerObserver.observe(target);
};

// Bento Grid Cards Data with F5 Rotation
const rawBentoCards = computed(() => [
  {
    id: 'ca-nhan',
    title: t('home.bentoPersonalTitle'),
    desc: t('home.bentoPersonalDesc'),
    bgClass: 'bg-dark-blue has-dark-overlay',
    contentClass: 'content-center text-white',
    bgImage: '/images/canhan.jpg',
    bgImgClass: 'bento-bg-tint',
    link: '/courses/category/dao-tao-ca-nhan'
  },
  {
    id: 'inhouse',
    title: t('home.bentoInhouseTitle'),
    desc: t('home.bentoInhouseDesc'),
    bgClass: 'bg-slate-gray has-dark-overlay',
    contentClass: 'content-center text-white',
    bgImage: '/images/inhouse.jpg',
    bgImgClass: 'bento-bg-tint',
    link: '/courses/category/dao-tao-doanh-nghiep'
  },
  {
    id: 'andrews',
    title: t('home.bentoAndrewsTitle'),
    desc: t('home.bentoAndrewsDesc'),
    bgClass: 'bg-slate-gray has-dark-overlay',
    contentClass: 'content-top text-white',
    bgImage: '/images/mba.jpg',
    bgImgClass: 'bento-bg-tint',
    link: '/admissions'
  }
]);

const bentoCardsOffset = ref(0);

const getBentoRotationOffset = () => {
  if (typeof window !== 'undefined' && window.sessionStorage) {
    let currentIdx = parseInt(sessionStorage.getItem('acc_bento_rotate_idx') || '0', 10);
    const nextIdx = (currentIdx + 1) % rawBentoCards.value.length;
    sessionStorage.setItem('acc_bento_rotate_idx', nextIdx.toString());
    return currentIdx;
  }
  return 0;
};

const bentoCards = computed(() => {
  const cards = rawBentoCards.value;
  const offset = bentoCardsOffset.value;
  const len = cards.length;
  const rotated = [];
  for (let i = 0; i < len; i++) {
    rotated.push(cards[(i + offset) % len]);
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
const homeCategories = computed(() => {
  return (courseStore.categories || []).filter(c => c.slug !== 'bundles');
});
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
  const list = courseStore.lecturers || [];
  const featured = list.filter(l => l.is_featured);
  if (featured.length > 0) {
    return featured.slice(0, 4);
  }
  return list.slice(0, 4);
});

// 10. Student Shared Feedbacks photos for Home from API
const homeStudentFeedbacks = computed(() => {
  const photoList = testimonialStore.photoTestimonials || [];
  if (photoList.length > 0) {
    return photoList.slice(0, 3);
  }
  return (testimonialStore.testimonials || []).slice(0, 3);
});

// 11. Consultation Auto Pop-up Modal State & Handler
const isContactModalOpen = ref(false);
const isSubmittingContact = ref(false);
const homePhoneError = ref('');
const homeEmailError = ref('');

// Anti-spam Honeypot & Cooldown state
const homeHoneypotValue = ref('');
const homeCooldown = ref(0);
let homeCooldownTimer = null;

const startHomeCooldown = (seconds = 30) => {
  homeCooldown.value = seconds;
  if (homeCooldownTimer) clearInterval(homeCooldownTimer);
  homeCooldownTimer = setInterval(() => {
    homeCooldown.value -= 1;
    if (homeCooldown.value <= 0) {
      clearInterval(homeCooldownTimer);
      homeCooldownTimer = null;
    }
  }, 1000);
};

const contactForm = ref({
  fullname: '',
  phone: '',
  email: '',
  courseHandle: '',
  message: ''
});

const validateHomePhone = () => {
  if (!contactForm.value.phone) {
    homePhoneError.value = '';
    return;
  }
  const check = validateVietnamesePhone(contactForm.value.phone);
  homePhoneError.value = check.isValid ? '' : check.error;
};

const validateHomeEmail = () => {
  if (!contactForm.value.email) {
    homeEmailError.value = '';
    return;
  }
  const check = validateEmail(contactForm.value.email);
  homeEmailError.value = check.isValid ? '' : check.error;
};

const MODAL_STORAGE_KEY = 'acc_home_consult_modal_date';
let modalTimer = null;

const checkAndShowContactModal = () => {
  try {
    const today = new Date().toDateString();
    const lastShownDate = localStorage.getItem(MODAL_STORAGE_KEY);
    if (lastShownDate === today) {
      return;
    }

    modalTimer = setTimeout(() => {
      isContactModalOpen.value = true;
      try {
        localStorage.setItem(MODAL_STORAGE_KEY, today);
      } catch (e) {
        // Ignore localStorage error if storage is restricted
      }
    }, 600);
  } catch (err) {
    modalTimer = setTimeout(() => {
      isContactModalOpen.value = true;
    }, 600);
  }
};

const closeContactModal = () => {
  isContactModalOpen.value = false;
  homePhoneError.value = '';
  homeEmailError.value = '';
};

const submitContactModal = async () => {
  if (homeCooldown.value > 0) {
    courseStore.showToast(`Bạn vừa gửi yêu cầu rồi. Vui lòng đợi ${homeCooldown.value} giây trước khi gửi tiếp!`, 'warning');
    return;
  }

  const cleanName = (contactForm.value.fullname || '').trim();
  if (!cleanName) {
    courseStore.showToast('Vui lòng nhập họ và tên của bạn', 'warning');
    return;
  }

  const phoneCheck = validateVietnamesePhone(contactForm.value.phone);
  if (!phoneCheck.isValid) {
    homePhoneError.value = phoneCheck.error;
    courseStore.showToast(phoneCheck.error, 'warning');
    return;
  }
  homePhoneError.value = '';

  const emailCheck = validateEmail(contactForm.value.email);
  if (!emailCheck.isValid) {
    homeEmailError.value = emailCheck.error;
    courseStore.showToast(emailCheck.error, 'warning');
    return;
  }
  homeEmailError.value = '';

  isSubmittingContact.value = true;
  try {
    const nameParts = cleanName.split(' ');
    const lastName = nameParts.length > 0 ? nameParts[nameParts.length - 1] : '';
    const firstName = nameParts.length > 1 ? nameParts[0] : cleanName;
    const middleName = nameParts.length > 2 ? nameParts.slice(1, -1).join(' ') : '';

    await courseStore.sendContact(
      firstName,
      middleName,
      lastName,
      emailCheck.email,
      phoneCheck.normalized,
      contactForm.value.courseHandle || 'Tư vấn thông tin (Popup Trang Chủ)',
      contactForm.value.message || 'Khách hàng đăng ký tư vấn từ Popup Trang Chủ',
      homeHoneypotValue.value
    );

    courseStore.showToast(t('home.popupSuccess'), 'success');
    startHomeCooldown(30);
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

let lastHomeScrollY = 0;
let isNavigatingAway = false;

const onWindowScroll = () => {
  if (!isNavigatingAway && typeof window !== 'undefined') {
    const y = window.scrollY;
    if (y > 100) {
      lastHomeScrollY = y;
    }
  }
};

onMounted(() => {
  window.addEventListener('scroll', onWindowScroll, { passive: true });
  bentoCardsOffset.value = getBentoRotationOffset();
  startHeroAutoplay();
  setupEcoTitleObserver();
  setupCountersObserver();
  setupPartnerObserver();
  setupVideoWarmupObserver();

  // Auto pop-up consultation modal (at most once per day)
  checkAndShowContactModal();

  courseStore.fetchCourses();
  courseStore.fetchLecturers();
  courseStore.fetchHomeIntroSettings(true);
  courseStore.fetchPartners();
  testimonialStore.fetchTestimonials();
});

onBeforeRouteLeave((to, from) => {
  isNavigatingAway = true;
  const currentY = window.scrollY > 100 ? window.scrollY : lastHomeScrollY;
  if (currentY > 100) {
    lastHomeScrollY = currentY;
    try {
      sessionStorage.setItem('home_scroll_y', String(currentY));
    } catch (e) {}
  }
});

onDeactivated(() => {
  stopHeroAutoplay();
});

onActivated(() => {
  isNavigatingAway = false;
  startHeroAutoplay();
  const targetY = lastHomeScrollY || Number(sessionStorage.getItem('home_scroll_y') || 0);
  if (targetY > 100) {
    const doScroll = () => {
      window.scrollTo({ top: targetY, behavior: 'instant' });
    };
    doScroll();
    requestAnimationFrame(doScroll);
    setTimeout(doScroll, 50);
    setTimeout(doScroll, 150);
    setTimeout(doScroll, 300);
  }
});

onUnmounted(() => {
  window.removeEventListener('scroll', onWindowScroll);
  stopHeroAutoplay();
  if (modalTimer) {
    clearTimeout(modalTimer);
    modalTimer = null;
  }
  if (ecoObserver) {
    ecoObserver.disconnect();
    ecoObserver = null;
  }
  if (countersObserver) {
    countersObserver.disconnect();
    countersObserver = null;
  }
  if (partnerObserver) {
    partnerObserver.disconnect();
    partnerObserver = null;
  }
  animRafIds.forEach(id => cancelAnimationFrame(id));
  animRafIds = [];
});
</script>

<style scoped src="@/styles/views/Home.css"></style>
