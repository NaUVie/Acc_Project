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
            HỖ TRỢ TÀI KHOẢN
          </div>

          <h1 class="brand-lead-title">
            Yêu cầu cấp lại mật khẩu
          </h1>

          <p class="brand-lead-desc">
            Cung cấp thông tin tài khoản học viên của bạn để Ban quản trị ACC Academy xác minh và hỗ trợ đặt lại mật khẩu nhanh chóng.
          </p>

          <!-- 3 Steps -->
          <div class="brand-perks-list">
            <div class="brand-perk-item">
              <div class="perk-icon-circle">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                  <polyline points="22,6 12,13 2,6"></polyline>
                </svg>
              </div>
              <div>
                <div class="perk-content-title">1. Gửi thông tin tài khoản</div>
                <div class="perk-content-subtitle">Nhập chính xác Email bạn đã đăng ký tại hệ thống</div>
              </div>
            </div>

            <div class="brand-perk-item">
              <div class="perk-icon-circle">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                  <polyline points="22 4 12 14.01 9 11.01"></polyline>
                </svg>
              </div>
              <div>
                <div class="perk-content-title">2. Tiếp nhận &amp; Xác thực</div>
                <div class="perk-content-subtitle">Ban quản trị kiểm tra và liên hệ hỗ trợ bạn</div>
              </div>
            </div>

            <div class="brand-perk-item">
              <div class="perk-icon-circle">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                </svg>
              </div>
              <div>
                <div class="perk-content-title">3. Khôi phục quyền truy cập</div>
                <div class="perk-content-subtitle">Mật khẩu mới được cấp để bạn tiếp tục lộ trình học</div>
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
        <!-- Back Link -->
        <div style="margin-bottom: 20px;">
          <router-link to="/login" class="auth-forgot-link" style="display: inline-flex; align-items: center; gap: 6px;">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <line x1="19" y1="12" x2="5" y2="12"></line>
              <polyline points="12 19 5 12 12 5"></polyline>
            </svg>
            Quay lại Đăng nhập
          </router-link>
        </div>

        <!-- State 1: Form Not Submitted -->
        <div v-if="!submitted">
          <div class="auth-form-heading">
            <h2 class="auth-form-title">Quên mật khẩu</h2>
            <p class="auth-form-subtitle">Điền thông tin bên dưới, Ban quản trị sẽ hỗ trợ cấp lại mật khẩu cho bạn.</p>
          </div>

          <form @submit.prevent="handleSubmit" class="auth-form-grid" novalidate>
            <!-- Email -->
            <div class="auth-field-group">
              <label for="reset-email" class="auth-field-label">
                Email tài khoản đã đăng ký
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
                  id="reset-email"
                  v-model.trim="resetForm.email"
                  type="email"
                  class="auth-text-input"
                  placeholder="name@company.com"
                  autocomplete="email"
                  required
                />
              </div>
            </div>

            <!-- Phone -->
            <div class="auth-field-group">
              <div class="auth-field-label-row">
                <label for="reset-phone" class="auth-field-label">
                  Số điện thoại liên hệ
                </label>
                <span style="font-size: 12px; color: #64748b;">Khuyên dùng để liên hệ nhanh</span>
              </div>
              <div class="auth-input-wrapper">
                <span class="auth-input-icon">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
                  </svg>
                </span>
                <input
                  id="reset-phone"
                  v-model.trim="resetForm.phone"
                  type="tel"
                  class="auth-text-input"
                  placeholder="0901234567"
                  autocomplete="tel"
                />
              </div>
            </div>

            <!-- Note / Reason -->
            <div class="auth-field-group">
              <label for="reset-note" class="auth-field-label">
                Ghi chú thêm (Nếu có)
              </label>
              <textarea
                id="reset-note"
                v-model.trim="resetForm.note"
                class="auth-textarea"
                rows="3"
                placeholder="Ví dụ: Tôi không nhớ mật khẩu cũ, cần hỗ trợ kiểm tra khóa học..."
              ></textarea>
            </div>

            <!-- Anti-spam Honeypot field (hidden from view and bots will auto-fill) -->
            <div style="opacity: 0; position: absolute; top: 0; left: -9999px; height: 0; width: 0; z-index: -1; overflow: hidden; pointer-events: none;" aria-hidden="true">
              <label for="fax_forgot">Do not fill this</label>
              <input type="text" id="fax_forgot" v-model="honeypotValue" autocomplete="off" tabindex="-1" />
            </div>

            <!-- Submit Button -->
            <button type="submit" class="auth-submit-btn" :disabled="loading">
              <span v-if="loading" class="auth-spinner"></span>
              <span>{{ loading ? 'Đang gửi yêu cầu...' : 'Gửi yêu cầu hỗ trợ' }}</span>
              <svg v-if="!loading" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="22" y1="2" x2="11" y2="13"></line>
                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
              </svg>
            </button>
          </form>

          <p class="auth-switch-prompt" style="margin-top: 24px;">
            Nhớ mật khẩu rồi?
            <router-link to="/login" class="auth-switch-link">
              Đăng nhập ngay
            </router-link>
          </p>
        </div>

        <!-- State 2: Form Submitted Successfully -->
        <div v-else class="auth-success-box animate-fade-in">
          <div class="auth-success-icon">
            <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
          </div>

          <h3 class="auth-success-title">Đã gửi yêu cầu thành công!</h3>
          <p class="auth-success-desc">
            Yêu cầu cấp lại mật khẩu cho tài khoản <strong>{{ submittedEmail }}</strong> đã được chuyển tới Ban quản trị ACC Academy.
            Chúng tôi sẽ kiểm tra và liên hệ hỗ trợ bạn trong thời gian sớm nhất.
          </p>

          <div class="auth-contact-actions">
            <a
              v-if="contactZalo"
              :href="contactZalo"
              target="_blank"
              rel="noopener noreferrer"
              class="auth-contact-btn btn-zalo"
            >
              💬 Nhắn tin Zalo hỗ trợ ngay
            </a>

            <button type="button" @click="resetAnother" class="auth-contact-btn btn-back">
              Gửi lại yêu cầu khác
            </button>

            <router-link to="/login" class="auth-contact-btn btn-back">
              Quay về trang Đăng nhập
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useCourseStore } from '@/stores/courses';
import { validateVietnamesePhone, validateEmail } from '@/utils/validation';
import '@/styles/auth.css';

const router = useRouter();
const courseStore = useCourseStore();

const loading = ref(false);
const submitted = ref(false);
const submittedEmail = ref('');
const contactZalo = ref('https://zalo.me/0901234567');
const honeypotValue = ref('');

const resetForm = ref({
  email: '',
  phone: '',
  note: ''
});

onMounted(async () => {
  // If user is already logged in, redirect to dashboard
  if (courseStore.token) {
    router.push('/dashboard');
    return;
  }

  // Fetch contact settings for actual Zalo link if available
  try {
    if (courseStore.fetchContactSettings) {
      await courseStore.fetchContactSettings();
      if (courseStore.contactSettings?.zalo) {
        contactZalo.value = courseStore.contactSettings.zalo;
      }
    }
  } catch (e) {
    // Silent fallback
  }
});

const handleSubmit = async () => {
  const emailCheck = validateEmail(resetForm.value.email);
  if (!emailCheck.isValid) {
    courseStore.showToast(emailCheck.error, 'warning');
    return;
  }

  let cleanPhone = null;
  if (resetForm.value.phone && resetForm.value.phone.trim()) {
    const phoneCheck = validateVietnamesePhone(resetForm.value.phone);
    if (!phoneCheck.isValid) {
      courseStore.showToast(phoneCheck.error, 'warning');
      return;
    }
    cleanPhone = phoneCheck.normalized;
  }

  loading.value = true;
  try {
    await courseStore.requestPasswordReset(
      emailCheck.email,
      cleanPhone,
      resetForm.value.note,
      honeypotValue.value
    );

    submittedEmail.value = emailCheck.email;
    submitted.value = true;
    courseStore.showToast('Yêu cầu đã được gửi đến Ban quản trị thành công! Chúng tôi sẽ kiểm tra và hỗ trợ bạn sớm nhất.', 'success');
  } catch (err) {
    courseStore.showToast('Không thể gửi yêu cầu: ' + (err.message || 'Lỗi kết nối máy chủ'), 'error');
  } finally {
    loading.value = false;
  }
};

const resetAnother = () => {
  resetForm.value = {
    email: '',
    phone: '',
    note: ''
  };
  submitted.value = false;
};
</script>

