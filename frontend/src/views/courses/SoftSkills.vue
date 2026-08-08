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
        <router-link :to="'/course/' + course.handle" class="card-image-container">
          <img :src="course.image" :alt="course.title" class="course-image" @error="handleImageError" />
          <div class="card-image-overlay">
            <span v-for="tag in course.tags.slice(0, 2)" :key="tag" class="image-tag">{{ tag }}</span>
          </div>
        </router-link>
        <div class="card-body">
          <div class="card-header-meta">
            <span class="course-badge" :class="{ 'best-seller': course.price > 3000000 }">
              {{ course.price > 3000000 ? 'Chuyên sâu' : 'Hot' }}
            </span>
            <span class="level-badge">{{ course.level }}</span>
          </div>
          <h3>
            <router-link :to="'/course/' + course.handle" class="course-title-link">
              {{ course.title }}
            </router-link>
          </h3>
          <p>{{ course.description }}</p>
          <div class="course-meta">
            <span class="duration">⏱️ {{ course.duration }}</span>
          </div>
          <div class="card-footer">
            <div class="price-container">
              <span class="original-price" v-if="course.originalPrice">{{ formatPrice(course.originalPrice) }}</span>
              <span class="price">{{ formatPrice(course.price) }}</span>
            </div>
            <button @click.stop="handleEnroll(course.id)" class="btn btn-primary btn-sm">Đăng ký học</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { useCourseStore } from '@/stores/courses';

const router = useRouter();
const courseStore = useCourseStore();
const softSkillsCourses = computed(() => courseStore.getCoursesByCategory('ky-nang-mem'));

const formatPrice = (value) => {
  return value.toLocaleString('vi-VN') + 'đ';
};

const handleEnroll = (courseId) => {
  if (!courseStore.token) {
    alert('Vui lòng đăng nhập để đăng ký khóa học!');
    router.push('/login');
    return;
  }
  try {
    courseStore.buyNow(courseId);
    router.push('/checkout');
  } catch (err) {
    alert(err.message || 'Có lỗi xảy ra khi đăng ký khóa học!');
  }
};

const handleImageError = (e) => {
  e.target.src = 'https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?q=80&w=600&auto=format&fit=crop';
};
</script>

<style scoped src="@/styles/views/courses/SoftSkills.css"></style>
