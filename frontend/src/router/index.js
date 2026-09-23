import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import AboutUs from '../views/AboutUs.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
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
    path: '/tuyen-sinh',
    alias: ['/post-graduate/mba', '/post-graduate/gei', '/post-graduate/mini-mba'],
    name: 'Admissions',
    component: () => import('../views/tuyen-sinh/AdmissionsView.vue')
  },
  {
    path: '/tuyen-sinh/detail/:id',
    alias: ['/tuyen-sinh/:id'],
    name: 'AdmissionDetail',
    component: () => import('../views/tuyen-sinh/AdmissionDetailView.vue')
  },
  {
    path: '/bundles',
    alias: ['/pages/bundle-2026', '/pages/bundle'],
    name: 'Bundles',
    component: () => import('../views/Bundles.vue')
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
    path: '/du-an',
    alias: ['/corporate/case-studies', '/projects', '/su-kien'],
    name: 'Projects',
    component: () => import('../views/Projects.vue')
  },
  {
    path: '/du-an/:id',
    name: 'ProjectDetail',
    component: () => import('../views/ProjectDetail.vue')
  },
  {
    path: '/library/blog',
    name: 'LibraryBlog',
    component: () => import('../views/library/Blog.vue')
  },
  {
    path: '/library/recipes',
    name: 'LibraryRecipes',
    component: () => import('../views/library/Recipes.vue')
  },
  {
    path: '/gioi-thieu',
    alias: ['/referral', '/referrals', '/gioi-thieu-nhan-thuong'],
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
    component: AboutUs
  },
  {
    path: '/doi-ngu-giang-vien',
    name: 'Lecturers',
    component: () => import('../views/Lecturers.vue')
  },
  {
    path: '/giang-vien/:id',
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
    path: '/cart',
    name: 'Cart',
    component: () => import('../views/Cart.vue')
  },
  {
    path: '/checkout',
    name: 'Checkout',
    component: () => import('../views/Checkout.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/chia-se-hoc-vien',
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
    path: '/admin',
    name: 'AdminDashboard',
    component: () => import('../views/admin/AdminDashboard.vue'),
    meta: { requiresAdmin: true }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFound.vue')
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 };
  }
});

import { useCourseStore } from '../stores/courses';

router.beforeEach(async (to, from, next) => {
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

export default router;
