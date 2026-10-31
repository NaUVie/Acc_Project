// Dynamic API URL builder to avoid hardcoded URLs
export const getApiBase = () => {
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

export const API_BASE = getApiBase();

// Helper to clean course properties mapping from API to Frontend camelCase format
export const mapCourse = (c) => {
  if (!c) return null;
  return {
    id: c.id,
    title: c.title,
    category: c.category_slug,
    programId: c.program_id,
    handle: c.handle,
    price: c.price,
    originalPrice: c.original_price,
    image: c.image,
    coverImage: c.cover_image,
    tags: c.tags ? c.tags.map(t => t.tag) : [],
    description: c.description,
    duration: c.duration,
    level: c.level,
    curriculumData: c.curriculum_data,
    outcomes: c.outcomes,
    requirements: c.requirements,
    customRoadmap: c.custom_roadmap,
    lecturerIds: c.lecturer_ids
  };
};

