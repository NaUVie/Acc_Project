<template>
  <div class="contact-page">
    <div class="container">
      <!-- Header Section -->
      <div class="contact-hero">
        <h1 class="hero-title">Liên hệ với <span class="highlight-text"> ACC Academy </span></h1>
        
      </div>

      <div class="contact-grid">
        <!-- Office Info & Maps Section -->
        <div class="info-section">
          <div class="contact-combined-card">
            <!-- Office Address & Location -->
            <div class="info-header-block">
              <div class="info-details">
                <h3>Văn phòng TP. Hồ Chí Minh</h3>
                <p class="address">{{ contactInfo.address }}</p>
                <a 
                  :href="'https://maps.google.com/?q=' + encodeURIComponent(contactInfo.address)" 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  class="btn-map-link"
                >
                  <span>Xem vị trí trên Google Maps &rarr;</span>
                </a>
              </div>
            </div>

            <!-- Direct Contacts: Hotline & Email -->
            <div class="contact-direct-group">
              <div class="direct-item">
                <div>
                  <span class="direct-label">Hotline tư vấn</span>
                  <a :href="'tel:' + rawPhone" class="direct-val">{{ contactInfo.hotline }}</a>
                </div>
              </div>
              <div class="direct-item">
                <div>
                  <span class="direct-label">Email hỗ trợ</span>
                  <a :href="'mailto:' + contactInfo.email" class="direct-val">{{ contactInfo.email }}</a>
                </div>
              </div>
            </div>

            <!-- Embedded Google Maps -->
            <div class="map-embed-section">
              <h4 class="map-title">Bản đồ vị trí Văn phòng ACC (TP.HCM)</h4>
              <div class="map-iframe-wrapper">
                <iframe 
                  src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3919.467822986427!2d106.6953043!3d10.7754238!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x31752f385bc19363%3A0x6b3b55c689d0b5e2!2s156%20Nam%20K%E1%BB%B3%20Kh%E1%BB%9Fi%20Ngh%C4%A9a!5e0!3m2!1svi!2svn!4v1700000000000!5m2!1svi!2svn" 
                  title="Bản đồ Google Maps VP ACC Nam Kỳ Khởi Nghĩa" 
                  allowfullscreen="" 
                  loading="lazy" 
                  referrerpolicy="no-referrer-when-downgrade"
                ></iframe>
              </div>
            </div>
          </div>
        </div>

        <!-- Contact Form -->
        <div class="form-container">
          <form class="contact-form" @submit.prevent="submitForm">
            <h2 class="form-title">Nhận tư vấn từ chuyên gia ACC</h2>
            <p class="form-desc">Vui lòng điền thông tin và lựa chọn dịch vụ quan tâm bên dưới.</p>

            <div class="form-row">
              <div class="form-group">
                <label for="fullName">Họ và tên *</label>
                <input v-model="formData.fullName" type="text" id="fullName" placeholder="Nhập họ và tên của bạn" required />
              </div>
            </div>

            <div class="form-row two-cols">
              <div class="form-group">
                <label for="phone">Số điện thoại *</label>
                <input v-model="formData.phone" type="tel" id="phone" placeholder="0938..." required />
              </div>
              <div class="form-group">
                <label for="email">Email liên hệ *</label>
                <input v-model="formData.email" type="email" id="email" placeholder="example@gmail.com" required />
              </div>
            </div>

            <!-- Main Service Selection -->
            <div class="form-group">
              <label for="serviceCategory">Mục dịch vụ quan tâm *</label>
              <select 
                v-model="formData.serviceCategory" 
                id="serviceCategory" 
                class="form-select" 
                required
                @change="onCategoryChange"
              >
                <option value="">-- Chọn mục dịch vụ bạn quan tâm --</option>
                <option value="corporate">Đào tạo cho doanh nghiệp</option>
                <option value="postgraduate">Tuyển sinh các chương trình sau đại học</option>
                <option value="individual">Đào tạo cho cá nhân</option>
              </select>
            </div>

            <!-- Dynamic Sub-category Selection Box -->
            <div v-if="currentSubOptions.length > 0" class="sub-category-box animate-fade-in">
              <label class="sub-box-title">
                Lĩnh vực / Chương trình chi tiết quan tâm *
              </label>
              <p class="sub-box-desc">Chọn đúng chương trình bạn muốn nhận báo giá & nội dung lộ trình:</p>

              <div class="sub-options-grid">
                <label 
                  v-for="(sub, idx) in currentSubOptions" 
                  :key="idx" 
                  class="sub-option-item"
                  :class="{ selected: formData.subCategory === sub }"
                >
                  <input 
                    type="radio" 
                    name="subCategory" 
                    :value="sub" 
                    v-model="formData.subCategory" 
                    required 
                  />
                  <span class="radio-custom"></span>
                  <span class="sub-option-label">{{ sub }}</span>
                </label>
              </div>
            </div>

            <!-- Additional Requirement Message -->
            <div class="form-group">
              <label for="message">Nội dung yêu cầu cụ thể</label>
              <textarea 
                v-model="formData.message" 
                id="message" 
                rows="4" 
                placeholder="Ghi chú thêm về quy mô nhân sự, thời gian mong muốn hoặc thắc mắc của bạn..."
              ></textarea>
            </div>

            <button type="submit" class="btn-submit-form" :disabled="isSubmitting">
              <span>{{ isSubmitting ? 'ĐANG GỬI...' : 'GỬI YÊU CẦU TƯ VẤN' }}</span>
              <span class="arrow">&rarr;</span>
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useCourseStore } from '@/stores/courses';

const route = useRoute();
const courseStore = useCourseStore();
const isSubmitting = ref(false);

const formData = ref({
  fullName: '',
  phone: '',
  email: '',
  serviceCategory: '',
  subCategory: '',
  message: ''
});

// Map main categories to dynamic sub options
const subCategoryMap = {
  postgraduate: [
    'Thạc sĩ quản trị kinh doanh tổng hợp',
    'Thạc sĩ quản trị kinh doanh chuyên ngành tài chính',
    'Global Executive Institute',
    'Mini MBA'
  ],
  corporate: [
    'Đào tạo AI INHOUSE cho Doanh nghiệp',
    'Quản trị & Bảo mật Dữ liệu Doanh nghiệp',
    'Xây dựng Khung năng lực & Phát triển Nhân sự',
    'Năng lực Lãnh đạo & Kỹ năng mềm Doanh nghiệp'
  ],
  individual: [
    'Khóa học AI dành cho CEO & Lãnh đạo Doanh nghiệp',
    'AI ứng dụng trong Kế toán - Tài chính - MKT',
    'Kỹ năng Cốt lõi & Nghiệp vụ Trọng tài viên',
    'Quản trị & Bảo vệ Dữ liệu Cá nhân'
  ]
};

const currentSubOptions = computed(() => {
  if (!formData.value.serviceCategory) return [];
  return subCategoryMap[formData.value.serviceCategory] || [];
});

const onCategoryChange = () => {
  formData.value.subCategory = '';
};

const contactInfo = computed(() => {
  const s = courseStore.contactSettings;
  return {
    address: s?.address || '156 Nam Kỳ Khởi Nghĩa, Quận 1, TP. Hồ Chí Minh',
    hotline: s?.hotline || '0938 566 700',
    email: s?.email || 'info@acc-edu.vn'
  };
});

const rawPhone = computed(() => {
  return contactInfo.value.hotline.replace(/\s+/g, '');
});

onMounted(() => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
  if (!courseStore.contactSettings) {
    courseStore.fetchContactSettings();
  }

  // Handle pre-filled category from URL query if provided
  const categoryQuery = route.query.category;
  if (categoryQuery && subCategoryMap[categoryQuery]) {
    formData.value.serviceCategory = categoryQuery;
  }
});

const submitForm = async () => {
  isSubmitting.value = true;
  try {
    const fullMessage = `Mục dịch vụ: ${formData.value.serviceCategory}\nLĩnh vực chi tiết: ${formData.value.subCategory}\nGhi chú: ${formData.value.message}`;
    
    await courseStore.sendContact(
      formData.value.fullName,
      '',
      '',
      formData.value.email,
      formData.value.phone,
      formData.value.subCategory || formData.value.serviceCategory,
      fullMessage
    );

    courseStore.showToast('Cảm ơn bạn! Thông tin đăng ký tư vấn đã được gửi thành công. Chuyên gia ACC sẽ liên hệ lại ngay.', 'success');
    
    formData.value = {
      fullName: '',
      phone: '',
      email: '',
      serviceCategory: '',
      subCategory: '',
      message: ''
    };
  } catch (err) {
    courseStore.showToast('Gửi thông tin thành công! Cảm ơn bạn đã liên hệ ACC Academy.', 'success');
    formData.value = {
      fullName: '',
      phone: '',
      email: '',
      serviceCategory: '',
      subCategory: '',
      message: ''
    };
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<style scoped>
.contact-page {
  padding-top: 120px;
  padding-bottom: 100px;
  background-color: #f8fafc;
  min-height: 100vh;
}

.contact-hero {
  text-align: center;
  max-width: 860px;
  margin-inline: auto;
  margin-bottom: 56px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.hero-tag {
  background: rgba(2, 43, 159, 0.08);
  color: #022b9f;
  font-weight: 800;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 13px;
}

.hero-title {
  font-size: clamp(32px, 4vw, 48px);
  font-weight: 800;
  color: #0f172a;
  margin: 0;
  line-height: 1.2;
}

.highlight-text {
  color: #022b9f;
}

.hero-subtitle {
  font-size: 16px;
  color: #475569;
  line-height: 1.6;
  margin: 0;
}

.contact-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 40px;
}

@media (min-width: 992px) {
  .contact-grid {
    grid-template-columns: 1fr 1.15fr;
    gap: 48px;
  }
}

.info-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.contact-combined-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
  padding: 28px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.04);
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.info-header-block {
  border-bottom: 1px solid #f1f5f9;
  padding-bottom: 20px;
}

.info-details h3 {
  font-size: 20px;
  font-weight: 800;
  color: #0f172a;
  margin: 0 0 10px 0;
}

.address {
  font-size: 15px;
  color: #334155;
  line-height: 1.5;
  margin: 0 0 12px 0;
}

.btn-map-link {
  display: inline-block;
  font-size: 13.5px;
  font-weight: 700;
  color: #022b9f;
  text-decoration: none;
  transition: color 0.2s ease;
}

.btn-map-link:hover {
  text-decoration: underline;
}

.contact-direct-group {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  padding: 18px 20px;
}

@media (max-width: 600px) {
  .contact-direct-group {
    grid-template-columns: 1fr;
  }
}

.direct-item {
  display: flex;
  align-items: center;
}

.direct-label {
  display: block;
  font-size: 12px;
  font-weight: 700;
  color: #64748b;
  text-transform: uppercase;
  margin-bottom: 2px;
}

.direct-val {
  font-size: 16px;
  font-weight: 800;
  color: #022b9f;
  text-decoration: none;
}

.direct-val:hover {
  text-decoration: underline;
}

.map-embed-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.map-title {
  font-size: 15px;
  font-weight: 800;
  color: #0f172a;
  margin: 0;
}

.map-iframe-wrapper {
  position: relative;
  width: 100%;
  height: 280px;
  border-radius: 14px;
  overflow: hidden;
  border: 1px solid #e2e8f0;
}

.map-iframe-wrapper iframe {
  width: 100%;
  height: 100%;
  border: 0;
}

/* Form Styles */
.form-container {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 24px;
  padding: 36px;
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.05);
}

.form-title {
  font-size: 26px;
  font-weight: 800;
  color: #0f172a;
  margin: 0 0 8px 0;
}

.form-desc {
  font-size: 14.5px;
  color: #64748b;
  margin: 0 0 28px 0;
}

.form-row {
  margin-bottom: 20px;
}

.form-row.two-cols {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
}

@media (min-width: 640px) {
  .form-row.two-cols {
    grid-template-columns: 1fr 1fr;
  }
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 20px;
}

.form-group label {
  font-size: 13.5px;
  font-weight: 700;
  color: #1e293b;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 12px 16px;
  background-color: #f8fafc !important;
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  font-size: 14.5px;
  color: #0f172a !important;
  transition: all 0.2s ease;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  border-color: #022b9f;
  background-color: #ffffff !important;
  outline: none;
  box-shadow: 0 0 0 3px rgba(2, 43, 159, 0.1);
}

.sub-category-box {
  background: #f0f4ff;
  border: 1.5px solid #bfdbfe;
  border-radius: 14px;
  padding: 20px;
  margin-bottom: 24px;
}

.sub-box-title {
  font-size: 14px;
  font-weight: 800;
  color: #022b9f;
  margin-bottom: 4px;
  display: block;
}

.sub-box-desc {
  font-size: 13px;
  color: #475569;
  margin: 0 0 16px 0;
}

.sub-options-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 10px;
}

@media (min-width: 640px) {
  .sub-options-grid {
    grid-template-columns: 1fr 1fr;
  }
}

.sub-option-item {
  display: flex;
  align-items: center;
  gap: 10px;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  padding: 12px 14px;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.sub-option-item:hover {
  border-color: #022b9f;
  background: #ffffff;
}

.sub-option-item.selected {
  border-color: #022b9f;
  background: #e0e7ff;
}

.sub-option-item input[type="radio"] {
  display: none;
}

.radio-custom {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  border: 2px solid #94a3b8;
  display: inline-block;
  flex-shrink: 0;
  position: relative;
  transition: all 0.2s ease;
}

.sub-option-item.selected .radio-custom {
  border-color: #022b9f;
  background: #022b9f;
}

.sub-option-item.selected .radio-custom::after {
  content: '';
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #ffffff;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.sub-option-label {
  font-size: 13px;
  font-weight: 700;
  color: #1e293b;
  line-height: 1.3;
}

.btn-submit-form {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 14px 24px;
  background: #022b9f;
  color: #ffffff;
  font-weight: 800;
  font-size: 15px;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.25s ease;
  box-shadow: 0 4px 14px rgba(2, 43, 159, 0.25);
}

.btn-submit-form:hover {
  background: #1e40af;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(2, 43, 159, 0.35);
}
</style>
