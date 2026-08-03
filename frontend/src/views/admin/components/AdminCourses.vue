<template>
  <div class="tab-content animate-fade-in">
    <div class="content-header flex-between">
      <div>
        <h2>Quản lý Danh mục Khóa học</h2>
        <p>Danh sách và thông tin chi tiết các khóa học hiển thị trên website.</p>
      </div>
      <button @click="openAddCourseModal" class="btn btn-primary btn-sm">+ Thêm khóa học</button>
    </div>

    <!-- Filters -->
    <div class="filter-bar mt-4">
      <input 
        v-model="courseSearch" 
        type="text" 
        placeholder="Tìm theo tên khóa học, mô tả..." 
        class="admin-search-input"
      />
      <select v-model="courseFilterCategory" class="admin-select">
        <option value="all">Tất cả chuyên mục</option>
        <option value="ky-nang-ai">Kỹ năng AI</option>
        <option value="ky-nang-mem">Kỹ năng mềm</option>
        <option value="ky-nang-chuyen-mon">Kỹ năng chuyên môn</option>
        <option value="bundles">Combo khóa học</option>
      </select>
    </div>

    <!-- Courses Table -->
    <div class="table-responsive mt-6">
      <table class="admin-table">
        <thead>
          <tr>
            <th>Hình ảnh</th>
            <th>Tên khóa học</th>
            <th>Chuyên mục</th>
            <th>Thời lượng</th>
            <th>Trình độ</th>
            <th>Giá hiển thị</th>
            <th>Hành động</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="c in filteredCourses" :key="c.id">
            <td>
              <img :src="c.image" :alt="c.title" class="admin-course-thumb" />
            </td>
            <td class="font-bold">
              <div>{{ c.title }}</div>
              <small class="text-muted">Slug: {{ c.handle }}</small>
            </td>
            <td>
              <span class="badge badge-primary">{{ translateCategory(c.category) }}</span>
            </td>
            <td>{{ c.duration }}</td>
            <td>{{ c.level }}</td>
            <td>
              <div class="price-text font-bold">{{ formatPrice(c.price) }}</div>
              <del class="text-muted text-xs" v-if="c.originalPrice > c.price">{{ formatPrice(c.originalPrice) }}</del>
            </td>
            <td>
              <div class="action-buttons">
                <button @click="openCurriculumModal(c)" class="btn-action edit" style="background: linear-gradient(135deg, #6366f1, #4f46e5); color: white; border: none; font-size: 13px;" title="Quản lý bài giảng">📚</button>
                <button @click="editCourseDetails(c)" class="btn-action edit" title="Sửa thông tin">✏️</button>
                <button @click="deleteCourse(c.id)" class="btn-action delete" title="Xóa">🗑️</button>
              </div>
            </td>
          </tr>
          <tr v-if="filteredCourses.length === 0">
            <td colspan="7" class="text-center py-8 text-muted">Không tìm thấy khóa học nào phù hợp.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- ==================== MODAL: ADD/EDIT COURSE ==================== -->
    <div v-if="courseModalOpen" class="modal-overlay">
      <div class="modal-content glass-card">
        <h3>{{ isEditingCourse ? 'Chỉnh sửa khóa học' : 'Thêm khóa học mới' }}</h3>
        <form @submit.prevent="saveCourse" class="mt-4">
          <div class="form-group">
            <label>Tên khóa học</label>
            <input v-model="courseForm.title" type="text" required class="admin-input-style" placeholder="Ví dụ: ChatGPT thực chiến nâng cao" />
          </div>
          <div class="form-group mt-3">
            <label>Đường dẫn tĩnh (Slug / Handle)</label>
            <input v-model="courseForm.handle" type="text" required class="admin-input-style" placeholder="chatgpt-nang-cao" />
          </div>
          <div class="form-group mt-3">
            <label>Chuyên mục</label>
            <select v-model="courseForm.category" class="admin-input-style">
              <option value="ky-nang-ai">Kỹ năng AI</option>
              <option value="ky-nang-mem">Kỹ năng mềm</option>
              <option value="ky-nang-chuyen-mon">Kỹ năng chuyên môn</option>
              <option value="bundles">Combo khóa học</option>
            </select>
          </div>
          <div class="form-group mt-3">
            <label>Hình ảnh khóa học (URL)</label>
            <input v-model="courseForm.image" type="text" required class="admin-input-style" />
          </div>
          <div class="grid-2 mt-3">
            <div class="form-group">
              <label>Giá bán (VNĐ)</label>
              <input v-model.number="courseForm.price" type="number" required class="admin-input-style" />
            </div>
            <div class="form-group">
              <label>Giá gốc niêm yết (VNĐ)</label>
              <input v-model.number="courseForm.originalPrice" type="number" required class="admin-input-style" />
            </div>
          </div>
          <div class="grid-2 mt-3">
            <div class="form-group">
              <label>Thời lượng</label>
              <input v-model="courseForm.duration" type="text" required class="admin-input-style" placeholder="12 tuần, 24 giờ học..." />
            </div>
            <div class="form-group">
              <label>Trình độ</label>
              <input v-model="courseForm.level" type="text" required class="admin-input-style" placeholder="Cơ bản, Trung cấp, Nâng cao" />
            </div>
          </div>
          <div class="form-group mt-3">
            <label>Mô tả chi tiết khóa học</label>
            <textarea v-model="courseForm.description" rows="3" required class="admin-input-style" placeholder="Mô tả tóm tắt khóa học..."></textarea>
          </div>
          <div class="modal-actions mt-6">
            <button type="button" @click="courseModalOpen = false" class="btn btn-secondary btn-sm">Hủy</button>
            <button type="submit" class="btn btn-primary btn-sm">Lưu lại</button>
          </div>
        </form>
      </div>
    </div>

    <!-- ==================== MODAL: MANAGE CURRICULUM ==================== -->
    <div v-if="curriculumModalOpen" class="modal-overlay">
      <div class="modal-content glass-card" style="max-width: 850px; width: 95%; max-height: 85vh; overflow-y: auto;">
        <div class="flex-between">
          <h3>Quản lý bài giảng & tài liệu: {{ selectedCourseForCurriculum?.title }}</h3>
          <button @click="curriculumModalOpen = false" class="btn btn-outline btn-xs">❌ Đóng</button>
        </div>
        
        <p class="text-muted text-sm mt-1">Thiết lập cấu trúc chương trình học, link Zoom, video bài giảng và các tài nguyên đính kèm.</p>

        <!-- Chapter list builder -->
        <div class="chapters-builder mt-6">
          <div v-for="(chapter, cIdx) in curriculumForm" :key="cIdx" class="chapter-build-card glass-card mb-6" style="padding: 18px; border: 1px solid var(--border-color); background: rgba(255, 255, 255, 0.03);">
            <div class="chapter-build-header flex-between" style="gap: 12px;">
              <div style="flex: 1; display: flex; align-items: center; gap: 8px;">
                <span style="font-weight: bold; min-width: 80px;">Chương {{ cIdx + 1 }}:</span>
                <input v-model="chapter.name" type="text" class="admin-input-style" placeholder="Tên chương học..." required />
              </div>
              <button type="button" @click="removeChapter(cIdx)" class="btn btn-sm btn-danger" style="padding: 6px 12px;">Xóa chương</button>
            </div>

            <!-- Lessons list builder -->
            <div class="lessons-builder mt-4" style="padding-left: 20px; border-left: 2px dashed var(--border-color);">
              <div v-for="(lesson, lIdx) in chapter.lessons" :key="lIdx" class="lesson-build-card mt-3" style="padding: 12px; background: rgba(0,0,0,0.05); border-radius: 6px; border: 1px solid rgba(255,255,255,0.05);">
                <div class="flex-between" style="gap: 12px;">
                  <div style="font-weight: 500; font-size: 13px;">Bài học {{ lIdx + 1 }}:</div>
                  <button type="button" @click="removeLesson(cIdx, lIdx)" class="btn btn-xs btn-danger" style="font-size: 11px;">Xóa bài học</button>
                </div>

                <div class="grid-2 mt-2">
                  <div class="form-group">
                    <label style="font-size: 12px;">Tiêu đề bài học</label>
                    <input v-model="lesson.title" type="text" class="admin-input-style" placeholder="Tên bài giảng..." required />
                  </div>
                  <div class="form-group">
                    <label style="font-size: 12px;">Loại bài học</label>
                    <select v-model="lesson.type" class="admin-input-style">
                      <option value="video">🎥 Video bài giảng</option>
                      <option value="zoom">🔗 Lớp học Live Zoom</option>
                      <option value="document">📄 Slide & Tài liệu</option>
                    </select>
                  </div>
                </div>

                <!-- Custom inputs based on lesson type -->
                <div class="type-custom-fields mt-3" style="padding: 10px; background: rgba(255,255,255,0.02); border-radius: 4px; border: 1px solid rgba(255,255,255,0.02);">
                  <!-- Video fields -->
                  <div v-if="lesson.type === 'video'" class="form-group">
                    <label style="font-size: 12px;">Đường dẫn Video bài giảng (MP4/HLS Link)</label>
                    <input v-model="lesson.videoUrl" type="text" class="admin-input-style" placeholder="https://example.com/lecture.mp4" />
                  </div>

                  <!-- Zoom fields -->
                  <div v-if="lesson.type === 'zoom'">
                    <div class="grid-2">
                      <div class="form-group">
                        <label style="font-size: 12px;">Lịch học Zoom</label>
                        <input v-model="lesson.zoomTime" type="text" class="admin-input-style" placeholder="Thứ Ba tuần tới lúc 19:30" />
                      </div>
                      <div class="form-group">
                        <label style="font-size: 12px;">Zoom Link trực tiếp</label>
                        <input v-model="lesson.zoomLink" type="text" class="admin-input-style" placeholder="https://zoom.us/j/..." />
                      </div>
                    </div>
                    <div class="grid-2 mt-2">
                      <div class="form-group">
                        <label style="font-size: 12px;">Meeting ID</label>
                        <input v-model="lesson.meetingId" type="text" class="admin-input-style" placeholder="888 999 6688" />
                      </div>
                      <div class="form-group">
                        <label style="font-size: 12px;">Mật mã (Passcode)</label>
                        <input v-model="lesson.passcode" type="text" class="admin-input-style" placeholder="ACC2026" />
                      </div>
                    </div>
                  </div>

                  <!-- Document fields -->
                  <div v-if="lesson.type === 'document'" class="grid-2">
                    <div class="form-group">
                      <label style="font-size: 12px;">Link tải Slide bài giảng (PDF)</label>
                      <input v-model="lesson.docUrl" type="text" class="admin-input-style" placeholder="Link tải slide..." />
                    </div>
                    <div class="form-group">
                      <label style="font-size: 12px;">Link tải Source code / Prompt mẫu</label>
                      <input v-model="lesson.srcCodeUrl" type="text" class="admin-input-style" placeholder="Link tải code mẫu..." />
                    </div>
                  </div>
                </div>

                <!-- Learning detail fields (Objective, Key Points, Instructions) -->
                <div class="mt-3">
                  <div class="form-group">
                    <label style="font-size: 12px;">Mục tiêu bài học</label>
                    <input v-model="lesson.objective" type="text" class="admin-input-style" placeholder="Mô tả mục tiêu của bài học này..." />
                  </div>
                  <div class="grid-2 mt-2">
                    <div class="form-group">
                      <label style="font-size: 12px;">Nội dung cốt lõi (Ngăn cách bởi dấu phẩy)</label>
                      <input 
                        :value="lesson.keyPoints ? lesson.keyPoints.join(', ') : ''" 
                        @input="lesson.keyPoints = $event.target.value.split(',').map(x => x.trim()).filter(Boolean)" 
                        type="text" 
                        class="admin-input-style" 
                        placeholder="Nội dung 1, Nội dung 2, Nội dung 3..." 
                      />
                    </div>
                    <div class="form-group">
                      <label style="font-size: 12px;">Hướng dẫn thực hành</label>
                      <input v-model="lesson.instructions" type="text" class="admin-input-style" placeholder="Các tác vụ thực hành cần làm..." />
                    </div>
                  </div>
                </div>

              </div>

              <button type="button" @click="addLesson(cIdx)" class="btn btn-outline btn-xs mt-3">+ Thêm bài học mới</button>
            </div>

          </div>
          
          <button type="button" @click="addChapter" class="btn btn-secondary btn-sm mt-2">+ Thêm chương mới</button>
        </div>

        <div class="modal-actions mt-8" style="border-top: 1px solid var(--border-color); padding-top: 20px;">
          <button type="button" @click="curriculumModalOpen = false" class="btn btn-secondary btn-sm">Hủy</button>
          <button type="button" @click="saveCurriculum" class="btn btn-primary btn-sm">Lưu giáo trình khóa học</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useCourseStore } from '@/stores/courses';

const courseStore = useCourseStore();

const courses = computed(() => courseStore.courses);

const courseSearch = ref('');
const courseFilterCategory = ref('all');

const filteredCourses = computed(() => {
  return courses.value.filter(c => {
    const matchesSearch = c.title.toLowerCase().includes(courseSearch.value.toLowerCase()) || 
                          c.description.toLowerCase().includes(courseSearch.value.toLowerCase());
    const matchesCat = courseFilterCategory.value === 'all' || c.category === courseFilterCategory.value;
    return matchesSearch && matchesCat;
  });
});

// CRUD Course Modal States
const courseModalOpen = ref(false);
const isEditingCourse = ref(false);
const editingCourseId = ref(null);
const courseForm = ref({
  title: '',
  handle: '',
  category: 'ky-nang-ai',
  image: '',
  price: 0,
  originalPrice: 0,
  duration: '12 tuần',
  level: 'Trung cấp',
  description: ''
});

const openAddCourseModal = () => {
  isEditingCourse.value = false;
  courseForm.value = {
    title: '',
    handle: '',
    category: 'ky-nang-ai',
    image: '/images/default.jpg',
    price: 9800000,
    originalPrice: 12000000,
    duration: '12 tuần',
    level: 'Trung cấp',
    description: ''
  };
  courseModalOpen.value = true;
};

const editCourseDetails = (c) => {
  isEditingCourse.value = true;
  editingCourseId.value = c.id;
  courseForm.value = {
    title: c.title,
    handle: c.handle,
    category: c.category,
    image: c.image,
    price: c.price,
    originalPrice: c.originalPrice,
    duration: c.duration,
    level: c.level,
    description: c.description
  };
  courseModalOpen.value = true;
};

const saveCourse = async () => {
  try {
    if (isEditingCourse.value) {
      await courseStore.updateAdminCourse(editingCourseId.value, courseForm.value);
      alert('Cập nhật khóa học thành công!');
    } else {
      if (courses.value.some(c => c.handle === courseForm.value.handle)) {
        alert('Đường dẫn tĩnh (Slug) này đã tồn tại!');
        return;
      }
      await courseStore.addAdminCourse(courseForm.value);
      alert('Thêm khóa học mới thành công!');
    }
    courseModalOpen.value = false;
  } catch (err) {
    alert(err.message || 'Không thể lưu khóa học.');
  }
};

const deleteCourse = async (courseId) => {
  if (confirm('Bạn có chắc muốn xóa khóa học này khỏi danh mục?')) {
    try {
      await courseStore.deleteAdminCourse(courseId);
      alert('Đã xóa khóa học thành công.');
    } catch (err) {
      alert(err.message || 'Không thể xóa khóa học.');
    }
  }
};

// Curriculum Builder State & Methods
const curriculumModalOpen = ref(false);
const selectedCourseForCurriculum = ref(null);
const curriculumForm = ref([]);

const getDefaultCurriculum = (handle) => {
  if (handle === 'chatgpt-work-automation') {
    return [
      {
        name: 'Tổng quan & Thiết lập trợ lý OpenAI',
        lessons: [
          { id: 'chat-1', type: 'video', title: 'Bài 1: Giới thiệu hệ sinh thái OpenAI và ChatGPT', videoUrl: 'https://www.w3schools.com/html/mov_bbb.mp4', objective: 'Tổng quan về cuộc cách mạng AI và cơ chế hoạt động của ChatGPT.', keyPoints: ['Hiểu cách học máy sinh text', 'Cách tạo tài khoản OpenAI Plus', 'Thiết lập cấu hình giao diện tối ưu'], instructions: 'Mở ứng dụng ChatGPT và thiết lập các thông số ban đầu.' },
          { id: 'chat-2', type: 'document', title: 'Bài 2: Tài liệu cấu trúc thiết kế Prompt mẫu', docUrl: '#', srcCodeUrl: '#', objective: 'Nắm vững các mẫu prompt phổ biến áp dụng cho công việc văn phòng.', keyPoints: ['Mô hình prompt ROLE-TASK-CONTEXT', 'Tối ưu hóa phản hồi của AI', 'Cách sửa đổi câu trả lời theo tone giọng'], instructions: 'Tải PDF tài liệu và viết thử 3 prompt đầu tiên theo hướng dẫn.' }
        ]
      },
      {
        name: 'Tự động hóa tác vụ văn phòng chuyên sâu',
        lessons: [
          { id: 'chat-3', type: 'zoom', title: 'Bài 3: Thực hành Viết Prompt nâng cao (Live qua Zoom)', zoomTime: 'Thứ Ba tuần tới lúc 19:30', meetingId: '864 2291 9900', passcode: 'OPENAI10X', zoomLink: 'https://zoom.us', objective: 'Tham gia tương tác trực tiếp giải đề bài thực tế từ giảng viên.', keyPoints: ['Sửa lỗi prompt phổ biến', 'Chữa bài tập thực hành của học viên', 'Q&A trực tiếp cùng giảng viên'], instructions: 'Chuẩn bị micro và bài tập chương 1 để trao đổi trực tiếp.' },
          { id: 'chat-4', type: 'video', title: 'Bài 4: Tự động soạn thảo văn bản, email, báo cáo', videoUrl: 'https://www.w3schools.com/html/mov_bbb.mp4', objective: 'Học cách soạn thảo nhanh các loại văn bản công sở chỉ trong 2 phút.', keyPoints: ['Công thức viết email phản hồi khách hàng tự động', 'Tạo dàn ý báo cáo doanh số chi tiết', 'Tối ưu hóa cấu trúc bài viết chuẩn SEO'], instructions: 'Chạy thử công thức viết email trên ChatGPT.' }
        ]
      }
    ];
  } else if (handle === 'ai-center-of-excellence') {
    return [
      {
        name: 'Chiến lược quản trị AI trong tổ chức',
        lessons: [
          { id: 'coe-1', type: 'video', title: 'Bài 1: Tại sao doanh nghiệp cần xây dựng AI Center of Excellence', videoUrl: 'https://www.w3schools.com/html/mov_bbb.mp4', objective: 'Hiểu về cấu trúc ban điều hành AI chuyên trách.', keyPoints: ['Mô hình AI COE hiện đại', 'Vai trò của CXO trong chỉ đạo chuyển đổi số', 'Các rủi ro bảo mật dữ liệu'], instructions: 'Xem hết video bài giảng và thảo luận cùng đội nhóm.' },
          { id: 'coe-2', type: 'zoom', title: 'Bài 2: Thiết lập quy chuẩn sử dụng AI an toàn (Live qua Zoom)', zoomTime: 'Thứ Năm tuần này lúc 20:00', meetingId: '822 5506 1234', passcode: 'AICOE2026', zoomLink: 'https://zoom.us', objective: 'Quy chế sử dụng AI để không rò rỉ dữ liệu mật công ty.', keyPoints: ['Các quy định an toàn thông tin', 'Thiết lập mạng nội bộ sử dụng API', 'Kiểm tra tài khoản dùng chung'], instructions: 'Đọc kỹ tài liệu nội bộ trước khi tham gia buổi Zoom.' }
        ]
      }
    ];
  } else {
    return [
      {
        name: 'Giới thiệu & Tổng quan',
        lessons: [
          { id: 'def-1', type: 'video', title: 'Bài 1: Giới thiệu tổng quan và Lộ trình học tập', videoUrl: 'https://www.w3schools.com/html/mov_bbb.mp4', objective: 'Tìm hiểu tổng quan lộ trình và chuẩn bị môi trường thực hành.', keyPoints: ['Hiểu rõ mục tiêu đầu ra', 'Cài đặt công cụ cần thiết', 'Tài liệu hướng dẫn bắt đầu'], instructions: 'Xem video và ghi chú lại lộ trình học tập của bạn.' },
          { id: 'def-2', type: 'document', title: 'Bài 2: Tài liệu giáo trình học tập', docUrl: '#', srcCodeUrl: '#', objective: 'Nắm bắt lý thuyết nền tảng.', keyPoints: ['Tóm tắt kiến thức cốt lõi', 'Sơ đồ tư duy bài học', 'Danh sách tài nguyên tham khảo'], instructions: 'Tải slide bài học để đọc kỹ trước khi thực hành.' }
        ]
      },
      {
        name: 'Kiến thức cốt lõi & Thực hành',
        lessons: [
          { id: 'def-3', type: 'zoom', title: 'Bài 3: Hướng dẫn thực hành trực tuyến (Live qua Zoom)', zoomTime: 'Thứ Ba tuần tới lúc 19:30', meetingId: '888 777 9999', passcode: 'ACC2026', zoomLink: 'https://zoom.us', objective: 'Tương tác trực tiếp chữa bài tập và giải đáp thắc mắc cùng Mentor.', keyPoints: ['Giải đáp câu hỏi thực hành', 'Chia sẻ kinh nghiệm thực chiến', 'Mentor chữa bài trực tiếp'], instructions: 'Đăng nhập vào Zoom đúng giờ và chuẩn bị sẵn câu hỏi.' },
          { id: 'def-4', type: 'video', title: 'Bài 4: Bài tập ứng dụng thực tế', videoUrl: 'https://www.w3schools.com/html/mov_bbb.mp4', objective: 'Áp dụng kiến thức để giải quyết bài toán thực tế.', keyPoints: ['Các bước triển khai chi tiết', 'Tối ưu hóa kết quả đầu ra', 'Kiểm thử và đánh giá'], instructions: 'Thực hành lại các bước được hướng dẫn trong video.' }
        ]
      }
    ];
  }
};

const openCurriculumModal = (c) => {
  selectedCourseForCurriculum.value = c;
  if (c.curriculumData) {
    try {
      curriculumForm.value = JSON.parse(c.curriculumData);
    } catch (e) {
      console.error("Failed to parse curriculum JSON, loading defaults", e);
      curriculumForm.value = getDefaultCurriculum(c.handle);
    }
  } else {
    curriculumForm.value = getDefaultCurriculum(c.handle);
  }
  curriculumModalOpen.value = true;
};

const addChapter = () => {
  curriculumForm.value.push({
    name: '',
    expanded: true,
    lessons: []
  });
};

const removeChapter = (cIdx) => {
  curriculumForm.value.splice(cIdx, 1);
};

const addLesson = (cIdx) => {
  curriculumForm.value[cIdx].lessons.push({
    id: 'lesson-' + Date.now(),
    type: 'video',
    title: '',
    videoUrl: 'https://www.w3schools.com/html/mov_bbb.mp4',
    zoomTime: '',
    zoomLink: '',
    meetingId: '',
    passcode: '',
    docUrl: '',
    srcCodeUrl: '',
    objective: '',
    keyPoints: [],
    instructions: ''
  });
};

const removeLesson = (cIdx, lIdx) => {
  curriculumForm.value[cIdx].lessons.splice(lIdx, 1);
};

const saveCurriculum = async () => {
  try {
    const jsonString = JSON.stringify(curriculumForm.value);
    await courseStore.updateAdminCourse(selectedCourseForCurriculum.value.id, {
      curriculumData: jsonString
    });
    alert('Lưu giáo trình khóa học thành công!');
    curriculumModalOpen.value = false;
  } catch (err) {
    alert(err.message || 'Không thể lưu giáo trình.');
  }
};

// Helpers
const formatPrice = (value) => {
  if (value === undefined || value === null) return '0đ';
  return value.toLocaleString('vi-VN') + 'đ';
};

const translateCategory = (cat) => {
  switch (cat) {
    case 'ky-nang-ai': return 'Kỹ năng AI';
    case 'ky-nang-mem': return 'Kỹ năng mềm';
    case 'ky-nang-chuyen-mon': return 'Kỹ năng chuyên môn';
    case 'bundles': return 'Combo / Gói';
    default: return cat;
  }
};
</script>
