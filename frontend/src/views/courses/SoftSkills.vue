<template>
  <div class="course-category-view container">
    <div class="header-section animate-fade-in">
      <div class="badge">CHUYÊN ĐỀ PHÁT TRIỂN NĂNG LỰC</div>
      <h1>Kỹ năng <span class="gradient-text">Mềm & Lãnh đạo</span></h1>
      <p class="subtitle">Trang bị tư duy phản biện, kỹ năng giải quyết vấn đề, nghệ thuật giao tiếp và năng lực lãnh đạo đội ngũ hướng đến hiệu suất tối ưu.</p>
    </div>

    <!-- Courses Grid -->
    <div class="courses-grid">
      <div v-for="course in softSkillsCourses" :key="course.id" class="course-card glass-card animate-slide-up">
        <div class="card-image-container">
          <img :src="course.image" :alt="course.title" class="course-image" @error="handleImageError" />
          <div class="card-image-overlay">
            <span v-for="tag in course.tags.slice(0, 2)" :key="tag" class="image-tag">{{ tag }}</span>
          </div>
        </div>
        <div class="card-body">
          <div class="card-header-meta">
            <span class="course-badge" :class="{ 'best-seller': course.price > 3000000 }">
              {{ course.price > 3000000 ? 'Chuyên sâu' : 'Hot' }}
            </span>
            <span class="level-badge">{{ course.level }}</span>
          </div>
          <h3>{{ course.title }}</h3>
          <p>{{ course.description }}</p>
          <div class="course-meta">
            <span class="duration">⏱️ {{ course.duration }}</span>
          </div>
          <div class="card-footer">
            <div class="price-container">
              <span class="original-price" v-if="course.originalPrice">{{ formatPrice(course.originalPrice) }}</span>
              <span class="price">{{ formatPrice(course.price) }}</span>
            </div>
            <router-link :to="`/contact?course=${course.handle}`" class="btn btn-primary btn-sm">Đăng ký học</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useCourseStore } from '@/stores/courses';

const courseStore = useCourseStore();
const softSkillsCourses = computed(() => courseStore.getCoursesByCategory('ky-nang-mem'));

const formatPrice = (value) => {
  return value.toLocaleString('vi-VN') + 'đ';
};

const handleImageError = (e) => {
  e.target.src = 'https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?q=80&w=600&auto=format&fit=crop';
};
</script>

<style scoped>
.course-category-view {
  padding: 80px 24px;
}

.header-section {
  text-align: center;
  max-width: 800px;
  margin: 0 auto 60px auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.badge {
  background: rgba(14, 165, 233, 0.15);
  border: 1px solid rgba(14, 165, 233, 0.3);
  color: var(--primary);
  padding: 8px 20px;
  border-radius: var(--radius-full);
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 1px;
}

.header-section h1 {
  font-family: var(--font-display);
  font-size: 52px;
  font-weight: 800;
  line-height: 1.2;
}

.subtitle {
  font-size: 18px;
  color: var(--text-secondary);
  line-height: 1.6;
}

/* Courses Grid */
.courses-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 30px;
}

.course-card {
  overflow: hidden;
  border-radius: var(--radius-lg);
  display: flex;
  flex-direction: column;
  transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.4s ease;
  height: 100%;
}

.course-card:hover {
  transform: translateY(-8px);
  box-shadow: var(--shadow-lg);
  border-color: rgba(14, 165, 233, 0.3);
}

.card-image-container {
  position: relative;
  height: 220px;
  overflow: hidden;
  border-bottom: 1px solid var(--border-color);
}

.course-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

.course-card:hover .course-image {
  transform: scale(1.05);
}

.card-image-overlay {
  position: absolute;
  bottom: 12px;
  left: 12px;
  display: flex;
  gap: 8px;
}

.image-tag {
  background: rgba(15, 23, 42, 0.75);
  backdrop-filter: blur(4px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: white;
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 500;
}

.card-body {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  flex-grow: 1;
}

.card-header-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.course-badge {
  background: rgba(16, 185, 129, 0.12);
  color: #10b981;
  padding: 4px 12px;
  border-radius: var(--radius-full);
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  border: 1px solid rgba(16, 185, 129, 0.2);
}

.course-badge.best-seller {
  background: rgba(245, 158, 11, 0.12);
  color: #f59e0b;
  border-color: rgba(245, 158, 11, 0.2);
}

.level-badge {
  font-size: 12px;
  color: var(--text-muted);
}

.card-body h3 {
  font-family: var(--font-display);
  font-size: 20px;
  font-weight: 700;
  line-height: 1.4;
  color: var(--text-primary);
}

.card-body p {
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.6;
  flex-grow: 1;
}

.course-meta {
  display: flex;
  gap: 16px;
  font-size: 13px;
  color: var(--text-muted);
  border-top: 1px solid var(--border-color);
  padding-top: 14px;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 8px;
}

.price-container {
  display: flex;
  flex-direction: column;
}

.original-price {
  font-size: 12px;
  color: var(--text-muted);
  text-decoration: line-through;
  margin-bottom: 2px;
}

.price {
  font-family: var(--font-display);
  font-size: 20px;
  font-weight: 700;
  color: var(--primary);
}

.btn-sm {
  padding: 10px 20px;
  font-size: 13px;
  font-weight: 600;
}

@media (max-width: 768px) {
  .header-section h1 {
    font-size: 38px;
  }
  
  .courses-grid {
    grid-template-columns: 1fr;
  }
}
</style>
