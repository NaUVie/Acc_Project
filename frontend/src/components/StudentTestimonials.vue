<template>
  <section class="testimonials-section">
    <div class="container">
      <!-- Section Header -->
      <div class="section-header">
        <h2 class="section-title">
          Góc nhìn & Phản hồi Thực tế từ Học viên ACC Academy
        </h2>
      </div>

      <!-- Filter Tabs -->
      <div class="filter-tabs">
        <button 
          class="tab-btn"
          :class="{ active: activeTab === 'all' }"
          @click="activeTab = 'all'"
        >
          Tất cả phản hồi ({{ videoTestimonialsData.length + photoTestimonialsData.length }})
        </button>
        <button 
          class="tab-btn"
          :class="{ active: activeTab === 'video' }"
          @click="activeTab = 'video'"
        >
          Video Feedback YouTube ({{ videoTestimonialsData.length }})
        </button>
        <button 
          class="tab-btn"
          :class="{ active: activeTab === 'photo' }"
          @click="activeTab = 'photo'"
        >
          Hình ảnh & Cảm nhận ({{ photoTestimonialsData.length }})
        </button>
      </div>

      <!-- Video Feedbacks Grid -->
      <div v-if="activeTab === 'all' || activeTab === 'video'" class="feedback-sub-section">
        <h3 class="sub-section-title">Video Feedback từ Học viên </h3>
        
        <div v-if="videoTestimonialsData.length > 0" class="video-grid">
          <div 
            v-for="(v, idx) in videoTestimonialsData" 
            :key="v.id" 
            class="video-card"
            @click="openVideo(v.videoUrl)"
          >
            <div class="video-thumb-wrapper">
              <img :src="formatImageUrl(v.thumbnail)" :alt="v.title" class="video-thumb-img" referrerpolicy="no-referrer" />
              <div class="play-overlay">
                <div class="play-btn-circle">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                    <polygon points="5 3 19 12 5 21 5 3"></polygon>
                  </svg>
                </div>
              </div>
            </div>
            <div class="video-card-body">
              <span class="program-tag-badge" v-if="v.courseName"> {{ v.courseName }}</span>
              <h4 class="video-card-title">{{ v.title }}</h4>
              <div class="student-profile-info">
                <span class="s-name"> {{ v.studentName || v.name }}</span>
                <span class="s-role" v-if="v.role || v.company">{{ v.role }} <span v-if="v.company">• {{ v.company }}</span></span>
              </div>
              <span class="yt-link-small">
                Bấm để xem video ngay ;
              </span>
            </div>
          </div>
        </div>

        <div v-else class="empty-feedback-box">
          <p class="empty-feedback-text">Hiện chưa có video cảm nhận nào từ học viên.</p>
        </div>

        <!-- YouTube Playlist Banner Button -->
        <div class="youtube-playlist-banner">
          <div class="yt-banner-info">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="#FF0000">
              <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
            </svg>
            <div>
              <h4 class="yt-title">FEEDBACK TỪ HỌC VIÊN TRÊN YOUTUBE</h4>
            </div>
          </div>
          <a :href="youtubePlaylistUrl" target="_blank" rel="noopener noreferrer" class="btn-yt-playlist">
            <span>XEM THÊM TRÊN YOUTUBE&rarr;</span>
          </a>
        </div>
      </div>

      <!-- Photo & Text Feedbacks Grid -->
      <div v-if="activeTab === 'all' || activeTab === 'photo'" class="feedback-sub-section style-mt">
        <h3 class="sub-section-title"> Hình ảnh & Cảm nhận Học viên</h3>
        
        <div v-if="photoTestimonialsData.length > 0" class="photo-grid">
          <div 
            v-for="p in photoTestimonialsData" 
            :key="p.id" 
            class="photo-card"
          >
            <div class="photo-card-img-wrapper" v-if="p.image">
              <img :src="formatImageUrl(p.image)" :alt="p.name" class="photo-card-img" referrerpolicy="no-referrer" />
            </div>

            <div class="photo-card-content">
              <div class="student-profile">
                <img :src="formatImageUrl(p.avatar)" :alt="p.name" class="profile-avatar" referrerpolicy="no-referrer" />
                <div>
                  <h4 class="profile-name">{{ p.name }}</h4>
                  <p class="profile-title">{{ p.role }} • {{ p.company }}</p>
                </div>
              </div>

              <div class="stars">★★★★★</div>
              <p class="quote-text">"{{ p.quote }}"</p>
              <span class="course-badge">{{ p.courseName }}</span>
            </div>
          </div>
        </div>

        <div v-else class="empty-feedback-box">
          <p class="empty-feedback-text">Hiện chưa có hình ảnh & cảm nhận nào từ học viên.</p>
        </div>
      </div>
    </div>

    <!-- Video Modal Player -->
    <Teleport to="body">
      <div v-if="activeVideoUrl" class="video-modal-backdrop" @click="closeVideo">
        <div class="video-modal-container" @click.stop>
          <button class="video-close-btn" @click="closeVideo" aria-label="Đóng video">&times;</button>
          <div class="iframe-wrapper">
            <iframe 
              :src="activeVideoUrl" 
              title="YouTube Feedback Video ACC Academy"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
              allowfullscreen
            ></iframe>
          </div>
        </div>
      </div>
    </Teleport>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { youtubePlaylistUrl } from '@/data/testimonials';
import { useTestimonialStore } from '@/stores/testimonials';
import { formatImageUrl } from '@/utils/imageHelper';

const testimonialStore = useTestimonialStore();

const activeTab = ref('all');
const activeVideoUrl = ref('');

const videoTestimonialsData = computed(() => testimonialStore.videoTestimonials);
const photoTestimonialsData = computed(() => testimonialStore.photoTestimonials);

onMounted(() => {
  testimonialStore.fetchTestimonials();
});

const openVideo = (url) => {
  if (!url) return;
  activeVideoUrl.value = url;
};

const closeVideo = () => {
  activeVideoUrl.value = '';
};
</script>

<style scoped>
.testimonials-section {
  padding-top: 120px;
  padding-bottom: 100px;
  background-color: #f8fafc;
  min-height: 100vh;
}

.section-header {
  text-align: center;
  max-width: 860px;
  margin-inline: auto;
  margin-bottom: 48px;
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

.section-title {
  font-size: clamp(30px, 4vw, 44px);
  font-weight: 800;
  color: #0f172a;
  margin: 0;
  line-height: 1.25;
}

.highlight-text {
  color: #022b9f;
}

.section-desc {
  font-size: 16px;
  color: #475569;
  line-height: 1.6;
  margin: 0;
}

.youtube-playlist-banner {
  width: 100%;
  margin-top: 32px;
  padding: 20px 28px;
  background: linear-gradient(135deg, #fff1f2 0%, #ffe4e6 100%);
  border: 1.5px solid #fecdd3;
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  flex-wrap: wrap;
  text-align: left;
}

.yt-banner-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.yt-title {
  font-size: 16px;
  font-weight: 800;
  color: #9f1239;
  margin: 0 0 4px 0;
}

.yt-subtitle {
  font-size: 13.5px;
  color: #be123c;
  margin: 0;
}

.btn-yt-playlist {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: #e11d48;
  color: #ffffff;
  font-weight: 800;
  font-size: 13px;
  border-radius: 10px;
  text-decoration: none;
  transition: background 0.2s ease;
}

.btn-yt-playlist:hover {
  background: #be123c;
}

.filter-tabs {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-bottom: 48px;
  flex-wrap: wrap;
}

.tab-btn {
  padding: 10px 24px;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 24px;
  color: #475569;
  font-weight: 700;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.25s ease;
}

.tab-btn:hover {
  border-color: #022b9f;
  color: #022b9f;
  background: #f0f4ff;
}

.tab-btn.active {
  background: #022b9f;
  color: #ffffff;
  border-color: #022b9f;
  box-shadow: 0 4px 14px rgba(2, 43, 159, 0.25);
}

.feedback-sub-section {
  margin-bottom: 56px;
}

.feedback-sub-section.style-mt {
  margin-top: 48px;
}

.sub-section-title {
  font-size: 22px;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 24px;
}

.video-grid {
  display: grid;
  grid-template-columns: repeat(1, 1fr);
  gap: 28px;
}

@media (min-width: 768px) {
  .video-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1200px) {
  .video-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.video-card {
  background: #ffffff;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.04);
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
}

.video-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 36px rgba(0, 0, 0, 0.1);
  border-color: #022b9f;
}

.video-thumb-wrapper {
  position: relative;
  width: 100%;
  height: 200px;
  background-color: #0f172a;
  overflow: hidden;
}

.video-thumb-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0.9;
  transition: transform 0.4s ease;
}

.video-card:hover .video-thumb-img {
  transform: scale(1.06);
  opacity: 1;
}

.play-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(15, 23, 42, 0.25);
  transition: background 0.25s ease;
}

.video-card:hover .play-overlay {
  background: rgba(15, 23, 42, 0.1);
}

.play-btn-circle {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: #e11d48;
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 6px 20px rgba(225, 29, 72, 0.45);
  transition: transform 0.25s ease;
}

.video-card:hover .play-btn-circle {
  transform: scale(1.15);
  background: #be123c;
}

.video-badge {
  position: absolute;
  top: 12px;
  left: 12px;
  background: #022b9f;
  color: #ffffff;
  font-size: 11px;
  font-weight: 800;
  padding: 4px 10px;
  border-radius: 8px;
  letter-spacing: 0.5px;
}

.video-card-body {
  padding: 20px;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.program-tag-badge {
  display: inline-block;
  font-size: 11.5px;
  font-weight: 700;
  color: #022b9f;
  background: rgba(2, 43, 159, 0.08);
  padding: 4px 10px;
  border-radius: 8px;
  margin-bottom: 8px;
  width: fit-content;
}

.video-card-title {
  font-size: 16px;
  font-weight: 800;
  color: #0f172a;
  margin: 0 0 12px 0;
  line-height: 1.4;
}

.student-profile-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 13px;
  margin-bottom: 14px;
  background: #f8fafc;
  padding: 10px 12px;
  border-radius: 10px;
}

.s-name {
  font-weight: 700;
  color: #0f172a;
}

.s-role {
  font-size: 12.5px;
  color: #64748b;
  font-weight: 600;
}

.yt-link-small {
  font-size: 12.5px;
  font-weight: 700;
  color: #e11d48;
  margin-top: auto;
}

.photo-grid {
  display: grid;
  grid-template-columns: repeat(1, 1fr);
  gap: 28px;
}

@media (min-width: 768px) {
  .photo-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1200px) {
  .photo-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.photo-card {
  background: #ffffff;
  border-radius: 18px;
  border: 1px solid #e2e8f0;
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.04);
  display: flex;
  flex-direction: column;
}

.photo-card-img-wrapper {
  width: 100%;
  height: 220px;
  overflow: hidden;
  background-color: #f1f5f9;
}

.photo-card-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.photo-card-content {
  padding: 24px;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.student-profile {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 14px;
}

.profile-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #022b9f;
}

.profile-name {
  font-size: 16px;
  font-weight: 800;
  color: #0f172a;
  margin: 0;
}

.profile-title {
  font-size: 12.5px;
  color: #64748b;
  margin: 2px 0 0 0;
}

.stars {
  color: #f59e0b;
  font-size: 14px;
  margin-bottom: 10px;
}

.quote-text {
  font-size: 14px;
  line-height: 1.6;
  color: #334155;
  font-style: italic;
  margin: 0 0 20px 0;
  flex-grow: 1;
}

.course-badge {
  display: inline-block;
  font-size: 11.5px;
  font-weight: 700;
  color: #022b9f;
  background: rgba(2, 43, 159, 0.08);
  padding: 4px 12px;
  border-radius: 12px;
  width: max-content;
}

/* Video Modal */
.video-modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.85);
  backdrop-filter: blur(8px);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.video-modal-container {
  position: relative;
  width: 100%;
  max-width: 900px;
  background: #000000;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
}

.video-close-btn {
  position: absolute;
  top: 12px;
  right: 16px;
  background: rgba(255, 255, 255, 0.25);
  color: #ffffff;
  border: none;
  font-size: 28px;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s ease;
}

.video-close-btn:hover {
  background: #e11d48;
}

.iframe-wrapper {
  position: relative;
  padding-bottom: 56.25%; /* 16:9 Aspect Ratio */
  height: 0;
}

.iframe-wrapper iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border: 0;
}

.empty-feedback-box {
  background: #ffffff;
  border: 1px dashed #cbd5e1;
  border-radius: 16px;
  padding: 48px 24px;
  text-align: center;
  margin-bottom: 24px;
}

.empty-feedback-text {
  color: #64748b;
  font-size: 15px;
  margin: 0;
  font-weight: 500;
}
</style>
