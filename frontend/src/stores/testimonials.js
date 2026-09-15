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

export const useTestimonialStore = defineStore('testimonials', {
  state: () => ({
    testimonials: [
      // Fallback/Initial state
      {
        id: 1,
        text: "Tôi đã học được rất nhiều, không chỉ về kỹ năng giải quyết vấn đề và ra quyết định, mà còn ở cách tư duy và áp dụng vào công việc thực tế.",
        name: "Lê Hồng Minh",
        role: "Founder & CEO, VNG Corporation",
        image: "https://images.unsplash.com/photo-1560250097-0b93528c311a?q=80&w=400&auto=format&fit=crop",
        videoUrl: "https://www.w3schools.com/html/mov_bbb.mp4"
      },
      {
        id: 2,
        text: "Khóa học được chuẩn bị một cách kỹ lưỡng, thể hiện qua các hoạt động tình huống sinh động và lôi cuốn, giúp tôi dễ dàng tiếp cận và ghi nhớ kiến thức.",
        name: "Nguyễn Thành Nam",
        role: "Cựu CEO FPT, Founder FUNiX",
        image: "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?q=80&w=400&auto=format&fit=crop",
        videoUrl: null
      }
    ],
    loading: false
  }),

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
              role: item.role,
              text: item.text,
              image: item.image,
              videoUrl: item.video_url
            }));
          }
        }
      } catch (err) {
        console.error("Failed to fetch testimonials from backend:", err);
      } finally {
        this.loading = false;
      }
    }
  }
});
