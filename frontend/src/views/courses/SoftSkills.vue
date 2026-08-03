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
            <button @click="handleEnroll(course.id)" class="btn btn-primary btn-sm">Đăng ký học</button>
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

const handleEnroll = async (courseId) => {
  try {
    await courseStore.addToCart(courseId);
  } catch (err) {
    console.error(err);
  }
};

const handleImageError = (e) => {
  e.target.src = 'https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?q=80&w=600&auto=format&fit=crop';
};
</script>

<style scoped src="@/styles/views/courses/SoftSkills.css"></style>
