<template>
  <div class="student-dashboard-page">
    <div class="container dashboard-container animate-fade-in">
      
      <!-- LEFT SIDEBAR NAV -->
      <aside class="dashboard-sidebar glass-card">
        <!-- User Identity Box -->
        <div class="sidebar-user-header">
          <div class="user-avatar-initials">
            {{ getUserInitials(courseStore.userMe?.fullname) }}
          </div>
          <div class="user-info-text">
            <h3 class="user-name" :title="courseStore.userMe?.fullname">{{ courseStore.userMe?.fullname || 'Học viên' }}</h3>
            <span class="user-role-label">{{ courseStore.userMe?.role === 'admin' ? 'Quản trị viên' : 'Học viên ACC' }}</span>
            <small class="user-id-sub">Mã: #ACC-{{ String(courseStore.userMe?.id || 1).padStart(5, '0') }}</small>
          </div>
        </div>

        <div class="sidebar-divider"></div>

        <!-- Section Label -->
        <span class="sidebar-section-title">ĐIỀU HƯỚNG</span>

        <!-- Main Dashboard Navigation Tabs -->
        <nav class="sidebar-nav-list">
          <button 
            type="button"
            class="sidebar-nav-item" 
            :class="{ active: activeTab === 'overview' }"
            @click="activeTab = 'overview'"
          >
            <span>Tổng quan</span>
          </button>

          <button 
            type="button"
            class="sidebar-nav-item" 
            :class="{ active: activeTab === 'wishlist' }"
            @click="activeTab = 'wishlist'"
          >
            <span>Khóa học quan tâm</span>
            <span class="tab-badge" v-if="courseStore.wishlist?.length > 0">{{ courseStore.wishlist.length }}</span>
          </button>

          <button 
            type="button"
            class="sidebar-nav-item" 
            :class="{ active: activeTab === 'profile' }"
            @click="activeTab = 'profile'"
          >
            <span>Hồ sơ cá nhân</span>
          </button>
        </nav>

        <div class="sidebar-divider"></div>

        <!-- Section Label -->
        <span class="sidebar-section-title">KHÁM PHÁ</span>

        <!-- Quick Portal Links (100% Valid Routes) -->
        <div class="sidebar-quick-links">
          <router-link to="/courses" class="sidebar-link-row">
            <span>Danh mục Khóa học</span>
            <span>→</span>
          </router-link>
          <router-link to="/admissions" class="sidebar-link-row">
            <span>Lịch Tuyển sinh mới</span>
            <span>→</span>
          </router-link>
          <router-link to="/library/blog" class="sidebar-link-row">
            <span>Cẩm nang & Kiến thức</span>
            <span>→</span>
          </router-link>
          <router-link to="/contact" class="sidebar-link-row">
            <span>Liên hệ Cố vấn học tập</span>
            <span>→</span>
          </router-link>
        </div>

        <div class="sidebar-footer">
          <button type="button" @click="handleLogout" class="sidebar-logout-btn">
            Đăng xuất tài khoản
          </button>
        </div>
      </aside>

      <!-- RIGHT MAIN CONTENT AREA -->
      <main class="dashboard-main-content">

        <!-- ==================== TAB 0: TỔNG QUAN ==================== -->
        <div v-show="activeTab === 'overview'" class="tab-pane animate-fade-in">
          
          <!-- Hero Banner -->
          <div class="overview-hero-card">
            <div class="overview-hero-content">
              <div class="overview-hero-badge">
                CỔNG THÔNG TIN HỌC VIÊN
              </div>
              <h1 class="overview-hero-title">
                Xin chào, {{ courseStore.userMe?.fullname || 'Học viên' }}
              </h1>
              <p class="overview-hero-desc">
                Chào mừng bạn đến với không gian học tập và định hướng nghề nghiệp ACC Academy. Theo dõi các chương trình đào tạo quan tâm, nắm bắt lịch tuyển sinh và kết nối trực tiếp cùng ban cố vấn chuyên môn.
              </p>
              <div class="overview-hero-actions">
                <router-link to="/courses" class="btn-hero-primary">
                  Khám phá khóa học
                </router-link>
                <button type="button" @click="activeTab = 'wishlist'" class="btn-hero-secondary">
                  Khóa học đã lưu ({{ courseStore.wishlist?.length || 0 }})
                </button>
                <button type="button" @click="activeTab = 'profile'" class="btn-hero-ghost">
                  Cập nhật hồ sơ
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
                <div class="status-info-box">
                  <div class="status-box-label">Email tài khoản</div>
                  <div class="status-box-email" :title="courseStore.userMe?.email">
                    {{ courseStore.userMe?.email }}
                  </div>
                  <div class="status-box-tag">Đã xác thực trên hệ thống</div>
                </div>
              </div>
            </div>
          </div>

          <!-- 4 Core Metric Cards (100% Valid Routes) -->
          <div class="overview-metrics-grid">
            <router-link to="/courses" class="metric-card" style="text-decoration: none;">
              <div>
                <div class="metric-track">CHƯƠNG TRÌNH</div>
                <div class="metric-value">{{ courseStore.courses?.length || 0 }}</div>
                <div class="metric-label">Khóa học Đào tạo</div>
              </div>
              <div class="metric-sub">Xem toàn bộ lộ trình →</div>
            </router-link>

            <div class="metric-card" @click="activeTab = 'wishlist'">
              <div>
                <div class="metric-track">QUAN TÂM</div>
                <div class="metric-value">{{ courseStore.wishlist?.length || 0 }}</div>
                <div class="metric-label">Khóa học Đã lưu</div>
              </div>
              <div class="metric-sub">Xem danh sách quan tâm →</div>
            </div>

            <router-link to="/admissions" class="metric-card" style="text-decoration: none;">
              <div>
                <div class="metric-track">KHAI GIẢNG</div>
                <div class="metric-value">Chiêu sinh</div>
                <div class="metric-label">Lịch Tuyển sinh mới</div>
              </div>
              <div class="metric-sub">Xem lịch khai giảng mới nhất →</div>
            </router-link>

            <router-link to="/library/blog" class="metric-card" style="text-decoration: none;">
              <div>
                <div class="metric-track">TÀI NGUYÊN</div>
                <div class="metric-value">Cẩm nang</div>
                <div class="metric-label">Kiến thức Thực chiến</div>
              </div>
              <div class="metric-sub">Đọc các bài viết hữu ích →</div>
            </router-link>
          </div>

          <!-- 2-Column Main Section -->
          <div class="overview-columns-layout">
            
            <!-- Left Column (Main Focus - 68%) -->
            <div class="overview-main-col">
              
              <!-- Section 1: Khóa học bạn đang quan tâm -->
              <div class="overview-section-card">
                <div class="section-card-header">
                  <div>
                    <h3 class="section-card-title">Khóa học bạn đang quan tâm</h3>
                    <p class="section-card-desc">Danh sách các chương trình đào tạo bạn đã lưu để theo dõi và nhận tư vấn</p>
                  </div>
                  <button v-if="courseStore.wishlist?.length > 0" type="button" @click="activeTab = 'wishlist'" class="btn-text-action">
                    Xem tất cả ({{ courseStore.wishlist.length }}) →
                  </button>
                </div>

                <div v-if="!courseStore.wishlist || courseStore.wishlist.length === 0" class="empty-mini-state">
                  <p class="empty-mini-title">Bạn chưa lưu khóa học nào vào danh sách quan tâm.</p>
                  <p class="empty-mini-desc">Hãy khám phá danh mục khóa học của viện và nhấn lưu lại để xem sau.</p>
                  <router-link to="/courses" class="btn btn-primary btn-sm mt-3 inline-block">
                    Khám phá khóa học ngay
                  </router-link>
                </div>

                <div v-else class="wishlist-preview-list">
                  <div v-for="item in courseStore.wishlist.slice(0, 3)" :key="item.id || item.course?.id" class="wishlist-preview-item">
                    <img 
                      :src="formatImageUrl(item.course?.image || item.image, 'w800') || 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=400&q=80'" 
                      :alt="item.course?.title || item.title" 
                      class="wishlist-preview-img" 
                    />
                    <div class="wishlist-preview-body">
                      <span class="preview-cat-badge">{{ item.course?.category || 'Chương trình đào tạo' }}</span>
                      <h4 class="preview-title">{{ item.course?.title || item.title }}</h4>
                      <div class="preview-meta">
                        <span>{{ item.course?.duration || 'Lộ trình thực chiến' }}</span>
                        <span>•</span>
                        <span>Khóa học chuyên sâu</span>
                      </div>
                    </div>
                    <div class="preview-actions">
                      <router-link :to="'/course/' + (item.course?.handle || item.handle || item.course?.id)" class="btn btn-sm btn-primary">
                        Xem chi tiết
                      </router-link>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Section 2: Chương trình đào tạo tiêu biểu -->
              <div class="overview-section-card">
                <div class="section-card-header">
                  <div>
                    <h3 class="section-card-title">Chương trình đào tạo tiêu biểu</h3>
                    <p class="section-card-desc">Các khóa học được thiết kế thực chiến, giảng dạy bởi đội ngũ chuyên gia hàng đầu</p>
                  </div>
                  <router-link to="/courses" class="btn-text-action">
                    Xem toàn bộ khóa học →
                  </router-link>
                </div>

                <div class="featured-courses-grid">
                  <div v-for="course in recommendedCourses" :key="course.id" class="featured-course-item">
                    <div class="featured-img-wrap">
                      <img 
                        :src="formatImageUrl(course.image, 'w800') || 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=600&q=80'" 
                        :alt="course.title" 
                        class="featured-course-img" 
                      />
                      <span class="featured-tag">{{ course.category || 'Khóa học ACC' }}</span>
                    </div>
                    <div class="featured-body">
                      <h5 class="featured-name">{{ course.title }}</h5>
                      <div class="featured-footer-row">
                        <span class="featured-duration">{{ course.duration || 'Lộ trình bài bản' }}</span>
                        <router-link :to="'/course/' + (course.handle || course.id)" class="btn-view-detail-link">
                          Chi tiết →
                        </router-link>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

            </div>

            <!-- Right Column (Sidebar Widgets - 32%) -->
            <div class="overview-side-col">
              
              <!-- Widget 1: Hỗ trợ & Tư vấn trực tiếp -->
              <div class="side-widget-card consult-widget">
                <div class="widget-header-row">
                  <h4 class="widget-title">Tư vấn Tuyển sinh & Học vụ</h4>
                </div>
                <p class="widget-desc">Bạn đang cần giải đáp về lộ trình học, lịch khai giảng hay học phí ưu đãi?</p>
                <div class="hotline-box">
                  <div class="hotline-number">098.384.7176</div>
                  <div class="hotline-time">Phục vụ: 08:00 - 21:00 (Thứ 2 - Thứ 7)</div>
                </div>
                <div class="widget-action-group">
                  <router-link to="/contact" class="btn-widget-primary">
                    Đăng ký tư vấn miễn phí
                  </router-link>
                  <router-link to="/admissions" class="btn-widget-secondary">
                    Xem lịch chiêu sinh
                  </router-link>
                </div>
              </div>

              <!-- Widget 2: Tóm tắt thông tin tài khoản -->
              <div class="side-widget-card account-widget">
                <div class="widget-header-row">
                  <h4 class="widget-title">Tài khoản & Định danh</h4>
                </div>
                <div class="account-summary-body">
                  <div class="summary-avatar-row">
                    <div class="summary-avatar">
                      {{ getUserInitials(courseStore.userMe?.fullname) }}
                    </div>
                    <div class="summary-user-text">
                      <span class="summary-name">{{ courseStore.userMe?.fullname }}</span>
                      <span class="summary-email" :title="courseStore.userMe?.email">{{ courseStore.userMe?.email }}</span>
                    </div>
                  </div>
                  <div class="summary-meta-list">
                    <div class="meta-row">
                      <span class="meta-label">Trạng thái</span>
                      <span class="meta-val verified">Đã kích hoạt</span>
                    </div>
                    <div class="meta-row">
                      <span class="meta-label">Mật khẩu</span>
                      <span class="meta-val">Được mã hóa an toàn</span>
                    </div>
                  </div>
                  <button type="button" @click="openEditModal" class="btn-edit-profile-quick">
                    Cập nhật thông tin & Đổi mật khẩu
                  </button>
                </div>
              </div>

              <!-- Widget 3: Quy chế & Tài nguyên học viện (100% Valid Routes) -->
              <div class="side-widget-card support-widget">
                <div class="widget-header-row">
                  <h4 class="widget-title">Quy chế & Hướng dẫn</h4>
                </div>
                <p class="widget-desc">Các chính sách, quy chế đào tạo và hướng dẫn học viên chính thức tại ACC Academy.</p>
                <div class="support-links-list">
                  <router-link to="/contact" class="support-link-item">
                    <span class="support-item-title">Liên hệ Cố vấn học tập</span>
                    <span class="support-item-sub">Giải đáp mọi thắc mắc học vụ</span>
                  </router-link>

                  <router-link to="/library/blog" class="support-link-item">
                    <span class="support-item-title">Cẩm nang & Kinh nghiệm</span>
                    <span class="support-item-sub">Kiến thức chuyên ngành Kế toán - AI</span>
                  </router-link>

                  <router-link to="/terms-of-service" class="support-link-item">
                    <span class="support-item-title">Điều khoản Dịch vụ</span>
                    <span class="support-item-sub">Quy chế đào tạo & học vụ</span>
                  </router-link>

                  <router-link to="/privacy-policy" class="support-link-item">
                    <span class="support-item-title">Chính sách Bảo mật</span>
                    <span class="support-item-sub">Bảo vệ thông tin cá nhân</span>
                  </router-link>

                  <router-link to="/refund-policy" class="support-link-item">
                    <span class="support-item-title">Chính sách Hoàn phí & Bảo lưu</span>
                    <span class="support-item-sub">Quy định chuyển lớp & bảo lưu</span>
                  </router-link>
                </div>
              </div>

            </div>
          </div>
        </div>

        <!-- ==================== TAB 1: KHÓA HỌC QUAN TÂM ==================== -->
        <div v-show="activeTab === 'wishlist'" class="tab-pane animate-fade-in">
          <div class="panel-card glass-card">
            <div class="panel-header-row">
              <div>
                <h2 class="panel-title">
                  Khóa học bạn đang quan tâm ({{ courseStore.wishlist?.length || 0 }})
                </h2>
                <p class="panel-subtitle">
                  Danh sách các chương trình đào tạo bạn đã lưu để theo dõi và đăng ký tư vấn tuyển sinh
                </p>
              </div>
              <router-link to="/courses" class="btn btn-outline btn-sm">
                Khám phá thêm khóa học
              </router-link>
            </div>
            
            <div v-if="!courseStore.wishlist || courseStore.wishlist.length === 0" class="empty-mini-state py-12">
              <p class="empty-mini-title">Danh sách khóa học quan tâm đang trống.</p>
              <p class="empty-mini-desc">
                Hãy duyệt các chương trình đào tạo tại ACC Academy và nhấn lưu lại các khóa học bạn yêu thích nhé!
              </p>
              <router-link to="/courses" class="btn btn-primary btn-sm mt-4 inline-block">
                Khám phá các khóa học ngay
              </router-link>
            </div>
            
            <div v-else class="wishlist-courses-grid">
              <div v-for="item in courseStore.wishlist" :key="item.id || item.course?.id" class="wishlist-course-card">
                <div class="wishlist-card-media">
                  <img 
                    :src="formatImageUrl(item.course?.image || item.image, 'w800') || 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=600&q=80'" 
                    :alt="item.course?.title || item.title" 
                    class="wishlist-card-img" 
                  />
                  <span class="wishlist-card-badge">{{ item.course?.category || 'Đào tạo ACC' }}</span>
                </div>
                <div class="wishlist-card-body">
                  <h4 class="wishlist-course-title">{{ item.course?.title || item.title }}</h4>
                  <p class="wishlist-course-desc">{{ item.course?.summary || item.course?.description || 'Chương trình đào tạo thực chiến tại ACC Academy' }}</p>
                  
                  <div class="wishlist-course-meta">
                    <span>{{ item.course?.duration || 'Lộ trình thực chiến' }}</span>
                    <span>•</span>
                    <span>{{ item.course?.level || 'Chuyên sâu' }}</span>
                  </div>

                  <div class="wishlist-action-row">
                    <router-link :to="'/course/' + (item.course?.handle || item.handle || item.course?.id)" class="btn btn-primary btn-sm" style="flex: 1; text-align: center;">
                      Xem chi tiết
                    </router-link>
                    <button type="button" @click="handleRemoveWishlist(item.course?.id || item.id)" class="btn-remove-wishlist" title="Xóa khỏi danh sách lưu">
                      Bỏ lưu
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- ==================== TAB 2: HỒ SƠ CÁ NHÂN ==================== -->
        <div v-show="activeTab === 'profile'" class="tab-pane animate-fade-in">
          <div class="panel-card glass-card">
            <div class="panel-header-row">
              <div>
                <h2 class="panel-title">Thông tin Hồ sơ Học viên</h2>
                <p class="panel-subtitle">Quản lý định danh tài khoản, thông tin liên hệ và cài đặt bảo mật</p>
              </div>
              <button type="button" @click="openEditModal" class="btn btn-primary btn-sm" style="border-radius: 10px; padding: 8px 18px; font-weight: 600;">
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
                      <span class="active-pill">Tài khoản đang hoạt động</span>
                    </div>
                  </div>
                </div>

                <div class="profile-details-list">
                  <div class="detail-row">
                    <span class="detail-label">Họ và tên</span>
                    <span class="detail-value font-bold">{{ courseStore.userMe?.fullname || 'Chưa cập nhật' }}</span>
                  </div>
                  <div class="detail-row">
                    <span class="detail-label">Địa chỉ Email</span>
                    <div class="detail-value email-row">
                      <span>{{ courseStore.userMe?.email }}</span>
                      <span class="email-verified-tag">Đã kích hoạt</span>
                    </div>
                  </div>
                  <div class="detail-row">
                    <span class="detail-label">Số điện thoại</span>
                    <span class="detail-value">{{ courseStore.userMe?.phone || 'Chưa cập nhật số điện thoại' }}</span>
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
                    <span class="detail-label">Trạng thái định danh</span>
                    <span class="detail-value text-emerald font-bold">Thành viên chính thức ACC Academy</span>
                  </div>
                </div>
              </div>

              <!-- Right: Security & Privileges -->
              <div class="profile-side-column">
                <!-- Security Card -->
                <div class="profile-sub-card">
                  <div class="sub-card-title">Bảo mật & Đăng nhập</div>
                  <div class="sub-card-content">
                    <div class="security-item">
                      <div class="sec-label">Mật khẩu đăng nhập</div>
                      <div class="sec-val">•••••••••••• (Được mã hóa an toàn)</div>
                    </div>
                    <div class="security-item">
                      <div class="sec-label">Phiên đăng nhập</div>
                      <div class="sec-val">JWT Token được bảo vệ đa lớp</div>
                    </div>
                    <button type="button" @click="openEditModal" class="btn btn-outline btn-sm w-full mt-3">
                      Đổi mật khẩu tài khoản
                    </button>
                  </div>
                </div>

                <!-- Privileges Card -->
                <div class="profile-sub-card">
                  <div class="sub-card-title">Đặc quyền học viên ACC</div>
                  <ul class="privileges-list">
                    <li>Tư vấn định hướng lộ trình đào tạo chuyên sâu miễn phí</li>
                    <li>Hỗ trợ giải đáp chuyên môn từ đội ngũ giảng viên & ban cố vấn</li>
                    <li>Cập nhật liên tục các thông báo chiêu sinh và ưu đãi mới nhất</li>
                    <li>Nhận tài liệu học tập, biểu mẫu & cẩm nang chuyên sâu độc quyền</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>

      </main>
    </div>

    <!-- ==================== MODAL CẬP NHẬT HỒ SƠ ==================== -->
    <div v-if="showEditModal" class="modal-overlay" @click.self="showEditModal = false">
      <div class="profile-modal-card">
        <!-- Modal Header -->
        <div class="profile-modal-header">
          <div>
            <h3 class="profile-modal-title">Cập nhật Hồ sơ</h3>
            <p class="profile-modal-subtitle">Thay đổi thông tin cá nhân và thiết lập mật khẩu bảo mật</p>
          </div>
          <button type="button" @click="showEditModal = false" class="modal-close-button" title="Đóng">
            &times;
          </button>
        </div>

        <!-- User Quick Info Banner -->
        <div class="profile-modal-user-banner">
          <div class="profile-modal-avatar">
            {{ getUserInitials(courseStore.userMe?.fullname) }}
          </div>
          <div class="profile-modal-user-meta">
            <div class="profile-modal-user-email">
              <span>{{ courseStore.userMe?.email }}</span>
            </div>
            <div class="profile-modal-badge">
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
                <span>Bảo mật & Đổi mật khẩu</span>
              </div>
              <span class="password-card-hint">Để trống nếu không đổi</span>
            </div>

            <!-- Old Password -->
            <div class="modal-form-section">
              <label class="modal-input-label">Mật khẩu hiện tại (Mật khẩu cũ)</label>
              <div class="modal-input-wrapper">
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
                  {{ showOldPassword ? 'Ẩn' : 'Hiện' }}
                </button>
              </div>
            </div>

            <!-- New Password -->
            <div class="modal-form-section">
              <label class="modal-input-label">Mật khẩu mới</label>
              <div class="modal-input-wrapper">
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
                  {{ showNewPassword ? 'Ẩn' : 'Hiện' }}
                </button>
              </div>
            </div>

            <!-- Confirm New Password -->
            <div class="modal-form-section">
              <label class="modal-input-label">Xác nhận mật khẩu mới</label>
              <div class="modal-input-wrapper">
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
                  {{ showConfirmPassword ? 'Ẩn' : 'Hiện' }}
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
              <span v-if="savingProfile">Đang lưu...</span>
              <span v-else>Lưu thay đổi</span>
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
import { formatImageUrl } from '@/utils/imageHelper';

const router = useRouter();
const courseStore = useCourseStore();

const activeTab = ref('overview');

// Edit Profile Modal States
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
  if (editPassword.value) {
    if (editPassword.value.length < 6) {
      courseStore.showToast('Mật khẩu mới phải có ít nhất 6 ký tự!', 'warning');
      return;
    }
    if (editPassword.value !== editConfirmPassword.value) {
      courseStore.showToast('Mật khẩu xác nhận không khớp!', 'warning');
      return;
    }
  }

  savingProfile.value = true;
  try {
    const payload = {
      fullname: editFullname.value.trim(),
      phone: editPhone.value.trim() || undefined
    };
    if (editPassword.value) {
      payload.old_password = editOldPassword.value;
      payload.password = editPassword.value;
    }
    await courseStore.updateProfile(payload);
    courseStore.showToast('Cập nhật thông tin hồ sơ thành công!', 'success');
    showEditModal.value = false;
  } catch (err) {
    courseStore.showToast(err.message || 'Lỗi khi cập nhật hồ sơ', 'error');
  } finally {
    savingProfile.value = false;
  }
};

const handleLogout = () => {
  courseStore.logout();
  router.push('/login');
};

// Recommended courses for overview
const recommendedCourses = computed(() => {
  return (courseStore.courses || []).slice(0, 3);
});

const formatJoinDate = (dateStr) => {
  if (!dateStr) return 'Mới gia nhập';
  const d = new Date(dateStr);
  return `${d.getDate().toString().padStart(2, '0')}/${(d.getMonth() + 1).toString().padStart(2, '0')}/${d.getFullYear()}`;
};

onMounted(async () => {
  if (!courseStore.token) {
    courseStore.showToast('Vui lòng đăng nhập để truy cập Dashboard!', 'warning');
    router.push('/login');
    return;
  }
  
  refreshDashboardData();
});

// Refresh dashboard data in parallel
const refreshDashboardData = async () => {
  try {
    const promises = [
      courseStore.fetchUserMe(),
      courseStore.fetchWishlist()
    ];
    if (courseStore.courses.length === 0) {
      promises.push(courseStore.fetchCourses());
    }
    await Promise.all(promises);
  } catch (err) {
    console.error('Dashboard refresh error:', err);
  }
};

const handleRemoveWishlist = async (courseId) => {
  if (!courseId) return;
  await courseStore.toggleWishlist(courseId);
};

const formatDate = (dateStr) => {
  if (!dateStr) return '';
  const d = new Date(dateStr);
  return `${d.getDate().toString().padStart(2, '0')}/${(d.getMonth() + 1).toString().padStart(2, '0')}/${d.getFullYear()}`;
};

const getUserInitials = (name) => {
  if (!name) return 'HV';
  const parts = name.trim().split(' ');
  if (parts.length === 1) return parts[0].substring(0, 2).toUpperCase();
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
};
</script>

<style scoped src="@/styles/views/Dashboard.css"></style>
