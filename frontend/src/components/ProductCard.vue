<template>
  <div class="product-card" :data-handle="course.handle">
    <!-- Discount Badge -->
    <div v-if="discount > 0" class="product-card__badge-list">
      <span class="badge badge--on-sale">Giảm {{ formatPrice(discount) }}</span>
    </div>

    <!-- Product Figure (Image + Quick Buy) -->
    <div class="product-card__figure">
      <a href="#" @click.prevent="handleQuickBuy" class="product-card__image-link">
        <img 
          :src="course.image" 
          :alt="course.title" 
          class="product-card__image"
          @error="handleImageError"
        />
      </a>
      
      <!-- Quick Buy Buttons -->
      <div class="product-card__quick-buy">
        <!-- Desktop Quick Buy -->
        <button 
          @click="handleQuickBuy"
          class="button button--quick-buy desktop-only" 
          type="button"
        >
          + Thêm nhanh
        </button>
        <!-- Mobile Quick Buy Icon -->
        <button 
          @click="handleQuickBuy"
          class="product-card__mobile-quick-buy-button mobile-only" 
          aria-label="+ Thêm nhanh"
          type="button"
        >
          <svg role="presentation" fill="none" stroke-width="2" focusable="false" width="16" height="14" class="icon icon-quick-buy-cart" viewBox="0 0 16 14">
            <path d="M7.75 4.75H2.283a1 1 0 0 0-.97 1.244l1.574 6.25a1 1 0 0 0 .97.756h7.787a1 1 0 0 0 .97-.756l1.573-6.25a1 1 0 0 0-.97-1.244H7.75Zm0 0V1" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"></path>
          </svg>
        </button>
      </div>
    </div>

    <!-- Product Details -->
    <div class="product-card__info">
      <div class="product-card__meta">
        <span class="product-card__title">
          <a href="#" @click.prevent="handleQuickBuy" class="bold">
            {{ course.title }}
          </a>
        </span>
        <div class="price-list">
          <span class="price-list__sale text-on-sale">
            {{ formatPrice(course.price) }}
          </span>
          <span v-if="course.originalPrice" class="price-list__compare text-subdued line-through">
            {{ formatPrice(course.originalPrice) }}
          </span>
        </div>
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

const handleQuickBuy = async () => {
  try {
    await courseStore.addToCart(props.course.id);
  } catch (err) {
    console.error(err);
  }
};
</script>

<style scoped src="@/styles/components/ProductCard.css"></style>
