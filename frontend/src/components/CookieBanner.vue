<template>
  <transition name="slide-up">
    <div v-if="visible" class="cookie-consent-bar" role="dialog" aria-live="polite" aria-label="Thông báo Cookie">
      <div class="cookie-container">
        <div class="cookie-icon-wrapper">
          <span class="cookie-emoji">🍪</span>
        </div>
        <div class="cookie-text-content">
          <p class="cookie-title">Thông báo Cookie & Bảo mật dữ liệu</p>
          <p class="cookie-desc">
            ACC Academy sử dụng cookie để duy trì phiên đăng nhập, cá nhân hóa trải nghiệm học tập và đảm bảo an toàn hệ thống theo 
            <router-link to="/privacy-policy" class="cookie-privacy-link">Chính sách bảo mật thông tin</router-link>.
          </p>
        </div>
        <div class="cookie-actions">
          <button type="button" @click="acceptCookies" class="btn-cookie-accept">
            Đồng ý
          </button>
          <button type="button" @click="closeBanner" class="btn-cookie-close" title="Đóng thông báo">
            ✕
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const visible = ref(false);

onMounted(() => {
  const consent = localStorage.getItem('acc_cookie_consent');
  if (!consent) {
    // Hiện banner sau 1.2s để không che giấu trang khi vừa vào
    setTimeout(() => {
      visible.value = true;
    }, 1200);
  }
});

const acceptCookies = () => {
  localStorage.setItem('acc_cookie_consent', 'accepted');
  visible.value = false;
};

const closeBanner = () => {
  // Ghi nhận đã đóng phiên này
  sessionStorage.setItem('acc_cookie_dismissed', 'true');
  visible.value = false;
};
</script>

<style scoped>
.cookie-consent-bar {
  position: fixed;
  bottom: 24px;
  left: 24px;
  right: 24px;
  max-width: 680px;
  margin: 0 auto;
  z-index: 9999;
  background: rgba(15, 23, 42, 0.95);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 16px;
  padding: 16px 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.35);
  color: #f1f5f9;
}

.cookie-container {
  display: flex;
  align-items: center;
  gap: 16px;
}

.cookie-icon-wrapper {
  flex-shrink: 0;
  width: 42px;
  height: 42px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.08);
  display: flex;
  align-items: center;
  justify-content: center;
}

.cookie-emoji {
  font-size: 22px;
}

.cookie-text-content {
  flex: 1;
}

.cookie-title {
  font-size: 13.5px;
  font-weight: 700;
  color: #ffffff;
  margin: 0 0 3px 0;
}

.cookie-desc {
  font-size: 12.5px;
  line-height: 1.5;
  color: #94a3b8;
  margin: 0;
}

.cookie-privacy-link {
  color: #38bdf8;
  text-decoration: underline;
  text-underline-offset: 3px;
  transition: color 0.2s;
}

.cookie-privacy-link:hover {
  color: #7dd3fc;
}

.cookie-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
}

.btn-cookie-accept {
  background: linear-gradient(135deg, #022B9F 0%, #0369a1 100%);
  color: #ffffff;
  border: none;
  font-size: 13px;
  font-weight: 700;
  padding: 8px 18px;
  border-radius: 10px;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(2, 43, 159, 0.3);
  transition: all 0.2s ease;
  white-space: nowrap;
}

.btn-cookie-accept:hover {
  filter: brightness(1.15);
  transform: translateY(-1px);
}

.btn-cookie-close {
  background: transparent;
  border: none;
  color: #64748b;
  font-size: 15px;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.btn-cookie-close:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
}

/* Transitions */
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}

.slide-up-enter-from,
.slide-up-leave-to {
  opacity: 0;
  transform: translateY(30px) scale(0.96);
}

@media (max-width: 640px) {
  .cookie-consent-bar {
    left: 14px;
    right: 14px;
    bottom: 14px;
    padding: 14px;
  }
  .cookie-container {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  .cookie-actions {
    width: 100%;
    justify-content: space-between;
  }
  .btn-cookie-accept {
    flex: 1;
    text-align: center;
  }
}
</style>

