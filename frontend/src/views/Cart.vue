<template>
  <div class="cart-page">
    <div class="container">
      <div class="cart-page-header">
        <h1 class="page-title">Giỏ hàng của bạn</h1>
        <p class="page-subtitle">Kiểm tra lại các khóa học và ưu đãi trước khi tiến hành thanh toán</p>
      </div>

      <div v-if="cartItems.length === 0" class="empty-cart-state">
        <div class="empty-icon">🛒</div>
        <h3>Giỏ hàng đang trống</h3>
        <p>Bạn chưa thêm khóa học nào vào giỏ hàng.</p>
        <router-link to="/courses/ai" class="btn-browse">Khám phá khóa học ngay</router-link>
      </div>

      <div v-else class="cart-layout">
        <!-- Main Cart Items List -->
        <div class="cart-main-content">
          <div class="cart-table-card">
            <div class="table-header">
              <span class="col-product">Khóa học</span>
              <span class="col-price">Đơn giá</span>
              <span class="col-quantity">Số lượng</span>
              <span class="col-total">Thành tiền</span>
              <span class="col-action"></span>
            </div>

            <div class="table-body">
              <div v-for="item in cartItems" :key="item.id" class="cart-row">
                <div class="col-product product-info">
                  <img :src="item.image" :alt="item.name" class="product-thumb" />
                  <div class="product-details">
                    <h4 class="product-name">
                      {{ item.name }}
                      <span v-if="item.isGift" class="gift-badge">🎁 QUÀ TẶNG 0đ</span>
                    </h4>
                    <span class="product-cat" v-if="item.category">{{ item.category }}</span>
                  </div>
                </div>

                <div class="col-price">
                  <span class="price-current">{{ formatCurrency(item.price) }}</span>
                  <span v-if="item.originalPrice" class="price-original">{{ formatCurrency(item.originalPrice) }}</span>
                </div>

                <div class="col-quantity">
                  <div class="qty-picker">
                    <button class="qty-btn" @click="updateQty(item.id, item.quantity - 1)" :disabled="item.quantity <= 1">-</button>
                    <span class="qty-val">{{ item.quantity }}</span>
                    <button class="qty-btn" @click="updateQty(item.id, item.quantity + 1)">+</button>
                  </div>
                </div>

                <div class="col-total">
                  <span class="row-total-price">{{ formatCurrency(item.price * item.quantity) }}</span>
                </div>

                <div class="col-action">
                  <button class="remove-btn" @click="removeItem(item.id)" title="Xóa khóa học">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <polyline points="3 6 5 6 21 6"></polyline>
                      <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div class="cart-actions-row">
            <router-link to="/courses/ai" class="btn-back">
              &larr; Tiếp tục chọn khóa học
            </router-link>
          </div>
        </div>

        <!-- Sidebar Summary -->
        <div class="cart-summary-sidebar">
          <div class="summary-card">
            <h3 class="summary-title">Tóm tắt đơn hàng</h3>

            <div class="summary-line">
              <span>Tạm tính</span>
              <span class="val">{{ formatCurrency(currentSubtotal) }}</span>
            </div>

            <div class="summary-line discount-line" v-if="discountAmount > 0">
              <span>Ưu đãi giảm giá ({{ discountRate * 100 }}%)</span>
              <span class="val-discount">-{{ formatCurrency(discountAmount) }}</span>
            </div>

            <!-- Promotion code input -->
            <div class="promo-box">
              <input type="text" v-model="promoCode" placeholder="Mã giảm giá (nếu có)" class="promo-input" />
              <button class="promo-btn" @click="applyPromo">Áp dụng</button>
            </div>

            <div class="divider"></div>

            <div class="summary-line total-line">
              <span>Tổng cộng</span>
              <span class="total-amount">{{ formatCurrency(finalTotal) }}</span>
            </div>

            <button class="btn-proceed-checkout" @click="goToCheckout">
              Tiến hành thanh toán
            </button>

            <div class="security-note">
              <span>🔒 Giao dịch thanh toán an toàn & bảo mật 100%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useCourseStore } from '@/stores/courses'

const router = useRouter()
const courseStore = useCourseStore()
const promoCode = ref('')

const sampleCartItems = ref([
  {
    id: 1,
    name: 'Khóa học Thiết kế UI/UX Chuyên Nghiệp',
    price: 490000,
    originalPrice: 850000,
    quantity: 1,
    image: 'https://images.unsplash.com/photo-1581291518633-83b4ebd1d83e?auto=format&fit=crop&w=300&q=80',
    category: 'Kỹ năng chuyên môn',
    isGift: false
  },
  {
    id: 2,
    name: 'Ebook Sổ Tay Phím Tắt Figma & Adobe XD',
    price: 0,
    originalPrice: 150000,
    quantity: 1,
    image: 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?auto=format&fit=crop&w=300&q=80',
    category: 'Tài liệu tặng kèm',
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
      category: item.course.category,
      isGift: item.course.price === 0
    }))
  }
  return sampleCartItems.value
})

const currentSubtotal = computed(() => {
  return cartItems.value.reduce((total, item) => total + (item.price * item.quantity), 0)
})

const discountRate = computed(() => {
  const subtotal = currentSubtotal.value
  if (subtotal >= 1000000) return 0.25
  if (subtotal >= 600000) return 0.22
  if (subtotal >= 300000) return 0.10
  return 0
})

const discountAmount = computed(() => {
  return currentSubtotal.value * discountRate.value
})

const finalTotal = computed(() => {
  return currentSubtotal.value - discountAmount.value
})

const formatCurrency = (val) => {
  return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(val)
}

const updateQty = (id, newQty) => {
  if (newQty < 1) return
  const item = sampleCartItems.value.find(i => i.id === id)
  if (item) item.quantity = newQty
}

const removeItem = async (id) => {
  if (courseStore.cart && courseStore.cart.length > 0) {
    try {
      await courseStore.removeFromCart(id)
    } catch (e) {
      console.error(e)
    }
  } else {
    sampleCartItems.value = sampleCartItems.value.filter(i => i.id !== id)
  }
}

const applyPromo = () => {
  if (!promoCode.value.trim()) return
  alert(`Mã giảm giá "${promoCode.value}" đã được áp dụng thành công!`)
}

const goToCheckout = () => {
  router.push('/checkout')
}
</script>

<style scoped src="@/styles/views/Cart.css"></style>
