<template>
  <div class="contact-view container">
    <div class="header-section animate-fade-in">
      <div class="badge">HỖ TRỢ & LIÊN HỆ</div>
      <h1>Liên hệ với <span class="gradient-text">ACC Academy</span></h1>
      <p class="subtitle">Hãy gửi thông tin của bạn, đội ngũ hỗ trợ của chúng tôi sẽ liên hệ lại trong vòng 24 giờ làm việc.</p>
    </div>

    <div class="contact-grid">
      <!-- Contact Info -->
      <div class="info-section">
        <div class="info-card glass-card animate-slide-up">
          <h3>Trụ sở chính</h3>
          <p>Tòa nhà ACC, 123 Đường Điện Biên Phủ, Quận Bình Thạnh, TP. Hồ Chí Minh</p>
        </div>

        <div class="info-card glass-card animate-slide-up">
          <h3>Thông tin liên lạc</h3>
          <p>📞 Hotline: 090 123 4567</p>
          <p>✉️ Email: support@accacademy.vn</p>
        </div>
      </div>

      <!-- Contact Form -->
      <form class="contact-form glass-card animate-slide-up" @submit.prevent="submitForm">
        <div class="form-group">
          <label for="name">Họ và tên</label>
          <input v-model="formData.name" type="text" id="name" placeholder="Nguyễn Văn A" required>
        </div>
        
        <div class="form-group">
          <label for="email">Email</label>
          <input v-model="formData.email" type="email" id="email" placeholder="name@company.com" required>
        </div>

        <div class="form-group">
          <label for="course">Khóa học quan tâm</label>
          <select v-model="formData.courseHandle" id="course" class="form-select">
            <option value="">-- Chọn khóa học / dịch vụ </option>
            <optgroup label="Kỹ năng AI">
              <option v-for="c in aiCourses" :key="c.id" :value="c.handle">{{ c.title }}</option>
            </optgroup>
            <optgroup label="Kỹ năng Mềm">
              <option v-for="c in softCourses" :key="c.id" :value="c.handle">{{ c.title }}</option>
            </optgroup>
            <optgroup label="Kỹ năng Chuyên môn">
              <option v-for="c in proCourses" :key="c.id" :value="c.handle">{{ c.title }}</option>
            </optgroup>
            <optgroup label="Combo Khóa học">
              <option v-for="c in comboCourses" :key="c.id" :value="c.handle">{{ c.title }}</option>
            </optgroup>
          </select>
        </div>

        <div class="form-group">
          <label for="message">Lời nhắn / Yêu cầu tư vấn</label>
          <textarea v-model="formData.message" id="message" rows="5" placeholder="Tôi muốn nhận tư vấn về khóa học..." required></textarea>
        </div>

        <button type="submit" class="btn btn-primary">Gửi lời nhắn</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useCourseStore } from '@/stores/courses';

const route = useRoute();
const courseStore = useCourseStore();

const aiCourses = computed(() => courseStore.getCoursesByCategory('ky-nang-ai'));
const softCourses = computed(() => courseStore.getCoursesByCategory('ky-nang-mem'));
const proCourses = computed(() => courseStore.getCoursesByCategory('ky-nang-chuyen-mon'));
const comboCourses = computed(() => courseStore.getCoursesByCategory('bundles'));

const formData = ref({
  name: '',
  email: '',
  courseHandle: '',
  message: ''
});

onMounted(() => {
  // Pre-fill course from query param
  const courseParam = route.query.course;
  if (courseParam) {
    formData.value.courseHandle = courseParam;
    const matchedCourse = courseStore.courses.find(c => c.handle === courseParam);
    if (matchedCourse) {
      formData.value.message = `Tôi muốn nhận tư vấn chi tiết về khóa học "${matchedCourse.title}".`;
    }
  }
});

const submitForm = async () => {
  try {
    await courseStore.sendContact(
      formData.value.name,
      formData.value.email,
      formData.value.courseHandle,
      formData.value.message
    );
    alert('Cảm ơn bạn! Yêu cầu của bạn đã được gửi đi thành công và đã được lưu vào cơ sở dữ liệu.');
    formData.value = {
      name: '',
      email: '',
      courseHandle: '',
      message: ''
    };
  } catch (err) {
    alert('Có lỗi xảy ra khi gửi yêu cầu: ' + err.message);
  }
};
</script>

<style scoped>
.contact-view {
  padding: 80px 24px;
}

.header-section {
  text-align: center;
  max-width: 800px;
  margin: 0 auto 60px auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.badge {
  background: rgba(14, 165, 233, 0.15);
  border: 1px solid rgba(14, 165, 233, 0.3);
  color: var(--primary);
  padding: 8px 20px;
  border-radius: var(--radius-full);
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 1px;
}

.header-section h1 {
  font-family: var(--font-display);
  font-size: 52px;
  font-weight: 800;
  line-height: 1.2;
}

.subtitle {
  font-size: 18px;
  color: var(--text-secondary);
  line-height: 1.6;
}

.contact-grid {
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  gap: 40px;
  align-items: start;
}

.info-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.info-card {
  padding: 30px;
  border-radius: var(--radius-md);
}

.info-card h3 {
  font-family: var(--font-display);
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 12px;
}

.info-card p {
  color: var(--text-secondary);
  font-size: 15px;
  line-height: 1.6;
}

.contact-form {
  padding: 40px;
  border-radius: var(--radius-lg);
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.form-group input,
.form-group select,
.form-group textarea {
  background-color: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border-color);
  padding: 12px 16px;
  border-radius: var(--radius-sm);
  color: white;
  font-family: inherit;
  font-size: 14px;
  transition: var(--transition);
}

.form-group select option {
  background-color: #0f172a;
  color: white;
}

.form-group select optgroup {
  background-color: #1e293b;
  color: var(--primary);
  font-weight: 600;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  border-color: var(--primary);
  outline: none;
  background-color: rgba(255, 255, 255, 0.05);
}

@media (max-width: 768px) {
  .contact-grid {
    grid-template-columns: 1fr;
  }
  
  .header-section h1 {
    font-size: 38px;
  }
}
</style>
