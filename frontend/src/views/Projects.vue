<template>
  <div class="projects-page">
    <div class="container">
      <!-- Hero Section -->
      <div class="projects-hero">
        <h1 class="hero-title">Dự án Đã Thực Hiện & Đang Triển Khai</h1>
        <p class="hero-subtitle">
          Khám phá các dự án đào tạo In-house thực chiến và tư vấn chuyển đổi số may đo cho các tập đoàn, doanh nghiệp hàng đầu do ACC Academy thực hiện.
        </p>
      </div>

      <!-- Filter Tabs / Navbar -->
      <div class="filter-tabs">
        <button 
          class="tab-btn" 
          :class="{ active: currentCategory === 'all' }"
          @click="selectCategory('all')"
        >
          Tất cả dự án
        </button>
        <button 
          class="tab-btn" 
          :class="{ active: currentCategory === 'du-an-doanh-nghiep' }"
          @click="selectCategory('du-an-doanh-nghiep')"
        >
          🏢 Dự án Doanh nghiệp
        </button>
        <button 
          class="tab-btn" 
          :class="{ active: currentCategory === 'du-an-ca-nhan' }"
          @click="selectCategory('du-an-ca-nhan')"
        >
          👤 Dự án Cá nhân
        </button>
        <button 
          class="tab-btn" 
          :class="{ active: currentCategory === 'du-an-nha-nuoc' }"
          @click="selectCategory('du-an-nha-nuoc')"
        >
          🏛️ Dự án Nhà nước
        </button>
      </div>

      <!-- Projects Grid -->
      <div class="projects-grid">
        <div 
          v-for="item in filteredProjects" 
          :key="item.id"
          class="project-card"
        >
          <div class="card-image-wrapper">
            <img :src="item.image" :alt="item.title" class="card-image" referrerpolicy="no-referrer" />
            <span class="category-badge" :class="item.category">
              {{ item.categoryName }}
            </span>
          </div>

          <div class="card-body">
            <div class="card-meta">
              <span class="meta-date">📅 {{ item.date }}</span>
              <span v-if="item.client" class="meta-client">🏛️ {{ item.client }}</span>
            </div>
            <h3 class="card-title">
              <router-link :to="'/du-an/' + item.id" class="title-link">
                {{ item.title }}
              </router-link>
            </h3>
            <p class="card-summary">{{ item.summary }}</p>

            <div class="card-footer">
              <router-link :to="'/du-an/' + item.id" class="btn-read-more">
                <span>Xem chi tiết dự án</span>
                <span class="arrow">&rarr;</span>
              </router-link>
              
              <a v-if="item.driveProfile" :href="item.driveProfile" target="_blank" rel="noopener noreferrer" class="btn-drive-link">
                <span>DRIVE PROFILE</span>
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                  <polyline points="15 3 21 3 21 9"></polyline>
                  <line x1="10" y1="14" x2="21" y2="3"></line>
                </svg>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useCourseStore } from '@/stores/courses';

const route = useRoute();
const router = useRouter();
const courseStore = useCourseStore();

const currentCategory = ref('all');

const syncCategoryFromQuery = () => {
  const cat = route.query.cat;
  if (cat && ['du-an-doanh-nghiep', 'du-an-ca-nhan', 'du-an-nha-nuoc'].includes(cat)) {
    currentCategory.value = cat;
  } else {
    currentCategory.value = 'all';
  }
};

onMounted(() => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
  syncCategoryFromQuery();
  if (!courseStore.projects || courseStore.projects.length === 0) {
    courseStore.fetchProjects();
  }
});

watch(() => route.query.cat, () => {
  syncCategoryFromQuery();
});

const selectCategory = (cat) => {
  currentCategory.value = cat;
  if (cat === 'all') {
    router.push({ path: '/du-an' });
  } else {
    router.push({ path: '/du-an', query: { cat } });
  }
};

const allProjects = computed(() => courseStore.projects || []);

const filteredProjects = computed(() => {
  if (currentCategory.value === 'all') {
    return allProjects.value;
  }
  return allProjects.value.filter(item => item.category === currentCategory.value);
});
</script>

<style scoped>
.projects-page {
  padding-top: 120px;
  padding-bottom: 100px;
  background-color: #f8fafc;
  min-height: 100vh;
}

.projects-hero {
  text-align: center;
  max-width: 860px;
  margin-inline: auto;
  margin-bottom: 48px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.hero-tag {
  background: rgba(2, 43, 159, 0.08);
  color: #022b9f;
  font-weight: 800;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 13px;
}

.hero-title {
  font-size: clamp(32px, 4vw, 48px);
  font-weight: 800;
  color: #0f172a;
  margin: 0;
  line-height: 1.2;
}

.hero-subtitle {
  font-size: 16px;
  color: #475569;
  line-height: 1.6;
  margin: 0;
}

.filter-tabs {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-bottom: 48px;
  flex-wrap: wrap;
}

.tab-btn {
  padding: 10px 24px;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 24px;
  color: #475569;
  font-weight: 700;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.25s ease;
}

.tab-btn:hover {
  border-color: #022b9f;
  color: #022b9f;
  background: #f0f4ff;
}

.tab-btn.active {
  background: #022b9f;
  color: #ffffff;
  border-color: #022b9f;
  box-shadow: 0 4px 14px rgba(2, 43, 159, 0.25);
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(1, 1fr);
  gap: 32px;
}

@media (min-width: 768px) {
  .projects-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1200px) {
  .projects-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.project-card {
  background: #ffffff;
  border-radius: 18px;
  border: 1px solid #e2e8f0;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
}

.project-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
  border-color: #022b9f;
}

.card-image-wrapper {
  position: relative;
  width: 100%;
  height: 220px;
  overflow: hidden;
  background-color: #e2e8f0;
}

.card-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.project-card:hover .card-image {
  transform: scale(1.06);
}

.category-badge {
  position: absolute;
  top: 14px;
  left: 14px;
  padding: 5px 12px;
  border-radius: 12px;
  font-size: 11.5px;
  font-weight: 800;
  color: #ffffff;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.category-badge.du-an-doanh-nghiep {
  background: #022b9f;
}

.category-badge.du-an-ca-nhan {
  background: #0284c7;
}

.category-badge.du-an-nha-nuoc {
  background: #059669;
}

.card-body {
  padding: 24px;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.card-meta {
  display: flex;
  align-items: center;
  gap: 16px;
  font-size: 12.5px;
  font-weight: 600;
  color: #64748b;
  margin-bottom: 12px;
}

.card-title {
  font-size: 18px;
  font-weight: 800;
  color: #0f172a;
  margin: 0 0 10px 0;
  line-height: 1.4;
}

.title-link {
  color: inherit;
  text-decoration: none;
  transition: color 0.2s ease;
}

.title-link:hover {
  color: #022b9f;
}

.card-summary {
  font-size: 14px;
  color: #475569;
  line-height: 1.6;
  margin: 0 0 20px 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-footer {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.btn-read-more {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 18px;
  background: #022b9f;
  color: #ffffff;
  font-weight: 700;
  font-size: 13.5px;
  border-radius: 10px;
  text-decoration: none;
  transition: background 0.2s ease;
}

.btn-read-more:hover {
  background: #1e40af;
}

.btn-drive-link {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 18px;
  background: transparent;
  border: 1px solid #cbd5e1;
  color: #334155;
  font-weight: 700;
  font-size: 12.5px;
  border-radius: 10px;
  text-decoration: none;
  transition: all 0.2s ease;
}

.btn-drive-link:hover {
  background: #f1f5f9;
  color: #022b9f;
  border-color: #94a3b8;
}
</style>
