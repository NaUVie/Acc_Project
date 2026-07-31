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
            <router-link :to="`/contact?course=${bundle.handle}`" class="btn btn-primary">Mua gói Combo</router-link>
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

const calculateDiscount = (original, current) => {
  if (!original) return 20;
  return Math.round(((original - current) / original) * 100);
};

const handleImageError = (e) => {
  e.target.src = 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?q=80&w=600&auto=format&fit=crop';
};
</script>

<style scoped>
.bundles-view {
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

.bundles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(460px, 1fr));
  gap: 40px;
}

.bundle-card {
  border-radius: var(--radius-lg);
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
  transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.4s ease;
  height: 100%;
}

.bundle-card:hover {
  transform: translateY(-8px);
  box-shadow: var(--shadow-lg);
  border-color: rgba(14, 165, 233, 0.3);
}

.bundle-badge {
  position: absolute;
  top: 20px;
  right: 20px;
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  padding: 6px 14px;
  border-radius: var(--radius-full);
  font-size: 12px;
  font-weight: 700;
  box-shadow: 0 4px 10px rgba(239, 68, 68, 0.3);
  z-index: 10;
}

.bundle-image-container {
  height: 240px;
  overflow: hidden;
  border-bottom: 1px solid var(--border-color);
}

.bundle-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

.bundle-card:hover .bundle-image {
  transform: scale(1.03);
}

.bundle-content {
  padding: 30px;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.bundle-content h2 {
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 800;
  margin-bottom: 16px;
  line-height: 1.3;
  color: var(--text-primary);
}

.bundle-desc {
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 24px;
}

.included-info {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid var(--border-color);
  padding: 20px;
  border-radius: var(--radius-md);
  margin-bottom: 30px;
  flex-grow: 1;
}

.included-info h3 {
  font-family: var(--font-display);
  font-size: 14px;
  font-weight: 700;
  margin-bottom: 12px;
  color: var(--text-primary);
}

.included-info ul {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 0;
}

.included-info li {
  font-size: 14px;
  color: var(--text-secondary);
}

.bundle-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid var(--border-color);
  padding-top: 24px;
}

.price-section {
  display: flex;
  flex-direction: column;
}

.old-price {
  font-size: 13px;
  color: var(--text-muted);
  text-decoration: line-through;
  margin-bottom: 2px;
}

.new-price {
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 800;
  color: var(--primary);
}

@media (max-width: 968px) {
  .bundles-grid {
    grid-template-columns: 1fr;
  }
}
</style>
