<template>
  <div class="lecturer-detail-page">
    <div class="container" v-if="lecturer">
      <!-- Breadcrumb -->
      <nav class="breadcrumb">
        <router-link to="/">Trang chủ</router-link>
        <span class="sep">/</span>
        <router-link to="/about-us">Đội ngũ giảng viên</router-link>
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
            <a :href="lecturer.driveProfile" target="_blank" rel="noopener noreferrer" class="btn-profile-drive">
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

      <!-- Other Lecturers Carousel / Grid -->
      <section class="other-lecturers-section">
        <h2 class="other-title">Giảng viên khác tại ACC Academy</h2>
        <div class="other-grid">
          <div 
            v-for="item in otherLecturers" 
            :key="item.id" 
            class="other-card"
          >
            <router-link :to="'/giang-vien/' + item.id" class="other-card-link">
              <div class="other-avatar-box">
                <img :src="item.avatar" :alt="item.name" />
              </div>
              <div class="other-info">
                <h4 class="other-name">{{ item.name }}</h4>
                <p class="other-title-text">{{ item.title }}</p>
              </div>
            </router-link>
          </div>
        </div>
      </section>
    </div>

    <div v-else class="not-found-box container">
      <h2>Không tìm thấy thông tin giảng viên</h2>
      <router-link to="/about-us" class="btn-back">Quay lại Đội ngũ giảng viên</router-link>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { lecturersData } from '@/data/lecturers';

const route = useRoute();

const lecturer = computed(() => {
  const id = route.params.id;
  return lecturersData.find(l => l.id === id);
});

const otherLecturers = computed(() => {
  if (!lecturer.value) return lecturersData;
  return lecturersData.filter(l => l.id !== lecturer.value.id).slice(0, 4);
});

onMounted(() => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});

watch(() => route.params.id, () => {
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

.other-lecturers-section {
  margin-top: 40px;
}

.other-title {
  font-size: 22px;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 24px;
}

.other-grid {
  display: grid;
  grid-template-columns: repeat(1, 1fr);
  gap: 20px;
}

@media (min-width: 640px) {
  .other-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .other-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

.other-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 20px;
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
}

.other-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
  border-color: #022b9f;
}

.other-card-link {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  text-decoration: none;
}

.other-avatar-box img {
  width: 90px;
  height: 90px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 12px;
  border: 2px solid #022b9f;
}

.other-name {
  font-size: 16px;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 4px;
}

.other-title-text {
  font-size: 13px;
  color: #64748b;
  line-height: 1.4;
}
</style>
