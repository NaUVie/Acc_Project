<template>
  <header class="main-header" :class="{ 'scrolled': isScrolled }">
    <div class="container header-container">
      <!-- Logo -->
      <router-link to="/" class="logo">
        <span class="logo-text">ACC <span class="logo-accent">Academy</span></span>
      </router-link>

      <!-- Desktop Nav -->
      <nav class="desktop-nav">
        <!-- Mega Menu: Chương trình -->
        <div class="nav-item mega-dropdown">
          <button class="nav-link dropdown-toggle" aria-haspopup="true" @click.prevent="openDrawer('programs')">
            Chương trình
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
                  <router-link to="/courses/ai" class="mega-view-all-link">
                    Xem tất cả {{ activeCategoryName }} chương trình &rarr;
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

        <!-- Dropdown: Bundle chương trình -->
        <div class="nav-item dropdown">
          <button class="nav-link dropdown-toggle" @click.prevent="openDrawer('bundles')">
            Bundle chương trình
            <svg class="chevron-icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M6 9l6 6 6-6"/>
            </svg>
          </button>
          <div class="dropdown-menu">
            <router-link to="/bundles" class="dropdown-item">
              <div class="dropdown-title">Combo khóa học</div>
              <div class="dropdown-desc">Các gói combo tiết kiệm và lộ trình học toàn diện</div>
            </router-link>
          </div>
        </div>

        <!-- Dropdown: Doanh nghiệp -->
        <div class="nav-item dropdown">
          <button class="nav-link dropdown-toggle" @click.prevent="openDrawer('corporate')">
            Doanh nghiệp
            <svg class="chevron-icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M6 9l6 6 6-6"/>
            </svg>
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

        <!-- Dropdown: Thư viện -->
        <div class="nav-item dropdown">
          <button class="nav-link dropdown-toggle" @click.prevent="openDrawer('library')">
            Thư viện
            <svg class="chevron-icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M6 9l6 6 6-6"/>
            </svg>
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
        <router-link to="/login" class="login-btn">Đăng nhập học viên</router-link>
        
        <button class="icon-btn" aria-label="Tìm kiếm">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"/>
            <path d="M21 21l-4.35-4.35"/>
          </svg>
        </button>
        
        <router-link to="/cart" class="icon-btn cart-btn" aria-label="Giỏ hàng">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/>
            <line x1="3" y1="6" x2="21" y2="6"/>
            <path d="M16 10a4 4 0 0 1-8 0"/>
          </svg>
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
        <!-- Mobile Accordion: Chương trình -->
        <div class="mobile-nav-group">
          <div class="mobile-nav-label" @click="toggleMobileSection('programs')">
            Chương trình
            <svg class="chevron-icon" :class="{ 'rotate': activeMobileSection === 'programs' }" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M6 9l6 6 6-6"/>
            </svg>
          </div>
          <div class="mobile-nav-links" v-show="activeMobileSection === 'programs'">
            <div v-for="cat in categories" :key="cat.id" class="mobile-sub-group">
              <div class="mobile-sub-label" @click="toggleMobileSubSection(cat.id)">
                <span>{{ cat.name }}</span>
                <span class="plus-icon">{{ activeMobileSubSection === cat.id ? '−' : '+' }}</span>
              </div>
              <div class="mobile-sub-content" v-show="activeMobileSubSection === cat.id">
                <router-link 
                  v-for="program in getProgramsByCategoryId(cat.id)" 
                  :key="program.id" 
                  :to="program.link" 
                  @click="closeMobileMenu"
                  class="mobile-sub-link"
                >
                  {{ program.title }}
                </router-link>
              </div>
            </div>
          </div>
        </div>

        <!-- Mobile Accordion: Bundle chương trình -->
        <div class="mobile-nav-group">
          <div class="mobile-nav-label" @click="toggleMobileSection('bundles')">
            Bundle chương trình
            <svg class="chevron-icon" :class="{ 'rotate': activeMobileSection === 'bundles' }" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M6 9l6 6 6-6"/>
            </svg>
          </div>
          <div class="mobile-nav-links" v-show="activeMobileSection === 'bundles'">
            <router-link to="/bundles" @click="closeMobileMenu">Combo khóa học</router-link>
          </div>
        </div>

        <!-- Mobile Accordion: Doanh nghiệp -->
        <div class="mobile-nav-group">
          <div class="mobile-nav-label" @click="toggleMobileSection('corporate')">
            Doanh nghiệp
            <svg class="chevron-icon" :class="{ 'rotate': activeMobileSection === 'corporate' }" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M6 9l6 6 6-6"/>
            </svg>
          </div>
          <div class="mobile-nav-links" v-show="activeMobileSection === 'corporate'">
            <router-link to="/corporate/dao-tao" @click="closeMobileMenu">Đào tạo doanh nghiệp</router-link>
            <router-link to="/corporate/coe" @click="closeMobileMenu">AI Center of Excellence</router-link>
            <router-link to="/corporate/for-team" @click="closeMobileMenu">AI for Team</router-link>
            <router-link to="/corporate/case-studies" @click="closeMobileMenu">Câu chuyện đào tạo</router-link>
          </div>
        </div>

        <!-- Mobile Accordion: Thư viện -->
        <div class="mobile-nav-group">
          <div class="mobile-nav-label" @click="toggleMobileSection('library')">
            Thư viện
            <svg class="chevron-icon" :class="{ 'rotate': activeMobileSection === 'library' }" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M6 9l6 6 6-6"/>
            </svg>
          </div>
          <div class="mobile-nav-links" v-show="activeMobileSection === 'library'">
            <router-link to="/library/blog" @click="closeMobileMenu">Thư viện bài viết</router-link>
            <router-link to="/library/recipes" @click="closeMobileMenu">Công thức viết prompt</router-link>
          </div>
        </div>

        <router-link to="/contact" class="mobile-single-link" @click="closeMobileMenu">Liên hệ</router-link>
        <router-link to="/about-us" class="mobile-single-link" @click="closeMobileMenu">Về chúng tôi</router-link>
        
        <router-link to="/login" class="mobile-login-btn" @click="closeMobileMenu">Đăng nhập học viên</router-link>
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
            <router-link 
              v-for="item in drawerItems" 
              :key="item.link"
              :to="item.link" 
              @click="closeDrawer"
              class="drawer-link-item"
            >
              {{ item.title }}
            </router-link>
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
  </header>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue';

const isScrolled = ref(false);
const isMobileMenuOpen = ref(false);
const activeMobileSection = ref('');
const activeMobileSubSection = ref('');

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

// 1. Mega Menu Categories Data
const categories = [
  { id: 'tien-si', name: 'Tiến Sĩ' },
  { id: 'giao-duc', name: 'Giáo dục' },
  { id: 'cxo', name: 'CXO / Ban điều hành' },
  { id: 'thac-si', name: 'Thạc sĩ Quản trị' },
  { id: 'data-science', name: 'Khoa học Dữ liệu' },
  { id: 'ai-learning', name: 'Học Máy & AI' },
  { id: 'quan-tri', name: 'Quản trị' },
  { id: 'du-hoc', name: 'Du học' }
];

const selectedCategory = ref('tien-si');

// 2. Mega Menu Programs Dataset mapping with local verified logos
const programs = [
  // Tiến sĩ
  { id: 101, categoryId: 'tien-si', title: 'Tiến sĩ Quản trị Kinh doanh (DBA)', school: 'RMIT University', logo: '/images/RMIT.png', link: '/courses/chuyen-mon' },
  { id: 102, categoryId: 'tien-si', title: 'Tiến sĩ Khoa học Máy tính & AI', school: 'FPT Education', logo: '/images/FPT.png', link: '/courses/ai' },
  { id: 103, categoryId: 'tien-si', title: 'Tiến sĩ Quản lý Giáo dục Đột phá', school: 'BUV University', logo: '/images/BUV.png', link: '/courses/mem' },
  
  // Giáo dục
  { id: 201, categoryId: 'giao-duc', title: 'Thạc sĩ Quản lý Giáo dục Quốc tế', school: 'BUV University', logo: '/images/BUV.png', link: '/courses/mem' },
  { id: 202, categoryId: 'giao-duc', title: 'Phương pháp Giảng dạy Hiện đại', school: 'RMIT University', logo: '/images/RMIT.png', link: '/courses/mem' },
  { id: 203, categoryId: 'giao-duc', title: 'Chứng chỉ Đào tạo Chuyên nghiệp', school: 'FPT Education', logo: '/images/FPT.png', link: '/courses/mem' },
  
  // CXO
  { id: 301, categoryId: 'cxo', title: 'Giám đốc Điều hành Chuyên nghiệp (CEO)', school: 'RMIT University', logo: '/images/RMIT.png', link: '/courses/chuyen-mon' },
  { id: 302, categoryId: 'cxo', title: 'Giám đốc Công nghệ & AI (CTO)', school: 'Google Academy', logo: '/images/Google.png', link: '/courses/ai' },
  { id: 303, categoryId: 'cxo', title: 'Giám đốc Chiến lược Số (CSO)', school: 'Axon Active', logo: '/images/AXON.png', link: '/courses/chuyen-mon' },
  
  // Thạc sĩ
  { id: 401, categoryId: 'thac-si', title: 'Thạc sĩ Quản trị Kinh doanh Quốc tế (MBA)', school: 'BUV University', logo: '/images/BUV.png', link: '/bundles' },
  { id: 402, categoryId: 'thac-si', title: 'Thạc sĩ Vận hành Chuỗi cung ứng', school: 'RMIT University', logo: '/images/RMIT.png', link: '/bundles' },
  { id: 403, categoryId: 'thac-si', title: 'Thạc sĩ Tài chính Doanh nghiệp', school: 'FPT Education', logo: '/images/FPT.png', link: '/bundles' },
  
  // Data Science
  { id: 501, categoryId: 'data-science', title: 'Chuyên viên Phân tích Dữ liệu (DA)', school: 'Google Academy', logo: '/images/Google.png', link: '/courses/chuyen-mon' },
  { id: 502, categoryId: 'data-science', title: 'Khoa học Dữ liệu Thực chiến (DS)', school: 'RMIT University', logo: '/images/RMIT.png', link: '/courses/chuyen-mon' },
  { id: 503, categoryId: 'data-science', title: 'Phân tích Dữ liệu với Python', school: 'Bosch Global', logo: '/images/BOSCH.png', link: '/courses/chuyen-mon' },
  
  // AI
  { id: 601, categoryId: 'ai-learning', title: 'Kỹ sư Học máy & Học sâu', school: 'Google Academy', logo: '/images/Google.png', link: '/courses/ai' },
  { id: 602, categoryId: 'ai-learning', title: 'Ứng dụng ChatGPT & GenAI Vận hành', school: 'FPT Education', logo: '/images/FPT.png', link: '/courses/ai' },
  { id: 603, categoryId: 'ai-learning', title: 'Phát triển Sản phẩm AI', school: 'Axon Active', logo: '/images/AXON.png', link: '/courses/ai' },
  
  // Quản trị
  { id: 701, categoryId: 'quan-tri', title: 'Quản trị Doanh nghiệp Vừa và Nhỏ', school: 'RMIT University', logo: '/images/RMIT.png', link: '/courses/chuyen-mon' },
  { id: 702, categoryId: 'quan-tri', title: 'Quản trị Dự án Chuẩn Agile/Scrum', school: 'Axon Active', logo: '/images/AXON.png', link: '/courses/chuyen-mon' },
  { id: 703, categoryId: 'quan-tri', title: 'Năng lực Lãnh đạo Khởi nghiệp', school: 'BUV University', logo: '/images/BUV.png', link: '/courses/chuyen-mon' },
  
  // Du học
  { id: 801, categoryId: 'du-hoc', title: 'Chương trình Chuyển tiếp RMIT Melbourne', school: 'RMIT University', logo: '/images/RMIT.png', link: '/about-us' },
  { id: 802, categoryId: 'du-hoc', title: 'Cử nhân Anh Quốc Song bằng BUV', school: 'BUV University', logo: '/images/BUV.png', link: '/about-us' },
  { id: 803, categoryId: 'du-hoc', title: 'Liên kết Đào tạo Công nghệ Toàn cầu', school: 'FPT Education', logo: '/images/FPT.png', link: '/about-us' }
];

const filteredPrograms = computed(() => {
  return programs.filter(p => p.categoryId === selectedCategory.value);
});

const activeCategoryName = computed(() => {
  const cat = categories.find(c => c.id === selectedCategory.value);
  return cat ? cat.name : '';
});

const getProgramsByCategoryId = (catId) => {
  return programs.filter(p => p.categoryId === catId);
};

// Drawer Title & Items computation
const drawerTitle = computed(() => {
  switch (drawerType.value) {
    case 'programs': return 'Chương trình';
    case 'bundles': return 'Gói Combo chương trình';
    case 'corporate': return 'Giải pháp Doanh nghiệp';
    case 'library': return 'Thư viện & Tài liệu';
    default: return '';
  }
});

const drawerItems = computed(() => {
  switch (drawerType.value) {
    case 'programs':
      return [
        { title: 'Kỹ năng AI', link: '/courses/ai' },
        { title: 'Kỹ năng mềm', link: '/courses/mem' },
        { title: 'Kỹ năng chuyên môn', link: '/courses/chuyen-mon' }
      ];
    case 'bundles':
      return [
        { title: 'Combo khóa học', link: '/bundles' }
      ];
    case 'corporate':
      return [
        { title: 'Đào tạo doanh nghiệp', link: '/corporate/dao-tao' },
        { title: 'AI Center of Excellence', link: '/corporate/coe' },
        { title: 'AI for Team', link: '/corporate/for-team' },
        { title: 'Câu chuyện đào tạo', link: '/corporate/case-studies' }
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

const handleScroll = () => {
  isScrolled.value = window.scrollY > 20;
};

onMounted(() => {
  window.addEventListener('scroll', handleScroll);
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
  document.body.classList.remove('lock-scroll'); // teardown scroll lock safety
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
  z-index: 1002;
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
  gap: 6px;
  cursor: pointer;
  background: transparent;
  border: none;
}

.nav-link:hover, .dropdown-toggle:hover, .router-link-active {
  color: var(--text-primary);
  background-color: rgba(255, 255, 255, 0.05);
}

.chevron-icon {
  transition: var(--transition);
  opacity: 0.6;
}

.nav-item:hover .chevron-icon {
  transform: rotate(180deg);
}

/* Standard Dropdown Menu */
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
  background-color: #ffffff;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: var(--radius-md);
  padding: 8px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
  transition: var(--transition);
  z-index: 1001;
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
  background-color: rgba(0, 0, 0, 0.03);
}

.dropdown-title {
  font-weight: 600;
  font-size: 14px;
  color: #0f172a;
  margin-bottom: 2px;
}

.dropdown-desc {
  font-size: 12px;
  color: #64748b;
  line-height: 1.4;
}

/* ==========================================================================
   MEGA MENU STYLES
   ========================================================================== */
.mega-dropdown {
  position: static;
}

.mega-menu-panel {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  background-color: #ffffff;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
  opacity: 0;
  visibility: hidden;
  transform: translateY(15px);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 999;
}

.mega-dropdown:hover .mega-menu-panel {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.mega-menu-container {
  display: grid;
  grid-template-columns: 280px 1fr;
  height: 480px;
  padding: 0;
}

/* Sidebar Column */
.mega-menu-sidebar {
  background-color: #f8fafc;
  padding: 24px 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  overflow-y: auto;
  border-right: 1px solid rgba(0, 0, 0, 0.06);
}

.mega-sidebar-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  background: transparent;
  border: none;
  color: #475467;
  font-size: 14px;
  font-weight: 600;
  text-align: left;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  transition: all 0.2s ease;
}

.mega-sidebar-item .indicator-bar {
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 0;
  background-color: #022B9F; /* Royal Blue */
  transition: height 0.25s ease;
  border-radius: 0 2px 2px 0;
}

.mega-sidebar-item:hover,
.mega-sidebar-item.active {
  color: #022B9F;
  background-color: rgba(2, 43, 159, 0.05);
}

.mega-sidebar-item:hover .indicator-bar,
.mega-sidebar-item.active .indicator-bar {
  height: 60%;
}

.mega-sidebar-item.active {
  background-color: rgba(2, 43, 159, 0.08);
}

/* Right Content Column */
.mega-menu-content {
  background-color: #ffffff;
  padding: 32px 40px;
  display: flex;
  flex-direction: column;
  gap: 24px;
  overflow-y: auto;
}

.mega-content-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
  padding-bottom: 16px;
}

.mega-content-title {
  font-size: 20px;
  font-weight: 800;
  color: #0f172a;
  margin: 0;
}

.mega-view-all-link {
  font-size: 13px;
  font-weight: 700;
  color: #022B9F !important;
  text-decoration: none;
  transition: color 0.2s ease;
}

.mega-view-all-link:hover {
  color: #38bdf8 !important;
}

/* Program Card Grid */
.mega-programs-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.mega-program-card {
  background-color: #ffffff;
  border: 1px solid rgba(0, 0, 0, 0.06);
  border-radius: 10px;
  padding: 16px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.mega-program-card:hover {
  transform: translateY(-2px);
  background-color: #f8fafc;
  border-color: rgba(2, 43, 159, 0.15);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.04);
}

.mega-card-link {
  display: flex;
  gap: 12px;
  align-items: center;
  text-decoration: none;
  height: 100%;
}

.mega-school-logo {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  background-color: #ffffff;
  padding: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.mega-school-logo img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.mega-card-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  overflow: hidden;
}

.mega-school-name {
  color: #022B9F; /* Royal Blue */
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.mega-program-title {
  color: #1e293b;
  font-size: 13px;
  font-weight: 600;
  line-height: 1.4;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  transition: color 0.2s ease;
}

.mega-program-card:hover .mega-program-title {
  color: #022B9F;
}

/* Custom Scrollbars */
.mega-menu-sidebar::-webkit-scrollbar,
.mega-menu-content::-webkit-scrollbar,
.drawer-panel::-webkit-scrollbar {
  width: 6px;
}

.mega-menu-sidebar::-webkit-scrollbar-track,
.mega-menu-content::-webkit-scrollbar-track {
  background: transparent;
}

.mega-menu-sidebar::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.08);
  border-radius: 3px;
}

.mega-menu-content::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.1);
  border-radius: 3px;
}

/* ==========================================================================
   OFF-CANVAS DRAWER SIDEBAR STYLES
   ========================================================================== */
:global(body.lock-scroll) {
  overflow: hidden !important;
}

.drawer-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  z-index: 1999;
}

.drawer-panel {
  position: fixed;
  top: 0;
  left: 0;
  width: 380px;
  max-width: 100vw;
  height: 100vh;
  background-color: #ffffff;
  border-right: 1px solid rgba(0, 0, 0, 0.08);
  box-shadow: 20px 0 50px rgba(0, 0, 0, 0.05);
  z-index: 2000;
  padding: 40px;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
}

.drawer-header {
  display: flex;
  justify-content: flex-start;
  margin-bottom: 40px;
}

.drawer-close-btn {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background-color: rgba(0, 0, 0, 0.03);
  border: 1px solid rgba(0, 0, 0, 0.08);
  color: #0f172a;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.drawer-close-btn:hover {
  background-color: #0f172a;
  color: #ffffff;
  transform: rotate(90deg);
}

.drawer-body {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.drawer-tagline {
  font-size: 11px;
  font-weight: 700;
  color: #022B9F; /* Royal Blue */
  text-transform: uppercase;
  letter-spacing: 2px;
  margin-bottom: 8px;
}

.drawer-title {
  font-size: 24px;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 40px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
  padding-bottom: 16px;
}

.drawer-links-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.drawer-link-item {
  font-size: 22px;
  font-weight: 700;
  color: #334155;
  text-decoration: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: inline-block;
  align-self: flex-start;
}

.drawer-link-item:hover {
  color: #022B9F; /* Royal Blue */
  transform: translateX(12px);
}

.drawer-footer {
  margin-top: auto;
  padding-top: 24px;
  border-top: 1px solid rgba(0, 0, 0, 0.08);
  display: flex;
  align-items: center;
  justify-content: flex-start;
}

.drawer-zalo-btn {
  text-decoration: none;
  display: inline-block;
}

.zalo-bubble {
  background-color: #0068ff;
  color: #ffffff;
  font-family: var(--font-sans);
  font-weight: 800;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  box-shadow: 0 4px 12px rgba(0, 104, 255, 0.3);
  transition: all 0.3s ease;
}

.zalo-bubble:hover {
  transform: scale(1.08);
  box-shadow: 0 6px 16px rgba(0, 104, 255, 0.5);
}

/* Vue Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-enter-active,
.slide-leave-active {
  transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(-100%);
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
  background: none;
  border: none;
  cursor: pointer;
  z-index: 1002;
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

/* Mobile Sub Accordion for Program Categories */
.mobile-sub-group {
  margin-bottom: 8px;
}

.mobile-sub-label {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  padding: 6px 0;
  cursor: pointer;
}

.mobile-sub-label .plus-icon {
  font-size: 16px;
  color: var(--primary);
}

.mobile-sub-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding-left: 12px;
  border-left: 2px solid rgba(2, 43, 159, 0.2);
  margin-top: 4px;
  margin-bottom: 8px;
}

.mobile-sub-link {
  font-size: 13px;
  color: var(--text-secondary) !important;
  text-decoration: none;
  padding: 4px 0;
}

.mobile-single-link {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  border-bottom: 1px solid var(--border-color);
  padding: 8px 0 20px 0;
  text-decoration: none;
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
  text-decoration: none;
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
