<template>
  <div class="blog-detail-wrapper">
    <!-- Top Running Progress Bar (Thanh chạy hiệu ứng tải bài viết) -->
    <div v-if="isLoading || isFetchingContent" class="blog-top-progress-bar">
      <div class="progress-bar-line"></div>
    </div>

    <!-- 1. SKELETON LOADING STATE (Thay thế spinner màn hình trắng) -->
    <div class="blog-detail-page skeleton-loading-page" v-if="isLoading && !post">
      <div class="container">
        <!-- Skeleton Breadcrumb -->
        <div class="skeleton-block" style="width: 240px; height: 16px; border-radius: 4px; margin-bottom: 24px;"></div>

        <div class="article-layout-grid">
          <div class="article-main-column">
            <!-- Skeleton Header -->
            <div class="article-header">
              <div class="header-badges" style="display: flex; gap: 12px; margin-bottom: 16px;">
                <div class="skeleton-block" style="width: 90px; height: 26px; border-radius: 20px;"></div>
                <div class="skeleton-block" style="width: 140px; height: 18px; border-radius: 4px;"></div>
              </div>
              <div class="skeleton-block" style="width: 95%; height: 38px; border-radius: 8px; margin-bottom: 12px;"></div>
              <div class="skeleton-block" style="width: 75%; height: 38px; border-radius: 8px; margin-bottom: 16px;"></div>
              <div class="skeleton-block" style="width: 85%; height: 20px; border-radius: 4px;"></div>
            </div>

            <!-- Skeleton Cover Image -->
            <div class="skeleton-block cover-skeleton" style="width: 100%; height: 380px; border-radius: 16px; margin-bottom: 32px;"></div>

            <!-- Skeleton Article Body lines -->
            <div class="skeleton-body-lines">
              <div class="skeleton-block" style="width: 100%; height: 16px; margin-bottom: 12px; border-radius: 4px;"></div>
              <div class="skeleton-block" style="width: 96%; height: 16px; margin-bottom: 12px; border-radius: 4px;"></div>
              <div class="skeleton-block" style="width: 92%; height: 16px; margin-bottom: 12px; border-radius: 4px;"></div>
              <div class="skeleton-block" style="width: 80%; height: 16px; margin-bottom: 24px; border-radius: 4px;"></div>

              <div class="skeleton-block" style="width: 45%; height: 26px; margin-bottom: 16px; border-radius: 6px;"></div>
              <div class="skeleton-block" style="width: 100%; height: 16px; margin-bottom: 12px; border-radius: 4px;"></div>
              <div class="skeleton-block" style="width: 95%; height: 16px; margin-bottom: 12px; border-radius: 4px;"></div>
              <div class="skeleton-block" style="width: 88%; height: 16px; margin-bottom: 12px; border-radius: 4px;"></div>
            </div>
          </div>

          <!-- Skeleton Sidebar -->
          <aside class="article-sidebar">
            <div class="sidebar-sticky-box">
              <div class="skeleton-block" style="width: 60%; height: 22px; border-radius: 6px; margin-bottom: 16px;"></div>
              <div v-for="n in 3" :key="n" style="display: flex; gap: 12px; margin-bottom: 14px;">
                <div class="skeleton-block" style="width: 80px; height: 60px; border-radius: 8px; flex-shrink: 0;"></div>
                <div style="flex: 1;">
                  <div class="skeleton-block" style="width: 50%; height: 12px; border-radius: 4px; margin-bottom: 6px;"></div>
                  <div class="skeleton-block" style="width: 90%; height: 14px; border-radius: 4px; margin-bottom: 6px;"></div>
                  <div class="skeleton-block" style="width: 40%; height: 12px; border-radius: 4px;"></div>
                </div>
              </div>
            </div>
          </aside>
        </div>
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
              <div v-else-if="isFetchingContent" class="content-loading-shimmer">
                <div class="skeleton-block" style="width: 100%; height: 16px; margin-bottom: 12px; border-radius: 4px;"></div>
                <div class="skeleton-block" style="width: 96%; height: 16px; margin-bottom: 12px; border-radius: 4px;"></div>
                <div class="skeleton-block" style="width: 92%; height: 16px; margin-bottom: 12px; border-radius: 4px;"></div>
                <div class="skeleton-block" style="width: 80%; height: 16px; margin-bottom: 24px; border-radius: 4px;"></div>
                <div class="skeleton-block" style="width: 45%; height: 26px; margin-bottom: 14px; border-radius: 6px;"></div>
                <div class="skeleton-block" style="width: 98%; height: 16px; margin-bottom: 12px; border-radius: 4px;"></div>
                <div class="skeleton-block" style="width: 94%; height: 16px; margin-bottom: 12px; border-radius: 4px;"></div>
                <div class="skeleton-block" style="width: 88%; height: 16px; margin-bottom: 12px; border-radius: 4px;"></div>
              </div>
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
const isFetchingContent = ref(true);

const fetchPostDetail = async () => {
  const handleOrId = String(route.params.handle || '').toLowerCase().trim();
  if (!handleOrId) {
    isLoading.value = false;
    isFetchingContent.value = false;
    return;
  }

  isFetchingContent.value = true;

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
    // Đã có sẵn metadata trong store -> hiển thị khung ngay lập tức, không để màn hình trắng
    isLoading.value = false;
  } else {
    isLoading.value = true;
  }

  // Also fetch directly from backend API for fresh and full content
  try {
    const data = await courseStore.apiRequest(`/blogs/${handleOrId}`);
    if (data) {
      currentPost.value = data;
    }
  } catch (err) {
    console.warn("Could not fetch blog detail from API:", err);
  } finally {
    isLoading.value = false;
    isFetchingContent.value = false;
  }
};

onMounted(() => {
  isLoading.value = !currentPost.value;
  isFetchingContent.value = true;
  // Run detail + list (for sidebar related posts) in parallel instead of sequentially
  courseStore.fetchBlogs().catch(() => {});
  fetchPostDetail();
});

watch(() => route.params.handle, async () => {
  isLoading.value = true;
  isFetchingContent.value = true;
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

<style scoped src="@/styles/views/library/BlogDetail.css"></style>
