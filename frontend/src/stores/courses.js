import { defineStore } from 'pinia';
import { getApiBase, API_BASE, mapCourse } from './modules/helpers';
import { uiActions } from './modules/uiActions';
import { courseActions } from './modules/courseActions';
import { cartActions } from './modules/cartActions';
import { authActions } from './modules/authActions';
import { lecturerActions } from './modules/lecturerActions';
import { blogActions } from './modules/blogActions';
import { projectActions } from './modules/projectActions';
import { marketingActions } from './modules/marketingActions';
import { adminActions } from './modules/adminActions';

export const useCourseStore = defineStore('courses', {
  state: () => ({
    // Catalog states
    courses: (() => {
      try {
        const cached = localStorage.getItem('acc_courses_cache_v1');
        return cached ? JSON.parse(cached).map(mapCourse) : [];
      } catch {
        return [];
      }
    })(),
    categories: (() => {
      try {
        const cached = localStorage.getItem('acc_categories_cache');
        return cached ? JSON.parse(cached) : [
          { slug: 'dao-tao-ca-nhan', name: 'Đào tạo cá nhân' },
          { slug: 'dao-tao-inhouse', name: 'Đào tạo INHOUSE' }
        ];
      } catch {
        return [];
      }
    })(),
    programs: [],
    bundles: [],
    lecturers: (() => {
      try {
        localStorage.removeItem('acc_lecturers_cache');
        const cached = localStorage.getItem('acc_lecturers_v2');
        return cached ? JSON.parse(cached) : [];
      } catch {
        return [];
      }
    })(),
    lecturerMajors: (() => {
      try {
        localStorage.removeItem('acc_lecturer_majors_cache');
        const cached = localStorage.getItem('acc_lecturer_majors_v2');
        return cached ? JSON.parse(cached) : [];
      } catch {
        return [];
      }
    })(),
    lecturersLoaded: false,
    lecturersLoading: false,
    lecturerMajorsLoaded: false,
    contactSettings: null,
    blogPosts: [],
    blogCategories: [],
    loading: false,
    coursesLoaded: false,
    blogsLoaded: false,
    blogsLoading: false,
    projectsLoaded: false,
    projectsLoading: false,
    bannersLoaded: false,
    boardMembers: [],
    adminBoardMembers: [],
    boardMembersLoaded: false,
    admissions: (() => {
      try {
        const cached = localStorage.getItem('acc_admissions_cache');
        return cached ? JSON.parse(cached) : [];
      } catch {
        return [];
      }
    })(),
    adminAdmissions: (() => {
      try {
        const cached = localStorage.getItem('acc_admin_admissions_cache');
        return cached ? JSON.parse(cached) : [];
      } catch {
        return [];
      }
    })(),
    admissionsLoaded: false,
    admissionsLoading: false,
    adminAdmissionsLoading: false,
    boardMembersLoading: false,
    error: null,

    // Auth states
    token: localStorage.getItem('token') || null,
    user: (() => {
      try {
        const raw = localStorage.getItem('user');
        return raw ? JSON.parse(raw) : null;
      } catch (e) {
        return null;
      }
    })(),
    referralSummary: null,
    isRegistering: false,

    // Toast Notification State
    toast: {
      show: false,
      message: '',
      type: 'info'
    },

    // Global Confirm Modal State
    confirmModal: {
      show: false,
      title: 'Xác nhận hành động',
      message: '',
      confirmText: 'Đồng ý',
      cancelText: 'Hủy',
      type: 'danger',
      resolve: null
    },

    // Cart states
    cart: [], // holds cart items: { id, course }

    // Orders states
    orders: [], // holds order history

    // Enrollment states (courses user has paid access to)
    enrollments: [], // list of { id, course, enrolled_at }

    // Engagement & Marketing states
    wishlist: [], // list of wishlist items
    appliedCoupon: null,
    adminCoupons: [],
    adminCommissions: [],

    // Admin Dashboard States
    adminUsers: (() => {
      try {
        const cached = localStorage.getItem('acc_admin_users_cache');
        return cached ? JSON.parse(cached) : [];
      } catch {
        return [];
      }
    })(),
    adminOrders: (() => {
      try {
        const cached = localStorage.getItem('acc_admin_orders_cache');
        return cached ? JSON.parse(cached) : [];
      } catch {
        return [];
      }
    })(),
    adminContacts: (() => {
      try {
        const cached = localStorage.getItem('acc_admin_contacts_cache');
        return cached ? JSON.parse(cached) : [];
      } catch {
        return [];
      }
    })(),
    adminBanners: [],
    adminTestimonials: [],
    adminProjects: [],
    adminBlogPosts: [],
    adminPartners: [],
    projects: [],
    banners: [],
    bannersLoading: false,
    partners: (() => {
      try {
        const cached = localStorage.getItem('acc_partners_cache');
        return cached ? JSON.parse(cached) : [];
      } catch {
        return [];
      }
    })(),
    homeIntroSettings: (() => {
      try {
        const cached = localStorage.getItem('acc_home_intro_cache');
        return cached ? JSON.parse(cached) : null;
      } catch {
        return null;
      }
    })()
  }),

  getters: {
    getCoursesByCategory: (state) => (categorySlug) => {
      if (!categorySlug) return state.courses;
      let targetSlug = String(categorySlug).toLowerCase();
      if (['all', 'courses', 'dao-tao'].includes(targetSlug)) {
        return state.courses;
      }
      const SUB_ALIASES = {
        'hiep-hoi': 'inhouse-hiep-hoi',
        'inhouse-hiep-hoi': 'inhouse-hiep-hoi',
        'truong-hoc': 'inhouse-truong-hoc',
        'inhouse-truong-hoc': 'inhouse-truong-hoc',
        'inhouse-doanh-nghiep': 'inhouse-doanh-nghiep',
        'co-quan-nha-nuoc': 'inhouse-co-quan-nha-nuoc',
        'nha-nuoc': 'inhouse-co-quan-nha-nuoc',
        'inhouse-co-quan-nha-nuoc': 'inhouse-co-quan-nha-nuoc'
      };

      const ALIASES = {
        'doanh-nghiep': 'dao-tao-inhouse',
        'dao-tao-doanh-nghiep': 'dao-tao-inhouse',
        'inhouse': 'dao-tao-inhouse',
        'dao-tao-inhouse': 'dao-tao-inhouse',
        'ca-nhan': 'dao-tao-ca-nhan',
        'dao-tao-ca-nhan': 'dao-tao-ca-nhan',
        'ai': 'dao-tao-inhouse',
        'ky-nang-ai': 'dao-tao-inhouse',
        'mem': 'dao-tao-ca-nhan',
        'ky-nang-mem': 'dao-tao-ca-nhan',
        'chuyen-mon': 'dao-tao-ca-nhan',
        'ky-nang-chuyen-mon': 'dao-tao-ca-nhan'
      };

      if (SUB_ALIASES[targetSlug]) {
        const subSlug = SUB_ALIASES[targetSlug];
        return state.courses.filter(course => {
          if (!course.category) return false;
          const cCat = String(course.category).toLowerCase();
          const mappedCCat = ALIASES[cCat] || cCat;
          if (mappedCCat !== 'dao-tao-inhouse' && mappedCCat !== subSlug) return false;
          const text = `${course.title || ''} ${course.description || ''} ${course.category || ''}`.toLowerCase();
          if (subSlug === 'inhouse-hiep-hoi') {
            return text.includes('saca') || text.includes('hiệp hội') || text.includes('hiep hoi');
          }
          if (subSlug === 'inhouse-truong-hoc') {
            return text.includes('giáo dục') || text.includes('trường học') || text.includes('truong hoc');
          }
          if (subSlug === 'inhouse-co-quan-nha-nuoc') {
            return text.includes('nhà nước') || text.includes('cơ quan') || text.includes('ubnd');
          }
          if (subSlug === 'inhouse-doanh-nghiep') {
            return (!text.includes('saca') && !text.includes('hiệp hội') && !text.includes('giáo dục') && !text.includes('trường học') && !text.includes('nhà nước') && !text.includes('cơ quan') && !text.includes('ubnd')) || text.includes('doanh nghiệp');
          }
          return false;
        });
      }

      if (ALIASES[targetSlug]) {
        targetSlug = ALIASES[targetSlug];
      }
      return state.courses.filter(course => {
        if (!course.category) return false;
        const cCat = String(course.category).toLowerCase();
        const mappedCCat = ALIASES[cCat] || cCat;
        return mappedCCat === targetSlug;
      });
    },
    getCourseByHandle: (state) => (handle) => {
      return state.courses.find(course => course.handle === handle);
    },
    getBlogPosts: (state) => {
      return state.blogPosts;
    },
    isAuthenticated: (state) => !!state.token,
    cartCount: (state) => state.cart.length,
    cartTotal: (state) => state.cart.reduce((sum, item) => sum + (item.course?.price || 0), 0),
    userMe: (state) => state.user,
    enrolledCourseIds: (state) => state.enrollments.map(e => e.course?.id),
    isEnrolled: (state) => (courseIdOrHandle) => {
      if (!state.token) return false;

      // 1. Check actual enrolled courses
      if (state.enrollments && state.enrollments.length > 0) {
        const match = state.enrollments.some(e => {
          if (!e.course) return false;
          return String(e.course.id) === String(courseIdOrHandle) || e.course.handle === courseIdOrHandle;
        });
        if (match) return true;
      }

      // 2. Check completed paid orders
      if (state.orders && state.orders.length > 0) {
        const match = state.orders.some(order => {
          if (order.status !== 'paid') return false;
          return order.items && order.items.some(item => {
            return item.course && (String(item.course.id) === String(courseIdOrHandle) || item.course.handle === courseIdOrHandle);
          });
        });
        if (match) return true;
      }

      return false;
    }
  },

  actions: {
    ...uiActions,
    ...courseActions,
    ...cartActions,
    ...authActions,
    ...lecturerActions,
    ...blogActions,
    ...projectActions,
    ...marketingActions,
    ...adminActions
  }
});
