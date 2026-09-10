<template>
  <div class="lecturers-page">
    <div class="container">
      <!-- Header Banner Section -->
      <div class="lecturers-hero">
        <span class="custom-ui-tag hero-tag">ĐỘI NGŨ GIẢNG VIÊN</span>
        <h1 class="hero-title">Đội ngũ Giảng viên & Chuyên gia Thực chiến</h1>
        <p class="hero-subtitle">
          Học viện ACC tự hào sở hữu đội ngũ giảng viên, chuyên gia hàng đầu sở hữu bề dày kinh nghiệm tư vấn và đào tạo thực chiến tại các tập đoàn lớn, sẵn sàng đồng hành nâng tầm năng lực tổ chức và cá nhân trong kỷ nguyên AI & Số.
        </p>
      </div>

      <!-- Lecturers Grid -->
      <div class="lecturers-grid">
        <div 
          v-for="l in lecturersData" 
          :key="l.id"
          class="lecturer-card"
        >
          <div class="lecturer-card-inner">
            <div class="lecturer-avatar-wrapper">
              <img 
                :src="l.avatar" 
                :alt="l.name" 
                class="lecturer-card-avatar" 
                @error="(e) => e.target.src = '/images/1_6.png'"
                referrerpolicy="no-referrer"
              />
              <span v-if="l.id === 'nguyen-vu-huy-hoang'" class="featured-badge">Master AI Trainer</span>
            </div>
            <div class="lecturer-card-info">
              <h3 class="lecturer-card-name">{{ l.name }}</h3>
              <p class="lecturer-card-title">{{ l.title }}</p>
              <p class="lecturer-card-bio">{{ l.bioShort }}</p>
              
              <div class="lecturer-card-actions">
                <router-link :to="'/giang-vien/' + l.id" class="btn-read-bio">
                  <span>Xem chi tiết giới thiệu</span>
                  <span class="arrow">&rarr;</span>
                </router-link>
                <a v-if="l.driveProfile" :href="l.driveProfile" target="_blank" rel="noopener noreferrer" class="btn-drive-link">
                  <span>PROFILE GIẢNG VIÊN (DRIVE)</span>
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                    <polyline points="15 3 21 3 21 9"></polyline>
                    <line x1="10" y1="14" x2="21" y2="3"></line>
                  </svg>
                </a>
                <span v-else class="btn-drive-link disabled">
                  <span>PROFILE GIẢNG VIÊN (Cập nhật sau)</span>
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { lecturersData } from '@/data/lecturers';

onMounted(() => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});
</script>

<style scoped>
.lecturers-page {
  padding-top: 120px;
  padding-bottom: 100px;
  background-color: #f8fafc;
  min-height: 100vh;
}

.lecturers-hero {
  text-align: center;
  max-width: 860px;
  margin-inline: auto;
  margin-bottom: 60px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.hero-tag {
  background: rgba(2, 43, 159, 0.08);
  color: #022b9f;
  font-weight: 800;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 13px;
}

.hero-title {
  font-size: clamp(32px, 4vw, 48px);
  font-weight: 800;
  color: #0f172a;
  margin: 0;
  line-height: 1.2;
}

.hero-subtitle {
  font-size: 16px;
  color: #475569;
  line-height: 1.6;
  margin: 0;
}

.lecturers-grid {
  display: grid;
  grid-template-columns: repeat(1, 1fr);
  gap: 32px;
}

@media (min-width: 768px) {
  .lecturers-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1200px) {
  .lecturers-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.lecturer-card {
  background: #ffffff;
  border-radius: 20px;
  border: 1px solid #e2e8f0;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
}

.lecturer-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
  border-color: #022b9f;
}

.lecturer-card-inner {
  padding: 28px;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.lecturer-avatar-wrapper {
  position: relative;
  width: 120px;
  height: 120px;
  margin-bottom: 20px;
}

.lecturer-card-avatar {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #022b9f;
  box-shadow: 0 6px 16px rgba(2, 43, 159, 0.15);
}

.featured-badge {
  position: absolute;
  bottom: -6px;
  left: 50%;
  transform: translateX(-50%);
  background: #022b9f;
  color: #ffffff;
  font-size: 11px;
  font-weight: 800;
  padding: 3px 10px;
  border-radius: 12px;
  white-space: nowrap;
  letter-spacing: 0.5px;
}

.lecturer-card-info {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.lecturer-card-name {
  font-size: 22px;
  font-weight: 800;
  color: #0f172a;
  margin: 0 0 6px 0;
}

.lecturer-card-title {
  font-size: 14px;
  font-weight: 700;
  color: #022b9f;
  margin: 0 0 14px 0;
  line-height: 1.4;
}

.lecturer-card-bio {
  font-size: 14px;
  line-height: 1.6;
  color: #475569;
  margin: 0 0 24px 0;
  display: -webkit-box;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.lecturer-card-actions {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.btn-read-bio {
  display: inline-flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 20px;
  background: #022b9f;
  color: #ffffff;
  font-weight: 700;
  font-size: 13.5px;
  border-radius: 10px;
  text-decoration: none;
  transition: all 0.2s ease;
}

.btn-read-bio:hover {
  background: #1e40af;
  color: #ffffff;
}

.btn-drive-link {
  display: inline-flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 20px;
  background: transparent;
  border: 1px solid #cbd5e1;
  color: #334155;
  font-weight: 700;
  font-size: 12.5px;
  border-radius: 10px;
  text-decoration: none;
  transition: all 0.2s ease;
}

.btn-drive-link:hover {
  background: #f1f5f9;
  border-color: #94a3b8;
  color: #022b9f;
}
</style>
