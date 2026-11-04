let fetchBannersPromise = null;
let fetchPartnersPromise = null;
let fetchBoardMembersPromise = null;

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

  async fetchAdminBanners(force = false) {
    try {
      const url = force ? `/admin/banners?_t=${Date.now()}` : '/admin/banners';
      const data = await this.apiRequest(url, force ? { cache: 'no-store' } : {});
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

  async fetchAdminPartners(force = false) {
    try {
      const url = force ? `/admin/partners?_t=${Date.now()}` : '/admin/partners';
      const data = await this.apiRequest(url, force ? { cache: 'no-store' } : {});
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

  async fetchBoardMembers(force = false) {
    if (!force && this.boardMembers && this.boardMembers.length > 0) {
      return this.boardMembers;
    }
    if (fetchBoardMembersPromise) {
      return fetchBoardMembersPromise;
    }
    this.boardMembersLoading = true;
    fetchBoardMembersPromise = (async () => {
      try {
        const data = await this.apiRequest('/courses/board-members');
        if (Array.isArray(data)) {
          this.boardMembers = data;
          this.boardMembersLoaded = true;
          try {
            localStorage.setItem('acc_board_members_cache', JSON.stringify(data));
          } catch (e) {}
        }
        return this.boardMembers;
      } catch (err) {
        console.error("Failed to fetch board members:", err);
        return this.boardMembers || [];
      } finally {
        this.boardMembersLoading = false;
        fetchBoardMembersPromise = null;
      }
    })();
    return fetchBoardMembersPromise;
  },

  async fetchAdminBoardMembers(force = false) {
    try {
      const url = force ? `/admin/board-members?_t=${Date.now()}` : '/admin/board-members';
      const data = await this.apiRequest(url, force ? { cache: 'no-store' } : {});
      this.adminBoardMembers = data || [];
      return this.adminBoardMembers;
    } catch (err) {
      console.error("Failed to fetch admin board members:", err);
      throw err;
    }
  },

  async createBoardMember(memberData) {
    const data = await this.apiRequest('/admin/board-members', {
      method: 'POST',
      body: JSON.stringify(memberData)
    });
    await Promise.all([this.fetchAdminBoardMembers(true).catch(() => {}), this.fetchBoardMembers(true).catch(() => {})]);
    this.showToast('Thêm thành viên ban điều hành thành công!', 'success');
    return data;
  },

  async updateBoardMember(memberId, memberData) {
    const data = await this.apiRequest(`/admin/board-members/${memberId}`, {
      method: 'PUT',
      body: JSON.stringify(memberData)
    });
    await Promise.all([this.fetchAdminBoardMembers(true).catch(() => {}), this.fetchBoardMembers(true).catch(() => {})]);
    this.showToast('Cập nhật thành viên ban điều hành thành công!', 'success');
    return data;
  },

  async deleteBoardMember(memberId) {
    const data = await this.apiRequest(`/admin/board-members/${memberId}`, {
      method: 'DELETE'
    });
    if (this.adminBoardMembers) {
      this.adminBoardMembers = this.adminBoardMembers.filter(m => m.id !== memberId);
    }
    if (this.boardMembers) {
      this.boardMembers = this.boardMembers.filter(m => m.id !== memberId);
    }
    this.showToast('Xóa thành viên ban điều hành thành công!', 'success');
    return data;
  },

    async fetchAdmissions(force = false) {
    if (!force && this.admissions && this.admissions.length > 0) {
      return this.admissions;
    }
    if (fetchAdmissionsPromise) {
      return fetchAdmissionsPromise;
    }
    this.admissionsLoading = true;
    fetchAdmissionsPromise = (async () => {
      try {
        const data = await this.apiRequest('/courses/admissions');
        if (Array.isArray(data)) {
          this.admissions = data;
          this.admissionsLoaded = true;
          try {
            localStorage.setItem('acc_admissions_cache', JSON.stringify(data));
          } catch (e) {}
        }
        return this.admissions;
      } catch (err) {
        console.error("Failed to fetch admissions:", err);
        return this.admissions || [];
      } finally {
        this.admissionsLoading = false;
        fetchAdmissionsPromise = null;
      }
    })();
    return fetchAdmissionsPromise;
  },

  async fetchAdmissionBySlug(slug, force = false) {
    try {
      const data = await this.apiRequest(`/courses/admissions/${slug}`);
      return data;
    } catch (err) {
      console.error(`Failed to fetch admission post ${slug}:`, err);
      return null;
    }
  },

  async fetchAdminAdmissions(force = false) {
    try {
      const url = force ? `/admin/admissions?_t=${Date.now()}` : '/admin/admissions';
      const data = await this.apiRequest(url, force ? { cache: 'no-store' } : {});
      this.adminAdmissions = data || [];
      return this.adminAdmissions;
    } catch (err) {
      console.error("Failed to fetch admin admissions:", err);
      throw err;
    }
  },

  async createAdmissionPost(postData) {
    const data = await this.apiRequest('/admin/admissions', {
      method: 'POST',
      body: JSON.stringify(postData)
    });
    await Promise.all([this.fetchAdminAdmissions(true).catch(() => {}), this.fetchAdmissions(true).catch(() => {})]);
    this.showToast('Thêm bài viết tuyển sinh thành công!', 'success');
    return data;
  },

  async updateAdmissionPost(id, postData) {
    const data = await this.apiRequest(`/admin/admissions/${id}`, {
      method: 'PUT',
      body: JSON.stringify(postData)
    });
    await Promise.all([this.fetchAdminAdmissions(true).catch(() => {}), this.fetchAdmissions(true).catch(() => {})]);
    this.showToast('Cập nhật bài viết tuyển sinh thành công!', 'success');
    return data;
  },

  async deleteAdmissionPost(id) {
    const data = await this.apiRequest(`/admin/admissions/${id}`, {
      method: 'DELETE'
    });
    if (this.adminAdmissions) {
      this.adminAdmissions = this.adminAdmissions.filter(p => p.id !== id);
    }
    if (this.admissions) {
      this.admissions = this.admissions.filter(p => p.id !== id);
    }
    this.showToast('Xóa bài viết tuyển sinh thành công!', 'success');
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

  async fetchAdminTestimonials(force = false) {
    if (!this.token) return;
    try {
      const url = force ? `/admin/testimonials?_t=${Date.now()}` : '/admin/testimonials';
      const data = await this.apiRequest(url, force ? { cache: 'no-store' } : {});
      this.adminTestimonials = (data || []).map(item => ({
        ...item,
        courseId: item.course_id || null,
        courseName: item.course_name || '',
        isApproved: item.is_approved !== false
      }));
      return this.adminTestimonials;
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
        course_id: (testimonial.courseId !== null && testimonial.courseId !== undefined && testimonial.courseId !== '') ? Number(testimonial.courseId) : null,
        is_approved: testimonial.isApproved !== undefined ? testimonial.isApproved : true,
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
        course_id: testimonial.courseId !== undefined ? (testimonial.courseId ? Number(testimonial.courseId) : null) : undefined,
        is_approved: testimonial.isApproved !== undefined ? testimonial.isApproved : undefined,
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

