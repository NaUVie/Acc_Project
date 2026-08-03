<template>
  <div class="tab-content animate-fade-in">
    <div class="content-header flex-between">
      <div>
        <h2>Quản lý Đơn hàng</h2>
        <p>Danh sách các đơn đăng ký học và hóa đơn khóa học.</p>
      </div>
      <button @click="openAddOrderModal" class="btn btn-primary btn-sm">+ Tạo đơn hàng</button>
    </div>

    <!-- Filters -->
    <div class="filter-bar mt-4">
      <input 
        v-model="orderSearch" 
        type="text" 
        placeholder="Tìm theo mã đơn, tên học viên..." 
        class="admin-search-input"
      />
      <select v-model="orderFilterStatus" class="admin-select">
        <option value="all">Tất cả trạng thái</option>
        <option value="pending">Chờ thanh toán</option>
        <option value="paid">Đã thanh toán</option>
        <option value="cancelled">Đã hủy</option>
      </select>
    </div>

    <!-- Orders Table -->
    <div class="table-responsive mt-6">
      <table class="admin-table">
        <thead>
          <tr>
            <th>Mã đơn</th>
            <th>Học viên</th>
            <th>Sản phẩm khóa học</th>
            <th>Khấu trừ giảm giá</th>
            <th>Thành tiền</th>
            <th>Trạng thái</th>
            <th>Hành động</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="order in filteredOrders" :key="order.id">
            <td class="font-bold">#{{ order.id }}</td>
            <td>
              <div>{{ order.userFullname }}</div>
              <small class="text-muted">{{ order.userEmail }}</small>
            </td>
            <td>
              <div v-for="item in order.items" :key="item.id">• {{ item.course.title }}</div>
            </td>
            <td class="discount-price">-{{ formatPrice(order.discountApplied) }}</td>
            <td class="price-text font-bold">{{ formatPrice(order.totalPrice) }}</td>
            <td>
              <select 
                :value="order.status" 
                @change="changeOrderStatus(order.id, $event.target.value)"
                class="status-select"
                :class="order.status"
              >
                <option value="pending">Chờ thanh toán</option>
                <option value="paid">Đã thanh toán</option>
                <option value="cancelled">Đã hủy</option>
              </select>
            </td>
            <td>
              <div class="action-buttons">
                <button @click="editOrderDetails(order)" class="btn-action edit" title="Sửa chi tiết">✏️</button>
                <button @click="deleteOrder(order.id)" class="btn-action delete" title="Xóa đơn">🗑️</button>
              </div>
            </td>
          </tr>
          <tr v-if="filteredOrders.length === 0">
            <td colspan="7" class="text-center py-8 text-muted">Không tìm thấy đơn hàng nào phù hợp.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- ==================== MODAL: ADD/EDIT ORDER ==================== -->
    <div v-if="orderModalOpen" class="modal-overlay">
      <div class="modal-content glass-card">
        <h3>{{ isEditingOrder ? 'Chỉnh sửa đơn hàng' : 'Tạo đơn hàng mới' }}</h3>
        <form @submit.prevent="saveOrder" class="mt-4">
          <div class="form-group">
            <label>Học viên mua hàng</label>
            <select 
              v-model="orderForm.userId" 
              required 
              class="admin-input-style"
              @change="onOrderUserChange"
              :disabled="isEditingOrder"
            >
              <option value="" disabled>-- Chọn học viên --</option>
              <option v-for="u in users" :key="u.id" :value="u.id">
                {{ u.fullname }} ({{ u.email }})
              </option>
            </select>
          </div>

          <div class="form-group mt-3">
            <label>Chọn khóa học (Giữ Ctrl / Cmd để chọn nhiều)</label>
            <select 
              v-model="orderForm.selectedCourses" 
              multiple 
              required 
              class="admin-input-style" 
              style="height: 120px;"
              @change="autoCalculateOrderTotal"
            >
              <option v-for="c in courses" :key="c.id" :value="c">
                {{ c.title }} - {{ formatPrice(c.price) }}
              </option>
            </select>
          </div>

          <div class="grid-2 mt-3">
            <div class="form-group">
              <label>Khấu trừ giảm giá (VNĐ)</label>
              <input 
                v-model.number="orderForm.discountApplied" 
                type="number" 
                class="admin-input-style" 
                @input="autoCalculateOrderTotal" 
              />
            </div>
            <div class="form-group">
              <label>Thành tiền thực tế (VNĐ)</label>
              <input v-model.number="orderForm.totalPrice" type="number" required class="admin-input-style" />
            </div>
          </div>

          <div class="form-group mt-3">
            <label>Trạng thái thanh toán</label>
            <select v-model="orderForm.status" class="admin-input-style">
              <option value="pending">Chờ thanh toán</option>
              <option value="paid">Đã thanh toán</option>
              <option value="cancelled">Đã hủy</option>
            </select>
          </div>

          <div class="modal-actions mt-6">
            <button type="button" @click="orderModalOpen = false" class="btn btn-secondary btn-sm">Hủy</button>
            <button type="submit" class="btn btn-primary btn-sm">Lưu đơn hàng</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useCourseStore } from '@/stores/courses';

const courseStore = useCourseStore();

const users = computed(() => courseStore.adminUsers);
const orders = computed(() => courseStore.adminOrders);
const courses = computed(() => courseStore.courses);

const orderSearch = ref('');
const orderFilterStatus = ref('all');

const filteredOrders = computed(() => {
  return orders.value.filter(o => {
    const matchesSearch = o.id.toString().includes(orderSearch.value) || 
                          o.userFullname.toLowerCase().includes(orderSearch.value.toLowerCase()) ||
                          o.userEmail.toLowerCase().includes(orderSearch.value.toLowerCase());
    const matchesStatus = orderFilterStatus.value === 'all' || o.status === orderFilterStatus.value;
    return matchesSearch && matchesStatus;
  });
});

// CRUD Order Modal States
const orderModalOpen = ref(false);
const isEditingOrder = ref(false);
const editingOrderId = ref(null);
const orderForm = ref({
  userId: '',
  selectedCourses: [],
  discountApplied: 0,
  totalPrice: 0,
  status: 'pending'
});

const openAddOrderModal = () => {
  isEditingOrder.value = false;
  orderForm.value = { userId: '', selectedCourses: [], discountApplied: 0, totalPrice: 0, status: 'pending' };
  orderModalOpen.value = true;
};

const editOrderDetails = (order) => {
  isEditingOrder.value = true;
  editingOrderId.value = order.id;
  
  // Find selected courses from the catalog
  const selected = order.items.map(item => {
    return courses.value.find(c => c.id === item.course.id);
  }).filter(Boolean);

  orderForm.value = {
    userId: order.userId,
    selectedCourses: selected,
    discountApplied: order.discountApplied,
    totalPrice: order.totalPrice,
    status: order.status
  };
  orderModalOpen.value = true;
};

const onOrderUserChange = () => {
  // If user has a referrer, prefill a 10% discount
  const u = users.value.find(user => user.id === orderForm.value.userId);
  if (u && u.referredById) {
    orderForm.value.discountApplied = 1450000; // prefill standard discount
  } else {
    orderForm.value.discountApplied = 0;
  }
  autoCalculateOrderTotal();
};

const autoCalculateOrderTotal = () => {
  const sum = orderForm.value.selectedCourses.reduce((total, c) => total + c.price, 0);
  orderForm.value.totalPrice = Math.max(0, sum - (orderForm.value.discountApplied || 0));
};

const saveOrder = async () => {
  const u = users.value.find(user => user.id === orderForm.value.userId);
  if (!u) {
    alert('Vui lòng chọn học viên!');
    return;
  }
  if (orderForm.value.selectedCourses.length === 0) {
    alert('Vui lòng chọn ít nhất một khóa học!');
    return;
  }

  const orderData = {
    userId: u.id,
    selectedCourses: orderForm.value.selectedCourses,
    discountApplied: orderForm.value.discountApplied,
    totalPrice: orderForm.value.totalPrice,
    status: orderForm.value.status
  };

  try {
    if (isEditingOrder.value) {
      const payload = {
        status: orderForm.value.status,
        discount_applied: Number(orderForm.value.discountApplied) || 0,
        total_price: Number(orderForm.value.totalPrice) || 0,
        course_ids: orderForm.value.selectedCourses.map(c => c.id)
      };
      await courseStore.apiRequest(`/admin/orders/${editingOrderId.value}`, {
        method: 'PUT',
        body: JSON.stringify(payload)
      });
      await courseStore.fetchAdminOrders();
      alert('Cập nhật đơn hàng thành công!');
    } else {
      await courseStore.addAdminOrder(orderData);
      alert('Tạo đơn hàng mới thành công!');
    }
    orderModalOpen.value = false;
  } catch (err) {
    alert(err.message || 'Không thể lưu đơn hàng.');
  }
};

const deleteOrder = async (orderId) => {
  if (confirm('Bạn có chắc chắn muốn xóa đơn hàng này?')) {
    try {
      await courseStore.deleteAdminOrder(orderId);
      alert('Đã xóa đơn hàng thành công.');
    } catch (err) {
      alert(err.message || 'Không thể xóa đơn hàng.');
    }
  }
};

const changeOrderStatus = async (orderId, status) => {
  try {
    await courseStore.updateAdminOrderStatus(orderId, status);
    alert('Đã cập nhật trạng thái đơn hàng.');
  } catch (err) {
    alert(err.message || 'Không thể cập nhật trạng thái đơn hàng.');
  }
};

// Helpers
const formatPrice = (value) => {
  if (value === undefined || value === null) return '0đ';
  return value.toLocaleString('vi-VN') + 'đ';
};
</script>
