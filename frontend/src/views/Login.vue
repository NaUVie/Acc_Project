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
            Học viện Đào tạo &amp; Ứng dụng Thực chiến
          </h1>

          <p class="brand-lead-desc">
            Đồng hành cùng bạn trên hành trình nâng cao năng lực làm chủ công nghệ, AI và kỹ năng quản trị thực tiễn.
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
                <div class="perk-content-title">Ứng dụng thực tiễn</div>
                <div class="perk-content-subtitle">Nội dung học bám sát công việc và thao tác thực tế</div>
              </div>
            </div>

            <div class="brand-perk-item">
              <div class="perk-icon-circle">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                  <circle cx="9" cy="7" r="4"></circle>
                  <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                  <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                </svg>
              </div>
              <div>
                <div class="perk-content-title">Đội ngũ giảng viên thực chiến</div>
                <div class="perk-content-subtitle">Chia sẻ kinh nghiệm thực tế qua các tình huống thực tế</div>
              </div>
            </div>

            <div class="brand-perk-item">
              <div class="perk-icon-circle">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
                  <line x1="8" y1="21" x2="16" y2="21"></line>
                  <line x1="12" y1="17" x2="12" y2="21"></line>
                </svg>
              </div>
              <div>
                <div class="perk-content-title">Học tập chủ động</div>
                <div class="perk-content-subtitle">Theo dõi bài giảng và quản lý tiến độ học tập tiện lợi</div>
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
          <button class="auth-nav-pill active" type="button">
            {{ $t('header.login') }}
          </button>
          <router-link to="/register" class="auth-nav-pill">
            {{ $t('header.register') }}
          </router-link>
        </div>

        <!-- Form Heading -->
        <div class="auth-form-heading">
          <h2 class="auth-form-title">{{ $t('auth.loginTitle') }}</h2>
          <p class="auth-form-subtitle">{{ $t('auth.loginDesc') }}</p>
        </div>

        <!-- Login Form -->
        <form @submit.prevent="handleLogin" class="auth-form-grid" novalidate>
          <!-- Email Field -->
          <div class="auth-field-group">
            <label for="login-email" class="auth-field-label">
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
                id="login-email"
                v-model.trim="loginData.email"
                type="email"
                class="auth-text-input"
                placeholder="name@company.com"
                autocomplete="email"
                required
              />
            </div>
          </div>

          <!-- Password Field -->
          <div class="auth-field-group">
            <div class="auth-field-label-row">
              <label for="login-password" class="auth-field-label">
                {{ $t('auth.passwordLabel') }}
                <span class="required-star">*</span>
              </label>
              <router-link to="/forgot-password" class="auth-forgot-link">
                {{ $t('auth.forgotPassword') }}
              </router-link>
            </div>
            <div class="auth-input-wrapper">
              <span class="auth-input-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                </svg>
              </span>
              <input
                id="login-password"
                v-model="loginData.password"
                :type="showPassword ? 'text' : 'password'"
                class="auth-text-input has-toggle"
                placeholder="••••••••"
                autocomplete="current-password"
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

          <!-- Options Row (Remember Me) -->
          <div class="auth-options-row">
            <label class="auth-remember-label">
              <input type="checkbox" v-model="rememberMe" class="auth-checkbox" />
              <span>Ghi nhớ tài khoản</span>
            </label>
          </div>

          <!-- Submit Button -->
          <button type="submit" class="auth-submit-btn" :disabled="loading">
            <span v-if="loading" class="auth-spinner"></span>
            <span>{{ loading ? $t('auth.signingIn') : $t('auth.signInBtn') }}</span>
            <svg v-if="!loading" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="5" y1="12" x2="19" y2="12"></line>
              <polyline points="12 5 19 12 12 19"></polyline>
            </svg>
          </button>
        </form>

        <!-- Switch to Register -->
        <p class="auth-switch-prompt">
          {{ $t('auth.noAccount') }}
          <router-link to="/register" class="auth-switch-link">
            {{ $t('header.register') }} ngay
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useCourseStore } from '@/stores/courses';
import '@/styles/auth.css';

const router = useRouter();
const courseStore = useCourseStore();

const loading = ref(false);
const showPassword = ref(false);
const rememberMe = ref(true);

const loginData = ref({
  email: '',
  password: ''
});

onMounted(() => {
  if (courseStore.token) {
    router.push('/dashboard');
    return;
  }

  const savedEmail = localStorage.getItem('acc_saved_email');
  if (savedEmail) {
    loginData.value.email = savedEmail;
    rememberMe.value = true;
  }
});

const forgotPassword = () => {
  if (!loginData.value.email) {
    courseStore.showToast('Vui lòng nhập Email tài khoản để nhận hướng dẫn khôi phục mật khẩu!', 'warning');
    return;
  }
  courseStore.showToast(`Yêu cầu đặt lại mật khẩu đã được gửi tới Email ${loginData.value.email}. Vui lòng kiểm tra hộp thư!`, 'info');
};

const handleLogin = async () => {
  if (!loginData.value.email || !loginData.value.password) {
    courseStore.showToast('Vui lòng điền đầy đủ Email và Mật khẩu!', 'warning');
    return;
  }

  loading.value = true;
  try {
    await courseStore.login(loginData.value.email, loginData.value.password);

    if (rememberMe.value) {
      localStorage.setItem('acc_saved_email', loginData.value.email);
    } else {
      localStorage.removeItem('acc_saved_email');
    }

    courseStore.showToast('Đăng nhập thành công! Chào mừng bạn quay trở lại.', 'success');
    router.push('/dashboard');
  } catch (err) {
    courseStore.showToast('Đăng nhập thất bại: ' + err.message, 'error');
  } finally {
    loading.value = false;
  }
};
</script>
