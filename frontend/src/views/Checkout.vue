<template>
  <div class="checkout-page">
    <div class="container">
      <div class="checkout-header">
        <h1 class="page-title">Thanh toán đơn hàng</h1>
        <p class="page-subtitle">Vui lòng hoàn tất thông tin đăng ký học viên và chọn phương thức thanh toán</p>
      </div>

      <div class="checkout-layout">
        <!-- Main Form -->
        <div class="checkout-main">
          <!-- Step 1: Customer Info -->
          <div class="form-card">
            <h2 class="card-title">
              <span class="step-num">1</span> Thông tin học viên
            </h2>

            <div class="form-grid">
              <div class="form-group full-width">
                <label>Họ và tên <span class="required">*</span></label>
                <input type="text" v-model="form.fullname" placeholder="Nguyễn Văn A" class="form-control" />
              </div>

              <div class="form-group">
                <label>Địa chỉ Email <span class="required">*</span></label>
                <input type="email" v-model="form.email" placeholder="example@gmail.com" class="form-control" />
              </div>

              <div class="form-group">
                <label>Số điện thoại <span class="required">*</span></label>
                <input type="tel" v-model="form.phone" placeholder="0901234567" class="form-control" />
              </div>

              <div class="form-group full-width">
                <label>Ghi chú đơn hàng (nếu có)</label>
                <textarea v-model="form.note" rows="2" placeholder="Cần tư vấn thêm lộ trình học hoặc hỗ trợ xuất hóa đơn VAT..." class="form-control"></textarea>
              </div>
            </div>
          </div>

          <!-- Step 2: Payment Methods -->
          <div class="form-card">
            <h2 class="card-title">
              <span class="step-num">2</span> Phương thức thanh toán
            </h2>

            <div class="payment-methods">
              <label class="payment-option" :class="{ active: paymentMethod === 'qr' }">
                <input type="radio" v-model="paymentMethod" value="qr" />
                <div class="option-content">
                  <div class="option-header">
                    <span class="option-title">Quét mã QR Ngân hàng (VietQR / Chuyển khoản 24/7)</span>
                    <span class="badge-recommended">Khuyên dùng - Duyệt tự động</span>
                  </div>
                  <p class="option-desc">Mở app Ngân hàng (MB, Vietcombank, Techcombank, VPBank...) quét mã QR để kích hoạt khóa học tức thì.</p>
                </div>
              </label>

              <label class="payment-option" :class="{ active: paymentMethod === 'momo' }">
                <input type="radio" v-model="paymentMethod" value="momo" />
                <div class="option-content">
                  <div class="option-header">
                    <span class="option-title">Ví điện tử MoMo / ZaloPay</span>
                  </div>
                  <p class="option-desc">Thanh toán nhanh chóng qua ứng dụng ví điện tử MoMo hoặc ZaloPay.</p>
                </div>
              </label>

              <label class="payment-option" :class="{ active: paymentMethod === 'card' }">
                <input type="radio" v-model="paymentMethod" value="card" />
                <div class="option-content">
                  <div class="option-header">
                    <span class="option-title">Thẻ ATM nội địa / Thẻ quốc tế (Visa, Mastercard)</span>
                  </div>
                  <p class="option-desc">Cổng thanh toán bảo mật OnePay / VNPay hỗ trợ thẻ tất cả các ngân hàng Việt Nam & Quốc tế.</p>
                </div>
              </label>
            </div>
          </div>
        </div>

        <!-- Sidebar Summary -->
        <div class="checkout-sidebar">
          <div class="order-summary-card">
            <h3 class="summary-title">Thông tin đơn hàng</h3>

            <div class="items-preview-list">
              <div v-for="item in cartItems" :key="item.id" class="preview-item">
                <img :src="item.image" :alt="item.name" class="preview-thumb" />
                <div class="preview-info">
                  <span class="preview-name">{{ item.name }}</span>
                  <div class="preview-meta">
                    <span class="preview-qty">SL: {{ item.quantity }}</span>
                    <span class="preview-price">{{ formatCurrency(item.price * item.quantity) }}</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="summary-divider"></div>

            <div class="summary-row">
              <span>Tạm tính</span>
              <span>{{ formatCurrency(currentSubtotal) }}</span>
            </div>

            <div class="summary-row discount" v-if="discountAmount > 0">
              <span>Ưu đãi áp dụng ({{ discountRate * 100 }}%)</span>
              <span>-{{ formatCurrency(discountAmount) }}</span>
            </div>

            <div class="summary-divider"></div>

            <div class="summary-row total">
              <span>Tổng thanh toán</span>
              <span class="total-price">{{ formatCurrency(finalTotal) }}</span>
            </div>

            <button class="btn-complete-order" :disabled="loading" @click="handlePlaceOrder">
              <span v-if="loading">Đang xử lý đơn hàng...</span>
              <span v-else>XÁC NHẬN & THANH TOÁN</span>
            </button>

            <p class="terms-notice">
              Bằng cách nhấn "Xác nhận & Thanh toán", bạn đồng ý với <a href="#" @click.prevent>Điều khoản dịch vụ</a> của ACC Academy.
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- QR Modal Success / Payment Modal -->
    <Teleport to="body">
      <div v-if="showSuccessModal" class="modal-backdrop" @click="showSuccessModal = false">
        <div class="modal-box" @click.stop>
          <button class="modal-close" @click="showSuccessModal = false">&times;</button>
          <div class="modal-body text-center">
            <div class="success-icon">🎉</div>
            <h2 class="modal-title">Đặt hàng thành công!</h2>
            <p class="modal-desc">Mã đơn hàng: <strong>#ACC-{{ Math.floor(100000 + Math.random() * 900000) }}</strong></p>

            <div class="qr-payment-box" v-if="paymentMethod === 'qr'">
              <p class="qr-instruction">Quét mã QR dưới đây bằng app Ngân hàng để hoàn tất thanh toán:</p>
              <img src="https://api.qrserver.com/v1/create-qr-code/?size=220x220&data=ACC_ACADEMY_PAYMENT" alt="Mã QR Thanh Toán" class="qr-img" />
              <div class="bank-details">
                <p>Ngân hàng: <strong>MBBank (Ngân Hàng Quân Đội)</strong></p>
                <p>Số tài khoản: <strong>999988886666</strong></p>
                <p>Chủ tài khoản: <strong>ACC ACADEMY CO. LTD</strong></p>
                <p>Nội dung CK: <strong>ACC {{ form.phone || 'PAY' }}</strong></p>
              </div>
            </div>

            <p v-else class="success-note">Hệ thống sẽ gửi thông tin tài khoản học qua Email <strong>{{ form.email }}</strong> của bạn ngay lập tức.</p>

            <button class="btn-dashboard" @click="finishOrder">Đến trang Học tập ngay</button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCourseStore } from '@/stores/courses'

const router = useRouter()
const courseStore = useCourseStore()

const loading = ref(false)
const showSuccessModal = ref(false)
const paymentMethod = ref('qr')

const form = ref({
  fullname: '',
  email: '',
  phone: '',
  note: ''
})

onMounted(() => {
  if (courseStore.userMe) {
    form.value.fullname = courseStore.userMe.fullname || ''
    form.value.email = courseStore.userMe.email || ''
  }
})

const sampleCartItems = ref([
  {
    id: 1,
    name: 'Khóa học Thiết kế UI/UX Chuyên Nghiệp',
    price: 490000,
    quantity: 1,
    image: 'https://images.unsplash.com/photo-1581291518633-83b4ebd1d83e?auto=format&fit=crop&w=200&q=80'
  },
  {
    id: 2,
    name: 'Ebook Sổ Tay Phím Tắt Figma & Adobe XD',
    price: 0,
    quantity: 1,
    image: 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?auto=format&fit=crop&w=200&q=80'
  }
])

const cartItems = computed(() => {
  if (courseStore.cart && courseStore.cart.length > 0) {
    return courseStore.cart.map(item => ({
      id: item.id || item.course.id,
      name: item.course.title,
      price: item.course.price,
      quantity: item.quantity || 1,
      image: item.course.image || '/images/logo2.jpg'
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

const handlePlaceOrder = async () => {
  if (!form.value.fullname || !form.value.email || !form.value.phone) {
    alert('Vui lòng điền đầy đủ Họ tên, Email và Số điện thoại!')
    return
  }

  loading.value = true

  try {
    if (courseStore.token) {
      await courseStore.checkout()
    }
  } catch (e) {
    console.log("Mocking order submission for frontend display", e)
  } finally {
    loading.value = false
    showSuccessModal.value = true
  }
}

const finishOrder = () => {
  showSuccessModal.value = false
  router.push('/dashboard')
}
</script>

<style scoped src="@/styles/views/Checkout.css"></style>
