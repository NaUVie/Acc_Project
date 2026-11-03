<template>
  <div class="admin-coupons-component">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
      <div>
        <h2 style="font-size: 20px; font-weight: 800; color: #0f172a; margin: 0;">Quản lý Mã giảm giá (Coupons)</h2>
        <p style="font-size: 13px; color: #64748b; margin: 4px 0 0 0;">Tạo mã voucher khuyến mãi giảm theo % hoặc số tiền cố định cho học viên khi checkout.</p>
      </div>
      <div style="display: flex; gap: 10px; align-items: center;">
        <button @click="refreshCoupons" :disabled="isRefreshing" class="btn btn-secondary btn-sm" style="display: flex; align-items: center; gap: 6px; font-weight: 600;" title="Tải lại danh sách mã giảm giá mới nhất">
          <span :class="{ 'spin-icon': isRefreshing }">🔄</span>
          <span>{{ isRefreshing ? 'Đang đồng bộ...' : 'Làm mới dữ liệu' }}</span>
        </button>
        <button @click="showModal = true" class="btn btn-primary btn-sm" style="border-radius: 8px; padding: 8px 16px; font-weight: 700;">
          + Tạo Mã Coupon Mới
        </button>
      </div>
    </div>

    <!-- Coupons Table -->
    <div class="table-responsive mt-6" style="background: white; border: 1px solid #e2e8f0; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
      <table class="admin-table" style="min-width: 650px; border-collapse: collapse; font-size: 14px; text-align: left;">
        <thead style="background: #f8fafc; border-bottom: 1px solid #e2e8f0; color: #475569; font-weight: 700;">
          <tr>
            <th style="padding: 12px 16px;">Mã Coupon</th>
            <th style="padding: 12px 16px;">Mức giảm</th>
            <th style="padding: 12px 16px;">Đơn tối thiểu</th>
            <th style="padding: 12px 16px;">Lượt dùng</th>
            <th style="padding: 12px 16px;">Trạng thái</th>
            <th style="padding: 12px 16px; text-align: right;">Thao tác</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="courseStore.adminCoupons.length === 0">
            <td colspan="6" style="text-align: center; padding: 30px; color: #94a3b8;">Chưa có mã giảm giá nào được tạo.</td>
          </tr>
          <tr v-for="c in courseStore.adminCoupons" :key="c.id" style="border-bottom: 1px solid #f1f5f9;">
            <td style="padding: 12px 16px; font-weight: 800; color: #0284c7; font-family: monospace; font-size: 15px;">{{ c.code }}</td>
            <td style="padding: 12px 16px; font-weight: 700; color: #16a34a;">
              {{ c.discount_type === 'percent' ? `${c.discount_value}%` : formatPrice(c.discount_value) }}
            </td>
            <td style="padding: 12px 16px; color: #475569;">{{ formatPrice(c.min_order_value) }}</td>
            <td style="padding: 12px 16px; color: #475569;">{{ c.times_used }} / {{ c.usage_limit > 0 ? c.usage_limit : '∞' }}</td>
            <td style="padding: 12px 16px;">
              <span style="background: #dcfce7; color: #15803d; padding: 4px 8px; border-radius: 6px; font-size: 12px; font-weight: 700;">
                {{ c.is_active ? 'Hoạt động' : 'Tắt' }}
              </span>
            </td>
            <td style="padding: 12px 16px; text-align: right;">
              <button @click="handleDelete(c.id)" style="background: #fef2f2; color: #ef4444; border: 1px solid #fecaca; border-radius: 6px; padding: 6px 12px; font-weight: 600; cursor: pointer;">
                🗑️ Xóa
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Create Coupon Modal -->
    <div v-if="showModal" style="position: fixed; inset: 0; background: rgba(15,23,42,0.6); display: flex; align-items: center; justify-content: center; z-index: 1000; padding: 20px;">
      <div style="background: white; border-radius: 16px; width: 100%; max-width: 520px; padding: 24px; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1); max-height: 90vh; overflow-y: auto;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
          <h3 style="font-size: 18px; font-weight: 800; color: #0f172a; margin: 0;">Tạo Mã Coupon Mới</h3>
          <button @click="showModal = false" style="background: none; border: none; font-size: 20px; cursor: pointer; color: #64748b;">✕</button>
        </div>

        <form @submit.prevent="handleCreate">
          <div style="margin-bottom: 14px;">
            <label style="font-size: 13px; font-weight: 700; color: #475569; display: block; margin-bottom: 4px;">Mã Coupon (VD: ACC2026, SUMMER50)</label>
            <input type="text" v-model="form.code" required placeholder="NHAPMA..." style="width: 100%; padding: 10px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 14px; text-transform: uppercase; box-sizing: border-box;" />
          </div>

          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 14px;">
            <div>
              <label style="font-size: 13px; font-weight: 700; color: #475569; display: block; margin-bottom: 4px;">Loại giảm giá</label>
              <select v-model="form.discount_type" style="width: 100%; padding: 10px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 14px; box-sizing: border-box;">
                <option value="percent">Theo phần trăm (%)</option>
                <option value="fixed">Số tiền cố định (VND)</option>
              </select>
            </div>
            <div>
              <label style="font-size: 13px; font-weight: 700; color: #475569; display: block; margin-bottom: 4px;">Giá trị giảm</label>
              <input type="number" v-model.number="form.discount_value" required placeholder="VD: 20 hoặc 100000" style="width: 100%; padding: 10px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 14px; box-sizing: border-box;" />
            </div>
          </div>

          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 14px;">
            <div>
              <label style="font-size: 13px; font-weight: 700; color: #475569; display: block; margin-bottom: 4px;">Đơn tối thiểu (VND)</label>
              <input type="number" v-model.number="form.min_order_value" placeholder="0" style="width: 100%; padding: 10px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 14px; box-sizing: border-box;" />
            </div>
            <div>
              <label style="font-size: 13px; font-weight: 700; color: #475569; display: block; margin-bottom: 4px;">Giới hạn lượt dùng</label>
              <input type="number" v-model.number="form.usage_limit" placeholder="0 (Không giới hạn)" style="width: 100%; padding: 10px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 14px; box-sizing: border-box;" />
            </div>
          </div>

          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 20px;">
            <div>
              <label style="font-size: 13px; font-weight: 700; color: #475569; display: block; margin-bottom: 4px;">Ngày bắt đầu</label>
              <input type="date" v-model="form.valid_from" style="width: 100%; padding: 10px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 14px; box-sizing: border-box;" />
            </div>
            <div>
              <label style="font-size: 13px; font-weight: 700; color: #475569; display: block; margin-bottom: 4px;">Hạn sử dụng</label>
              <input type="date" v-model="form.valid_to" style="width: 100%; padding: 10px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 14px; box-sizing: border-box;" />
            </div>
          </div>

          <div style="display: flex; justify-content: flex-end; gap: 10px;">
            <button type="button" @click="showModal = false" style="background: #f1f5f9; border: none; padding: 10px 16px; border-radius: 8px; font-weight: 700; cursor: pointer; color: #475569;">Hủy</button>
            <button type="submit" :disabled="submitting" style="background: #0284c7; color: white; border: none; padding: 10px 20px; border-radius: 8px; font-weight: 700; cursor: pointer;">
              {{ submitting ? 'Đang tạo...' : 'Tạo Coupon' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useCourseStore } from '@/stores/courses';

const courseStore = useCourseStore();
const showModal = ref(false);
const submitting = ref(false);
const isRefreshing = ref(false);

const refreshCoupons = async () => {
  isRefreshing.value = true;
  try {
    await courseStore.fetchAdminCoupons(true);
    courseStore.showToast('Đã làm mới danh sách mã giảm giá!', 'success');
  } catch (err) {
    courseStore.showToast('Lỗi khi làm mới: ' + (err.message || err), 'error');
  } finally {
    isRefreshing.value = false;
  }
};

const form = ref({
  code: '',
  discount_type: 'percent',
  discount_value: 10,
  min_order_value: 0,
  usage_limit: 0,
  valid_from: '',
  valid_to: ''
});

const formatPrice = (val) => {
  if (!val && val !== 0) return '0đ';
  return val.toLocaleString('vi-VN') + 'đ';
};

const handleCreate = async () => {
  submitting.value = true;
  try {
    await courseStore.addAdminCoupon({
      code: form.value.code.toUpperCase().trim(),
      discount_type: form.value.discount_type,
      discount_value: form.value.discount_value,
      min_order_value: form.value.min_order_value || 0,
      usage_limit: form.value.usage_limit || 0,
      valid_from: form.value.valid_from ? new Date(form.value.valid_from).toISOString() : null,
      valid_to: form.value.valid_to ? new Date(form.value.valid_to).toISOString() : null
    });
    showModal.value = false;
    form.value.code = '';
  } catch (err) {
    // handled in store
  } finally {
    submitting.value = false;
  }
};


const handleDelete = async (couponId) => {
  const isConfirmed = await courseStore.showConfirm({
    title: 'Xác nhận xóa mã giảm giá',
    message: 'Bạn có chắc chắn muốn xóa mã coupon giảm giá này?',
    confirmText: 'Đồng ý xóa',
    cancelText: 'Hủy bỏ',
    type: 'danger'
  });

  if (isConfirmed) {
    await courseStore.deleteAdminCoupon(couponId);
  }
};

onMounted(() => {
  courseStore.fetchAdminCoupons();
});
</script>
