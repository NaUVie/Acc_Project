<template>
  <div class="cart-page">
    <div class="container">
      <div class="cart-page-header">
        <h1 class="page-title">Giỏ hàng của bạn</h1>
        <p class="page-subtitle">Kiểm tra lại các khóa học và ưu đãi trước khi tiến hành thanh toán</p>
      </div>

      <!-- Trạng thái chưa đăng nhập -->
      <div v-if="!courseStore.token" class="empty-cart-state">
        <div class="empty-icon">🔑</div>
        <h3>Bạn chưa đăng nhập</h3>
        <p>Vui lòng đăng nhập để xem giỏ hàng của bạn.</p>
        <router-link to="/login" class="btn-browse">Đăng nhập ngay</router-link>
      </div>

      <!-- Giỏ hàng trống (đã đăng nhập) -->
      <div v-else-if="cartItems.length === 0" class="empty-cart-state">
        <div class="empty-icon">🛒</div>
        <h3>Giỏ hàng đang trống</h3>
        <p>Bạn chưa thêm khóa học nào vào giỏ hàng.</p>
        <router-link to="/courses/category/ky-nang-ai" class="btn-browse">Khám phá khóa học ngay</router-link>
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
                      <span v-if="item.price === 0" class="gift-badge" style="background: #f1f5f9; color: #475569; border: 1px solid #cbd5e1;">Miễn phí</span>
                    </h4>
                    <span class="product-cat" v-if="item.category">{{ item.category }}</span>
                  </div>
                </div>

                <div class="col-price">
                  <span class="price-current">{{ formatCurrency(item.price) }}</span>
                  <span v-if="item.originalPrice && item.originalPrice > item.price" class="price-original">{{ formatCurrency(item.originalPrice) }}</span>
                </div>

                <div class="col-quantity">
                  <span class="qty-val" style="padding: 0 16px; font-weight: 600;">1</span>
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
            <router-link to="/courses/category/ky-nang-ai" class="btn-back">
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

            <div class="summary-line discount-line" v-if="appliedCouponDiscount > 0" style="display: flex; justify-content: space-between; color: #16a34a; font-weight: 600; margin: 8px 0;">
              <span>Mã giảm giá ({{ courseStore.appliedCoupon?.code }})</span>
              <span class="val-discount">-{{ formatCurrency(appliedCouponDiscount) }}</span>
            </div>

            <!-- Promotion code input -->
            <div class="promo-box">
              <input type="text" v-model="promoCode" placeholder="Mã giảm giá (nếu có)" class="promo-input" style="text-transform: uppercase;" />
              <button class="promo-btn" @click="applyPromo" :disabled="applyingPromo">{{ applyingPromo ? '...' : 'Áp dụng' }}</button>
            </div>

            <div class="divider"></div>

            <div class="summary-line total-line">
              <div>
                <span>Tổng cộng</span>
                <div style="font-size: 11px; font-weight: 500; color: #16a34a; margin-top: 2px;">(Đã bao gồm thuế GTGT / VAT)</div>
              </div>
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
const promoCode = ref(courseStore.appliedCoupon?.code || '')
const applyingPromo = ref(false)

const appliedCouponDiscount = computed(() => {
  if (!courseStore.appliedCoupon) return 0
  return courseStore.appliedCoupon.discount_amount || 0
})

const cartItems = computed(() => {
  if (!courseStore.token) return [];
  return courseStore.cart.map(item => ({
    id: item.course?.id || item.id,
    cartId: item.id,
    name: item.course?.title || 'Khóa học',
    price: item.course?.price || 0,
    originalPrice: item.course?.originalPrice || null,
    quantity: 1,
    image: item.course?.image || '/images/logo3.png',
    category: item.course?.category,
    isGift: item.course?.price === 0
  }));
})

const currentSubtotal = computed(() => {
  return cartItems.value.reduce((total, item) => total + (item.price * item.quantity), 0)
})

const finalTotal = computed(() => {
  return Math.max(0, currentSubtotal.value - appliedCouponDiscount.value)
})

const formatCurrency = (val) => {
  return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(val)
}

const removeItem = async (id) => {
  try {
    await courseStore.removeFromCart(id)
    courseStore.showToast('Đã xóa khóa học khỏi giỏ hàng', 'success')
  } catch (e) {
    console.error(e)
  }
}

const applyPromo = async () => {
  if (!promoCode.value.trim()) {
    courseStore.appliedCoupon = null
    return
  }
  applyingPromo.value = true
  try {
    const res = await courseStore.applyCoupon(promoCode.value.trim(), currentSubtotal.value)
    if (!res.valid) {
      courseStore.appliedCoupon = null
      courseStore.showToast(res.message || 'Mã giảm giá không hợp lệ!', 'error')
      return
    }
    courseStore.appliedCoupon = res
    courseStore.showToast(`Áp dụng thành công mã "${res.code}"! Giảm ${formatCurrency(res.discount_amount)}`, 'success')
  } catch (err) {
    courseStore.appliedCoupon = null
    courseStore.showToast(err.message || 'Lỗi khi kiểm tra mã giảm giá', 'error')
  } finally {
    applyingPromo.value = false
  }
}

const goToCheckout = () => {
  if (!courseStore.token) {
    courseStore.showToast('Vui lòng đăng nhập để tiến hành thanh toán!', 'warning')
    router.push('/login')
    return
  }
  router.push('/checkout')
}
</script>

<style scoped src="@/styles/views/Cart.css"></style>
