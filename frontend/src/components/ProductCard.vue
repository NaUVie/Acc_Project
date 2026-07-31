<template>
  <div class="product-card" :data-handle="course.handle">
    <!-- Discount Badge -->
    <div v-if="discount > 0" class="product-card__badge-list">
      <span class="badge badge--on-sale">Giảm {{ formatPrice(discount) }}</span>
    </div>

    <!-- Product Figure (Image + Quick Buy) -->
    <div class="product-card__figure">
      <router-link :to="`/contact?course=${course.handle}`" class="product-card__image-link">
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
          <router-link :to="`/contact?course=${course.handle}`" class="bold">
            {{ course.title }}
          </router-link>
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

const props = defineProps({
  course: {
    type: Object,
    required: true
  }
});

const router = useRouter();

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

const handleQuickBuy = () => {
  // Navigate to contact page with prefilled course
  router.push(`/contact?course=${props.props?.course?.handle || props.course.handle}`);
};
</script>

<style scoped>
.product-card {
  position: relative;
  display: flex;
  flex-direction: column;
  background: var(--bg-secondary, #ffffff);
  border-radius: var(--radius-md, 12px);
  border: 1px solid var(--border-color, rgba(16, 24, 40, 0.08));
  overflow: hidden;
  transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.4s ease, border-color 0.4s ease;
  height: 100%;
}

.product-card:hover {
  transform: translateY(-6px);
  box-shadow: var(--shadow-md, 0 10px 30px rgba(16, 24, 40, 0.06));
  border-color: rgba(2, 43, 159, 0.25);
}

/* Badge List */
.product-card__badge-list {
  position: absolute;
  top: 12px;
  left: 12px;
  z-index: 5;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  font-size: 11px;
  font-weight: 700;
  line-height: 1.2;
  border-radius: 4px;
  text-transform: uppercase;
}

.badge--on-sale {
  background-color: #f04438;
  color: #ffffff;
}

/* Product Figure */
.product-card__figure {
  position: relative;
  width: 100%;
  aspect-ratio: 1 / 1;
  background-color: #f9fafb;
  overflow: hidden;
}

.product-card__image-link {
  display: block;
  width: 100%;
  height: 100%;
}

.product-card__image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

.product-card:hover .product-card__image {
  transform: scale(1.05);
}

/* Quick Buy Overlay */
.product-card__quick-buy {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  padding: 12px;
  background: linear-gradient(to top, rgba(16, 24, 40, 0.15) 0%, rgba(16, 24, 40, 0) 100%);
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0;
  transform: translateY(10px);
  transition: opacity 0.3s ease, transform 0.3s ease;
  pointer-events: none;
  z-index: 4;
}

.product-card:hover .product-card__quick-buy {
  opacity: 1;
  transform: translateY(0);
  pointer-events: auto;
}

/* Quick Buy Buttons style */
.button--quick-buy {
  background-color: #ffffff;
  color: #101828;
  border: 1px solid rgba(16, 24, 40, 0.1);
  padding: 8px 16px;
  font-size: 13px;
  font-weight: 600;
  border-radius: var(--radius-full, 9999px);
  box-shadow: 0 2px 8px rgba(16, 24, 40, 0.05);
  transition: background-color 0.2s ease, transform 0.2s ease;
  width: 100%;
  cursor: pointer;
  text-align: center;
}

.button--quick-buy:hover {
  background-color: #101828;
  color: #ffffff;
  transform: scale(1.02);
}

.product-card__mobile-quick-buy-button {
  background-color: #ffffff;
  color: #101828;
  border: 1px solid rgba(16, 24, 40, 0.1);
  border-radius: 50%;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(16, 24, 40, 0.05);
  cursor: pointer;
}

/* Product Info */
.product-card__info {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex-grow: 1;
}

.product-card__meta {
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex-grow: 1;
}

.product-card__title {
  font-size: 14px;
  font-weight: 500;
  line-height: 1.4;
  color: var(--text-primary-color, #101828);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  height: 2.8em; /* Force height for 2 lines alignment */
  flex-grow: 1;
}

.product-card__title a {
  color: inherit;
  text-decoration: none;
}

.product-card__title a:hover {
  color: var(--primary, #20869a);
}

.price-list {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: var(--font-sans);
  margin-top: auto;
}

.price-list__sale {
  font-size: 15px;
  font-weight: 700;
  color: #f04438;
}

.price-list__compare {
  font-size: 13px;
  color: var(--text-muted, #667085);
}

/* Visibility utilities based on pointer type */
.desktop-only {
  display: block;
}

.mobile-only {
  display: none;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .product-card__quick-buy {
    opacity: 1;
    transform: translateY(0);
    pointer-events: auto;
    background: transparent;
    padding: 8px;
    bottom: auto;
    top: 12px;
    right: 12px;
    left: auto;
    width: auto;
  }
  
  .desktop-only {
    display: none;
  }
  
  .mobile-only {
    display: flex;
  }
  
  .product-card__info {
    padding: 12px;
  }
  
  .product-card__title {
    font-size: 13px;
  }
  
  .price-list__sale {
    font-size: 14px;
  }
  
  .price-list__compare {
    font-size: 12px;
  }
}
</style>
