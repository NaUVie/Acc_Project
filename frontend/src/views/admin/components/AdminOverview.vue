<template>
  <div class="tab-content animate-fade-in">
    <div class="content-header" style="display: flex; justify-content: space-between; align-items: center;">
      <div>
        <h2>Bảng điều khiển Tổng quan</h2>
        <p>Thống kê số liệu vận hành của nền tảng ACC Academy.</p>
      </div>
      <div style="display: flex; gap: 8px; align-items: center;">
        <select v-model="exportPeriod" style="padding: 8px 12px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 13px; font-weight: 600; color: #334155; background: white;">
          <option value="all">Tất cả thời gian</option>
          <option value="month">30 ngày qua (Tháng)</option>
          <option value="quarter">90 ngày qua (Quý)</option>
          <option value="year">365 ngày qua (Năm)</option>
        </select>
        <button @click="courseStore.exportAdminReport('orders', exportPeriod)" style="background: #0284c7; color: white; border: none; border-radius: 8px; padding: 8px 14px; font-weight: 700; font-size: 13px; cursor: pointer; display: flex; align-items: center; gap: 4px;">
          Xuất CSV Đơn hàng
        </button>
        <button @click="courseStore.exportAdminReport('users', exportPeriod)" style="background: #0d9488; color: white; border: none; border-radius: 8px; padding: 8px 14px; font-weight: 700; font-size: 13px; cursor: pointer; display: flex; align-items: center; gap: 4px;">
          Xuất CSV Học viên
        </button>
        <button @click="courseStore.exportAdminReport('revenue', exportPeriod)" style="background: #16a34a; color: white; border: none; border-radius: 8px; padding: 8px 14px; font-weight: 700; font-size: 13px; cursor: pointer; display: flex; align-items: center; gap: 4px;">
          Báo cáo Doanh thu
        </button>
      </div>
    </div>

    <!-- Stats Grid -->
    <div class="stats-grid">
      <div class="admin-stat-card">
        <div class="stat-info">
          <h3>Doanh thu</h3>
          <div class="stat-number">{{ formatPrice(totalRevenue) }}</div>
          <p class="stat-helper">Đã đối soát thanh toán</p>
        </div>
      </div>
      <div class="admin-stat-card">
        <div class="stat-info">
          <h3>Học viên</h3>
          <div class="stat-number">{{ users.length }}</div>
          <p class="stat-helper">Tài khoản trên hệ thống</p>
        </div>
      </div>
      <div class="admin-stat-card">
        <div class="stat-info">
          <h3>Đơn hàng</h3>
          <div class="stat-number">{{ orders.length }}</div>
          <p class="stat-helper">{{ orders.filter(o => o.status === 'pending').length }} đơn chờ thanh toán</p>
        </div>
      </div>
      <div class="admin-stat-card">
        <div class="stat-info">
          <h3>Yêu cầu tư vấn</h3>
          <div class="stat-number">{{ contacts.filter(c => !c.isResolved).length }}</div>
          <p class="stat-helper">Chưa phản hồi hỗ trợ</p>
        </div>
      </div>
    </div>

    <!-- Recent activities grid -->
    <div class="recent-grid mt-8">
      <div class="recent-panel glass-card">
        <h3>Đơn hàng mới nhất</h3>
        <div class="table-responsive">
          <table class="admin-table">
            <thead>
              <tr>
                <th>Mã đơn</th>
                <th>Khách hàng</th>
                <th>Tổng tiền</th>
                <th>Trạng thái</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="order in orders.slice(-3).reverse()" :key="order.id">
                <td class="font-bold">#{{ order.id }}</td>
                <td>{{ order.userFullname }}</td>
                <td class="price-text">{{ formatPrice(order.totalPrice) }}</td>
                <td>
                  <span class="status-badge" :class="order.status">
                    {{ translateOrderStatus(order.status) }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="recent-panel glass-card">
        <h3>Học viên mới đăng ký</h3>
        <div class="table-responsive">
          <table class="admin-table">
            <thead>
              <tr>
                <th>Tên</th>
                <th>Email</th>
                <th>Ngày tạo</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in users.slice(-3).reverse()" :key="user.id">
                <td class="font-bold">{{ user.fullname }}</td>
                <td>{{ user.email }}</td>
                <td>{{ formatDateShort(user.createdAt) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useCourseStore } from '@/stores/courses';

const courseStore = useCourseStore();
const exportPeriod = ref('all');

const users = computed(() => courseStore.adminUsers);
const orders = computed(() => courseStore.adminOrders);
const contacts = computed(() => courseStore.adminContacts);

// Calculate total revenue from paid orders
const totalRevenue = computed(() => {
  return orders.value
    .filter(o => o.status === 'paid')
    .reduce((sum, o) => sum + o.totalPrice, 0);
});

// Helpers
const formatPrice = (value) => {
  if (value === undefined || value === null) return '0đ';
  return value.toLocaleString('vi-VN') + 'đ';
};

const formatDateShort = (dateStr) => {
  if (!dateStr) return '';
  const d = new Date(dateStr);
  return `${d.getDate()}/${d.getMonth() + 1}/${d.getFullYear()}`;
};

const translateOrderStatus = (status) => {
  switch (status) {
    case 'pending': return 'Chờ thanh toán';
    case 'paid': return 'Đã thanh toán';
    case 'cancelled': return 'Đã hủy';
    default: return status;
  }
};
</script>
