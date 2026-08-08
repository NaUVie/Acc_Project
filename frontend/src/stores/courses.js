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
  curriculumData: c.curriculum_data
});

export const useCourseStore = defineStore('courses', {
  state: () => ({
    // Catalog states
    courses: [],
    programs: [],
    bundles: [],
    blogPosts: [],
    loading: false,
    error: null,

    // Auth states
    token: localStorage.getItem('token') || null,
    user: null,
    referralSummary: null,

    // Cart states
    cart: [], // holds cart items: { id, course }

    // Orders states
    orders: [], // holds order history

    // Enrollment states (courses user has paid access to)
    enrollments: [], // list of { id, course, enrolled_at }

    // Admin Dashboard States
    adminUsers: [],
    adminOrders: [],
    adminContacts: [],
    contactSettings: null
  }),

  getters: {
    getCoursesByCategory: (state) => (category) => {
      return state.courses.filter(course => course.category === category);
    },
    getCourseByHandle: (state) => (handle) => {
      return state.courses.find(course => course.handle === handle);
    },
    getBlogPosts: (state) => {
      return state.blogPosts;
    },
    isAuthenticated: (state) => !!state.token,
    cartCount: (state) => state.cart.length,
    cartTotal: (state) => state.cart.reduce((sum, item) => sum + item.course.price, 0),
    userMe: (state) => state.user,
    enrolledCourseIds: (state) => state.enrollments.map(e => e.course?.id),
    isEnrolled: (state) => (courseId) => {
      return state.enrollments.some(e => e.course?.id === courseId || e.course?.handle === courseId);
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
    async fetchCourses() {
      this.loading = true;
      try {
        const data = await this.apiRequest('/courses');
        this.courses = data.map(mapCourse);
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
      } catch (err) {
        this.logout();
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

    // --- Shopping Cart Actions ---
    async fetchCart() {
      if (!this.token) return;
      try {
        const data = await this.apiRequest('/cart');
        this.cart = data.map(item => ({
          id: item.id,
          course: mapCourse(item.course)
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
      const targetCourse = this.courses.find(c => c.id === courseId);

      // 1. Optimistic instant cart update in memory (0ms delay!)
      if (targetCourse) {
        this.cart = [{ id: Date.now(), course: targetCourse }];
      }

      // 2. Background network sync to DB
      try {
        await this.apiRequest('/cart', { method: 'DELETE' });
        const data = await this.apiRequest('/cart', {
          method: 'POST',
          body: JSON.stringify({ course_id: courseId })
        });
        if (data && data.course) {
          this.cart = [{ id: data.id, course: mapCourse(data.course) }];
        }
      } catch (err) {
        console.error("Buy now sync error:", err);
      }
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
          items: order.items.map(item => ({
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

    async fetchEnrollments() {
      if (!this.token) return;
      try {
        const data = await this.apiRequest('/enrollments');
        this.enrollments = data.map(e => ({
          id: e.id,
          course: mapCourse(e.course),
          enrolledAt: e.enrolled_at
        }));
      } catch (err) {
        console.error('Failed to fetch enrollments:', err);
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
          password: 'defaultPassword123!',
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
          curriculum_data: course.curriculumData || ''
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
          curriculum_data: updatedData.curriculumData
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
    async deleteAdminCourse(courseId) {
      if (!this.token) return;
      try {
        await this.apiRequest(`/admin/courses/${courseId}`, {
          method: 'DELETE'
        });
        await this.fetchCourses();
      } catch (err) {
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
    }
  }
});
