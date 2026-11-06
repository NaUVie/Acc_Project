<template>
  <div class="contact-page">
    <!-- Hero Banner Section với nền xanh navy gradient nhạt dần -->
    <section class="contact-hero-section">
      <div class="hero-backdrop-glow"></div>
      <div class="container hero-inner">
        <h1 class="hero-title animate-fade-in">
          {{ $t('contact.heroTitle') }} <span class="highlight-text">{{ $t('contact.heroHighlight') }}</span>
        </h1>
        <p class="hero-subtitle animate-fade-in">
          Đội ngũ chuyên gia ACC Academy luôn sẵn sàng đồng hành, giải đáp mọi thắc mắc và tư vấn lộ trình đào tạo tối ưu nhất cho bạn
        </p>
      </div>
    </section>

    <div class="container contact-content-container">
      <div class="contact-grid">
        <!-- Office Info & Maps Section -->
        <div class="info-section">
          <div class="contact-combined-card">
            <!-- Office Address & Location -->
            <div class="info-header-block">
              <div class="info-details">
                <h3>{{ $t('contact.officeHcm') }}</h3>
                <p class="address">{{ contactInfo.address }}</p>
                <a 
                  :href="'https://maps.google.com/?q=' + encodeURIComponent(contactInfo.address)" 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  class="btn-map-link"
                >
                  <span style="display: inline-flex; align-items: center; gap: 6px;">
                    <span>{{ $t('contact.viewMap') }}</span>
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                      <line x1="5" y1="12" x2="19" y2="12"></line>
                      <polyline points="12 5 19 12 12 19"></polyline>
                    </svg>
                  </span>
                </a>
              </div>
            </div>

            <!-- Direct Contacts: Hotline & Email -->
            <div class="contact-direct-group">
              <div class="direct-item">
                <div>
                  <span class="direct-label">{{ $t('contact.hotlineLabel') }}</span>
                  <a :href="'tel:' + rawPhone" class="direct-val">{{ contactInfo.hotline }}</a>
                </div>
              </div>
              <div class="direct-item">
                <div>
                  <span class="direct-label">{{ $t('contact.emailLabel') }}</span>
                  <a :href="'mailto:' + contactInfo.email" class="direct-val">{{ contactInfo.email }}</a>
                </div>
              </div>
            </div>

            <!-- Embedded Google Maps -->
            <div class="map-embed-section">
              <h4 class="map-title">{{ $t('contact.mapTitle') }}</h4>
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
            <h2 class="form-title">{{ $t('contact.formTitle') }}</h2>
            <p class="form-desc">{{ $t('contact.formDesc') }}</p>

            <!-- Selected Course Banner if navigated from Course Detail -->
            <div v-if="selectedCourseTitle" class="selected-course-banner">
              <div class="selected-course-left">
                <span class="selected-course-icon">🎓</span>
                <div class="selected-course-info">
                  <span class="selected-course-label">Khóa học quan tâm tư vấn</span>
                  <strong class="selected-course-title">{{ selectedCourseTitle }}</strong>
                </div>
              </div>
              <button type="button" class="btn-clear-course" @click="clearSelectedCourse" title="Bỏ chọn">&times;</button>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="fullName">{{ $t('contact.fullNameLabel') }}</label>
                <input v-model="formData.fullName" type="text" id="fullName" placeholder="Nhập họ và tên của bạn" required />
              </div>
            </div>

            <div class="form-row two-cols">
              <div class="form-group" :class="{ 'has-error': phoneError }">
                <label for="phone">{{ $t('contact.phoneLabel') }} <span class="required-star">*</span></label>
                <input 
                  v-model="formData.phone" 
                  type="tel" 
                  id="phone" 
                  placeholder="Ví dụ: 0938 566 700" 
                  required 
                  @blur="validatePhoneField"
                  @input="onPhoneInput"
                />
                <span v-if="phoneError" class="field-error-text">
                  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
                  {{ phoneError }}
                </span>
              </div>
              <div class="form-group" :class="{ 'has-error': emailError }">
                <label for="email">{{ $t('contact.emailFormLabel') }} <span class="required-star">*</span></label>
                <input 
                  v-model="formData.email" 
                  type="email" 
                  id="email" 
                  placeholder="Ví dụ: example@gmail.com" 
                  required 
                  @blur="validateEmailField"
                  @input="onEmailInput"
                />
                <span v-if="emailError" class="field-error-text">
                  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
                  {{ emailError }}
                </span>
              </div>
            </div>

            <!-- Main Service Selection -->
            <div class="form-group">
              <label for="serviceCategory">{{ $t('contact.serviceLabel') }}</label>
              <select 
                v-model="formData.serviceCategory" 
                id="serviceCategory" 
                class="form-select" 
                required
                
              >
                <option value="">{{ $t('contact.selectService') }}</option>
                <option value="corporate">{{ $t('contact.serviceInhouse') }}</option>
                <option value="postgraduate">{{ $t('contact.serviceAndrews') }}</option>
                <option value="individual">{{ $t('contact.serviceAI') }}</option>
              </select>
            </div>

            <!-- Additional Requirement Message -->
            <div class="form-group">
              <label for="message">{{ $t('contact.messageLabel') }}</label>
              <textarea 
                v-model="formData.message" 
                id="message" 
                rows="4" 
                :placeholder="$t('contact.messagePlaceholder')"
              ></textarea>
            </div>

            <!-- Anti-spam Honeypot field (hidden from real users, bots will auto-fill) -->
            <div class="ohnohoney" aria-hidden="true">
              <label for="fax_number">Do not fill this</label>
              <input type="text" id="fax_number" v-model="honeypotValue" autocomplete="off" tabindex="-1" />
            </div>

            <button type="submit" class="btn-submit-form" :disabled="isSubmitting || submitCooldown > 0">
              <span v-if="submitCooldown > 0">Đã gửi yêu cầu (Đợi {{ submitCooldown }}s)</span>
              <span v-else>{{ isSubmitting ? $t('contact.submittingBtn') : $t('contact.submitBtn') }}</span>
              <span v-if="submitCooldown <= 0" class="arrow" style="display: inline-flex; align-items: center;">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="5" y1="12" x2="19" y2="12"></line>
                  <polyline points="12 5 19 12 12 19"></polyline>
                </svg>
              </span>
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRoute } from 'vue-router';
import { useCourseStore } from '@/stores/courses';
import { validateVietnamesePhone, validateEmail } from '@/utils/validation';

const route = useRoute();
const courseStore = useCourseStore();
const { t } = useI18n();
const isSubmitting = ref(false);
const selectedCourseTitle = ref('');
const selectedCourseHandle = ref('');

const phoneError = ref('');
const emailError = ref('');

// Anti-spam Honeypot & Cooldown state
const honeypotValue = ref('');
const submitCooldown = ref(0);
let cooldownTimer = null;

const startCooldown = (seconds = 30) => {
  submitCooldown.value = seconds;
  try {
    localStorage.setItem('acc_contact_cooldown_until', (Date.now() + seconds * 1000).toString());
  } catch (e) {}

  if (cooldownTimer) clearInterval(cooldownTimer);
  cooldownTimer = setInterval(() => {
    submitCooldown.value -= 1;
    if (submitCooldown.value <= 0) {
      clearInterval(cooldownTimer);
      cooldownTimer = null;
      try {
        localStorage.removeItem('acc_contact_cooldown_until');
      } catch (e) {}
    }
  }, 1000);
};

const checkExistingCooldown = () => {
  try {
    const until = Number(localStorage.getItem('acc_contact_cooldown_until') || 0);
    const remaining = Math.ceil((until - Date.now()) / 1000);
    if (remaining > 0) {
      startCooldown(remaining);
    }
  } catch (e) {}
};

const clearSelectedCourse = () => {
  selectedCourseTitle.value = '';
  selectedCourseHandle.value = '';
  formData.value.message = '';
};

const formData = ref({
  fullName: '',
  phone: '',
  email: '',
  serviceCategory: '',
  message: ''
});

const validatePhoneField = () => {
  if (!formData.value.phone) {
    phoneError.value = '';
    return;
  }
  const check = validateVietnamesePhone(formData.value.phone);
  phoneError.value = check.isValid ? '' : check.error;
};

const onPhoneInput = () => {
  if (phoneError.value) {
    const check = validateVietnamesePhone(formData.value.phone);
    if (check.isValid) phoneError.value = '';
  }
};

const validateEmailField = () => {
  if (!formData.value.email) {
    emailError.value = '';
    return;
  }
  const check = validateEmail(formData.value.email);
  emailError.value = check.isValid ? '' : check.error;
};

const onEmailInput = () => {
  if (emailError.value) {
    const check = validateEmail(formData.value.email);
    if (check.isValid) emailError.value = '';
  }
};

const contactInfo = computed(() => {
  const s = courseStore.contactSettings;
  return {
    address: s?.address || '156 Nam Kỳ Khởi Nghĩa, Phường Sài Gòn, TP.HCM',
    hotline: s?.hotline || '0938 566 700',
    email: s?.email || 'info@acc-edu.vn'
  };
});

const rawPhone = computed(() => {
  return contactInfo.value.hotline.replace(/\s+/g, '');
});

const initFromQuery = () => {
  const courseQuery = route.query.course || route.query.course_title;
  const handleQuery = route.query.handle || route.query.course_handle;
  const programQuery = route.query.program;
  const categoryQuery = route.query.category;

  if (courseQuery) {
    selectedCourseTitle.value = courseQuery;
    selectedCourseHandle.value = handleQuery || courseQuery;
    if (!formData.value.message) {
      formData.value.message = `Tôi muốn nhận tư vấn thông tin và đăng ký khóa học: ${courseQuery}`;
    }
  } else if (programQuery) {
    const progUpper = String(programQuery).toUpperCase();
    selectedCourseTitle.value = `Chương trình: ${progUpper}`;
    selectedCourseHandle.value = programQuery;
    formData.value.serviceCategory = 'postgraduate';
    if (!formData.value.message) {
      formData.value.message = `Tôi muốn nhận tư vấn thông tin chương trình tuyển sinh: ${progUpper}`;
    }
  }

  if (categoryQuery) {
    const cat = String(categoryQuery).toLowerCase();
    if (cat.includes('doanh-nghiep') || cat.includes('corporate') || cat.includes('nha-nuoc')) {
      formData.value.serviceCategory = 'corporate';
    } else if (cat.includes('postgraduate') || cat.includes('mba') || cat.includes('gei') || cat.includes('tuyen-sinh')) {
      formData.value.serviceCategory = 'postgraduate';
    } else if (cat.includes('individual') || cat.includes('ai') || cat.includes('ca-nhan') || cat.includes('mem') || cat.includes('chuyen-mon')) {
      formData.value.serviceCategory = 'individual';
    } else {
      formData.value.serviceCategory = categoryQuery;
    }
  }

  // Auto-fill logged in user info if available (NOT required!)
  if (courseStore.userMe) {
    if (!formData.value.fullName) formData.value.fullName = courseStore.userMe.fullname || '';
    if (!formData.value.phone) formData.value.phone = courseStore.userMe.phone || '';
    if (!formData.value.email) formData.value.email = courseStore.userMe.email || '';
  }
};

onMounted(() => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
  if (!courseStore.contactSettings) {
    courseStore.fetchContactSettings();
  }
  initFromQuery();
  checkExistingCooldown();
});

onUnmounted(() => {
  if (cooldownTimer) clearInterval(cooldownTimer);
});

const submitForm = async () => {
  if (submitCooldown.value > 0) {
    courseStore.showToast(`Bạn vừa gửi yêu cầu rồi. Vui lòng đợi ${submitCooldown.value} giây trước khi gửi tiếp!`, 'warning');
    return;
  }

  const cleanName = (formData.value.fullName || '').trim();
  if (!cleanName) {
    courseStore.showToast('Vui lòng nhập họ và tên của bạn', 'warning');
    const el = document.getElementById('fullName');
    if (el) el.focus();
    return;
  }

  const phoneCheck = validateVietnamesePhone(formData.value.phone);
  if (!phoneCheck.isValid) {
    phoneError.value = phoneCheck.error;
    courseStore.showToast(phoneCheck.error, 'warning');
    const el = document.getElementById('phone');
    if (el) el.focus();
    return;
  }
  phoneError.value = '';

  const emailCheck = validateEmail(formData.value.email);
  if (!emailCheck.isValid) {
    emailError.value = emailCheck.error;
    courseStore.showToast(emailCheck.error, 'warning');
    const el = document.getElementById('email');
    if (el) el.focus();
    return;
  }
  emailError.value = '';

  isSubmitting.value = true;
  try {
    const getCategoryName = (cat) => {
      const map = {
        corporate: 'Đào tạo cho doanh nghiệp',
        postgraduate: 'Tuyển sinh các chương trình sau đại học',
        individual: 'Đào tạo cho cá nhân'
      };
      return map[cat] || cat || '';
    };

    const categoryTitle = getCategoryName(formData.value.serviceCategory);

    // Xác định tên Khóa học / Chủ đề tư vấn
    let courseTarget = '';
    if (selectedCourseTitle.value) {
      courseTarget = categoryTitle 
        ? `${selectedCourseTitle.value} (${categoryTitle})`
        : selectedCourseTitle.value;
    } else if (categoryTitle) {
      courseTarget = categoryTitle;
    } else {
      courseTarget = 'Tư vấn thông tin chung';
    }

    // Giữ nguyên nội dung lời nhắn của khách hàng, không chèn tiền tố slug thô
    const userMsg = (formData.value.message || '').trim();
    const fullMessage = userMsg || (selectedCourseTitle.value
      ? `Đăng ký nhận tư vấn khóa học: ${selectedCourseTitle.value}`
      : `Đăng ký nhận tư vấn dịch vụ: ${categoryTitle || 'ACC Academy'}`);

    const nameParts = cleanName.split(' ');
    const lastName = nameParts.length > 0 ? nameParts[nameParts.length - 1] : '';
    const firstName = nameParts.length > 1 ? nameParts[0] : cleanName;
    const middleName = nameParts.length > 2 ? nameParts.slice(1, -1).join(' ') : '';

    await courseStore.sendContact(
      firstName,
      middleName,
      lastName,
      emailCheck.email,
      phoneCheck.normalized,
      courseTarget,
      fullMessage,
      honeypotValue.value
    );

    courseStore.showToast(t('contact.successToast'), 'success');
    startCooldown(30);
    
    formData.value = {
      fullName: '',
      phone: '',
      email: '',
      serviceCategory: '',
      message: ''
    };
    selectedCourseTitle.value = '';
    selectedCourseHandle.value = '';
  } catch (err) {
    courseStore.showToast(err.message || 'Gửi thông tin thất bại. Vui lòng liên hệ Hotline 0938 566 700!', 'error');
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<style scoped src="@/styles/views/Contact.css"></style>
