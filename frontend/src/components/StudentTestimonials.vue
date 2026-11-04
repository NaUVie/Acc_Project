<template>
  <section class="testimonials-section">
    <div class="container">
      <!-- Section Header -->
      <div class="section-header">
        <h2 class="section-title">{{ $t('testimonials.pageTitle') }}</h2>
      </div>

      <!-- Filter Tabs -->
      <div class="filter-tabs">
        <button 
          class="tab-btn"
          :class="{ active: activeTab === 'all' }"
          @click="setTab('all')"
        >
          {{ $t('testimonials.tabAll') }} ({{ videoTestimonialsData.length + photoTestimonialsData.length }})
        </button>
        <button 
          class="tab-btn"
          :class="{ active: activeTab === 'video' }"
          @click="setTab('video')"
        >
          {{ $t('testimonials.tabVideo') }} ({{ videoTestimonialsData.length }})
        </button>
        <button 
          class="tab-btn"
          :class="{ active: activeTab === 'photo' }"
          @click="setTab('photo')"
        >
          {{ $t('testimonials.tabPhoto') }} ({{ photoTestimonialsData.length }})
        </button>
      </div>

      <!-- Video Feedbacks Grid -->
      <div v-if="activeTab === 'all' || activeTab === 'video'" class="feedback-sub-section">
        <h3 class="sub-section-title">{{ $t('testimonials.videoHeading') }} </h3>
        
        <template v-if="videoTestimonialsData.length > 0">
          <div class="video-grid">
            <div 
              v-for="(v, idx) in paginatedVideoData" 
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
                <span class="program-tag-badge" v-if="v.courseName">📚 Khóa học: {{ v.courseName }}</span>
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

          <!-- Video Pagination Component -->
          <Pagination 
            v-if="videoTestimonialsData.length > videoPageSize"
            v-model:currentPage="videoPage"
            :totalItems="videoTestimonialsData.length"
            :pageSize="videoPageSize"
            @page-change="onVideoPageChange"
          />
        </template>

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
            <span style="display: inline-flex; align-items: center; gap: 6px;">
              <span>XEM THÊM TRÊN YOUTUBE</span>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="5" y1="12" x2="19" y2="12"></line>
                <polyline points="12 5 19 12 12 19"></polyline>
              </svg>
            </span>
          </a>
        </div>
      </div>

      <!-- Photo & Text Feedbacks Grid -->
      <div v-if="activeTab === 'all' || activeTab === 'photo'" class="feedback-sub-section style-mt">
        <h3 class="sub-section-title"> {{ $t('testimonials.tabPhoto') }} Học viên</h3>
        
        <template v-if="photoTestimonialsData.length > 0">
          <div class="photo-grid">
            <div 
              v-for="p in paginatedPhotoData" 
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
                <span class="course-badge" v-if="p.courseName">📚 Khóa học: {{ p.courseName }}</span><span class="course-badge" v-else>📚 Học viên ACC Academy</span>
              </div>
            </div>
          </div>

          <!-- Photo Pagination Component -->
          <Pagination 
            v-if="photoTestimonialsData.length > photoPageSize"
            v-model:currentPage="photoPage"
            :totalItems="photoTestimonialsData.length"
            :pageSize="photoPageSize"
            @page-change="onPhotoPageChange"
          />
        </template>

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
import { useTestimonialStore } from '@/stores/testimonials';
import { formatImageUrl } from '@/utils/imageHelper';
import Pagination from '@/components/Pagination.vue';

const youtubePlaylistUrl = 'https://www.youtube.com/playlist?list=PLB-PopIBDBXk';
const testimonialStore = useTestimonialStore();

const activeTab = ref('all');
const activeVideoUrl = ref('');

const videoPage = ref(1);
const videoPageSize = ref(6);

const photoPage = ref(1);
const photoPageSize = ref(6);

const videoTestimonialsData = computed(() => testimonialStore.videoTestimonials);
const photoTestimonialsData = computed(() => testimonialStore.photoTestimonials);

const paginatedVideoData = computed(() => {
  const start = (videoPage.value - 1) * videoPageSize.value;
  return videoTestimonialsData.value.slice(start, start + videoPageSize.value);
});

const paginatedPhotoData = computed(() => {
  const start = (photoPage.value - 1) * photoPageSize.value;
  return photoTestimonialsData.value.slice(start, start + photoPageSize.value);
});

const setTab = (tab) => {
  activeTab.value = tab;
  videoPage.value = 1;
  photoPage.value = 1;
};

const onVideoPageChange = () => {
  window.scrollTo({ top: 220, behavior: 'smooth' });
};

const onPhotoPageChange = () => {
  window.scrollTo({ top: 450, behavior: 'smooth' });
};

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

<style scoped src="@/styles/components/StudentTestimonials.css"></style>
