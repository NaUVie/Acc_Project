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

let fetchTestimonialsPromise = null;

export const useTestimonialStore = defineStore('testimonials', {
  state: () => ({
    testimonials: [],
    loading: false
  }),

  getters: {
    videoTestimonials(state) {
      return state.testimonials.filter(t => t.testimonialType === 'video');
    },
    photoTestimonials(state) {
      return state.testimonials.filter(t => t.testimonialType === 'photo' || t.testimonialType === 'text');
    }
  },

  actions: {
    async fetchTestimonials(force = false) {
      if (!force && this.testimonials && this.testimonials.length > 0) {
        return this.testimonials;
      }
      if (fetchTestimonialsPromise) {
        return fetchTestimonialsPromise;
      }

      this.loading = true;
      fetchTestimonialsPromise = (async () => {
        try {
          const response = await fetch(`${API_BASE}/testimonials`);
          if (response.ok) {
            const data = await response.json();
            if (Array.isArray(data)) {
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
                courseId: item.course_id || null,
                isApproved: item.is_approved !== false,
                testimonialType: item.testimonial_type || 'text',
                youtubeId: item.youtube_id || '',
                thumbnail: item.thumbnail || (item.youtube_id ? `https://img.youtube.com/vi/${item.youtube_id}/hqdefault.jpg` : ''),
                videoUrl: item.video_url || (item.youtube_id ? `https://www.youtube.com/embed/${item.youtube_id}?autoplay=1` : ''),
                title: item.text || item.quote || `Chia sẻ từ học viên ${item.name}`
              }));
            }
          }
          return this.testimonials;
        } catch (err) {
          console.warn("Backend server connection failed for testimonials:", err);
          return this.testimonials;
        } finally {
          this.loading = false;
          fetchTestimonialsPromise = null;
        }
      })();
      return fetchTestimonialsPromise;
    },

    async submitPublicTestimonial(testimonial) {
      try {
        const payload = {
          name: testimonial.name,
          role: testimonial.role || '',
          company: testimonial.company || '',
          text: testimonial.text,
          quote: testimonial.text,
          rating: Number(testimonial.rating) || 5,
          course_id: testimonial.courseId ? Number(testimonial.courseId) : null,
          course_name: testimonial.courseName || '',
          testimonial_type: 'text'
        };
        const response = await fetch(`${API_BASE}/testimonials`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        if (!response.ok) {
          const errData = await response.json().catch(() => ({}));
          throw new Error(errData.detail || 'Không thể gửi nhận xét');
        }
        return await response.json();
      } catch (err) {
        console.error("submitPublicTestimonial error:", err);
        throw err;
      }
    },

    async fetchCourseTestimonials(courseId) {
      if (!courseId) return [];
      try {
        const response = await fetch(`${API_BASE}/testimonials?course_id=${courseId}`);
        if (response.ok) {
          const data = await response.json();
          return Array.isArray(data) ? data.map(item => ({
            id: item.id,
            name: item.name,
            role: item.role || '',
            company: item.company || '',
            text: item.text || item.quote || '',
            quote: item.quote || item.text || '',
            rating: item.rating || 5,
            image: item.image || item.thumbnail || '',
            avatar: item.thumbnail || item.image || '',
            courseName: item.course_name || '',
            courseId: item.course_id || null,
            createdAt: item.created_at || null
          })) : [];
        }
        return [];
      } catch (err) {
        console.error("fetchCourseTestimonials error:", err);
        return [];
      }
    }
  }
});
