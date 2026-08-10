<template>
  <div class="login-view container">
    <div class="dashboard-sidebar-layout animate-fade-in">
      
      <!-- LEFT SIDEBAR NAV -->
      <aside class="dashboard-sidebar glass-card">
        <div class="sidebar-user-header">
          <div class="user-avatar-initials">
            {{ getUserInitials(courseStore.userMe?.fullname) }}
          </div>
          <div class="user-info-text">
            <h3 class="user-name">{{ courseStore.userMe?.fullname || 'Học viên' }}</h3>
            <span class="user-role-label">{{ courseStore.userMe?.role === 'admin' ? '👑 Quản trị viên' : '🎓 Học viên ACC' }}</span>
          </div>
        </div>

        <div class="sidebar-divider"></div>

        <nav class="sidebar-nav-list">
          <button 
            class="sidebar-nav-item" 
            :class="{ active: activeTab === 'courses' }"
            @click="activeTab = 'courses'"
          >
            <span class="tab-icon">📚</span>
            <span class="tab-label">Khóa học của tôi</span>
            <span class="tab-badge" v-if="purchasedCourses.length > 0">{{ purchasedCourses.length }}</span>
          </button>

          <button 
            class="sidebar-nav-item" 
            :class="{ active: activeTab === 'profile' }"
            @click="activeTab = 'profile'"
          >
            <span class="tab-icon">👤</span>
            <span class="tab-label">Hồ sơ cá nhân</span>
          </button>

          <button 
            class="sidebar-nav-item" 
            :class="{ active: activeTab === 'referral' }"
            @click="activeTab = 'referral'"
          >
            <span class="tab-icon">🎁</span>
            <span class="tab-label">Lan tỏa & Nhận quà</span>
          </button>

          <button 
            class="sidebar-nav-item" 
            :class="{ active: activeTab === 'cart' }"
            @click="activeTab = 'cart'"
          >
            <span class="tab-icon">🛒</span>
            <span class="tab-label">Giỏ hàng</span>
            <span class="tab-badge" v-if="courseStore.cart.length > 0">{{ courseStore.cart.length }}</span>
          </button>

          <button 
            class="sidebar-nav-item" 
            :class="{ active: activeTab === 'wishlist' }"
            @click="activeTab = 'wishlist'"
          >
            <span class="tab-icon">❤️</span>
            <span class="tab-label">Yêu thích</span>
            <span class="tab-badge" v-if="courseStore.wishlist.length > 0">{{ courseStore.wishlist.length }}</span>
          </button>

          <button 
            class="sidebar-nav-item" 
            :class="{ active: activeTab === 'orders' }"
            @click="activeTab = 'orders'"
          >
            <span class="tab-icon">📋</span>
            <span class="tab-label">Lịch sử đơn hàng</span>
            <span class="tab-badge" v-if="orders.length > 0">{{ orders.length }}</span>
          </button>
        </nav>

        <div class="sidebar-footer">
          <button @click="handleLogout" class="sidebar-logout-btn">
            <span>🚪</span> Đăng xuất tài khoản
          </button>
        </div>
      </aside>

      <!-- RIGHT MAIN CONTENT AREA -->
      <main class="dashboard-main-content">

      <!-- TAB 1: COURSES -->
      <div v-show="activeTab === 'courses'" class="tab-pane animate-fade-in">
        <div class="panel-card glass-card">
          <div class="section-title-row">
            <h2 class="panel-title">📚 Khóa học của tôi ({{ filteredPurchasedCourses.length }})</h2>
            
            <div class="courses-filter-bar">
              <select v-model="courseCategoryFilter" class="category-select-control">
                <option v-for="cat in availableCourseCategories" :key="cat.value" :value="cat.value">
                  {{ cat.label }}
                </option>
              </select>

              <div class="search-input-wrapper">
                <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="11" cy="11" r="8"/>
                  <path d="M21 21l-4.35-4.35"/>
                </svg>
                <input 
                  type="text" 
                  v-model="courseSearchQuery" 
                  placeholder="Tìm khóa học của bạn..." 
                  class="search-control"
                />
                <button v-if="courseSearchQuery" @click="courseSearchQuery = ''" class="clear-search-btn">✕</button>
              </div>
              <router-link to="/courses/ai" class="btn btn-outline btn-sm" style="font-size: 13px;">+ Khám phá mới</router-link>
            </div>
          </div>
          
          <div v-if="purchasedCourses.length === 0" class="empty-state py-12">
            <div style="font-size: 40px; margin-bottom: 12px;">🎓</div>
            <p style="font-size: 15px; font-weight: 600; color: #0f172a;">Bạn chưa sở hữu khóa học nào.</p>
            <p style="font-size: 13px; color: #64748b; margin-top: 4px;">Hãy tham gia ngay các khóa học AI & Kỹ năng tại ACC Academy!</p>
            <router-link to="/courses/ai" class="btn btn-primary btn-sm mt-4 inline-block">Khám phá các khóa học</router-link>
          </div>

          <div v-else-if="filteredPurchasedCourses.length === 0" class="empty-state py-12">
            <div style="font-size: 36px; margin-bottom: 8px;">🔍</div>
            <p style="font-size: 15px; font-weight: 600; color: #0f172a;">Không tìm thấy khóa học nào khớp với bộ lọc hiện tại.</p>
            <button @click="courseSearchQuery = ''; courseCategoryFilter = 'all'" class="btn btn-outline btn-sm mt-3">Xóa bộ lọc</button>
          </div>
          
          <div v-else>
            <div class="purchased-courses-grid">
              <div v-for="course in paginatedPurchasedCourses" :key="course.id" class="purchased-course-card glass-card">
                <img :src="course.image" :alt="course.title" class="purchased-card-img" />
                <div class="purchased-card-body">
                  <h4>{{ course.title }}</h4>
                  <p class="course-meta">Thời lượng: {{ course.duration || '12 tuần' }} • Trình độ: {{ course.level || 'Trung cấp' }}</p>
                  <div class="card-action-row">
                    <router-link :to="'/courses/' + course.handle + '/study'" class="btn btn-primary btn-sm w-full">
                      🚀 Vào lớp học ngay
                    </router-link>
                  </div>
                </div>
              </div>
            </div>

            <!-- Pagination Controls -->
            <div v-if="totalCoursePages > 1" class="pagination-wrapper">
              <button 
                class="page-btn prev-btn" 
                :disabled="coursePage === 1" 
                @click="coursePage--"
              >
                ‹ Trước
              </button>
              <div class="page-numbers">
                <button 
                  v-for="p in totalCoursePages" 
                  :key="p" 
                  class="page-num-btn" 
                  :class="{ active: coursePage === p }"
                  @click="coursePage = p"
                >
                  {{ p }}
                </button>
              </div>
              <button 
                class="page-btn next-btn" 
                :disabled="coursePage === totalCoursePages" 
                @click="coursePage++"
              >
                Sau ›
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- TAB 2: PROFILE -->
      <div v-show="activeTab === 'profile'" class="tab-pane animate-fade-in">
        <div class="panel-card glass-card profile-info-card">
          <div class="profile-header-row">
            <h2 class="panel-title">👤 Thông tin Hồ sơ Học viên</h2>
            <button @click="openEditModal" class="btn btn-outline btn-sm" style="border-radius: 20px; padding: 6px 16px; font-size: 13px;">
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
      </div>

      <!-- TAB 3: REFERRAL -->
      <div v-show="activeTab === 'referral'" class="tab-pane animate-fade-in">
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
              <div class="stat-label">Bạn bè giới thiệu</div>
            </div>
            <div class="stat-card highlighted">
              <div class="stat-num">{{ formatPrice(referralSummary?.totalCommissionEarned || 0) }}</div>
              <div class="stat-label">Hoa hồng nhận được</div>
            </div>
            <div class="stat-card" style="border: 1px solid #bbf7d0; background: #f0fdf4;">
              <div class="stat-num" style="color: #16a34a;">{{ formatPrice(courseStore.userMe?.storeCreditBalance || referralSummary?.storeCreditBalance || 0) }}</div>
              <div class="stat-label" style="color: #15803d; font-weight: 700;">Ví giảm giá khả dụng</div>
            </div>
          </div>

          <!-- Referred Friends Table -->
          <div class="friends-list-section">
            <h3>Danh sách bạn bè đã giới thiệu</h3>
            <div v-if="!referralSummary?.referralsList || referralSummary.referralsList.length === 0" class="empty-state py-6">
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
                        {{ ref.status === 'completed' ? 'Đã nhập học (Thành công)' : 'Đã đăng ký (Chờ nhập học)' }}
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- TAB 4: CART -->
      <div v-show="activeTab === 'cart'" class="tab-pane animate-fade-in">
        <div class="panel-card glass-card">
          <h2 class="panel-title">🛒 Giỏ hàng của bạn ({{ courseStore.cart.length }})</h2>
          
          <div v-if="courseStore.cart.length === 0" class="empty-state py-12">
            <div style="font-size: 40px; margin-bottom: 12px;">🛒</div>
            <p style="font-size: 15px; font-weight: 600; color: #0f172a;">Giỏ hàng của bạn đang trống.</p>
            <router-link to="/courses/ai" class="btn btn-primary btn-sm mt-4 inline-block">Khám phá các khóa học</router-link>
          </div>
          
          <div v-else class="cart-tab-wrapper">
            <div class="cart-items-list">
              <div v-for="item in courseStore.cart" :key="item.id" class="cart-item-row">
                <img :src="item.course.image" :alt="item.course.title" class="cart-item-img" />
                <div class="cart-item-info">
                  <h4>{{ item.course.title }}</h4>
                  <div class="price">{{ formatPrice(item.course.price) }}</div>
                </div>
                <button @click="handleRemoveFromCart(item.course.id)" class="remove-btn" title="Xóa khỏi giỏ hàng">
                  🗑️ Xóa
                </button>
              </div>
            </div>

            <!-- Checkout discount indicator -->
            <div class="checkout-summary-box mt-6">
              <div class="summary-row" v-if="hasReferralDiscount">
                <span>Giảm giá giới thiệu (10%):</span>
                <span class="discount-price">- {{ formatPrice(calculatedDiscount) }}</span>
              </div>
              <div class="summary-row total-row">
                <span>Tổng tiền thanh toán:</span>
                <span class="total-price">{{ formatPrice(calculatedTotal) }}</span>
              </div>
              
              <button @click="handleCheckout" class="btn btn-primary w-full mt-4" :disabled="loading">
                {{ loading ? 'Đang tạo đơn hàng...' : '⚡ Xác nhận Đặt hàng & Nhận ưu đãi' }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- TAB 5: WISHLIST -->
      <div v-show="activeTab === 'wishlist'" class="tab-pane animate-fade-in">
        <div class="panel-card glass-card">
          <h2 class="panel-title">❤️ Danh sách Khóa học Yêu thích ({{ courseStore.wishlist.length }})</h2>
          
          <div v-if="courseStore.wishlist.length === 0" class="empty-state py-12">
            <div style="font-size: 40px; margin-bottom: 12px;">❤️</div>
            <p style="font-size: 15px; font-weight: 600; color: #0f172a;">Danh sách yêu thích của bạn đang trống.</p>
            <p style="font-size: 13px; color: #64748b; margin-top: 4px;">Hãy nhấn biểu tượng trái tim ở trang chi tiết khóa học để lưu lại xem sau!</p>
            <router-link to="/courses/ai" class="btn btn-primary btn-sm mt-4 inline-block">Khám phá các khóa học</router-link>
          </div>
          
          <div v-else class="purchased-courses-grid">
            <div v-for="item in courseStore.wishlist" :key="item.id" class="purchased-course-card glass-card">
              <img :src="item.course?.image || '/images/default.jpg'" :alt="item.course?.title" class="purchased-card-img" />
              <div class="purchased-card-body">
                <h4>{{ item.course?.title }}</h4>
                <p class="course-meta">Giá bán: <strong style="color: #0284c7;">{{ formatPrice(item.course?.price) }}</strong></p>
                <div class="card-action-row" style="display: flex; gap: 8px; margin-top: 12px;">
                  <router-link :to="'/course/' + item.course?.handle" class="btn btn-primary btn-sm" style="flex: 1; text-align: center;">
                    Xem chi tiết
                  </router-link>
                  <button @click="handleRemoveWishlist(item.course?.id)" class="btn btn-outline btn-sm btn-danger" title="Xóa khỏi wishlist">
                    🗑️ Bỏ lưu
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- TAB 6: ORDERS -->
      <div v-show="activeTab === 'orders'" class="tab-pane animate-fade-in">
        <div class="panel-card glass-card">
          <h2 class="panel-title">📋 Lịch sử đơn hàng & Thanh toán</h2>
          
          <div v-if="orders.length === 0" class="empty-state py-12">
            <div style="font-size: 40px; margin-bottom: 12px;">📋</div>
            <p style="font-size: 15px; font-weight: 600; color: #0f172a;">Chưa có đơn hàng nào được tạo.</p>
          </div>
          
          <div v-else class="orders-list">
            <div v-for="order in orders" :key="order.id" class="order-card">
              <div class="order-header">
                <div>
                  <span class="order-id">Đơn hàng #{{ String(order.id).padStart(6, '0') }}</span>
                  <span class="order-date">{{ formatDate(order.createdAt) }}</span>
                </div>
                <span class="status-badge" :class="order.status">
                  {{ translateOrderStatus(order.status) }}
                </span>
              </div>
              
              <!-- Items list in this order -->
              <div class="order-items mt-3">
                <div v-for="item in order.items" :key="item.id" class="order-item-detail">
                  <span class="order-item-title">• {{ item.course?.title || 'Khóa học ACC' }}</span>
                  <span style="font-weight: 600;">{{ formatPrice(item.price) }}</span>
                </div>
              </div>

              <div class="order-footer mt-4">
                <div class="discount-row" v-if="order.discountApplied > 0">
                  Đã giảm giá: -{{ formatPrice(order.discountApplied) }}
                </div>
                <div class="total-row">
                  Tổng cộng: <span class="price">{{ formatPrice(order.totalPrice) }}</span>
                </div>
                
                <!-- Actions Row -->
                <div style="display: flex; gap: 8px; margin-top: 12px;">
                  <router-link
                    :to="`/order/${order.id}`"
                    class="btn btn-outline btn-sm"
                    style="flex: 1; text-align: center; padding: 8px 12px; font-size: 13px;"
                  >
                    📋 Xem chi tiết
                  </router-link>
                  <button 
                    v-if="order.status === 'pending'" 
                    @click="handlePayOrder(order.id)" 
                    class="btn btn-outline btn-sm btn-success"
                    :disabled="loading"
                    style="flex: 1;"
                  >
                    🏦 Thanh toán (Demo)
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      </main>
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
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useCourseStore } from '@/stores/courses';

// Import separated stylesheet
import '@/styles/dashboard.css';

const router = useRouter();
const route = useRoute();
const courseStore = useCourseStore();

const activeTab = ref(route.query.tab || 'courses');

watch(() => route.query.tab, (newTab) => {
  if (newTab) {
    activeTab.value = newTab;
  }
});

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
    courseStore.showToast('Vui lòng nhập họ và tên!', 'warning');
    return;
  }
  savingProfile.value = true;
  try {
    const payload = { fullname: editFullname.value.trim() };
    if (editPassword.value.trim()) {
      payload.password = editPassword.value.trim();
    }
    await courseStore.updateProfile(payload);
    courseStore.showToast('Cập nhật thông tin học viên thành công!', 'success');
    showEditModal.value = false;
  } catch (err) {
    courseStore.showToast('Lỗi cập nhật hồ sơ: ' + err.message, 'error');
  } finally {
    savingProfile.value = false;
  }
};

// Reactively bind referrals and orders from store state
const referralSummary = computed(() => courseStore.referralSummary);
const orders = computed(() => courseStore.orders);

const purchasedCourses = computed(() => {
  // Prefer enrollments data (direct from backend)
  if (courseStore.enrollments && courseStore.enrollments.length > 0) {
    return courseStore.enrollments.map(e => e.course).filter(Boolean);
  }
  // Fallback: derive from paid orders
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

// Search, Category Filtering & Pagination for My Courses
const courseSearchQuery = ref('');
const courseCategoryFilter = ref('all');
const coursePage = ref(1);
const courseItemsPerPage = 8;

watch([courseSearchQuery, courseCategoryFilter], () => {
  coursePage.value = 1;
});

const availableCourseCategories = computed(() => {
  const catSet = new Map();
  catSet.set('all', 'Tất cả danh mục');
  
  purchasedCourses.value.forEach(c => {
    const slug = c.category_slug || c.category;
    if (slug && !catSet.has(slug)) {
      let label = slug;
      if (slug === 'ky-nang-ai') label = 'Kỹ năng AI';
      else if (slug === 'ky-nang-chuyen-mon') label = 'Chuyên môn & Dữ liệu';
      else if (slug === 'ky-nang-mem') label = 'Kỹ năng mềm';
      else if (slug === 'bundles') label = 'Gói Combo';
      else label = slug.charAt(0).toUpperCase() + slug.slice(1);
      
      catSet.set(slug, label);
    }
  });
  
  return Array.from(catSet.entries()).map(([value, label]) => ({ value, label }));
});

const filteredPurchasedCourses = computed(() => {
  const q = courseSearchQuery.value.trim().toLowerCase();
  const cat = courseCategoryFilter.value;

  return purchasedCourses.value.filter(c => {
    const cCat = c.category_slug || c.category;
    const catMatch = cat === 'all' || cCat === cat;

    if (!catMatch) return false;
    if (!q) return true;

    const titleMatch = (c.title || '').toLowerCase().includes(q);
    const categoryTextMatch = (cCat || '').toLowerCase().includes(q);
    const descMatch = (c.description || '').toLowerCase().includes(q);
    return titleMatch || categoryTextMatch || descMatch;
  });
});

const totalCoursePages = computed(() => {
  return Math.ceil(filteredPurchasedCourses.value.length / courseItemsPerPage) || 1;
});

const paginatedPurchasedCourses = computed(() => {
  const start = (coursePage.value - 1) * courseItemsPerPage;
  return filteredPurchasedCourses.value.slice(start, start + courseItemsPerPage);
});

onMounted(async () => {
  if (!courseStore.token) {
    courseStore.showToast('Vui lòng đăng nhập để truy cập Dashboard!', 'warning');
    router.push('/login');
    return;
  }
  
  refreshDashboardData();
});

// Refresh dashboard data in parallel for instant UI responsiveness
const refreshDashboardData = async () => {
  try {
    const promises = [
      courseStore.fetchUserMe(),
      courseStore.fetchCart(),
      courseStore.fetchReferrals(),
      courseStore.fetchOrders(),
      courseStore.fetchEnrollments(),
      courseStore.fetchWishlist()
    ];
    if (courseStore.courses.length === 0) {
      promises.push(courseStore.fetchCourses());
    }
    await Promise.all(promises);
  } catch (err) {
    console.error("Dashboard refresh error:", err);
  }
};

const handleRemoveWishlist = async (courseId) => {
  if (!courseId) return;
  await courseStore.toggleWishlist(courseId);
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
  courseStore.showToast('Đã đăng xuất khỏi tài khoản.', 'info');
  router.push('/login');
};

// Shopping cart actions
const handleRemoveFromCart = async (courseId) => {
  try {
    await courseStore.removeFromCart(courseId);
  } catch (err) {
    courseStore.showToast('Không thể xóa khóa học: ' + err.message, 'error');
  }
};

const handleCheckout = async () => {
  loading.value = true;
  try {
    await courseStore.checkout();
    courseStore.showToast('Đơn hàng đã được tạo thành công!', 'success');
    await refreshDashboardData();
  } catch (err) {
    courseStore.showToast('Đơn hàng lỗi: ' + err.message, 'error');
  } finally {
    loading.value = false;
  }
};

const handlePayOrder = async (orderId) => {
  loading.value = true;
  try {
    await courseStore.payOrder(orderId);
    courseStore.showToast('Thanh toán giả lập thành công! Khóa học đã được kích hoạt.', 'success');
    await refreshDashboardData();
  } catch (err) {
    courseStore.showToast('Lỗi thanh toán: ' + err.message, 'error');
  } finally {
    loading.value = false;
  }
};

// Helpers
const getReferralLink = (code) => {
  if (!code) return '';
  const port = window.location.port ? `:${window.location.port}` : '';
  return `${window.location.protocol}//${window.location.hostname}${port}/register?ref=${code}`;
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
