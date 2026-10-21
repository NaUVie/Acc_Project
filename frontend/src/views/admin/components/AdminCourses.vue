<template>
  <div class="tab-content animate-fade-in">
    <!-- VIEW 1: LIST TABLE -->
    <div v-if="activeView === 'list'">
      <div class="content-header flex-between">
        <div>
          <h2>Quản lý Danh mục Khóa học</h2>
          <p>Danh sách và thông tin chi tiết các khóa học hiển thị trên website.</p>
        </div>
        <button @click="openAddCourseModal" class="btn btn-primary btn-sm">+ Thêm khóa học mới</button>
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
          <option v-for="cat in categories" :key="cat.slug" :value="cat.slug">{{ cat.name }}</option>
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
            <tr v-for="c in paginatedCourses" :key="c.id">
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
                  <button @click="openCurriculumModal(c)" class="btn-action edit" title="Quản lý giáo trình & bài giảng">📚</button>
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

      <!-- Pagination Component -->
      <Pagination 
        :currentPage="currentPage" 
        :totalItems="filteredCourses.length" 
        :pageSize="pageSize" 
        @update:currentPage="currentPage = $event"
      />
    </div>

    <!-- VIEW 2: COURSE ADD/EDIT FORM (TRANG RIÊNG) -->
    <div v-else-if="activeView === 'course_form'" class="admin-page-card" style="background: #ffffff; color: #0f172a; border-radius: 16px; padding: 28px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); border: 1px solid #e2e8f0;">
      <div class="flex-between pb-4 mb-4" style="border-bottom: 1px solid #e2e8f0;">
        <div style="display: flex; align-items: center; gap: 12px;">
          <button type="button" @click="activeView = 'list'" class="btn btn-secondary btn-sm" style="padding: 8px 16px; font-weight: 600;">
            ← Quay lại danh sách
          </button>
          <h3 style="margin: 0; color: #0f172a; font-size: 20px; font-weight: 800;">
            {{ isEditingCourse ? 'Chỉnh sửa thông tin khóa học' : 'Thêm khóa học mới' }}
          </h3>
        </div>
        <button type="button" @click="activeView = 'list'" class="btn btn-secondary btn-sm">Hủy</button>
      </div>

      <form @submit.prevent="saveCourse">
        <div class="form-group">
          <label style="color: #1e293b; font-weight: 600;">Tên khóa học</label>
          <input v-model="courseForm.title" @input="onTitleInput" type="text" required class="admin-input-style" placeholder="Ví dụ: ChatGPT thực chiến nâng cao" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
        </div>

        <div class="form-group mt-3">
          <label style="color: #1e293b; font-weight: 600;">Đường dẫn tĩnh (Slug / Handle - Tự động tạo)</label>
          <input v-model="courseForm.handle" type="text" required class="admin-input-style" placeholder="chatgpt-nang-cao" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
        </div>

        <div class="grid-2 mt-3">
          <div class="form-group">
            <label style="color: #1e293b; font-weight: 600;">Chuyên mục</label>
            <select v-model="courseForm.category" class="admin-input-style" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;">
              <option v-for="cat in categories" :key="cat.slug" :value="cat.slug">{{ cat.name }} ({{ cat.slug }})</option>
              <option value="custom">+ Nhập chuyên mục tùy chỉnh mới...</option>
            </select>
            <div v-if="courseForm.category === 'custom'" class="mt-2">
              <input v-model="customCategorySlug" type="text" placeholder="Nhập mã slug chuyên mục mới (ví dụ: marketing-ai)" class="admin-input-style" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
            </div>
          </div>
          <div class="form-group">
            <label style="color: #1e293b; font-weight: 600;">Chương trình đào tạo mẹ (Program)</label>
            <select v-model="courseForm.programId" class="admin-input-style" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;">
              <option :value="null">-- Không thuộc chương trình --</option>
              <option v-for="p in programs" :key="p.id" :value="p.id">{{ p.title }}</option>
            </select>
          </div>
        </div>

        <div class="grid-2 mt-3">
          <div class="form-group">
            <label style="color: #1e293b; font-weight: 600;">Ảnh Thumbnail / Danh sách (Card)</label>
            <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
              <input v-model="courseForm.image" type="text" required class="admin-input-style" placeholder="/images/default.jpg hoặc URL Cloudinary" style="flex: 1; min-width: 200px; background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
              <label class="btn btn-primary btn-sm" style="padding: 10px 14px; cursor: pointer; display: inline-flex; align-items: center; gap: 6px; white-space: nowrap; margin: 0; font-weight: 600;">
                <span>Tải ảnh</span>
                <input type="file" accept="image/*" @change="uploadCourseImage" style="display: none;" />
              </label>
            </div>
            <div v-if="uploadingCourseImage" style="font-size: 12px; color: #0284c7; margin-top: 4px; font-weight: 600;">
              Đang tải ảnh thumbnail lên Cloudinary...
            </div>
            <div v-if="courseForm.image" class="mt-2">
              <img :src="courseForm.image" alt="Thumbnail Preview" style="max-height: 100px; border-radius: 8px; border: 1px solid #cbd5e1; object-fit: contain; background: #ffffff;" />
            </div>
          </div>

          <div class="form-group">
            <label style="color: #1e293b; font-weight: 600;">Ảnh Bìa hiển thị trang chi tiết (Cover Image)</label>
            <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
              <input v-model="courseForm.coverImage" type="text" class="admin-input-style" placeholder="Để trống sẽ dùng chung ảnh Thumbnail" style="flex: 1; min-width: 200px; background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
              <label class="btn btn-primary btn-sm" style="padding: 10px 14px; cursor: pointer; display: inline-flex; align-items: center; gap: 6px; white-space: nowrap; margin: 0; font-weight: 600; background: #475569;">
                <span>Tải ảnh</span>
                <input type="file" accept="image/*" @change="uploadCourseCoverImage" style="display: none;" />
              </label>
            </div>
            <div v-if="uploadingCoverImage" style="font-size: 12px; color: #0284c7; margin-top: 4px; font-weight: 600;">
              Đang tải ảnh bìa chi tiết lên Cloudinary...
            </div>
            <div v-if="courseForm.coverImage" class="mt-2">
              <img :src="courseForm.coverImage" alt="Cover Preview" style="max-height: 100px; border-radius: 8px; border: 1px solid #cbd5e1; object-fit: contain; background: #ffffff;" />
            </div>
          </div>
        </div>

        <div class="grid-2 mt-3">
          <div class="form-group">
            <label style="color: #1e293b; font-weight: 600;">Giá bán (VNĐ)</label>
            <input v-model.number="courseForm.price" type="number" required class="admin-input-style" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1; font-weight: bold;" />
          </div>
          <div class="form-group">
            <label style="color: #1e293b; font-weight: 600;">Giá gốc niêm yết (VNĐ)</label>
            <input v-model.number="courseForm.originalPrice" type="number" required class="admin-input-style" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
          </div>
        </div>

        <div class="grid-2 mt-3">
          <div class="form-group">
            <label style="color: #1e293b; font-weight: 600;">Thời lượng</label>
            <input v-model="courseForm.duration" type="text" required class="admin-input-style" placeholder="12 tuần, 24 giờ học..." style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
          </div>
          <div class="form-group">
            <label style="color: #1e293b; font-weight: 600;">Trình độ</label>
            <input v-model="courseForm.level" type="text" required class="admin-input-style" placeholder="Cơ bản, Trung cấp, Nâng cao" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;" />
          </div>
        </div>

        <div class="form-group mt-3">
          <label style="color: #1e293b; font-weight: 600;">Mô tả chi tiết & Tổng quan khóa học (Soạn thảo văn bản)</label>
          <RichTextEditor v-model="courseForm.description" placeholder="Soạn thảo mô tả chi tiết, tổng quan nội dung khóa học..." />
        </div>

        <div class="form-group mt-3">
          <label style="color: #1e293b; font-weight: 600;">Lộ trình khóa học tùy chỉnh (Giai đoạn 1, 2, 3...)</label>
          <RichTextEditor v-model="courseForm.customRoadmap" placeholder="Ví dụ:&#10;Giai đoạn 1 – AI Foundation | 2 ngày&#10;Xây dựng nền tảng sử dụng AI...&#10;Giai đoạn 2 – AI Agent Operating System | 2 ngày&#10;Thực hành xây dựng ứng dụng..." />
          <small class="text-muted" style="display: block; margin-top: 4px;">Soạn thảo chi tiết các giai đoạn lộ trình học (Nếu để trống sẽ hiển thị bài giảng từ mục Giáo trình).</small>
        </div>

        <div class="form-group mt-3">
          <label style="color: #1e293b; font-weight: 600;">Đội ngũ Giảng viên / Người thực hiện khóa học</label>
          <div style="display: flex; flex-direction: column; gap: 8px;">
            <select v-model="selectedLecturerToAdd" @change="addLecturerToCourse" class="admin-input-style" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;">
              <option value="">-- Chọn Giảng viên để thêm vào khóa học --</option>
              <option v-for="l in lecturers" :key="l.id" :value="l.id">{{ l.name }} ({{ l.title }})</option>
            </select>
            <!-- Selected Lecturers Tags -->
            <div v-if="selectedLecturersList.length > 0" style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 4px;">
              <span v-for="lec in selectedLecturersList" :key="lec.id" style="background: #e0f2fe; color: #0369a1; border: 1px solid #bae6fd; padding: 6px 12px; border-radius: 20px; font-size: 13px; font-weight: 600; display: inline-flex; align-items: center; gap: 8px;">
                <span>{{ lec.name }} - {{ lec.title }}</span>
                <button type="button" @click="removeLecturerFromCourse(lec.id)" style="background: none; border: none; color: #ef4444; font-weight: 800; cursor: pointer; padding: 0 4px; font-size: 14px;">✕</button>
              </span>
            </div>
          </div>
        </div>

        <div class="form-group mt-3">
          <label style="color: #1e293b; font-weight: 600;">Bạn sẽ đạt được gì sau khóa học này? (Mỗi mục 1 dòng)</label>
          <textarea v-model="courseForm.outcomes" rows="4" class="admin-input-style" placeholder="Ví dụ:&#10;Rèn luyện tư duy giao tiếp và thuyết phục hiệu quả trong công việc&#10;Làm chủ phương pháp quản lý thời gian và giải quyết vấn đề linh hoạt&#10;Nâng cao khả năng làm việc nhóm và đàm phán chuyên nghiệp" style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;"></textarea>
          <small class="text-muted" style="display: block; margin-top: 4px;">Nhập từng kết quả đạt được trên một dòng riêng biệt.</small>
        </div>

        <div class="form-group mt-3">
          <label style="color: #1e293b; font-weight: 600;">Yêu cầu & Đối tượng phù hợp (Mỗi mục 1 dòng)</label>
          <textarea v-model="courseForm.requirements" rows="4" class="admin-input-style" placeholder="Ví dụ:&#10;Dành cho Quản lý, Chuyên viên, Freelancer và bất kỳ ai muốn nâng cao năng lực thời AI.&#10;Không yêu cầu kiến thức lập trình phức tạp – bài giảng cầm tay chỉ việc.&#10;Chỉ cần máy tính kết nối Internet để tham gia học trực tuyến." style="background: #ffffff; color: #0f172a; border: 1px solid #cbd5e1;"></textarea>
          <small class="text-muted" style="display: block; margin-top: 4px;">Nhập từng yêu cầu hoặc đối tượng trên một dòng riêng biệt.</small>
        </div>

        <div class="flex-between mt-6 pt-4" style="border-top: 1px solid #e2e8f0;">
          <button type="button" @click="activeView = 'list'" class="btn btn-secondary btn-sm" style="padding: 10px 24px;">Hủy bỏ</button>
          <button type="submit" class="btn btn-primary btn-sm" style="padding: 10px 32px; font-weight: 700;">Lưu thông tin khóa học</button>
        </div>
      </form>
    </div>

    <!-- VIEW 3: CURRICULUM FORM (TRANG RIÊNG) -->
    <div v-else-if="activeView === 'curriculum_form'" class="admin-page-card" style="background: #ffffff; color: #0f172a; border-radius: 16px; padding: 28px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); border: 1px solid #e2e8f0;">
      <div class="flex-between pb-4 mb-4" style="border-bottom: 1px solid #e2e8f0;">
        <div style="display: flex; align-items: center; gap: 12px;">
          <button type="button" @click="activeView = 'list'" class="btn btn-secondary btn-sm" style="padding: 8px 16px; font-weight: 600;">
            ← Quay lại danh sách
          </button>
          <div>
            <h3 style="margin: 0; color: #0f172a; font-size: 20px; font-weight: 800;">
              Quản lý giáo trình & tài liệu: {{ selectedCourseForCurriculum?.title }}
            </h3>
            <p style="margin: 4px 0 0; color: #64748b; font-size: 13px;">
              Thiết lập các chương học, bài giảng video, phòng học Live Zoom và slide tài liệu đính kèm.
            </p>
          </div>
        </div>
        <button type="button" @click="activeView = 'list'" class="btn btn-secondary btn-sm">Quay lại</button>
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
        <button type="button" @click="activeView = 'list'" class="btn btn-secondary btn-sm" style="padding: 10px 24px;">Hủy bỏ</button>
        <button type="button" @click="saveCurriculum" class="btn btn-primary btn-sm" style="padding: 10px 32px; font-weight: 700;">Lưu giáo trình khóa học</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useCourseStore } from '@/stores/courses';
import { slugify } from '@/utils/slugify';
import { formatImageUrl } from '@/utils/imageHelper';
import Pagination from '@/components/Pagination.vue';
import RichTextEditor from '@/components/RichTextEditor.vue';

const courseStore = useCourseStore();

const courses = computed(() => courseStore.courses);
const categories = computed(() => courseStore.categories || []);
const programs = computed(() => courseStore.programs);
const customCategorySlug = ref('');

const currentPage = ref(1);
const pageSize = ref(8);

const onTitleInput = () => {
  if (!isEditingCourse.value || !courseForm.value.handle) {
    courseForm.value.handle = slugify(courseForm.value.title);
  }
};

const lecturers = computed(() => courseStore.lecturers || []);
const selectedLecturerToAdd = ref('');

const selectedLecturersList = computed(() => {
  if (!courseForm.value.lecturerIds) return [];
  const ids = courseForm.value.lecturerIds.split(',').map(s => s.trim()).filter(Boolean);
  return ids.map(id => lecturers.value.find(l => String(l.id) === String(id))).filter(Boolean);
});

const addLecturerToCourse = () => {
  if (!selectedLecturerToAdd.value) return;
  const currentIds = courseForm.value.lecturerIds ? courseForm.value.lecturerIds.split(',').map(s => s.trim()).filter(Boolean) : [];
  if (!currentIds.includes(String(selectedLecturerToAdd.value))) {
    currentIds.push(String(selectedLecturerToAdd.value));
    courseForm.value.lecturerIds = currentIds.join(',');
  }
  selectedLecturerToAdd.value = '';
};

const removeLecturerFromCourse = (id) => {
  const currentIds = courseForm.value.lecturerIds ? courseForm.value.lecturerIds.split(',').map(s => s.trim()).filter(Boolean) : [];
  const updated = currentIds.filter(i => String(i) !== String(id));
  courseForm.value.lecturerIds = updated.join(',');
};

onMounted(() => {
  courseStore.fetchCourses();
  if (courseStore.categories.length === 0) {
    courseStore.fetchCategories();
  }
  if (courseStore.programs.length === 0) {
    courseStore.fetchPrograms();
  }
  if (courseStore.lecturers.length === 0) {
    courseStore.fetchLecturers();
  }
});

const courseSearch = ref('');
const courseFilterCategory = ref('all');

watch([courseSearch, courseFilterCategory], () => {
  currentPage.value = 1;
});

const filteredCourses = computed(() => {
  const query = (courseSearch.value || '').toLowerCase().trim();
  return (courses.value || []).filter(c => {
    const title = (c.title || '').toLowerCase();
    const desc = (c.description || '').toLowerCase();
    const matchesSearch = !query || title.includes(query) || desc.includes(query);
    const matchesCat = courseFilterCategory.value === 'all' || c.category === courseFilterCategory.value;
    return matchesSearch && matchesCat;
  });
});

const paginatedCourses = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  return filteredCourses.value.slice(start, start + pageSize.value);
});

// CRUD & Navigation States ('list' | 'course_form' | 'curriculum_form')
const activeView = ref('list');
const isEditingCourse = ref(false);
const editingCourseId = ref(null);
const uploadingCourseImage = ref(false);
const uploadingCoverImage = ref(false);

const uploadCourseImage = async (e) => {
  const file = e.target.files[0];
  if (!file) return;
  uploadingCourseImage.value = true;
  try {
    const url = await courseStore.uploadImage(file);
    courseForm.value.image = url;
    courseStore.showToast('Tải ảnh thumbnail thành công!', 'success');
  } catch (err) {
    courseStore.showToast('Lỗi khi tải ảnh lên Cloudinary: ' + err.message, 'error');
  } finally {
    uploadingCourseImage.value = false;
  }
};

const uploadCourseCoverImage = async (e) => {
  const file = e.target.files[0];
  if (!file) return;
  uploadingCoverImage.value = true;
  try {
    const url = await courseStore.uploadImage(file);
    courseForm.value.coverImage = url;
    courseStore.showToast('Tải ảnh bìa chi tiết thành công!', 'success');
  } catch (err) {
    courseStore.showToast('Lỗi khi tải ảnh bìa lên Cloudinary: ' + err.message, 'error');
  } finally {
    uploadingCoverImage.value = false;
  }
};

const courseForm = ref({
  title: '',
  handle: '',
  category: 'dao-tao-doanh-nghiep',
  programId: null,
  image: '',
  coverImage: '',
  price: 0,
  originalPrice: 0,
  duration: '12 tuần',
  level: 'Trung cấp',
  description: '',
  outcomes: '',
  requirements: '',
  customRoadmap: '',
  lecturerIds: ''
});

const openAddCourseModal = () => {
  isEditingCourse.value = false;
  courseForm.value = {
    title: '',
    handle: '',
    category: 'dao-tao-doanh-nghiep',
    programId: null,
    image: '/images/default.jpg',
    coverImage: '',
    price: 9800000,
    originalPrice: 12000000,
    duration: '12 tuần',
    level: 'Trung cấp',
    description: '',
    outcomes: '',
    requirements: '',
    customRoadmap: '',
    lecturerIds: ''
  };
  activeView.value = 'course_form';
};

const editCourseDetails = (c) => {
  isEditingCourse.value = true;
  editingCourseId.value = c.id;
  
  // Format outcomes and requirements array/string into newline-separated string for textarea
  let formattedOutcomes = c.outcomes || '';
  if (Array.isArray(formattedOutcomes)) {
    formattedOutcomes = formattedOutcomes.join('\n');
  } else if (typeof formattedOutcomes === 'string') {
    try {
      const parsed = JSON.parse(formattedOutcomes);
      if (Array.isArray(parsed)) formattedOutcomes = parsed.join('\n');
    } catch (e) {}
  }

  let formattedRequirements = c.requirements || '';
  if (Array.isArray(formattedRequirements)) {
    formattedRequirements = formattedRequirements.join('\n');
  } else if (typeof formattedRequirements === 'string') {
    try {
      const parsed = JSON.parse(formattedRequirements);
      if (Array.isArray(parsed)) formattedRequirements = parsed.join('\n');
    } catch (e) {}
  }

  courseForm.value = {
    title: c.title,
    handle: c.handle,
    category: c.category,
    programId: c.programId || null,
    image: c.image,
    coverImage: c.coverImage || '',
    price: c.price,
    originalPrice: c.originalPrice,
    duration: c.duration,
    level: c.level,
    description: c.description,
    outcomes: formattedOutcomes,
    requirements: formattedRequirements,
    customRoadmap: c.customRoadmap || '',
    lecturerIds: c.lecturerIds || ''
  };
  activeView.value = 'course_form';
};

const saveCourse = async () => {
  try {
    const payload = { 
      ...courseForm.value,
      image: formatImageUrl(courseForm.value.image),
      coverImage: courseForm.value.coverImage ? formatImageUrl(courseForm.value.coverImage) : null
    };
    if (payload.category === 'custom') {
      if (!customCategorySlug.value.trim()) {
        courseStore.showToast('Vui lòng nhập mã slug cho chuyên mục mới!', 'warning');
        return;
      }
      payload.category = customCategorySlug.value.trim();
    }
    if (isEditingCourse.value) {
      await courseStore.updateAdminCourse(editingCourseId.value, payload);
      courseStore.showToast('Cập nhật khóa học thành công!', 'success');
    } else {
      if (courses.value.some(c => c.handle === payload.handle)) {
        courseStore.showToast('Đường dẫn tĩnh (Slug) này đã tồn tại!', 'warning');
        return;
      }
      await courseStore.addAdminCourse(payload);
      courseStore.showToast('Thêm khóa học mới thành công!', 'success');
    }
    activeView.value = 'list';
  } catch (err) {
    courseStore.showToast(err.message || 'Không thể lưu khóa học.', 'error');
  }
};

const deleteCourse = async (courseId) => {
  const c = courses.value.find(item => item.id === courseId);
  const title = c ? c.title : '';

  const isConfirmed = await courseStore.showConfirm({
    title: 'Xác nhận xóa khóa học',
    message: `Bạn có chắc chắn muốn xóa khóa học "${title}" khỏi hệ thống?\n\nHệ thống sẽ đồng thời dọn dẹp các dữ liệu liên quan (học viên, đánh giá, ghi chú, giỏ hàng...).`,
    confirmText: 'Đồng ý xóa',
    cancelText: 'Hủy bỏ',
    type: 'danger'
  });

  if (isConfirmed) {
    try {
      await courseStore.deleteAdminCourse(courseId);
      courseStore.showToast(`Đã xóa khóa học "${title}" thành công.`, 'success');
    } catch (err) {
      courseStore.showToast(err.message || 'Không thể xóa khóa học.', 'error');
    }
  }
};

// Curriculum Builder State & Methods
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
  activeView.value = 'curriculum_form';
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
    courseStore.showToast('Lưu giáo trình khóa học thành công!', 'success');
    activeView.value = 'list';
  } catch (err) {
    courseStore.showToast(err.message || 'Không thể lưu giáo trình.', 'error');
  }
};

// Helpers
const formatPrice = (value) => {
  if (value === undefined || value === null) return '0đ';
  return value.toLocaleString('vi-VN') + 'đ';
};

const translateCategory = (cat) => {
  switch (cat) {
    case 'dao-tao-doanh-nghiep': return 'Đào tạo cho doanh nghiệp';
    case 'dao-tao-ca-nhan': return 'Đào tạo cho cá nhân';
    case 'dao-tao-co-quan-nha-nuoc': return 'Đào tạo cho khối cơ quan - nhà nước';
    case 'ky-nang-ai': return 'Đào tạo cho doanh nghiệp';
    case 'ky-nang-mem': return 'Đào tạo cho cá nhân';
    case 'ky-nang-chuyen-mon': return 'Đào tạo cho cá nhân';
    case 'bundles': return 'Combo / Gói';
    default: return cat;
  }
};
</script>
