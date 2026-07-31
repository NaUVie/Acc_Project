<template>
  <header class="main-header" :class="{ 'scrolled': isScrolled }">
    <div class="container header-container">
      <!-- Logo -->
      <router-link to="/" class="logo">
        <span class="logo-text">ACC <span class="logo-accent">Academy</span></span>
      </router-link>

      <!-- Desktop Nav -->
      <nav class="desktop-nav">
        <div class="nav-item dropdown">
          <button class="nav-link dropdown-toggle">
            Khóa học
            <svg class="chevron-icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>
          </button>
          <div class="dropdown-menu">
            <router-link to="/courses/ai" class="dropdown-item">
              <div class="dropdown-title">Kỹ năng AI</div>
              <div class="dropdown-desc">Làm chủ công cụ AI để đột phá hiệu suất làm việc</div>
            </router-link>
            <router-link to="/courses/mem" class="dropdown-item">
              <div class="dropdown-title">Kỹ năng mềm</div>
              <div class="dropdown-desc">Tư duy lãnh đạo, quản lý và giao tiếp chuyên nghiệp</div>
            </router-link>
            <router-link to="/courses/chuyen-mon" class="dropdown-item">
              <div class="dropdown-title">Kỹ năng chuyên môn</div>
              <div class="dropdown-desc">Nâng cao chuyên môn về dữ liệu, tiếp thị và vận hành</div>
            </router-link>
          </div>
        </div>

        <div class="nav-item dropdown">
          <button class="nav-link dropdown-toggle">
            Bundle khóa học
            <svg class="chevron-icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>
          </button>
          <div class="dropdown-menu">
            <router-link to="/bundles" class="dropdown-item">
              <div class="dropdown-title">Combo khóa học</div>
              <div class="dropdown-desc">Các gói combo tiết kiệm và lộ trình học toàn diện</div>
            </router-link>
          </div>
        </div>

        <div class="nav-item dropdown">
          <button class="nav-link dropdown-toggle">
            Doanh nghiệp
            <svg class="chevron-icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>
          </button>
          <div class="dropdown-menu">
            <router-link to="/corporate/dao-tao" class="dropdown-item">
              <div class="dropdown-title">Đào tạo doanh nghiệp</div>
              <div class="dropdown-desc">Giải pháp đào tạo in-house may đo riêng cho tổ chức</div>
            </router-link>
            <router-link to="/corporate/coe" class="dropdown-item">
              <div class="dropdown-title">AI Center of Excellence</div>
              <div class="dropdown-desc">Xây dựng năng lực AI cốt lõi cho doanh nghiệp</div>
            </router-link>
            <router-link to="/corporate/for-team" class="dropdown-item">
              <div class="dropdown-title">AI for Team</div>
              <div class="dropdown-desc">Ứng dụng AI nâng tầm năng lực đội ngũ</div>
            </router-link>
            <router-link to="/corporate/case-studies" class="dropdown-item">
              <div class="dropdown-title">Câu chuyện đào tạo</div>
              <div class="dropdown-desc">Các dự án thực tế đã triển khai thành công</div>
            </router-link>
          </div>
        </div>

        <div class="nav-item dropdown">
          <button class="nav-link dropdown-toggle">
            Thư viện
            <svg class="chevron-icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>
          </button>
          <div class="dropdown-menu">
            <router-link to="/library/blog" class="dropdown-item">
              <div class="dropdown-title">Thư viện bài viết</div>
              <div class="dropdown-desc">Kiến thức, tin tức công nghệ và kỹ năng số mới nhất</div>
            </router-link>
            <router-link to="/library/recipes" class="dropdown-item">
              <div class="dropdown-title">Công thức viết prompt</div>
              <div class="dropdown-desc">Thư viện câu lệnh AI thực chiến hữu ích</div>
            </router-link>
          </div>
        </div>

        <router-link to="/contact" class="nav-link">Liên hệ</router-link>
        <router-link to="/about-us" class="nav-link">Về chúng tôi</router-link>
      </nav>

      <!-- Action buttons -->
      <div class="header-actions">
        <router-link to="/login" class="login-btn">Đăng nhập khóa học</router-link>
        
        <button class="icon-btn" aria-label="Tìm kiếm">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
        </button>
        
        <router-link to="/cart" class="icon-btn cart-btn" aria-label="Giỏ hàng">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>
          <span class="cart-badge">0</span>
        </router-link>

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
        <!-- Accordion items -->
        <div class="mobile-nav-group">
          <div class="mobile-nav-label" @click="toggleMobileSection('courses')">
            Khóa học
            <svg class="chevron-icon" :class="{ 'rotate': activeMobileSection === 'courses' }" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>
          </div>
          <div class="mobile-nav-links" v-show="activeMobileSection === 'courses'">
            <router-link to="/courses/ai" @click="closeMobileMenu">Kỹ năng AI</router-link>
            <router-link to="/courses/mem" @click="closeMobileMenu">Kỹ năng mềm</router-link>
            <router-link to="/courses/chuyen-mon" @click="closeMobileMenu">Kỹ năng chuyên môn</router-link>
          </div>
        </div>

        <div class="mobile-nav-group">
          <div class="mobile-nav-label" @click="toggleMobileSection('bundles')">
            Bundle khóa học
            <svg class="chevron-icon" :class="{ 'rotate': activeMobileSection === 'bundles' }" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>
          </div>
          <div class="mobile-nav-links" v-show="activeMobileSection === 'bundles'">
            <router-link to="/bundles" @click="closeMobileMenu">Combo khóa học</router-link>
          </div>
        </div>

        <div class="mobile-nav-group">
          <div class="mobile-nav-label" @click="toggleMobileSection('corporate')">
            Doanh nghiệp
            <svg class="chevron-icon" :class="{ 'rotate': activeMobileSection === 'corporate' }" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>
          </div>
          <div class="mobile-nav-links" v-show="activeMobileSection === 'corporate'">
            <router-link to="/corporate/dao-tao" @click="closeMobileMenu">Đào tạo doanh nghiệp</router-link>
            <router-link to="/corporate/coe" @click="closeMobileMenu">AI Center of Excellence</router-link>
            <router-link to="/corporate/for-team" @click="closeMobileMenu">AI for Team</router-link>
            <router-link to="/corporate/case-studies" @click="closeMobileMenu">Câu chuyện đào tạo</router-link>
          </div>
        </div>

        <div class="mobile-nav-group">
          <div class="mobile-nav-label" @click="toggleMobileSection('library')">
            Thư viện
            <svg class="chevron-icon" :class="{ 'rotate': activeMobileSection === 'library' }" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>
          </div>
          <div class="mobile-nav-links" v-show="activeMobileSection === 'library'">
            <router-link to="/library/blog" @click="closeMobileMenu">Thư viện bài viết</router-link>
            <router-link to="/library/recipes" @click="closeMobileMenu">Công thức viết prompt</router-link>
          </div>
        </div>

        <router-link to="/contact" class="mobile-single-link" @click="closeMobileMenu">Liên hệ</router-link>
        <router-link to="/about-us" class="mobile-single-link" @click="closeMobileMenu">Về chúng tôi</router-link>
        
        <router-link to="/login" class="mobile-login-btn" @click="closeMobileMenu">Đăng nhập khóa học</router-link>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const isScrolled = ref(false);
const isMobileMenuOpen = ref(false);
const activeMobileSection = ref('');

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
};

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false;
  activeMobileSection.value = '';
};

const toggleMobileSection = (section) => {
  if (activeMobileSection.value === section) {
    activeMobileSection.value = '';
  } else {
    activeMobileSection.value = section;
  }
};

const handleScroll = () => {
  isScrolled.value = window.scrollY > 20;
};

onMounted(() => {
  window.addEventListener('scroll', handleScroll);
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
});
</script>

<style scoped>
.main-header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 80px;
  background-color: transparent;
  border-bottom: 1px solid transparent;
  z-index: 100;
  transition: var(--transition);
}

.main-header.scrolled {
  background-color: var(--glass-bg);
  border-bottom: 1px solid var(--glass-border);
  backdrop-filter: blur(12px);
  box-shadow: var(--glass-shadow);
  height: 70px;
}

.header-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
}

/* Logo */
.logo {
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 800;
  letter-spacing: -0.5px;
  display: flex;
  align-items: center;
}

.logo-text {
  color: var(--text-primary);
}

.logo-accent {
  background: var(--primary-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* Desktop Nav */
.desktop-nav {
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-link, .dropdown-toggle {
  display: inline-flex;
  align-items: center;
  padding: 8px 16px;
  color: var(--text-secondary);
  font-size: 15px;
  font-weight: 500;
  border-radius: var(--radius-sm);
  gap: 4px;
  cursor: pointer;
}

.nav-link:hover, .dropdown-toggle:hover, .router-link-active {
  color: var(--text-primary);
  background-color: rgba(255, 255, 255, 0.05);
}

/* Chevron anim */
.chevron-icon {
  transition: var(--transition);
  opacity: 0.6;
}

.dropdown:hover .chevron-icon {
  transform: rotate(180deg);
}

/* Dropdown Menu */
.dropdown {
  position: relative;
  padding-bottom: 8px;
  margin-bottom: -8px;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%) translateY(10px);
  opacity: 0;
  visibility: hidden;
  width: 280px;
  background-color: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 8px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
  transition: var(--transition);
}

.dropdown:hover .dropdown-menu {
  opacity: 1;
  visibility: visible;
  transform: translateX(-50%) translateY(0);
}

.dropdown-item {
  display: block;
  padding: 10px 14px;
  border-radius: var(--radius-sm);
}

.dropdown-item:hover {
  background-color: rgba(255, 255, 255, 0.04);
}

.dropdown-title {
  font-weight: 600;
  font-size: 14px;
  color: var(--text-primary);
  margin-bottom: 2px;
}

.dropdown-desc {
  font-size: 12px;
  color: var(--text-muted);
  line-height: 1.4;
}

/* Actions */
.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.login-btn {
  display: inline-flex;
  padding: 10px 20px;
  background-color: transparent;
  border: 1px solid var(--primary);
  color: var(--primary);
  border-radius: var(--radius-full);
  font-size: 14px;
  font-weight: 600;
  transition: var(--transition);
}

.login-btn:hover {
  background: var(--primary-gradient);
  color: white;
  box-shadow: 0 4px 14px rgba(14, 165, 233, 0.3);
  border-color: transparent;
}

.icon-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  color: var(--text-secondary);
  border-radius: var(--radius-full);
  position: relative;
  transition: var(--transition);
}

.icon-btn:hover {
  background-color: rgba(255, 255, 255, 0.05);
  color: var(--text-primary);
}

.cart-badge {
  position: absolute;
  top: 4px;
  right: 4px;
  background-color: #ef4444;
  color: white;
  font-size: 10px;
  font-weight: 700;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Mobile Toggle */
.mobile-menu-toggle {
  display: none;
  flex-direction: column;
  justify-content: space-between;
  width: 24px;
  height: 18px;
}

.mobile-menu-toggle .bar {
  width: 100%;
  height: 2px;
  background-color: var(--text-primary);
  transition: var(--transition);
}

.mobile-menu-toggle .bar.open:nth-child(1) {
  transform: translateY(8px) rotate(45deg);
}

.mobile-menu-toggle .bar.open:nth-child(2) {
  opacity: 0;
}

.mobile-menu-toggle .bar.open:nth-child(3) {
  transform: translateY(-8px) rotate(-45deg);
}

/* Mobile Nav Overlay */
.mobile-nav {
  position: fixed;
  top: 80px;
  left: 0;
  width: 100%;
  height: calc(100vh - 80px);
  background-color: var(--bg-primary);
  z-index: 99;
  transform: translateX(100%);
  transition: var(--transition);
  padding: 24px;
  overflow-y: auto;
}

.main-header.scrolled + .main-content .mobile-nav {
  top: 70px;
  height: calc(100vh - 70px);
}

.mobile-nav.open {
  transform: translateX(0);
}

.mobile-nav-inner {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.mobile-nav-group {
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 12px;
}

.mobile-nav-label {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  cursor: pointer;
  padding: 8px 0;
}

.mobile-nav-links {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding-left: 16px;
  margin-top: 12px;
}

.mobile-nav-links a {
  color: var(--text-secondary);
  font-size: 15px;
}

.mobile-single-link {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  border-bottom: 1px solid var(--border-color);
  padding: 8px 0 20px 0;
}

.mobile-login-btn {
  display: block;
  text-align: center;
  padding: 14px;
  background: var(--primary-gradient);
  color: white;
  border-radius: var(--radius-md);
  font-weight: 600;
  margin-top: 16px;
}

/* Responsive */
@media (max-width: 1024px) {
  .desktop-nav {
    display: none;
  }
  
  .login-btn {
    display: none;
  }

  .mobile-menu-toggle {
    display: flex;
  }
}
</style>
