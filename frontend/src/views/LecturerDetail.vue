<template>
  <div class="lecturer-detail-page">
    <div class="container" v-if="lecturer">
      <!-- Breadcrumb -->
      <nav class="breadcrumb">
        <router-link to="/">Trang chủ</router-link>
        <span class="sep">/</span>
        <router-link to="/lecturers">Đội ngũ giảng viên</router-link>
        <span class="sep">/</span>
        <span class="current">{{ lecturer.name }}</span>
      </nav>

      <!-- Profile Header -->
      <div class="lecturer-profile-card">
        <div class="lecturer-avatar-col">
          <img 
            :src="formatImageUrl(lecturer.avatar)" 
            :alt="lecturer.name" 
            class="lecturer-avatar-img" 
            @error="(e) => e.target.src = '/images/1_6.png'"
            referrerpolicy="no-referrer"
          />
        </div>
        <div class="lecturer-info-col">
          <!-- <span class="badge-tag">Giảng viên ACC Academy</span> -->
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
        <div v-if="lecturer.bioShort" class="bio-lead">{{ lecturer.bioShort }}</div>
        <div 
          v-if="lecturer.detailsHtml" 
          class="content-rich" 
          v-html="sanitizeHtml(formatLecturerDetails(lecturer.detailsHtml))"
        ></div>
        <div v-else-if="!lecturer.bioShort" class="content-rich" style="color: #94a3b8; font-style: italic;">
          Nội dung giới thiệu chi tiết của giảng viên đang được cập nhật...
        </div>

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
                    :src="formatImageUrl(item.avatar)" 
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
      <router-link to="/lecturers" class="btn-back">Quay lại Đội ngũ giảng viên</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useCourseStore } from '@/stores/courses';
import { formatImageUrl } from '@/utils/imageHelper';
import { sanitizeHtml } from '@/utils/sanitize';

const route = useRoute();
const courseStore = useCourseStore();
const currentIndex = ref(0);
const windowWidth = ref(typeof window !== 'undefined' ? window.innerWidth : 1200);

const handleResize = () => {
  windowWidth.value = window.innerWidth;
};

const allLecturers = computed(() => {
  return courseStore.lecturers || [];
});

const lecturer = computed(() => {
  const id = route.params.id;
  return allLecturers.value.find(l => l.id === id);
});

const otherLecturers = computed(() => {
  if (!lecturer.value) return allLecturers.value;
  return allLecturers.value.filter(l => l.id !== lecturer.value.id);
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

const formatLecturerDetails = (content) => {
  if (!content) return '';
  // Nếu đã chứa thẻ HTML (p, div, br, h1-h6, img, ul, ol...), giữ nguyên
  if (/<(?:p|div|br|h[1-6]|img|ul|ol|li|table|blockquote|span|b|strong|i|em)[>\s]/i.test(content)) {
    return content;
  }
  // Nếu là văn bản thuần có xuống dòng: tự động chuyển \n thành <br>
  return content.replace(/\r\n/g, '<br>').replace(/\n/g, '<br>');
};

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

const loadLecturerDetail = async () => {
  const id = route.params.id;
  if (!id) return;
  try {
    const data = await courseStore.apiRequest(`/lecturers/${id}`);
    if (data) {
      const idx = courseStore.lecturers.findIndex(l => l.id === id);
      const mapped = {
        ...data,
        bioShort: data.bio_short || '',
        detailsHtml: data.details_html || '',
        majorName: data.major_name || 'AI & Công nghệ Số'
      };
      if (idx !== -1) {
        courseStore.lecturers[idx] = { ...courseStore.lecturers[idx], ...mapped };
      } else {
        courseStore.lecturers.push(mapped);
      }
    }
  } catch (err) {
    console.warn("Could not fetch lecturer detail from API:", err);
  }
};

onMounted(() => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
  window.addEventListener('resize', handleResize);
  courseStore.fetchLecturers();
  loadLecturerDetail();
});

onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
});

watch(() => route.params.id, () => {
  currentIndex.value = 0;
  window.scrollTo({ top: 0, behavior: 'smooth' });
  loadLecturerDetail();
});
</script>

<style scoped src="@/styles/views/LecturerDetail.css"></style>
