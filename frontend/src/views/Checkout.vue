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
              <label class="payment-option" :class="{ active: paymentMethod === 'vnpay' }">
                <input type="radio" v-model="paymentMethod" value="vnpay" />
                <div class="option-content">
                  <div class="option-header">
                    <span class="option-title">Cổng thanh toán VNPAY (Thẻ ATM, QR VNPAY, Thẻ Quốc Tế)</span>
                    <span class="badge-recommended">Thanh toán trực tiếp - Tự động</span>
                  </div>
                  <p class="option-desc">Chuyển hướng trực tiếp sang cổng VNPAY (môi trường Demo Sandbox) để thanh toán an toàn và kích hoạt ngay tức thì.</p>
                </div>
              </label>

              <label class="payment-option" :class="{ active: paymentMethod === 'qr' }">
                <input type="radio" v-model="paymentMethod" value="qr" />
                <div class="option-content">
                  <div class="option-header">
                    <span class="option-title">Chuyển khoản Ngân hàng qua VietQR</span>
                  </div>
                  <p class="option-desc">Nhận thông tin số tài khoản và mã QR để chuyển khoản thủ công sau khi tạo đơn.</p>
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

            <!-- Coupon Input Box -->
            <div style="margin-bottom: 16px;">
              <label style="font-size: 12px; font-weight: 700; color: #475569; display: block; margin-bottom: 6px;">MÃ GIẢM GIÁ (COUPON)</label>
              <div style="display: flex; gap: 8px;">
                <input 
                  type="text" 
                  v-model="couponCode" 
                  placeholder="Nhập mã coupon..." 
                  style="flex: 1; padding: 8px 12px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 13px; text-transform: uppercase;"
                />
                <button 
                  @click="applyCouponCode" 
                  :disabled="applyingCoupon"
                  style="background: #0284c7; color: white; border: none; border-radius: 8px; padding: 8px 14px; font-weight: 700; font-size: 13px; cursor: pointer;"
                >
                  {{ applyingCoupon ? '...' : 'Áp dụng' }}
                </button>
              </div>
              <p v-if="couponMessage" :style="{ color: couponSuccess ? '#16a34a' : '#dc2626' }" style="font-size: 12px; margin: 4px 0 0 0; font-weight: 600;">
                {{ couponMessage }}
              </p>
            </div>

            <!-- Store Credit Wallet Checkbox -->
            <div v-if="userStoreCredit > 0" style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 10px; padding: 12px; margin-bottom: 16px;">
              <label style="display: flex; align-items: center; gap: 10px; cursor: pointer;">
                <input type="checkbox" v-model="useStoreCredit" style="width: 18px; height: 18px; accent-color: #16a34a;" />
                <div>
                  <div style="font-size: 13px; font-weight: 700; color: #15803d;">Dùng số dư Ví tích lũy</div>
                  <div style="font-size: 12px; color: #166534;">Khả dụng: {{ formatCurrency(userStoreCredit) }}</div>
                </div>
              </label>
            </div>

            <div class="summary-row">
              <span>Tạm tính</span>
              <span>{{ formatCurrency(currentSubtotal) }}</span>
            </div>

            <div class="summary-row discount" v-if="referralDiscountAmount > 0">
              <span>Ưu đãi Giới thiệu (10%)</span>
              <span>-{{ formatCurrency(referralDiscountAmount) }}</span>
            </div>

            <div class="summary-row discount" v-if="couponDiscount > 0">
              <span>Mã giảm giá ({{ couponCodeApplied }})</span>
              <span>-{{ formatCurrency(couponDiscount) }}</span>
            </div>

            <div class="summary-row discount" v-if="storeCreditDiscount > 0">
              <span>Trừ Ví tích lũy</span>
              <span>-{{ formatCurrency(storeCreditDiscount) }}</span>
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
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCourseStore } from '@/stores/courses'

const router = useRouter()
const courseStore = useCourseStore()

const loading = ref(false)
const paymentMethod = ref('vnpay')

const form = ref({
  fullname: '',
  email: '',
  phone: '',
  note: ''
})

const couponCode = ref('')
const couponCodeApplied = ref('')
const couponDiscount = ref(0)
const applyingCoupon = ref(false)
const couponMessage = ref('')
const couponSuccess = ref(false)

const useStoreCredit = ref(false)
const userStoreCredit = computed(() => {
  return courseStore.userMe?.storeCreditBalance || courseStore.referralSummary?.storeCreditBalance || 0
})

onMounted(async () => {
  if (!courseStore.token) {
    courseStore.showToast('Vui lòng đăng nhập để tiến hành thanh toán!', 'warning')
    router.push('/login')
    return
  }
  if (courseStore.userMe) {
    form.value.fullname = courseStore.userMe.fullname || ''
    form.value.email = courseStore.userMe.email || ''
  }
  const tasks = [courseStore.fetchMyReferralSummary()];
  if (!courseStore.userMe) tasks.push(courseStore.fetchUserMe());
  if (courseStore.cart.length === 0) tasks.push(courseStore.fetchCart());
  await Promise.all(tasks).catch(() => {});
  if (courseStore.userMe) {
    if (!form.value.fullname) form.value.fullname = courseStore.userMe.fullname || '';
    if (!form.value.email) form.value.email = courseStore.userMe.email || '';
  }
})

const cartItems = computed(() => {
  if (!courseStore.token) return [];
  return courseStore.cart.map(item => ({
    id: item.id || item.course.id,
    name: item.course.title,
    price: item.course.price,
    quantity: 1,
    image: item.course.image || '/images/logo3.png'
  }));
})

const currentSubtotal = computed(() => {
  return cartItems.value.reduce((total, item) => total + (item.price * item.quantity), 0)
})

const isFirstPurchase = computed(() => {
  return (courseStore.orders || []).filter(o => o.status === 'paid').length === 0
})

const isReferredUser = computed(() => {
  return Boolean(courseStore.userMe?.referredById || courseStore.userMe?.referred_by_id)
})

const referralDiscountAmount = computed(() => {
  if (isReferredUser.value && isFirstPurchase.value) {
    return Math.floor(currentSubtotal.value * 0.10)
  }
  return 0
})

const storeCreditDiscount = computed(() => {
  if (!useStoreCredit.value) return 0;
  const afterPrior = Math.max(0, currentSubtotal.value - referralDiscountAmount.value - couponDiscount.value);
  return Math.min(userStoreCredit.value, afterPrior);
})

const finalTotal = computed(() => {
  const total = currentSubtotal.value - referralDiscountAmount.value - couponDiscount.value - storeCreditDiscount.value;
  return Math.max(0, total);
})

const applyCouponCode = async () => {
  if (!couponCode.value.trim()) {
    couponMessage.value = 'Vui lòng nhập mã coupon';
    couponSuccess.value = false;
    return;
  }
  applyingCoupon.value = true;
  couponMessage.value = '';
  try {
    const res = await courseStore.applyCoupon(couponCode.value.trim(), currentSubtotal.value);
    couponDiscount.value = res.discount_amount;
    couponCodeApplied.value = res.code;
    couponMessage.value = res.message;
    couponSuccess.value = true;
  } catch (err) {
    couponDiscount.value = 0;
    couponCodeApplied.value = '';
    couponMessage.value = err.message || 'Mã giảm giá không hợp lệ';
    couponSuccess.value = false;
  } finally {
    applyingCoupon.value = false;
  }
}

const formatCurrency = (val) => {
  return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(val)
}

const handlePlaceOrder = async () => {
  if (!courseStore.token) {
    courseStore.showToast('Vui lòng đăng nhập để thực hiện thanh toán!', 'warning')
    router.push('/login')
    return
  }
  if (!form.value.fullname || !form.value.email || !form.value.phone) {
    courseStore.showToast('Vui lòng điền đầy đủ Họ tên, Email và Số điện thoại!', 'warning')
    return
  }

  loading.value = true

  try {
    const order = await courseStore.checkoutWithOptions(couponCodeApplied.value || null, useStoreCredit.value)
    if (order && order.id) {
      if (paymentMethod.value === 'vnpay' && order.status !== 'paid' && order.total_price > 0) {
        // Generate VNPay URL & redirect
        try {
          const vnpRes = await courseStore.createVnpayPaymentUrl(order.id);
          if (vnpRes && vnpRes.payment_url) {
            window.location.href = vnpRes.payment_url;
            return;
          }
        } catch (vnpErr) {
          console.error("VNPay init error:", vnpErr);
          courseStore.showToast("Không thể khởi tạo cổng VNPAY. Chuyển sang xem thông tin đơn hàng.", "warning");
        }
      }
      router.push(`/order/${order.id}`)
    } else {
      router.push('/dashboard')
    }
  } catch (e) {
    console.log("Order submission error", e)
    courseStore.showToast(e.message || "Có lỗi xảy ra khi tạo đơn hàng. Vui lòng thử lại!", 'error')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped src="@/styles/views/Checkout.css"></style>
