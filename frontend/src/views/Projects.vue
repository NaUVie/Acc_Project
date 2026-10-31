<template>
  <div class="projects-page">
    <div class="container">
      <!-- Hero Section -->
      <div class="projects-hero">
        <h1 class="hero-title">{{ $t('projects.pageTitle') }}</h1>
        <p class="hero-subtitle">{{ $t('projects.pageSubtitle') }}</p>
      </div>

      <!-- Filter Tabs / Navbar -->
      <div class="filter-tabs">
        <button 
          class="tab-btn" 
          :class="{ active: currentCategory === 'all' }"
          @click="selectCategory('all')"
        >
          {{ $t('projects.tabAll') }}
        </button>
        <button 
          class="tab-btn" 
          :class="{ active: currentCategory === 'du-an-doanh-nghiep' }"
          @click="selectCategory('du-an-doanh-nghiep')"
        >
           {{ $t('projects.tabCorporate') }}
        </button>
        <button 
          class="tab-btn" 
          :class="{ active: currentCategory === 'du-an-ca-nhan' }"
          @click="selectCategory('du-an-ca-nhan')"
        >
           {{ $t('projects.tabPersonal') }}
        </button>
        <button 
          class="tab-btn" 
          :class="{ active: currentCategory === 'du-an-nha-nuoc' }"
          @click="selectCategory('du-an-nha-nuoc')"
        >
           {{ $t('projects.tabGov') }}
        </button>
      </div>

      <!-- Projects Grid -->
      <div class="projects-grid" ref="projectsGridRef">
        <div 
          v-for="item in paginatedProjects" 
          :key="item.id"
          class="project-card"
        >
          <div class="card-image-wrapper">
            <img :src="item.image" :alt="item.title" class="card-image" loading="lazy" decoding="async" width="400" height="250" referrerpolicy="no-referrer" />
            <span class="category-badge" :class="item.category">
              {{ item.categoryName }}
            </span>
          </div>

          <div class="card-body">
            <div class="card-meta">
              <span class="meta-date">{{ item.date }}</span>
              <span v-if="item.client" class="meta-client">{{ item.client }}</span>
            </div>
            <h3 class="card-title">
              <router-link :to="'/projects/' + item.id" class="title-link">
                {{ item.title }}
              </router-link>
            </h3>
            <p class="card-summary">{{ item.summary }}</p>

            <div class="card-footer">
              <router-link :to="'/projects/' + item.id" class="btn-read-more">
                <span>{{ $t('projects.viewDetailBtn') }}</span>
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

      <!-- Pagination Component -->
      <Pagination 
        v-if="filteredProjects.length > pageSize"
        v-model:currentPage="currentPage"
        :totalItems="filteredProjects.length"
        :pageSize="pageSize"
        @page-change="onPageChange"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useCourseStore } from '@/stores/courses';
import Pagination from '@/components/Pagination.vue';

const route = useRoute();
const router = useRouter();
const courseStore = useCourseStore();

const currentCategory = ref('all');
const currentPage = ref(1);
const pageSize = ref(6); // 6 dự án mỗi trang (lưới 2 hoặc 3 cột cân đối)
const projectsGridRef = ref(null);

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
  currentPage.value = 1;
  if (cat === 'all') {
    router.push({ path: '/projects' });
  } else {
    router.push({ path: '/projects', query: { cat } });
  }
};

const allProjects = computed(() => courseStore.projects || []);

const filteredProjects = computed(() => {
  if (currentCategory.value === 'all') {
    return allProjects.value;
  }
  return allProjects.value.filter(item => item.category === currentCategory.value);
});

const paginatedProjects = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  return filteredProjects.value.slice(start, start + pageSize.value);
});

const onPageChange = () => {
  nextTick(() => {
    if (projectsGridRef.value) {
      const topOffset = projectsGridRef.value.getBoundingClientRect().top + window.scrollY - 100;
      window.scrollTo({ top: topOffset, behavior: 'smooth' });
    }
  });
};
</script>

<style scoped src="@/styles/views/Projects.css"></style>
