import { mapCourse } from './helpers';

export const cartActions = {
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
    this.cart = this.cart.filter(item => item.course?.id !== courseId && item.id !== courseId);
    try {
      await this.apiRequest(`/cart/${courseId}`, {
        method: 'DELETE'
      });
    } catch (err) {
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
      await this.fetchCart();
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
      await this.fetchEnrollments();
      await this.fetchUserMe();
      await this.fetchCart();
      return order;
    } catch (err) {
      throw err;
    }
  },

  async createVnpayPaymentUrl(orderId, bankCode = null) {
    if (!this.token) return null;
    try {
      const query = bankCode ? `?bank_code=${encodeURIComponent(bankCode)}` : '';
      const res = await this.apiRequest(`/orders/${orderId}/vnpay-url${query}`, {
        method: 'POST'
      });
      return res;
    } catch (err) {
      console.error("Failed to create VNPay URL:", err);
      throw err;
    }
  },

  async verifyVnpayReturn(queryParams) {
    try {
      const search = new URLSearchParams(queryParams).toString();
      const res = await this.apiRequest(`/orders/vnpay-return?${search}`);
      if (this.token) {
        await this.fetchOrders();
        await this.fetchEnrollments();
        await this.fetchUserMe();
        await this.fetchCart();
      }
      return res;
    } catch (err) {
      console.error("Failed to verify VNPay return:", err);
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
  }
};

