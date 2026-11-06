<template>
  <div class="vnpay-return-page container" style="max-width: 600px; margin: 60px auto; padding: 24px;">
    <div class="glass-card text-center" style="background: white; border-radius: 16px; padding: 36px 24px; box-shadow: 0 4px 24px rgba(0,0,0,0.06); border: 1px solid #e2e8f0;">
      
      <!-- Loading State -->
      <div v-if="loading" style="padding: 30px 0;">
        <div class="spinner" style="margin: 0 auto 16px auto; width: 44px; height: 44px; border: 4px solid #e2e8f0; border-top-color: #0284c7; border-radius: 50%; animation: spin 1s linear infinite;"></div>
        <h3 style="font-size: 18px; color: #0f172a; margin-bottom: 8px;">Đang xác thực giao dịch VNPAY...</h3>
        <p style="color: #64748b; font-size: 14px;">Vui lòng giữ nguyên màn hình, không đóng trình duyệt.</p>
      </div>

      <!-- Success State -->
      <div v-else-if="result && result.success">
        <div style="font-size: 56px; line-height: 1; margin-bottom: 16px;">🎉</div>
        <h2 style="color: #16a34a; font-weight: 800; font-size: 24px; margin-bottom: 12px;">Thanh toán thành công!</h2>
        <p style="color: #475569; font-size: 15px; margin-bottom: 24px;">
          Giao dịch VNPAY của đơn hàng <strong style="color: #0f172a;">#ACC-{{ String(result.order_id).padStart(6, '0') }}</strong> đã được xử lý hoàn tất. Khóa học của bạn đã được kích hoạt thành công!
        </p>
        <div style="display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;">
          <router-link :to="`/order/${result.order_id}`" class="btn btn-secondary" style="padding: 10px 20px; font-weight: 600;">
            Xem chi tiết đơn hàng
          </router-link>
          <router-link to="/dashboard" class="btn btn-primary" style="padding: 10px 24px; font-weight: 700; background: #0284c7; color: white;">
            Về trang cá nhân →
          </router-link>
        </div>
      </div>

      <!-- Failure State -->
      <div v-else>
        <div style="font-size: 56px; line-height: 1; margin-bottom: 16px;">❌</div>
        <h2 style="color: #dc2626; font-weight: 800; font-size: 24px; margin-bottom: 12px;">Thanh toán không thành công</h2>
        <p style="color: #475569; font-size: 15px; margin-bottom: 24px;">
          {{ result?.message || 'Giao dịch qua cổng VNPAY đã bị hủy hoặc xảy ra lỗi trong quá trình xử lý.' }}
        </p>
        <div style="display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;">
          <router-link v-if="result?.order_id" :to="`/order/${result.order_id}`" class="btn btn-primary" style="padding: 10px 24px; font-weight: 700; background: #0284c7; color: white;">
            Thử thanh toán lại
          </router-link>
          <router-link to="/cart" class="btn btn-secondary" style="padding: 10px 20px; font-weight: 600;">
            Về giỏ hàng
          </router-link>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useCourseStore } from '@/stores/courses';

const route = useRoute();
const courseStore = useCourseStore();

const loading = ref(true);
const result = ref(null);

onMounted(async () => {
  try {
    const res = await courseStore.verifyVnpayReturn(route.query);
    result.value = res;
    if (res && res.success) {
      courseStore.showToast('Giao dịch thành công! Khóa học đã được kích hoạt.', 'success');
    } else {
      courseStore.showToast(res?.message || 'Giao dịch không thành công.', 'error');
    }
  } catch (err) {
    result.value = {
      success: false,
      message: err.message || 'Lỗi kết nối khi kiểm tra trạng thái thanh toán'
    };
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
