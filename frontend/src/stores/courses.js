import { defineStore } from 'pinia';

// Dynamic API URL builder to avoid hardcoded URLs
const getApiBase = () => {
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL;
  }
  if (typeof window !== 'undefined') {
    const isDev = import.meta.env.DEV;
    if (isDev) {
      return `${window.location.protocol}//${window.location.hostname}:8000/api`;
    }
    return `${window.location.origin}/api`;
  }
  return '/api';
};

const API_BASE = getApiBase();

// Helper to clean course properties mapping from API to Frontend camelCase format
const mapCourse = (c) => ({
  id: c.id,
  title: c.title,
  category: c.category_slug,
  programId: c.program_id,
  handle: c.handle,
  price: c.price,
  originalPrice: c.original_price,
  image: c.image,
  tags: c.tags ? c.tags.map(t => t.tag) : [],
  description: c.description,
  duration: c.duration,
  level: c.level,
  curriculumData: c.curriculum_data,
  outcomes: c.outcomes,
  requirements: c.requirements,
  customRoadmap: c.custom_roadmap,
  lecturerIds: c.lecturer_ids
});

export const useCourseStore = defineStore('courses', {
  state: () => ({
    // Catalog states
    courses: [],
    categories: [
      { slug: 'dao-tao-doanh-nghiep', name: 'Đào tạo Inhouse' },
      { slug: 'dao-tao-ca-nhan', name: 'Đào tạo cá nhân' }
    ],
    programs: [],
    bundles: [],
    lecturers: [],
    contactSettings: null,
    blogPosts: [],
    loading: false,
    error: null,

    // Auth states
    token: localStorage.getItem('token') || null,
    user: null,
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
    adminCoupons: [],
    adminCommissions: [],

    // Admin Dashboard States
    adminUsers: [],
    adminOrders: [],
    adminContacts: [],
    adminBanners: [],
    adminTestimonials: [],
    adminProjects: [],
    adminBlogPosts: [],
    projects: [],
    banners: [],
    contactSettings: null
  }),

  getters: {
    getCoursesByCategory: (state) => (categorySlug) => {
      if (!categorySlug) return state.courses;
      let targetSlug = String(categorySlug).toLowerCase();
      if (['all', 'courses', 'dao-tao'].includes(targetSlug)) {
        return state.courses;
      }
      const ALIASES = {
        'doanh-nghiep': 'dao-tao-doanh-nghiep',
        'ca-nhan': 'dao-tao-ca-nhan',
        'nha-nuoc': 'dao-tao-co-quan-nha-nuoc',
        'co-quan-nha-nuoc': 'dao-tao-co-quan-nha-nuoc',
        'ai': 'dao-tao-doanh-nghiep',
        'ky-nang-ai': 'dao-tao-doanh-nghiep',
        'mem': 'dao-tao-ca-nhan',
        'ky-nang-mem': 'dao-tao-ca-nhan',
        'chuyen-mon': 'dao-tao-ca-nhan',
        'ky-nang-chuyen-mon': 'dao-tao-ca-nhan'
      };
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
      if (state.user?.role === 'admin') return true;

      if (state.enrollments && state.enrollments.length > 0) {
        const match = state.enrollments.some(e => {
          if (!e.course) return false;
          return String(e.course.id) === String(courseIdOrHandle) || e.course.handle === courseIdOrHandle;
        });
        if (match) return true;
      }

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
    // Standard request wrapper with JWT token injection
    async apiRequest(endpoint, options = {}) {
      const url = `${API_BASE}${endpoint}`;
      const headers = {
        'Content-Type': 'application/json',
        ...options.headers
      };

      if (this.token) {
        headers['Authorization'] = `Bearer ${this.token}`;
      }

      try {
        const response = await fetch(url, { ...options, headers });
        if (!response.ok) {
          if (response.status === 401) {
            // Only clear token & redirect if specifically failing user authentication check (/auth/me)
            // or if explicitly unauthenticated to prevent accidental logouts on transient server errors
            if (endpoint === '/auth/me') {
              this.token = null;
              this.user = null;
              localStorage.removeItem('token');
              if (typeof window !== 'undefined' && !window.location.pathname.startsWith('/login')) {
                window.location.href = '/login';
              }
            }
          }
          const errData = await response.json().catch(() => ({}));
          let message = `HTTP error! status: ${response.status}`;
          if (typeof errData.detail === 'string') {
            message = errData.detail;
          } else if (Array.isArray(errData.detail)) {
            message = errData.detail.map(e => `${e.loc ? e.loc.join('.') + ': ' : ''}${e.msg}`).join('; ');
          } else if (errData.message) {
            message = errData.message;
          }
          throw new Error(message);
        }
        return await response.json();
      } catch (err) {
        console.error(`API Request Error on ${endpoint}:`, err);
        throw err;
      }
    },

    // --- Dynamic Catalog Actions ---
    async fetchBanners() {
      try {
        const data = await this.apiRequest('/courses/banners');
        this.banners = data;
        return data;
      } catch (err) {
        console.error("Failed to fetch banners:", err);
      }
    },

    async fetchAdminBanners() {
      try {
        const data = await this.apiRequest('/admin/banners');
        this.adminBanners = data;
        return data;
      } catch (err) {
        console.error("Failed to fetch admin banners:", err);
        throw err;
      }
    },

    async createBanner(bannerData) {
      const data = await this.apiRequest('/admin/banners', {
        method: 'POST',
        body: JSON.stringify(bannerData)
      });
      await Promise.all([this.fetchAdminBanners().catch(() => {}), this.fetchBanners().catch(() => {})]);
      return data;
    },

    async updateBanner(bannerId, bannerData) {
      const data = await this.apiRequest(`/admin/banners/${bannerId}`, {
        method: 'PUT',
        body: JSON.stringify(bannerData)
      });
      await Promise.all([this.fetchAdminBanners().catch(() => {}), this.fetchBanners().catch(() => {})]);
      return data;
    },

    async deleteBanner(bannerId) {
      const data = await this.apiRequest(`/admin/banners/${bannerId}`, {
        method: 'DELETE'
      });
      await Promise.all([this.fetchAdminBanners().catch(() => {}), this.fetchBanners().catch(() => {})]);
      return data;
    },

    showToast(message, type = 'info', duration = 3500) {
      this.toast.message = message;
      this.toast.type = type;
      this.toast.show = true;
      setTimeout(() => {
        this.toast.show = false;
      }, duration);
    },

    hideToast() {
      this.toast.show = false;
    },

    showConfirm({ title = 'Xác nhận hành động', message, confirmText = 'Đồng ý', cancelText = 'Hủy', type = 'danger' }) {
      return new Promise((resolve) => {
        this.confirmModal = {
          show: true,
          title,
          message,
          confirmText,
          cancelText,
          type,
          resolve
        };
      });
    },

    handleConfirmResult(result) {
      if (this.confirmModal.resolve) {
        this.confirmModal.resolve(result);
      }
      this.confirmModal.show = false;
      this.confirmModal.resolve = null;
    },

    async fetchCategories() {
      try {
        const data = await this.apiRequest('/courses/categories');
        this.categories = data;
        return data;
      } catch (err) {
        console.error("Failed to fetch categories:", err);
        return [];
      }
    },

    async createCategory(catData) {
      try {
        const data = await this.apiRequest('/admin/categories', {
          method: 'POST',
          body: JSON.stringify(catData)
        });
        await this.fetchCategories();
        this.showToast(`Đã thêm chuyên mục "${data.name}"`, 'success');
        return data;
      } catch (err) {
        this.showToast(err.message || 'Lỗi khi tạo chuyên mục', 'error');
        throw err;
      }
    },

    async updateCategory(slug, name) {
      try {
        const data = await this.apiRequest(`/admin/categories/${slug}`, {
          method: 'PUT',
          body: JSON.stringify({ name })
        });
        await this.fetchCategories();
        this.showToast(`Đã cập nhật chuyên mục "${name}"`, 'success');
        return data;
      } catch (err) {
        this.showToast(err.message || 'Lỗi khi sửa chuyên mục', 'error');
        throw err;
      }
    },

    async deleteCategory(slug) {
      try {
        await this.apiRequest(`/admin/categories/${slug}`, {
          method: 'DELETE'
        });
        await this.fetchCategories();
        this.showToast('Đã xóa chuyên mục', 'success');
      } catch (err) {
        this.showToast(err.message || 'Lỗi khi xóa chuyên mục', 'error');
        throw err;
      }
    },

    // --- Programs Actions ---
    async fetchPrograms() {
      try {
        const data = await this.apiRequest('/courses/programs');
        this.programs = data.map(p => ({
          id: p.id,
          title: p.title,
          slug: p.slug,
          description: p.description,
          image: p.image
        }));
        return this.programs;
      } catch (err) {
        console.error("Failed to fetch programs:", err);
        return [];
      }
    },

    async addAdminProgram(progData) {
      const payload = {
        title: progData.title,
        slug: progData.slug,
        image: progData.image,
        description: progData.description,
        course_ids: progData.courseIds || []
      };
      const data = await this.apiRequest('/admin/programs', {
        method: 'POST',
        body: JSON.stringify(payload)
      });
      await this.fetchPrograms();
      await this.fetchCourses();
      return data;
    },

    async updateAdminProgram(id, progData) {
      const payload = {
        title: progData.title,
        slug: progData.slug,
        image: progData.image,
        description: progData.description,
        course_ids: progData.courseIds || []
      };
      const data = await this.apiRequest(`/admin/programs/${id}`, {
        method: 'PUT',
        body: JSON.stringify(payload)
      });
      await this.fetchPrograms();
      await this.fetchCourses();
      return data;
    },

    async deleteAdminProgram(id) {
      const data = await this.apiRequest(`/admin/programs/${id}`, {
        method: 'DELETE'
      });
      await this.fetchPrograms();
      await this.fetchCourses();
      return data;
    },

    // --- Bundles Actions ---
    async fetchBundles() {
      try {
        const data = await this.apiRequest('/courses/bundles');
        this.bundles = data.map(b => ({
          id: b.id,
          title: b.title,
          handle: b.handle,
          description: b.description,
          price: b.price,
          original_price: b.original_price,
          originalPrice: b.original_price,
          image: b.image,
          courses: (b.courses || []).map(mapCourse),
          gift_courses: (b.gift_courses || []).map(mapCourse),
          giftCourses: (b.gift_courses || []).map(mapCourse)
        }));
        return this.bundles;
      } catch (err) {
        console.error("Failed to fetch bundles:", err);
        return [];
      }
    },

    async addAdminBundle(bundleData) {
      const payload = {
        title: bundleData.title,
        handle: bundleData.handle,
        price: bundleData.price,
        original_price: bundleData.originalPrice,
        image: bundleData.image,
        description: bundleData.description,
        course_ids: bundleData.courseIds || [],
        gift_course_ids: bundleData.giftCourseIds || []
      };
      const data = await this.apiRequest('/admin/bundles', {
        method: 'POST',
        body: JSON.stringify(payload)
      });
      await this.fetchBundles();
      return data;
    },

    async updateAdminBundle(id, bundleData) {
      const payload = {
        title: bundleData.title,
        handle: bundleData.handle,
        price: bundleData.price,
        original_price: bundleData.originalPrice,
        image: bundleData.image,
        description: bundleData.description,
        course_ids: bundleData.courseIds || [],
        gift_course_ids: bundleData.giftCourseIds || []
      };
      const data = await this.apiRequest(`/admin/bundles/${id}`, {
        method: 'PUT',
        body: JSON.stringify(payload)
      });
      await this.fetchBundles();
      return data;
    },

    async deleteAdminBundle(id) {
      const data = await this.apiRequest(`/admin/bundles/${id}`, {
        method: 'DELETE'
      });
      await this.fetchBundles();
      return data;
    },

    // --- Contact Settings Actions ---
    async fetchContactSettings() {
      try {
        const data = await this.apiRequest('/contacts/settings');
        this.contactSettings = data;
        return data;
      } catch (err) {
        console.error("Failed to fetch contact settings:", err);
        return null;
      }
    },

    async updateContactSettings(settingsData) {
      const data = await this.apiRequest('/admin/contact-settings', {
        method: 'PUT',
        body: JSON.stringify(settingsData)
      });
      this.contactSettings = data;
      return data;
    },

    async fetchCourses() {
      this.loading = true;
      try {
        const [coursesData] = await Promise.all([
          this.apiRequest('/courses'),
          this.fetchCategories().catch(() => {}),
          this.fetchBanners().catch(() => {})
        ]);
        this.courses = coursesData.map(mapCourse);
      } catch (err) {
        this.error = err.message;
      } finally {
        this.loading = false;
      }
    },

    async fetchCourseByHandle(handle) {
      this.loading = true;
      try {
        const data = await this.apiRequest(`/courses/${handle}`);
        return mapCourse(data);
      } catch (err) {
        // Fallback: try finding course by handle or slug in local state
        const found = this.courses.find(c => c.handle === handle || c.slug === handle || c.id == handle);
        if (found) return found;
        this.error = err.message;
        throw err;
      } finally {
        this.loading = false;
      }
    },

    async fetchCourseStudyData(handle) {
      if (!this.token) return null;
      try {
        const data = await this.apiRequest(`/courses/${handle}/study`);
        return mapCourse(data);
      } catch (err) {
        console.error(`Failed to fetch course study data for ${handle}:`, err);
        throw err;
      }
    },

    async fetchLessonProgress(handle) {
      if (!this.token) return [];
      try {
        const data = await this.apiRequest(`/courses/${handle}/progress`);
        return data.completed_lessons || [];
      } catch (err) {
        console.warn(`Could not fetch backend progress for ${handle}:`, err);
        return [];
      }
    },

    async saveLessonProgress(handle, completedLessons) {
      if (!this.token) return;
      try {
        await this.apiRequest(`/courses/${handle}/progress`, {
          method: 'POST',
          body: JSON.stringify({ completed_lessons: completedLessons })
        });
      } catch (err) {
        console.warn(`Could not save progress to backend for ${handle}:`, err);
      }
    },

    async fetchBlogs() {
      try {
        const data = await this.apiRequest('/blogs');
        this.blogPosts = data; // schema properties match exactly
      } catch (err) {
        console.error("Failed to load blog posts:", err);
      }
    },

    async sendContact(firstName, middleName, lastName, email, phone, courseHandle, message) {
      try {
        const res = await this.apiRequest('/contacts', {
          method: 'POST',
          body: JSON.stringify({
            first_name: firstName,
            middle_name: middleName,
            last_name: lastName,
            email,
            phone,
            course_handle: courseHandle,
            message
          })
        });
        return res;
      } catch (err) {
        console.error("Failed to send contact inquiry:", err);
        throw err;
      }
    },

    // --- Authentication Actions ---
    async register(fullname, email, password, referralCodeUsed = null) {
      try {
        const result = await this.apiRequest('/auth/register', {
          method: 'POST',
          body: JSON.stringify({
            fullname,
            email,
            password,
            referral_code_used: referralCodeUsed || null
          })
        });
        return result;
      } catch (err) {
        throw err;
      }
    },

    async login(email, password) {
      try {
        // OAuth2 Password Request Form format: URL Encoded form fields
        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);

        const result = await this.apiRequest('/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          },
          body: formData
        });

        this.token = result.access_token;
        localStorage.setItem('token', result.access_token);
        
        // Fetch user data in parallel
        await Promise.all([
          this.fetchUserMe(),
          this.fetchCart(),
          this.fetchOrders(),
          this.fetchReferrals(),
          this.fetchEnrollments()
        ]).catch(e => console.error("Error preloading user data on login:", e));
        
        return result;
      } catch (err) {
        throw err;
      }
    },

    async logout() {
      this.token = null;
      this.user = null;
      this.referralSummary = null;
      this.cart = [];
      this.orders = [];
      this.enrollments = [];
      localStorage.removeItem('token');
    },

    async fetchUserMe() {
      if (!this.token) return;
      try {
        const data = await this.apiRequest('/auth/me');
        this.user = {
          id: data.id,
          fullname: data.fullname,
          email: data.email,
          role: data.role,
          referralCode: data.referral_code,
          referredById: data.referred_by_id,
          createdAt: data.created_at
        };
        return this.user;
      } catch (err) {
        console.error("Failed to fetch user me profile:", err);
      }
    },

    async updateProfile(payload) {
      if (!this.token) return;
      const data = await this.apiRequest('/auth/me', {
        method: 'PUT',
        body: JSON.stringify(payload)
      });
      this.user = {
        id: data.id,
        fullname: data.fullname,
        email: data.email,
        role: data.role,
        referralCode: data.referral_code,
        referredById: data.referred_by_id,
        createdAt: data.created_at
      };
      return data;
    },

    async fetchReferrals() {
      if (!this.token) return;
      try {
        const data = await this.apiRequest('/auth/referrals');
        this.referralSummary = {
          totalReferrals: data.total_referrals,
          totalCommissionEarned: data.total_commission_earned,
          referralCode: data.referral_code,
          referralsList: data.referrals_list ? data.referrals_list.map(ref => ({
            id: ref.id,
            referredFullname: ref.referred_fullname,
            commissionAmount: ref.commission_amount,
            status: ref.status,
            createdAt: ref.created_at
          })) : []
        };
      } catch (err) {
        console.error("Failed to load referrals:", err);
      }
    },

    async fetchEnrollments() {
      if (!this.token) return;
      try {
        const data = await this.apiRequest('/enrollments');
        this.enrollments = data.map(item => ({
          id: item.id,
          courseId: item.course_id,
          orderId: item.order_id,
          enrolledAt: item.enrolled_at,
          createdAt: item.created_at || item.enrolled_at,
          course: item.course ? mapCourse(item.course) : null
        }));
      } catch (err) {
        console.error("Failed to load enrollments:", err);
      }
    },

    // --- Shopping Cart Actions ---
    async fetchCart() {
      if (!this.token) return;
      try {
        const data = await this.apiRequest('/cart');
        this.cart = data.map(item => ({
          id: item.id,
          course: mapCourse(item.course),
          createdAt: item.created_at
        }));
      } catch (err) {
        console.error("Failed to load cart:", err);
      }
    },

    async addToCart(courseIdOrObject) {
      if (!this.token) {
        throw new Error("Vui lòng đăng nhập để thêm khóa học vào giỏ hàng");
      }
      
      let rawId = courseIdOrObject;
      if (typeof courseIdOrObject === 'object' && courseIdOrObject !== null) {
        rawId = courseIdOrObject.id || courseIdOrObject.course_id;
      }
      
      const courseId = Number(rawId);
      if (!courseId || isNaN(courseId)) {
        throw new Error("Mã khóa học không hợp lệ");
      }

      try {
        const data = await this.apiRequest('/cart', {
          method: 'POST',
          body: JSON.stringify({ course_id: courseId })
        });
        
        // Optimistically update in-memory cart instantly without extra round-trip
        if (data && data.course) {
          const newItem = { id: data.id, course: mapCourse(data.course) };
          const existsIndex = this.cart.findIndex(i => i.course?.id === courseId);
          if (existsIndex >= 0) {
            this.cart[existsIndex] = newItem;
          } else {
            this.cart.push(newItem);
          }
        } else {
          this.fetchCart();
        }
        return data;
      } catch (err) {
        throw err;
      }
    },

    async removeFromCart(courseId) {
      if (!this.token) return;
      // Optimistic update in memory
      this.cart = this.cart.filter(item => item.course?.id !== courseId && item.id !== courseId);
      try {
        await this.apiRequest(`/cart/${courseId}`, {
          method: 'DELETE'
        });
      } catch (err) {
        // Rollback on error
        this.fetchCart();
        throw err;
      }
    },

    async clearCart() {
      if (!this.token) return;
      this.cart = [];
      try {
        await this.apiRequest('/cart', {
          method: 'DELETE'
        });
      } catch (err) {
        console.error("Failed to clear cart:", err);
      }
    },

    async buyNow(courseIdOrObject) {
      if (!this.token) {
        throw new Error("Vui lòng đăng nhập để đăng ký khóa học!");
      }
      let rawId = courseIdOrObject;
      if (typeof courseIdOrObject === 'object' && courseIdOrObject !== null) {
        rawId = courseIdOrObject.id || courseIdOrObject.course_id;
      }
      const courseId = Number(rawId);
      const alreadyInCart = this.cart.some(item => item.course?.id === courseId);
      if (!alreadyInCart && courseId) {
        await this.addToCart(courseId);
      }
      return true;
    },

    // --- Order Checkout Actions ---
    async fetchOrders() {
      if (!this.token) return;
      try {
        const data = await this.apiRequest('/orders');
        this.orders = data.map(order => ({
          id: order.id,
          totalPrice: order.total_price,
          discountApplied: order.discount_applied,
          status: order.status,
          createdAt: order.created_at,
          items: (order.items || []).map(item => ({
            id: item.id,
            price: item.price,
            course: mapCourse(item.course)
          }))
        }));
      } catch (err) {
        console.error("Failed to fetch orders:", err);
      }
    },

    async checkout() {
      if (!this.token) return;
      try {
        const order = await this.apiRequest('/orders/checkout', {
          method: 'POST'
        });
        await this.fetchCart(); // cart gets cleared on success
        await this.fetchOrders();
        return order;
      } catch (err) {
        throw err;
      }
    },

    async payOrder(orderId) {
      if (!this.token) return;
      try {
        const order = await this.apiRequest(`/orders/${orderId}/pay`, {
          method: 'POST'
        });
        await this.fetchOrders();
        await this.fetchEnrollments(); // refresh access list after payment
        await this.fetchUserMe();
        return order;
      } catch (err) {
        throw err;
      }
    },

    async checkEnrollment(courseId) {
      if (!this.token) return false;
      try {
        const data = await this.apiRequest(`/enrollments/check/${courseId}`);
        return data.enrolled;
      } catch (err) {
        return false;
      }
    },

    // --- Admin CRUD Actions ---
    async fetchAdminUsers() {
      if (!this.token) return;
      try {
        const data = await this.apiRequest('/admin/users');
        this.adminUsers = data.map(u => ({
          id: u.id,
          fullname: u.fullname,
          email: u.email,
          role: u.role,
          referralCode: u.referral_code,
          referredById: u.referred_by_id,
          isActive: u.is_active,
          createdAt: u.created_at
        }));
      } catch (err) {
        console.error("Failed to fetch admin users:", err);
      }
    },

    async fetchAdminOrders() {
      if (!this.token) return;
      try {
        const data = await this.apiRequest('/admin/orders');
        this.adminOrders = data.map(o => ({
          id: o.id,
          userId: o.user_id,
          userFullname: o.user_fullname,
          userEmail: o.user_email,
          totalPrice: o.total_price,
          discountApplied: o.discount_applied,
          status: o.status,
          createdAt: o.created_at,
          items: o.items.map(item => ({
            id: item.id,
            price: item.price,
            course: mapCourse(item.course)
          }))
        }));
      } catch (err) {
        console.error("Failed to fetch admin orders:", err);
      }
    },

    async fetchAdminContacts() {
      if (!this.token) return;
      try {
        const data = await this.apiRequest('/admin/contacts');
        this.adminContacts = data.map(c => ({
          id: c.id,
          firstName: c.first_name,
          middleName: c.middle_name,
          lastName: c.last_name,
          email: c.email,
          phone: c.phone,
          courseHandle: c.course_handle,
          message: c.message,
          isResolved: c.is_resolved,
          createdAt: c.created_at
        }));
      } catch (err) {
        console.error("Failed to fetch admin contacts:", err);
      }
    },

    // Orders CRUD
    async addAdminOrder(order) {
      if (!this.token) return;
      try {
        const payload = {
          user_id: Number(order.userId),
          course_ids: order.selectedCourses.map(c => c.id),
          discount_applied: Number(order.discountApplied) || 0,
          total_price: Number(order.totalPrice) || 0,
          status: order.status
        };
        await this.apiRequest('/admin/orders', {
          method: 'POST',
          body: JSON.stringify(payload)
        });
        await this.fetchAdminOrders();
      } catch (err) {
        console.error("Failed to add admin order:", err);
        throw err;
      }
    },
    async updateAdminOrderStatus(orderId, status) {
      if (!this.token) return;
      try {
        const order = this.adminOrders.find(o => o.id === orderId);
        const payload = {
          status: status,
          discount_applied: order ? order.discountApplied : 0,
          total_price: order ? order.totalPrice : 0
        };
        await this.apiRequest(`/admin/orders/${orderId}`, {
          method: 'PUT',
          body: JSON.stringify(payload)
        });
        await this.fetchAdminOrders();
      } catch (err) {
        console.error("Failed to update admin order status:", err);
        throw err;
      }
    },
    async deleteAdminOrder(orderId) {
      if (!this.token) return;
      try {
        await this.apiRequest(`/admin/orders/${orderId}`, {
          method: 'DELETE'
        });
        await this.fetchAdminOrders();
      } catch (err) {
        console.error("Failed to delete admin order:", err);
        throw err;
      }
    },

    // Users CRUD
    async addAdminUser(user) {
      if (!this.token) return;
      try {
        const payload = {
          fullname: user.fullname,
          email: user.email,
          password: user.password || 'Acc123456!',
          role: user.role,
          referred_by_id: user.referredById ? Number(user.referredById) : null
        };
        await this.apiRequest('/admin/users', {
          method: 'POST',
          body: JSON.stringify(payload)
        });
        await this.fetchAdminUsers();
      } catch (err) {
        console.error("Failed to add admin user:", err);
        throw err;
      }
    },
    async updateAdminUser(userId, updatedData) {
      if (!this.token) return;
      try {
        const payload = {
          fullname: updatedData.fullname,
          email: updatedData.email,
          role: updatedData.role,
          is_active: updatedData.isActive,
          referred_by_id: updatedData.referredById !== undefined ? (updatedData.referredById ? Number(updatedData.referredById) : 0) : undefined
        };
        await this.apiRequest(`/admin/users/${userId}`, {
          method: 'PUT',
          body: JSON.stringify(payload)
        });
        await this.fetchAdminUsers();
      } catch (err) {
        console.error("Failed to update admin user:", err);
        throw err;
      }
    },
    async deleteAdminUser(userId) {
      if (!this.token) return;
      try {
        await this.apiRequest(`/admin/users/${userId}`, {
          method: 'DELETE'
        });
        await this.fetchAdminUsers();
      } catch (err) {
        console.error("Failed to delete admin user:", err);
        throw err;
      }
    },

    // Contacts CRUD
    async toggleContactResolved(contactId) {
      if (!this.token) return;
      try {
        await this.apiRequest(`/admin/contacts/${contactId}/resolve`, {
          method: 'PUT'
        });
        await this.fetchAdminContacts();
      } catch (err) {
        console.error("Failed to toggle contact resolved status:", err);
        throw err;
      }
    },
    async deleteAdminContact(contactId) {
      if (!this.token) return;
      try {
        await this.apiRequest(`/admin/contacts/${contactId}`, {
          method: 'DELETE'
        });
        await this.fetchAdminContacts();
      } catch (err) {
        console.error("Failed to delete admin contact:", err);
        throw err;
      }
    },

    // Programs CRUD (Chương trình đào tạo)
    async fetchPrograms() {
      try {
        const data = await this.apiRequest('/courses/programs');
        this.programs = data;
      } catch (err) {
        console.error("Failed to fetch programs:", err);
      }
    },
    async addAdminProgram(program) {
      if (!this.token) return;
      try {
        await this.apiRequest('/admin/programs', {
          method: 'POST',
          body: JSON.stringify({
            title: program.title,
            slug: program.slug,
            description: program.description || '',
            image: program.image || '/images/default.jpg',
            course_ids: program.courseIds || []
          })
        });
        await this.fetchPrograms();
        await this.fetchCourses();
      } catch (err) {
        console.error("Failed to add admin program:", err);
        throw err;
      }
    },
    async updateAdminProgram(programId, updatedData) {
      if (!this.token) return;
      try {
        const payload = {
          title: updatedData.title,
          slug: updatedData.slug,
          description: updatedData.description,
          image: updatedData.image,
          course_ids: updatedData.courseIds
        };
        await this.apiRequest(`/admin/programs/${programId}`, {
          method: 'PUT',
          body: JSON.stringify(payload)
        });
        await this.fetchPrograms();
        await this.fetchCourses();
      } catch (err) {
        console.error("Failed to update admin program:", err);
        throw err;
      }
    },
    async deleteAdminProgram(programId) {
      if (!this.token) return;
      try {
        await this.apiRequest(`/admin/programs/${programId}`, {
          method: 'DELETE'
        });
        await this.fetchPrograms();
        await this.fetchCourses();
      } catch (err) {
        console.error("Failed to delete admin program:", err);
        throw err;
      }
    },

    // Bundles CRUD (Gói Combo Bundle)
    async fetchBundles() {
      try {
        const data = await this.apiRequest('/courses/bundles');
        this.bundles = data;
      } catch (err) {
        console.error("Failed to fetch bundles:", err);
      }
    },
    async addAdminBundle(bundle) {
      if (!this.token) return;
      try {
        await this.apiRequest('/admin/bundles', {
          method: 'POST',
          body: JSON.stringify({
            title: bundle.title,
            handle: bundle.handle,
            description: bundle.description || '',
            price: Number(bundle.price) || 0,
            original_price: Number(bundle.originalPrice) || 0,
            image: bundle.image || '/images/default.jpg',
            course_ids: bundle.courseIds || [],
            gift_course_ids: bundle.giftCourseIds || []
          })
        });
        await this.fetchBundles();
      } catch (err) {
        console.error("Failed to add admin bundle:", err);
        throw err;
      }
    },
    async updateAdminBundle(bundleId, updatedData) {
      if (!this.token) return;
      try {
        const payload = {
          title: updatedData.title,
          handle: updatedData.handle,
          description: updatedData.description,
          price: updatedData.price !== undefined ? Number(updatedData.price) : undefined,
          original_price: updatedData.originalPrice !== undefined ? Number(updatedData.originalPrice) : undefined,
          image: updatedData.image,
          course_ids: updatedData.courseIds,
          gift_course_ids: updatedData.giftCourseIds
        };
        await this.apiRequest(`/admin/bundles/${bundleId}`, {
          method: 'PUT',
          body: JSON.stringify(payload)
        });
        await this.fetchBundles();
      } catch (err) {
        console.error("Failed to update admin bundle:", err);
        throw err;
      }
    },
    async deleteAdminBundle(bundleId) {
      if (!this.token) return;
      try {
        await this.apiRequest(`/admin/bundles/${bundleId}`, {
          method: 'DELETE'
        });
        await this.fetchBundles();
      } catch (err) {
        console.error("Failed to delete admin bundle:", err);
        throw err;
      }
    },

    // Lecturers Action
    async fetchLecturers() {
      try {
        const data = await this.apiRequest('/lecturers');
        const { lecturersData } = await import('@/data/lecturers.js');
        if (Array.isArray(data)) {
          this.lecturers = data.map(l => {
            const staticItem = lecturersData.find(s => s.id === l.id) || {};
            return {
              ...staticItem,
              ...l,
              majorId: staticItem.majorId || 'ai-cong-nghe',
              majorName: staticItem.majorName || 'AI & Công nghệ Số',
              bioShort: l.bio_short || staticItem.bioShort || '',
              detailsHtml: l.details_html || staticItem.detailsHtml || '',
              avatarDriveLink: l.avatar_drive_link || staticItem.avatarDriveLink || '',
              driveProfile: l.drive_profile || staticItem.driveProfile || ''
            };
          });
        } else {
          this.lecturers = [];
        }
      } catch (err) {
        console.error("Failed to fetch lecturers API:", err);
        this.lecturers = [];
      }
    },
    async addAdminLecturer(lecturer) {
      if (!this.token) return;
      try {
        await this.apiRequest('/admin/lecturers', {
          method: 'POST',
          body: JSON.stringify({
            id: lecturer.id,
            name: lecturer.name,
            title: lecturer.title,
            tagline: lecturer.tagline || '',
            avatar: lecturer.avatar || '/images/default-avatar.jpg',
            avatar_drive_link: lecturer.avatarDriveLink || '',
            drive_profile: lecturer.driveProfile || '',
            bio_short: lecturer.bioShort || '',
            details_html: lecturer.detailsHtml || ''
          })
        });
        await this.fetchLecturers();
      } catch (err) {
        console.error("Failed to add lecturer:", err);
        throw err;
      }
    },
    async updateAdminLecturer(id, lecturer) {
      if (!this.token) return;
      try {
        await this.apiRequest(`/admin/lecturers/${id}`, {
          method: 'PUT',
          body: JSON.stringify({
            name: lecturer.name,
            title: lecturer.title,
            tagline: lecturer.tagline,
            avatar: lecturer.avatar,
            avatar_drive_link: lecturer.avatarDriveLink,
            drive_profile: lecturer.driveProfile,
            bio_short: lecturer.bioShort,
            details_html: lecturer.detailsHtml
          })
        });
        await this.fetchLecturers();
      } catch (err) {
        console.error("Failed to update lecturer:", err);
        throw err;
      }
    },
    async reorderLecturers(reorderedList) {
      if (!this.token) return;
      try {
        const payload = reorderedList.map((item, idx) => ({
          id: item.id,
          position: idx + 1
        }));
        await this.apiRequest('/admin/lecturers/reorder', {
          method: 'PUT',
          body: JSON.stringify(payload)
        });
        this.lecturers = [...reorderedList.map((item, idx) => ({ ...item, position: idx + 1 }))];
      } catch (err) {
        console.error("Failed to reorder lecturers:", err);
        throw err;
      }
    },
    async toggleLecturerFeatured(id) {
      if (!this.token) return;
      try {
        const updated = await this.apiRequest(`/admin/lecturers/${id}/toggle-featured`, {
          method: 'PUT'
        });
        const index = this.lecturers.findIndex(l => l.id === id);
        if (index !== -1) {
          this.lecturers[index].is_featured = updated.is_featured;
        }
        return updated;
      } catch (err) {
        console.error("Failed to toggle lecturer featured:", err);
        throw err;
      }
    },
    async deleteAdminLecturer(id) {
      if (!this.token) return;
      try {
        await this.apiRequest(`/admin/lecturers/${id}`, {
          method: 'DELETE'
        });
        await this.fetchLecturers();
      } catch (err) {
        console.error("Failed to delete lecturer:", err);
        throw err;
      }
    },

    // Courses CRUD
    async addAdminCourse(course) {
      if (!this.token) return;
      try {
        const payload = {
          title: course.title,
          category_slug: course.category,
          program_id: course.programId ? Number(course.programId) : null,
          handle: course.handle,
          price: Number(course.price) || 0,
          original_price: Number(course.originalPrice) || Number(course.price) || 0,
          image: course.image || '/images/default.jpg',
          description: course.description || '',
          duration: course.duration || '12 tuần',
          level: course.level || 'Trung cấp',
          curriculum_data: course.curriculumData || '',
          outcomes: course.outcomes || '',
          requirements: course.requirements || '',
          custom_roadmap: course.customRoadmap || '',
          lecturer_ids: course.lecturerIds || ''
        };
        await this.apiRequest('/admin/courses', {
          method: 'POST',
          body: JSON.stringify(payload)
        });
        await this.fetchCourses();
      } catch (err) {
        console.error("Failed to add admin course:", err);
        throw err;
      }
    },
    async updateAdminCourse(courseId, updatedData) {
      if (!this.token) return;
      try {
        const payload = {
          title: updatedData.title,
          category_slug: updatedData.category,
          program_id: updatedData.programId !== undefined ? (updatedData.programId ? Number(updatedData.programId) : null) : undefined,
          handle: updatedData.handle,
          price: updatedData.price !== undefined ? Number(updatedData.price) : undefined,
          original_price: updatedData.originalPrice !== undefined ? Number(updatedData.originalPrice) : undefined,
          image: updatedData.image,
          description: updatedData.description,
          duration: updatedData.duration,
          level: updatedData.level,
          curriculum_data: updatedData.curriculumData,
          outcomes: updatedData.outcomes,
          requirements: updatedData.requirements,
          custom_roadmap: updatedData.customRoadmap,
          lecturer_ids: updatedData.lecturerIds
        };
        await this.apiRequest(`/admin/courses/${courseId}`, {
          method: 'PUT',
          body: JSON.stringify(payload)
        });
        await this.fetchCourses();
      } catch (err) {
        console.error("Failed to update admin course:", err);
        throw err;
      }
    },
    async getCourseRelatedSummary(courseId) {
      if (!this.token) return null;
      try {
        return await this.apiRequest(`/admin/courses/${courseId}/related-summary`);
      } catch (err) {
        console.error("Failed to fetch course related summary:", err);
        return null;
      }
    },
    async deleteAdminCourse(courseId) {
      if (!this.token) {
        throw new Error("Bạn chưa đăng nhập hoặc phiên làm việc đã hết hạn. Vui lòng đăng nhập lại!");
      }
      const originalCourses = [...this.courses];
      // Optimistic update: Disappear immediately from UI (0ms delay)
      this.courses = this.courses.filter(c => String(c.id) !== String(courseId));
      try {
        await this.apiRequest(`/admin/courses/${courseId}`, {
          method: 'DELETE'
        });
      } catch (err) {
        // Rollback on error
        this.courses = originalCourses;
        console.error("Failed to delete admin course:", err);
        throw err;
      }
    },
    async fetchContactSettings() {
      try {
        const data = await this.apiRequest('/contacts/settings');
        this.contactSettings = data;
      } catch (err) {
        console.error("Failed to fetch contact settings:", err);
      }
    },
    async updateContactSettings(settings) {
      if (!this.token) return;
      try {
        const data = await this.apiRequest('/admin/contact-settings', {
          method: 'PUT',
          body: JSON.stringify(settings)
        });
        this.contactSettings = data;
        return data;
      } catch (err) {
        console.error("Failed to update contact settings:", err);
        throw err;
      }
    },
    async uploadImage(file) {
      const formData = new FormData();
      formData.append('file', file);
      
      const headers = {};
      if (this.token) {
        headers['Authorization'] = `Bearer ${this.token}`;
      }
      
      const res = await fetch(`${API_BASE}/upload/image`, {
        method: 'POST',
        headers,
        body: formData
      });
      
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'Lỗi khi tải ảnh lên Cloudinary');
      }
      
      const data = await res.json();
      return data.url;
    },

    // --- Engagement Actions (Reviews, Notes, Wishlist) ---
    async fetchCourseReviews(courseHandle) {
      try {
        return await this.apiRequest(`/engagement/reviews/${courseHandle}`);
      } catch (err) {
        console.error(`Failed to fetch reviews for ${courseHandle}:`, err);
        return [];
      }
    },

    async addCourseReview(courseHandle, reviewData) {
      try {
        const data = await this.apiRequest(`/engagement/reviews/${courseHandle}`, {
          method: 'POST',
          body: JSON.stringify(reviewData)
        });
        this.showToast('Cảm ơn bạn đã viết đánh giá cho khóa học!', 'success');
        return data;
      } catch (err) {
        this.showToast(err.message || 'Không thể gửi đánh giá', 'error');
        throw err;
      }
    },

    async fetchLessonNotes(courseHandle) {
      if (!this.token) return [];
      try {
        return await this.apiRequest(`/engagement/notes/${courseHandle}`);
      } catch (err) {
        console.error(`Failed to fetch notes for ${courseHandle}:`, err);
        return [];
      }
    },

    async addLessonNote(noteData) {
      try {
        const data = await this.apiRequest('/engagement/notes', {
          method: 'POST',
          body: JSON.stringify(noteData)
        });
        this.showToast('Đã lưu ghi chú bài học!', 'success');
        return data;
      } catch (err) {
        this.showToast(err.message || 'Không thể lưu ghi chú', 'error');
        throw err;
      }
    },

    async deleteLessonNote(noteId) {
      try {
        await this.apiRequest(`/engagement/notes/${noteId}`, {
          method: 'DELETE'
        });
        this.showToast('Đã xóa ghi chú', 'info');
      } catch (err) {
        this.showToast(err.message || 'Lỗi khi xóa ghi chú', 'error');
        throw err;
      }
    },

    async fetchWishlist() {
      if (!this.token) return [];
      try {
        const data = await this.apiRequest('/engagement/wishlist');
        this.wishlist = data.map(item => ({
          id: item.id,
          createdAt: item.created_at,
          course: mapCourse(item.course)
        }));
        return this.wishlist;
      } catch (err) {
        console.error('Failed to fetch wishlist:', err);
        return [];
      }
    },

    async toggleWishlist(courseId) {
      if (!this.token) {
        this.showToast('Vui lòng đăng nhập để lưu khóa học yêu thích!', 'error');
        return false;
      }
      try {
        const res = await this.apiRequest(`/engagement/wishlist/toggle/${courseId}`, {
          method: 'POST'
        });
        this.showToast(res.message, res.added ? 'success' : 'info');
        await this.fetchWishlist();
        return res.added;
      } catch (err) {
        this.showToast(err.message || 'Lỗi khi lưu wishlist', 'error');
        return false;
      }
    },

    // --- Marketing Actions (Coupons, Store Credit & Commissions) ---
    async applyCoupon(code, cartTotal) {
      try {
        const res = await this.apiRequest('/marketing/coupons/apply', {
          method: 'POST',
          body: JSON.stringify({ code, cart_total: cartTotal })
        });
        return res;
      } catch (err) {
        throw err;
      }
    },

    async fetchAdminCoupons() {
      if (!this.token) return;
      try {
        const data = await this.apiRequest('/marketing/admin/coupons');
        this.adminCoupons = data;
        return data;
      } catch (err) {
        console.error('Failed to fetch admin coupons:', err);
      }
    },

    async addAdminCoupon(couponData) {
      try {
        const data = await this.apiRequest('/marketing/admin/coupons', {
          method: 'POST',
          body: JSON.stringify(couponData)
        });
        await this.fetchAdminCoupons();
        this.showToast('Tạo mã giảm giá thành công!', 'success');
        return data;
      } catch (err) {
        this.showToast(err.message || 'Lỗi khi tạo mã giảm giá', 'error');
        throw err;
      }
    },

    async deleteAdminCoupon(couponId) {
      try {
        await this.apiRequest(`/marketing/admin/coupons/${couponId}`, {
          method: 'DELETE'
        });
        await this.fetchAdminCoupons();
        this.showToast('Đã xóa mã giảm giá', 'success');
      } catch (err) {
        this.showToast(err.message || 'Lỗi khi xóa mã', 'error');
        throw err;
      }
    },

    async fetchMyReferralSummary() {
      if (!this.token) return;
      try {
        const data = await this.apiRequest('/marketing/referrals/my-summary');
        this.referralSummary = {
          referralCode: data.referral_code,
          storeCreditBalance: data.store_credit_balance,
          totalReferrals: data.total_referrals,
          totalCommissionEarned: data.total_commission_earned,
          referralsList: (data.referrals_list || []).map(ref => ({
            id: ref.id,
            referredFullname: ref.referred_fullname,
            commissionAmount: ref.commission_amount,
            status: ref.status,
            createdAt: ref.created_at
          }))
        };
        // Also update local user object store_credit_balance
        if (this.user) {
          this.user.storeCreditBalance = data.store_credit_balance;
        }
        return this.referralSummary;
      } catch (err) {
        console.error('Failed to load referral summary:', err);
      }
    },

    async checkoutWithOptions(couponCode = null, useStoreCredit = false) {
      if (!this.token) return;
      try {
        let endpoint = '/marketing/checkout-options';
        const params = new URLSearchParams();
        if (couponCode) params.append('coupon_code', couponCode);
        if (useStoreCredit) params.append('use_store_credit', 'true');
        if (params.toString()) {
          endpoint += `?${params.toString()}`;
        }
        const order = await this.apiRequest(endpoint, {
          method: 'POST'
        });
        await Promise.all([
          this.fetchCart(),
          this.fetchOrders(),
          this.fetchUserMe(),
          this.fetchMyReferralSummary()
        ]);
        return order;
      } catch (err) {
        throw err;
      }
    },

    async fetchAdminCommissions() {
      if (!this.token) return;
      try {
        const data = await this.apiRequest('/marketing/admin/commissions');
        this.adminCommissions = data;
        return data;
      } catch (err) {
        console.error('Failed to fetch admin commissions:', err);
      }
    },

    async setAdminCommission(userId, courseId, percent) {
      try {
        const data = await this.apiRequest('/marketing/admin/commissions/set', {
          method: 'POST',
          body: JSON.stringify({
            user_id: Number(userId),
            course_id: Number(courseId),
            commission_percent: Number(percent)
          })
        });
        await this.fetchAdminCommissions();
        this.showToast('Cấu hình tỷ lệ hoa hồng thành công!', 'success');
        return data;
      } catch (err) {
        this.showToast(err.message || 'Lỗi khi cài đặt hoa hồng', 'error');
        throw err;
      }
    },

    // --- Admin Data Export ---
    async exportAdminReport(type = 'orders', period = 'all') {
      if (!this.token) return;
      try {
        const url = `${API_BASE}/admin/export/${type}?period=${period}`;
        const res = await fetch(url, {
          headers: {
            'Authorization': `Bearer ${this.token}`
          }
        });
        if (!res.ok) throw new Error('Không thể tải file xuất dữ liệu');
        const blob = await res.blob();
        const downloadUrl = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = downloadUrl;
        a.download = `bao_cao_${type}_${period}_acc.csv`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(downloadUrl);
        this.showToast('Xuất báo cáo dữ liệu thành công!', 'success');
      } catch (err) {
        this.showToast(err.message || 'Lỗi xuất file dữ liệu', 'error');
      }
    },

    // --- Admin Testimonials CRUD ---
    async fetchAdminTestimonials() {
      if (!this.token) return;
      try {
        const data = await this.apiRequest('/admin/testimonials');
        this.adminTestimonials = data;
        return data;
      } catch (err) {
        console.error("Failed to fetch admin testimonials:", err);
      }
    },

    async addAdminTestimonial(testimonial) {
      if (!this.token) return;
      try {
        const payload = {
          name: testimonial.name,
          role: testimonial.role || '',
          company: testimonial.company || '',
          text: testimonial.text || '',
          image: testimonial.image || '',
          rating: Number(testimonial.rating) || 5,
          quote: testimonial.quote || testimonial.text || '',
          course_name: testimonial.courseName || '',
          testimonial_type: testimonial.testimonialType || 'text',
          youtube_id: testimonial.youtubeId || '',
          thumbnail: testimonial.thumbnail || '',
          video_url: testimonial.videoUrl || ''
        };
        await this.apiRequest('/admin/testimonials', {
          method: 'POST',
          body: JSON.stringify(payload)
        });
        await this.fetchAdminTestimonials();
        this.showToast('Thêm cảm nhận học viên thành công!', 'success');
      } catch (err) {
        console.error("Failed to add admin testimonial:", err);
        this.showToast(err.message || 'Không thể thêm cảm nhận', 'error');
        throw err;
      }
    },

    async updateAdminTestimonial(id, testimonial) {
      if (!this.token) return;
      try {
        const payload = {
          name: testimonial.name,
          role: testimonial.role,
          company: testimonial.company,
          text: testimonial.text,
          image: testimonial.image,
          rating: Number(testimonial.rating) || 5,
          quote: testimonial.quote,
          course_name: testimonial.courseName,
          testimonial_type: testimonial.testimonialType,
          youtube_id: testimonial.youtubeId,
          thumbnail: testimonial.thumbnail,
          video_url: testimonial.videoUrl
        };
        await this.apiRequest(`/admin/testimonials/${id}`, {
          method: 'PUT',
          body: JSON.stringify(payload)
        });
        await this.fetchAdminTestimonials();
        this.showToast('Cập nhật cảm nhận học viên thành công!', 'success');
      } catch (err) {
        console.error("Failed to update admin testimonial:", err);
        this.showToast(err.message || 'Không thể cập nhật cảm nhận', 'error');
        throw err;
      }
    },

    async deleteAdminTestimonial(id) {
      if (!this.token) return;
      try {
        await this.apiRequest(`/admin/testimonials/${id}`, {
          method: 'DELETE'
        });
        await this.fetchAdminTestimonials();
        this.showToast('Đã xóa cảm nhận học viên thành công!', 'success');
      } catch (err) {
        console.error("Failed to delete admin testimonial:", err);
        this.showToast(err.message || 'Không thể xóa cảm nhận', 'error');
        throw err;
      }
    },

    // --- Admin Projects CRUD ---
    async fetchProjects() {
      try {
        const data = await this.apiRequest('/projects');
        if (Array.isArray(data) && data.length > 0) {
          this.projects = data.map(p => ({
            id: p.id,
            category: p.category,
            categoryName: p.category_name,
            title: p.title,
            summary: p.summary,
            image: p.image,
            date: p.date,
            client: p.client,
            driveProfile: p.drive_profile,
            content: typeof p.content === 'string' ? (JSON.parse(p.content || '[]')) : (p.content || [])
          }));
        } else {
          const { projectsData } = await import('@/data/projects.js');
          this.projects = projectsData;
        }
      } catch (err) {
        console.error("Failed to fetch projects:", err);
        const { projectsData } = await import('@/data/projects.js');
        this.projects = projectsData;
      }
    },

    async fetchAdminProjects() {
      if (!this.token) return;
      try {
        const data = await this.apiRequest('/admin/projects');
        this.adminProjects = data;
        return data;
      } catch (err) {
        console.error("Failed to fetch admin projects:", err);
      }
    },

    async addAdminProject(project) {
      if (!this.token) return;
      try {
        const payload = {
          id: project.id,
          category: project.category,
          category_name: project.categoryName || 'Dự án Doanh nghiệp',
          title: project.title,
          summary: project.summary || '',
          image: project.image || '',
          date: project.date || '',
          client: project.client || '',
          drive_profile: project.driveProfile || '',
          content: typeof project.content === 'object' ? JSON.stringify(project.content) : (project.content || '[]')
        };
        await this.apiRequest('/admin/projects', {
          method: 'POST',
          body: JSON.stringify(payload)
        });
        await this.fetchAdminProjects();
        await this.fetchProjects();
        this.showToast('Thêm dự án thành công!', 'success');
      } catch (err) {
        console.error("Failed to add admin project:", err);
        this.showToast(err.message || 'Không thể thêm dự án', 'error');
        throw err;
      }
    },

    async updateAdminProject(id, project) {
      if (!this.token) return;
      try {
        const payload = {
          category: project.category,
          category_name: project.categoryName,
          title: project.title,
          summary: project.summary,
          image: project.image,
          date: project.date,
          client: project.client,
          drive_profile: project.driveProfile,
          content: typeof project.content === 'object' ? JSON.stringify(project.content) : project.content
        };
        await this.apiRequest(`/admin/projects/${id}`, {
          method: 'PUT',
          body: JSON.stringify(payload)
        });
        await this.fetchAdminProjects();
        await this.fetchProjects();
        this.showToast('Cập nhật dự án thành công!', 'success');
      } catch (err) {
        console.error("Failed to update admin project:", err);
        this.showToast(err.message || 'Không thể cập nhật dự án', 'error');
        throw err;
      }
    },

    async deleteAdminProject(id) {
      if (!this.token) return;
      try {
        await this.apiRequest(`/admin/projects/${id}`, {
          method: 'DELETE'
        });
        await this.fetchAdminProjects();
        await this.fetchProjects();
        this.showToast('Đã xóa dự án thành công!', 'success');
      } catch (err) {
        console.error("Failed to delete admin project:", err);
        this.showToast(err.message || 'Không thể xóa dự án', 'error');
        throw err;
      }
    },

    // --- Admin Blog Posts CRUD ---
    async fetchAdminBlogPosts() {
      if (!this.token) return;
      try {
        const data = await this.apiRequest('/admin/blogs');
        this.adminBlogPosts = data;
        this.blogPosts = data;
        return data;
      } catch (err) {
        console.error("Failed to fetch admin blog posts:", err);
      }
    },

    async addAdminBlogPost(blog) {
      if (!this.token) return;
      try {
        const payload = {
          title: blog.title,
          handle: blog.handle,
          category: blog.category || 'AI 2026',
          image: blog.image || '',
          excerpt: blog.excerpt || '',
          date: blog.date || '',
          link: blog.link || `/blog/${blog.handle}`,
          content: blog.content || ''
        };
        await this.apiRequest('/admin/blogs', {
          method: 'POST',
          body: JSON.stringify(payload)
        });
        await this.fetchAdminBlogPosts();
        this.showToast('Thêm bài viết / tin tức thành công!', 'success');
      } catch (err) {
        console.error("Failed to add admin blog post:", err);
        this.showToast(err.message || 'Không thể thêm bài viết', 'error');
        throw err;
      }
    },

    async updateAdminBlogPost(id, blog) {
      if (!this.token) return;
      try {
        const payload = {
          title: blog.title,
          handle: blog.handle,
          category: blog.category,
          image: blog.image,
          excerpt: blog.excerpt,
          date: blog.date,
          link: blog.link,
          content: blog.content
        };
        await this.apiRequest(`/admin/blogs/${id}`, {
          method: 'PUT',
          body: JSON.stringify(payload)
        });
        await this.fetchAdminBlogPosts();
        this.showToast('Cập nhật bài viết thành công!', 'success');
      } catch (err) {
        console.error("Failed to update admin blog post:", err);
        this.showToast(err.message || 'Không thể cập nhật bài viết', 'error');
        throw err;
      }
    },

    async deleteAdminBlogPost(id) {
      if (!this.token) return;
      try {
        await this.apiRequest(`/admin/blogs/${id}`, {
          method: 'DELETE'
        });
        await this.fetchAdminBlogPosts();
        this.showToast('Đã xóa bài viết thành công!', 'success');
      } catch (err) {
        console.error("Failed to delete admin blog post:", err);
        this.showToast(err.message || 'Không thể xóa bài viết', 'error');
        throw err;
      }
    }

  }
});
