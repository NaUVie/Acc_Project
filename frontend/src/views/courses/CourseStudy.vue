<template>
  <div class="study-room-view">
    <!-- STUDY ROOM HEADER -->
    <header class="study-header glass-card">
      <div class="header-left">
        <router-link to="/dashboard" class="back-btn" title="Quay lại trang cá nhân">
          <div class="back-icon-box">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <path d="M19 12H5M12 19l-7-7 7-7"/>
            </svg>
          </div>
          <span class="back-text">Dashboard</span>
        </router-link>
        
        <span class="divider"></span>
        
        <div class="course-meta-header">
          <span class="course-badge">ACC PLATFORM</span>
          <h1 class="course-title">{{ course?.title || 'Phòng học ACC Academy' }}</h1>
        </div>
      </div>
      
      <div class="header-right">
        <!-- Progress Widget -->
        <div class="progress-widget">
          <div class="progress-text-row">
            <span class="progress-title">Tiến độ khóa học</span>
            <span class="progress-percent-badge">{{ progressPercent }}%</span>
          </div>
          <div class="progress-track">
            <div class="progress-fill" :style="{ width: progressPercent + '%' }"></div>
          </div>
        </div>

        <button 
          class="btn-mark-complete-header" 
          :class="{ 'completed': activeLesson?.completed }"
          @click="markActiveLessonCompleted"
          title="Đánh dấu hoàn thành bài học này"
        >
          <span class="check-icon">{{ activeLesson?.completed ? '✓' : '○' }}</span>
          <span class="btn-label">{{ activeLesson?.completed ? 'Đã hoàn thành' : 'Đánh dấu đã học' }}</span>
        </button>
      </div>
    </header>

    <!-- STUDY ROOM BODY -->
    <div class="study-body" v-if="course">
      <!-- SIDEBAR: CURRICULUM ACCORDION -->
      <aside class="study-sidebar glass-card">
        <div class="sidebar-header">
          <div class="sidebar-title-group">
            <h3>Nội dung khóa học</h3>
            <p class="lessons-count">{{ completedLessonsCount }} / {{ totalLessonsCount }} bài đã học</p>
          </div>
          <div class="sidebar-progress-ring">
            <svg class="ring-svg" width="36" height="36" viewBox="0 0 36 36">
              <path class="ring-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
              <path class="ring-fill" :stroke-dasharray="progressPercent + ', 100'" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
            </svg>
            <span class="ring-text">{{ progressPercent }}%</span>
          </div>
        </div>
        
        <div class="chapters-list">
          <div 
            v-for="(chapter, cIdx) in curriculum" 
            :key="cIdx" 
            class="chapter-item"
            :class="{ 'expanded': chapter.expanded }"
          >
            <div class="chapter-title-row" @click="chapter.expanded = !chapter.expanded">
              <div class="chapter-info">
                <span class="chapter-index">CHƯƠNG {{ cIdx + 1 }}</span>
                <span class="chapter-name">{{ chapter.name }}</span>
              </div>
              <div class="chapter-right-meta">
                <span class="chapter-lessons-badge">{{ chapter.lessons.length }} bài</span>
                <svg class="chevron-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M6 9l6 6 6-6"/>
                </svg>
              </div>
            </div>
            
            <div class="lessons-list" v-show="chapter.expanded">
              <div 
                v-for="lesson in chapter.lessons" 
                :key="lesson.id" 
                class="lesson-item-row"
                :class="{ 'active': activeLesson?.id === lesson.id, 'is-completed': lesson.completed }"
                @click="selectLesson(lesson)"
              >
                <div class="lesson-check-wrapper" @click.stop="toggleLessonCompleted(lesson)">
                  <span class="custom-checkbox" :class="{ 'checked': lesson.completed }">
                    <svg v-if="lesson.completed" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                      <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                  </span>
                </div>
                
                <div class="lesson-content-meta">
                  <span class="lesson-type-badge" :class="lesson.type">
                    <span v-if="lesson.type === 'video'">🎥 Video</span>
                    <span v-else-if="lesson.type === 'zoom'">⚡ Live Zoom</span>
                    <span v-else-if="lesson.type === 'document'">📄 Slide</span>
                    <span v-else>📝 Bài tập</span>
                  </span>
                  <span class="lesson-title">{{ lesson.title }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </aside>

      <!-- MAIN CONTENT AREA -->
      <main class="study-main">
        <!-- LESSON CONTENT SCREEN CONTAINER -->
        <div class="lesson-screen glass-card">
          <!-- 1. VIDEO LESSON SCREEN -->
          <div v-if="activeLesson?.type === 'video'" class="video-player-container">
            <div class="screen-watermark">
              <span class="watermark-logo">ACC ACADEMY</span>
              <span class="watermark-status">● HQ VIDEO PLAYER</span>
            </div>
            <video 
              v-if="videoUrl" 
              controls 
              autoplay
              :src="videoUrl" 
              class="lesson-video"
              @ended="markActiveLessonCompleted"
            ></video>
            <div v-else class="video-placeholder">
              <div class="play-pulse-ring">
                <span class="play-btn-large">▶</span>
              </div>
              <p>Đang chuẩn bị video bài giảng HD...</p>
            </div>
          </div>

          <!-- 2. ZOOM MEETING LINK SCREEN -->
          <div v-else-if="activeLesson?.type === 'zoom'" class="zoom-screen-container">
            <div class="zoom-card-glow">
              <div class="zoom-header-banner">
                <span class="live-pulsing-badge">
                  <span class="live-dot"></span> BÀI HỌC TRỰC TUYẾN LIVE
                </span>
                <span class="zoom-tag">ZOOM INTERACTIVE CLASS</span>
              </div>

              <div class="zoom-brand-header">
                <img src="/images/logo3.png" alt="ACC Logo" class="zoom-logo-img" />
                <h2>Lớp Học Trực Tuyến Qua Zoom</h2>
                <p class="zoom-subtitle">Tương tác trực tiếp 1:1 với Chuyên gia ACC Academy. Đặt câu hỏi và cùng giải bài tập thực chiến.</p>
              </div>
              
              <div class="zoom-details-grid">
                <div class="detail-card">
                  <div class="detail-icon">🗓️</div>
                  <div class="detail-info">
                    <span class="detail-label">Lịch học Live</span>
                    <strong class="detail-value">{{ activeLesson.zoomTime || 'Thứ 3 & 5 hàng tuần (19:30)' }}</strong>
                  </div>
                </div>
                <div class="detail-card">
                  <div class="detail-icon">🔑</div>
                  <div class="detail-info">
                    <span class="detail-label">Meeting ID</span>
                    <strong class="detail-value code-font">{{ activeLesson.meetingId || '888 999 6688' }}</strong>
                  </div>
                </div>
                <div class="detail-card">
                  <div class="detail-icon">🔒</div>
                  <div class="detail-info">
                    <span class="detail-label">Mật mã (Passcode)</span>
                    <strong class="detail-value code-font">{{ activeLesson.passcode || 'ACC2026' }}</strong>
                  </div>
                </div>
                <div class="detail-card">
                  <div class="detail-icon">👨‍🏫</div>
                  <div class="detail-info">
                    <span class="detail-label">Giảng viên hướng dẫn</span>
                    <strong class="detail-value">Senior AI Mentor ACC</strong>
                  </div>
                </div>
              </div>
              
              <div class="zoom-action-box">
                <a :href="activeLesson.zoomLink || 'https://zoom.us'" target="_blank" class="btn btn-primary btn-zoom-launch">
                  🚀 VÀO PHÒNG HỌC ZOOM NGAY
                </a>
                
                <button @click="markActiveLessonCompleted" class="btn-mark-zoom">
                  {{ activeLesson?.completed ? '✓ Đã đánh dấu hoàn thành buổi học' : 'Đánh dấu đã hoàn thành buổi học này' }}
                </button>
              </div>
            </div>
          </div>

          <!-- 3. DOCUMENT SCREEN -->
          <div v-else-if="activeLesson?.type === 'document'" class="doc-screen-container">
            <div class="doc-card-wrapper">
              <div class="doc-header-icon">
                <div class="icon-circle">📂</div>
              </div>
              <h2>Giáo trình Slide & Tài liệu thực hành</h2>
              <p class="doc-desc">Tải giáo trình chi tiết, bộ prompt câu lệnh và bài tập thực hành dành riêng cho bài học này.</p>
              
              <div class="doc-download-grid">
                <a :href="activeLesson.docUrl || '#'" class="doc-card-button" download @click="markActiveLessonCompleted">
                  <div class="doc-file-type pdf">PDF</div>
                  <div class="doc-file-info">
                    <strong>Slide bài giảng chi tiết (PDF)</strong>
                    <span class="file-meta">Tài liệu chính thức • 14.8 MB</span>
                  </div>
                  <span class="download-icon">📥</span>
                </a>

                <a :href="activeLesson.srcCodeUrl || '#'" class="doc-card-button" download @click="markActiveLessonCompleted">
                  <div class="doc-file-type zip">ZIP</div>
                  <div class="doc-file-info">
                    <strong>Bộ Prompt mẫu & Source code thực hành</strong>
                    <span class="file-meta">Tệp tài nguyên mẫu • 4.2 MB</span>
                  </div>
                  <span class="download-icon">📥</span>
                </a>
              </div>
            </div>
          </div>

          <!-- LESSON NAVIGATION TOOLBAR -->
          <div class="lesson-navigation-bar">
            <button @click="prevLesson" class="nav-arrow-btn" :disabled="isFirstLesson">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M15 18l-6-6 6-6"/>
              </svg>
              <span>Bài trước</span>
            </button>

            <div class="current-lesson-info">
              <span class="current-badge">Đang học:</span>
              <h3 class="current-title">{{ activeLesson?.title }}</h3>
            </div>

            <button @click="nextLesson" class="nav-arrow-btn primary" :disabled="isLastLesson">
              <span>Bài tiếp theo</span>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 18l6-6-6-6"/>
              </svg>
            </button>
          </div>
        </div>

        <!-- TABS CONTAINER -->
        <div class="tabs-container glass-card">
          <div class="tabs-header-bar">
            <button 
              class="tab-nav-item" 
              :class="{ 'active': activeTab === 'overview' }"
              @click="activeTab = 'overview'"
            >
              <span class="tab-icon">📝</span>
              <span>Nội dung bài học</span>
            </button>
            
            <button 
              class="tab-nav-item" 
              :class="{ 'active': activeTab === 'resources' }"
              @click="activeTab = 'resources'"
            >
              <span class="tab-icon">📂</span>
              <span>Tài nguyên đính kèm</span>
            </button>

            <button 
              class="tab-nav-item" 
              :class="{ 'active': activeTab === 'qa' }"
              @click="activeTab = 'qa'"
            >
              <span class="tab-icon">💬</span>
              <span>Thảo luận & Hỏi đáp</span>
              <span class="qa-badge-count">{{ qas.length }}</span>
            </button>
          </div>

          <div class="tab-content-body">
            <!-- TAB 1: OVERVIEW -->
            <div v-if="activeTab === 'overview'" class="tab-pane overview-pane">
              <div class="content-section-card">
                <div class="section-title-row">
                  <span class="section-icon">🎯</span>
                  <h3>Mục tiêu bài học</h3>
                </div>
                <p class="section-paragraph">{{ activeLesson?.objective || 'Nắm vững khái niệm cốt lõi và vận dụng ngay vào công việc thực tế.' }}</p>
              </div>

              <div class="content-section-card mt-6">
                <div class="section-title-row">
                  <span class="section-icon">✨</span>
                  <h3>Nội dung cốt lõi bài học</h3>
                </div>
                <div class="key-points-grid">
                  <div v-for="(point, pIdx) in activeLesson?.keyPoints" :key="pIdx" class="key-point-item">
                    <span class="point-check-icon">✓</span>
                    <span class="point-text">{{ point }}</span>
                  </div>
                </div>
              </div>

              <div class="content-section-card mt-6 highlight-box">
                <div class="section-title-row">
                  <span class="section-icon">💡</span>
                  <h3>Hướng dẫn thực hành</h3>
                </div>
                <p class="section-paragraph italic">{{ activeLesson?.instructions || 'Đọc tài liệu đính kèm, làm theo video bài giảng và thực hành lại bài tập mẫu.' }}</p>
              </div>
            </div>

            <!-- TAB 2: RESOURCES -->
            <div v-if="activeTab === 'resources'" class="tab-pane resources-pane">
              <div class="resources-grid">
                <div class="resource-card">
                  <div class="resource-card-icon">📂</div>
                  <div class="resource-card-details">
                    <h4>Slide bài giảng chi tiết</h4>
                    <p>Tóm tắt toàn bộ sơ đồ tư duy và lý thuyết cốt lõi dạng slide PDF.</p>
                    <a :href="activeLesson?.docUrl || '#'" target="_blank" class="resource-btn">📥 Tải slide PDF</a>
                  </div>
                </div>

                <div v-if="activeLesson?.srcCodeUrl" class="resource-card">
                  <div class="resource-card-icon">💻</div>
                  <div class="resource-card-details">
                    <h4>Mã nguồn & Prompt mẫu</h4>
                    <p>Bộ câu lệnh prompt và source code mẫu dùng trực tiếp cho bài thực hành.</p>
                    <a :href="activeLesson?.srcCodeUrl" target="_blank" class="resource-btn">📥 Tải bộ Prompt</a>
                  </div>
                </div>

                <div class="resource-card">
                  <div class="resource-card-icon">💬</div>
                  <div class="resource-card-details">
                    <h4>Nhóm Hỗ trợ Học viên 24/7</h4>
                    <p>Tham gia cộng đồng Zalo/Discord để được Mentor hỗ trợ trực tiếp.</p>
                    <a href="https://zalo.me" target="_blank" class="resource-btn zalo">🚀 Tham gia nhóm Zalo</a>
                  </div>
                </div>
              </div>
            </div>

            <!-- TAB 3: Q&A -->
            <div v-if="activeTab === 'qa'" class="tab-pane qa-pane">
              <form @submit.prevent="submitQa" class="qa-submit-box">
                <div class="form-header-row">
                  <div class="user-avatar-sm">{{ getUserInitials(courseStore.userMe?.fullname) }}</div>
                  <span class="form-hint">Đặt câu hỏi của bạn cho bài học này:</span>
                </div>
                <textarea 
                  v-model="newQaText" 
                  placeholder="Nhập nội dung thắc mắc hoặc câu hỏi cần trợ giúp..."
                  required
                  rows="3"
                ></textarea>
                <div class="form-action-row">
                  <button type="submit" class="btn btn-primary btn-sm">🚀 Gửi câu hỏi cho Mentor</button>
                </div>
              </form>

              <div class="qa-comments-feed mt-6">
                <div v-for="qa in currentLessonQas" :key="qa.id" class="qa-comment-card">
                  <div class="comment-author-row">
                    <div class="avatar-circle">{{ getUserInitials(qa.username) }}</div>
                    <div class="author-meta">
                      <span class="author-name">{{ qa.username }}</span>
                      <span class="comment-time">{{ qa.time }}</span>
                    </div>
                  </div>
                  <p class="comment-body">{{ qa.text }}</p>

                  <div v-if="qa.reply" class="mentor-reply-card">
                    <div class="comment-author-row">
                      <div class="avatar-circle mentor-avatar">👨‍🏫</div>
                      <div class="author-meta">
                        <span class="author-name mentor-name">Senior Mentor ACC Academy</span>
                        <span class="comment-time mentor-badge">Chuyên gia giải đáp</span>
                      </div>
                    </div>
                    <p class="comment-body mentor-body">{{ qa.reply }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>

    <div v-else class="loading-container py-12 text-center">
      <div class="loading-spinner"></div>
      <h2>Đang tải không gian học tập...</h2>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useCourseStore } from '@/stores/courses';

const route = useRoute();
const router = useRouter();
const courseStore = useCourseStore();

const activeTab = ref('overview');
const newQaText = ref('');
const videoUrl = computed(() => {
  return activeLesson.value?.videoUrl || 'https://www.w3schools.com/html/mov_bbb.mp4';
});

const studyCourseData = ref(null);
const course = computed(() => {
  return studyCourseData.value || courseStore.getCourseByHandle(route.params.handle);
});

// Dynamic curriculum generator based on handle
const curriculum = ref([]);

// Generate syllabus upon mounting
onMounted(async () => {
  const handle = route.params.handle;
  try {
    const data = await courseStore.fetchCourseStudyData(handle);
    if (data) {
      studyCourseData.value = data;
    }
  } catch (err) {
    alert(err.message || 'Bạn chưa có quyền truy cập khóa học này!');
    router.push(`/course/${handle}`);
    return;
  }

  if (!course.value) {
    if (courseStore.courses.length === 0) {
      await courseStore.fetchCourses();
    }
  }

  if (!course.value) {
    alert('Không tìm thấy khóa học này!');
    router.push('/dashboard');
    return;
  }
  
  // Build customized curriculum structure
  generateCurriculum(course.value);
  
  // Set first lesson active
  if (curriculum.value.length > 0 && curriculum.value[0].lessons.length > 0) {
    activeLesson.value = curriculum.value[0].lessons[0];
  }
});

const activeLesson = ref(null);

const generateCurriculum = (c) => {
  if (c.curriculumData) {
    try {
      curriculum.value = JSON.parse(c.curriculumData).map(ch => ({
        ...ch,
        expanded: ch.expanded !== undefined ? ch.expanded : true,
        lessons: ch.lessons.map(l => ({ ...l, completed: l.completed || false }))
      }));
      return;
    } catch (e) {
      console.error("Failed to parse course curriculumData", e);
    }
  }

  const handle = c.handle;
  if (handle === 'chatgpt-work-automation') {
    curriculum.value = [
      {
        name: 'Tổng quan & Thiết lập trợ lý OpenAI',
        expanded: true,
        lessons: [
          { id: 'chat-1', type: 'video', title: 'Bài 1: Giới thiệu hệ sinh thái OpenAI và ChatGPT', completed: false, objective: 'Tổng quan về cuộc cách mạng AI và cơ chế hoạt động của ChatGPT.', keyPoints: ['Hiểu cách học máy sinh text', 'Cách tạo tài khoản OpenAI Plus', 'Thiết lập cấu hình giao diện tối ưu'], instructions: 'Mở ứng dụng ChatGPT và thiết lập các thông số ban đầu.' },
          { id: 'chat-2', type: 'document', title: 'Bài 2: Tài liệu cấu trúc thiết kế Prompt mẫu', completed: false, objective: 'Nắm vững các mẫu prompt phổ biến áp dụng cho công việc văn phòng.', keyPoints: ['Mô hình prompt ROLE-TASK-CONTEXT', 'Tối ưu hóa phản hồi của AI', 'Cách sửa đổi câu trả lời theo tone giọng'], instructions: 'Tải PDF tài liệu và viết thử 3 prompt đầu tiên theo hướng dẫn.' }
        ]
      },
      {
        name: 'Tự động hóa tác vụ văn phòng chuyên sâu',
        expanded: true,
        // Zoom and Video modules
        lessons: [
          { id: 'chat-3', type: 'zoom', title: 'Bài 3: Thực hành Viết Prompt nâng cao (Live qua Zoom)', completed: false, objective: 'Tham gia tương tác trực tiếp giải đề bài thực tế từ giảng viên.', zoomTime: 'Thứ Ba tuần tới lúc 19:30', meetingId: '864 2291 9900', passcode: 'OPENAI10X', zoomLink: 'https://zoom.us', keyPoints: ['Sửa lỗi prompt phổ biến', 'Chữa bài tập thực hành của học viên', 'Q&A trực tiếp cùng giảng viên'], instructions: 'Chuẩn bị micro và bài tập chương 1 để trao đổi trực tiếp.' },
          { id: 'chat-4', type: 'video', title: 'Bài 4: Tự động soạn thảo văn bản, email, báo cáo', completed: false, objective: 'Học cách soạn thảo nhanh các loại văn bản công sở chỉ trong 2 phút.', keyPoints: ['Công thức viết email phản hồi khách hàng tự động', 'Tạo dàn ý báo cáo doanh số chi tiết', 'Tối ưu hóa cấu trúc bài viết chuẩn SEO'], instructions: 'Chạy thử công thức viết email trên ChatGPT.' }
        ]
      }
    ];
  } else if (handle === 'ai-center-of-excellence') {
    curriculum.value = [
      {
        name: 'Chiến lược quản trị AI trong tổ chức',
        expanded: true,
        lessons: [
          { id: 'coe-1', type: 'video', title: 'Bài 1: Tại sao doanh nghiệp cần xây dựng AI Center of Excellence', completed: false, objective: 'Hiểu về cấu trúc ban điều hành AI chuyên trách.', keyPoints: ['Mô hình AI COE hiện đại', 'Vai trò của CXO trong chỉ đạo chuyển đổi số', 'Các rủi ro bảo mật dữ liệu'], instructions: 'Xem hết video bài giảng và thảo luận cùng đội nhóm.' },
          { id: 'coe-2', type: 'zoom', title: 'Bài 2: Thiết lập quy chuẩn sử dụng AI an toàn (Live qua Zoom)', completed: false, objective: 'Quy chế sử dụng AI để không rò rỉ dữ liệu mật công ty.', zoomTime: 'Thứ Năm tuần này lúc 20:00', meetingId: '822 5506 1234', passcode: 'AICOE2026', zoomLink: 'https://zoom.us', keyPoints: ['Các quy định an toàn thông tin', 'Thiết lập mạng nội bộ sử dụng API', 'Kiểm tra tài khoản dùng chung'], instructions: 'Đọc kỹ tài liệu nội bộ trước khi tham gia buổi Zoom.' }
        ]
      }
    ];
  } else {
    // Default Curriculum for other courses
    curriculum.value = [
      {
        name: 'Giới thiệu & Tổng quan',
        expanded: true,
        lessons: [
          { id: 'def-1', type: 'video', title: 'Bài 1: Giới thiệu tổng quan và Lộ trình học tập', completed: false, objective: 'Tìm hiểu tổng quan lộ trình và chuẩn bị môi trường thực hành.', keyPoints: ['Hiểu rõ mục tiêu đầu ra', 'Cài đặt công cụ cần thiết', 'Tài liệu hướng dẫn bắt đầu'], instructions: 'Xem video và ghi chú lại lộ trình học tập của bạn.' },
          { id: 'def-2', type: 'document', title: 'Bài 2: Tài liệu giáo trình học tập', completed: false, objective: 'Nắm bắt lý thuyết nền tảng.', keyPoints: ['Tóm tắt kiến thức cốt lõi', 'Sơ đồ tư duy bài học', 'Danh sách tài nguyên tham khảo'], instructions: 'Tải slide bài học để đọc kỹ trước khi thực hành.' }
        ]
      },
      {
        name: 'Kiến thức cốt lõi & Thực hành',
        expanded: true,
        lessons: [
          { id: 'def-3', type: 'zoom', title: 'Bài 3: Hướng dẫn thực hành trực tuyến (Live qua Zoom)', completed: false, objective: 'Tương tác trực tiếp chữa bài tập và giải đáp thắc mắc cùng Mentor.', zoomTime: 'Thứ Ba tuần tới lúc 19:30', meetingId: '888 777 9999', passcode: 'ACC2026', zoomLink: 'https://zoom.us', keyPoints: ['Giải đáp câu hỏi thực hành', 'Chia sẻ kinh nghiệm thực chiến', 'Mentor chữa bài trực tiếp'], instructions: 'Đăng nhập vào Zoom đúng giờ và chuẩn bị sẵn câu hỏi.' },
          { id: 'def-4', type: 'video', title: 'Bài 4: Bài tập ứng dụng thực tế', completed: false, objective: 'Áp dụng kiến thức để giải quyết bài toán thực tế.', keyPoints: ['Các bước triển khai chi tiết', 'Tối ưu hóa kết quả đầu ra', 'Kiểm thử và đánh giá'], instructions: 'Thực hành lại các bước được hướng dẫn trong video.' }
        ]
      }
    ];
  }
};

// Selection
const selectLesson = (lesson) => {
  activeLesson.value = lesson;
};

// Completion state calculations
const totalLessonsCount = computed(() => {
  let count = 0;
  curriculum.value.forEach(chapter => {
    count += chapter.lessons.length;
  });
  return count;
});

const completedLessonsCount = computed(() => {
  let count = 0;
  curriculum.value.forEach(chapter => {
    chapter.lessons.forEach(l => {
      if (l.completed) count++;
    });
  });
  return count;
});

const progressPercent = computed(() => {
  if (totalLessonsCount.value === 0) return 0;
  return Math.round((completedLessonsCount.value / totalLessonsCount.value) * 100);
});

const toggleLessonCompleted = (lesson) => {
  lesson.completed = !lesson.completed;
};

const markActiveLessonCompleted = () => {
  if (activeLesson.value) {
    activeLesson.value.completed = true;
  }
};

// Navigation
const flatLessons = computed(() => {
  const list = [];
  curriculum.value.forEach(c => {
    c.lessons.forEach(l => {
      list.push(l);
    });
  });
  return list;
});

const activeLessonIndex = computed(() => {
  if (!activeLesson.value) return -1;
  return flatLessons.value.findIndex(l => l.id === activeLesson.value.id);
});

const isFirstLesson = computed(() => activeLessonIndex.value === 0);
const isLastLesson = computed(() => activeLessonIndex.value === flatLessons.value.length - 1);

const prevLesson = () => {
  const idx = activeLessonIndex.value;
  if (idx > 0) {
    activeLesson.value = flatLessons.value[idx - 1];
  }
};

const nextLesson = () => {
  const idx = activeLessonIndex.value;
  if (idx < flatLessons.value.length - 1) {
    activeLesson.value = flatLessons.value[idx + 1];
  }
};

// Mock Q&As database
const qas = ref([
  { id: 1, lessonId: 'chat-1', username: 'Lê Văn Nam', time: '1 giờ trước', text: 'Thầy cho em hỏi tài khoản OpenAI Plus hiện tại thanh toán bằng thẻ Visa Việt Nam được không ạ?', reply: 'Được em nhé. OpenAI hiện đã mở rộng hỗ trợ cổng thanh toán cho các thẻ Visa/Mastercard tại Việt Nam rất dễ dàng.' },
  { id: 2, lessonId: 'chat-1', username: 'Trần Thị Mai', time: '3 giờ trước', text: 'Bài học rất hay và trực quan, em cảm ơn thầy!', reply: 'Cảm ơn Mai, chúc em học tốt và ứng dụng thành công nhé!' },
  { id: 3, lessonId: 'chat-2', username: 'Hoàng Long', time: 'Hôm qua', text: 'Em dùng Claude thay ChatGPT để viết prompt theo cấu trúc này có được không ạ?', reply: 'Claude cực kỳ giỏi ngữ cảnh nên áp dụng cấu trúc prompt ROLE-TASK-CONTEXT này còn đem lại kết quả viết xuất sắc hơn nữa em nhé.' }
]);

const currentLessonQas = computed(() => {
  if (!activeLesson.value) return [];
  // Return comments for active lesson, or default ones if none match
  const filtered = qas.value.filter(q => q.lessonId === activeLesson.value.id);
  if (filtered.length > 0) return filtered;
  
  // Provide general mock QA if none specifically defined for this lesson ID
  return [
    { id: 99, lessonId: activeLesson.value.id, username: 'Nguyễn Văn Linh', time: 'Vừa xong', text: 'Tài liệu phần thực hành tải ở đâu vậy ạ?', reply: 'Bạn bấm sang Tab "Tài nguyên đính kèm" ngay bên cạnh để lấy link tải giáo trình Slide và source code mẫu nhé.' }
  ];
});

const submitQa = () => {
  if (!newQaText.value.trim() || !activeLesson.value) return;
  
  qas.value.unshift({
    id: Date.now(),
    lessonId: activeLesson.value.id,
    username: courseStore.userMe?.fullname || 'Học viên',
    time: 'Vừa xong',
    text: newQaText.value.trim(),
    reply: null
  });
  
  newQaText.value = '';
};

// Helpers
const getUserInitials = (name) => {
  if (!name) return 'HV';
  const parts = name.trim().split(' ');
  if (parts.length === 1) return parts[0].substring(0, 2).toUpperCase();
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
};
</script>

<style scoped src="@/styles/views/courses/CourseStudy.css"></style>
