<template>
  <div class="login-view container">
    <div class="dashboard-wrapper animate-fade-in">
      <!-- Welcome Header -->
      <div class="dashboard-header glass-card">
        <div class="user-intro">
          <div class="user-avatar-initials">
            {{ getUserInitials(courseStore.userMe?.fullname) }}
          </div>
          <div>
            <h1>Xin chào, <span class="gradient-text">{{ courseStore.userMe?.fullname }}</span>!</h1>
            <p>Học viên ACC Academy • Lớp: {{ courseStore.userMe?.role === 'admin' ? 'Quản trị viên' : 'Lớp tiêu chuẩn' }}</p>
          </div>
        </div>
        <button @click="handleLogout" class="btn btn-outline btn-sm btn-danger">
          Đăng xuất
        </button>
      </div>

      <div class="dashboard-grid">
        <!-- LEFT PANEL: PROFILE & REFERRAL CENTER -->
        <div class="dashboard-column referral-center">
          <!-- Student Profile Card -->
          <div class="panel-card glass-card profile-info-card mb-6">
            <div class="profile-header-row">
              <h2 class="panel-title">👤 Thông tin Hồ sơ Học viên</h2>
              <button @click="openEditModal" class="btn btn-outline btn-sm" style="border-radius: 20px; padding: 6px 14px; font-size: 13px;">
                ✏️ Chỉnh sửa hồ sơ
              </button>
            </div>
            
            <div class="profile-details-grid">
              <div class="profile-detail-item">
                <span class="detail-label">Họ và tên</span>
                <span class="detail-value">{{ courseStore.userMe?.fullname }}</span>
              </div>
              <div class="profile-detail-item">
                <span class="detail-label">Email tài khoản</span>
                <span class="detail-value">{{ courseStore.userMe?.email }}</span>
              </div>
              <div class="profile-detail-item">
                <span class="detail-label">Vai trò hệ thống</span>
                <span class="detail-value">{{ courseStore.userMe?.role === 'admin' ? '👑 Quản trị viên' : '🎓 Học viên' }}</span>
              </div>
              <div class="profile-detail-item">
                <span class="detail-label">Ngày tham gia</span>
                <span class="detail-value">{{ formatDate(courseStore.userMe?.createdAt) }}</span>
              </div>
            </div>
          </div>

          <div class="panel-card glass-card">
            <h2 class="panel-title">🎁 Chương trình Lan tỏa & Nhận quà</h2>
            <p class="panel-subtitle">Chia sẻ mã giới thiệu của bạn để bạn bè nhận ưu đãi học phí cao nhất lên tới 14,5 triệu VND, và nhận hoa hồng lên tới 29 triệu VND khi họ thanh toán thành công.</p>
            
            <!-- Referral Code Display -->
            <div class="referral-link-box">
              <div class="link-label">Mã giới thiệu của bạn:</div>
              <div class="code-badge">{{ referralSummary?.referralCode || 'Đang tạo...' }}</div>
              
              <div class="link-label mt-4">Đường dẫn giới thiệu trực tiếp:</div>
              <div class="link-input-group">
                <input 
                  type="text" 
                  readonly 
                  :value="getReferralLink(referralSummary?.referralCode)" 
                  ref="refLinkInput"
                  class="link-input"
                />
                <button @click="copyReferralLink" class="btn btn-primary btn-sm">
                  {{ copied ? 'Đã chép!' : 'Sao chép' }}
                </button>
              </div>
            </div>

            <!-- Reward Summary Cards -->
            <div class="stats-cards-grid">
              <div class="stat-card">
                <div class="stat-num">{{ referralSummary?.totalReferrals || 0 }}</div>
                <div class="stat-label">Bạn bè nhập học</div>
              </div>
              <div class="stat-card highlighted">
                <div class="stat-num">{{ formatPrice(referralSummary?.totalCommissionEarned || 0) }}</div>
                <div class="stat-label">Hoa hồng nhận được</div>
              </div>
            </div>

            <!-- Referred Friends Table -->
            <div class="friends-list-section">
              <h3>Danh sách bạn bè đã giới thiệu</h3>
              <div v-if="!referralSummary?.referralsList || referralSummary.referralsList.length === 0" class="empty-state">
                Chưa có bạn bè nào đăng ký tài khoản qua liên kết của bạn. Hãy gửi link cho họ nhé!
              </div>
              <div v-else class="table-container">
                <table class="friends-table">
                  <thead>
                    <tr>
                      <th>Tên bạn bè</th>
                      <th>Ngày tham gia</th>
                      <th>Hoa hồng</th>
                      <th>Trạng thái</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="ref in referralSummary.referralsList" :key="ref.id">
                      <td class="font-bold">{{ ref.referredFullname }}</td>
                      <td>{{ formatDate(ref.createdAt) }}</td>
                      <td class="price-text">{{ formatPrice(ref.commissionAmount) }}</td>
                      <td>
                        <span class="status-badge" :class="ref.status">
                          {{ ref.status === 'completed' ? 'Thành công' : 'Đang xử lý' }}
                        </span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

        <!-- RIGHT PANEL: CART & ORDER HISTORY -->
        <div class="dashboard-column shop-center">
          <!-- My Purchased Courses Section -->
          <div class="panel-card glass-card mb-6">
            <h2 class="panel-title">📚 Khóa học của tôi (Đã mua)</h2>
            
            <div v-if="purchasedCourses.length === 0" class="empty-state py-8">
              <p>Bạn chưa sở hữu khóa học nào.</p>
              <router-link to="/courses/ai" class="btn btn-outline btn-sm mt-3 inline-block">Khám phá các khóa học</router-link>
            </div>
            
            <div v-else class="purchased-courses-list">
              <div v-for="course in purchasedCourses" :key="course.id" class="purchased-course-row">
                <img :src="course.image" :alt="course.title" class="purchased-course-img" />
                <div class="purchased-course-info">
                  <h4>{{ course.title }}</h4>
                  <p class="text-xs text-muted" style="margin-top: 2px; color: var(--text-muted);">Thời lượng: {{ course.duration || '12 tuần' }} • Trình độ: {{ course.level || 'Trung cấp' }}</p>
                </div>
                <router-link :to="'/courses/' + course.handle + '/study'" class="btn btn-primary btn-sm" style="padding: 6px 12px; font-size: 12px; border-radius: var(--radius-sm); border: none;">
                  Vào học
                </router-link>
              </div>
            </div>
          </div>

          <!-- Shopping Cart Section -->
          <div class="panel-card glass-card mb-6">
            <h2 class="panel-title">🛒 Giỏ hàng của bạn ({{ courseStore.cart.length }})</h2>
            
            <div v-if="courseStore.cart.length === 0" class="empty-state py-8">
              <p>Giỏ hàng trống.</p>
              <router-link to="/courses/ai" class="btn btn-outline btn-sm mt-3 inline-block">Khám phá các khóa học</router-link>
            </div>
            
            <div v-else class="cart-items-list">
              <div v-for="item in courseStore.cart" :key="item.id" class="cart-item-row">
                <img :src="item.course.image" :alt="item.course.title" class="cart-item-img" />
                <div class="cart-item-info">
                  <h4>{{ item.course.title }}</h4>
                  <div class="price">{{ formatPrice(item.course.price) }}</div>
                </div>
                <button @click="handleRemoveFromCart(item.course.id)" class="remove-btn" title="Xóa khỏi giỏ hàng">
                  🗑️
                </button>
              </div>

              <!-- Checkout discount indicator -->
              <div class="checkout-summary-box">
                <div class="summary-row" v-if="hasReferralDiscount">
                  <span>Giảm giá giới thiệu (10%):</span>
                  <span class="discount-price">- {{ formatPrice(calculatedDiscount) }}</span>
                </div>
                <div class="summary-row total-row">
                  <span>Tổng tiền thanh toán:</span>
                  <span class="total-price">{{ formatPrice(calculatedTotal) }}</span>
                </div>
                
                <button @click="handleCheckout" class="btn btn-primary w-full mt-4" :disabled="loading">
                  {{ loading ? 'Đang tạo đơn hàng...' : 'Xác nhận Đặt hàng & Nhận ưu đãi' }}
                </button>
              </div>
            </div>
          </div>

          <!-- Order History Section -->
          <div class="panel-card glass-card">
            <h2 class="panel-title">📋 Lịch sử đơn hàng & Thanh toán</h2>
            
            <div v-if="orders.length === 0" class="empty-state py-8">
              Chưa có đơn hàng nào được tạo.
            </div>
            
            <div v-else class="orders-list">
              <div v-for="order in orders" :key="order.id" class="order-card">
                <div class="order-header">
                  <div>
                    <span class="order-id">Đơn hàng #{{ order.id }}</span>
                    <span class="order-date">{{ formatDate(order.createdAt) }}</span>
                  </div>
                  <span class="status-badge" :class="order.status">
                    {{ translateOrderStatus(order.status) }}
                  </span>
                </div>
                
                <!-- Items list in this order -->
                <div class="order-items mt-3">
                  <div v-for="item in order.items" :key="item.id" class="order-item-detail">
                    <span>• {{ item.course.title }}</span>
                    <span>{{ formatPrice(item.price) }}</span>
                  </div>
                </div>

                <div class="order-footer mt-4">
                  <div class="discount-row" v-if="order.discountApplied > 0">
                    Đã giảm giá: -{{ formatPrice(order.discountApplied) }}
                  </div>
                  <div class="total-row">
                    Tổng cộng: <span class="price">{{ formatPrice(order.totalPrice) }}</span>
                  </div>
                  
                  <!-- Pay Simulator Button -->
                  <button 
                    v-if="order.status === 'pending'" 
                    @click="handlePayOrder(order.id)" 
                    class="btn btn-outline btn-sm btn-success w-full mt-3"
                    :disabled="loading"
                  >
                    🏦 Giả lập Thanh toán (VNPay / MoMo)
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Profile Modal -->
    <div v-if="showEditModal" class="modal-overlay" @click.self="showEditModal = false">
      <div class="modal-content animate-fade-in">
        <div class="modal-header">
          <h3 class="modal-title">✏️ Cập nhật Hồ sơ Học viên</h3>
          <button @click="showEditModal = false" class="remove-btn" style="color: white; font-size: 20px;">✕</button>
        </div>
        
        <form @submit.prevent="handleSaveProfile">
          <div class="form-group">
            <label>Họ và tên học viên</label>
            <input 
              type="text" 
              v-model="editFullname" 
              class="form-control" 
              placeholder="Nhập họ và tên đầy đủ..." 
              required 
            />
          </div>
          
          <div class="form-group">
            <label>Mật khẩu mới (Để trống nếu không muốn đổi)</label>
            <input 
              type="password" 
              v-model="editPassword" 
              class="form-control" 
              placeholder="Nhập mật khẩu mới (tối thiểu 6 ký tự)..." 
            />
          </div>

          <div class="modal-actions">
            <button type="button" @click="showEditModal = false" class="btn btn-outline btn-sm">
              Hủy bỏ
            </button>
            <button type="submit" class="btn btn-primary btn-sm" :disabled="savingProfile">
              {{ savingProfile ? 'Đang lưu...' : 'Lưu thay đổi' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useCourseStore } from '@/stores/courses';

// Import separated stylesheet
import '@/styles/dashboard.css';

const router = useRouter();
const courseStore = useCourseStore();

const loading = ref(false);
const copied = ref(false);

// Edit profile reactive state
const showEditModal = ref(false);
const editFullname = ref('');
const editPassword = ref('');
const savingProfile = ref(false);

const openEditModal = () => {
  editFullname.value = courseStore.userMe?.fullname || '';
  editPassword.value = '';
  showEditModal.value = true;
};

const handleSaveProfile = async () => {
  if (!editFullname.value.trim()) {
    alert('Vui lòng nhập họ và tên!');
    return;
  }
  savingProfile.value = true;
  try {
    const payload = { fullname: editFullname.value.trim() };
    if (editPassword.value.trim()) {
      payload.password = editPassword.value.trim();
    }
    await courseStore.updateProfile(payload);
    alert('Cập nhật thông tin học viên thành công!');
    showEditModal.value = false;
  } catch (err) {
    alert('Lỗi cập nhật hồ sơ: ' + err.message);
  } finally {
    savingProfile.value = false;
  }
};

// Reactively bind referrals and orders from store state
const referralSummary = computed(() => courseStore.referralSummary);
const orders = computed(() => courseStore.orders);

const purchasedCourses = computed(() => {
  const list = [];
  const seen = new Set();
  orders.value.forEach(order => {
    if (order.status === 'paid') {
      order.items.forEach(item => {
        if (item.course && !seen.has(item.course.id)) {
          seen.add(item.course.id);
          list.push(item.course);
        }
      });
    }
  });
  return list;
});

onMounted(async () => {
  if (!courseStore.token) {
    alert('Vui lòng đăng nhập để truy cập Dashboard!');
    router.push('/login');
    return;
  }
  
  await refreshDashboardData();
});

// Refresh dashboard data
const refreshDashboardData = async () => {
  try {
    await courseStore.fetchUserMe();
    await courseStore.fetchCart();
    await courseStore.fetchReferrals();
    await courseStore.fetchOrders();
  } catch (err) {
    console.error("Dashboard refresh error:", err);
  }
};

// Calculations for active checkout
const hasReferralDiscount = computed(() => {
  // If the user has a referrer, they get a 10% discount on their first checkout
  const isFirstPurchase = orders.value.filter(o => o.status === 'paid').length === 0;
  return courseStore.userMe?.referredById && isFirstPurchase;
});

const calculatedDiscount = computed(() => {
  if (!hasReferralDiscount.value) return 0;
  const standardTotal = courseStore.cart.reduce((sum, item) => sum + item.course.price, 0);
  const discount = Math.floor(standardTotal * 0.10);
  return Math.min(discount, 14500000); // capped at 14,500,000 VND
});

const calculatedTotal = computed(() => {
  const standardTotal = courseStore.cart.reduce((sum, item) => sum + item.course.price, 0);
  return standardTotal - calculatedDiscount.value;
});

const handleLogout = () => {
  courseStore.logout();
  alert('Đã đăng xuất khỏi tài khoản.');
  router.push('/login');
};

// Shopping cart actions
const handleRemoveFromCart = async (courseId) => {
  try {
    await courseStore.removeFromCart(courseId);
  } catch (err) {
    alert('Không thể xóa khóa học: ' + err.message);
  }
};

const handleCheckout = async () => {
  loading.value = true;
  try {
    await courseStore.checkout();
    alert('Đơn hàng đã được tạo thành công! Hãy bấm Thanh toán giả lập bên dưới để kích hoạt đơn hàng.');
    await refreshDashboardData();
  } catch (err) {
    alert('Đơn hàng lỗi: ' + err.message);
  } finally {
    loading.value = false;
  }
};

const handlePayOrder = async (orderId) => {
  loading.value = true;
  try {
    await courseStore.payOrder(orderId);
    alert('Thanh toán giả lập thành công! Người giới thiệu bạn đã nhận được hoa hồng trực tiếp.');
    await refreshDashboardData();
  } catch (err) {
    alert('Lỗi thanh toán: ' + err.message);
  } finally {
    loading.value = false;
  }
};

// Helpers
const getReferralLink = (code) => {
  if (!code) return '';
  const port = window.location.port ? `:${window.location.port}` : '';
  return `${window.location.protocol}//${window.location.hostname}${port}/#/register?ref=${code}`;
};

const copyReferralLink = () => {
  const link = getReferralLink(referralSummary.value?.referralCode);
  if (!link) return;
  navigator.clipboard.writeText(link);
  copied.value = true;
  setTimeout(() => copied.value = false, 2000);
};

const formatPrice = (value) => {
  if (value === undefined || value === null) return '0đ';
  return value.toLocaleString('vi-VN') + 'đ';
};

const formatDate = (dateStr) => {
  if (!dateStr) return '';
  const d = new Date(dateStr);
  return `${d.getDate()}/${d.getMonth() + 1}/${d.getFullYear()} ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`;
};

const getUserInitials = (name) => {
  if (!name) return 'HV';
  const parts = name.trim().split(' ');
  if (parts.length === 1) return parts[0].substring(0, 2).toUpperCase();
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
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
