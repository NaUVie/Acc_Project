<template>
  <div class="admissions-view">
    <!-- Hero Banner Section -->
    <section class="admissions-hero">
      <div class="container hero-container">

        <h1 class="hero-title animate-fade-in">
          {{ $t('admissions.heroTitle1') }} <br />
          &amp; <span class="gradient-text">{{ $t('admissions.heroTitle2') }}</span>
        </h1>
        <p class="hero-subtitle animate-fade-in">
          {{ $t('admissions.heroSubtitle') }}
        </p>

        <!-- Quick Jump Pills -->
        <div class="jump-pills">
          <button @click="scrollToSection('mba')" class="jump-pill active">
           {{ $t('admissions.jumpMba') }}
          </button>
          <!-- <button @click="scrollToSection('mini-mba')" class="jump-pill">
            ⚡ Mini MBA
          </button> -->
          <button @click="scrollToSection('gei')" class="jump-pill">
          {{ $t('admissions.jumpGei') }}
          </button>
        </div>
      </div>
    </section>

    <!-- Admission Programs Section -->
    <section class="programs-section container">
      
      <!-- Program 1: MBA Andrews -->
      <div id="mba" class="program-card glass-card animate-slide-up">
        <div class="program-grid">
          <div class="program-media">
            <img src="/images/andrew.jpg" alt="MBA Andrews Hoa Kỳ" class="program-img" />
            <div class="program-tag-overlay">{{ $t('admissions.mbaTag') }}</div>
          </div>
          <div class="program-content">
            <span class="program-category">{{ $t('admissions.mbaCategory') }}</span>
            <h2 class="program-title">{{ $t('admissions.mbaTitle') }}</h2>
            <p class="program-desc">{{ $t('admissions.mbaDesc') }}</p>

            <div class="program-highlights">
              <div class="highlight-item">
                <span>{{ $t('admissions.mbaH1') }}</span>
              </div>
              <div class="highlight-item">
                <span>{{ $t('admissions.mbaH2') }}</span>
              </div>
              <div class="highlight-item">
                <span>{{ $t('admissions.mbaH3') }}</span>
              </div>
            </div>

            <div class="program-footer">
              <router-link to="/admissions/detail/mba" class="btn btn-primary">
                {{ $t('admissions.btnMbaDetail') }} &rarr;
              </router-link>
              <router-link to="/contact?program=mba" class="btn btn-outline">
                {{ $t('admissions.btnConsult') }}
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Program 2: Mini MBA -->
      <!-- <div id="mini-mba" class="program-card glass-card animate-slide-up">
        <div class="program-grid reverse">
          <div class="program-media">
            <img src="/images/Service_card_2.png" alt="Mini MBA Thực chiến" class="program-img" />
            <div class="program-tag-overlay badge-teal">Quản trị Tinh gọn</div>
          </div>
          <div class="program-content">
            <span class="program-category">QUẢN TRỊ THỰC CHUYÊN SÂU</span>
            <h2 class="program-title">Mini MBA Practical</h2>
            <p class="program-desc">
              Chương trình tinh gọn cô đọng những giá trị cốt lõi nhất của MBA trong 3-6 tháng. 
              Dành riêng cho các Giám đốc bộ phận, Quản lý cấp trung và Chủ doanh nghiệp SME 
              muốn tối ưu năng lực vận hành, tài chính, nhân sự và chiến lược tăng trưởng tức thì.
            </p>

            <div class="program-highlights">
              <div class="highlight-item">
                <span class="icon">⚡</span>
                <span>Tập trung 100% vào bài tập & case study thực tế</span>
              </div>
              <div class="highlight-item">
                <span class="icon">👨‍🏫</span>
                <span>Giảng dạy bởi đội ngũ Chuyên gia & C-Level thực chiến</span>
              </div>
              <div class="highlight-item">
                <span class="icon">📈</span>
                <span>Áp dụng ngay giải pháp vào doanh nghiệp của học viên</span>
              </div>
            </div>

            <div class="program-footer">
              <router-link to="/admissions/detail/mini-mba" class="btn btn-primary">
                Xem chi tiết bài viết Mini MBA &rarr;
              </router-link>
              <router-link to="/contact?program=mini-mba" class="btn btn-outline">
                {{ $t('admissions.btnConsult') }}
              </router-link>
            </div>
          </div>
        </div>
      </div> -->

      <!-- Program 3: GEI (GOLBAL EXECUTIVE INSTITUTE) -->
      <div id="gei" class="program-card glass-card animate-slide-up">
        <div class="program-grid">
          <div class="program-media">
            <img src="/images/GEL.jpg" alt="GOLBAL EXECUTIVE INSTITUTE (GEI)" class="program-img" />
            <div class="program-tag-overlay badge-gold">{{ $t('admissions.geiTag') }}</div>
          </div>
          <div class="program-content">
            <span class="program-category">{{ $t('admissions.geiCategory') }}</span>
            <h2 class="program-title">{{ $t('admissions.jumpGei') }}</h2>
            <p class="program-desc">{{ $t('admissions.geiDesc') }}</p>

            <div class="program-highlights">
              <div class="highlight-item">
                <span>{{ $t('admissions.geiH1') }}</span>
              </div>
              <div class="highlight-item">
                <span>{{ $t('admissions.geiH2') }}</span>
              </div>
              <div class="highlight-item">
                <span>{{ $t('admissions.geiH3') }}</span>
              </div>
            </div>

            <div class="program-footer">
              <router-link to="/admissions/detail/gei" class="btn btn-primary">
                {{ $t('admissions.btnGeiDetail') }} &rarr;
              </router-link>
              <router-link to="/contact?program=gei" class="btn btn-outline">
                {{ $t('admissions.btnConsult') }}
              </router-link>
            </div>
          </div>
        </div>
      </div>

    </section>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';

const scrollToSection = (id) => {
  const el = document.getElementById(id);
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
};

onMounted(() => {
  window.scrollTo(0, 0);
});
</script>

<style scoped src="@/styles/views/tuyen-sinh/AdmissionsView.css"></style>
