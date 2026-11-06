<template>
  <header class="main-header" :class="{ 'scrolled': isScrolled, 'header-hidden': isHidden }">
    <div class="container header-container">
      <!-- Logo -->
      <router-link to="/" class="logo">
        <img src="/images/logo3.png" alt="ACC Academy Logo" class="logo-image" />
      </router-link>

      <!-- Desktop Nav -->
      <nav class="desktop-nav">
        <!-- 1. VỀ CHÚNG TÔI (Dropdown: Giới thiệu, Đội ngũ giảng viên, Đối tác) -->
        <div class="nav-item dropdown">
          <router-link to="/about-us" class="nav-link dropdown-toggle" :class="{ 'router-link-active': isAboutActive }">
            {{ $t("nav.about").toUpperCase() }}
            <svg class="chevron-icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M6 9l6 6 6-6"/>
            </svg>
          </router-link>
          <div class="dropdown-menu">
            <router-link to="/about-us" class="dropdown-item">
              <div class="dropdown-title">{{ $t("nav.aboutIntro").toUpperCase() }}</div>
              <div class="dropdown-desc">Tầm nhìn, sứ mệnh & giá trị cốt lõi của ACC Academy</div>
            </router-link>
            <router-link to="/lecturers" class="dropdown-item">
              <div class="dropdown-title">{{ $t("nav.lecturers").toUpperCase() }}</div>
              <div class="dropdown-desc">Đội ngũ chuyên gia, học giả & lãnh đạo doanh nghiệp hàng đầu</div>
            </router-link>
            <a href="javascript:void(0)" class="dropdown-item" @click.prevent="openDrawer('trusted-partners')">
              <div class="dropdown-title">{{ $t("nav.partners").toUpperCase() }}</div>
              <div class="dropdown-desc">MBA Đại học Andrews, Hoa Kỳ & Viện Leadman</div>
            </a>
          </div>
        </div>

        <!-- 2. LĨNH VỰC (Dropdown: Tuyển sinh, Đào tạo) -->
        <div class="nav-item dropdown">
          <router-link to="/courses" class="nav-link dropdown-toggle" :class="{ 'router-link-active': isFieldsActive }">
            {{ $t("nav.fields").toUpperCase() }}
            <svg class="chevron-icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M6 9l6 6 6-6"/>
            </svg>
          </router-link>
          <div class="dropdown-menu">
            <router-link to="/admissions" class="dropdown-item">
              <div class="dropdown-title">
                <span class="bell-ringing-icon" style="margin-right: 4px;">🔔</span>
                {{ $t("nav.admissions").toUpperCase() }}
              </div>
              <div class="dropdown-desc">Thạc sĩ MBA Andrews Hoa Kỳ & Hội thảo Lãnh đạo cấp cao GEI</div>
            </router-link>
            <router-link to="/courses" class="dropdown-item">
              <div class="dropdown-title">{{ $t("nav.courses").toUpperCase() }}</div>
              <div class="dropdown-desc">Các chương trình đào tạo Doanh nghiệp, Cá nhân & Khối Nhà nước</div>
            </router-link>
          </div>
        </div>

        <!-- 3. TIN TỨC -->
        <router-link to="/library/blog" class="nav-link">{{ $t("nav.blog").toUpperCase() }}</router-link>

        <!-- 5. CHIA SẺ HỌC VIÊN -->
        <router-link to="/testimonials" class="nav-link">{{ $t("nav.testimonials").toUpperCase() }}</router-link>

        <!-- 6. LIÊN HỆ -->
        <router-link to="/contact" class="nav-link">{{ $t("nav.contact").toUpperCase() }}</router-link>
      </nav>

      <!-- Action buttons -->
      <div class="header-actions">
        <router-link v-if="!courseStore.token" to="/login" class="login-btn">{{ $t('header.login') }}</router-link>
        
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
                <span class="dropdown-icon">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="3" width="7" height="7"></rect>
                    <rect x="14" y="3" width="7" height="7"></rect>
                    <rect x="14" y="14" width="7" height="7"></rect>
                    <rect x="3" y="14" width="7" height="7"></rect>
                  </svg>
                </span>
                <div class="dropdown-link-text">
                  <span class="link-title">{{ $t("header.adminPanel") }}</span>
                  <span class="link-desc">Quản lý khóa học, đơn hàng & học viên</span>
                </div>
              </router-link>

              <router-link :to="currentLang === 'en' ? '/en/dashboard' : '/dashboard'" class="user-dropdown-link" @click="isUserDropdownOpen = false">
                <span class="dropdown-icon">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                    <circle cx="12" cy="7" r="4"></circle>
                  </svg>
                </span>
                <div class="dropdown-link-text">
                  <span class="link-title">{{ $t("header.profile") }}</span>
                  <span class="link-desc">Thông tin cá nhân & khóa học</span>
                </div>
              </router-link>
            </div>

            <div class="user-dropdown-divider"></div>

            <button class="user-dropdown-logout" @click="handleLogout">
              <span class="dropdown-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                  <polyline points="16 17 21 12 16 7"></polyline>
                  <line x1="21" y1="12" x2="9" y2="12"></line>
                </svg>
              </span>
              <span>{{ $t("header.logout") }}</span>
            </button>
          </div>
        </div>
        
        <button class="icon-btn" aria-label="Tìm kiếm" @click="isSearchOpen = true">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"/>
            <path d="M21 21l-4.35-4.35"/>
          </svg>
        </button>

        <!-- Language Switcher Pill Button -->
        <button 
          class="lang-header-btn" 
          :title="currentLang === 'vi' ? 'Switch to English' : 'Chuyển sang Tiếng Việt'"
          @click="toggleLang"
          aria-label="Toggle Language"
        >
          <span class="lang-flag">{{ currentLang === 'vi' ? '🇻🇳' : '🇬🇧' }}</span>
          <span class="lang-code">{{ currentLang.toUpperCase() }}</span>
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
        <!-- 1. VỀ CHÚNG TÔI (Dropdown: Giới thiệu, Đội ngũ giảng viên, Đối tác) -->
        <div class="mobile-nav-group">
          <div class="mobile-nav-label" @click="toggleMobileSection('about-menu')">
            {{ $t("nav.about").toUpperCase() }}
            <svg class="chevron-icon" :class="{ 'rotate': activeMobileSection === 'about-menu' }" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M6 9l6 6 6-6"/>
            </svg>
          </div>
          <div class="mobile-nav-links" v-show="activeMobileSection === 'about-menu'">
            <router-link to="/about-us" @click="closeMobileMenu" class="mobile-single-sublink">{{ $t("nav.aboutIntro").toUpperCase() }}</router-link>
            <router-link to="/lecturers" @click="closeMobileMenu" class="mobile-single-sublink">{{ $t("nav.lecturers").toUpperCase() }}</router-link>
            <a href="javascript:void(0)" @click="closeMobileMenu(); openDrawer('trusted-partners')" class="mobile-single-sublink">{{ $t("nav.partners").toUpperCase() }}</a>
          </div>
        </div>

        <!-- 2. LĨNH VỰC (Dropdown: Tuyển sinh, Đào tạo) -->
        <div class="mobile-nav-group">
          <div class="mobile-nav-label" @click="toggleMobileSection('fields-menu')">
            {{ $t("nav.fields").toUpperCase() }}
            <svg class="chevron-icon" :class="{ 'rotate': activeMobileSection === 'fields-menu' }" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M6 9l6 6 6-6"/>
            </svg>
          </div>
          <div class="mobile-nav-links" v-show="activeMobileSection === 'fields-menu'">
            <router-link to="/admissions" @click="closeMobileMenu" class="mobile-single-sublink">
              <span class="bell-ringing-icon" style="margin-right: 4px;">🔔</span>
              {{ $t("nav.admissions").toUpperCase() }}
            </router-link>
            <router-link to="/courses" @click="closeMobileMenu" class="mobile-single-sublink">{{ $t("nav.courses").toUpperCase() }}</router-link>
          </div>
        </div>

        <!-- 3. TIN TỨC -->
        <router-link to="/library/blog" class="mobile-single-link" @click="closeMobileMenu">{{ $t("nav.blog").toUpperCase() }}</router-link>

        <!-- 8. CHIA SẺ HỌC VIÊN -->
        <router-link to="/testimonials" class="mobile-single-link" @click="closeMobileMenu">{{ $t("nav.testimonials").toUpperCase() }}</router-link>

        <!-- 8. LIÊN HỆ -->
        <router-link to="/contact" class="mobile-single-link" @click="closeMobileMenu">{{ $t("nav.contact").toUpperCase() }}</router-link>
        
        <div class="mobile-lang-row" style="margin-bottom: 12px; display: flex; align-items: center; justify-content: space-between; padding: 10px 14px; background: #f8fafc; border-radius: 8px; border: 1px solid #e2e8f0;">
          <span style="font-size: 13px; color: #475569; font-weight: 600;">{{ $t('header.switchLang') }}:</span>
          <button type="button" class="lang-switch-btn" @click="toggleLang">
            <span>{{ currentLang === 'vi' ? '🇻🇳 Tiếng Việt' : '🇬🇧 English' }}</span>
          </button>
        </div>
        <router-link v-if="!courseStore.token" to="/login" class="mobile-login-btn" @click="closeMobileMenu">{{ $t("header.login") }}</router-link>
        <div v-else class="mobile-user-menu" style="display: flex; flex-direction: column; gap: 8px; width: 100%;">
          <router-link v-if="courseStore.userMe?.role === 'admin'" to="/admin" class="mobile-login-btn" style="background: var(--primary-gradient); color: white;" @click="closeMobileMenu">👑 Quản trị hệ thống</router-link>
          <router-link :to="currentLang === 'en' ? '/en/dashboard' : '/dashboard'" class="mobile-login-btn" @click="closeMobileMenu">🙋‍♂️ {{ courseStore.userMe?.fullname || 'Học viên' }}</router-link>
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

    <!-- Slide-over Search -->
    <SlideOverSearch
      :isOpen="isSearchOpen"
      @close="isSearchOpen = false"
    />
  </header>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { setLanguage } from '@/i18n';
import { clearGoogleTranslate } from '@/utils/googleTranslate';
import { useCourseStore } from '@/stores/courses';
import { slugify } from '@/utils/slugify';
import SlideOverSearch from '@/components/SlideOverSearch.vue';

const router = useRouter();
const route = useRoute();

const isAboutActive = computed(() => {
  return ['/about-us', '/lecturers'].some(p => route.path.startsWith(p));
});

const isFieldsActive = computed(() => {
  return ['/courses', '/admissions', '/course/'].some(p => route.path.startsWith(p));
});
const courseStore = useCourseStore();
const { locale } = useI18n();

const isEnActive = () => {
  if (locale.value === 'en') return true;
  if (typeof document !== 'undefined') {
    if (document.cookie.includes('googtrans=/vi/en') || document.documentElement.classList.contains('translated-ltr')) {
      return true;
    }
  }
  if (typeof window !== 'undefined' && localStorage.getItem('acc_lang') === 'en') {
    return true;
  }
  return false;
};

const currentLang = computed(() => isEnActive() ? 'en' : 'vi');

const toggleLang = () => {
  const route = router.currentRoute.value;
  const isEnCurrently = isEnActive();

  // Functional / admin pages have no /en version: just switch the UI language in place
  if ((route.meta && route.meta.noLocale) || route.path.startsWith('/admin')) {
    const nextLang = isEnCurrently ? 'vi' : 'en';
    if (nextLang === 'vi') {
      clearGoogleTranslate();
      setLanguage('vi');
    } else {
      setLanguage('en');
    }
    window.location.reload();
    return;
  }
  const currentPath = route.fullPath;
  if (!isEnCurrently) {
    setLanguage('en');
    let newPath = '/en' + (currentPath === '/' ? '' : currentPath);
    if (!newPath) newPath = '/en';
    window.location.href = newPath;
  } else {
    clearGoogleTranslate();
    setLanguage('vi');
    let newPath = currentPath.replace(/^\/en(\/|$)/, '/');
    if (!newPath) newPath = '/';
    window.location.href = newPath;
  }
};

// Dynamic categories for Navigation Header
const navCategories = computed(() => {
  const cats = courseStore.categories || [];
  return cats.filter(c => c.slug !== 'bundles');
});

const getCategoryLink = (cat) => {
  return '/courses/category/' + cat.slug;
};

const getCategoryDesc = (cat) => {
  if (cat.description) return cat.description;
  const s = (cat.slug || '').toLowerCase();
  if (s.includes('inhouse') || s.includes('doanh-nghiep')) {
    return 'Các giải pháp đào tạo Inhouse & chuyển đổi số cho doanh nghiệp';
  }
  if (s.includes('ca-nhan')) {
    return 'Kỹ năng ứng dụng AI, chuyên môn & kỹ năng mềm cho cá nhân';
  }
  if (s.includes('nha-nuoc')) {
    return 'Bồi dưỡng năng lực số cho khối cơ quan - nhà nước';
  }
  return 'Khám phá các khóa học thuộc chuyên mục ' + cat.name;
};


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
        { title: 'VIỆN KHOA HỌC LÃNH ĐẠO VÀ QUẢN TRỊ DOANH NGHIỆP - LEADMAN', externalLink: 'https://alumni.andrews.edu.vn/' }
      ];
    case 'post-graduate':
      return [
        { title: '🎓 MBA ANDREW (Thạc sĩ Quản trị Kinh doanh Hoa Kỳ)', link: '/admissions#mba' },
        // { title: '⚡ MINI MBA Practical (Quản trị Tinh gọn)', link: '/admissions#mini-mba' },
        { title: '🌐 GEL (Global Executive Leadership)', link: '/admissions#gei' }
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

let scrollTicking = false;
const handleScroll = () => {
  if (scrollTicking) return;
  scrollTicking = true;
  window.requestAnimationFrame(() => {
    const scrollTop = window.scrollY || document.documentElement.scrollTop;
    const scrolled = scrollTop > 20;
    if (isScrolled.value !== scrolled) {
      isScrolled.value = scrolled;
    }
    
    // Prevent hiding header if mobile menu, mega drawer, cart, or search is open
    if (isMobileMenuOpen.value || isDrawerOpen.value || isSearchOpen.value) {
      isHidden.value = false;
      lastScrollTop.value = scrollTop;
      scrollTicking = false;
      return;
    }
    
    // Hide header when scrolling down, show when scrolling up
    if (scrollTop > lastScrollTop.value && scrollTop > 80) {
      if (!isHidden.value) isHidden.value = true;
    } else if (scrollTop < lastScrollTop.value) {
      if (isHidden.value) isHidden.value = false;
    }
    
    lastScrollTop.value = scrollTop;
    scrollTicking = false;
  });
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
  window.addEventListener('scroll', handleScroll, { passive: true });
  try {
    const tasks = [];
    if (!courseStore.categories || courseStore.categories.length === 0) {
      tasks.push(courseStore.fetchCategories(false));
    }
    if (courseStore.courses.length === 0) {
      tasks.push(courseStore.fetchCourses());
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
  window.removeEventListener('scroll', handleScroll);
  document.body.classList.remove('lock-scroll'); // teardown scroll lock safety
});
</script>

<style scoped src="@/styles/components/Header.css"></style>
