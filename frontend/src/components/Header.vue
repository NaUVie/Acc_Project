<template>
  <header class="main-header" :class="{ 'scrolled': isScrolled, 'header-hidden': isHidden }">
    <div class="container header-container">
      <!-- Logo -->
      <router-link to="/" class="logo">
        <img src="/images/logo3.png" alt="ACC Academy Logo" class="logo-image" />
      </router-link>

      <!-- Desktop Nav -->
      <nav class="desktop-nav">
        <!-- 1. VỀ CHÚNG TÔI -->
        <router-link to="/about-us" class="nav-link">VỀ CHÚNG TÔI</router-link>

        <!-- 2. ĐÀO TẠO -->
        <div class="nav-item dropdown">
          <router-link to="/courses" class="nav-link dropdown-toggle">
            ĐÀO TẠO
            <svg class="chevron-icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M6 9l6 6 6-6"/>
            </svg>
          </router-link>
          <div class="dropdown-menu">
            <router-link to="/courses" class="dropdown-item">
              <div class="dropdown-title">TẤT CẢ KHÓA HỌC</div>
              <div class="dropdown-desc">Khám phá toàn bộ các khóa học & chương trình đào tạo</div>
            </router-link>
            <router-link to="/courses/category/dao-tao-doanh-nghiep" class="dropdown-item">
              <div class="dropdown-title">ĐÀO TẠO INHOUSE</div>
              <div class="dropdown-desc">Các giải pháp đào tạo Inhouse & chuyển đổi số cho doanh nghiệp</div>
            </router-link>
            <router-link to="/courses/category/dao-tao-ca-nhan" class="dropdown-item">
              <div class="dropdown-title">ĐÀO TẠO CÁ NHÂN</div>
              <div class="dropdown-desc">Kỹ năng ứng dụng AI, chuyên môn & kỹ năng mềm cho cá nhân</div>
            </router-link>
          </div>
        </div>

        <!-- 3. TUYỂN SINH (Single Link) -->
        <router-link to="/tuyen-sinh" class="nav-link nav-link-admission">
          <span class="bell-ringing-icon">🔔</span>
          TUYỂN SINH
        </router-link>

        <!-- 4. ĐỐI TÁC TIN CẬY -->
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

        <!-- 5. TIN TỨC -->
        <router-link to="/library/blog" class="nav-link">TIN TỨC</router-link>

        <!-- 6. ĐỘI NGŨ GIẢNG VIÊN -->
        <router-link to="/doi-ngu-giang-vien" class="nav-link">ĐỘI NGŨ GIẢNG VIÊN</router-link>

        <!-- 7. DỰ ÁN -->
        <div class="nav-item dropdown">
          <router-link to="/du-an" class="nav-link dropdown-toggle">
            DỰ ÁN
            <svg class="chevron-icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M6 9l6 6 6-6"/>
            </svg>
          </router-link>
          <div class="dropdown-menu">
            <router-link to="/du-an?cat=du-an-doanh-nghiep" class="dropdown-item">
              <div class="dropdown-title">DỰ ÁN DOANH NGHIỆP</div>
              <div class="dropdown-desc">Các dự án đào tạo In-house & chuyển đổi số may đo cho doanh nghiệp</div>
            </router-link>
            <router-link to="/du-an?cat=du-an-ca-nhan" class="dropdown-item">
              <div class="dropdown-title">DỰ ÁN CÁ NHÂN</div>
              <div class="dropdown-desc">Các chương trình huấn luyện gia tốc năng lực 1:1 cho nhà quản lý</div>
            </router-link>
            <router-link to="/du-an?cat=du-an-nha-nuoc" class="dropdown-item">
              <div class="dropdown-title">DỰ ÁN NHÀ NƯỚC</div>
              <div class="dropdown-desc">Bồi dưỡng năng lực số & an toàn thông tin khối cơ quan - nhà nước</div>
            </router-link>
          </div>
        </div>

        <!-- 8. CHIA SẺ HỌC VIÊN -->
        <router-link to="/chia-se-hoc-vien" class="nav-link">CHIA SẺ HỌC VIÊN</router-link>

        <!-- 9. LIÊN HỆ -->
        <router-link to="/contact" class="nav-link">LIÊN HỆ</router-link>
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
        <!-- 1. VỀ CHÚNG TÔI -->
        <router-link to="/about-us" class="mobile-single-link" @click="closeMobileMenu">VỀ CHÚNG TÔI</router-link>

        <!-- 2. ĐÀO TẠO -->
        <div class="mobile-nav-group">
          <div class="mobile-nav-label" @click="toggleMobileSection('courses-menu')">
            ĐÀO TẠO
            <svg class="chevron-icon" :class="{ 'rotate': activeMobileSection === 'courses-menu' }" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M6 9l6 6 6-6"/>
            </svg>
          </div>
          <div class="mobile-nav-links" v-show="activeMobileSection === 'courses-menu'">
            <router-link to="/courses" @click="closeMobileMenu" class="mobile-single-sublink">Tất cả khóa học</router-link>
            <router-link to="/courses/category/dao-tao-doanh-nghiep" @click="closeMobileMenu" class="mobile-single-sublink">Đào tạo Inhouse</router-link>
            <router-link to="/courses/category/dao-tao-ca-nhan" @click="closeMobileMenu" class="mobile-single-sublink">Đào tạo cá nhân</router-link>
          </div>
        </div>

        <!-- 3. TUYỂN SINH -->
        <router-link to="/tuyen-sinh" class="mobile-single-link" @click="closeMobileMenu">TUYỂN SINH</router-link>

        <!-- 4. ĐỐI TÁC TIN CẬY -->
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

        <!-- 5. TIN TỨC -->
        <router-link to="/library/blog" class="mobile-single-link" @click="closeMobileMenu">TIN TỨC</router-link>

        <!-- 6. ĐỘI NGŨ GIẢNG VIÊN -->
        <router-link to="/doi-ngu-giang-vien" class="mobile-single-link" @click="closeMobileMenu">ĐỘI NGŨ GIẢNG VIÊN</router-link>

        <!-- 7. DỰ ÁN -->
        <div class="mobile-nav-group">
          <div class="mobile-nav-label" @click="toggleMobileSection('projects')">
            DỰ ÁN
            <svg class="chevron-icon" :class="{ 'rotate': activeMobileSection === 'projects' }" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M6 9l6 6 6-6"/>
            </svg>
          </div>
          <div class="mobile-nav-links" v-show="activeMobileSection === 'projects'">
            <router-link to="/du-an?cat=du-an-doanh-nghiep" @click="closeMobileMenu" class="mobile-single-sublink">DỰ ÁN DOANH NGHIỆP</router-link>
            <router-link to="/du-an?cat=du-an-ca-nhan" @click="closeMobileMenu" class="mobile-single-sublink">DỰ ÁN CÁ NHÂN</router-link>
            <router-link to="/du-an?cat=du-an-nha-nuoc" @click="closeMobileMenu" class="mobile-single-sublink">DỰ ÁN NHÀ NƯỚC</router-link>
          </div>
        </div>

        <!-- 8. CHIA SẺ HỌC VIÊN -->
        <router-link to="/chia-se-hoc-vien" class="mobile-single-link" @click="closeMobileMenu">CHIA SẺ HỌC VIÊN</router-link>

        <!-- 8. LIÊN HỆ -->
        <router-link to="/contact" class="mobile-single-link" @click="closeMobileMenu">LIÊN HỆ</router-link>
        
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
          <a href="https://zalo.me/0938566700" target="_blank" rel="noopener" class="drawer-zalo-btn" aria-label="Chat Zalo">
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
  const defaultBase = [
    { id: 'dao-tao-doanh-nghiep', name: 'Đào tạo cho doanh nghiệp', viewAllLink: '/courses/category/dao-tao-doanh-nghiep' },
    { id: 'dao-tao-ca-nhan', name: 'Đào tạo cho cá nhân', viewAllLink: '/courses/category/dao-tao-ca-nhan' },
    { id: 'dao-tao-co-quan-nha-nuoc', name: 'Đào tạo cho khối cơ quan - nhà nước', viewAllLink: '/courses/category/dao-tao-co-quan-nha-nuoc' },
    { id: 'bundles', name: 'Combo khóa học', viewAllLink: '/bundles' }
  ];
  let baseList = [];
  if (courseStore.categories && courseStore.categories.length > 0) {
    const validSlugs = ['dao-tao-doanh-nghiep', 'dao-tao-ca-nhan', 'dao-tao-co-quan-nha-nuoc', 'bundles'];
    const filtered = courseStore.categories.filter(c => validSlugs.includes(c.slug));
    if (filtered.length > 0) {
      baseList = filtered.map(c => ({
        id: c.slug,
        name: c.name,
        viewAllLink: c.slug === 'bundles' ? '/bundles' : `/courses/category/${c.slug}`
      }));
    } else {
      baseList = defaultBase;
    }
  } else {
    baseList = defaultBase;
  }
  return [
    ...baseList,
    { id: 'corporate', name: 'Đào tạo Doanh nghiệp', viewAllLink: '/corporate/dao-tao' }
  ];
});

const selectedCategory = ref('dao-tao-doanh-nghiep');

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
        { title: '🎓 MBA ANDREW (Thạc sĩ Quản trị Kinh doanh Hoa Kỳ)', link: '/tuyen-sinh#mba' },
        // { title: '⚡ MINI MBA Practical (Quản trị Tinh gọn)', link: '/tuyen-sinh#mini-mba' },
        { title: '🌐 GEL (Global Executive Leadership)', link: '/tuyen-sinh#gel' }
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
    const tasks = [];
    if (courseStore.courses.length === 0) {
      tasks.push(courseStore.fetchCourses());
    }
    if (courseStore.programs.length === 0) {
      tasks.push(courseStore.fetchPrograms());
    }
    if (tasks.length > 0) {
      await Promise.all(tasks);
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
