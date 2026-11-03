let fetchLecturersPromise = null;
let fetchLecturerMajorsPromise = null;

export const lecturerActions = {
  async fetchLecturerMajors(force = false) {
    if (!force && this.lecturerMajorsLoaded && this.lecturerMajors.length > 0) {
      return this.lecturerMajors;
    }
    if (fetchLecturerMajorsPromise) {
      return fetchLecturerMajorsPromise;
    }

    fetchLecturerMajorsPromise = (async () => {
      try {
        const endpoint = this.token ? '/admin/lecturer-majors' : '/lecturers/majors';
        const url = force ? `${endpoint}?_t=${Date.now()}` : endpoint;
        const data = await this.apiRequest(url, force ? { cache: 'no-store' } : {});
        if (Array.isArray(data)) {
          this.lecturerMajors = data.map(m => ({
            id: m.id,
            name: m.name,
            description: m.description || '',
            icon: m.icon || '🎓',
            badge: m.badge || m.name.toUpperCase(),
            position: m.position || 0
          }));
          this.lecturerMajorsLoaded = true;
          try {
            localStorage.setItem('acc_lecturer_majors_v2', JSON.stringify(this.lecturerMajors));
          } catch {}
        } else {
          this.lecturerMajors = [];
        }
        return this.lecturerMajors;
      } catch (err) {
        console.error("Failed to fetch lecturer majors:", err);
        return this.lecturerMajors || [];
      } finally {
        fetchLecturerMajorsPromise = null;
      }
    })();

    return fetchLecturerMajorsPromise;
  },

  async addAdminLecturerMajor(majorData) {
    if (!this.token) return;
    try {
      const data = await this.apiRequest('/admin/lecturer-majors', {
        method: 'POST',
        body: JSON.stringify({
          id: majorData.id,
          name: majorData.name,
          description: majorData.description || '',
          icon: majorData.icon || '🎓',
          badge: majorData.badge || majorData.name.toUpperCase(),
          position: Number(majorData.position) || 0
        })
      });
      await this.fetchLecturerMajors();
      return data;
    } catch (err) {
      console.error("Failed to add lecturer major:", err);
      throw err;
    }
  },

  async updateAdminLecturerMajor(id, majorData) {
    if (!this.token) return;
    try {
      const data = await this.apiRequest(`/admin/lecturer-majors/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
          name: majorData.name,
          description: majorData.description,
          icon: majorData.icon,
          badge: majorData.badge,
          position: majorData.position !== undefined ? Number(majorData.position) : undefined
        })
      });
      await this.fetchLecturerMajors();
      await this.fetchLecturers();
      return data;
    } catch (err) {
      console.error("Failed to update lecturer major:", err);
      throw err;
    }
  },

  async deleteAdminLecturerMajor(id) {
    if (!this.token) return;
    try {
      const data = await this.apiRequest(`/admin/lecturer-majors/${id}`, {
        method: 'DELETE'
      });
      await this.fetchLecturerMajors();
      await this.fetchLecturers();
      return data;
    } catch (err) {
      console.error("Failed to delete lecturer major:", err);
      throw err;
    }
  },

  async fetchLecturers(force = false) {
    if (!force && this.lecturersLoaded && this.lecturers && this.lecturers.length > 0) {
      return this.lecturers;
    }
    if (fetchLecturersPromise) {
      return fetchLecturersPromise;
    }

    this.lecturersLoading = true;
    fetchLecturersPromise = (async () => {
      try {
        const isAdmin = this.user?.role === 'admin' && typeof window !== 'undefined' && window.location.pathname.startsWith('/admin');
        const endpoint = isAdmin ? '/admin/lecturers' : '/lecturers';
        const url = force ? `${endpoint}?_t=${Date.now()}` : endpoint;
        const data = await this.apiRequest(url, force ? { cache: 'no-store' } : {});
        if (Array.isArray(data) && data.length > 0) {
          this.lecturers = data.map(l => {
            let mIds = [];
            if (l.major_ids) {
              mIds = l.major_ids.split(',').map(s => s.trim()).filter(Boolean);
            } else if (l.major_id) {
              mIds = [l.major_id];
            }
            return {
              ...l,
              major_positions: l.major_positions || {},
              majorIds: mIds,
              majorId: mIds[0] || l.major_id || 'ai-cong-nghe',
              majorName: l.major_name || 'AI & Công nghệ Số',
              bioShort: l.bio_short || '',
              detailsHtml: l.details_html || '',
              avatar: l.avatar || '',
              avatarDriveLink: l.avatar_drive_link || '',
              driveProfile: l.drive_profile || '',
              show_detail_btn: l.show_detail_btn !== undefined ? !!l.show_detail_btn : false
            };
          });
          this.lecturersLoaded = true;
          try {
            localStorage.setItem('acc_lecturers_v2', JSON.stringify(this.lecturers));
          } catch {}
        }
        return this.lecturers;
      } catch (err) {
        console.error("Failed to fetch lecturers API:", err);
        return this.lecturers || [];
      } finally {
        this.lecturersLoading = false;
        fetchLecturersPromise = null;
      }
    })();

    return fetchLecturersPromise;
  },

  async addAdminLecturer(lecturer) {
    if (!this.token) return;
    try {
      const majorIdsStr = Array.isArray(lecturer.majorIds) ? lecturer.majorIds.join(',') : (lecturer.majorIds || lecturer.majorId || '');
      const primaryMajorId = Array.isArray(lecturer.majorIds) && lecturer.majorIds.length > 0 ? lecturer.majorIds[0] : (lecturer.majorId || null);
      const created = await this.apiRequest('/admin/lecturers', {
        method: 'POST',
        body: JSON.stringify({
          id: lecturer.id,
          name: lecturer.name,
          title: lecturer.title,
          tagline: lecturer.tagline || '',
          avatar: lecturer.avatar || '/images/default-avatar.jpg',
          avatar_drive_link: lecturer.avatarDriveLink || '',
          drive_profile: lecturer.driveProfile || '',
          bio_short: lecturer.bioShort || '',
          details_html: lecturer.detailsHtml || '',
          major_id: primaryMajorId,
          major_ids: majorIdsStr,
          major_name: lecturer.majorName || null,
          position: lecturer.position !== undefined ? Number(lecturer.position) : 0,
          major_positions: lecturer.major_positions || {},
          is_featured: lecturer.is_featured || false,
          show_detail_btn: !!lecturer.show_detail_btn
        })
      });
      if (created) {
        const mIds = created.major_ids ? created.major_ids.split(',').map(s => s.trim()).filter(Boolean) : (created.major_id ? [created.major_id] : []);
        this.lecturers.unshift({
          ...created,
          majorIds: mIds,
          majorId: mIds[0] || created.major_id,
          majorName: created.major_name,
          avatar: created.avatar,
          avatarDriveLink: created.avatar_drive_link || '',
          show_detail_btn: !!created.show_detail_btn
        });
      }
      this.fetchLecturers(true).catch(() => {});
      return created;
    } catch (err) {
      console.error("Failed to add lecturer:", err);
      throw err;
    }
  },

  async updateAdminLecturer(id, lecturer) {
    if (!this.token) return;
    try {
      const majorIdsStr = Array.isArray(lecturer.majorIds) ? lecturer.majorIds.join(',') : (lecturer.majorIds || lecturer.majorId || '');
      const primaryMajorId = Array.isArray(lecturer.majorIds) && lecturer.majorIds.length > 0 ? lecturer.majorIds[0] : (lecturer.majorId || null);
      const updated = await this.apiRequest(`/admin/lecturers/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
          name: lecturer.name,
          title: lecturer.title,
          tagline: lecturer.tagline,
          avatar: lecturer.avatar,
          avatar_drive_link: lecturer.avatarDriveLink || '',
          drive_profile: lecturer.driveProfile,
          bio_short: lecturer.bioShort,
          details_html: lecturer.detailsHtml,
          major_id: primaryMajorId,
          major_ids: majorIdsStr,
          major_name: lecturer.majorName || null,
          position: lecturer.position !== undefined ? Number(lecturer.position) : undefined,
          major_positions: lecturer.major_positions !== undefined ? lecturer.major_positions : undefined,
          is_featured: lecturer.is_featured,
          show_detail_btn: lecturer.show_detail_btn !== undefined ? !!lecturer.show_detail_btn : undefined
        })
      });

      if (updated) {
        const index = this.lecturers.findIndex(l => l.id === id);
        if (index !== -1) {
          const mIds = updated.major_ids ? updated.major_ids.split(',').map(s => s.trim()).filter(Boolean) : (updated.major_id ? [updated.major_id] : []);
          this.lecturers[index] = {
            ...this.lecturers[index],
            ...updated,
            majorIds: mIds,
            majorId: mIds[0] || updated.major_id,
            majorName: updated.major_name,
            avatar: updated.avatar,
            avatarDriveLink: updated.avatar_drive_link || '',
            show_detail_btn: !!updated.show_detail_btn
          };
        }
      }

      this.fetchLecturers(true).catch(() => {});
      return updated;
    } catch (err) {
      console.error("Failed to update lecturer:", err);
      throw err;
    }
  },

  async reorderLecturers(reorderedList, majorId = 'all') {
    if (!this.token) return;
    try {
      const payload = reorderedList.map((item, idx) => ({
        id: item.id,
        position: idx + 1
      }));
      const queryParam = majorId && majorId !== 'all' ? `?major_id=${encodeURIComponent(majorId)}` : '';
      await this.apiRequest(`/admin/lecturers/reorder${queryParam}`, {
        method: 'PUT',
        body: JSON.stringify(payload)
      });
      
      if (majorId && majorId !== 'all') {
        this.lecturers = this.lecturers.map(l => {
          const reorderedIdx = reorderedList.findIndex(item => item.id === l.id);
          if (reorderedIdx !== -1) {
            const majorPositions = { ...(l.major_positions || {}) };
            majorPositions[majorId] = reorderedIdx + 1;
            return { ...l, major_positions: majorPositions };
          }
          return l;
        });
      } else {
        const positionMap = new Map();
        reorderedList.forEach((item, idx) => {
          positionMap.set(item.id, idx + 1);
        });
        this.lecturers = this.lecturers.map(l => {
          if (positionMap.has(l.id)) {
            return { ...l, position: positionMap.get(l.id) };
          }
          return l;
        }).sort((a, b) => (a.position ?? 999) - (b.position ?? 999));
      }
    } catch (err) {
      console.error("Failed to reorder lecturers:", err);
      throw err;
    }
  },

  async toggleLecturerFeatured(id) {
    if (!this.token) return;
    try {
      const updated = await this.apiRequest(`/admin/lecturers/${id}/toggle-featured`, {
        method: 'PUT'
      });
      const index = this.lecturers.findIndex(l => l.id === id);
      if (index !== -1) {
        this.lecturers[index].is_featured = updated.is_featured;
      }
      return updated;
    } catch (err) {
      console.error("Failed to toggle lecturer featured:", err);
      throw err;
    }
  },

  async deleteAdminLecturer(id) {
    if (!this.token) return;
    try {
      await this.apiRequest(`/admin/lecturers/${id}`, {
        method: 'DELETE'
      });
      this.lecturers = this.lecturers.filter(l => l.id !== id);
      this.fetchLecturers().catch(() => {});
    } catch (err) {
      console.error("Failed to delete lecturer:", err);
      throw err;
    }
  }
};

