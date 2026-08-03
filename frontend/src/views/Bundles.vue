<template>
  <div class="bundles-view container">
    <div class="header-section animate-fade-in">
      <div class="badge">COMBO TIẾT KIỆM</div>
      <h1>Các gói <span class="gradient-text">Combo Khóa học</span></h1>
      <p class="subtitle">Tiết kiệm chi phí lên đến 30% và sở hữu lộ trình phát triển kỹ năng toàn diện cùng các gói bundle được thiết kế tối ưu.</p>
    </div>

    <!-- Bundles List -->
    <div class="bundles-grid">
      <div v-for="bundle in bundles" :key="bundle.id" class="bundle-card glass-card animate-slide-up">
        <div class="bundle-badge">GIẢM {{ calculateDiscount(bundle.originalPrice, bundle.price) }}%</div>
        <div class="bundle-image-container">
          <img :src="bundle.image" :alt="bundle.title" class="bundle-image" @error="handleImageError" />
        </div>
        <div class="bundle-content">
          <h2>{{ bundle.title }}</h2>
          <p class="bundle-desc">{{ bundle.description }}</p>
          
          <div class="included-info">
            <h3>Lợi ích & Thời lượng:</h3>
            <ul>
              <li>⏱️ Thời lượng: {{ bundle.duration }}</li>
              <li>⚡ Cấp độ: {{ bundle.level }}</li>
              <li>🎓 Chứng nhận tốt nghiệp & Hỗ trợ trọn đời</li>
            </ul>
          </div>
          
          <div class="bundle-footer">
            <div class="price-section">
              <span class="old-price" v-if="bundle.originalPrice">{{ formatPrice(bundle.originalPrice) }}</span>
              <span class="new-price">{{ formatPrice(bundle.price) }}</span>
            </div>
            <button @click="handleEnroll(bundle.id)" class="btn btn-primary">Mua gói Combo</button>
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
const bundles = computed(() => courseStore.getCoursesByCategory('bundles'));

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

const calculateDiscount = (original, current) => {
  if (!original) return 20;
  return Math.round(((original - current) / original) * 100);
};

const handleImageError = (e) => {
  e.target.src = 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?q=80&w=600&auto=format&fit=crop';
};
</script>

<style scoped src="@/styles/views/Bundles.css"></style>
