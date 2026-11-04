<template>
  <div class="product-card" :data-handle="course.handle">

    <!-- Product Figure (Image + Quick Buy) -->
    <div class="product-card__figure">
      <router-link :to="'/course/' + course.handle" class="product-card__image-link">
        <img 
          :src="course.image" 
          :alt="course.title" 
          class="product-card__image"
          @error="handleImageError"
        />
      </router-link>
      
      <!-- Quick Buy Buttons -->
      <div class="product-card__quick-buy">
        <!-- Desktop Quick Buy -->
        <button 
          @click="handleQuickBuy"
          class="button button--quick-buy desktop-only" 
          type="button"
        >
          Xem chi tiết
        </button>
        <!-- Mobile Quick Buy Icon -->
        <button 
          @click="handleQuickBuy"
          class="product-card__mobile-quick-buy-button mobile-only" 
          aria-label="Xem chi tiết"
          type="button"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="9 18 15 12 9 6"></polyline>
          </svg>
        </button>
      </div>
    </div>

    <!-- Product Details -->
    <div class="product-card__info">
      <div class="product-card__meta">
        <span class="product-card__title">
          <router-link :to="'/course/' + course.handle" class="bold">
            {{ course.title }}
          </router-link>
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { useCourseStore } from '@/stores/courses';

const props = defineProps({
  course: {
    type: Object,
    required: true
  }
});

const router = useRouter();
const courseStore = useCourseStore();

const discount = computed(() => {
  if (props.course.originalPrice && props.course.originalPrice > props.course.price) {
    return props.course.originalPrice - props.course.price;
  }
  return 0;
});

const formatPrice = (value) => {
  return value.toLocaleString('vi-VN') + '₫';
};

const handleImageError = (e) => {
  e.target.src = '/images/LS_Looker_Studio_for_Everyone_SQR.png';
};

const handleQuickBuy = (e) => {
  if (e && e.stopPropagation) e.stopPropagation();
  router.push('/courses/' + (props.course.handle || props.course.id));
};
</script>

<style scoped src="@/styles/components/ProductCard.css"></style>
