let fetchBannersPromise = null;
let fetchPartnersPromise = null;

export const marketingActions = {
  async fetchBanners(force = false) {
    if (!force && this.bannersLoaded && this.banners.length > 0) {
      return this.banners;
    }
    if (fetchBannersPromise) {
      return fetchBannersPromise;
    }

    this.bannersLoading = true;
    fetchBannersPromise = (async () => {
      try {
        const data = await this.apiRequest('/courses/banners');
        this.banners = data || [];
        this.bannersLoaded = true;
        return this.banners;
      } catch (err) {
        console.error("Failed to fetch banners:", err);
        return this.banners;
      } finally {
        this.bannersLoading = false;
        fetchBannersPromise = null;
      }
    })();

    return fetchBannersPromise;
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
    await Promise.all([this.fetchAdminBanners().catch(() => {}), this.fetchBanners(true).catch(() => {})]);
    return data;
  },

  async updateBanner(bannerId, bannerData) {
    const data = await this.apiRequest(`/admin/banners/${bannerId}`, {
      method: 'PUT',
      body: JSON.stringify(bannerData)
    });
    await Promise.all([this.fetchAdminBanners().catch(() => {}), this.fetchBanners(true).catch(() => {})]);
    return data;
  },

  async deleteBanner(bannerId) {
    const data = await this.apiRequest(`/admin/banners/${bannerId}`, {
      method: 'DELETE'
    });
    if (this.adminBanners) {
      this.adminBanners = this.adminBanners.filter(b => b.id !== bannerId);
    }
    if (this.banners) {
      this.banners = this.banners.filter(b => b.id !== bannerId);
    }
    return data;
  },

  async fetchPartners(force = false) {
    if (!force && this.partners && this.partners.length > 0) {
      return this.partners;
    }
    if (fetchPartnersPromise) {
      return fetchPartnersPromise;
    }
    fetchPartnersPromise = (async () => {
      try {
        const data = await this.apiRequest('/courses/partners');
        if (Array.isArray(data) && data.length > 0) {
          this.partners = data;
          try {
            localStorage.setItem('acc_partners_cache', JSON.stringify(data));
          } catch (e) {}
        }
        return this.partners;
      } catch (err) {
        console.error("Failed to fetch partners:", err);
        return this.partners || [];
      } finally {
        fetchPartnersPromise = null;
      }
    })();
    return fetchPartnersPromise;
  },

  async fetchAdminPartners() {
    try {
      const data = await this.apiRequest('/admin/partners');
      this.adminPartners = data;
      return data;
    } catch (err) {
      console.error("Failed to fetch admin partners:", err);
      throw err;
    }
  },

  async createPartner(partnerData) {
    const data = await this.apiRequest('/admin/partners', {
      method: 'POST',
      body: JSON.stringify(partnerData)
    });
    await Promise.all([this.fetchAdminPartners().catch(() => {}), this.fetchPartners().catch(() => {})]);
    this.showToast('Thêm đối tác thành công!', 'success');
    return data;
  },

  async updatePartner(partnerId, partnerData) {
    const data = await this.apiRequest(`/admin/partners/${partnerId}`, {
      method: 'PUT',
      body: JSON.stringify(partnerData)
    });
    await Promise.all([this.fetchAdminPartners().catch(() => {}), this.fetchPartners().catch(() => {})]);
    this.showToast('Cập nhật đối tác thành công!', 'success');
    return data;
  },

  async deletePartner(partnerId) {
    const data = await this.apiRequest(`/admin/partners/${partnerId}`, {
      method: 'DELETE'
    });
    if (this.adminPartners) {
      this.adminPartners = this.adminPartners.filter(p => p.id !== partnerId);
    }
    if (this.partners) {
      this.partners = this.partners.filter(p => p.id !== partnerId);
    }
    this.showToast('Xóa đối tác thành công!', 'success');
    return data;
  },

  async fetchContactSettings(force = false) {
    if (!force && this.contactSettings) return this.contactSettings;
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

  async fetchHomeIntroSettings(force = false) {
    if (!force && this.homeIntroSettings) return this.homeIntroSettings;
    try {
      const data = await this.apiRequest('/contacts/home-intro');
      this.homeIntroSettings = data;
      return data;
    } catch (err) {
      console.error("Failed to fetch home intro settings:", err);
      return null;
    }
  },

  async updateHomeIntroSettings(settings) {
    try {
      const data = await this.apiRequest('/admin/home-intro', {
        method: 'PUT',
        body: JSON.stringify(settings)
      });
      this.homeIntroSettings = data;
      return data;
    } catch (err) {
      console.error("Failed to update home intro settings:", err);
      throw err;
    }
  },

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
      if (this.adminTestimonials) {
        this.adminTestimonials = this.adminTestimonials.filter(t => t.id !== id);
      }
      this.showToast('Đã xóa cảm nhận học viên thành công!', 'success');
    } catch (err) {
      console.error("Failed to delete admin testimonial:", err);
      this.showToast(err.message || 'Không thể xóa cảm nhận', 'error');
      throw err;
    }
  }
};

