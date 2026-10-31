import { API_BASE, mapCourse } from './helpers';

let fetchAdminUsersPromise = null;
let fetchAdminOrdersPromise = null;
let fetchAdminContactsPromise = null;

export const adminActions = {
  async fetchAdminUsers() {
    if (!this.token) return;
    if (fetchAdminUsersPromise) return fetchAdminUsersPromise;
    fetchAdminUsersPromise = (async () => {
      try {
        const data = await this.apiRequest('/admin/users');
        this.adminUsers = (data || []).map(u => ({
          id: u.id,
          fullname: u.fullname,
          email: u.email,
          role: u.role,
          referralCode: u.referral_code,
          referredById: u.referred_by_id,
          isActive: u.is_active,
          createdAt: u.created_at
        }));
        try {
          localStorage.setItem('acc_admin_users_cache', JSON.stringify(this.adminUsers));
        } catch (e) {}
        return this.adminUsers;
      } catch (err) {
        console.error("Failed to fetch admin users:", err);
      } finally {
        fetchAdminUsersPromise = null;
      }
    })();
    return fetchAdminUsersPromise;
  },

  async fetchAdminOrders() {
    if (!this.token) return;
    if (fetchAdminOrdersPromise) return fetchAdminOrdersPromise;
    fetchAdminOrdersPromise = (async () => {
      try {
        const data = await this.apiRequest('/admin/orders');
        this.adminOrders = (data || []).map(o => ({
          id: o.id,
          userId: o.user_id,
          userFullname: o.user_fullname,
          userEmail: o.user_email,
          totalPrice: o.total_price,
          discountApplied: o.discount_applied,
          status: o.status,
          createdAt: o.created_at,
          items: (o.items || []).map(item => ({
            id: item.id,
            price: item.price,
            course: mapCourse(item.course)
          }))
        }));
        try {
          localStorage.setItem('acc_admin_orders_cache', JSON.stringify(this.adminOrders));
        } catch (e) {}
        return this.adminOrders;
      } catch (err) {
        console.error("Failed to fetch admin orders:", err);
      } finally {
        fetchAdminOrdersPromise = null;
      }
    })();
    return fetchAdminOrdersPromise;
  },

  async fetchAdminContacts() {
    if (!this.token) return;
    if (fetchAdminContactsPromise) return fetchAdminContactsPromise;
    fetchAdminContactsPromise = (async () => {
      try {
        const data = await this.apiRequest('/admin/contacts');
        this.adminContacts = (data || []).map(c => ({
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
        try {
          localStorage.setItem('acc_admin_contacts_cache', JSON.stringify(this.adminContacts));
        } catch (e) {}
        return this.adminContacts;
      } catch (err) {
        console.error("Failed to fetch admin contacts:", err);
      } finally {
        fetchAdminContactsPromise = null;
      }
    })();
    return fetchAdminContactsPromise;
  },

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
  }
};

