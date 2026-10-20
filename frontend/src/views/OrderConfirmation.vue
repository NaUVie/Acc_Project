<template>
  <div class="order-confirmation-page">
    <div class="oc-container">
      <!-- Loading -->
      <div v-if="loading" class="oc-loading">
        <div class="spinner"></div>
        <p>Đang tải thông tin đơn hàng...</p>
      </div>

      <!-- Error -->
      <div v-else-if="!order" class="oc-error-card">
        <div class="error-icon">⚠️</div>
        <h2>Không tìm thấy đơn hàng</h2>
        <p>Đơn hàng #{{ orderId }} không tồn tại hoặc không thuộc tài khoản của bạn.</p>
        <router-link to="/dashboard" class="btn-primary-solid">Về Dashboard</router-link>
      </div>

      <!-- Order Confirmed -->
      <div v-else>
        <!-- Banner -->
        <div :class="['oc-banner', order.status === 'paid' ? 'banner-paid' : 'banner-pending']">
          <div class="banner-text">
            <h1 class="banner-title">
              {{ order.status === 'paid' ? 'Thanh toán thành công!' : 'Đặt hàng thành công!' }}
            </h1>
            <p class="banner-desc">
              {{ order.status === 'paid'
                ? 'Khóa học đã được kích hoạt trong tài khoản của bạn. Chúc bạn học tốt!'
                : 'Đơn hàng đã được ghi nhận. Vui lòng hoàn tất thanh toán để kích hoạt khóa học.' }}
            </p>
          </div>
        </div>

        <!-- Order Info Grid -->
        <div class="oc-grid">
          <!-- Left: Order Details -->
          <div class="oc-main">
            <!-- Order Meta Info -->
            <div class="oc-card">
              <h2 class="oc-card-title">📋 Thông tin đơn hàng</h2>
              <div class="oc-meta-grid">
                <div class="oc-meta-item">
                  <span class="meta-label">Mã đơn hàng</span>
                  <span class="meta-value code">#ACC-{{ String(order.id).padStart(6, '0') }}</span>
                </div>
                <div class="oc-meta-item">
                  <span class="meta-label">Ngày đặt hàng</span>
                  <span class="meta-value">{{ formatDate(order.createdAt) }}</span>
                </div>
                <div class="oc-meta-item">
                  <span class="meta-label">Trạng thái</span>
                  <span :class="['status-badge', order.status === 'paid' ? 'status-paid' : order.status === 'cancelled' ? 'status-cancelled' : 'status-pending']">
                    {{ statusLabel(order.status) }}
                  </span>
                </div>
                <div class="oc-meta-item">
                  <span class="meta-label">Tổng thanh toán</span>
                  <span class="meta-value price">{{ formatCurrency(order.totalPrice) }}</span>
                </div>
                <div v-if="order.discountApplied > 0" class="oc-meta-item">
                  <span class="meta-label">Giảm giá đã áp dụng</span>
                  <span class="meta-value discount">-{{ formatCurrency(order.discountApplied) }}</span>
                </div>
              </div>
            </div>

            <!-- Course Items -->
            <div class="oc-card">
              <h2 class="oc-card-title">📚 Khóa học trong đơn hàng ({{ order.items.length }} khóa)</h2>
              <div class="course-items-list">
                <div v-for="item in order.items" :key="item.id" class="course-item-row">
                  <img :src="item.course.image || '/images/default.jpg'" :alt="item.course.title" class="course-thumb" />
                  <div class="course-item-info">
                    <h3 class="course-item-title">{{ item.course.title }}</h3>
                    <span class="course-cat-tag">{{ translateCategory(item.course.category) }}</span>
                  </div>
                  <div class="course-item-price">{{ formatCurrency(item.price) }}</div>
                  <div class="course-item-action">
                    <router-link
                      v-if="order.status === 'paid'"
                      :to="`/courses/${item.course.handle}/study`"
                      class="btn-study"
                    >
                      ▶ Học ngay
                    </router-link>
                    <span v-else class="btn-study-disabled">🔒 Chờ thanh toán</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- QR Payment Section (only for pending orders) -->
            <div v-if="order.status === 'pending'" class="oc-card payment-card">
              <h2 class="oc-card-title">💳 Hoàn tất thanh toán</h2>
              <div class="qr-section">
                <div class="qr-box">
                  <img
                    :src="`https://api.vietqr.io/image/MB-999988886666-compact2.jpg?amount=${order.totalPrice}&addInfo=ACC${String(order.id).padStart(6,'0')}&accountName=ACC%20ACADEMY`"
                    alt="QR Thanh Toán"
                    class="qr-img"
                    @error="handleQrError"
                  />
                  <p class="qr-hint">Mở app Ngân hàng, quét mã QR để thanh toán</p>
                </div>
                <div class="bank-info-box">
                  <div class="bank-info-row">
                    <span class="bank-label">Ngân hàng</span>
                    <span class="bank-value">MB Bank (Quân Đội)</span>
                  </div>
                  <div class="bank-info-row">
                    <span class="bank-label">Số tài khoản</span>
                    <span class="bank-value code">999988886666</span>
                  </div>
                  <div class="bank-info-row">
                    <span class="bank-label">Chủ tài khoản</span>
                    <span class="bank-value">ACC ACADEMY CO. LTD</span>
                  </div>
                  <div class="bank-info-row highlight">
                    <span class="bank-label">Nội dung CK</span>
                    <span class="bank-value code">ACC{{ String(order.id).padStart(6, '0') }}</span>
                  </div>
                  <div class="bank-info-row highlight">
                    <span class="bank-label">Số tiền</span>
                    <span class="bank-value price">{{ formatCurrency(order.totalPrice) }}</span>
                  </div>

                  <!-- VNPay Sandbox Pay Button -->
                  <button @click="payWithVnpay" :disabled="paying" class="btn-primary-solid w-full mb-3" style="width: 100%; padding: 12px; font-weight: 700; border-radius: 8px; font-size: 14px; background: #0284c7; color: white; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px;">
                    <span>💳 Thanh toán qua cổng VNPAY</span>
                  </button>

                  <div style="font-size: 12px; color: #64748b; margin-bottom: 12px; line-height: 1.4; background: #f8fafc; padding: 10px; border-radius: 6px; border: 1px dashed #cbd5e1;">
                    <strong style="color: #0f172a;">Thông tin thẻ test VNPAY Sandbox:</strong><br/>
                    • Ngân hàng: <strong>NCB</strong><br/>
                    • Số thẻ: <strong>9704198526191432198</strong><br/>
                    • Tên: <strong>NGUYEN VAN A</strong> | Ngày: <strong>07/15</strong><br/>
                    • OTP: <strong>123456</strong>
                  </div>

                  <!-- Mock Pay Button for Testing -->
                  <button @click="mockConfirmPayment" :disabled="paying" class="btn-mock-pay">
                    <span v-if="paying">⏳ Đang xử lý...</span>
                    <span v-else>✅ Xác nhận đã chuyển khoản (Thủ công)</span>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Right: Action Sidebar -->
          <div class="oc-sidebar">
            <div class="oc-sidebar-card">
              <h3 class="sidebar-title">🚀 Bước tiếp theo</h3>
              <div v-if="order.status === 'paid'" class="next-steps">
                <div class="step-item">
                  <span class="step-num">1</span>
                  <span>Vào <strong>Dashboard</strong> để xem toàn bộ khoá học đã mua</span>
                </div>
                <div class="step-item">
                  <span class="step-num">2</span>
                  <span>Nhấn <strong>"Học ngay"</strong> ở từng khoá học để bắt đầu học</span>
                </div>
                <div class="step-item">
                  <span class="step-num">3</span>
                  <span>Chia sẻ <strong>mã giới thiệu</strong> của bạn để nhận hoa hồng</span>
                </div>
              </div>
              <div v-else class="next-steps">
                <div class="step-item">
                  <span class="step-num">1</span>
                  <span>Chuyển khoản theo thông tin bên cạnh</span>
                </div>
                <div class="step-item">
                  <span class="step-num">2</span>
                  <span>Hệ thống xác nhận trong <strong>5-15 phút</strong></span>
                </div>
                <div class="step-item">
                  <span class="step-num">3</span>
                  <span>Khóa học sẽ tự động kích hoạt trong tài khoản</span>
                </div>
              </div>

              <div class="sidebar-actions">
                <router-link to="/dashboard" class="btn-action primary">
                  📊 Về Dashboard
                </router-link>
                <router-link to="/" class="btn-action secondary">
                  🏠 Trang chủ
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useCourseStore } from '@/stores/courses';

const route = useRoute();
const router = useRouter();
const courseStore = useCourseStore();

const orderId = computed(() => route.params.id);
const order = ref(null);
const loading = ref(true);
const paying = ref(false);

const formatCurrency = (v) =>
  new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(v || 0);

const formatDate = (d) =>
  d ? new Date(d).toLocaleString('vi-VN', { dateStyle: 'medium', timeStyle: 'short' }) : '—';

const statusLabel = (s) => ({
  paid: '✅ Đã thanh toán',
  pending: '⏳ Chờ thanh toán',
  cancelled: '❌ Đã hủy'
}[s] || s);

const translateCategory = (cat) => ({
  'ky-nang-ai': 'Kỹ năng AI',
  'ky-nang-mem': 'Kỹ năng mềm',
  'ky-nang-chuyen-mon': 'Kỹ năng chuyên môn',
  'bundles': 'Combo',
}[cat] || cat);

const handleQrError = (e) => {
  e.target.src = `https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=ACC-ACADEMY-ORDER-${orderId.value}`;
};

onMounted(async () => {
  // Check store cache first for instant 0ms rendering
  const existingOrder = courseStore.orders.find(o => o.id === parseInt(orderId.value));
  if (existingOrder) {
    order.value = existingOrder;
    loading.value = false;
  }

  try {
    await courseStore.fetchOrders();
    const found = courseStore.orders.find(o => o.id === parseInt(orderId.value));
    if (found) {
      order.value = found;
    }
  } finally {
    loading.value = false;
  }
});

const payWithVnpay = async () => {
  paying.value = true;
  try {
    const res = await courseStore.createVnpayPaymentUrl(parseInt(orderId.value));
    if (res && res.payment_url) {
      window.location.href = res.payment_url;
      return;
    } else if (res && res.status === 'paid') {
      order.value = { ...order.value, status: 'paid' };
      courseStore.showToast('Đơn hàng đã được thanh toán thành công!', 'success');
    }
  } catch (err) {
    courseStore.showToast(err.message || 'Không thể tạo cổng thanh toán VNPAY', 'error');
  } finally {
    paying.value = false;
  }
};

const mockConfirmPayment = async () => {
  paying.value = true;
  try {
    const updated = await courseStore.payOrder(parseInt(orderId.value));
    if (updated) {
      order.value = courseStore.orders.find(o => o.id === parseInt(orderId.value));
      courseStore.showToast('Xác nhận thanh toán thành công! Khóa học đã được kích hoạt.', 'success');
    }
  } catch (e) {
    courseStore.showToast('Không thể xác nhận thanh toán: ' + e.message, 'error');
  } finally {
    paying.value = false;
  }
};
</script>

<style scoped src="@/styles/views/OrderConfirmation.css"></style>
