<template>
  <div class="lecturers-page container">
    <!-- Hero Header -->
    <div class="header-section animate-fade-in">
      <h1>Đội ngũ <span class="gradient-text">Giảng viên & Chuyên gia <span style="white-space: nowrap;">Thực chiến</span></span></h1>
    </div>

    <!-- Mega Dropdown-Style Layout Container (Giao diện giống hệt ĐÀO TẠO) -->
    <div class="mega-style-layout glass-card">
      <!-- Left Sidebar: Categories Navigation -->
      <div class="mega-menu-sidebar">
        <button 
          v-for="major in majors" 
          :key="major.id"
          class="mega-sidebar-item"
          :class="{ active: selectedMajor === major.id }"
          @click="selectMajor(major.id)"
          @mouseenter="selectMajorHover(major.id)"
        >
          <span class="indicator-bar"></span>
          <span>{{ major.name }}</span>
          <span class="cat-count-badge">{{ getMajorCount(major.id) }}</span>
        </button>
      </div>

      <!-- Right Content: Lecturers Grid for selected major -->
      <div class="mega-menu-content">
        <div class="mega-content-header">
          <div>
            <span class="cat-badge-small">{{ activeMajorMeta.badge }}</span>
            <h2 class="mega-content-title">{{ activeMajorMeta.name }}</h2>
          </div>
          <p class="cat-desc-small">{{ activeMajorMeta.description }}</p>
        </div>

        <!-- Lecturers Cards Grid -->
        <template v-if="filteredLecturers.length > 0">
          <div class="mega-programs-grid">
            <div 
              v-for="l in paginatedLecturers" 
              :key="l.id"
              class="mega-program-card lecturer-mega-card"
            >
              <div class="mega-card-link">
                <div class="mega-school-logo lecturer-avatar-box">
                  <img :src="formatImageUrl(l.avatar, 's400')" :alt="l.name" loading="lazy" decoding="async" width="160" height="160" @error="(e) => e.target.src = '/images/1_6.png'" referrerpolicy="no-referrer" />
                </div>
                <div class="mega-card-info">
                  <div class="card-header-badge-row">
                    <span class="mega-school-name">{{ l.majorName || 'Chuyên gia Đào tạo' }}</span>
                  </div>
                  <h4 class="mega-program-title" :title="l.name">{{ l.name }}</h4>
                  <p class="lecturer-sub-title">{{ l.title }}</p>

                  <p class="mega-program-desc" style="white-space: pre-line;">{{ l.bioShort }}</p>
                  <div class="mega-card-footer" v-if="l.show_detail_btn || l.showDetailBtn">
                    <router-link :to="'/giang-vien/' + l.id" class="mega-enroll-btn">Xem chi tiết giới thiệu &rarr;</router-link>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Pagination Component -->
          <Pagination 
            v-if="filteredLecturers.length > pageSize"
            v-model:currentPage="currentPage"
            :totalItems="filteredLecturers.length"
            :pageSize="pageSize"
            @page-change="onPageChange"
          />
        </template>

        <div v-else class="empty-state">
          <p>Chưa tìm thấy giảng viên phù hợp trong chuyên ngành này.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useCourseStore } from '@/stores/courses';
import { formatImageUrl } from '@/utils/imageHelper';
import Pagination from '@/components/Pagination.vue';

const courseStore = useCourseStore();
const selectedMajor = ref('all');
const currentPage = ref(1);
const pageSize = ref(6);

const majors = computed(() => {
  const list = courseStore.lecturerMajors || [];
  return [
    { id: 'all', name: 'Tất cả chuyên ngành' },
    ...list
  ];
});

const allLecturers = computed(() => {
  return courseStore.lecturers || [];
});

const selectMajor = (id) => {
  currentPage.value = 1;
  selectedMajor.value = id;
};

const selectMajorHover = (id) => {
  if (selectedMajor.value !== id) {
    currentPage.value = 1;
  }
  selectedMajor.value = id;
};

const getMajorCount = (id) => {
  if (id === 'all') return allLecturers.value.length;
  return allLecturers.value.filter(l => {
    const ids = l.majorIds || (l.majorId ? [l.majorId] : []);
    return ids.includes(id);
  }).length;
};

const activeMajorMeta = computed(() => {
  const currentMajor = majors.value.find(m => m.id === selectedMajor.value);
  if (!currentMajor || selectedMajor.value === 'all') {
    return {
      name: ' Đội ngũ Giảng viên & Chuyên gia',
    };
  }
  return {
    name: `Chuyên gia ${currentMajor.name}`,
    // badge: (currentMajor.badge || currentMajor.name).toUpperCase(),
    // description: currentMajor.description || `Đội ngũ giảng viên thực chiến chuyên sâu thuộc lĩnh vực ${currentMajor.name} tại ACC Academy.`
  };
});

const filteredLecturers = computed(() => {
  if (selectedMajor.value === 'all') {
    return allLecturers.value;
  }
  const majorId = selectedMajor.value;
  return allLecturers.value
    .filter(l => {
      const ids = l.majorIds || (l.majorId ? [l.majorId] : []);
      return ids.includes(majorId);
    })
    .sort((a, b) => {
      const posA = a.major_positions && a.major_positions[majorId] !== undefined ? a.major_positions[majorId] : (a.position ?? 999);
      const posB = b.major_positions && b.major_positions[majorId] !== undefined ? b.major_positions[majorId] : (b.position ?? 999);
      if (posA !== posB) return posA - posB;
      return (a.name || '').localeCompare(b.name || '', 'vi');
    });
});

const paginatedLecturers = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  return filteredLecturers.value.slice(start, start + pageSize.value);
});

const onPageChange = () => {
  window.scrollTo({ top: 180, behavior: 'smooth' });
};

onMounted(() => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
  const tasks = [];
  tasks.push(courseStore.fetchLecturerMajors());
  tasks.push(courseStore.fetchLecturers());
  if (tasks.length > 0) {
    Promise.all(tasks).catch(() => {});
  }
});
</script>

<style scoped src="@/styles/views/Lecturers.css"></style>
