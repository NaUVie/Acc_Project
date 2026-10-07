<template>
  <div class="blog-detail-wrapper">
    <!-- 1. LOADING STATE -->
    <div class="loading-container" v-if="isLoading">
      <div class="container text-center">
        <div class="loading-spinner"></div>
        <p class="loading-text">Đang tải bài viết...</p>
      </div>
    </div>

    <!-- 2. ARTICLE DETAIL -->
    <div class="blog-detail-page" v-else-if="post">
      <div class="container">
        <!-- Breadcrumb -->
        <div class="breadcrumb">
          <router-link to="/">Trang chủ</router-link>
          <span class="sep">&rsaquo;</span>
          <router-link to="/library/blog">Tin tức & Bài viết</router-link>
          <span class="sep">&rsaquo;</span>
          <span class="current">{{ post.title }}</span>
        </div>

        <!-- Main Grid Layout (Article Content + Sidebar) -->
        <div class="article-layout-grid">
          <!-- Main Content Area (Left Side) -->
          <div class="article-main-column">
            <!-- Article Header -->
            <div class="article-header">
              <div class="header-badges">
                <span class="category-badge">
                  {{ post.category }}
                </span>
                <span class="publish-date">📅 Đăng ngày {{ post.date }}</span>
              </div>
              <h1 class="article-title">{{ post.title }}</h1>
              <p class="article-lead" v-if="post.excerpt">{{ post.excerpt }}</p>
            </div>

            <!-- Cover Image -->
            <div class="cover-wrapper" v-if="post.image">
              <img :src="post.image" :alt="post.title" class="cover-image" referrerpolicy="no-referrer" />
            </div>

            <!-- Article Body (Rich HTML text) -->
            <div class="article-body">
              <div v-if="post.content" class="content-html-wrapper" v-html="post.content"></div>
              <div v-else class="content-html-wrapper">
                <p>{{ post.excerpt }}</p>
              </div>
            </div>
          </div>

          <!-- Sidebar (Right Side: Related Posts & Quick Contact) -->
          <aside class="article-sidebar">
            <div class="sidebar-sticky-box">
              <div class="related-sidebar-card" v-if="relatedPosts.length > 0">
                <h3 class="sidebar-title">Bài viết liên quan</h3>
                <div class="sidebar-related-list">
                  <div v-for="rel in relatedPosts" :key="rel.id" class="sidebar-related-item">
                    <router-link :to="'/blog/' + rel.handle" class="sidebar-rel-link">
                      <div class="sidebar-rel-img" v-if="rel.image">
                        <img :src="rel.image" :alt="rel.title" />
                      </div>
                      <div class="sidebar-rel-info">
                        <span class="sidebar-rel-cat">{{ rel.category }}</span>
                        <h4 class="sidebar-rel-title">{{ rel.title }}</h4>
                        <span class="sidebar-rel-date">{{ rel.date }}</span>
                      </div>
                    </router-link>
                  </div>
                </div>
              </div>

              <!-- CTA Consultation Box in Sidebar -->
              <div class="sidebar-cta-card">
                <h4 class="sidebar-cta-title">Tư vấn đào tạo ACC</h4>
                <p class="sidebar-cta-desc">Nhận lộ trình tư vấn cá nhân hóa & doanh nghiệp cùng chuyên gia.</p>
                <router-link to="/contact" class="sidebar-cta-btn">Liên hệ tư vấn ngay</router-link>
              </div>
            </div>
          </aside>
        </div>
      </div>
    </div>

    <!-- 3. NOT FOUND STATE -->
    <div class="not-found-container" v-else>
      <div class="container text-center">
        <h2>Không tìm thấy bài viết</h2>
        <p>Bài viết bạn đang tìm kiếm không tồn tại hoặc đã thay đổi đường dẫn tĩnh.</p>
        <router-link to="/library/blog" class="btn-back">Quay lại danh sách tin tức</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useCourseStore } from '@/stores/courses';

const route = useRoute();
const courseStore = useCourseStore();

const currentPost = ref(null);
const isLoading = ref(true);

const fetchPostDetail = async () => {
  const handleOrId = String(route.params.handle || '').toLowerCase().trim();
  if (!handleOrId) {
    isLoading.value = false;
    return;
  }

  // Function to search in store
  const matchPost = (list) => {
    return list.find(p => {
      const pHandle = String(p.handle || '').toLowerCase().trim();
      const pId = String(p.id || '').toLowerCase().trim();
      const pLink = String(p.link || '').toLowerCase().trim();
      return pHandle === handleOrId || 
             pId === handleOrId || 
             pLink.endsWith(`/${handleOrId}`) || 
             pLink === `/blog/${handleOrId}`;
    });
  };

  let found = matchPost(courseStore.blogPosts);
  if (found) {
    currentPost.value = found;
  }

  // Also fetch directly from backend API for fresh content
  try {
    const data = await courseStore.apiRequest(`/blogs/${handleOrId}`);
    if (data) {
      currentPost.value = data;
    }
  } catch (err) {
    console.warn("Could not fetch blog detail from API:", err);
  } finally {
    isLoading.value = false;
  }
};

onMounted(async () => {
  isLoading.value = true;
  await courseStore.fetchBlogs().catch(() => {});
  await fetchPostDetail();
});

watch(() => route.params.handle, async () => {
  isLoading.value = true;
  await fetchPostDetail();
});

const post = computed(() => currentPost.value);

const relatedPosts = computed(() => {
  if (!post.value) return [];
  return courseStore.blogPosts
    .filter(p => p.id !== post.value.id)
    .slice(0, 3);
});
</script>

<style scoped>
.blog-detail-page {
  padding: 40px 0 80px;
  background: #f8fafc;
  min-height: 80vh;
}
.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #64748b;
  margin-bottom: 24px;
  flex-wrap: wrap;
}
.breadcrumb a {
  color: #022b9f;
  text-decoration: none;
  font-weight: 500;
}
.breadcrumb a:hover {
  text-decoration: underline;
}
.breadcrumb .sep {
  color: #94a3b8;
}
.breadcrumb .current {
  color: #1e293b;
  font-weight: 600;
  max-width: 300px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.article-layout-grid {
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 40px;
  align-items: start;
}

@media (max-width: 992px) {
  .article-layout-grid {
    grid-template-columns: 1fr;
    gap: 32px;
  }
}

.article-main-column {
  min-width: 0;
}

.article-header {
  margin-bottom: 32px;
  text-align: left;
}

.header-badges {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 12px;
  margin-bottom: 16px;
}

.category-badge {
  background: rgba(2, 43, 159, 0.08);
  color: #022b9f;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 700;
}

.publish-date {
  font-size: 13px;
  color: #64748b;
  font-weight: 500;
}

.article-title {
  font-size: 32px;
  font-weight: 800;
  color: #0f172a;
  line-height: 1.3;
  margin-bottom: 16px;
}

.article-lead {
  font-size: 17px;
  color: #475569;
  line-height: 1.6;
}

.cover-wrapper {
  width: 100%;
  margin-bottom: 32px;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.06);
}

.cover-image {
  width: 100%;
  max-height: 440px;
  object-fit: cover;
  display: block;
}

.article-body {
  background: #ffffff;
  padding: 36px;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
}

.content-html-wrapper {
  font-size: 16px;
  line-height: 1.8;
  color: #334155;
}

.content-html-wrapper :deep(h2) {
  font-size: 24px;
  font-weight: 800;
  color: #0f172a;
  margin-top: 32px;
  margin-bottom: 16px;
  border-left: 4px solid #022b9f;
  padding-left: 12px;
}

.content-html-wrapper :deep(h3) {
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
  margin-top: 24px;
  margin-bottom: 12px;
}

.content-html-wrapper :deep(p) {
  margin-bottom: 16px;
}

.content-html-wrapper :deep(ul),
.content-html-wrapper :deep(ol) {
  margin-bottom: 20px;
  padding-left: 24px;
}

.content-html-wrapper :deep(li) {
  margin-bottom: 8px;
}

.content-html-wrapper :deep(img) {
  max-width: 100%;
  border-radius: 12px;
  margin: 20px 0;
}

/* Sidebar Styles */
.article-sidebar {
  width: 100%;
}

.sidebar-sticky-box {
  position: sticky;
  top: 100px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.related-sidebar-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.03);
}

.sidebar-title {
  font-size: 18px;
  font-weight: 800;
  color: #0f172a;
  margin: 0 0 16px 0;
  padding-bottom: 12px;
  border-bottom: 2px solid #f1f5f9;
}

.sidebar-related-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.sidebar-related-item {
  border-bottom: 1px solid #f1f5f9;
  padding-bottom: 14px;
}

.sidebar-related-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.sidebar-rel-link {
  display: flex;
  gap: 12px;
  text-decoration: none;
}

.sidebar-rel-img {
  width: 72px;
  height: 64px;
  border-radius: 8px;
  overflow: hidden;
  flex-shrink: 0;
  background: #f1f5f9;
}

.sidebar-rel-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.sidebar-rel-link:hover .sidebar-rel-img img {
  transform: scale(1.08);
}

.sidebar-rel-info {
  display: flex;
  flex-direction: column;
  justify-content: center;
  flex-grow: 1;
}

.sidebar-rel-cat {
  font-size: 11px;
  font-weight: 700;
  color: #022b9f;
  text-transform: uppercase;
}

.sidebar-rel-title {
  font-size: 13.5px;
  font-weight: 700;
  color: #0f172a;
  margin: 2px 0 4px 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  transition: color 0.2s ease;
}

.sidebar-rel-link:hover .sidebar-rel-title {
  color: #022b9f;
}

.sidebar-rel-date {
  font-size: 11px;
  color: #94a3b8;
}

/* Sidebar CTA Consultation Card */
.sidebar-cta-card {
  background: linear-gradient(135deg, #022b9f 0%, #1e40af 100%);
  color: #ffffff;
  border-radius: 16px;
  padding: 24px;
  text-align: center;
  box-shadow: 0 10px 24px rgba(2, 43, 159, 0.2);
}

.sidebar-cta-title {
  font-size: 18px;
  font-weight: 800;
  margin: 0 0 8px 0;
  color: #ffffff;
}

.sidebar-cta-desc {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.85);
  line-height: 1.5;
  margin: 0 0 16px 0;
}

.sidebar-cta-btn {
  display: block;
  width: 100%;
  padding: 11px 16px;
  background: #ffffff;
  color: #022b9f;
  font-size: 13.5px;
  font-weight: 800;
  border-radius: 10px;
  text-decoration: none;
  box-sizing: border-box;
  transition: all 0.25s ease;
}

.sidebar-cta-btn:hover {
  background: #f8fafc;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
}

.not-found-container {
  padding: 100px 0;
}
.loading-container {
  padding: 120px 0;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}
.loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid rgba(2, 43, 159, 0.1);
  border-top-color: #022b9f;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 16px;
}
.loading-text {
  font-size: 16px;
  font-weight: 600;
  color: #475569;
}
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
.btn-back {
  display: inline-block;
  margin-top: 16px;
  padding: 10px 24px;
  background: #022b9f;
  color: #fff;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
}
</style>
