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
            <span class="user-role-label">{{ courseStore.userMe?.role === 'admin' ? 'Quản trị viên' : 'Học viên ACC' }}</span>
          </div>
        </div>

        <div class="sidebar-divider"></div>

        <nav class="sidebar-nav-list">
          <button 
            class="sidebar-nav-item" 
            :class="{ active: activeTab === 'overview' }"
            @click="activeTab = 'overview'"
          >
            <span class="tab-label">Tổng quan</span>
          </button>

          <button 
            class="sidebar-nav-item" 
            :class="{ active: activeTab === 'courses' }"
            @click="activeTab = 'courses'"
          >
            <span class="tab-label">Khóa học của tôi</span>
            <span class="tab-badge" v-if="purchasedCourses.length > 0">{{ purchasedCourses.length }}</span>
          </button>

          <button 
            class="sidebar-nav-item" 
            :class="{ active: activeTab === 'profile' }"
            @click="activeTab = 'profile'"
          >
            <span class="tab-label">Hồ sơ cá nhân</span>
          </button>

          <button 
            class="sidebar-nav-item" 
            :class="{ active: activeTab === 'referral' }"
            @click="activeTab = 'referral'"
          >
            <span class="tab-label">Lan tỏa & Nhận quà</span>
          </button>

          <button 
            class="sidebar-nav-item" 
            :class="{ active: activeTab === 'orders' }"
            @click="activeTab = 'orders'"
          >
            <span class="tab-label">Lịch sử đơn hàng</span>
            <span class="tab-badge" v-if="orders.length > 0">{{ orders.length }}</span>
          </button>

          <button 
            class="sidebar-nav-item" 
            :class="{ active: activeTab === 'cart' }"
            @click="activeTab = 'cart'"
          >
            <span class="tab-label">Giỏ hàng</span>
            <span class="tab-badge" v-if="courseStore.cart.length > 0">{{ courseStore.cart.length }}</span>
          </button>

          <button 
            class="sidebar-nav-item" 
            :class="{ active: activeTab === 'wishlist' }"
            @click="activeTab = 'wishlist'"
          >
            <span class="tab-label">Yêu thích</span>
            <span class="tab-badge" v-if="courseStore.wishlist.length > 0">{{ courseStore.wishlist.length }}</span>
          </button>
        </nav>

        <div class="sidebar-footer">
          <button @click="handleLogout" class="sidebar-logout-btn">
            Đăng xuất tài khoản
          </button>
        </div>
      </aside>

      <!-- RIGHT MAIN CONTENT AREA -->
      <main class="dashboard-main-content">

        <!-- TAB 0: OVERVIEW (TỔNG QUAN HỌC TẬP) -->
        <div v-show="activeTab === 'overview'" class="tab-pane animate-fade-in">
          
          <!-- Hero Banner -->
          <div class="overview-hero-card">
            <div class="overview-hero-content">
              <div class="overview-hero-badge">
                <span class="pulse-dot"></span>
                <span>Trung tâm học tập ACC Academy</span>
              </div>
              <h1 class="overview-hero-title">
                Xin chào, {{ courseStore.userMe?.fullname || 'Học viên' }}!
              </h1>
              <p class="overview-hero-desc">
                Chào mừng bạn trở lại. Hãy tiếp tục hành trình nâng tầm kỹ năng thực chiến và làm chủ công nghệ AI hôm nay nhé!
              </p>
              <div class="overview-hero-actions">
                <button 
                  v-if="purchasedCourses.length > 0" 
                  @click="activeTab = 'courses'" 
                  class="btn-hero-primary"
                >
                  <span>Vào lớp học ngay</span>
                  <span class="hero-action-badge">{{ purchasedCourses.length }}</span>
                </button>
                <router-link v-else to="/courses/ai" class="btn-hero-primary">
                  <span>Khám phá khóa học</span>
                </router-link>
                <button @click="activeTab = 'referral'" class="btn-hero-secondary">
                  <span>Nhận thưởng giới thiệu</span>
                </button>
                <button @click="openEditModal" class="btn-hero-ghost">
                  <span>Cài đặt tài khoản</span>
                </button>
              </div>
            </div>
            
            <div class="overview-hero-widget">
              <div class="hero-user-status-card">
                <div class="status-card-header">
                  <div class="status-avatar">
                    {{ getUserInitials(courseStore.userMe?.fullname) }}
                  </div>
                  <div>
                    <div class="status-role-badge">
                      {{ courseStore.userMe?.role === 'admin' ? 'Quản trị viên' : 'Học viên chính thức' }}
                    </div>
                    <div class="status-joined">Gia nhập: {{ formatJoinDate(courseStore.userMe?.createdAt) }}</div>
                  </div>
                </div>
                <div class="status-wallet-box">
                  <div class="wallet-label">Ví giảm giá khả dụng</div>
                  <div class="wallet-amount">{{ formatPrice(courseStore.userMe?.storeCreditBalance || 0) }}</div>
                  <div class="wallet-note">Tự động trừ vào đơn thanh toán tiếp theo</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Key Metrics Row -->
          <div class="overview-metrics-grid">
            <div class="metric-card" @click="activeTab = 'courses'">
              <div class="metric-icon-box blue">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>
              </div>
              <div class="metric-info">
                <div class="metric-value">{{ purchasedCourses.length }}</div>
                <div class="metric-label">Khóa học sở hữu</div>
                <div class="metric-sub">Truy cập học trọn đời ›</div>
              </div>
            </div>

            <div class="metric-card" @click="activeTab = 'referral'">
              <div class="metric-icon-box emerald">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect><line x1="1" y1="10" x2="23" y2="10"></line></svg>
              </div>
              <div class="metric-info">
                <div class="metric-value">{{ formatPrice(courseStore.userMe?.storeCreditBalance || 0) }}</div>
                <div class="metric-label">Ví giảm giá khả dụng</div>
                <div class="metric-sub">Tự động trừ khi đặt hàng ›</div>
              </div>
            </div>

            <div class="metric-card" @click="activeTab = 'referral'">
              <div class="metric-icon-box amber">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 12 20 22 4 22 4 12"></polyline><rect x="2" y="7" width="20" height="5"></rect><line x1="12" y1="22" x2="12" y2="7"></line><path d="M12 7H7.5a2.5 2.5 0 0 1 0-5C11 2 12 7 12 7z"></path><path d="M12 7h4.5a2.5 2.5 0 0 0 0-5C13 2 12 7 12 7z"></path></svg>
              </div>
              <div class="metric-info">
                <div class="metric-value">{{ formatPrice(referralSummary?.totalCommissionEarned || 0) }}</div>
                <div class="metric-label">Hoa hồng nhận được</div>
                <div class="metric-sub">{{ referralSummary?.totalReferrals || 0 }} bạn bè đã mời ›</div>
              </div>
            </div>

            <div class="metric-card" @click="activeTab = 'orders'">
              <div class="metric-icon-box violet">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
              </div>
              <div class="metric-info">
                <div class="metric-value">{{ orders.length }}</div>
                <div class="metric-label">Đơn hàng đã đặt</div>
                <div class="metric-sub">{{ paidOrdersCount }} đơn hoàn tất ›</div>
              </div>
            </div>
          </div>

          <!-- 2-Column Main Section -->
          <div class="overview-columns-layout">
            
            <!-- Left Column (Main Focus) -->
            <div class="overview-main-col">
              
              <!-- Section: Khóa học của bạn -->
              <div class="overview-section-card">
                <div class="section-card-header">
                  <div class="section-card-title-group">
                                        <div>
                      <h3 class="section-card-title">Khóa học của bạn</h3>
                      <p class="section-card-desc">Truy cập bài giảng và học tập trực tuyến 24/7</p>
                    </div>
                  </div>
                  <button v-if="purchasedCourses.length > 0" @click="activeTab = 'courses'" class="btn-text-action">
                    Xem tất cả ({{ purchasedCourses.length }}) ›
                  </button>
                </div>

                <!-- If user has courses -->
                <div v-if="purchasedCourses.length > 0" class="in-progress-courses-list">
                  <div v-for="course in purchasedCourses.slice(0, 3)" :key="course.id" class="in-progress-course-item">
                    <img :src="course.image" :alt="course.title" class="in-progress-img" />
                    <div class="in-progress-info">
                      <span class="in-progress-category">{{ course.category_slug || course.category || 'Khóa học' }}</span>
                      <h4 class="in-progress-title">{{ course.title }}</h4>
                      <div class="in-progress-meta">
                        <span>{{ course.duration || '12 tuần' }}</span>
                        <span>•</span>
                        <span>{{ course.level || 'Chuyên sâu' }}</span>
                        <span>•</span>
                        <span class="badge-lifetime">Quyền học trọn đời</span>
                      </div>
                    </div>
                    <div class="in-progress-action">
                      <router-link :to="'/courses/' + course.handle + '/study'" class="btn-resume-study">
                        Vào học ngay →
                      </router-link>
                    </div>
                  </div>
                </div>

                <!-- If user has NO courses: Show nice welcome banner + Suggested courses -->
                <div v-else class="no-courses-overview">
                  <div class="no-courses-hero-prompt">
                                        <div class="prompt-text">
                      <h4>Bắt đầu hành trình nâng cao kỹ năng</h4>
                      <p>Bạn chưa kích hoạt khóa học nào. Hãy khám phá các chương trình thực chiến từ ACC Academy để bắt đầu ngay hôm nay!</p>
                    </div>
                  </div>

                  <div class="suggested-courses-title">Gợi ý khóa học tiêu biểu dành cho bạn:</div>
                  <div class="suggested-courses-grid">
                    <div v-for="course in recommendedCourses" :key="course.id" class="suggested-course-card">
                      <img :src="course.image" :alt="course.title" class="suggested-img" />
                      <div class="suggested-body">
                        <span class="suggested-cat">{{ course.category || 'Khóa học' }}</span>
                        <h5 class="suggested-name">{{ course.title }}</h5>
                        <div class="suggested-price-row">
                          <span class="suggested-price">{{ formatPrice(course.price) }}</span>
                          <router-link :to="'/course/' + course.handle" class="btn-suggested-enroll">
                            Chi tiết
                          </router-link>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Section: Lịch sử đơn hàng gần đây -->
              <div class="overview-section-card">
                <div class="section-card-header">
                  <div class="section-card-title-group">
                                        <div>
                      <h3 class="section-card-title">Đơn hàng gần đây</h3>
                      <p class="section-card-desc">Lịch sử giao dịch và trạng thái thanh toán</p>
                    </div>
                  </div>
                  <button v-if="orders.length > 0" @click="activeTab = 'orders'" class="btn-text-action">
                    Xem tất cả ({{ orders.length }}) ›
                  </button>
                </div>

                <div v-if="orders.length === 0" class="empty-mini-state">
                  <p>Chưa có giao dịch đơn hàng nào được ghi nhận.</p>
                  <router-link to="/courses/ai" class="btn btn-outline btn-sm mt-2 inline-block">
                    + Đặt khóa học đầu tiên
                  </router-link>
                </div>

                <div v-else class="recent-orders-list">
                  <div v-for="order in recentOrders" :key="order.id" class="recent-order-item">
                    <div class="recent-order-left">
                      <span class="recent-order-id">#{{ String(order.id).padStart(6, '0') }}</span>
                      <span class="recent-order-date">{{ formatDate(order.createdAt) }}</span>
                    </div>
                    <div class="recent-order-middle">
                      <span class="recent-order-items-count">{{ order.items?.length || 1 }} khóa học</span>
                      <span class="recent-order-total">{{ formatPrice(order.totalPrice) }}</span>
                    </div>
                    <div class="recent-order-right">
                      <span class="status-badge" :class="order.status">
                        {{ translateOrderStatus(order.status) }}
                      </span>
                      <router-link :to="`/order/${order.id}`" class="recent-order-link">
                        Chi tiết →
                      </router-link>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Right Column (Sidebar Widgets) -->
            <div class="overview-side-col">
              
              <!-- Widget 1: Referral Quick Share -->
              <div class="side-widget-card referral-widget">
                <div class="widget-header">
                                    <h4 class="widget-title">Lan tỏa & Nhận quà</h4>
                </div>
                <p class="widget-desc">
                  Chia sẻ mã giới thiệu để bạn bè nhận ưu đãi tới <strong>14,5 triệu</strong> và bạn nhận hoa hồng tới <strong>29 triệu</strong>.
                </p>
                <div class="widget-referral-box">
                  <div class="referral-code-label">MÃ GIỚI THIỆU CỦA BẠN</div>
                  <div class="referral-code-row">
                    <span class="referral-code-text">{{ referralSummary?.referralCode || 'ACC...' }}</span>
                    <button @click="copyReferralLink" class="btn-copy-code">
                      {{ copied ? '✓ Đã chép' : 'Sao chép' }}
                    </button>
                  </div>
                </div>
                <button @click="activeTab = 'referral'" class="btn-widget-link">
                  Xem chi tiết hoa hồng & danh sách bạn bè →
                </button>
              </div>

              <!-- Widget 2: Student Profile Card -->
              <div class="side-widget-card profile-summary-widget">
                <div class="widget-header">
                                    <h4 class="widget-title">Hồ sơ cá nhân</h4>
                </div>
                <div class="profile-summary-body">
                  <div class="summary-avatar-box">
                    <div class="summary-avatar">
                      {{ getUserInitials(courseStore.userMe?.fullname) }}
                    </div>
                    <div class="summary-user-text">
                      <span class="summary-name">{{ courseStore.userMe?.fullname }}</span>
                      <span class="summary-email">{{ courseStore.userMe?.email }}</span>
                    </div>
                  </div>
                  <div class="summary-meta-list">
                    <div class="meta-row">
                      <span class="meta-label">Trạng thái</span>
                      <span class="meta-val verified">✓ Đã kích hoạt</span>
                    </div>
                    <div class="meta-row">
                      <span class="meta-label">Bảo mật</span>
                      <span class="meta-val">Mật khẩu cá nhân</span>
                    </div>
                  </div>
                  <button @click="openEditModal" class="btn-edit-profile-quick">
                    Đổi thông tin & Mật khẩu
                  </button>
                </div>
              </div>

              <!-- Widget 3: Academic Support & Community -->
              <div class="side-widget-card support-widget">
                <div class="widget-header">
                                    <h4 class="widget-title">Hỗ trợ & Tài nguyên</h4>
                </div>
                <p class="widget-desc">Bạn cần trợ giúp về khóa học, tài liệu hay bài tập? Đội ngũ ACC sẵn sàng đồng hành cùng bạn.</p>
                <div class="support-links-list">
                  <router-link to="/contact" class="support-link-item">
                                        <div class="support-item-text">
                      <span class="support-item-title">Liên hệ Cố vấn học tập</span>
                      <span class="support-item-sub">Giải đáp mọi thắc mắc</span>
                    </div>
                  </router-link>
                  <router-link to="/library/blog" class="support-link-item">
                                        <div class="support-item-text">
                      <span class="support-item-title">Cẩm nang & Kinh nghiệm</span>
                      <span class="support-item-sub">Tài liệu tham khảo chuyên ngành</span>
                    </div>
                  </router-link>
                  <router-link to="/legal/chinh-sach-bao-luu" class="support-link-item">
                                        <div class="support-item-text">
                      <span class="support-item-title">Chính sách học viên</span>
                      <span class="support-item-sub">Quy chế học tập & bảo lưu</span>
                    </div>
                  </router-link>
                </div>
              </div>

            </div>
          </div>
        </div>

        <!-- TAB 1: COURSES -->
        <div v-show="activeTab === 'courses'" class="tab-pane animate-fade-in">
          <div class="panel-card glass-card">
            <div class="section-title-row">
              <h2 class="panel-title">Khóa học của tôi ({{ filteredPurchasedCourses.length }})</h2>
              
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
            
            <div v-if="purchasedCourses.length === 0" class="empty-state py-10">
              <div class="empty-state-icon" style="display: flex; justify-content: center; margin-bottom: 12px; color: #94a3b8;">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>
              </div>
              <h3 style="font-size: 17px; font-weight: 700; color: #0f172a; margin: 0 0 6px 0;">Bạn chưa sở hữu khóa học nào</h3>
              <p style="font-size: 13.5px; color: #64748b; margin: 0 0 16px 0;">Hãy tham gia ngay các khóa học AI & Kỹ năng tại ACC Academy để bắt đầu!</p>
              <router-link to="/courses/ai" class="btn btn-primary btn-sm inline-block">Khám phá các khóa học</router-link>

              <!-- Suggestions below empty state -->
              <div class="empty-suggestions-container mt-8 text-left">
                <div class="suggested-courses-title">Gợi ý khóa học tiêu biểu:</div>
                <div class="suggested-courses-grid">
                  <div v-for="course in recommendedCourses" :key="course.id" class="suggested-course-card">
                    <img :src="course.image" :alt="course.title" class="suggested-img" />
                    <div class="suggested-body">
                      <span class="suggested-cat">{{ course.category || 'Khóa học' }}</span>
                      <h5 class="suggested-name">{{ course.title }}</h5>
                      <div class="suggested-price-row">
                        <span class="suggested-price">{{ formatPrice(course.price) }}</span>
                        <router-link :to="'/course/' + course.handle" class="btn-suggested-enroll">
                          Chi tiết
                        </router-link>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div v-else-if="filteredPurchasedCourses.length === 0" class="empty-state py-12">
              <div class="empty-state-icon" style="display: flex; justify-content: center; margin-bottom: 12px; color: #94a3b8;">
                <svg width="42" height="42" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
              </div>
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
                        Vào lớp học ngay
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
          <div class="panel-card glass-card">
            <div class="profile-header-row">
              <div>
                <h2 class="panel-title">Thông tin Hồ sơ Học viên</h2>
                <p class="panel-subtitle">Quản lý định danh tài khoản, thông tin liên hệ và cài đặt bảo mật</p>
              </div>
              <button @click="openEditModal" class="btn btn-primary btn-sm" style="border-radius: 12px; padding: 9px 20px; font-size: 13.5px;">
                Cập nhật thông tin & Đổi mật khẩu
              </button>
            </div>
            
            <div class="profile-two-column-layout">
              <!-- Left: Identity & Info -->
              <div class="profile-main-card">
                <div class="profile-hero-badge-box">
                  <div class="profile-large-avatar">
                    {{ getUserInitials(courseStore.userMe?.fullname) }}
                  </div>
                  <div class="profile-large-info">
                    <h3 class="profile-large-name">{{ courseStore.userMe?.fullname }}</h3>
                    <div class="profile-badge-tags">
                      <span class="role-pill">{{ courseStore.userMe?.role === 'admin' ? 'Quản trị viên' : 'Học viên ACC' }}</span>
                      <span class="active-pill">✓ Tài khoản đang hoạt động</span>
                    </div>
                  </div>
                </div>

                <div class="profile-details-table">
                  <div class="detail-row">
                    <span class="detail-label">Họ và tên</span>
                    <span class="detail-value">{{ courseStore.userMe?.fullname }}</span>
                  </div>
                  <div class="detail-row">
                    <span class="detail-label">Email tài khoản</span>
                    <span class="detail-value">
                      {{ courseStore.userMe?.email }}
                      <span class="email-verified-tag">✓ Đã kích hoạt</span>
                    </span>
                  </div>
                  <div class="detail-row">
                    <span class="detail-label">Số điện thoại</span>
                    <span class="detail-value font-mono">{{ courseStore.userMe?.phone || 'Chưa cập nhật' }}</span>
                  </div>
                  <div class="detail-row">
                    <span class="detail-label">Mã học viên (ID)</span>
                    <span class="detail-value font-mono">#ACC-{{ String(courseStore.userMe?.id || 1).padStart(5, '0') }}</span>
                  </div>
                  <div class="detail-row">
                    <span class="detail-label">Ngày tham gia hệ thống</span>
                    <span class="detail-value">{{ formatDate(courseStore.userMe?.createdAt) }}</span>
                  </div>
                  <div class="detail-row">
                    <span class="detail-label">Số dư ví giảm giá</span>
                    <span class="detail-value text-emerald font-bold">{{ formatPrice(courseStore.userMe?.storeCreditBalance || 0) }}</span>
                  </div>
                </div>
              </div>

              <!-- Right: Security & Privileges -->
              <div class="profile-side-column">
                <!-- Security Card -->
                <div class="profile-sub-card">
                  <div class="sub-card-title">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
                    <span>Bảo mật & Đăng nhập</span>
                  </div>
                  <div class="sub-card-content">
                    <div class="security-item">
                      <div class="sec-label">Mật khẩu đăng nhập</div>
                      <div class="sec-val">•••••••••••• (Được mã hóa bảo vệ)</div>
                    </div>
                    <div class="security-item">
                      <div class="sec-label">Phiên đăng nhập</div>
                      <div class="sec-val">JWT Token được bảo vệ an toàn</div>
                    </div>
                    <button @click="openEditModal" class="btn btn-outline btn-sm w-full mt-3">
                      Đổi mật khẩu tài khoản
                    </button>
                  </div>
                </div>

                <!-- Privileges Card -->
                <div class="profile-sub-card">
                  <div class="sub-card-title">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"></path></svg>
                    <span>Đặc quyền học viên ACC</span>
                  </div>
                  <ul class="privileges-list">
                    <li>
                      <span class="priv-icon">✓</span>
                      <span>Quyền truy cập học trọn đời các khóa học đã đăng ký</span>
                    </li>
                    <li>
                      <span class="priv-icon">✓</span>
                      <span>Hỗ trợ giải đáp chuyên môn từ giảng viên & cố vấn</span>
                    </li>
                    <li>
                      <span class="priv-icon">✓</span>
                      <span>Chứng chỉ hoàn thành khóa học chính thức từ ACC Academy</span>
                    </li>
                    <li>
                      <span class="priv-icon">✓</span>
                      <span>Quyền tham gia chương trình nhận hoa hồng giới thiệu</span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- TAB 3: REFERRAL -->
        <div v-show="activeTab === 'referral'" class="tab-pane animate-fade-in">
          <div class="panel-card glass-card">
            <h2 class="panel-title">Chương trình Lan tỏa & Nhận quà</h2>
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

        <!-- TAB 4: ORDERS -->
        <div v-show="activeTab === 'orders'" class="tab-pane animate-fade-in">
          <div class="panel-card glass-card">
            <h2 class="panel-title">Lịch sử đơn hàng & Thanh toán</h2>
            
            <div v-if="orders.length === 0" class="empty-state py-12">
              <div class="empty-state-icon" style="display: flex; justify-content: center; margin-bottom: 12px; color: #94a3b8;">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
              </div>
              <p style="font-size: 15px; font-weight: 600; color: #0f172a;">Chưa có đơn hàng nào được tạo.</p>
              <router-link to="/courses/ai" class="btn btn-primary btn-sm mt-4 inline-block">Khám phá các khóa học</router-link>
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
                      Xem chi tiết
                    </router-link>
                    <button 
                      v-if="order.status === 'pending'" 
                      @click="handlePayOrder(order.id)" 
                      class="btn btn-outline btn-sm btn-success"
                      :disabled="loading"
                      style="flex: 1;"
                    >
                      Thanh toán (Demo)
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- TAB 5: CART -->
        <div v-show="activeTab === 'cart'" class="tab-pane animate-fade-in">
          <div class="panel-card glass-card">
            <h2 class="panel-title">Giỏ hàng của bạn ({{ courseStore.cart.length }})</h2>
            
            <div v-if="courseStore.cart.length === 0" class="empty-state py-12">
              <div class="empty-state-icon" style="display: flex; justify-content: center; margin-bottom: 12px; color: #94a3b8;">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"></circle><circle cx="20" cy="21" r="1"></circle><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path></svg>
              </div>
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
                    Xóa
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
                  {{ loading ? 'Đang tạo đơn hàng...' : 'Xác nhận Đặt hàng & Nhận ưu đãi' }}
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- TAB 6: WISHLIST -->
        <div v-show="activeTab === 'wishlist'" class="tab-pane animate-fade-in">
          <div class="panel-card glass-card">
            <h2 class="panel-title">Danh sách Khóa học Yêu thích ({{ courseStore.wishlist.length }})</h2>
            
            <div v-if="courseStore.wishlist.length === 0" class="empty-state py-12">
              <div class="empty-state-icon" style="display: flex; justify-content: center; margin-bottom: 12px; color: #94a3b8;">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path></svg>
              </div>
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
                      Bỏ lưu
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
      <div class="profile-modal-card">
        <!-- Modal Header -->
        <div class="profile-modal-header">
          <div class="profile-modal-header-info">
            <div class="modal-header-icon-box">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>
            </div>
            <div>
              <h3 class="profile-modal-title">Cập nhật Hồ sơ</h3>
              <p class="profile-modal-subtitle">Thay đổi thông tin cá nhân và thiết lập mật khẩu bảo mật</p>
            </div>
          </div>
          <button @click="showEditModal = false" class="modal-close-button" title="Đóng">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>

        <!-- User Quick Info Banner -->
        <div class="profile-modal-user-banner">
          <div class="profile-modal-avatar">
            {{ getUserInitials(courseStore.userMe?.fullname) }}
          </div>
          <div class="profile-modal-user-meta">
            <div class="profile-modal-user-email">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                <polyline points="22,6 12,13 2,6"></polyline>
              </svg>
              <span>{{ courseStore.userMe?.email }}</span>
            </div>
            <div class="profile-modal-badge">
              <span class="badge-dot"></span>
              {{ courseStore.userMe?.role === 'admin' ? 'Quản trị viên' : 'Học viên chính thức' }}
            </div>
          </div>
        </div>

        <form @submit.prevent="handleSaveProfile" class="profile-modal-form">
          <!-- Full Name Input -->
          <div class="modal-form-section">
            <label class="modal-input-label">
              <span>Họ và tên học viên</span>
              <span class="required-star">*</span>
            </label>
            <div class="modal-input-wrapper">
              <span class="modal-input-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"></path>
                  <circle cx="12" cy="7" r="4"></circle>
                </svg>
              </span>
              <input 
                type="text" 
                v-model="editFullname" 
                class="modal-form-input" 
                placeholder="Nhập họ và tên đầy đủ..." 
                required 
              />
            </div>
          </div>

                    <!-- Phone Section -->
          <div class="modal-form-section">
            <label class="modal-input-label">
              <span>Số điện thoại liên hệ</span>
            </label>
            <div class="modal-input-wrapper">
              <span class="modal-input-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
                </svg>
              </span>
              <input 
                type="tel" 
                v-model="editPhone" 
                class="modal-form-input" 
                placeholder="Nhập số điện thoại (ví dụ: 0901234567)..." 
              />
            </div>
          </div>

          <!-- Password Security Section -->
          <div class="modal-password-card">
            <div class="password-card-header">
              <div class="password-card-title">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                </svg>
                <span>Bảo mật & Đổi mật khẩu</span>
              </div>
              <span class="password-card-hint">Để trống nếu không đổi</span>
            </div>

            <!-- Old Password -->
            <div class="modal-form-section">
              <label class="modal-input-label">Mật khẩu hiện tại (Mật khẩu cũ)</label>
              <div class="modal-input-wrapper">
                <span class="modal-input-icon">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="7.5" cy="15.5" r="5.5"></circle>
                    <path d="m21 2-9.6 9.6"></path>
                    <path d="m15.5 7.5 3 3"></path>
                  </svg>
                </span>
                <input 
                  :type="showOldPassword ? 'text' : 'password'" 
                  v-model="editOldPassword" 
                  class="modal-form-input with-toggle" 
                  placeholder="Nhập mật khẩu hiện tại..." 
                  autocomplete="current-password"
                />
                <button 
                  type="button" 
                  class="modal-password-toggle" 
                  @click="showOldPassword = !showOldPassword"
                  tabindex="-1"
                >
                  <svg v-if="!showOldPassword" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8z"></path>
                    <circle cx="12" cy="12" r="3"></circle>
                  </svg>
                  <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                    <line x1="1" y1="1" x2="23" y2="23"></line>
                  </svg>
                </button>
              </div>
            </div>

            <!-- New Password -->
            <div class="modal-form-section">
              <label class="modal-input-label">Mật khẩu mới</label>
              <div class="modal-input-wrapper">
                <span class="modal-input-icon">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                    <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                  </svg>
                </span>
                <input 
                  :type="showNewPassword ? 'text' : 'password'" 
                  v-model="editPassword" 
                  class="modal-form-input with-toggle" 
                  placeholder="Nhập mật khẩu mới (tối thiểu 6 ký tự)..." 
                  autocomplete="new-password"
                />
                <button 
                  type="button" 
                  class="modal-password-toggle" 
                  @click="showNewPassword = !showNewPassword"
                  tabindex="-1"
                >
                  <svg v-if="!showNewPassword" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8z"></path>
                    <circle cx="12" cy="12" r="3"></circle>
                  </svg>
                  <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                    <line x1="1" y1="1" x2="23" y2="23"></line>
                  </svg>
                </button>
              </div>
            </div>

            <!-- Confirm New Password -->
            <div class="modal-form-section">
              <label class="modal-input-label">Xác nhận mật khẩu mới</label>
              <div class="modal-input-wrapper">
                <span class="modal-input-icon">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="20 6 9 17 4 12"></polyline>
                  </svg>
                </span>
                <input 
                  :type="showConfirmPassword ? 'text' : 'password'" 
                  v-model="editConfirmPassword" 
                  class="modal-form-input with-toggle" 
                  placeholder="Nhập lại mật khẩu mới để xác nhận..." 
                  autocomplete="new-password"
                />
                <button 
                  type="button" 
                  class="modal-password-toggle" 
                  @click="showConfirmPassword = !showConfirmPassword"
                  tabindex="-1"
                >
                  <svg v-if="!showConfirmPassword" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8z"></path>
                    <circle cx="12" cy="12" r="3"></circle>
                  </svg>
                  <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                    <line x1="1" y1="1" x2="23" y2="23"></line>
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <!-- Actions -->
          <div class="profile-modal-actions">
            <button type="button" @click="showEditModal = false" class="btn-modal-cancel">
              Hủy bỏ
            </button>
            <button type="submit" class="btn-modal-submit" :disabled="savingProfile">
              <span v-if="savingProfile" class="modal-spinner"></span>
              <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
                <polyline points="17 21 17 13 7 13 7 21"></polyline>
                <polyline points="7 3 7 8 15 8"></polyline>
              </svg>
              <span>{{ savingProfile ? 'Đang lưu...' : 'Lưu thay đổi' }}</span>
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

const activeTab = ref(route.query.tab || 'overview');

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
const editPhone = ref('');
const editOldPassword = ref('');
const editPassword = ref('');
const editConfirmPassword = ref('');
const showOldPassword = ref(false);
const showNewPassword = ref(false);
const showConfirmPassword = ref(false);
const savingProfile = ref(false);

const openEditModal = () => {
  editFullname.value = courseStore.userMe?.fullname || '';
  editPhone.value = courseStore.userMe?.phone || '';
  editOldPassword.value = '';
  editPassword.value = '';
  editConfirmPassword.value = '';
  showOldPassword.value = false;
  showNewPassword.value = false;
  showConfirmPassword.value = false;
  showEditModal.value = true;
};

const handleSaveProfile = async () => {
  if (!editFullname.value.trim()) {
    courseStore.showToast('Vui lòng nhập họ và tên!', 'warning');
    return;
  }
  const hasNewPass = Boolean(editPassword.value && editPassword.value.trim());
  const hasOldPass = Boolean(editOldPassword.value && editOldPassword.value.trim());

  if (hasNewPass || hasOldPass) {
    if (!hasOldPass) {
      courseStore.showToast('Vui lòng nhập mật khẩu hiện tại (mật khẩu cũ) để đổi mật khẩu mới!', 'warning');
      return;
    }
    if (!hasNewPass) {
      courseStore.showToast('Vui lòng nhập mật khẩu mới!', 'warning');
      return;
    }
    if (editPassword.value.trim().length < 6) {
      courseStore.showToast('Mật khẩu mới phải có tối thiểu 6 ký tự!', 'warning');
      return;
    }
    if (editPassword.value.trim() !== editConfirmPassword.value.trim()) {
      courseStore.showToast('Xác nhận mật khẩu mới không trùng khớp!', 'warning');
      return;
    }
  }
  savingProfile.value = true;
  try {
    const payload = { fullname: editFullname.value.trim(), phone: editPhone.value.trim() || null };
    if (hasNewPass) {
      payload.old_password = editOldPassword.value.trim();
      payload.password = editPassword.value.trim();
    }
    await courseStore.updateProfile(payload);
    courseStore.showToast('Cập nhật thông tin học viên thành công!', 'success');
    showEditModal.value = false;
  } catch (err) {
    courseStore.showToast('Lỗi cập nhật hồ sơ: ' + (err.message || 'Không thể cập nhật'), 'error');
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


// Recommended courses for empty states and overview
const recommendedCourses = computed(() => {
  const ownedIds = new Set(purchasedCourses.value.map(c => c.id));
  const available = courseStore.courses.filter(c => !ownedIds.has(c.id));
  return (available.length > 0 ? available : courseStore.courses).slice(0, 3);
});

// Recent orders for overview (top 3)
const recentOrders = computed(() => {
  return (orders.value || []).slice(0, 3);
});

// Paid orders count
const paidOrdersCount = computed(() => {
  return (orders.value || []).filter(o => o.status === 'paid').length;
});

const formatJoinDate = (dateStr) => {
  if (!dateStr) return 'Mới gia nhập';
  const d = new Date(dateStr);
  return `${d.getDate()}/${d.getMonth() + 1}/${d.getFullYear()}`;
};

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
