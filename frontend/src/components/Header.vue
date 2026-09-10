<template>
  <header class="main-header" :class="{ 'scrolled': isScrolled, 'header-hidden': isHidden }">
    <div class="container header-container">
      <!-- Logo -->
      <router-link to="/" class="logo">
        <img src="/images/logo3.png" alt="ACC Academy Logo" class="logo-image" />
      </router-link>

      <!-- Desktop Nav -->
      <nav class="desktop-nav">
        <!-- 1. ĐỐI TÁC TIN CẬY -->
        <div class="nav-item dropdown">
          <button class="nav-link dropdown-toggle" @click.prevent="openDrawer('trusted-partners')">
            ĐỐI TÁC TIN CẬY
            <svg class="chevron-icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M6 9l6 6 6-6"/>
            </svg>
          </button>
          <div class="dropdown-menu">
            <a href="https://andrews.edu.vn/" target="_blank" rel="noopener noreferrer" class="dropdown-item">
              <div class="dropdown-title">MBA ĐẠI HỌC ANDREWS, HOA KỲ</div>
              <div class="dropdown-desc">Chương trình Thạc sĩ Quản trị Kinh doanh hàng đầu Hoa Kỳ tại Việt Nam</div>
            </a>
            <a href="https://alumni.andrews.edu.vn/" target="_blank" rel="noopener noreferrer" class="dropdown-item">
              <div class="dropdown-title">Viện Khoa học Lãnh đạo và Quản trị doanh nghiệp – LEADMAN</div>
              <div class="dropdown-desc">Mạng lưới kết nối lãnh đạo và cựu học viên Andrews</div>
            </a>
          </div>
        </div>

        <!-- 2. CHO DOANH NGHIỆP (Mega Dropdown) -->
        <div class="nav-item mega-dropdown">
          <button class="nav-link dropdown-toggle" aria-haspopup="true" @click.prevent="openDrawer('corporate')">
            CHO DOANH NGHIỆP
            <svg class="chevron-icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M6 9l6 6 6-6"/>
            </svg>
          </button>
          
          <!-- Corporate Mega Menu Panel -->
          <div class="mega-menu-panel corporate-mega-panel">
            <div class="container corporate-mega-container">
              <div class="corporate-menu-grid">

                <!-- Col 1: Đào tạo AI INHOUSE -->
                <div class="corporate-menu-group">
                  <div class="corporate-group-header">
                    <router-link to="/corporate/dao-tao" class="corporate-group-title">
                      Đào tạo AI INHOUSE cho doanh nghiệp
                    </router-link>
                  </div>
                  <ul class="corporate-sub-list">
                    <li><router-link to="/corporate/dao-tao" class="corporate-sub-link">Đào tạo AI cho Cơ quan Nhà nước, UBND & Phường/Xã</router-link></li>
                    <li><router-link to="/corporate/dao-tao" class="corporate-sub-link">Đào tạo AI chuyên ngành Y tế & Thẩm mỹ</router-link></li>
                    <li><router-link to="/corporate/dao-tao" class="corporate-sub-link">Đào tạo AI chuyên ngành Xây dựng</router-link></li>
                    <li><router-link to="/corporate/dao-tao" class="corporate-sub-link">Đào tạo AI cho Doanh nghiệp Sản xuất & Thương mại</router-link></li>
                    <li><router-link to="/corporate/dao-tao" class="corporate-sub-link">Đào tạo AI cho Trường học & Cơ sở Giáo dục</router-link></li>
                  </ul>
                </div>

                <!-- Col 2: Quản trị & Bảo mật Dữ liệu & Xây dựng Khung Năng lực -->
                <div class="corporate-menu-group">
                  <div class="corporate-group-header">
                    <router-link to="/corporate/coe" class="corporate-group-title">
                      Quản trị & Bảo mật Dữ liệu Doanh nghiệp
                    </router-link>
                  </div>

                  <div class="corporate-group-header style-mt">
                    <router-link to="/corporate/for-team" class="corporate-group-title">
                      Xây dựng Khung năng lực & Phát triển Nhân sự
                    </router-link>
                  </div>
                  <ul class="corporate-sub-list">
                    <li><router-link to="/corporate/for-team" class="corporate-sub-link">Xây dựng Ma trận năng lực theo vị trí</router-link></li>
                    <li><router-link to="/corporate/for-team" class="corporate-sub-link">Tích hợp năng lực AI & năng lực số</router-link></li>
                    <li><router-link to="/corporate/for-team" class="corporate-sub-link">Xây dựng khung năng lực theo phòng ban</router-link></li>
                    <li><router-link to="/corporate/for-team" class="corporate-sub-link">Xây dựng Lộ trình đào tạo & phát triển toàn diện cho doanh nghiệp</router-link></li>
                  </ul>
                </div>

                <!-- Col 3: Kỹ năng & Lãnh đạo -->
                <div class="corporate-menu-group">
                  <div class="corporate-group-header">
                    <router-link to="/corporate/case-studies" class="corporate-group-title">
                      Năng lực Lãnh đạo Chủ động & Hiệu quả
                    </router-link>
                  </div>

                  <div class="corporate-group-header style-mt">
                    <router-link to="/corporate/case-studies" class="corporate-group-title">
                      Phát triển Kỹ năng mềm trong Môi trường Doanh nghiệp
                    </router-link>
                  </div>

                  <div class="corporate-group-header style-mt">
                    <router-link to="/corporate/case-studies" class="corporate-group-title">
                      Nghệ thuật Kể chuyện & Truyền cảm hứng
                    </router-link>
                  </div>
                </div>

              </div>
            </div>
          </div>
        </div>

        <!-- 3. TUYỂN SINH SAU ĐẠI HỌC -->
        <button class="nav-link dropdown-toggle" @click.prevent="openDrawer('post-graduate')">
          TUYỂN SINH SAU ĐẠI HỌC
          <svg class="chevron-icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M6 9l6 6 6-6"/>
          </svg>
        </button>

        <!-- 4. CHO CÁ NHÂN (Mega Menu: Khóa học) -->
        <div class="nav-item mega-dropdown">
          <button class="nav-link dropdown-toggle" aria-haspopup="true" @click.prevent="openDrawer('courses')">
            CHO CÁ NHÂN
            <svg class="chevron-icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M6 9l6 6 6-6"/>
            </svg>
          </button>
          
          <!-- Mega Menu Panel -->
          <div class="mega-menu-panel">
            <div class="container mega-menu-container">
              <!-- Left Sidebar: Categories -->
              <div class="mega-menu-sidebar">
                <button 
                  v-for="cat in categories" 
                  :key="cat.id"
                  class="mega-sidebar-item"
                  :class="{ active: selectedCategory === cat.id }"
                  @mouseenter="selectedCategory = cat.id"
                >
                  <span class="indicator-bar"></span>
                  {{ cat.name }}
                </button>
              </div>
              
              <!-- Right Content: Program Grid -->
              <div class="mega-menu-content">
                <div class="mega-content-header">
                  <h3 class="mega-content-title">{{ activeCategoryName }}</h3>
                  <router-link :to="activeCategoryLink" class="mega-view-all-link">
                    Xem tất cả {{ activeCategoryName }} &rarr;
                  </router-link>
                </div>
                
                <div class="mega-programs-grid">
                  <div 
                    v-for="program in filteredPrograms" 
                    :key="program.id"
                    class="mega-program-card"
                  >
                    <router-link :to="program.link" class="mega-card-link">
                      <div class="mega-school-logo">
                        <img :src="program.logo" :alt="program.school" />
                      </div>
                      <div class="mega-card-info">
                        <span class="mega-school-name">{{ program.school }}</span>
                        <h4 class="mega-program-title" :title="program.title">{{ program.title }}</h4>
                      </div>
                    </router-link>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 5. ĐỘI NGŨ GIẢNG VIÊN -->
        <router-link to="/doi-ngu-giang-vien" class="nav-link">ĐỘI NGŨ GIẢNG VIÊN</router-link>

        <!-- 6. DỰ ÁN -->
        <router-link to="/corporate/case-studies" class="nav-link">DỰ ÁN</router-link>

        <!-- 7. CHIA SẺ HỌC VIÊN -->
        <router-link to="/chia-se-hoc-vien" class="nav-link">CHIA SẺ HỌC VIÊN</router-link>

        <!-- 8. LIÊN HỆ -->
        <router-link to="/contact" class="nav-link">LIÊN HỆ</router-link>

        <!-- 9. VỀ CHÚNG TÔI -->
        <router-link to="/about-us" class="nav-link">VỀ CHÚNG TÔI</router-link>
      </nav>

      <!-- Action buttons -->
      <div class="header-actions">
        <router-link v-if="!courseStore.token" to="/login" class="login-btn">Đăng nhập</router-link>
        
        <!-- User Profile Dropdown -->
        <div 
          v-else 
          class="user-dropdown-wrapper" 
          @mouseenter="isUserDropdownOpen = true" 
          @mouseleave="isUserDropdownOpen = false"
        >
          <button class="user-btn-trigger" @click="isUserDropdownOpen = !isUserDropdownOpen">
            <span class="user-avatar-badge">{{ (courseStore.userMe?.fullname || 'H')[0].toUpperCase() }}</span>
            <span class="user-name-text">{{ courseStore.userMe?.fullname || 'Học viên' }}</span>
            <svg class="chevron-icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M6 9l6 6 6-6"/>
            </svg>
          </button>

          <div class="user-dropdown-menu" :class="{ 'open': isUserDropdownOpen }">
            <div class="user-dropdown-header">
              <div class="user-header-info">
                <div class="user-header-name">{{ courseStore.userMe?.fullname }}</div>
                <div class="user-header-email">{{ courseStore.userMe?.email }}</div>
              </div>
              <span v-if="courseStore.userMe?.role === 'admin'" class="user-role-tag">Quản trị viên</span>
            </div>

            <div class="user-dropdown-divider"></div>

            <div class="user-dropdown-body">
              <router-link 
                v-if="courseStore.userMe?.role === 'admin'" 
                to="/admin" 
                class="user-dropdown-link admin-highlight" 
                @click="isUserDropdownOpen = false"
              >
                <span class="dropdown-icon">👑</span>
                <div class="dropdown-link-text">
                  <span class="link-title">Trang quản trị hệ thống</span>
                  <span class="link-desc">Quản lý khóa học, đơn hàng & học viên</span>
                </div>
              </router-link>

              <router-link to="/dashboard" class="user-dropdown-link" @click="isUserDropdownOpen = false">
                <span class="dropdown-icon">🎓</span>
                <div class="dropdown-link-text">
                  <span class="link-title">Khóa học của tôi</span>
                  <span class="link-desc">Vào học & xem tiến độ</span>
                </div>
              </router-link>

              <router-link to="/gioi-thieu" class="user-dropdown-link" @click="isUserDropdownOpen = false">
                <span class="dropdown-icon">🎁</span>
                <div class="dropdown-link-text">
                  <span class="link-title">Giới thiệu & Nhận thưởng</span>
                  <span class="link-desc">Nhận đến 29.000.000 VNĐ hoa hồng</span>
                </div>
              </router-link>
            </div>

            <div class="user-dropdown-divider"></div>

            <button class="user-dropdown-logout" @click="handleLogout">
              <span class="dropdown-icon">🚪</span>
              <span>Đăng xuất tài khoản</span>
            </button>
          </div>
        </div>
        
        <button class="icon-btn" aria-label="Tìm kiếm" @click="isSearchOpen = true">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"/>
            <path d="M21 21l-4.35-4.35"/>
          </svg>
        </button>
        
        <button class="icon-btn cart-btn" aria-label="Giỏ hàng" @click="isCartOpen = true">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/>
            <line x1="3" y1="6" x2="21" y2="6"/>
            <path d="M16 10a4 4 0 0 1-8 0"/>
          </svg>
          <span class="cart-badge">{{ courseStore.cart.length }}</span>
        </button>

        <!-- Mobile Menu Trigger -->
        <button class="mobile-menu-toggle" @click="toggleMobileMenu" aria-label="Menu">
          <span class="bar" :class="{ 'open': isMobileMenuOpen }"></span>
          <span class="bar" :class="{ 'open': isMobileMenuOpen }"></span>
          <span class="bar" :class="{ 'open': isMobileMenuOpen }"></span>
        </button>
      </div>
    </div>

    <!-- Mobile Nav Overlay -->
    <div class="mobile-nav" :class="{ 'open': isMobileMenuOpen }">
      <div class="mobile-nav-inner">
        <!-- Mobile Accordion: Đối tác tin cậy -->
        <div class="mobile-nav-group">
          <div class="mobile-nav-label" @click="toggleMobileSection('trusted-partners')">
            ĐỐI TÁC TIN CẬY
            <svg class="chevron-icon" :class="{ 'rotate': activeMobileSection === 'trusted-partners' }" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M6 9l6 6 6-6"/>
            </svg>
          </div>
          <div class="mobile-nav-links" v-show="activeMobileSection === 'trusted-partners'">
            <a href="https://andrews.edu.vn/" target="_blank" rel="noopener noreferrer" @click="closeMobileMenu">MBA ĐẠI HỌC ANDREWS, HOA KỲ</a>
            <a href="https://alumni.andrews.edu.vn/" target="_blank" rel="noopener noreferrer" @click="closeMobileMenu">Viện Khoa học Lãnh đạo và Quản trị doanh nghiệp – LEADMAN</a>
          </div>
        </div>

        <!-- Mobile Accordion: Doanh nghiệp -->
        <div class="mobile-nav-group">
          <div class="mobile-nav-label" @click="toggleMobileSection('corporate')">
            CHO DOANH NGHIỆP
            <svg class="chevron-icon" :class="{ 'rotate': activeMobileSection === 'corporate' }" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M6 9l6 6 6-6"/>
            </svg>
          </div>
          <div class="mobile-nav-links" v-show="activeMobileSection === 'corporate'">
            <!-- Group 1: Đào tạo AI INHOUSE -->
            <div class="mobile-sub-group">
              <div class="mobile-sub-label" @click="toggleMobileSubSection('corp-ai')">
                <span>Đào tạo AI INHOUSE cho doanh nghiệp</span>
                <span class="plus-icon">{{ activeMobileSubSection === 'corp-ai' ? '−' : '+' }}</span>
              </div>
              <div class="mobile-sub-content" v-show="activeMobileSubSection === 'corp-ai'">
                <router-link to="/corporate/dao-tao" @click="closeMobileMenu" class="mobile-sub-link">Đào tạo AI cho Cơ quan Nhà nước, UBND & Phường/Xã</router-link>
                <router-link to="/corporate/dao-tao" @click="closeMobileMenu" class="mobile-sub-link">Đào tạo AI chuyên ngành Y tế & Thẩm mỹ</router-link>
                <router-link to="/corporate/dao-tao" @click="closeMobileMenu" class="mobile-sub-link">Đào tạo AI chuyên ngành Xây dựng</router-link>
                <router-link to="/corporate/dao-tao" @click="closeMobileMenu" class="mobile-sub-link">Đào tạo AI cho Doanh nghiệp Sản xuất & Thương mại</router-link>
                <router-link to="/corporate/dao-tao" @click="closeMobileMenu" class="mobile-sub-link">Đào tạo AI cho Trường học & Cơ sở Giáo dục</router-link>
              </div>
            </div>

            <!-- Group 2: Quản trị & Bảo mật Dữ liệu -->
            <router-link to="/corporate/coe" @click="closeMobileMenu" class="mobile-single-sublink">Quản trị & Bảo mật Dữ liệu Doanh nghiệp</router-link>

            <!-- Group 3: Xây dựng Khung Năng lực -->
            <div class="mobile-sub-group">
              <div class="mobile-sub-label" @click="toggleMobileSubSection('corp-framework')">
                <span>Xây dựng Khung năng lực & Phát triển Nhân sự</span>
                <span class="plus-icon">{{ activeMobileSubSection === 'corp-framework' ? '−' : '+' }}</span>
              </div>
              <div class="mobile-sub-content" v-show="activeMobileSubSection === 'corp-framework'">
                <router-link to="/corporate/for-team" @click="closeMobileMenu" class="mobile-sub-link">Xây dựng Ma trận năng lực theo vị trí</router-link>
                <router-link to="/corporate/for-team" @click="closeMobileMenu" class="mobile-sub-link">Tích hợp năng lực AI & năng lực số</router-link>
                <router-link to="/corporate/for-team" @click="closeMobileMenu" class="mobile-sub-link">Xây dựng khung năng lực theo phòng ban</router-link>
                <router-link to="/corporate/for-team" @click="closeMobileMenu" class="mobile-sub-link">Xây dựng Lộ trình đào tạo & phát triển toàn diện cho doanh nghiệp</router-link>
              </div>
            </div>

            <!-- Single sub-items -->
            <router-link to="/corporate/case-studies" @click="closeMobileMenu" class="mobile-single-sublink">Năng lực Lãnh đạo Chủ động & Hiệu quả</router-link>
            <router-link to="/corporate/case-studies" @click="closeMobileMenu" class="mobile-single-sublink">Phát triển Kỹ năng mềm trong Môi trường Doanh nghiệp</router-link>
            <router-link to="/corporate/case-studies" @click="closeMobileMenu" class="mobile-single-sublink">Nghệ thuật Kể chuyện & Truyền cảm hứng</router-link>
          </div>
        </div>

        <!-- Mobile Accordion: Tuyển sinh sau đại học -->
        <div class="mobile-nav-group">
          <div class="mobile-nav-label" @click="toggleMobileSection('post-graduate')">
            TUYỂN SINH SAU ĐẠI HỌC
            <svg class="chevron-icon" :class="{ 'rotate': activeMobileSection === 'post-graduate' }" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M6 9l6 6 6-6"/>
            </svg>
          </div>
          <div class="mobile-nav-links" v-show="activeMobileSection === 'post-graduate'">
            <router-link to="/post-graduate/mba" @click="closeMobileMenu" class="mobile-single-sublink">Thạc sĩ quản trị kinh doanh</router-link>
            <router-link to="/post-graduate/gei" @click="closeMobileMenu" class="mobile-single-sublink">Global Executive Institute</router-link>
            <router-link to="/post-graduate/mini-mba" @click="closeMobileMenu" class="mobile-single-sublink">Mini MBA</router-link>
          </div>
        </div>

        <!-- Mobile Accordion: Cho Cá Nhân -->
        <div class="mobile-nav-group">
          <div class="mobile-nav-label" @click="toggleMobileSection('courses')">
            CHO CÁ NHÂN
            <svg class="chevron-icon" :class="{ 'rotate': activeMobileSection === 'courses' }" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M6 9l6 6 6-6"/>
            </svg>
          </div>
          <div class="mobile-nav-links" v-show="activeMobileSection === 'courses'">
            <div class="mobile-sub-group">
              <div class="mobile-sub-label" @click="toggleMobileSubSection('individual-ai')">
                <span>Các khóa Đào tạo ứng dụng AI cho cá nhân</span>
                <span class="plus-icon">{{ activeMobileSubSection === 'individual-ai' ? '−' : '+' }}</span>
              </div>
              <div class="mobile-sub-content" v-show="activeMobileSubSection === 'individual-ai'">
                <router-link to="/courses/ai" @click="closeMobileMenu" class="mobile-sub-link">AI dành cho CEO & Lãnh đạo Doanh nghiệp</router-link>
                <router-link to="/courses/ai" @click="closeMobileMenu" class="mobile-sub-link">AI ứng dụng trong Kế toán - Tài chính</router-link>
                <router-link to="/courses/ai" @click="closeMobileMenu" class="mobile-sub-link">AI ứng dụng trong Hành chính - Nhân sự</router-link>
                <router-link to="/courses/ai" @click="closeMobileMenu" class="mobile-sub-link">AI ứng dụng trong Kinh doanh & Phát triển thị trường</router-link>
                <router-link to="/courses/ai" @click="closeMobileMenu" class="mobile-sub-link">AI ứng dụng trong Sales & Chăm sóc khách hàng</router-link>
                <router-link to="/courses/ai" @click="closeMobileMenu" class="mobile-sub-link">AI ứng dụng trong Marketing & Truyền thông</router-link>
                <router-link to="/courses/ai" @click="closeMobileMenu" class="mobile-sub-link">AI ứng dụng trong Sản xuất - Kỹ thuật - Vận hành</router-link>
              </div>
            </div>

            <router-link to="/courses/chuyen-mon" @click="closeMobileMenu" class="mobile-single-sublink">Kỹ năng Cốt lõi & Nghiệp vụ dành cho Trọng tài viên</router-link>
            <router-link to="/courses/chuyen-mon" @click="closeMobileMenu" class="mobile-single-sublink">Quản trị & Bảo vệ Dữ liệu Cá nhân</router-link>
            <router-link to="/courses/mem" @click="closeMobileMenu" class="mobile-single-sublink">Digital Marketing & Phát triển Thương hiệu Số</router-link>
            <router-link to="/courses/mem" @click="closeMobileMenu" class="mobile-single-sublink">Xây dựng & Phát triển Thương hiệu Cá nhân</router-link>
          </div>
        </div>

        <router-link to="/doi-ngu-giang-vien" class="mobile-single-link" @click="closeMobileMenu">ĐỘI NGŨ GIẢNG VIÊN</router-link>
        <router-link to="/corporate/case-studies" class="mobile-single-link" @click="closeMobileMenu">DỰ ÁN</router-link>
        <router-link to="/chia-se-hoc-vien" class="mobile-single-link" @click="closeMobileMenu">CHIA SẺ HỌC VIÊN</router-link>
        <router-link to="/contact" class="mobile-single-link" @click="closeMobileMenu">LIÊN HỆ</router-link>
        <router-link to="/about-us" class="mobile-single-link" @click="closeMobileMenu">VỀ CHÚNG TÔI</router-link>
        
        <router-link v-if="!courseStore.token" to="/login" class="mobile-login-btn" @click="closeMobileMenu">Đăng nhập</router-link>
        <div v-else class="mobile-user-menu" style="display: flex; flex-direction: column; gap: 8px; width: 100%;">
          <router-link v-if="courseStore.userMe?.role === 'admin'" to="/admin" class="mobile-login-btn" style="background: var(--primary-gradient); color: white;" @click="closeMobileMenu">👑 Quản trị hệ thống</router-link>
          <router-link to="/dashboard" class="mobile-login-btn" @click="closeMobileMenu">🙋‍♂️ {{ courseStore.userMe?.fullname || 'Học viên' }}</router-link>
        </div>
      </div>
    </div>

    <!-- Off-canvas Sidebar (Drawer Menu) -->
    <!-- Overlay backdrop -->
    <Transition name="fade">
      <div v-if="isDrawerOpen" class="drawer-overlay" @click="closeDrawer"></div>
    </Transition>

    <!-- Drawer Panel -->
    <Transition name="slide">
      <div v-if="isDrawerOpen" class="drawer-panel">
        <!-- Close Button at top left -->
        <div class="drawer-header">
          <button class="drawer-close-btn" @click="closeDrawer" aria-label="Close menu">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>

        <!-- Links List -->
        <div class="drawer-body">
          <span class="drawer-tagline">ACC Academy</span>
          <h2 class="drawer-title">{{ drawerTitle }}</h2>
          
          <div class="drawer-links-list">
            <div v-for="item in drawerItems" :key="item.title" class="drawer-item-block">
              <a 
                v-if="item.externalLink"
                :href="item.externalLink" 
                target="_blank" 
                rel="noopener noreferrer"
                @click="closeDrawer"
                class="drawer-link-item"
              >
                {{ item.title }}
              </a>
              <router-link 
                v-else
                :to="item.link" 
                @click="closeDrawer"
                class="drawer-link-item"
              >
                {{ item.title }}
              </router-link>

              <div v-if="item.subItems && item.subItems.length" class="drawer-sub-list">
                <router-link 
                  v-for="sub in item.subItems" 
                  :key="sub.title"
                  :to="sub.link" 
                  @click="closeDrawer"
                  class="drawer-sub-item-link"
                >
                  {{ sub.title }}
                </router-link>
              </div>
            </div>
          </div>
        </div>

        <!-- Zalo Button at bottom -->
        <div class="drawer-footer">
          <a href="https://zalo.me/your_zalo_number" target="_blank" rel="noopener" class="drawer-zalo-btn" aria-label="Chat Zalo">
            <div class="zalo-bubble">
              <span class="zalo-text">Zalo</span>
            </div>
          </a>
        </div>
      </div>
    </Transition>

    <!-- Slide-over Cart -->
    <SlideOverCart 
      :isOpen="isCartOpen" 
      @close="isCartOpen = false"
      @view-cart="handleViewCart"
      @checkout="handleCheckout"
    />

    <!-- Slide-over Search -->
    <SlideOverSearch
      :isOpen="isSearchOpen"
      @close="isSearchOpen = false"
    />
  </header>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { useCourseStore } from '@/stores/courses';
import { slugify } from '@/utils/slugify';
import SlideOverCart from '@/components/SlideOverCart.vue';
import SlideOverSearch from '@/components/SlideOverSearch.vue';

const router = useRouter();
const courseStore = useCourseStore();

const isCartOpen = ref(false);
const isSearchOpen = ref(false);
const isUserDropdownOpen = ref(false);
const isScrolled = ref(false);
const isHidden = ref(false);
const lastScrollTop = ref(0);
const isMobileMenuOpen = ref(false);
const activeMobileSection = ref('');
const activeMobileSubSection = ref('');

const handleLogout = () => {
  isUserDropdownOpen.value = false;
  courseStore.logout();
  courseStore.showToast('Đã đăng xuất thành công!', 'info');
  router.push('/login');
};

const handleViewCart = () => {
  isCartOpen.value = false;
  router.push('/cart');
};

const handleCheckout = () => {
  isCartOpen.value = false;
  if (!courseStore.token) {
    courseStore.showToast('Vui lòng đăng nhập để tiến hành thanh toán!', 'warning');
    router.push('/login');
    return;
  }
  router.push('/checkout');
};

// Drawer states
const isDrawerOpen = ref(false);
const drawerType = ref('');

const openDrawer = (type) => {
  drawerType.value = type;
  isDrawerOpen.value = true;
};

const closeDrawer = () => {
  isDrawerOpen.value = false;
  drawerType.value = '';
};

// Scroll Lock logic on Drawer Toggle
watch(isDrawerOpen, (val) => {
  if (val) {
    document.body.classList.add('lock-scroll');
  } else {
    document.body.classList.remove('lock-scroll');
  }
});

// 1. Mega Menu Categories Data dynamically loaded from store
const categories = computed(() => {
  if (courseStore.categories && courseStore.categories.length > 0) {
    return courseStore.categories.map(c => ({
      id: c.slug,
      name: c.name,
      viewAllLink: c.slug === 'bundles' ? '/bundles' : `/courses/category/${c.slug}`
    }));
  }
  return [
    { id: 'ky-nang-ai', name: 'Kỹ năng AI', viewAllLink: '/courses/category/ky-nang-ai' },
    { id: 'ky-nang-chuyen-mon', name: 'Kỹ năng chuyên môn', viewAllLink: '/courses/category/ky-nang-chuyen-mon' },
    { id: 'ky-nang-mem', name: 'Kỹ năng mềm', viewAllLink: '/courses/category/ky-nang-mem' },
    { id: 'bundles', name: 'Combo khóa học', viewAllLink: '/bundles' }
  ];
});

const selectedCategory = ref('ky-nang-ai');

const activeCategoryName = computed(() => {
  const cat = categories.value.find(c => c.id === selectedCategory.value);
  return cat ? cat.name : '';
});

const activeCategoryLink = computed(() => {
  const cat = categories.value.find(c => c.id === selectedCategory.value);
  return cat ? cat.viewAllLink : '/courses/category/ky-nang-ai';
});

const translateCategory = (cat) => {
  switch (cat) {
    case 'ky-nang-ai': return 'Kỹ năng AI';
    case 'ky-nang-mem': return 'Kỹ năng mềm';
    case 'ky-nang-chuyen-mon': return 'Kỹ năng chuyên môn';
    case 'bundles': return 'Combo / Gói';
    default: return cat;
  }
};

// 2. Mega Menu Programs Dataset mapping dynamically from Course Store
const programs = computed(() => {
  return courseStore.courses.map(c => {
    const handle = c.handle || c.slug || slugify(c.title || '');
    return {
      id: c.id,
      categoryId: c.category,
      title: c.title,
      school: translateCategory(c.category),
      logo: c.image || '/images/default.jpg',
      link: `/course/${handle}`
    };
  });
});

const filteredPrograms = computed(() => {
  return programs.value.filter(p => p.categoryId === selectedCategory.value);
});

const getProgramsByCategoryId = (catId) => {
  return programs.value.filter(p => p.categoryId === catId);
};

// Drawer Title & Items computation
const drawerTitle = computed(() => {
  switch (drawerType.value) {
    case 'trusted-partners': return 'Đối tác tin cậy';
    case 'post-graduate': return 'Tuyển sinh Sau Đại học';
    case 'courses': return 'Khóa học';
    case 'programs': return 'Chương trình đào tạo';
    case 'bundles': return 'Gói Combo chương trình';
    case 'corporate': return 'Giải pháp Doanh nghiệp';
    case 'library': return 'Thư viện & Tài liệu';
    default: return '';
  }
});

const drawerItems = computed(() => {
  switch (drawerType.value) {
    case 'trusted-partners':
      return [
        { title: 'MBA ĐẠI HỌC ANDREWS, HOA KỲ', externalLink: 'https://andrews.edu.vn/' },
        { title: 'Viện Khoa học Lãnh đạo và Quản trị doanh nghiệp – LEADMAN', externalLink: 'https://alumni.andrews.edu.vn/' }
      ];
    case 'post-graduate':
      return [
        { title: 'Thạc sĩ quản trị kinh doanh', link: '/post-graduate/mba' },
        { title: 'Global Executive Institute', link: '/post-graduate/gei' },
        { title: 'Mini MBA', link: '/post-graduate/mini-mba' }
      ];
    case 'courses':
      return [
        {
          title: 'Các khóa Đào tạo ứng dụng AI cho cá nhân',
          link: '/courses/ai',
          subItems: [
            { title: 'AI dành cho CEO & Lãnh đạo Doanh nghiệp', link: '/courses/ai' },
            { title: 'AI ứng dụng trong Kế toán - Tài chính', link: '/courses/ai' },
            { title: 'AI ứng dụng trong Hành chính - Nhân sự', link: '/courses/ai' },
            { title: 'AI ứng dụng trong Kinh doanh & Phát triển thị trường', link: '/courses/ai' },
            { title: 'AI ứng dụng trong Sales & Chăm sóc khách hàng', link: '/courses/ai' },
            { title: 'AI ứng dụng trong Marketing & Truyền thông', link: '/courses/ai' },
            { title: 'AI ứng dụng trong Sản xuất - Kỹ thuật - Vận hành', link: '/courses/ai' }
          ]
        },
        { title: 'Kỹ năng Cốt lõi & Nghiệp vụ dành cho Trọng tài viên', link: '/courses/chuyen-mon' },
        { title: 'Quản trị & Bảo vệ Dữ liệu Cá nhân', link: '/courses/chuyen-mon' },
        { title: 'Digital Marketing & Phát triển Thương hiệu Số', link: '/courses/mem' },
        { title: 'Xây dựng & Phát triển Thương hiệu Cá nhân', link: '/courses/mem' }
      ];
    case 'programs':
      return courseStore.programs.map(p => ({
        title: p.title,
        link: '/courses/chuyen-mon'
      }));
    case 'bundles':
      return [
        { title: 'Combo khóa học', link: '/bundles' }
      ];
    case 'corporate':
      return [
        { 
          title: 'Đào tạo AI INHOUSE cho doanh nghiệp', 
          link: '/corporate/dao-tao',
          subItems: [
            { title: 'Đào tạo AI cho Cơ quan Nhà nước, UBND & Phường/Xã', link: '/corporate/dao-tao' },
            { title: 'Đào tạo AI chuyên ngành Y tế & Thẩm mỹ', link: '/corporate/dao-tao' },
            { title: 'Đào tạo AI chuyên ngành Xây dựng', link: '/corporate/dao-tao' },
            { title: 'Đào tạo AI cho Doanh nghiệp Sản xuất & Thương mại', link: '/corporate/dao-tao' },
            { title: 'Đào tạo AI cho Trường học & Cơ sở Giáo dục', link: '/corporate/dao-tao' }
          ]
        },
        { title: 'Quản trị & Bảo mật Dữ liệu Doanh nghiệp', link: '/corporate/coe' },
        { 
          title: 'Xây dựng Khung năng lực & Phát triển Nhân sự', 
          link: '/corporate/for-team',
          subItems: [
            { title: 'Xây dựng Ma trận năng lực theo vị trí', link: '/corporate/for-team' },
            { title: 'Tích hợp năng lực AI & năng lực số', link: '/corporate/for-team' },
            { title: 'Xây dựng khung năng lực theo phòng ban', link: '/corporate/for-team' },
            { title: 'Xây dựng Lộ trình đào tạo & phát triển toàn diện cho doanh nghiệp', link: '/corporate/for-team' }
          ]
        },
        { title: 'Năng lực Lãnh đạo Chủ động & Hiệu quả', link: '/corporate/case-studies' },
        { title: 'Phát triển Kỹ năng mềm trong Môi trường Doanh nghiệp', link: '/corporate/case-studies' },
        { title: 'Nghệ thuật Kể chuyện & Truyền cảm hứng', link: '/corporate/case-studies' }
      ];
    case 'library':
      return [
        { title: 'Thư viện bài viết', link: '/library/blog' },
        { title: 'Công thức viết prompt', link: '/library/recipes' }
      ];
    default:
      return [];
  }
});

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
};

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false;
  activeMobileSection.value = '';
  activeMobileSubSection.value = '';
};

const toggleMobileSection = (section) => {
  activeMobileSection.value = activeMobileSection.value === section ? '' : section;
};

const toggleMobileSubSection = (subSec) => {
  activeMobileSubSection.value = activeMobileSubSection.value === subSec ? '' : subSec;
};

const handleScroll = (event) => {
  let scrollTop = window.scrollY;
  if (event && event.target && event.target !== document && event.target !== window) {
    scrollTop = event.target.scrollTop;
  }
  
  isScrolled.value = scrollTop > 20;
  
  // Prevent hiding header if mobile menu, mega drawer, cart, or search is open
  if (isMobileMenuOpen.value || isDrawerOpen.value || isCartOpen.value || isSearchOpen.value) {
    isHidden.value = false;
    lastScrollTop.value = scrollTop;
    return;
  }
  
  // Hide header when scrolling down, show when scrolling up
  if (scrollTop > lastScrollTop.value && scrollTop > 80) {
    isHidden.value = true;
  } else if (scrollTop < lastScrollTop.value) {
    isHidden.value = false;
  }
  
  lastScrollTop.value = scrollTop;
};

// Real Master Programs from Store & Mega Menu Navigation Logic
const selectedProgramId = ref(null);

watch(() => courseStore.programs, (newProgs) => {
  if (newProgs.length > 0 && !selectedProgramId.value) {
    selectedProgramId.value = newProgs[0].id;
  }
}, { immediate: true });

const activeProgram = computed(() => {
  if (!selectedProgramId.value && courseStore.programs.length > 0) {
    return courseStore.programs[0];
  }
  return courseStore.programs.find(p => p.id === selectedProgramId.value);
});

const activeProgramChildCourses = computed(() => {
  if (!activeProgram.value) return [];
  return courseStore.courses.filter(c => c.programId === activeProgram.value.id);
});

const getChildCoursesByProgId = (progId) => {
  return courseStore.courses.filter(c => c.programId === progId);
};

const getCourseLink = (c) => {
  if (!c) return '/';
  const handle = c.handle || c.slug || slugify(c.title || '');
  return `/course/${handle}`;
};

const realPrograms = computed(() => {
  return courseStore.programs.map(p => {
    const childCourses = courseStore.courses.filter(c => c.programId === p.id);
    return {
      id: p.id,
      title: p.title,
      slug: p.slug,
      image: p.image || '/images/default.jpg',
      description: p.description,
      childCourses: childCourses,
      link: '/courses/chuyen-mon'
    };
  });
});

onMounted(async () => {
  window.addEventListener('scroll', handleScroll, { capture: true, passive: true });
  try {
    if (courseStore.courses.length === 0) {
      await courseStore.fetchCourses();
    }
    if (courseStore.programs.length === 0) {
      await courseStore.fetchPrograms();
    }
    if (courseStore.programs.length > 0) {
      selectedProgramId.value = courseStore.programs[0].id;
    }
  } catch (e) {
    console.error('Failed to fetch catalog data in Header', e);
  }
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll, { capture: true });
  document.body.classList.remove('lock-scroll'); // teardown scroll lock safety
});
</script>

<style scoped src="@/styles/components/Header.css"></style>
