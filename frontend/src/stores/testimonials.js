import { defineStore } from 'pinia';

const getApiBase = () => {
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL;
  }
  if (typeof window !== 'undefined') {
    const isDev = import.meta.env.DEV;
    if (isDev) {
      return `${window.location.protocol}//${window.location.hostname}:8000/api`;
    }
    return `${window.location.origin}/api`;
  }
  return '/api';
};

const API_BASE = getApiBase();

import { videoTestimonialsData, photoTestimonialsData } from '@/data/testimonials';

export const useTestimonialStore = defineStore('testimonials', {
  state: () => ({
    testimonials: [],
    loading: false
  }),

  getters: {
    videoTestimonials(state) {
      const list = state.testimonials.filter(t => t.testimonialType === 'video');
      if (list.length > 0) return list;
      return videoTestimonialsData;
    },
    photoTestimonials(state) {
      const list = state.testimonials.filter(t => t.testimonialType === 'photo' || t.testimonialType === 'text');
      if (list.length > 0) return list;
      return photoTestimonialsData;
    }
  },

  actions: {
    async fetchTestimonials() {
      this.loading = true;
      try {
        const response = await fetch(`${API_BASE}/testimonials`);
        if (response.ok) {
          const data = await response.json();
          if (data && data.length > 0) {
            this.testimonials = data.map(item => ({
              id: item.id,
              name: item.name,
              studentName: item.name,
              role: item.role || '',
              company: item.company || '',
              text: item.text || '',
              quote: item.quote || item.text || '',
              rating: item.rating || 5,
              image: item.image || '',
              avatar: item.thumbnail || item.image || 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=200&q=80',
              courseName: item.course_name || '',
              testimonialType: item.testimonial_type || 'text',
              youtubeId: item.youtube_id || '',
              thumbnail: item.thumbnail || (item.youtube_id ? `https://img.youtube.com/vi/${item.youtube_id}/hqdefault.jpg` : ''),
              videoUrl: item.video_url || (item.youtube_id ? `https://www.youtube.com/embed/${item.youtube_id}?autoplay=1` : ''),
              title: item.text || item.quote || `Chia sẻ từ học viên ${item.name}`
            }));
          }
        }
      } catch (err) {
        console.warn("Backend server connection failed for testimonials, using initial fallback data:", err);
      } finally {
        this.loading = false;
      }
    }
  }
});
