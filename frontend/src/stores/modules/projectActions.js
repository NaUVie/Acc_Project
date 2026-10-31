let fetchProjectsPromise = null;

export const projectActions = {
  async fetchProjects(force = false) {
    if (!force && this.projectsLoaded && this.projects.length > 0) {
      return this.projects;
    }
    if (fetchProjectsPromise) {
      return fetchProjectsPromise;
    }

    this.projectsLoading = true;
    fetchProjectsPromise = (async () => {
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
          this.projects = [];
        }
        this.projectsLoaded = true;
        return this.projects;
      } catch (err) {
        console.error("Failed to fetch projects:", err);
        this.projects = [];
        this.projectsLoaded = true;
        return this.projects;
      } finally {
        this.projectsLoading = false;
        fetchProjectsPromise = null;
      }
    })();

    return fetchProjectsPromise;
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
      await this.fetchProjects(true);
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
      await this.fetchProjects(true);
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
      await this.fetchProjects(true);
      this.showToast('Đã xóa dự án thành công!', 'success');
    } catch (err) {
      console.error("Failed to delete admin project:", err);
      this.showToast(err.message || 'Không thể xóa dự án', 'error');
      throw err;
    }
  },

  async fetchProjectReviews(projectId) {
    try {
      return await this.apiRequest(`/projects/${projectId}/reviews`);
    } catch (err) {
      console.warn(`Could not fetch reviews for project ${projectId}:`, err);
      return [];
    }
  },

  async submitProjectReview(projectId, reviewData) {
    try {
      const data = await this.apiRequest(`/projects/${projectId}/reviews`, {
        method: 'POST',
        body: JSON.stringify(reviewData)
      });
      this.showToast('Nhận xét của bạn đã được gửi thành công và đang chờ quản trị viên duyệt!', 'success');
      return data;
    } catch (err) {
      this.showToast(err.message || 'Không thể gửi nhận xét', 'error');
      throw err;
    }
  },

  async fetchProjectReviewsAdmin(projectId = null) {
    const url = projectId ? `/admin/project-reviews?project_id=${projectId}` : '/admin/project-reviews';
    return await this.apiRequest(url);
  },

  async toggleProjectReviewApproval(reviewId) {
    try {
      const updated = await this.apiRequest(`/admin/project-reviews/${reviewId}/toggle-approval`, {
        method: 'PUT'
      });
      this.showToast('Đã cập nhật trạng thái duyệt nhận xét!', 'success');
      return updated;
    } catch (err) {
      this.showToast(err.message || 'Lỗi khi cập nhật trạng thái', 'error');
      throw err;
    }
  },

  async deleteProjectReviewAdmin(reviewId) {
    try {
      await this.apiRequest(`/admin/project-reviews/${reviewId}`, {
        method: 'DELETE'
      });
      this.showToast('Đã xóa nhận xét thành công!', 'success');
      return true;
    } catch (err) {
      this.showToast(err.message || 'Lỗi khi xóa nhận xét', 'error');
      throw err;
    }
  }
};

