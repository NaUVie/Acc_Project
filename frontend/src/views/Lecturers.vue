<template>
  <div class="lecturers-page container">
    <!-- Hero Header -->
    <div class="header-section animate-fade-in">
      <h1>Đội ngũ <span class="gradient-text">Giảng viên & Chuyên gia Thực chiến</span></h1>
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
        <div class="mega-programs-grid" v-if="filteredLecturers.length > 0">
          <div 
            v-for="l in filteredLecturers" 
            :key="l.id"
            class="mega-program-card lecturer-mega-card"
          >
            <div class="mega-card-link">
              <div class="mega-school-logo lecturer-avatar-box">
                <img :src="l.avatar" :alt="l.name" @error="(e) => e.target.src = '/images/1_6.png'" referrerpolicy="no-referrer" />
              </div>
              <div class="mega-card-info">
                <div class="card-header-badge-row">
                  <span class="mega-school-name">{{ l.majorName || 'Chuyên gia Đào tạo' }}</span>
                  <span v-if="l.id === 'nguyen-tan-binh'" class="mini-role-tag gold">Viện trưởng Leadman</span>
                  <span v-else-if="l.id === 'nguyen-vu-huy-hoang'" class="mini-role-tag blue">Giám đốc Đào tạo</span>
                </div>
                <h4 class="mega-program-title" :title="l.name">{{ l.name }}</h4>
                <p class="lecturer-sub-title">{{ l.title }}</p>

                <!-- Statistics Badges -->
                <div class="stats-row">
                  <span class="stat-pill">🎓 {{ l.totalStudents ? l.totalStudents.toLocaleString('vi-VN') : '10,000+' }} học viên</span>
                  <span class="stat-pill">🏫 {{ l.totalSessions || 150 }}+ buổi</span>
                </div>

                <p class="mega-program-desc">{{ l.bioShort }}</p>
                <div class="mega-card-footer">
                  <router-link :to="'/giang-vien/' + l.id" class="mega-enroll-btn">Xem chi tiết giới thiệu &rarr;</router-link>
                </div>
              </div>
            </div>
          </div>
        </div>

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
import { lecturersData } from '@/data/lecturers';

const courseStore = useCourseStore();
const selectedMajor = ref('all');

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
  selectedMajor.value = id;
};

const selectMajorHover = (id) => {
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
      name: 'Tất cả Đội ngũ Giảng viên & Chuyên gia',
      badge: 'TOÀN BỘ GIẢNG VIÊN',
      description: 'Quy tụ các chuyên gia thực chiến hàng đầu trong lĩnh vực AI, Quản trị, Tài chính, Marketing và Vận hành.'
    };
  }
  return {
    name: `Chuyên gia ${currentMajor.name}`,
    badge: (currentMajor.badge || currentMajor.name).toUpperCase(),
    description: currentMajor.description || `Đội ngũ giảng viên thực chiến chuyên sâu thuộc lĩnh vực ${currentMajor.name} tại ACC Academy.`
  };
});

const filteredLecturers = computed(() => {
  if (selectedMajor.value === 'all') {
    return allLecturers.value;
  }
  return allLecturers.value.filter(l => {
    const ids = l.majorIds || (l.majorId ? [l.majorId] : []);
    return ids.includes(selectedMajor.value);
  });
});

onMounted(() => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
  const tasks = [];
  if (courseStore.lecturerMajors.length === 0) {
    tasks.push(courseStore.fetchLecturerMajors());
  }
  if (courseStore.lecturers.length === 0) {
    tasks.push(courseStore.fetchLecturers());
  }
  if (tasks.length > 0) {
    Promise.all(tasks).catch(() => {});
  }
});
</script>

<style scoped src="@/styles/views/Lecturers.css"></style>
