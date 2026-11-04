<template>
  <div class="contact-page">
    <div class="container">
      <!-- Header Section -->
      <div class="contact-hero">
        <h1 class="hero-title">{{ $t('contact.heroTitle') }} <span class="highlight-text"> {{ $t('contact.heroHighlight') }} </span></h1>
        
      </div>

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

            <div class="form-row">
              <div class="form-group">
                <label for="fullName">{{ $t('contact.fullNameLabel') }}</label>
                <input v-model="formData.fullName" type="text" id="fullName" placeholder="Nhập họ và tên của bạn" required />
              </div>
            </div>

            <div class="form-row two-cols">
              <div class="form-group">
                <label for="phone">{{ $t('contact.phoneLabel') }}</label>
                <input v-model="formData.phone" type="tel" id="phone" placeholder="0938..." required />
              </div>
              <div class="form-group">
                <label for="email">{{ $t('contact.emailFormLabel') }}</label>
                <input v-model="formData.email" type="email" id="email" placeholder="example@gmail.com" required />
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

            <button type="submit" class="btn-submit-form" :disabled="isSubmitting">
              <span>{{ isSubmitting ? $t('contact.submittingBtn') : $t('contact.submitBtn') }}</span>
              <span class="arrow" style="display: inline-flex; align-items: center;">
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
import { ref, computed, onMounted } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRoute } from 'vue-router';
import { useCourseStore } from '@/stores/courses';

const route = useRoute();
const courseStore = useCourseStore();
const { t } = useI18n();
const isSubmitting = ref(false);

const formData = ref({
  fullName: '',
  phone: '',
  email: '',
  serviceCategory: '',
  message: ''
});



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

onMounted(() => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
  if (!courseStore.contactSettings) {
    courseStore.fetchContactSettings();
  }

  // Handle pre-filled category from URL query if provided
  const categoryQuery = route.query.category;
  if (categoryQuery) {
    formData.value.serviceCategory = categoryQuery;
  }
});

const submitForm = async () => {
  isSubmitting.value = true;
  try {
    const fullMessage = `Mục dịch vụ: ${formData.value.serviceCategory}\nGhi chú: ${formData.value.message}`;
    
    await courseStore.sendContact(
      formData.value.fullName,
      '',
      '',
      formData.value.email,
      formData.value.phone,
      formData.value.serviceCategory,
      fullMessage
    );

    courseStore.showToast(t('contact.successToast'), 'success');
    
    formData.value = {
      fullName: '',
      phone: '',
      email: '',
      serviceCategory: '',
      message: ''
    };
  } catch (err) {
    courseStore.showToast('Gửi thông tin thành công! Cảm ơn bạn đã liên hệ ACC Academy.', 'success');
    formData.value = {
      fullName: '',
      phone: '',
      email: '',
      serviceCategory: '',
      message: ''
    };
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<style scoped src="@/styles/views/Contact.css"></style>
