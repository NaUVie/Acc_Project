<template>
  <div class="study-room-view">
    <!-- STUDY ROOM HEADER -->
    <header class="study-header glass-card">
      <div class="header-left">
        <router-link to="/login" class="back-btn">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <line x1="19" y1="12" x2="5" y2="12"></line>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
          Quay lại Dashboard
        </router-link>
        <span class="divider">|</span>
        <h1 class="course-title">{{ course?.title || 'Phòng học ACC Academy' }}</h1>
      </div>
      
      <div class="header-right">
        <!-- Progress Bar -->
        <div class="progress-container">
          <div class="progress-label">Tiến độ học: {{ progressPercent }}%</div>
          <div class="progress-bar-bg">
            <div class="progress-bar-fill" :style="{ width: progressPercent + '%' }"></div>
          </div>
        </div>
      </div>
    </header>

    <!-- STUDY ROOM BODY -->
    <div class="study-body" v-if="course">
      <!-- SIDEBAR: CURRICULUM ACCORDION -->
      <aside class="study-sidebar glass-card">
        <div class="sidebar-header">
          <h3>Nội dung khóa học</h3>
          <span class="lessons-count">{{ completedLessonsCount }}/{{ totalLessonsCount }} bài học</span>
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
                <span class="chapter-index">Chương {{ cIdx + 1 }}:</span>
                <span class="chapter-name">{{ chapter.name }}</span>
              </div>
              <svg class="chevron-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M6 9l6 6 6-6"/>
              </svg>
            </div>
            
            <div class="lessons-list" v-show="chapter.expanded">
              <div 
                v-for="lesson in chapter.lessons" 
                :key="lesson.id" 
                class="lesson-item-row"
                :class="{ 'active': activeLesson?.id === lesson.id }"
                @click="selectLesson(lesson)"
              >
                <div class="lesson-check-wrapper" @click.stop="toggleLessonCompleted(lesson)">
                  <span class="checkbox" :class="{ 'checked': lesson.completed }">✓</span>
                </div>
                <div class="lesson-content-meta">
                  <span class="lesson-type-icon">
                    <span v-if="lesson.type === 'video'">🎥</span>
                    <span v-else-if="lesson.type === 'zoom'">🔗</span>
                    <span v-else-if="lesson.type === 'document'">📄</span>
                    <span v-else>📝</span>
                  </span>
                  <span class="lesson-title">{{ lesson.title }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </aside>

      <!-- MAIN CONTENT: LESSON VIEW & TABS -->
      <main class="study-main">
        <!-- LESSON CONTENT SCREEN -->
        <div class="lesson-screen glass-card">
          <!-- 1. VIDEO LESSON SCREEN -->
          <div v-if="activeLesson?.type === 'video'" class="video-player-container">
            <video 
              v-if="videoUrl" 
              controls 
              autoplay
              :src="videoUrl" 
              class="lesson-video"
              @ended="markActiveLessonCompleted"
            ></video>
            <div v-else class="video-placeholder">
              <span class="play-btn-large">▶</span>
              <p>Đang tải video bài giảng...</p>
            </div>
          </div>

          <!-- 2. ZOOM MEETING LINK SCREEN -->
          <div v-else-if="activeLesson?.type === 'zoom'" class="zoom-screen-container">
            <div class="zoom-card">
              <div class="zoom-badge-live">LIVE LỚP HỌC TRỰC TUYẾN</div>
              <img src="/images/logo2.jpg" alt="ACC Logo" class="zoom-logo" style="height: 50px; margin-bottom: 20px;" />
              <h2>Lớp Học Trực Tuyến Qua Zoom</h2>
              <p class="zoom-subtitle">Lớp học tương tác trực tiếp với chuyên gia của ACC Academy để giải đáp thắc mắc và chữa bài tập thực hành.</p>
              
              <div class="zoom-info-box">
                <div class="info-line">
                  <strong>🗓️ Lịch học:</strong> <span>{{ activeLesson.zoomTime || 'Thứ 3 & Thứ 5 hàng tuần lúc 19:30' }}</span>
                </div>
                <div class="info-line">
                  <strong>🔑 Meeting ID:</strong> <span>{{ activeLesson.meetingId || '888 999 6688' }}</span>
                </div>
                <div class="info-line">
                  <strong>🔒 Mật mã (Pass):</strong> <span>{{ activeLesson.passcode || 'ACC2026' }}</span>
                </div>
              </div>
              
              <a :href="activeLesson.zoomLink || 'https://zoom.us'" target="_blank" class="btn btn-primary btn-zoom mt-6">
                🚀 Tham gia Lớp Zoom Học Ngay
              </a>
              
              <button @click="markActiveLessonCompleted" class="btn btn-outline btn-sm btn-completed-zoom mt-4">
                Đánh dấu đã hoàn thành buổi học này
              </button>
            </div>
          </div>

          <!-- 3. DOCUMENT SCREEN -->
          <div v-else-if="activeLesson?.type === 'document'" class="doc-screen-container">
            <div class="doc-card">
              <div class="doc-icon">📂</div>
              <h2>Slide & Tài liệu bài học</h2>
              <p class="doc-desc">Tải về giáo trình slide PDF và bộ tài liệu hướng dẫn thực hành đi kèm bài học.</p>
              
              <div class="doc-links-box">
                <a :href="activeLesson.docUrl || '#'" class="doc-download-link" download @click="markActiveLessonCompleted">
                  <span>📥 Slide bài giảng (PDF)</span>
                  <span class="file-size">14.8 MB</span>
                </a>
                <a :href="activeLesson.srcCodeUrl || '#'" class="doc-download-link" download @click="markActiveLessonCompleted">
                  <span>📥 Bộ Source Code & Prompt mẫu thực hành</span>
                  <span class="file-size">4.2 MB</span>
                </a>
              </div>
            </div>
          </div>

          <!-- Lesson Navigation Bar -->
          <div class="lesson-navigation">
            <button @click="prevLesson" class="btn btn-outline btn-sm" :disabled="isFirstLesson">
              ← Bài trước
            </button>
            <div class="lesson-header-info">
              <h3>{{ activeLesson?.title }}</h3>
            </div>
            <button @click="nextLesson" class="btn btn-outline btn-sm" :disabled="isLastLesson">
              Bài tiếp theo →
            </button>
          </div>
        </div>

        <!-- TABS CONTAINER -->
        <div class="tabs-container glass-card">
          <div class="tabs-header">
            <button 
              class="tab-btn" 
              :class="{ 'active': activeTab === 'overview' }"
              @click="activeTab = 'overview'"
            >
              📝 Nội dung bài học
            </button>
            <button 
              class="tab-btn" 
              :class="{ 'active': activeTab === 'resources' }"
              @click="activeTab = 'resources'"
            >
              📂 Tài nguyên đính kèm
            </button>
            <button 
              class="tab-btn" 
              :class="{ 'active': activeTab === 'qa' }"
              @click="activeTab = 'qa'"
            >
              💬 Thảo luận & Hỏi đáp ({{ qas.length }})
            </button>
          </div>

          <div class="tab-body">
            <!-- TAB 1: OVERVIEW -->
            <div v-if="activeTab === 'overview'" class="tab-pane overview-pane">
              <h3>Mục tiêu bài học</h3>
              <p>{{ activeLesson?.objective || 'Tìm hiểu các khái niệm cơ bản và cách vận dụng lý thuyết vào thực tế.' }}</p>
              
              <h3 class="mt-4">Nội dung cốt lõi</h3>
              <ul class="key-points">
                <li v-for="(point, pIdx) in activeLesson?.keyPoints" :key="pIdx">
                  {{ point }}
                </li>
              </ul>
              
              <h3 class="mt-4">Hướng dẫn thực hành</h3>
              <div class="instructions-box">
                <p>{{ activeLesson?.instructions || 'Đọc tài liệu đính kèm, thực hành gõ code hoặc áp dụng công thức viết prompt theo hướng dẫn trong video.' }}</p>
              </div>
            </div>

            <!-- TAB 2: RESOURCES -->
            <div v-if="activeTab === 'resources'" class="tab-pane resources-pane">
              <div class="resource-item">
                <span class="resource-icon">📂</span>
                <div class="resource-info">
                  <h4>Slide bài giảng chi tiết</h4>
                  <p>Tóm tắt toàn bộ lý thuyết và sơ đồ tư duy của chương học.</p>
                  <a :href="activeLesson?.docUrl || '#'" target="_blank" class="btn btn-outline btn-xs mt-2 inline-block">Tải slide (PDF)</a>
                </div>
              </div>
              
              <div v-if="activeLesson?.srcCodeUrl" class="resource-item mt-4">
                <span class="resource-icon">💻</span>
                <div class="resource-info">
                  <h4>Tài liệu & Mã nguồn mẫu thực hành</h4>
                  <p>Tải bộ code mẫu hoặc các template prompts được chia sẻ.</p>
                  <a :href="activeLesson?.srcCodeUrl" target="_blank" class="btn btn-outline btn-xs mt-2 inline-block">Tải tài nguyên</a>
                </div>
              </div>

              <div class="resource-item mt-4">
                <span class="resource-icon">🔗</span>
                <div class="resource-info">
                  <h4>Cộng đồng học viên ACC Academy</h4>
                  <p>Tham gia group Zalo/Discord hỗ trợ giải đáp 24/7 từ mentor.</p>
                  <a href="https://zalo.me" target="_blank" class="btn btn-outline btn-xs mt-2 inline-block">Tham gia nhóm</a>
                </div>
              </div>
            </div>

            <!-- TAB 3: Q&A -->
            <div v-if="activeTab === 'qa'" class="tab-pane qa-pane">
              <!-- Comment Form -->
              <form @submit.prevent="submitQa" class="qa-form">
                <textarea 
                  v-model="newQaText" 
                  placeholder="Đặt câu hỏi hoặc chia sẻ ý kiến của bạn về bài học này..."
                  required
                  rows="3"
                ></textarea>
                <button type="submit" class="btn btn-primary btn-sm mt-2">Gửi câu hỏi</button>
              </form>

              <!-- Comments List -->
              <div class="qa-list mt-6">
                <div v-for="qa in currentLessonQas" :key="qa.id" class="qa-item">
                  <div class="qa-user-meta">
                    <div class="avatar">{{ getUserInitials(qa.username) }}</div>
                    <div>
                      <span class="username">{{ qa.username }}</span>
                      <span class="date">{{ qa.time }}</span>
                    </div>
                  </div>
                  <p class="qa-text">{{ qa.text }}</p>
                  
                  <!-- Reply from teacher if exists -->
                  <div v-if="qa.reply" class="qa-reply">
                    <div class="qa-user-meta">
                      <div class="avatar admin-avatar">👨‍🏫</div>
                      <div>
                        <span class="username admin-name">Chuyên gia ACC Academy</span>
                        <span class="date">Mentor</span>
                      </div>
                    </div>
                    <p class="qa-text">{{ qa.reply }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
    
    <div v-else class="loading-container py-12 text-center">
      <h2>Đang tải phòng học...</h2>
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

// Course from route handle
const course = computed(() => {
  return courseStore.getCourseByHandle(route.params.handle);
});

// Dynamic curriculum generator based on handle
const curriculum = ref([]);

// Generate syllabus upon mounting
onMounted(async () => {
  if (courseStore.courses.length === 0) {
    await courseStore.fetchCourses();
  }
  
  if (!course.value) {
    alert('Không tìm thấy khóa học này!');
    router.push('/login');
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
