<template>
  <div class="lecturer-detail-page">
    <div class="container" v-if="lecturer">
      <!-- Breadcrumb -->
      <nav class="breadcrumb">
        <router-link to="/">Trang chủ</router-link>
        <span class="sep">/</span>
        <router-link to="/doi-ngu-giang-vien">Đội ngũ giảng viên</router-link>
        <span class="sep">/</span>
        <span class="current">{{ lecturer.name }}</span>
      </nav>

      <!-- Profile Header -->
      <div class="lecturer-profile-card">
        <div class="lecturer-avatar-col">
          <img 
            :src="lecturer.avatar" 
            :alt="lecturer.name" 
            class="lecturer-avatar-img" 
            @error="(e) => e.target.src = '/images/1_6.png'"
            referrerpolicy="no-referrer"
          />
        </div>
        <div class="lecturer-info-col">
          <span class="badge-tag">Giảng viên ACC Academy</span>
          <h1 class="lecturer-name">{{ lecturer.name }}</h1>
          <p class="lecturer-title">{{ lecturer.title }}</p>
          <p class="lecturer-tagline">{{ lecturer.tagline }}</p>
          
          <div class="action-buttons">
            <a v-if="lecturer.driveProfile" :href="lecturer.driveProfile" target="_blank" rel="noopener noreferrer" class="btn-profile-drive">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14 2 14 8 20 8"/>
                <line x1="16" y1="13" x2="8" y2="13"/>
                <line x1="16" y1="17" x2="8" y2="17"/>
                <polyline points="10 9 9 9 8 9"/>
              </svg>
              <span>PROFILE GIẢNG VIÊN (DRIVE)</span>
            </a>
          </div>
        </div>
      </div>

      <!-- Detail Article Section -->
      <article class="lecturer-article-body">
        <h2 class="section-title">Giới thiệu chi tiết</h2>
        <p class="bio-lead">{{ lecturer.bioShort }}</p>
        <div class="content-rich" v-html="lecturer.detailsHtml"></div>

        <!-- Sticky / Bottom Callout Button -->
        <div class="drive-bottom-box" v-if="lecturer.driveProfile">
          <h3>Xem Hồ Sơ Năng Lực Đầy Đủ</h3>
          <p>Tải xuống hoặc xem bản thuyết minh Profile chi tiết của {{ lecturer.name }} trên Google Drive.</p>
          <a :href="lecturer.driveProfile" target="_blank" rel="noopener noreferrer" class="btn-profile-drive-large">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
              <polyline points="15 3 21 3 21 9"></polyline>
              <line x1="10" y1="14" x2="21" y2="3"></line>
            </svg>
            <span>PROFILE GIẢNG VIÊN (GOOGLE DRIVE)</span>
          </a>
        </div>
      </article>

      <!-- Other Lecturers Carousel / Slider Section -->
      <section class="other-lecturers-section" v-if="otherLecturers.length > 0">
        <div class="other-header-row">
          <h2 class="other-title">Giảng viên khác tại ACC Academy</h2>
          <div class="slider-arrows">
            <button 
              class="arrow-btn prev" 
              @click="prevSlide" 
              aria-label="Giảng viên trước"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <polyline points="15 18 9 12 15 6"></polyline>
              </svg>
            </button>
            <button 
              class="arrow-btn next" 
              @click="nextSlide" 
              aria-label="Giảng viên tiếp theo"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <polyline points="9 18 15 12 9 6"></polyline>
              </svg>
            </button>
          </div>
        </div>

        <div class="slider-wrapper">
          <div 
            class="slider-track" 
            :style="{ transform: `translateX(calc(-${currentIndex} * ((100% + 20px) / ${cardsToShow})))` }"
          >
            <div 
              v-for="item in otherLecturers" 
              :key="item.id" 
              class="other-card-item"
              :style="{ flex: `0 0 calc((100% - (20px * (${cardsToShow} - 1))) / ${cardsToShow})` }"
            >
              <router-link :to="'/giang-vien/' + item.id" class="team-card-wrapper group">
                <div class="team-card-image-box">
                  <img 
                    :src="item.avatar" 
                    :alt="item.name" 
                    class="team-card-img"
                    @error="(e) => e.target.src = '/images/1_6.png'"
                    referrerpolicy="no-referrer"
                  />
                  <!-- Dark Gradient Overlay -->
                  <div class="team-card-gradient"></div>
                  
                  <!-- Bottom Info Box -->
                  <div class="team-card-info-box">
                    <h3 class="team-card-name">{{ item.name }}</h3>
                    <div class="team-card-role-row">
                      <span class="accent-line"></span>
                      <span class="team-card-role">{{ item.title }}</span>
                    </div>
                  </div>
                </div>
              </router-link>
            </div>
          </div>
        </div>

        <!-- Slider Dots -->
        <div class="slider-dots" v-if="maxIndex > 0">
          <button 
            v-for="idx in (maxIndex + 1)" 
            :key="idx"
            class="slider-dot"
            :class="{ active: currentIndex === (idx - 1) }"
            @click="currentIndex = (idx - 1)"
            :aria-label="'Chuyển tới slide ' + idx"
          ></button>
        </div>
      </section>
    </div>

    <div v-else class="not-found-box container">
      <h2>Không tìm thấy thông tin giảng viên</h2>
      <router-link to="/doi-ngu-giang-vien" class="btn-back">Quay lại Đội ngũ giảng viên</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { lecturersData } from '@/data/lecturers';

const route = useRoute();
const currentIndex = ref(0);
const windowWidth = ref(typeof window !== 'undefined' ? window.innerWidth : 1200);

const handleResize = () => {
  windowWidth.value = window.innerWidth;
};

const lecturer = computed(() => {
  const id = route.params.id;
  return lecturersData.find(l => l.id === id);
});

const otherLecturers = computed(() => {
  if (!lecturer.value) return lecturersData;
  return lecturersData.filter(l => l.id !== lecturer.value.id);
});

const cardsToShow = computed(() => {
  if (windowWidth.value < 640) return 1;
  if (windowWidth.value < 1024) return 2;
  if (windowWidth.value < 1200) return 3;
  return 4;
});

const maxIndex = computed(() => {
  return Math.max(0, otherLecturers.value.length - cardsToShow.value);
});

const prevSlide = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--;
  } else {
    currentIndex.value = maxIndex.value;
  }
};

const nextSlide = () => {
  if (currentIndex.value < maxIndex.value) {
    currentIndex.value++;
  } else {
    currentIndex.value = 0;
  }
};

onMounted(() => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
  window.addEventListener('resize', handleResize);
});

onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
});

watch(() => route.params.id, () => {
  currentIndex.value = 0;
  window.scrollTo({ top: 0, behavior: 'smooth' });
});
</script>

<style scoped>
.lecturer-detail-page {
  padding-top: 100px;
  padding-bottom: 80px;
  background-color: #f8fafc;
  min-height: 100vh;
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #64748b;
  margin-bottom: 32px;
}
.breadcrumb a {
  color: #022b9f;
  text-decoration: none;
  font-weight: 500;
}
.breadcrumb a:hover {
  text-decoration: underline;
}
.breadcrumb .sep {
  color: #94a3b8;
}

.lecturer-profile-card {
  background: #ffffff;
  border-radius: 20px;
  padding: 40px;
  display: flex;
  flex-direction: column;
  gap: 32px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
  margin-bottom: 40px;
}

@media (min-width: 768px) {
  .lecturer-profile-card {
    flex-direction: row;
    align-items: center;
  }
}

.lecturer-avatar-col {
  flex-shrink: 0;
}

.lecturer-avatar-img {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid #022b9f;
  box-shadow: 0 8px 24px rgba(2, 43, 159, 0.2);
}

.lecturer-info-col {
  flex-grow: 1;
}

.badge-tag {
  display: inline-block;
  padding: 4px 12px;
  background: rgba(2, 43, 159, 0.08);
  color: #022b9f;
  font-size: 13px;
  font-weight: 700;
  border-radius: 20px;
  margin-bottom: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.lecturer-name {
  font-size: 32px;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 8px;
}

.lecturer-title {
  font-size: 18px;
  font-weight: 600;
  color: #022b9f;
  margin-bottom: 16px;
}

.lecturer-tagline {
  font-size: 15px;
  line-height: 1.6;
  color: #475569;
  margin-bottom: 24px;
}

.btn-profile-drive {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 14px 28px;
  background: linear-gradient(135deg, #022b9f 0%, #1e40af 100%);
  color: #ffffff;
  font-weight: 700;
  font-size: 14px;
  border-radius: 12px;
  text-decoration: none;
  box-shadow: 0 4px 16px rgba(2, 43, 159, 0.3);
  transition: all 0.3s ease;
}

.btn-profile-drive:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(2, 43, 159, 0.4);
  color: #ffffff;
}

.lecturer-article-body {
  background: #ffffff;
  border-radius: 20px;
  padding: 40px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04);
  margin-bottom: 60px;
}

.section-title {
  font-size: 24px;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 2px solid #e2e8f0;
}

.bio-lead {
  font-size: 17px;
  line-height: 1.7;
  color: #334155;
  font-weight: 500;
  margin-bottom: 24px;
}

.content-rich {
  font-size: 16px;
  line-height: 1.8;
  color: #475569;
}

.content-rich h4 {
  font-size: 18px;
  font-weight: 700;
  color: #0f172a;
  margin-top: 24px;
  margin-bottom: 12px;
}

.content-rich ul {
  padding-left: 24px;
  margin-bottom: 24px;
}

.content-rich li {
  margin-bottom: 8px;
}

.drive-bottom-box {
  margin-top: 40px;
  padding: 32px;
  background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
  border-radius: 16px;
  text-align: center;
  border: 1px solid #cbd5e1;
}

.drive-bottom-box h3 {
  font-size: 20px;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 8px;
}

.drive-bottom-box p {
  font-size: 15px;
  color: #475569;
  margin-bottom: 20px;
}

.btn-profile-drive-large {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  padding: 16px 36px;
  background: #022b9f;
  color: #ffffff;
  font-weight: 800;
  font-size: 15px;
  border-radius: 12px;
  text-decoration: none;
  box-shadow: 0 4px 16px rgba(2, 43, 159, 0.3);
  transition: all 0.3s ease;
}

.btn-profile-drive-large:hover {
  background: #1e40af;
  transform: scale(1.02);
}

/* Other Lecturers Slider Styles */
.other-lecturers-section {
  margin-top: 50px;
}

.other-header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}

.other-title {
  font-size: 24px;
  font-weight: 800;
  color: #0f172a;
  margin: 0;
}

.slider-arrows {
  display: flex;
  align-items: center;
  gap: 10px;
}

.arrow-btn {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  color: #0f172a;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  transition: all 0.25s ease;
}

.arrow-btn:hover {
  background: #022b9f;
  color: #ffffff;
  border-color: #022b9f;
  box-shadow: 0 6px 16px rgba(2, 43, 159, 0.25);
  transform: translateY(-2px);
}

.slider-wrapper {
  overflow: hidden;
  width: 100%;
  padding-block: 8px;
}

.slider-track {
  display: flex;
  gap: 20px;
  transition: transform 0.45s cubic-bezier(0.25, 1, 0.5, 1);
  will-change: transform;
}

.other-card-item {
  box-sizing: border-box;
}

.team-card-wrapper {
  display: block;
  text-decoration: none;
  width: 100%;
  height: 100%;
}

.team-card-image-box {
  position: relative;
  width: 100%;
  aspect-ratio: 3 / 4;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  background-color: #0f172a;
}

@media (min-width: 768px) {
  .team-card-image-box {
    aspect-ratio: 4 / 5;
  }
}

.team-card-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.7s cubic-bezier(0.16, 1, 0.3, 1);
}

.team-card-wrapper:hover .team-card-img {
  transform: scale(1.08);
}

.team-card-gradient {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.9) 0%, rgba(0, 0, 0, 0.35) 45%, transparent 100%);
  opacity: 0.85;
  transition: opacity 0.3s ease;
}

.team-card-wrapper:hover .team-card-gradient {
  opacity: 1;
}

.team-card-info-box {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  padding: 24px 20px;
  transform: translateY(6px);
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  box-sizing: border-box;
  text-align: left;
}

.team-card-wrapper:hover .team-card-info-box {
  transform: translateY(0);
}

.team-card-name {
  font-size: 20px;
  font-weight: 900;
  color: #ffffff;
  margin: 0 0 6px 0;
  line-height: 1.25;
  letter-spacing: -0.3px;
  text-transform: uppercase;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
}

.team-card-role-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.accent-line {
  height: 2px;
  width: 28px;
  background: #2563eb;
  display: inline-block;
  border-radius: 2px;
  flex-shrink: 0;
}

.team-card-role {
  font-size: 12px;
  font-weight: 700;
  color: #cbd5e1;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.slider-dots {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 24px;
}

.slider-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #cbd5e1;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
}

.slider-dot.active {
  background: #022b9f;
  width: 24px;
  border-radius: 12px;
}

.not-found-box {
  padding-top: 80px;
  text-align: center;
}

.btn-back {
  display: inline-block;
  margin-top: 16px;
  padding: 10px 20px;
  background: #022b9f;
  color: #ffffff;
  border-radius: 10px;
  text-decoration: none;
  font-weight: 700;
}
</style>
