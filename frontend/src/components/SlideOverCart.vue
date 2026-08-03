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
              <h2>Giỏ hàng</h2>
              <span class="cart-badge">{{ totalItems }}</span>
            </div>
            <button class="close-btn" @click="closeCart" aria-label="Đóng giỏ hàng">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>

          <!-- 2. Thanh Tiến Trình Ưu Đãi (Discount Progress Bar) -->
          <div class="discount-banner">
            <p class="discount-subtitle" v-if="nextThresholdText">
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
                <div class="tier-item" :class="{ active: currentSubtotal >= 300000 }">
                  <div class="tier-node">
                    <span v-if="currentSubtotal >= 300000" class="node-icon check">✓</span>
                    <span v-else class="node-icon">🎁</span>
                  </div>
                  <span class="tier-label">Giảm 10%</span>
                </div>

                <!-- Mốc 2: 22% -->
                <div class="tier-item" :class="{ active: currentSubtotal >= 600000 }">
                  <div class="tier-node">
                    <span v-if="currentSubtotal >= 600000" class="node-icon check">✓</span>
                    <span v-else class="node-icon">%</span>
                  </div>
                  <span class="tier-label">Giảm 22%</span>
                </div>

                <!-- Mốc 3: 25% -->
                <div class="tier-item" :class="{ active: currentSubtotal >= 1000000 }">
                  <div class="tier-node">
                    <span v-if="currentSubtotal >= 1000000" class="node-icon check">✓</span>
                    <span v-else class="node-icon">🎉</span>
                  </div>
                  <span class="tier-label">Giảm 25%</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 3. Danh sách sản phẩm -->
          <div class="cart-body">
            <div v-if="cartItems.length === 0" class="empty-cart">
              <div class="empty-icon">🛒</div>
              <p>Giỏ hàng của bạn đang trống</p>
              <button class="continue-shopping-btn" @click="closeCart">Tiếp tục mua sắm</button>
            </div>

            <div v-else class="cart-items-list">
              <div v-for="item in cartItems" :key="item.id" class="cart-item">
                <div class="item-image-wrapper">
                  <img :src="item.image" :alt="item.name" class="item-image" />
                </div>

                <div class="item-details">
                  <div class="item-title-row">
                    <h4 class="item-name">
                      {{ item.name }}
                      <span v-if="item.isGift" class="gift-tag">🎁 QUÀ TẶNG 0đ</span>
                    </h4>
                  </div>

                  <div class="item-price">
                    <span class="current-price">{{ formatCurrency(item.price) }}</span>
                    <span v-if="item.originalPrice" class="original-price">{{ formatCurrency(item.originalPrice) }}</span>
                  </div>

                  <div class="item-actions">
                    <!-- Controls số lượng -->
                    <div class="quantity-control">
                      <button class="qty-btn" @click="updateQuantity(item.id, item.quantity - 1)" :disabled="item.quantity <= 1">-</button>
                      <input 
                        type="number" 
                        class="qty-input" 
                        :value="item.quantity" 
                        @change="onQuantityInputChange(item.id, $event)"
                        min="1"
                      />
                      <button class="qty-btn" @click="updateQuantity(item.id, item.quantity + 1)">+</button>
                    </div>

                    <!-- Nút Xóa -->
                    <button class="remove-btn" @click="removeItem(item.id)">
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
            <div class="summary-row">
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
                Thanh toán
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
import { useCourseStore } from '@/stores/courses'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['close', 'view-cart', 'checkout'])

const courseStore = useCourseStore()

// Checkbox đồng ý điều khoản
const agreeTerms = ref(true)

// Fallback demo items khi giỏ hàng rỗng/chưa đăng nhập
const sampleCartItems = ref([
  {
    id: 1,
    name: 'Khóa học Thiết kế UI/UX Chuyên Nghiệp',
    price: 490000,
    originalPrice: 850000,
    quantity: 1,
    image: 'https://images.unsplash.com/photo-1581291518633-83b4ebd1d83e?auto=format&fit=crop&w=200&q=80',
    isGift: false
  },
  {
    id: 2,
    name: 'Ebook Sổ Tay Phím Tắt Figma & Adobe XD',
    price: 0,
    originalPrice: 150000,
    quantity: 1,
    image: 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?auto=format&fit=crop&w=200&q=80',
    isGift: true
  }
])

const cartItems = computed(() => {
  if (courseStore.cart && courseStore.cart.length > 0) {
    return courseStore.cart.map(item => ({
      id: item.id || item.course.id,
      name: item.course.title,
      price: item.course.price,
      originalPrice: item.course.originalPrice || item.course.price * 1.5,
      quantity: item.quantity || 1,
      image: item.course.image || '/images/logo3.png',
      isGift: item.course.price === 0
    }))
  }
  return sampleCartItems.value
})

// Tính tổng số lượng sản phẩm
const totalItems = computed(() => {
  return cartItems.value.reduce((total, item) => total + item.quantity, 0)
})

// Tính tổng tiền chưa giảm
const currentSubtotal = computed(() => {
  return cartItems.value.reduce((total, item) => total + (item.price * item.quantity), 0)
})

// Cấp độ giảm giá theo mốc: 300k (10%), 600k (22%), 1000k (25%)
const discountRate = computed(() => {
  const subtotal = currentSubtotal.value
  if (subtotal >= 1000000) return 0.25
  if (subtotal >= 600000) return 0.22
  if (subtotal >= 300000) return 0.10
  return 0
})

// Số tiền cần mua thêm để đạt mốc tiếp theo
const amountToNextTier = computed(() => {
  const subtotal = currentSubtotal.value
  if (subtotal < 300000) return 300000 - subtotal
  if (subtotal < 600000) return 600000 - subtotal
  if (subtotal < 1000000) return 1000000 - subtotal
  return 0
})

// Nhãn ưu đãi mốc tiếp theo
const nextDiscountLabel = computed(() => {
  const subtotal = currentSubtotal.value
  if (subtotal < 300000) return 'Giảm 10%'
  if (subtotal < 600000) return 'Giảm 22%'
  if (subtotal < 1000000) return 'Giảm 25%'
  return ''
})

const nextThresholdText = computed(() => {
  return amountToNextTier.value > 0
})

// Phần trăm thanh tiến trình (0% - 100%)
const progressPercentage = computed(() => {
  const subtotal = currentSubtotal.value
  if (subtotal >= 1000000) return 100
  if (subtotal >= 600000) return 66 + ((subtotal - 600000) / 400000) * 34
  if (subtotal >= 300000) return 33 + ((subtotal - 300000) / 300000) * 33
  return (subtotal / 300000) * 33
})

// Tổng tiền sau giảm giá
const finalTotal = computed(() => {
  return currentSubtotal.value * (1 - discountRate.value)
})

// Hàm định dạng tiền tệ VND
const formatCurrency = (val) => {
  return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(val)
}

// Thao tác giỏ hàng
const updateQuantity = (id, newQty) => {
  if (newQty < 1) return
  const item = sampleCartItems.value.find(i => i.id === id)
  if (item) item.quantity = newQty
}

const onQuantityInputChange = (id, event) => {
  const val = parseInt(event.target.value) || 1
  updateQuantity(id, val < 1 ? 1 : val)
}

const removeItem = async (id) => {
  if (courseStore.cart && courseStore.cart.length > 0) {
    try {
      await courseStore.removeFromCart(id)
    } catch (e) {
      console.error(e)
    }
  } else {
    sampleCartItems.value = sampleCartItems.value.filter(item => item.id !== id)
  }
}

const closeCart = () => {
  emit('close')
}

const goToCart = () => {
  emit('view-cart')
}

const checkout = () => {
  if (!agreeTerms.value) return
  emit('checkout', { items: cartItems.value, total: finalTotal.value })
}
</script>

<style scoped src="@/styles/components/SlideOverCart.css"></style>
