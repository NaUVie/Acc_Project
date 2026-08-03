<template>
  <section class="testimonials-section">
    <div class="testimonials-container">
      <div class="section-header">
        <span class="section-tag">Góc nhìn Học viên</span>
        <h2 class="section-title">
          Hơn <span class="highlight-text">10,000+ Doanh Nhân & Chuyên Gia</span> Đã Đồng Hành
        </h2>
        <p class="section-desc">
          Lắng nghe những trải nghiệm thực tế và thành quả đột phá từ các Founder, CEO, Idol giới doanh nhân sau khi ứng dụng tri thức từ ACC Academy.
        </p>
      </div>

      <!-- Filter Tabs -->
      <div class="filter-tabs">
        <button 
          v-for="tab in tabs" 
          :key="tab.id"
          class="tab-btn"
          :class="{ active: activeTab === tab.id }"
          @click="activeTab = tab.id"
        >
          {{ tab.name }}
        </button>
      </div>

      <!-- Grid Cards -->
      <div class="testimonials-grid">
        <!-- Text & Photo Card -->
        <div 
          v-for="item in filteredTestimonials" 
          :key="item.id" 
          class="testimonial-card"
          :class="{ 'video-card': item.type === 'video' }"
          @click="item.type === 'video' ? openVideo(item.videoUrl) : null"
        >
          <!-- If Video Type -->
          <template v-if="item.type === 'video'">
            <div class="video-thumb-container">
              <img :src="item.videoThumb" :alt="item.name" class="video-thumb-img" />
              <div class="play-button">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                  <polygon points="5 3 19 12 5 21 5 3"></polygon>
                </svg>
              </div>
              <span class="video-duration">{{ item.videoDuration }}</span>
            </div>
            <div class="video-info-body">
              <h3 class="video-title">{{ item.videoTitle }}</h3>
              <div class="card-top">
                <div class="avatar-wrapper">
                  <img :src="item.avatar" :alt="item.name" class="avatar-img" />
                  <span class="verified-icon">✓</span>
                </div>
                <div class="author-meta">
                  <h4 class="author-name">{{ item.name }}</h4>
                  <p class="author-title">{{ item.role }}</p>
                  <p class="author-company">{{ item.company }}</p>
                </div>
              </div>
            </div>
          </template>

          <!-- If Photo + Text Type -->
          <template v-else>
            <div>
              <div class="card-top">
                <div class="avatar-wrapper">
                  <img :src="item.avatar" :alt="item.name" class="avatar-img" />
                  <span class="verified-icon">✓</span>
                </div>
                <div class="author-meta">
                  <h4 class="author-name">{{ item.name }}</h4>
                  <p class="author-title">{{ item.role }}</p>
                  <p class="author-company">{{ item.company }}</p>
                </div>
              </div>

              <div class="rating-stars">
                <span v-for="star in 5" :key="star">★</span>
              </div>

              <p class="quote-content">
                "{{ item.quote }}"
              </p>
            </div>

            <div class="card-footer">
              <span class="course-tag">{{ item.courseName }}</span>
            </div>
          </template>
        </div>
      </div>
    </div>

    <!-- Video Modal -->
    <Teleport to="body">
      <div v-if="activeVideoUrl" class="video-modal-backdrop" @click="closeVideo">
        <div class="video-modal-container" @click.stop>
          <button class="video-close-btn" @click="closeVideo">&times;</button>
          <div class="iframe-wrapper">
            <iframe 
              :src="activeVideoUrl" 
              title="Phỏng vấn học viên ACC Academy"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
              allowfullscreen
            ></iframe>
          </div>
        </div>
      </div>
    </Teleport>
  </section>
</template>

<script setup>
import { ref, computed } from 'vue'

const activeTab = ref('all')
const activeVideoUrl = ref('')

const tabs = [
  { id: 'all', name: 'Tất cả chia sẻ' },
  { id: 'ceo', name: '👑 Doanh nhân & CEO' },
  { id: 'influencer', name: '⭐ Idol & Influencers' },
  { id: 'video', name: '🎬 Video Phỏng vấn' }
]

const testimonials = ref([
  {
    id: 1,
    type: 'text',
    category: 'ceo',
    name: 'Nguyễn Thanh Tùng',
    role: 'Founder & CEO',
    company: 'TechVision Group',
    avatar: 'https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&w=200&q=80',
    rating: 5,
    quote: 'Chương trình ứng dụng AI trong quản trị doanh nghiệp tại ACC Academy đã giúp chúng tôi tối ưu 40% chi phí vận hành nhân sự và tăng tốc độ xây dựng sản phẩm gấp 3 lần!',
    courseName: 'Khóa học AI Skills Cho Doanh Nhân'
  },
  {
    id: 2,
    type: 'video',
    category: 'video',
    name: 'Trần Minh Đức',
    role: 'Chủ tịch HĐQT',
    company: 'Alpha Media & Marketing',
    avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80',
    videoTitle: 'Học viên Trần Minh Đức chia sẻ bí quyết nhân 5 doanh số nhờ Prompt Engineering',
    videoThumb: 'https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=600&q=80',
    videoUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ?autoplay=1',
    videoDuration: '04:15',
    courseName: 'Chương Trình Đào Tạo Doanh Nghiệp'
  },
  {
    id: 3,
    type: 'text',
    category: 'influencer',
    name: 'Hoàng Anh Thư',
    role: 'KOL & Content Creator',
    company: '1.2M Followers TikTok',
    avatar: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=200&q=80',
    rating: 5,
    quote: 'Kho khóa học và thư viện prompt của ACC là vũ khí bí mật giúp tôi sản xuất kịch bản video hàng ngày mà không bao giờ bí ý tưởng. Cực kỳ đáng đầu tư!',
    courseName: 'Ebook & Công thức Prompt'
  },
  {
    id: 4,
    type: 'text',
    category: 'ceo',
    name: 'Phạm Quốc Bảo',
    role: 'Giám đốc Điều hành',
    company: 'GreenEco Logistics',
    avatar: 'https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&w=200&q=80',
    rating: 5,
    quote: 'Chất lượng bài giảng thực chiến, giảng viên giải đáp tận tình 1-1. Đội ngũ quản lý công ty tôi đã hoàn thành lộ trình đào tạo vô cùng ấn tượng.',
    courseName: 'Khóa học Kỹ năng chuyên môn'
  },
  {
    id: 5,
    type: 'video',
    category: 'video',
    name: 'Lê Minh Hương',
    role: 'Co-Founder',
    company: 'BeautyFlora Cosmetic',
    avatar: 'https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&w=200&q=80',
    videoTitle: 'Góc nhìn Doanh nhân: Hành trình đưa AI vào tự động hóa khâu Chăm sóc khách hàng',
    videoThumb: 'https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?auto=format&fit=crop&w=600&q=80',
    videoUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ?autoplay=1',
    videoDuration: '06:30',
    courseName: 'Khóa học AI Skills'
  },
  {
    id: 6,
    type: 'text',
    category: 'influencer',
    name: 'Vũ Đăng Khoa',
    role: 'Chuyên gia Tư vấn Thương hiệu',
    company: 'Khoa Brand Lab',
    avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=200&q=80',
    rating: 5,
    quote: 'Tôi khuyên bất kỳ ai muốn nâng cấp tư duy trong kỷ nguyên số nên học tại ACC Academy. Kiến thức được đóng gói tinh gọn và cập nhật liên tục.',
    courseName: 'Khóa học Kỹ năng mềm'
  }
])

const filteredTestimonials = computed(() => {
  if (activeTab.value === 'all') return testimonials.value
  return testimonials.value.filter(item => item.category === activeTab.value)
})

const openVideo = (url) => {
  activeVideoUrl.value = url
}

const closeVideo = () => {
  activeVideoUrl.value = ''
}
</script>

<style scoped src="@/styles/components/StudentTestimonials.css"></style>
