import { defineStore } from 'pinia';

const API_BASE = 'http://127.0.0.1:8000/api';

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
  level: c.level
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
    orders: [] // holds order history
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
    cartTotal: (state) => state.cart.reduce((sum, item) => sum + item.course.price, 0)
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

    async sendContact(name, email, courseHandle, message) {
      try {
        return await this.apiRequest('/contacts', {
          method: 'POST',
          body: JSON.stringify({ name, email, course_handle: courseHandle, message })
        });
      } catch (err) {
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
    }
  }
});
