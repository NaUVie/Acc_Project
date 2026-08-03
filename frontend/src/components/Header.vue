<template>
  <header class="main-header" :class="{ 'scrolled': isScrolled }">
    <div class="container header-container">
      <!-- Logo -->
      <router-link to="/" class="logo">
        <img src="/images/logo2.jpg" alt="ACC Academy Logo" class="logo-image" />
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
                  <router-link :to="activeCategoryLink" class="mega-view-all-link">
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

        <router-link to="/chia-se-hoc-vien" class="nav-link">Chia sẻ học viên</router-link>
        <router-link to="/contact" class="nav-link">Liên hệ</router-link>
        <router-link to="/about-us" class="nav-link">Về chúng tôi</router-link>
      </nav>

      <!-- Action buttons -->
      <div class="header-actions">
        <router-link v-if="!courseStore.token" to="/login" class="login-btn">Đăng nhập học viên</router-link>
        <div v-else class="user-menu-wrapper" style="display: flex; align-items: center; gap: 8px;">
          <router-link v-if="courseStore.userMe?.role === 'admin'" to="/admin" class="btn btn-primary" style="padding: 6px 12px; font-size: 13px; border-radius: var(--rounded-button); box-shadow: none; height: auto;">👑 Quản trị</router-link>
          <router-link to="/dashboard" class="login-btn user-btn">🙋‍♂️ {{ courseStore.userMe?.fullname || 'Học viên' }}</router-link>
        </div>
        
        <button class="icon-btn" aria-label="Tìm kiếm">
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

        <router-link to="/chia-se-hoc-vien" class="mobile-single-link" @click="closeMobileMenu">Chia sẻ học viên</router-link>
        <router-link to="/contact" class="mobile-single-link" @click="closeMobileMenu">Liên hệ</router-link>
        <router-link to="/about-us" class="mobile-single-link" @click="closeMobileMenu">Về chúng tôi</router-link>
        
        <router-link v-if="!courseStore.token" to="/login" class="mobile-login-btn" @click="closeMobileMenu">Đăng nhập học viên</router-link>
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

    <!-- Slide-over Cart -->
    <SlideOverCart 
      :isOpen="isCartOpen" 
      @close="isCartOpen = false"
      @view-cart="handleViewCart"
      @checkout="handleCheckout"
    />
  </header>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { useCourseStore } from '@/stores/courses';
import SlideOverCart from '@/components/SlideOverCart.vue';

const router = useRouter();
const courseStore = useCourseStore();

const isCartOpen = ref(false);
const isScrolled = ref(false);
const isMobileMenuOpen = ref(false);
const activeMobileSection = ref('');
const activeMobileSubSection = ref('');

const handleViewCart = () => {
  isCartOpen.value = false;
  router.push('/cart');
};

const handleCheckout = () => {
  isCartOpen.value = false;
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

// 1. Mega Menu Categories Data
const categories = [
  { id: 'ky-nang-ai', name: 'Kỹ năng AI', viewAllLink: '/courses/ai' },
  { id: 'ky-nang-chuyen-mon', name: 'Kỹ năng chuyên môn', viewAllLink: '/courses/chuyen-mon' },
  { id: 'ky-nang-mem', name: 'Kỹ năng mềm', viewAllLink: '/courses/mem' },
  { id: 'bundles', name: 'Combo khóa học', viewAllLink: '/bundles' }
];

const selectedCategory = ref('ky-nang-ai');

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
    let link = '/courses/ai';
    if (c.category === 'ky-nang-chuyen-mon') link = '/courses/chuyen-mon';
    else if (c.category === 'ky-nang-mem') link = '/courses/mem';
    else if (c.category === 'bundles') link = '/bundles';

    return {
      id: c.id,
      categoryId: c.category,
      title: c.title,
      school: translateCategory(c.category),
      logo: c.image || '/images/logo2.jpg',
      link: link
    };
  });
});

const filteredPrograms = computed(() => {
  return programs.value.filter(p => p.categoryId === selectedCategory.value);
});

const activeCategoryName = computed(() => {
  const cat = categories.find(c => c.id === selectedCategory.value);
  return cat ? cat.name : '';
});

const activeCategoryLink = computed(() => {
  const cat = categories.find(c => c.id === selectedCategory.value);
  return cat ? cat.viewAllLink : '/courses/ai';
});

const getProgramsByCategoryId = (catId) => {
  return programs.value.filter(p => p.categoryId === catId);
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

onMounted(async () => {
  window.addEventListener('scroll', handleScroll);
  if (courseStore.courses.length === 0) {
    try {
      await courseStore.fetchCourses();
    } catch (e) {
      console.error('Failed to fetch courses in Header', e);
    }
  }
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
  document.body.classList.remove('lock-scroll'); // teardown scroll lock safety
});
</script>

<style scoped src="@/styles/components/Header.css"></style>
