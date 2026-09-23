<template>
  <div class="project-detail-page" v-if="project">
    <div class="container">
      <!-- Breadcrumb -->
      <div class="breadcrumb">
        <router-link to="/">Trang chủ</router-link>
        <span class="sep">&rsaquo;</span>
        <router-link to="/du-an">Dự án Đào tạo & Tư vấn</router-link>
        <span class="sep">&rsaquo;</span>
        <span class="current">{{ project.title }}</span>
      </div>

      <!-- Article Header -->
      <div class="article-header">
        <div class="header-badges">
          <span class="category-badge" :class="project.category">
            {{ project.categoryName }}
          </span>
          <span class="publish-date">📅 Đăng ngày {{ project.date }}</span>
          <span v-if="project.client" class="client-tag">🏢 {{ project.client }}</span>
        </div>
        <h1 class="article-title">{{ project.title }}</h1>
        <p class="article-lead">{{ project.summary }}</p>
      </div>

      <!-- Cover Image -->
      <div class="cover-wrapper" v-if="project.image">
        <img :src="project.image" :alt="project.title" class="cover-image" referrerpolicy="no-referrer" />
      </div>

      <!-- Article Content -->
      <div class="article-body">
        <div 
          v-for="(block, idx) in project.content" 
          :key="idx"
          class="content-block"
        >
          <h2 v-if="block.type === 'heading'" class="block-heading">{{ block.text }}</h2>
          <p v-else-if="block.type === 'paragraph'" class="block-paragraph">{{ block.text }}</p>
          <ul v-else-if="block.type === 'bullets'" class="block-bullets">
            <li v-for="(item, bIdx) in block.items" :key="bIdx">{{ item }}</li>
          </ul>
        </div>

        <!-- Drive Profile Link Button -->
        <div v-if="project.driveProfile" class="drive-banner-box">
          <div class="drive-info">
            <h4 class="drive-title">Tài liệu & Hồ sơ Dự án (Google Drive)</h4>
            <p class="drive-desc">Bấm vào nút dưới đây để mở tài liệu chi tiết hoặc bài giới thiệu đầy đủ của dự án trên Google Drive.</p>
          </div>
          <a :href="project.driveProfile" target="_blank" rel="noopener noreferrer" class="btn-drive-full">
            <span>XEM TRÊN GOOGLE DRIVE</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
              <polyline points="15 3 21 3 21 9"></polyline>
              <line x1="10" y1="14" x2="21" y2="3"></line>
            </svg>
          </a>
        </div>
      </div>

      <!-- Related Projects -->
      <div class="related-section" v-if="relatedProjects.length > 0">
        <h3 class="related-title">Bài viết & Dự án Khác</h3>
        <div class="related-grid">
          <div v-for="rel in relatedProjects" :key="rel.id" class="related-card">
            <span class="rel-category">{{ rel.categoryName }}</span>
            <h4 class="rel-title">
              <router-link :to="'/du-an/' + rel.id">{{ rel.title }}</router-link>
            </h4>
            <p class="rel-date">{{ rel.date }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="not-found-container" v-else>
    <div class="container text-center">
      <h2>Không tìm thấy bài viết dự án</h2>
      <p>Bài viết dự án bạn đang tìm kiếm không tồn tại hoặc đã thay đổi đường dẫn.</p>
      <router-link to="/du-an" class="btn-back">Quay lại danh sách dự án</router-link>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { projectsData } from '@/data/projects';

const route = useRoute();

const project = computed(() => {
  return projectsData.find(p => p.id === route.params.id);
});

const relatedProjects = computed(() => {
  if (!project.value) return [];
  return projectsData
    .filter(p => p.id !== project.value.id)
    .slice(0, 3);
});

const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

onMounted(scrollToTop);
watch(() => route.params.id, scrollToTop);
</script>

<style scoped>
.project-detail-page {
  padding-top: 120px;
  padding-bottom: 100px;
  background-color: #ffffff;
  min-height: 100vh;
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13.5px;
  color: #64748b;
  margin-bottom: 32px;
  flex-wrap: wrap;
}

.breadcrumb a {
  color: #022b9f;
  text-decoration: none;
  font-weight: 600;
}

.breadcrumb .sep {
  color: #94a3b8;
}

.breadcrumb .current {
  color: #1e293b;
  font-weight: 600;
}

.article-header {
  max-width: 860px;
  margin-bottom: 36px;
}

.header-badges {
  display: flex;
  align-items: center;
  gap: 14px;
  flex-wrap: wrap;
  margin-bottom: 16px;
}

.category-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 800;
  color: #ffffff;
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

.publish-date, .client-tag {
  font-size: 13px;
  font-weight: 600;
  color: #64748b;
}

.article-title {
  font-size: clamp(28px, 4vw, 42px);
  font-weight: 800;
  color: #0f172a;
  line-height: 1.25;
  margin: 0 0 16px 0;
}

.article-lead {
  font-size: 18px;
  line-height: 1.6;
  color: #475569;
  font-weight: 500;
  margin: 0;
}

.cover-wrapper {
  max-width: 960px;
  height: 440px;
  border-radius: 20px;
  overflow: hidden;
  margin-bottom: 48px;
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.08);
}

.cover-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.article-body {
  max-width: 860px;
  margin-bottom: 60px;
}

.content-block {
  margin-bottom: 24px;
}

.block-heading {
  font-size: 24px;
  font-weight: 800;
  color: #0f172a;
  margin: 36px 0 16px 0;
  padding-bottom: 8px;
  border-bottom: 2px solid #f1f5f9;
}

.block-paragraph {
  font-size: 16px;
  line-height: 1.8;
  color: #334155;
  margin: 0;
}

.block-bullets {
  padding-left: 24px;
  margin: 0;
}

.block-bullets li {
  font-size: 16px;
  line-height: 1.8;
  color: #334155;
  margin-bottom: 8px;
}

.drive-banner-box {
  margin-top: 48px;
  padding: 28px;
  background: linear-gradient(135deg, #f0f4ff 0%, #e0e7ff 100%);
  border: 1.5px solid #c7d2fe;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  flex-wrap: wrap;
}

.drive-title {
  font-size: 18px;
  font-weight: 800;
  color: #1e1b4b;
  margin: 0 0 6px 0;
}

.drive-desc {
  font-size: 14px;
  color: #3730a3;
  margin: 0;
}

.btn-drive-full {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 12px 24px;
  background: #022b9f;
  color: #ffffff;
  font-weight: 700;
  font-size: 13.5px;
  border-radius: 10px;
  text-decoration: none;
  transition: background 0.2s ease;
  white-space: nowrap;
}

.btn-drive-full:hover {
  background: #1e40af;
}

.related-section {
  max-width: 960px;
  padding-top: 40px;
  border-top: 1px solid #e2e8f0;
}

.related-title {
  font-size: 22px;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 24px;
}

.related-grid {
  display: grid;
  grid-template-columns: repeat(1, 1fr);
  gap: 20px;
}

@media (min-width: 768px) {
  .related-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.related-card {
  background: #f8fafc;
  padding: 20px;
  border-radius: 14px;
  border: 1px solid #e2e8f0;
}

.rel-category {
  font-size: 11px;
  font-weight: 800;
  color: #022b9f;
  text-transform: uppercase;
}

.rel-title {
  font-size: 15px;
  font-weight: 700;
  margin: 8px 0;
  line-height: 1.4;
}

.rel-title a {
  color: #0f172a;
  text-decoration: none;
}

.rel-title a:hover {
  color: #022b9f;
}

.rel-date {
  font-size: 12px;
  color: #64748b;
  margin: 0;
}

.not-found-container {
  padding-top: 160px;
  padding-bottom: 120px;
}

.btn-back {
  display: inline-block;
  margin-top: 20px;
  padding: 12px 24px;
  background: #022b9f;
  color: #ffffff;
  border-radius: 10px;
  text-decoration: none;
  font-weight: 700;
}
</style>
