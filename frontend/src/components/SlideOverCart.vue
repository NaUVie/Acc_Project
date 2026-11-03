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
              <h2>{{ $t('cart.title') }}</h2>
              <span class="cart-badge">{{ cartCount }}</span>
            </div>
            <button class="close-btn" @click="closeCart" :aria-label="$t('cart.close')">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>

          <!-- 3. Danh sách sản phẩm thực từ Store -->
          <div class="cart-body">
            <div v-if="cartItems.length === 0" class="empty-cart">
              <div class="empty-icon">🛒</div>
              <p>{{ $t('cart.empty') }}</p>
              <button class="continue-shopping-btn" @click="closeCart">{{ $t('cart.continueShopping') }}</button>
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
            
            <div class="summary-row highlight">
              <div>
                <span class="summary-label">{{ $t('cart.total') }}</span>
                <div style="font-size: 11px; font-weight: 500; color: #16a34a; margin-top: 2px;">(Đã bao gồm VAT)</div>
              </div>
              <span class="summary-amount">{{ formatCurrency(finalTotal) }}</span>
            </div>

            <div class="terms-checkbox">
              <label class="checkbox-label">
                <input type="checkbox" v-model="agreeTerms" />
                <span class="checkmark"></span>
                <span class="text">
                  Tôi đồng ý với <router-link to="/terms-of-service" @click="emit('close')" style="color: #022B9F; text-decoration: underline;">Điều khoản dịch vụ</router-link> &amp; <router-link to="/privacy-policy" @click="emit('close')" style="color: #022B9F; text-decoration: underline;">Chính sách bảo mật</router-link>
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

const finalTotal = computed(() => {
  return currentSubtotal.value
})

const formatCurrency = (val) => {
  return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(val || 0)
}

const removeItem = async (courseId) => {
  if (!courseStore.token) {
    courseStore.showToast('Vui lòng đăng nhập để thao tác với giỏ hàng!', 'warning')
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
