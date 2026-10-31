import { compressImageBeforeUpload } from '@/utils/imageHelper';
import { API_BASE } from './helpers';

export const uiActions = {
  // Standard request wrapper with JWT token injection
  async apiRequest(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    try {
      const response = await fetch(url, { ...options, headers });
      if (!response.ok) {
        if (response.status === 401) {
          if (endpoint === '/auth/me') {
            this.token = null;
            this.user = null;
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            if (typeof window !== 'undefined' && !window.location.pathname.startsWith('/login')) {
              window.location.href = '/login';
            }
          }
        }
        const errData = await response.json().catch(() => ({}));
        let message = `HTTP error! status: ${response.status}`;
        if (typeof errData.detail === 'string') {
          message = errData.detail;
        } else if (Array.isArray(errData.detail)) {
          message = errData.detail.map(e => `${e.loc ? e.loc.join('.') + ': ' : ''}${e.msg}`).join('; ');
        } else if (errData.message) {
          message = errData.message;
        }
        throw new Error(message);
      }
      return await response.json();
    } catch (err) {
      console.error(`API Request Error on ${endpoint}:`, err);
      throw err;
    }
  },

  showToast(message, type = 'info', duration = 3500) {
    this.toast.message = message;
    this.toast.type = type;
    this.toast.show = true;
    setTimeout(() => {
      this.toast.show = false;
    }, duration);
  },

  hideToast() {
    this.toast.show = false;
  },

  showConfirm({ title = 'Xác nhận hành động', message, confirmText = 'Đồng ý', cancelText = 'Hủy', type = 'danger' }) {
    return new Promise((resolve) => {
      this.confirmModal = {
        show: true,
        title,
        message,
        confirmText,
        cancelText,
        type,
        resolve
      };
    });
  },

  handleConfirmResult(result) {
    if (this.confirmModal.resolve) {
      this.confirmModal.resolve(result);
    }
    this.confirmModal.show = false;
    this.confirmModal.resolve = null;
  },

  async uploadImage(file) {
    let fileToSend = file;
    try {
      fileToSend = await compressImageBeforeUpload(file);
    } catch (e) {
      console.warn('Client-side image compression fallback:', e);
    }

    const formData = new FormData();
    formData.append('file', fileToSend);
    
    const headers = {};
    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }
    
    const res = await fetch(`${API_BASE}/upload/image`, {
      method: 'POST',
      headers,
      body: formData
    });
    
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Lỗi khi tải ảnh lên Cloudinary');
    }
    
    const data = await res.json();
    return data.url;
  },

  async deleteImage(urlOrPublicId) {
    if (!urlOrPublicId || typeof urlOrPublicId !== 'string') return;
    const cleanTarget = urlOrPublicId.trim();
    if (!cleanTarget.includes('cloudinary.com') && !cleanTarget.startsWith('Acc Demo/')) {
      return;
    }
    try {
      const headers = { 'Content-Type': 'application/json' };
      if (this.token) {
        headers['Authorization'] = `Bearer ${this.token}`;
      }
      fetch(`${API_BASE}/upload/delete-image`, {
        method: 'POST',
        headers,
        body: JSON.stringify({ url: cleanTarget })
      }).catch(err => console.warn('Delete image background warning:', err));
    } catch (err) {
      console.warn('Delete image warning:', err);
    }
  },

  async deleteImages(urls) {
    if (!urls || !Array.isArray(urls) || urls.length === 0) return;
    const cleanTargets = urls
      .filter(u => typeof u === 'string' && (u.includes('cloudinary.com') || u.startsWith('Acc Demo/')))
      .map(u => u.trim());
    if (cleanTargets.length === 0) return;
    try {
      const headers = { 'Content-Type': 'application/json' };
      if (this.token) {
        headers['Authorization'] = `Bearer ${this.token}`;
      }
      fetch(`${API_BASE}/upload/delete-image`, {
        method: 'POST',
        headers,
        body: JSON.stringify({ urls: cleanTargets })
      }).catch(err => console.warn('Batch delete image background warning:', err));
    } catch (err) {
      console.warn('Batch delete image warning:', err);
    }
  }
};

