import { mapCourse } from './helpers';

let fetchCoursesPromise = null;
let fetchCategoriesPromise = null;

export const courseActions = {
  async fetchCategories(force = false) {
    if (!force && this.categories && this.categories.length > 0 && fetchCategoriesPromise) {
      return fetchCategoriesPromise;
    }
    fetchCategoriesPromise = (async () => {
      try {
        const url = force ? '/courses/categories?_t=' + Date.now() : '/courses/categories';
        const data = await this.apiRequest(url);
        if (Array.isArray(data) && data.length > 0) {
          this.categories = data;
          try {
            localStorage.setItem('acc_categories_cache', JSON.stringify(data));
          } catch (e) {}
        }
        return this.categories;
      } catch (err) {
        console.error("Failed to fetch categories:", err);
        return this.categories || [];
      } finally {
        fetchCategoriesPromise = null;
      }
    })();
    return fetchCategoriesPromise;
  },

  async createCategory(catData) {
    try {
      const data = await this.apiRequest('/admin/categories', {
        method: 'POST',
        body: JSON.stringify(catData)
      });
      await this.fetchCategories(true);
      this.showToast(`Đã thêm chuyên mục "${data.name}"`, 'success');
      return data;
    } catch (err) {
      this.showToast(err.message || 'Lỗi khi tạo chuyên mục', 'error');
      throw err;
    }
  },

  async updateCategory(slug, name) {
    try {
      const data = await this.apiRequest(`/admin/categories/${slug}`, {
        method: 'PUT',
        body: JSON.stringify({ name })
      });
      await this.fetchCategories();
      this.showToast(`Đã cập nhật chuyên mục "${name}"`, 'success');
      return data;
    } catch (err) {
      this.showToast(err.message || 'Lỗi khi sửa chuyên mục', 'error');
      throw err;
    }
  },

  async deleteCategory(slug) {
    try {
      await this.apiRequest(`/admin/categories/${slug}`, {
        method: 'DELETE'
      });
      await this.fetchCategories();
      this.showToast('Đã xóa chuyên mục', 'success');
    } catch (err) {
      this.showToast(err.message || 'Lỗi khi xóa chuyên mục', 'error');
      throw err;
    }
  },

  async fetchCourses(force = false) {
    if (!force && this.coursesLoaded && this.courses.length > 0) {
      return this.courses;
    }
    if (fetchCoursesPromise) {
      return fetchCoursesPromise;
    }

    this.loading = true;
    fetchCoursesPromise = (async () => {
      try {
        const [coursesData] = await Promise.all([
          this.apiRequest('/courses'),
          this.fetchCategories().catch(() => {}),
          this.fetchBanners().catch(() => {})
        ]);
        this.courses = coursesData.map(mapCourse);
        this.coursesLoaded = true;
        return this.courses;
      } catch (err) {
        this.error = err.message;
        return this.courses;
      } finally {
        this.loading = false;
        fetchCoursesPromise = null;
      }
    })();

    return fetchCoursesPromise;
  },

  async fetchCourseByHandle(handle) {
    this.loading = true;
    try {
      const data = await this.apiRequest(`/courses/${handle}`);
      return mapCourse(data);
    } catch (err) {
      const found = this.courses.find(c => c.handle === handle || c.slug === handle || c.id == handle);
      if (found) return found;
      this.error = err.message;
      throw err;
    } finally {
      this.loading = false;
    }
  },

  async fetchCourseStudyData(handle) {
    if (!this.token) return null;
    try {
      const data = await this.apiRequest(`/courses/${handle}/study`);
      return mapCourse(data);
    } catch (err) {
      console.error(`Failed to fetch course study data for ${handle}:`, err);
      throw err;
    }
  },

  async fetchLessonProgress(handle) {
    if (!this.token) return [];
    try {
      const data = await this.apiRequest(`/courses/${handle}/progress`);
      return data.completed_lessons || [];
    } catch (err) {
      console.warn(`Could not fetch backend progress for ${handle}:`, err);
      return [];
    }
  },

  async saveLessonProgress(handle, completedLessons) {
    if (!this.token) return;
    try {
      await this.apiRequest(`/courses/${handle}/progress`, {
        method: 'POST',
        body: JSON.stringify({ completed_lessons: completedLessons })
      });
    } catch (err) {
      console.warn(`Could not save progress to backend for ${handle}:`, err);
    }
  },

  async addAdminCourse(course) {
    if (!this.token) return;
    try {
      const payload = {
        title: course.title,
        category_slug: course.category,
        program_id: course.programId ? Number(course.programId) : null,
        handle: course.handle,
        price: Number(course.price) || 0,
        original_price: Number(course.originalPrice) || Number(course.price) || 0,
        image: course.image || '/images/default.jpg',
        cover_image: course.coverImage || null,
        description: course.description || '',
        duration: course.duration || '12 tuần',
        level: course.level || 'Trung cấp',
        curriculum_data: course.curriculumData || '',
        outcomes: course.outcomes || '',
        requirements: course.requirements || '',
        custom_roadmap: course.customRoadmap || '',
        lecturer_ids: course.lecturerIds || ''
      };
      await this.apiRequest('/admin/courses', {
        method: 'POST',
        body: JSON.stringify(payload)
      });
      await this.fetchCourses(true);
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
        program_id: updatedData.programId !== undefined ? (updatedData.programId ? Number(updatedData.programId) : null) : undefined,
        handle: updatedData.handle,
        price: updatedData.price !== undefined ? Number(updatedData.price) : undefined,
        original_price: updatedData.originalPrice !== undefined ? Number(updatedData.originalPrice) : undefined,
        image: updatedData.image,
        cover_image: updatedData.coverImage !== undefined ? updatedData.coverImage : undefined,
        description: updatedData.description,
        duration: updatedData.duration,
        level: updatedData.level,
        curriculum_data: updatedData.curriculumData,
        outcomes: updatedData.outcomes,
        requirements: updatedData.requirements,
        custom_roadmap: updatedData.customRoadmap,
        lecturer_ids: updatedData.lecturerIds
      };
      await this.apiRequest(`/admin/courses/${courseId}`, {
        method: 'PUT',
        body: JSON.stringify(payload)
      });
      await this.fetchCourses(true);
    } catch (err) {
      console.error("Failed to update admin course:", err);
      throw err;
    }
  },

  async getCourseRelatedSummary(courseId) {
    if (!this.token) return null;
    try {
      return await this.apiRequest(`/admin/courses/${courseId}/related-summary`);
    } catch (err) {
      console.error("Failed to fetch course related summary:", err);
      return null;
    }
  },

  async deleteAdminCourse(courseId) {
    if (!this.token) {
      throw new Error("Bạn chưa đăng nhập hoặc phiên làm việc đã hết hạn. Vui lòng đăng nhập lại!");
    }
    const originalCourses = [...this.courses];
    this.courses = this.courses.filter(c => String(c.id) !== String(courseId));
    try {
      await this.apiRequest(`/admin/courses/${courseId}`, {
        method: 'DELETE'
      });
    } catch (err) {
      this.courses = originalCourses;
      console.error("Failed to delete admin course:", err);
      throw err;
    }
  },

  async fetchCourseReviews(courseHandle) {
    try {
      return await this.apiRequest(`/engagement/reviews/${courseHandle}`);
    } catch (err) {
      console.error(`Failed to fetch reviews for ${courseHandle}:`, err);
      return [];
    }
  },

  async addCourseReview(courseHandle, reviewData) {
    try {
      const data = await this.apiRequest(`/engagement/reviews/${courseHandle}`, {
        method: 'POST',
        body: JSON.stringify(reviewData)
      });
      this.showToast('Cảm ơn bạn đã viết đánh giá cho khóa học!', 'success');
      return data;
    } catch (err) {
      this.showToast(err.message || 'Không thể gửi đánh giá', 'error');
      throw err;
    }
  },

  async fetchLessonNotes(courseHandle) {
    if (!this.token) return [];
    try {
      return await this.apiRequest(`/engagement/notes/${courseHandle}`);
    } catch (err) {
      console.error(`Failed to fetch notes for ${courseHandle}:`, err);
      return [];
    }
  },

  async addLessonNote(noteData) {
    try {
      const data = await this.apiRequest('/engagement/notes', {
        method: 'POST',
        body: JSON.stringify(noteData)
      });
      this.showToast('Đã lưu ghi chú bài học!', 'success');
      return data;
    } catch (err) {
      this.showToast(err.message || 'Không thể lưu ghi chú', 'error');
      throw err;
    }
  },

  async deleteLessonNote(noteId) {
    try {
      await this.apiRequest(`/engagement/notes/${noteId}`, {
        method: 'DELETE'
      });
      this.showToast('Đã xóa ghi chú', 'info');
    } catch (err) {
      this.showToast(err.message || 'Lỗi khi xóa ghi chú', 'error');
      throw err;
    }
  },

  // Safe backward compatibility fallbacks for deprecated Programs and Bundles
  async fetchPrograms() { return []; },
  async addAdminProgram() { return {}; },
  async updateAdminProgram() { return {}; },
  async deleteAdminProgram() { return true; },
  async fetchBundles() { return []; },
  async addAdminBundle() { return {}; },
  async updateAdminBundle() { return {}; },
  async deleteAdminBundle() { return true; }
};

