<template>
  <div class="admissions-view">
    <!-- Hero Banner Section (Luxury Corporate Presentation Slide Style) -->
    <section class="admissions-hero">
      <div class="hero-bg-media">
        <img src="/images/TuyenSinh.jpg" alt="Tuyển sinh ACC & Andrews" class="hero-bg-img" loading="eager" decoding="async" />
        <div class="hero-gradient-overlay"></div>
      </div>

      <div class="container hero-inner-container">
        <!-- 1. Top Co-Branding: ACC | Andrews University -->
        <div class="hero-brand-row animate-fade-in">
          <div class="brand-acc">
            <img src="/images/logo3.png" alt="ACC Kết Nối Tri Thức" class="hero-acc-logo" />
          </div>
  
        </div>

        <!-- 2. Overline Tag -->
        <div class="hero-tagline animate-fade-in">
          {{ $t('admissions.heroTagline') }}
        </div>

        <!-- 3. Two-Tone Main Title -->
        <h1 class="hero-main-title animate-fade-in">
          <span class="title-primary">{{ $t('admissions.heroTitle1') }}</span>
          <span class="title-accent">{{ $t('admissions.heroTitle2') }}</span>
        </h1>

        <!-- 4. Subtitle / Description -->
        <p class="hero-description animate-fade-in">
          {{ $t('admissions.heroSubtitle') }}
        </p>

        <!-- 5. Program Badges / Capsules -->
        <!-- <div class="hero-programs-list animate-fade-in">
          <a 
            href="#mba" 
            @click.prevent="scrollToProgram('mba')" 
            class="program-pill-row"
            title="Xem chi tiết chương trình MBA Andrews"
          >
            <span class="pill-badge">CHƯƠNG TRÌNH 1</span>
            <span class="pill-text">18 tháng • Thạc sĩ QTKD Đại học Andrews (Hoa Kỳ)</span>
          </a>

          <a 
            href="#gei" 
            @click.prevent="scrollToProgram('gei')" 
            class="program-pill-row"
            title="Xem chi tiết chương trình Lãnh đạo cấp cao GEI"
          >
            <span class="pill-badge">CHƯƠNG TRÌNH 2</span>
            <span class="pill-text">Lãnh đạo Cấp cao • Study Tour Michigan (Hoa Kỳ)</span>
          </a>
        </div> -->

        <!-- 6. Corporate Footnote -->
        <!-- <div class="hero-footer-note animate-fade-in">
          <span>Hội đồng Tuyển sinh ACC Academy & Đại học Andrews (Hoa Kỳ) | TP. Hồ Chí Minh, Việt Nam</span>
        </div> -->
      </div>
    </section>

    <!-- Admission Programs Section (Dynamic) -->
    <section class="programs-section container">
      <div 
        v-for="(prog, idx) in displayedPrograms" 
        :key="prog.slug || prog.id"
        :id="prog.slug || prog.id"
        class="program-card glass-card animate-slide-up"
      >
        <div class="program-grid" :class="{ reverse: idx % 2 === 1 }">
          <div class="program-media">
            <img :src="prog.image || '/images/andrew.jpg'" :alt="prog.title" class="program-img" loading="lazy" decoding="async" />
            <div v-if="prog.tag" class="program-tag-overlay" :class="idx % 2 === 1 ? 'badge-gold' : ''">
              {{ prog.tag }}
            </div>
          </div>
          <div class="program-content">
            <span v-if="prog.category" class="program-category">{{ prog.category }}</span>
            <h2 class="program-title">{{ prog.title }}</h2>
            <p class="program-desc">{{ prog.subtitle || prog.desc }}</p>

            <div class="program-highlights" v-if="getHighlights(prog).length > 0">
              <div v-for="(h, hIdx) in getHighlights(prog)" :key="hIdx" class="highlight-item">
                <span>{{ h }}</span>
              </div>
            </div>

            <div class="program-footer">
              <router-link :to="`/admissions/detail/${prog.slug || prog.id}`" class="btn btn-primary" style="display: inline-flex; align-items: center; gap: 8px;">
                <span>Xem chi tiết</span>
                <svg class="block-arrow-glow" width="34" height="15" viewBox="0 0 52 24" fill="none">
                  <path d="M 2 7 L 34 7 L 34 2 L 50 12 L 34 22 L 34 17 L 2 17 Z" fill="#ffffff" />
                </svg>
              </router-link>
              <router-link :to="`/contact?program=${prog.slug || prog.id}`" class="btn btn-outline">
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
import { computed, onMounted } from 'vue';
import { useCourseStore } from '@/stores/courses';
import { useI18n } from 'vue-i18n';

const courseStore = useCourseStore();
const { t } = useI18n();

const defaultPrograms = [
  {
    id: 'mba',
    slug: 'mba',
    tag: 'Đại học Andrews Hoa Kỳ',
    category: 'BẰNG QUỐC TẾ HOA KỲ',
    title: 'MBA Andrews Hoa Kỳ: Học quản trị theo chuẩn Mỹ, phát triển sự nghiệp tại Việt Nam',
    subtitle: 'Chương trình Thạc sĩ Quản trị Kinh doanh Đại học Andrews Hoa Kỳ được bảo chứng học thuật toàn cầu, học tại Việt Nam, cấp bằng chính quy từ Hoa Kỳ.',
    image: '/images/andrew.jpg',
    highlights: [
      'Bằng Thạc sĩ do ĐH Andrews (Hoa Kỳ) trực tiếp cấp',
      'Được Bộ Giáo dục & Đào tạo Việt Nam chính thức công nhận',
      'Lịch học cuối tuần linh hoạt, phù hợp người đi làm'
    ]
  },
  {
    id: 'gei',
    slug: 'gei',
    tag: 'AUCORE Andrews University',
    category: 'LÃNH ĐẠO TOÀN CẦU',
    title: 'Global Executive Institute (GEI): Chương trình phát triển năng lực lãnh đạo trong thời đại AI',
    subtitle: 'Chương trình lãnh đạo cấp cao gắn kết AI với chiến lược quản trị, thực thi ESG và tối ưu hóa vận hành tổ chức bền vững.',
    image: '/images/GEL.jpg',
    highlights: [
      'Phát triển năng lực lãnh đạo kết nối AI với chiến lược tổ chức',
      'Không gian trao đổi thực chiến giữa các nhà lãnh đạo đa ngành',
      'Được chứng nhận bởi AUCORE – Đại học Andrews (Hoa Kỳ)'
    ]
  }
];

const displayedPrograms = computed(() => {
  if (courseStore.admissions && courseStore.admissions.length > 0) {
    return [...courseStore.admissions].sort((a, b) => (Number(a.position) || 0) - (Number(b.position) || 0));
  }
  return defaultPrograms;
});

const getHighlights = (prog) => {
  if (Array.isArray(prog.highlights)) return prog.highlights;
  if (typeof prog.highlights === 'string') {
    try {
      const parsed = JSON.parse(prog.highlights);
      if (Array.isArray(parsed)) return parsed;
    } catch {
      return prog.highlights.split('\n').map(s => s.trim()).filter(Boolean);
    }
  }
  return [];
};

const scrollToProgram = (id) => {
  const el = document.getElementById(id);
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
};

onMounted(() => {
  window.scrollTo(0, 0);
  courseStore.fetchAdmissions().catch(() => {});
});
</script>

<style scoped src="@/styles/views/tuyen-sinh/AdmissionsView.css"></style>
