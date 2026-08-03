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
          <p>{{ courseStore.contactSettings?.address || 'Tòa nhà ACC, 123 Đường Điện Biên Phủ, Quận Bình Thạnh, TP. Hồ Chí Minh' }}</p>
        </div>

        <div class="info-card glass-card animate-slide-up">
          <h3>Thông tin liên lạc</h3>
          <p>📞 Hotline: {{ courseStore.contactSettings?.hotline || '090 123 4567' }}</p>
          <p>✉️ Email: {{ courseStore.contactSettings?.email || 'support@accacademy.vn' }}</p>
          <p v-if="courseStore.contactSettings?.zalo">💬 Zalo: <a :href="courseStore.contactSettings?.zalo" target="_blank" rel="noopener">{{ courseStore.contactSettings?.zalo }}</a></p>
          <p v-if="courseStore.contactSettings?.viber">📞 Viber: <a :href="courseStore.contactSettings?.viber" target="_blank" rel="noopener">{{ courseStore.contactSettings?.viber }}</a></p>
        </div>
      </div>

      <!-- Contact Form -->
      <form class="contact-form glass-card animate-slide-up" @submit.prevent="submitForm">
        <h3 class="mb-4 font-bold text-lg text-white" style="border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px;">Nhận tư vấn giải pháp từ Skills Bridge</h3>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; margin-bottom: 15px;">
          <div class="form-group" style="margin-bottom: 0;">
            <label for="lastName">Họ *</label>
            <input v-model="formData.lastName" type="text" id="lastName" placeholder="Họ của bạn" required>
          </div>
          <div class="form-group" style="margin-bottom: 0;">
            <label for="middleName">Tên đệm *</label>
            <input v-model="formData.middleName" type="text" id="middleName" placeholder="Tên đệm của bạn" required>
          </div>
          <div class="form-group" style="margin-bottom: 0;">
            <label for="firstName">Tên *</label>
            <input v-model="formData.firstName" type="text" id="firstName" placeholder="Tên của bạn" required>
          </div>
        </div>
        
        <div class="form-group">
          <label for="email">Email *</label>
          <input v-model="formData.email" type="email" id="email" placeholder="Nhập email của bạn" required>
        </div>

        <div class="form-group">
          <label for="phone">Số điện thoại của bạn là? *</label>
          <input v-model="formData.phone" type="text" id="phone" placeholder="Nhập số điện thoại" required>
        </div>

        <div class="form-group">
          <label for="course">Dịch vụ bạn quan tâm *</label>
          <select v-model="formData.courseHandle" id="course" class="form-select" required>
            <option value="">-- Chọn dịch vụ / khóa học --</option>
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
          <label for="message">Nội dung yêu cầu *</label>
          <textarea v-model="formData.message" id="message" rows="5" placeholder="Tôi muốn nhận tư vấn về..." required></textarea>
        </div>

        <button type="submit" class="btn btn-primary" style="width: 100%;">Gửi lời nhắn</button>
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
  firstName: '',
  middleName: '',
  lastName: '',
  email: '',
  phone: '',
  courseHandle: '',
  message: ''
});

onMounted(() => {
  courseStore.fetchContactSettings();
  
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
      formData.value.firstName,
      formData.value.middleName,
      formData.value.lastName,
      formData.value.email,
      formData.value.phone,
      formData.value.courseHandle,
      formData.value.message
    );
    alert('Cảm ơn bạn! Yêu cầu của bạn đã được gửi đi thành công và đã được lưu vào cơ sở dữ liệu.');
    formData.value = {
      firstName: '',
      middleName: '',
      lastName: '',
      email: '',
      phone: '',
      courseHandle: '',
      message: ''
    };
  } catch (err) {
    alert('Có lỗi xảy ra khi gửi yêu cầu: ' + err.message);
  }
};
</script>

<style scoped src="@/styles/views/Contact.css"></style>
