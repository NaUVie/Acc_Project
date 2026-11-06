<template>
  <div class="auth-page-container">
    <!-- Ambient Background Glows -->
    <div class="auth-bg-blob-1"></div>
    <div class="auth-bg-blob-2"></div>

    <div class="auth-master-card">
      <!-- LEFT BRAND PANEL -->
      <div class="auth-brand-side">
        <div class="brand-header">
          <router-link to="/" class="brand-logo-wrap" title="Về trang chủ ACC Academy">
            <img src="/images/logo3.png" alt="ACC Academy" class="brand-logo-img" />
          </router-link>

          <div class="brand-badge-pill">
            <span class="brand-pulse-dot"></span>
            ACC ACADEMY
          </div>

          <h1 class="brand-lead-title">
            Bắt đầu hành trình học tập cùng ACC
          </h1>

          <p class="brand-lead-desc">
            Đăng ký tài khoản để tham gia các chương trình đào tạo thực chiến về công nghệ, AI và quản trị.
          </p>

          <!-- Core Values -->
          <div class="brand-perks-list">
            <div class="brand-perk-item">
              <div class="perk-icon-circle">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
                  <path d="M2 17l10 5 10-5"></path>
                  <path d="M2 12l10 5 10-5"></path>
                </svg>
              </div>
              <div>
                <div class="perk-content-title">Học tập bài bản</div>
                <div class="perk-content-subtitle">Lộ trình rõ ràng, dễ tiếp cận và ứng dụng</div>
              </div>
            </div>

            <div class="brand-perk-item">
              <div class="perk-icon-circle">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
                </svg>
              </div>
              <div>
                <div class="perk-content-title">Nâng cao hiệu suất</div>
                <div class="perk-content-subtitle">Tối ưu quy trình và năng suất làm việc thực tế</div>
              </div>
            </div>

            <div class="brand-perk-item">
              <div class="perk-icon-circle">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path>
                </svg>
              </div>
              <div>
                <div class="perk-content-title">Đồng hành &amp; Hỗ trợ</div>
                <div class="perk-content-subtitle">Giải đáp thắc mắc trong suốt quá trình học tập</div>
              </div>
            </div>
          </div>
        </div>

        <div class="brand-footer-note">
          Kiến tạo năng lực — Dẫn dắt chuyển đổi bền vững
        </div>
      </div>

      <!-- RIGHT FORM PANEL -->
      <div class="auth-form-side">
        <!-- Segmented Tab Switcher -->
        <div class="auth-nav-segmented">
          <router-link to="/login" class="auth-nav-pill">
            {{ $t('header.login') }}
          </router-link>
          <button class="auth-nav-pill active" type="button">
            {{ $t('header.register') }}
          </button>
        </div>

        <!-- Form Heading -->
        <div class="auth-form-heading">
          <h2 class="auth-form-title">{{ $t('auth.registerTitle') }}</h2>
          <p class="auth-form-subtitle">{{ $t('auth.registerDesc') }}</p>
        </div>

        <!-- Register Form -->
        <form @submit.prevent="handleRegister" class="auth-form-grid" novalidate>
          <!-- Fullname Field -->
          <div class="auth-field-group">
            <label for="reg-name" class="auth-field-label">
              {{ $t('auth.fullNameLabel') }}
              <span class="required-star">*</span>
            </label>
            <div class="auth-input-wrapper">
              <span class="auth-input-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                  <circle cx="12" cy="7" r="4"></circle>
                </svg>
              </span>
              <input
                id="reg-name"
                v-model.trim="registerData.fullname"
                type="text"
                class="auth-text-input"
                placeholder="Nguyễn Văn A"
                autocomplete="name"
                required
              />
            </div>
          </div>

          <!-- Email Field -->
          <div class="auth-field-group">
            <label for="reg-email" class="auth-field-label">
              {{ $t('auth.emailLabel') }}
              <span class="required-star">*</span>
            </label>
            <div class="auth-input-wrapper">
              <span class="auth-input-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                  <polyline points="22,6 12,13 2,6"></polyline>
                </svg>
              </span>
              <input
                id="reg-email"
                v-model.trim="registerData.email"
                type="email"
                class="auth-text-input"
                placeholder="name@company.com"
                autocomplete="email"
                required
              />
            </div>
          </div>

          <!-- Phone Field -->
          <div class="auth-field-group">
            <label for="reg-phone" class="auth-field-label">
              {{ $t('auth.phoneLabel') }}
              <span class="required-star">*</span>
            </label>
            <div class="auth-input-wrapper">
              <span class="auth-input-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
                </svg>
              </span>
              <input
                id="reg-phone"
                v-model.trim="registerData.phone"
                type="tel"
                class="auth-text-input"
                placeholder="0901234567"
                autocomplete="tel"
                pattern="[0-9]{9,15}"
                required
              />
            </div>
          </div>

          <!-- Password Field -->
          <div class="auth-field-group">
            <label for="reg-password" class="auth-field-label">
              {{ $t('auth.passwordLabel') }}
              <span class="required-star">*</span>
            </label>
            <div class="auth-input-wrapper">
              <span class="auth-input-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                </svg>
              </span>
              <input
                id="reg-password"
                v-model="registerData.password"
                :type="showPassword ? 'text' : 'password'"
                class="auth-text-input has-toggle"
                placeholder="•••••••• (Tối thiểu 8 ký tự)"
                minlength="8"
                maxlength="72"
                autocomplete="new-password"
                required
              />
              <button
                type="button"
                class="auth-password-toggle-btn"
                :title="showPassword ? 'Ẩn mật khẩu' : 'Hiện mật khẩu'"
                @click="showPassword = !showPassword"
              >
                <!-- Eye Open -->
                <svg v-if="!showPassword" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                  <circle cx="12" cy="12" r="3"></circle>
                </svg>
                <!-- Eye Off -->
                <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                  <line x1="1" y1="1" x2="23" y2="23"></line>
                </svg>
              </button>
            </div>
          </div>

          <!-- Terms & Privacy Opt-in Checkbox -->
          <div class="auth-terms-checkbox-wrap">
            <label class="auth-terms-checkbox-label">
              <input type="checkbox" v-model="agreeTerms" required class="auth-terms-checkbox" />
              <span class="auth-terms-text">
                Tôi đồng ý với 
                <router-link to="/terms-of-service" target="_blank" class="auth-terms-link">Điều khoản dịch vụ</router-link> 
                &amp; 
                <router-link to="/privacy-policy" target="_blank" class="auth-terms-link">Chính sách bảo mật</router-link> 
                của ACC Academy. <span class="text-danger" style="color: #ef4444;">*</span>
              </span>
            </label>
          </div>

          <!-- Submit Button -->
          <button type="submit" class="auth-submit-btn" :disabled="loading || !agreeTerms">
            <span v-if="loading" class="auth-spinner"></span>
            <span>{{ loading ? $t('auth.signingUp') : $t('auth.signUpBtn') }}</span>
            <svg v-if="!loading" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="5" y1="12" x2="19" y2="12"></line>
              <polyline points="12 5 19 12 12 19"></polyline>
            </svg>
          </button>
        </form>

        <!-- Switch to Login -->
        <p class="auth-switch-prompt">
          {{ $t('auth.hasAccount') }}
          <router-link to="/login" class="auth-switch-link">
            {{ $t('header.login') }} ngay
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useCourseStore } from '@/stores/courses';
import '@/styles/auth.css';

const route = useRoute();
const router = useRouter();
const courseStore = useCourseStore();

const loading = ref(false);
const showPassword = ref(false);
const agreeTerms = ref(false);

const registerData = ref({
  fullname: '',
  email: '',
  phone: '',
  password: ''
});

onMounted(() => {
  if (courseStore.token) {
    router.push('/dashboard');
    return;
  }
});

const handleRegister = async () => {
  if (!agreeTerms.value) {
    courseStore.showToast('Vui lòng đọc và đồng ý với Điều khoản dịch vụ & Chính sách bảo mật!', 'warning');
    return;
  }

  if (!registerData.value.fullname || !registerData.value.email || !registerData.value.password || !registerData.value.phone) {
    courseStore.showToast('Vui lòng điền đầy đủ các thông tin bắt buộc (*)!', 'warning');
    return;
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(registerData.value.email)) {
    courseStore.showToast('Địa chỉ email không hợp lệ!', 'warning');
    return;
  }

  const phoneRegex = /^[0-9]{9,15}$/;
  if (!phoneRegex.test(registerData.value.phone)) {
    courseStore.showToast('Số điện thoại không hợp lệ (cần 9 - 15 chữ số)!', 'warning');
    return;
  }

  if (registerData.value.password.length < 8) {
    courseStore.showToast('Mật khẩu phải chứa ít nhất 8 ký tự!', 'warning');
    return;
  }

  if (registerData.value.password.length > 72) {
    courseStore.showToast('Mật khẩu không được vượt quá 72 ký tự!', 'warning');
    return;
  }

  loading.value = true;
  try {
    await courseStore.register(
      registerData.value.fullname,
      registerData.value.email,
      registerData.value.password,
      '',
      registerData.value.phone
    );

    await courseStore.login(registerData.value.email, registerData.value.password);
    courseStore.showToast('Đăng ký tài khoản thành công! Chào mừng bạn đến với ACC Academy.', 'success');
    router.push('/dashboard');
  } catch (err) {
    courseStore.showToast('Đăng ký thất bại: ' + err.message, 'error');
  } finally {
    loading.value = false;
  }
};
</script>
