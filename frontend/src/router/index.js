import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/courses/ai',
    name: 'CourseAISkills',
    component: () => import('../views/courses/AISkills.vue')
  },
  {
    path: '/courses/mem',
    name: 'CourseSoftSkills',
    component: () => import('../views/courses/SoftSkills.vue')
  },
  {
    path: '/courses/chuyen-mon',
    name: 'CourseProfessionalSkills',
    component: () => import('../views/courses/ProfessionalSkills.vue')
  },
  {
    path: '/course/:handle',
    alias: ['/courses/detail/:handle'],
    name: 'CourseDetail',
    component: () => import('../views/courses/CourseDetail.vue')
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
    path: '/corporate/case-studies',
    name: 'CorporateCaseStudies',
    component: () => import('../views/corporate/CaseStudies.vue')
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
    component: () => import('../views/Checkout.vue')
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
  
  if (courseStore.token && !courseStore.user) {
    try {
      await courseStore.fetchUserMe();
    } catch (err) {
      console.error("Route guard profile fetch error:", err);
    }
  }

  // Load enrollments if not yet fetched
  if (courseStore.token && courseStore.enrollments.length === 0) {
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
      alert('Bạn không có quyền truy cập trang quản trị!');
      next('/login');
    }
  } else if (to.meta.requiresEnrollment) {
    // Must be logged in AND enrolled in the specific course
    if (!courseStore.token) {
      alert('Vui lòng đăng nhập để học tập!');
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
      alert('Bạn chưa đăng ký khóa học này. Vui lòng mua khóa học để tiếp tục học tập!');
      next(`/course/${handle}`);
      return;
    }
    next();
  } else if (to.meta.requiresAuth) {
    if (courseStore.token) {
      next();
    } else {
      alert('Vui lòng đăng nhập để học tập!');
      next('/login');
    }
  } else {
    next();
  }
});

export default router;
