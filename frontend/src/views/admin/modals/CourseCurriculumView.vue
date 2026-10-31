<template>
  <div class="admin-page-card" style="background: #ffffff; color: #0f172a; border-radius: 16px; padding: 28px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); border: 1px solid #e2e8f0;">
    <div class="flex-between pb-4 mb-4" style="border-bottom: 1px solid #e2e8f0;">
      <div style="display: flex; align-items: center; gap: 12px;">
        <button type="button" @click="$emit('cancel')" class="btn btn-secondary btn-sm" style="padding: 8px 16px; font-weight: 600;">
          ← Quay lại danh sách
        </button>
        <div>
          <h3 style="margin: 0; color: #0f172a; font-size: 20px; font-weight: 800;">
            Quản lý giáo trình & tài liệu: {{ course?.title }}
          </h3>
          <p style="margin: 4px 0 0; color: #64748b; font-size: 13px;">
            Thiết lập các chương học, bài giảng video, phòng học Live Zoom và slide tài liệu đính kèm.
          </p>
        </div>
      </div>
      <button type="button" @click="$emit('cancel')" class="btn btn-secondary btn-sm">Quay lại</button>
    </div>

    <!-- Chapter list builder -->
    <div class="chapters-builder mt-4">
      <div v-for="(chapter, cIdx) in curriculumForm" :key="cIdx" class="chapter-build-card mb-6" style="padding: 20px; border: 1px solid #cbd5e1; background: #f8fafc; border-radius: 12px;">
        <div class="chapter-build-header flex-between" style="gap: 12px;">
          <div style="flex: 1; display: flex; align-items: center; gap: 12px;">
            <span style="font-weight: 700; color: #0284c7; min-width: 90px; font-size: 15px;">Chương {{ cIdx + 1 }}:</span>
            <input v-model="chapter.name" type="text" class="admin-input-style" placeholder="Tên chương học..." required style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1; font-weight: 600;" />
          </div>
          <button type="button" @click="removeChapter(cIdx)" class="btn btn-sm btn-danger" style="padding: 6px 14px; background: #ef4444; color: white; border: none; border-radius: 6px;">Xóa chương</button>
        </div>

        <!-- Lessons list builder -->
        <div class="lessons-builder mt-4" style="padding-left: 20px; border-left: 3px solid #cbd5e1;">
          <div v-for="(lesson, lIdx) in chapter.lessons" :key="lIdx" class="lesson-build-card mt-3" style="padding: 16px; background: #ffffff; border-radius: 8px; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
            <div class="flex-between mb-2" style="gap: 12px;">
              <div style="font-weight: 700; font-size: 14px; color: #1e293b;">Bài học {{ lIdx + 1 }}:</div>
              <button type="button" @click="removeLesson(cIdx, lIdx)" class="btn btn-xs btn-danger" style="font-size: 12px; background: #fee2e2; color: #dc2626; border: 1px solid #fca5a5; padding: 4px 10px; border-radius: 4px;">Xóa bài học</button>
            </div>

            <div class="grid-2 mt-2">
              <div class="form-group">
                <label style="font-size: 12px; color: #475569; font-weight: 600;">Tiêu đề bài học</label>
                <input v-model="lesson.title" type="text" class="admin-input-style" placeholder="Tên bài giảng..." required style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
              </div>
              <div class="form-group">
                <label style="font-size: 12px; color: #475569; font-weight: 600;">Loại bài học</label>
                <select v-model="lesson.type" class="admin-input-style" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;">
                  <option value="video">Video bài giảng</option>
                  <option value="zoom">Lớp học Live Zoom</option>
                  <option value="document">Slide & Tài liệu</option>
                </select>
              </div>
            </div>

            <!-- Custom inputs based on lesson type -->
            <div class="type-custom-fields mt-3" style="padding: 12px; background: #f1f5f9; border-radius: 6px; border: 1px solid #e2e8f0;">
              <!-- Video fields -->
              <div v-if="lesson.type === 'video'" class="form-group">
                <label style="font-size: 12px; color: #475569; font-weight: 600;">Đường dẫn Video bài giảng (MP4/HLS Link)</label>
                <input v-model="lesson.videoUrl" type="text" class="admin-input-style" placeholder="https://example.com/lecture.mp4" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
              </div>

              <!-- Zoom fields -->
              <div v-if="lesson.type === 'zoom'">
                <div class="grid-2">
                  <div class="form-group">
                    <label style="font-size: 12px; color: #475569; font-weight: 600;">Lịch học Zoom</label>
                    <input v-model="lesson.zoomTime" type="text" class="admin-input-style" placeholder="Thứ Ba tuần tới lúc 19:30" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
                  </div>
                  <div class="form-group">
                    <label style="font-size: 12px; color: #475569; font-weight: 600;">Zoom Link trực tiếp</label>
                    <input v-model="lesson.zoomLink" type="text" class="admin-input-style" placeholder="https://zoom.us/j/..." style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
                  </div>
                </div>
                <div class="grid-2 mt-2">
                  <div class="form-group">
                    <label style="font-size: 12px; color: #475569; font-weight: 600;">Meeting ID</label>
                    <input v-model="lesson.meetingId" type="text" class="admin-input-style" placeholder="888 999 6688" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
                  </div>
                  <div class="form-group">
                    <label style="font-size: 12px; color: #475569; font-weight: 600;">Mật mã (Passcode)</label>
                    <input v-model="lesson.passcode" type="text" class="admin-input-style" placeholder="ACC2026" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
                  </div>
                </div>
              </div>

              <!-- Document fields -->
              <div v-if="lesson.type === 'document'" class="grid-2">
                <div class="form-group">
                  <label style="font-size: 12px; color: #475569; font-weight: 600;">Link tải Slide bài giảng (PDF)</label>
                  <input v-model="lesson.docUrl" type="text" class="admin-input-style" placeholder="Link tải slide..." style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
                </div>
                <div class="form-group">
                  <label style="font-size: 12px; color: #475569; font-weight: 600;">Link tải Source code / Prompt mẫu</label>
                  <input v-model="lesson.srcCodeUrl" type="text" class="admin-input-style" placeholder="Link tải code mẫu..." style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
                </div>
              </div>
            </div>

            <!-- Learning detail fields -->
            <div class="mt-3">
              <div class="form-group">
                <label style="font-size: 12px; color: #475569; font-weight: 600;">Mục tiêu bài học</label>
                <input v-model="lesson.objective" type="text" class="admin-input-style" placeholder="Mô tả mục tiêu của bài học này..." style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
              </div>
              <div class="grid-2 mt-2">
                <div class="form-group">
                  <label style="font-size: 12px; color: #475569; font-weight: 600;">Nội dung cốt lõi (Ngăn cách bởi dấu phẩy)</label>
                  <input 
                    :value="lesson.keyPoints ? lesson.keyPoints.join(', ') : ''" 
                    @input="lesson.keyPoints = $event.target.value.split(',').map(x => x.trim()).filter(Boolean)" 
                    type="text" 
                    class="admin-input-style" 
                    placeholder="Nội dung 1, Nội dung 2, Nội dung 3..." 
                    style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;"
                  />
                </div>
                <div class="form-group">
                  <label style="font-size: 12px; color: #475569; font-weight: 600;">Hướng dẫn thực hành</label>
                  <input v-model="lesson.instructions" type="text" class="admin-input-style" placeholder="Các tác vụ thực hành cần làm..." style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
                </div>
              </div>
            </div>
          </div>

          <button type="button" @click="addLesson(cIdx)" class="btn btn-outline btn-xs mt-3" style="font-weight: 600;">+ Thêm bài học mới</button>
        </div>
      </div>
      
      <button type="button" @click="addChapter" class="btn btn-secondary btn-sm mt-2" style="font-weight: 600;">+ Thêm chương mới</button>
    </div>

    <div class="flex-between mt-8 pt-4" style="border-top: 1px solid #e2e8f0;">
      <button type="button" @click="$emit('cancel')" class="btn btn-secondary btn-sm" style="padding: 10px 24px;">Hủy bỏ</button>
      <button type="button" @click="saveCurriculum" class="btn btn-primary btn-sm" style="padding: 10px 32px; font-weight: 700;">Lưu giáo trình khóa học</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useCourseStore } from '@/stores/courses';

const props = defineProps({
  course: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['cancel', 'saved']);
const courseStore = useCourseStore();

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

onMounted(() => {
  const c = props.course;
  if (c.curriculumData) {
    try {
      curriculumForm.value = JSON.parse(c.curriculumData);
    } catch (e) {
      curriculumForm.value = getDefaultCurriculum(c.handle);
    }
  } else {
    curriculumForm.value = getDefaultCurriculum(c.handle);
  }
});

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
    id: 'les-' + Date.now().toString(36),
    title: '',
    type: 'video',
    videoUrl: '',
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
    const payload = {
      curriculumData: JSON.stringify(curriculumForm.value)
    };
    await courseStore.updateAdminCourse(props.course.id, payload);
    props.course.curriculumData = payload.curriculumData;
    courseStore.showToast('Lưu giáo trình khóa học thành công!', 'success');
    emit('saved');
  } catch (err) {
    courseStore.showToast(err.message || 'Lỗi khi lưu giáo trình.', 'error');
  }
};
</script>

