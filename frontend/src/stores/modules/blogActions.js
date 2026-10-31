let fetchBlogsPromise = null;

export const blogActions = {
  async fetchBlogs(force = false) {
    if (!force && this.blogsLoaded && this.blogPosts.length > 0) {
      return this.blogPosts;
    }
    if (fetchBlogsPromise) {
      return fetchBlogsPromise;
    }

    this.blogsLoading = true;
    fetchBlogsPromise = (async () => {
      try {
        const data = await this.apiRequest('/blogs');
        this.blogPosts = data || [];
        this.blogsLoaded = true;
        return this.blogPosts;
      } catch (err) {
        console.error("Failed to load blog posts:", err);
        return this.blogPosts;
      } finally {
        this.blogsLoading = false;
        fetchBlogsPromise = null;
      }
    })();

    return fetchBlogsPromise;
  },

  async fetchAdminBlogPosts(force = false) {
    if (!this.token) return [];
    if (!force && this.adminBlogPosts && this.adminBlogPosts.length > 0) {
      return this.adminBlogPosts;
    }
    try {
      const data = await this.apiRequest('/admin/blogs');
      if (Array.isArray(data)) {
        this.adminBlogPosts = data;
        this.blogPosts = data;
      }
      return this.adminBlogPosts;
    } catch (err) {
      console.error("Failed to fetch admin blog posts:", err);
      return this.adminBlogPosts || [];
    }
  },

  async addAdminBlogPost(blog) {
    if (!this.token) return;
    try {
      const payload = {
        title: blog.title,
        handle: blog.handle,
        category: blog.category || 'AI 2026',
        image: blog.image || '',
        excerpt: blog.excerpt || '',
        date: blog.date || '',
        link: blog.link || `/blog/${blog.handle}`,
        content: blog.content || ''
      };
      const created = await this.apiRequest('/admin/blogs', {
        method: 'POST',
        body: JSON.stringify(payload)
      });
      if (created) {
        this.adminBlogPosts = [created, ...(this.adminBlogPosts || [])];
        this.blogPosts = [created, ...(this.blogPosts || [])];
      }
      this.fetchAdminBlogPosts(true).catch(() => {});
      this.showToast('Thêm bài viết / tin tức thành công!', 'success');
      return created;
    } catch (err) {
      console.error("Failed to add admin blog post:", err);
      this.showToast(err.message || 'Không thể thêm bài viết', 'error');
      throw err;
    }
  },

  async updateAdminBlogPost(id, blog) {
    if (!this.token) return;
    try {
      const payload = {
        title: blog.title,
        handle: blog.handle,
        category: blog.category,
        image: blog.image,
        excerpt: blog.excerpt,
        date: blog.date,
        link: blog.link,
        content: blog.content
      };
      const updated = await this.apiRequest(`/admin/blogs/${id}`, {
        method: 'PUT',
        body: JSON.stringify(payload)
      });
      if (updated) {
        const updateItem = (item) => item.id === id ? { ...item, ...updated } : item;
        this.adminBlogPosts = (this.adminBlogPosts || []).map(updateItem);
        this.blogPosts = (this.blogPosts || []).map(updateItem);
      }
      this.fetchAdminBlogPosts(true).catch(() => {});
      this.showToast('Cập nhật bài viết thành công!', 'success');
      return updated;
    } catch (err) {
      console.error("Failed to update admin blog post:", err);
      this.showToast(err.message || 'Không thể cập nhật bài viết', 'error');
      throw err;
    }
  },

  async deleteAdminBlogPost(id) {
    if (!this.token) return;
    try {
      await this.apiRequest(`/admin/blogs/${id}`, {
        method: 'DELETE'
      });
      this.adminBlogPosts = (this.adminBlogPosts || []).filter(b => b.id !== id);
      this.blogPosts = (this.blogPosts || []).filter(b => b.id !== id);
      this.fetchAdminBlogPosts(true).catch(() => {});
      this.showToast('Đã xóa bài viết thành công!', 'success');
    } catch (err) {
      console.error("Failed to delete admin blog post:", err);
      this.showToast(err.message || 'Không thể xóa bài viết', 'error');
      throw err;
    }
  },

  async fetchBlogCategories(force = false) {
    if (!force && this.blogCategories && this.blogCategories.length > 0) {
      return this.blogCategories;
    }
    try {
      const endpoint = this.token ? '/admin/blogs/categories' : '/blogs/categories';
      const data = await this.apiRequest(endpoint);
      if (Array.isArray(data)) {
        this.blogCategories = data;
      }
      return this.blogCategories;
    } catch (err) {
      console.error("Failed to fetch blog categories:", err);
      return this.blogCategories || [];
    }
  },

  async addBlogCategory(category) {
    try {
      const created = await this.apiRequest('/admin/blogs/categories', {
        method: 'POST',
        body: JSON.stringify(category)
      });
      if (created) {
        this.blogCategories = [...(this.blogCategories || []), created];
        this.showToast?.('Đã thêm chuyên mục bài viết mới!', 'success');
        return created;
      }
    } catch (err) {
      console.error("Failed to add blog category:", err);
      this.showToast?.(err.message || 'Không thể thêm chuyên mục', 'error');
      throw err;
    }
  },

  async updateBlogCategory(id, category) {
    try {
      const updated = await this.apiRequest(`/admin/blogs/categories/${id}`, {
        method: 'PUT',
        body: JSON.stringify(category)
      });
      if (updated) {
        this.blogCategories = (this.blogCategories || []).map(c => c.id === id ? updated : c);
        this.fetchAdminBlogPosts(true).catch(() => {});
        this.showToast?.('Đã cập nhật chuyên mục bài viết!', 'success');
        return updated;
      }
    } catch (err) {
      console.error("Failed to update blog category:", err);
      this.showToast?.(err.message || 'Không thể cập nhật chuyên mục', 'error');
      throw err;
    }
  },

  async deleteBlogCategory(id) {
    try {
      await this.apiRequest(`/admin/blogs/categories/${id}`, {
        method: 'DELETE'
      });
      this.blogCategories = (this.blogCategories || []).filter(c => c.id !== id);
      this.showToast?.('Đã xóa chuyên mục bài viết thành công!', 'success');
    } catch (err) {
      console.error("Failed to delete blog category:", err);
      this.showToast?.(err.message || 'Không thể xóa chuyên mục', 'error');
      throw err;
    }
  }
};

