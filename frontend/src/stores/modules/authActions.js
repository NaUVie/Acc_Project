import { mapCourse } from './helpers';

let fetchUserMePromise = null;
let fetchReferralsPromise = null;
let fetchEnrollmentsPromise = null;

export const authActions = {
  async register(fullname, email, password, referralCodeUsed = null, phone = null) {
    try {
      const result = await this.apiRequest('/auth/register', {
        method: 'POST',
        body: JSON.stringify({
          fullname,
          email,
          phone: phone || null,
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

  async requestPasswordReset(email, phone = null, note = null) {
    try {
      const result = await this.apiRequest('/auth/forgot-password', {
        method: 'POST',
        body: JSON.stringify({
          email,
          phone: phone || null,
          note: note || null
        })
      });
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
    localStorage.removeItem('user');
  },

  async fetchUserMe() {
    if (!this.token) return;
    if (fetchUserMePromise) return fetchUserMePromise;
    fetchUserMePromise = (async () => {
      try {
        const data = await this.apiRequest('/auth/me');
        this.user = {
          id: data.id,
          fullname: data.fullname,
          email: data.email,
          phone: data.phone || '',
          role: data.role,
          referralCode: data.referral_code,
          referredById: data.referred_by_id,
          createdAt: data.created_at
        };
        try {
          localStorage.setItem('user', JSON.stringify(this.user));
        } catch (e) {}
        return this.user;
      } catch (err) {
        console.error("Failed to fetch user me profile:", err);
      } finally {
        fetchUserMePromise = null;
      }
    })();
    return fetchUserMePromise;
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
    if (fetchReferralsPromise) return fetchReferralsPromise;
    fetchReferralsPromise = (async () => {
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
        return this.referralSummary;
      } catch (err) {
        console.error("Failed to load referrals:", err);
      } finally {
        fetchReferralsPromise = null;
      }
    })();
    return fetchReferralsPromise;
  },

  async fetchEnrollments() {
    if (!this.token) return;
    if (fetchEnrollmentsPromise) return fetchEnrollmentsPromise;
    fetchEnrollmentsPromise = (async () => {
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
        return this.enrollments;
      } catch (err) {
        console.error("Failed to load enrollments:", err);
      } finally {
        fetchEnrollmentsPromise = null;
      }
    })();
    return fetchEnrollmentsPromise;
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
      if (this.user) {
        this.user.storeCreditBalance = data.store_credit_balance;
      }
      return this.referralSummary;
    } catch (err) {
      console.error('Failed to load referral summary:', err);
    }
  }
};

