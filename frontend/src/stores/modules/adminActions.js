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
          phone: u.phone,
          role: u.role,
          referralCode: u.referral_code,
          referredById: u.referred_by_id,
          storeCreditBalance: u.store_credit_balance || 0,
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
      // Update in-place without heavy remote re-fetch
      if (order) {
        order.status = status;
        try {
          localStorage.setItem('acc_admin_orders_cache', JSON.stringify(this.adminOrders));
        } catch (e) {}
      }
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
      // Remove in-place without heavy remote re-fetch
      if (this.adminOrders) {
        this.adminOrders = this.adminOrders.filter(o => o.id !== orderId);
        try {
          localStorage.setItem('acc_admin_orders_cache', JSON.stringify(this.adminOrders));
        } catch (e) {}
      }
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
        phone: updatedData.phone,
        role: updatedData.role,
        is_active: updatedData.isActive,
        referred_by_id: updatedData.referredById !== undefined ? (updatedData.referredById ? Number(updatedData.referredById) : 0) : undefined
      };
      if (updatedData.password && updatedData.password.trim()) {
        payload.password = updatedData.password.trim();
      }
      const updatedUser = await this.apiRequest(`/admin/users/${userId}`, {
        method: 'PUT',
        body: JSON.stringify(payload)
      });

      // Update in-place in local state instantly without redundant re-fetch
      if (updatedUser && this.adminUsers) {
        const idx = this.adminUsers.findIndex(u => u.id === userId);
        if (idx !== -1) {
          this.adminUsers[idx] = {
            ...this.adminUsers[idx],
            fullname: updatedUser.fullname,
            email: updatedUser.email,
            phone: updatedUser.phone,
            role: updatedUser.role,
            isActive: updatedUser.is_active,
            referralCode: updatedUser.referral_code,
            referredById: updatedUser.referred_by_id,
            storeCreditBalance: updatedUser.store_credit_balance || 0
          };
          try {
            localStorage.setItem('acc_admin_users_cache', JSON.stringify(this.adminUsers));
          } catch (e) {}
        }
      }
      return updatedUser;
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
      if (this.adminUsers) {
        this.adminUsers = this.adminUsers.filter(u => u.id !== userId);
        try {
          localStorage.setItem('acc_admin_users_cache', JSON.stringify(this.adminUsers));
        } catch (e) {}
      }
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
      // Update in-place
      const contact = (this.adminContacts || []).find(c => c.id === contactId);
      if (contact) {
        contact.is_resolved = !contact.is_resolved;
        try {
          localStorage.setItem('acc_admin_contacts_cache', JSON.stringify(this.adminContacts));
        } catch (e) {}
      }
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
      // Remove in-place
      if (this.adminContacts) {
        this.adminContacts = this.adminContacts.filter(c => c.id !== contactId);
        try {
          localStorage.setItem('acc_admin_contacts_cache', JSON.stringify(this.adminContacts));
        } catch (e) {}
      }
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
      if (data && this.adminCoupons) {
        this.adminCoupons.unshift(data);
      }
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
      if (this.adminCoupons) {
        this.adminCoupons = this.adminCoupons.filter(c => c.id !== couponId);
      }
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
  },

  async fetchAdminUserCourses(userId) {
    if (!this.token) return [];
    try {
      return await this.apiRequest(`/admin/users/${userId}/courses`);
    } catch (err) {
      console.error("Failed to fetch user courses:", err);
      return [];
    }
  },

  async grantAdminUserCourse(userId, courseId) {
    if (!this.token) return null;
    try {
      const res = await this.apiRequest(`/admin/users/${userId}/courses`, {
        method: 'POST',
        body: JSON.stringify({ course_id: Number(courseId) })
      });
      this.showToast('Cấp quyền truy cập khóa học thành công!', 'success');
      return res;
    } catch (err) {
      this.showToast(err.message || 'Lỗi khi cấp quyền khóa học', 'error');
      throw err;
    }
  },

  async revokeAdminUserCourse(userId, courseId) {
    if (!this.token) return false;
    try {
      await this.apiRequest(`/admin/users/${userId}/courses/${courseId}`, {
        method: 'DELETE'
      });
      this.showToast('Đã thu hồi quyền truy cập khóa học', 'success');
      return true;
    } catch (err) {
      this.showToast(err.message || 'Lỗi khi thu hồi quyền khóa học', 'error');
      throw err;
    }
  },
};