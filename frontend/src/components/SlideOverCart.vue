<template>
  <Teleport to="body">
    <div v-show="isOpen" class="cart-slideover-container">
      <!-- Backdrop overlay with transition -->
      <Transition name="fade" appear>
        <div v-if="isOpen" class="cart-backdrop" @click="closeCart"></div>
      </Transition>

      <!-- Slide-over panel with right-to-left transition -->
      <Transition name="slide" appear>
        <div v-if="isOpen" class="cart-panel">
          <!-- 1. Header Giỏ hàng -->
          <div class="cart-header">
            <div class="header-title">
              <h2>Giỏ hàng của bạn</h2>
              <span class="cart-badge">{{ cartCount }}</span>
            </div>
            <button class="close-btn" @click="closeCart" aria-label="Đóng giỏ hàng">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>

          <!-- 2. Thanh Tiến Trình Ưu Đãi (Discount Progress Bar) -->
          <div class="discount-banner" v-if="cartItems.length > 0">
            <p class="discount-subtitle" v-if="amountToNextTier > 0">
              Mua thêm <strong>{{ formatCurrency(amountToNextTier) }}</strong> để được <strong>{{ nextDiscountLabel }}</strong>!
            </p>
            <p class="discount-subtitle achieve-text" v-else>
              🎉 Bạn đã đạt mức ưu đãi cao nhất <strong>Giảm 25%</strong>!
            </p>

            <div class="progress-bar-wrapper">
              <div class="progress-track">
                <div class="progress-fill" :style="{ width: progressPercentage + '%' }"></div>
              </div>

              <div class="progress-tiers">
                <!-- Mốc 1: 10% -->
                <div class="tier-item" :class="{ active: currentSubtotal >= 3000000 }">
                  <div class="tier-node">
                    <span v-if="currentSubtotal >= 3000000" class="node-icon check">✓</span>
                    <span v-else class="node-icon">🎁</span>
                  </div>
                  <span class="tier-label">Giảm 10%</span>
                </div>

                <!-- Mốc 2: 20% -->
                <div class="tier-item" :class="{ active: currentSubtotal >= 6000000 }">
                  <div class="tier-node">
                    <span v-if="currentSubtotal >= 6000000" class="node-icon check">✓</span>
                    <span v-else class="node-icon">%</span>
                  </div>
                  <span class="tier-label">Giảm 20%</span>
                </div>

                <!-- Mốc 3: 25% -->
                <div class="tier-item" :class="{ active: currentSubtotal >= 10000000 }">
                  <div class="tier-node">
                    <span v-if="currentSubtotal >= 10000000" class="node-icon check">✓</span>
                    <span v-else class="node-icon">🎉</span>
                  </div>
                  <span class="tier-label">Giảm 25%</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 3. Danh sách sản phẩm thực từ Store -->
          <div class="cart-body">
            <div v-if="cartItems.length === 0" class="empty-cart">
              <div class="empty-icon">🛒</div>
              <p>Giỏ hàng của bạn đang trống</p>
              <button class="continue-shopping-btn" @click="closeCart">Tiếp tục khám phá khóa học</button>
            </div>

            <div v-else class="cart-items-list">
              <div v-for="item in cartItems" :key="item.cartId" class="cart-item">
                <div class="item-image-wrapper">
                  <img :src="item.image" :alt="item.name" class="item-image" />
                </div>

                <div class="item-details">
                  <div class="item-title-row">
                    <h4 class="item-name">
                      {{ item.name }}
                    </h4>
                  </div>

                  <div class="item-price">
                    <span class="current-price">{{ formatCurrency(item.price) }}</span>
                    <span v-if="item.originalPrice && item.originalPrice > item.price" class="original-price">
                      {{ formatCurrency(item.originalPrice) }}
                    </span>
                  </div>

                  <div class="item-actions">
                    <!-- Nút Xóa khỏi giỏ hàng -->
                    <button class="remove-btn" @click="removeItem(item.courseId)" :disabled="loading">
                      <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="3 6 5 6 21 6"></polyline>
                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                      </svg>
                      Xóa
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 4. Footer Thanh toán -->
          <div class="cart-footer" v-if="cartItems.length > 0">
            <div class="summary-row" v-if="discountRate > 0">
              <span class="summary-label">Tạm tính</span>
              <span class="summary-amount-sub">{{ formatCurrency(currentSubtotal) }}</span>
            </div>
            <div class="summary-row" v-if="discountRate > 0">
              <span class="summary-label">Ưu đãi giảm giá ({{ Math.round(discountRate * 100) }}%)</span>
              <span class="summary-amount-discount">-{{ formatCurrency(currentSubtotal * discountRate) }}</span>
            </div>
            <div class="summary-row highlight">
              <span class="summary-label">Tổng thanh toán</span>
              <span class="summary-amount">{{ formatCurrency(finalTotal) }}</span>
            </div>

            <div class="terms-checkbox">
              <label class="checkbox-label">
                <input type="checkbox" v-model="agreeTerms" />
                <span class="checkmark"></span>
                <span class="text">
                  Tôi đồng ý với <a href="#" @click.prevent>Điều khoản sử dụng</a> & <a href="#" @click.prevent>Chính sách quyền riêng tư</a>
                </span>
              </label>
            </div>

            <div class="action-buttons">
              <button class="btn btn-view-cart" @click="goToCart">
                Xem giỏ hàng
              </button>
              <button 
                class="btn btn-checkout" 
                :disabled="!agreeTerms"
                @click="checkout"
              >
                Thanh toán ngay
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useCourseStore } from '@/stores/courses'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'view-cart', 'checkout'])

const router = useRouter()
const courseStore = useCourseStore()

const agreeTerms = ref(true)
const loading = ref(false)

// Dynamic cart items bound to real backend store
const cartItems = computed(() => {
  if (!courseStore.cart) return []
  return courseStore.cart.map(item => ({
    cartId: item.id,
    courseId: item.course?.id,
    name: item.course?.title || 'Khóa học',
    price: item.course?.price || 0,
    originalPrice: item.course?.original_price || item.course?.originalPrice || null,
    image: item.course?.image || '/images/logo3.png'
  }))
})

const cartCount = computed(() => cartItems.value.length)

// Subtotal calculation
const currentSubtotal = computed(() => {
  return cartItems.value.reduce((total, item) => total + item.price, 0)
})

// Tier discounts: 3 triệu (10%), 6 triệu (20%), 10 triệu (25%)
const discountRate = computed(() => {
  const subtotal = currentSubtotal.value
  if (subtotal >= 10000000) return 0.25
  if (subtotal >= 6000000) return 0.20
  if (subtotal >= 3000000) return 0.10
  return 0
})

const amountToNextTier = computed(() => {
  const subtotal = currentSubtotal.value
  if (subtotal < 3000000) return 3000000 - subtotal
  if (subtotal < 6000000) return 6000000 - subtotal
  if (subtotal < 10000000) return 10000000 - subtotal
  return 0
})

const nextDiscountLabel = computed(() => {
  const subtotal = currentSubtotal.value
  if (subtotal < 3000000) return 'Giảm 10%'
  if (subtotal < 6000000) return 'Giảm 20%'
  if (subtotal < 10000000) return 'Giảm 25%'
  return ''
})

const progressPercentage = computed(() => {
  const subtotal = currentSubtotal.value
  if (subtotal >= 10000000) return 100
  if (subtotal >= 6000000) return 66 + ((subtotal - 6000000) / 4000000) * 34
  if (subtotal >= 3000000) return 33 + ((subtotal - 3000000) / 3000000) * 33
  return (subtotal / 3000000) * 33
})

const finalTotal = computed(() => {
  return currentSubtotal.value * (1 - discountRate.value)
})

const formatCurrency = (val) => {
  return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(val || 0)
}

const removeItem = async (courseId) => {
  if (!courseStore.token) {
    alert('Vui lòng đăng nhập để thao tác với giỏ hàng!')
    return
  }
  loading.value = true
  try {
    await courseStore.removeFromCart(courseId)
  } catch (e) {
    console.error('Error removing item from cart:', e)
  } finally {
    loading.value = false
  }
}

const closeCart = () => {
  emit('close')
}

const goToCart = () => {
  closeCart()
  router.push('/cart')
}

const checkout = () => {
  if (!agreeTerms.value) return
  closeCart()
  router.push('/checkout')
}
</script>

<style scoped src="@/styles/components/SlideOverCart.css"></style>
