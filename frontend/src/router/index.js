import { createRouter, createWebHistory } from 'vue-router';
import { i18n, setLanguage } from '../i18n';
import { applyGoogleTranslate, clearGoogleTranslate } from '../utils/googleTranslate';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/courses',
    alias: ['/dao-tao', '/courses/category'],
    name: 'AllCourses',
    component: () => import('../views/courses/CourseCategoryView.vue')
  },
  {
    path: '/courses/category/:categorySlug',
    name: 'CourseCategoryView',
    component: () => import('../views/courses/CourseCategoryView.vue')
  },
  { path: '/courses/ai', redirect: '/courses/category/ky-nang-ai' },
  { path: '/courses/mem', redirect: '/courses/category/ky-nang-mem' },
  { path: '/courses/chuyen-mon', redirect: '/courses/category/ky-nang-chuyen-mon' },
  {
    path: '/course/:handle',
    alias: ['/courses/detail/:handle'],
    name: 'CourseDetail',
    component: () => import('../views/courses/CourseDetail.vue')
  },
  {
    path: '/admissions',
    alias: ['/tuyen-sinh', '/post-graduate/mba', '/post-graduate/gei', '/post-graduate/mini-mba'],
    name: 'Admissions',
    component: () => import('../views/tuyen-sinh/AdmissionsView.vue')
  },
  {
    path: '/admissions/detail/:id',
    alias: ['/admissions/:id', '/tuyen-sinh/detail/:id', '/tuyen-sinh/:id'],
    name: 'AdmissionDetail',
    component: () => import('../views/tuyen-sinh/AdmissionDetailView.vue')
  },
  {
    path: '/bundles',
    alias: ['/pages/bundle-2026', '/pages/bundle'],
    redirect: '/courses'
  },
  {
    path: '/corporate/dao-tao',
    name: 'CorporateTraining',
    component: () => import('../views/corporate/CorporateTraining.vue')
  },
  {
    path: '/corporate/coe',
    name: 'CorporateCoe',
    component: () => import('../views/corporate/Coe.vue')
  },
  {
    path: '/corporate/for-team',
    name: 'CorporateForTeam',
    component: () => import('../views/corporate/ForTeam.vue')
  },
  {
    path: '/projects',
    alias: ['/du-an', '/corporate/case-studies', '/su-kien'],
    redirect: '/'
  },
  {
    path: '/projects/:id',
    alias: ['/du-an/:id'],
    redirect: '/'
  },
  {
    path: '/library/blog',
    alias: ['/blog'],
    name: 'LibraryBlog',
    component: () => import('../views/library/Blog.vue')
  },
  {
    path: '/blog/:handle',
    alias: ['/library/blog/:handle'],
    name: 'BlogDetail',
    component: () => import('../views/library/BlogDetail.vue')
  },
  {
    path: '/library/recipes',
    name: 'LibraryRecipes',
    component: () => import('../views/library/Recipes.vue')
  },
  {
    path: '/referral',
    alias: ['/gioi-thieu', '/referrals', '/gioi-thieu-nhan-thuong'],
    name: 'ReferralProgram',
    component: () => import('../views/ReferralProgram.vue')
  },
  {
    path: '/contact',
    name: 'Contact',
    component: () => import('../views/Contact.vue')
  },
  {
    path: '/about-us',
    name: 'AboutUs',
    component: () => import('../views/AboutUs.vue')
  },
  {
    path: '/lecturers',
    alias: ['/doi-ngu-giang-vien', '/giang-vien'],
    name: 'Lecturers',
    component: () => import('../views/Lecturers.vue')
  },
  {
    path: '/lecturers/:id',
    alias: ['/giang-vien/:id'],
    name: 'LecturerDetail',
    component: () => import('../views/LecturerDetail.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue')
  },
  {
    path: '/forgot-password',
    name: 'ForgotPassword',
    component: () => import('../views/ForgotPassword.vue')
  },
  {
    path: '/cart',
    redirect: '/courses'
  },
  {
    path: '/checkout',
    redirect: '/courses'
  },
  {
    path: '/testimonials',
    alias: ['/chia-se-hoc-vien', '/hoc-vien-chia-se'],
    name: 'Testimonials',
    component: () => import('../views/TestimonialsView.vue')
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/courses/:handle/study',
    name: 'CourseStudy',
    component: () => import('../views/courses/CourseStudy.vue'),
    meta: { requiresAuth: true, requiresEnrollment: true }
  },
  {
    path: '/order/:id',
    name: 'OrderConfirmation',
    component: () => import('../views/OrderConfirmation.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/payment/vnpay-return',
    redirect: '/courses'
  },
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: () => import('../views/admin/AdminDashboard.vue'),
    meta: { requiresAdmin: true }
  },
  {
    path: '/terms-of-service',
    alias: ['/terms', '/dieu-khoan-dich-vu'],
    name: 'TermsOfService',
    component: () => import('../views/LegalPolicy.vue')
  },
  {
    path: '/privacy-policy',
    alias: ['/privacy', '/chinh-sach-bao-mat'],
    name: 'PrivacyPolicy',
    component: () => import('../views/LegalPolicy.vue')
  },
  {
    path: '/refund-policy',
    alias: ['/chinh-sach-hoan-tien'],
    name: 'RefundPolicy',
    component: () => import('../views/LegalPolicy.vue')
  },
  {
    path: '/payment-guide',
    alias: ['/huong-dan-thanh-toan'],
    name: 'PaymentGuide',
    component: () => import('../views/LegalPolicy.vue')
  },
  {
    path: '/delivery-policy',
    alias: ['/chinh-sach-giao-nhan', '/kich-hoat-khoa-hoc'],
    name: 'DeliveryPolicy',
    component: () => import('../views/LegalPolicy.vue')
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFound.vue')
  }
];

// Functional pages (auth / cart / checkout / learning room ...) stay Vietnamese-only
// and are NOT duplicated under /en
const NO_LOCALE_PATHS = [
  '/login', '/register', '/dashboard',
  '/courses/:handle/study', '/order/:id', '/referral'
];
routes.forEach(r => {
  if (NO_LOCALE_PATHS.includes(r.path)) r.meta = { ...(r.meta || {}), noLocale: true };
});

// Generate English routes with /en prefix for international SEO
function generateEnRoutes(baseList) {
  const enRoutes = [];
  for (const r of baseList) {
    if (r.path === '/:pathMatch(.*)*' || r.path.startsWith('/admin') || (r.meta && r.meta.noLocale)) {
      continue;
    }
    const enPath = r.path === '/' ? '/en' : `/en${r.path}`;
    const enRoute = {
      ...r,
      path: enPath,
      name: r.name ? `En_${r.name}` : undefined
    };
    if (r.redirect) {
      enRoute.redirect = typeof r.redirect === 'string'
        ? (r.redirect.startsWith('/en') ? r.redirect : `/en${r.redirect}`)
        : r.redirect;
    }
    if (r.alias) {
      const aliases = Array.isArray(r.alias) ? r.alias : [r.alias];
      enRoute.alias = aliases.map(a => a === '/' ? '/en' : `/en${a}`);
    }
    enRoutes.push(enRoute);
  }
  return enRoutes;
}

const allRoutes = [
  ...routes.filter(r => r.path !== '/:pathMatch(.*)*'),
  ...generateEnRoutes(routes),
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFound.vue')
  }
];

if (typeof window !== 'undefined' && 'scrollRestoration' in window.history) {
  window.history.scrollRestoration = 'manual';
}

const router = createRouter({
  history: createWebHistory(),
  routes: allRoutes,
  scrollBehavior(to, from, savedPosition) {
    if (to.name === 'Home' || to.path === '/') {
      const savedY = Number(sessionStorage.getItem('home_scroll_y') || 0);
      const targetY = (savedPosition && savedPosition.top > 100) ? savedPosition.top : savedY;
      if (targetY > 100) {
        return new Promise((resolve) => {
          setTimeout(() => {
            resolve({ top: targetY, behavior: 'instant' });
          }, 50);
        });
      }
    }
    if (savedPosition) {
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve(savedPosition);
        }, 50);
      });
    }
    if (to.hash) {
      return { el: to.hash, behavior: 'smooth' };
    }
    return { top: 0 };
  }
});

import { useCourseStore } from '../stores/courses';

router.beforeEach(async (to, from, next) => {
  // Save scroll position when leaving Home
  if (typeof window !== 'undefined' && (from.name === 'Home' || from.path === '/')) {
    try {
      sessionStorage.setItem('home_scroll_y', String(window.scrollY));
    } catch (e) {}
  }

  // 1. Multilingual Route & SEO Guard
  const isEnRoute = to.path === '/en' || to.path.startsWith('/en/');
  const currentLocale = i18n.global.locale.value;

  if (isEnRoute) {
    if (currentLocale !== 'en') {
      setLanguage('en');
    }
  } else if (!to.path.startsWith('/admin') && !to.meta.noLocale) {
    // If navigating internally while currently in English, preserve /en/ prefix
    const fromIsEn = from.path === '/en' || (from.path && from.path.startsWith('/en/'));
    if (fromIsEn && currentLocale === 'en') {
      const enTarget = to.fullPath === '/' ? '/en' : `/en${to.fullPath}`;
      return next(enTarget);
    }
    if (currentLocale !== 'vi') {
      clearGoogleTranslate();
      setLanguage('vi');
    }
  }

  const courseStore = useCourseStore();
  const isProtected = to.meta.requiresAuth || to.meta.requiresAdmin || to.meta.requiresEnrollment;

  // Background fetch for user profile if token exists but user object is not yet populated
  if (courseStore.token && !courseStore.user) {
    if (isProtected) {
      try {
        await courseStore.fetchUserMe();
      } catch (err) {
        console.error("Route guard profile fetch error:", err);
      }
    } else {
      // Non-blocking background sync for public routes
      courseStore.fetchUserMe().catch(() => {});
    }
  } else if (courseStore.token && courseStore.user) {
    // Non-blocking background refresh to keep session and roles fresh without white screen delay
    courseStore.fetchUserMe().catch(() => {});
  }

  // Load enrollments only when accessing protected enrollment room
  if (to.meta.requiresEnrollment && courseStore.token && courseStore.enrollments.length === 0) {
    try {
      await courseStore.fetchEnrollments();
    } catch (err) {
      console.error('Failed to load enrollments in route guard:', err);
    }
  }

  if (to.meta.requiresAdmin) {
    if (courseStore.token && courseStore.user?.role === 'admin') {
      next();
    } else {
      courseStore.showToast('Bạn không có quyền truy cập trang quản trị!', 'error');
      next('/login');
    }
  } else if (to.meta.requiresEnrollment) {
    // Must be logged in AND enrolled in the specific course
    if (!courseStore.token) {
      courseStore.showToast('Vui lòng đăng nhập để truy cập phòng học!', 'warning');
      next('/login');
      return;
    }
    const handle = to.params.handle;
    const enrolled = courseStore.isEnrolled(handle);
    if (!enrolled) {
      // Allow admin to bypass
      if (courseStore.user?.role === 'admin') {
        next();
        return;
      }
      courseStore.showToast('Bạn chưa đăng ký khóa học này. Vui lòng đăng ký để tiếp tục!', 'info');
      next(`/course/${handle}`);
      return;
    }
    next();
  } else if (to.meta.requiresAuth) {
    if (courseStore.token) {
      next();
    } else {
      courseStore.showToast('Vui lòng đăng nhập để tiếp tục!', 'warning');
      next('/login');
    }
  } else {
    // Public routes navigate immediately!
    next();
  }
});

router.afterEach((to) => {
  if (typeof document !== 'undefined') {
    if (to.meta && to.meta.noLocale) {
      document.head.querySelectorAll('link[rel="alternate"][hreflang]').forEach(el => el.remove());
      return;
    }
    const isEn = to.path === '/en' || to.path.startsWith('/en/');
    document.documentElement.lang = isEn ? 'en' : 'vi';

    // Inject hreflang canonical alternate links for Google SEO
    try {
      const origin = window.location.origin;
      const cleanPath = isEn ? to.path.replace(/^\/en(\/|$)/, '/') : to.path;
      const viUrl = `${origin}${cleanPath === '/' ? '' : cleanPath}` || `${origin}/`;
      const enUrl = `${origin}/en${cleanPath === '/' ? '' : cleanPath}`;

      let viLink = document.head.querySelector('link[hreflang="vi"]');
      if (!viLink) {
        viLink = document.createElement('link');
        viLink.setAttribute('rel', 'alternate');
        viLink.setAttribute('hreflang', 'vi');
        document.head.appendChild(viLink);
      }
      viLink.setAttribute('href', viUrl);

      let enLink = document.head.querySelector('link[hreflang="en"]');
      if (!enLink) {
        enLink = document.createElement('link');
        enLink.setAttribute('rel', 'alternate');
        enLink.setAttribute('hreflang', 'en');
        document.head.appendChild(enLink);
      }
      enLink.setAttribute('href', enUrl);

      let xDefaultLink = document.head.querySelector('link[hreflang="x-default"]');
      if (!xDefaultLink) {
        xDefaultLink = document.createElement('link');
        xDefaultLink.setAttribute('rel', 'alternate');
        xDefaultLink.setAttribute('hreflang', 'x-default');
        document.head.appendChild(xDefaultLink);
      }
      xDefaultLink.setAttribute('href', viUrl);
    } catch (e) {
      // Ignore in non-browser context
    }

    // Auto-trigger Google Translate for newly rendered dynamic content when in English mode
    if (isEn) {
      setTimeout(() => {
        applyGoogleTranslate('en');
      }, 350);
    } else {
      clearGoogleTranslate();
    }
  }
});

export default router;
