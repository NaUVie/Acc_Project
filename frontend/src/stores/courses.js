import { defineStore } from 'pinia';

const API_BASE = import.meta.env.VITE_API_URL || 'https://acc-project-n4ji.onrender.com/api';

// Helper to clean course properties mapping from API to Frontend camelCase format
const mapCourse = (c) => ({
  id: c.id,
  title: c.title,
  category: c.category_slug,
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
    userMe: (state) => state.user
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
          throw new Error(errData.detail || `HTTP error! status: ${response.status}`);
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
        
        // Fetch profile
        await this.fetchUserMe();
        
        // Fetch cart online
        await this.fetchCart();
        
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
      localStorage.removeItem('token');
    },

    async fetchUserMe() {
      if (!this.token) return;
      try {
        const data = await this.apiRequest('/auth/me');
        this.user = data;
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
      this.user = data;
      return data;
    },

    async fetchReferrals() {
      if (!this.token) return;
      try {
        const data = await this.apiRequest('/auth/referrals');
        this.referralSummary = data;
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

    async addToCart(courseId) {
      if (!this.token) {
        // Fallback for anonymous users: add to memory, or prompt login
        throw new Error("Vui lòng đăng nhập để thêm khóa học vào giỏ hàng");
      }
      try {
        const data = await this.apiRequest('/cart', {
          method: 'POST',
          body: JSON.stringify({ course_id: courseId })
        });
        await this.fetchCart();
        return data;
      } catch (err) {
        throw err;
      }
    },

    async removeFromCart(courseId) {
      if (!this.token) return;
      try {
        await this.apiRequest(`/cart/${courseId}`, {
          method: 'DELETE'
        });
        await this.fetchCart();
      } catch (err) {
        throw err;
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
        await this.fetchUserMe(); // update referral balances if applicable
        return order;
      } catch (err) {
        throw err;
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

    // Courses CRUD
    async addAdminCourse(course) {
      if (!this.token) return;
      try {
        const payload = {
          title: course.title,
          category_slug: course.category,
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
    }
  }
});
