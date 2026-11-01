<template>
  <div class="tab-content animate-fade-in">
    <div class="content-header admin-overview-header">
      <div>
        <h2>Bảng điều khiển Tổng quan</h2>
        <p>Thống kê số liệu vận hành của nền tảng ACC Academy.</p>
      </div>
      <div class="admin-export-actions">
        <select v-model="exportPeriod" class="admin-select export-period-select">
          <option value="all">Tất cả thời gian</option>
          <option value="month">30 ngày qua (Tháng)</option>
          <option value="quarter">90 ngày qua (Quý)</option>
          <option value="year">365 ngày qua (Năm)</option>
        </select>
        <button @click="courseStore.exportAdminReport('orders', exportPeriod)" class="btn-export-action btn-blue">
          📊 CSV Đơn hàng
        </button>
        <button @click="courseStore.exportAdminReport('users', exportPeriod)" class="btn-export-action btn-teal">
          👥 CSV Học viên
        </button>
        <button @click="courseStore.exportAdminReport('revenue', exportPeriod)" class="btn-export-action btn-green">
          💰 Báo cáo Doanh thu
        </button>
      </div>
    </div>

    <!-- Stats Grid -->
    <div class="stats-grid">
      <div class="admin-stat-card">
        <div class="stat-info">
          <h3>Doanh thu</h3>
          <div class="stat-number">
            <span v-if="isLoading && orders.length === 0" class="stat-skeleton-pulse"></span>
            <span v-else>{{ formatPrice(totalRevenue) }}</span>
          </div>
          <p class="stat-helper">Đã đối soát thanh toán</p>
        </div>
      </div>
      <div class="admin-stat-card">
        <div class="stat-info">
          <h3>Học viên</h3>
          <div class="stat-number">
            <span v-if="isLoading && users.length === 0" class="stat-skeleton-pulse"></span>
            <span v-else>{{ users.length }}</span>
          </div>
          <p class="stat-helper">Tài khoản trên hệ thống</p>
        </div>
      </div>
      <div class="admin-stat-card">
        <div class="stat-info">
          <h3>Đơn hàng</h3>
          <div class="stat-number">
            <span v-if="isLoading && orders.length === 0" style="font-size: 18px; color: #94a3b8; font-weight: 600;">Đang nạp...</span>
            <span v-else>{{ orders.length }}</span>
          </div>
          <p class="stat-helper">{{ orders.filter(o => o.status === 'pending').length }} đơn chờ thanh toán</p>
        </div>
      </div>
      <div class="admin-stat-card">
        <div class="stat-info">
          <h3>Yêu cầu tư vấn</h3>
          <div class="stat-number">
            <span v-if="isLoading && contacts.length === 0" class="stat-skeleton-pulse"></span>
            <span v-else>{{ contacts.filter(c => !c.isResolved).length }}</span>
          </div>
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
              <tr v-if="isLoading && orders.length === 0">
                <td colspan="4">
                  <div class="admin-center-loader" style="padding: 28px 0; min-height: 120px;">
                    <div class="admin-spinner" style="width: 28px; height: 28px; border-width: 2.5px;"></div>
                    <p class="admin-loader-text" style="font-size: 13px;">Đang nạp danh sách đơn hàng...</p>
                  </div>
                </td>
              </tr>
              <tr v-else-if="orders.length === 0">
                <td colspan="4" style="text-align: center; padding: 24px; color: #94a3b8;">
                  Chưa có đơn hàng nào
                </td>
              </tr>
              <tr v-else v-for="order in orders.slice(-3).reverse()" :key="order.id">
                <td class="font-bold" data-label="Mã đơn">#{{ order.id }}</td>
                <td data-label="Khách hàng">{{ order.userFullname }}</td>
                <td class="price-text" data-label="Tổng tiền">{{ formatPrice(order.totalPrice) }}</td>
                <td data-label="Trạng thái">
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
              <tr v-if="isLoading && users.length === 0">
                <td colspan="3">
                  <div class="admin-center-loader" style="padding: 28px 0; min-height: 120px;">
                    <div class="admin-spinner" style="width: 28px; height: 28px; border-width: 2.5px;"></div>
                    <p class="admin-loader-text" style="font-size: 13px;">Đang nạp danh sách học viên...</p>
                  </div>
                </td>
              </tr>
              <tr v-else-if="users.length === 0">
                <td colspan="3" style="text-align: center; padding: 24px; color: #94a3b8;">
                  Chưa có học viên nào
                </td>
              </tr>
              <tr v-else v-for="user in users.slice(-3).reverse()" :key="user.id">
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
import { ref, computed, onMounted } from 'vue';
import { useCourseStore } from '@/stores/courses';

const courseStore = useCourseStore();
const exportPeriod = ref('all');

const users = computed(() => courseStore.adminUsers || []);
const orders = computed(() => courseStore.adminOrders || []);
const contacts = computed(() => courseStore.adminContacts || []);

const isLoading = ref(orders.value.length === 0 && users.value.length === 0);

onMounted(async () => {
  if (orders.value.length === 0 && users.value.length === 0) {
    isLoading.value = true;
  }
  try {
    await Promise.all([
      courseStore.fetchAdminUsers().catch(err => console.warn('fetchAdminUsers failed:', err)),
      courseStore.fetchAdminOrders().catch(err => console.warn('fetchAdminOrders failed:', err)),
      courseStore.fetchAdminContacts().catch(err => console.warn('fetchAdminContacts failed:', err))
    ]);
  } finally {
    isLoading.value = false;
  }
});

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
