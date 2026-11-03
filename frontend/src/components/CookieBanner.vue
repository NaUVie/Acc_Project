<template>
  <transition name="cookie-pop">
    <div v-if="visible" class="cookie-card-toast" role="dialog" aria-live="polite" aria-label="Thông báo Cookie">
      <div class="cookie-card-header">
        <div class="cookie-title-group">
          <div class="cookie-brand-icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
            </svg>
          </div>
          <span class="cookie-card-title">Quyền riêng tư & Cookie</span>
        </div>
        <button type="button" @click="closeBanner" class="cookie-dismiss-btn" title="Đóng thông báo">
          ✕
        </button>
      </div>

      <p class="cookie-card-body">
        Chúng tôi sử dụng cookie nhằm tối ưu hóa trải nghiệm học tập và bảo mật thông tin theo 
        <router-link to="/privacy-policy" class="cookie-link">Chính sách bảo mật</router-link> của ACC Academy.
      </p>

      <div class="cookie-card-actions">
        <button type="button" @click="closeBanner" class="btn-cookie-decline">
          Từ chối
        </button>
        <button type="button" @click="acceptCookies" class="btn-cookie-accept">
          Đồng ý
        </button>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const visible = ref(false);

onMounted(() => {
  const consent = localStorage.getItem('acc_cookie_consent');
  const dismissed = sessionStorage.getItem('acc_cookie_dismissed');
  if (!consent && !dismissed) {
    setTimeout(() => {
      visible.value = true;
    }, 1500);
  }
});

const acceptCookies = () => {
  localStorage.setItem('acc_cookie_consent', 'accepted');
  visible.value = false;
};

const closeBanner = () => {
  sessionStorage.setItem('acc_cookie_dismissed', 'true');
  visible.value = false;
};
</script>

<style scoped>
/* Giao diện trắng sáng đồng bộ với Brand Identity của ACC Academy */
.cookie-card-toast {
  position: fixed;
  bottom: 24px;
  left: 24px;
  width: 360px;
  max-width: calc(100vw - 48px);
  z-index: 999;
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(2, 43, 159, 0.14);
  border-radius: 16px;
  padding: 16px 18px;
  box-shadow: 0 16px 36px -8px rgba(2, 43, 159, 0.16), 0 4px 16px rgba(0, 0, 0, 0.04);
  color: #1e293b;
  font-family: inherit;
}

.cookie-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.cookie-title-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.cookie-brand-icon {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  background: #eff6ff;
  color: #022B9F;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.cookie-card-title {
  font-size: 13.5px;
  font-weight: 700;
  color: #0f172a;
}

.cookie-dismiss-btn {
  background: transparent;
  border: none;
  color: #94a3b8;
  font-size: 14px;
  width: 24px;
  height: 24px;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  padding: 0;
}

.cookie-dismiss-btn:hover {
  background: #f1f5f9;
  color: #334155;
}

.cookie-card-body {
  font-size: 12px;
  line-height: 1.55;
  color: #64748b;
  margin: 0 0 14px 0;
}

.cookie-link {
  color: #022B9F;
  font-weight: 600;
  text-decoration: underline;
  text-underline-offset: 2px;
  transition: color 0.2s;
}

.cookie-link:hover {
  color: #0284c7;
}

.cookie-card-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
}

.btn-cookie-decline {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  color: #64748b;
  font-size: 12px;
  font-weight: 600;
  padding: 6px 14px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-cookie-decline:hover {
  background: #f1f5f9;
  color: #334155;
}

.btn-cookie-accept {
  background: linear-gradient(135deg, #022B9F 0%, #0369a1 100%);
  color: #ffffff;
  border: none;
  font-size: 12px;
  font-weight: 700;
  padding: 6px 16px;
  border-radius: 8px;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(2, 43, 159, 0.25);
  transition: all 0.2s ease;
}

.btn-cookie-accept:hover {
  filter: brightness(1.1);
  transform: translateY(-1px);
}

/* Hiệu ứng trồi lên tinh tế ở góc màn hình */
.cookie-pop-enter-active,
.cookie-pop-leave-active {
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.cookie-pop-enter-from,
.cookie-pop-leave-to {
  opacity: 0;
  transform: translateY(20px) scale(0.95);
}

@media (max-width: 640px) {
  .cookie-card-toast {
    left: 16px;
    right: 16px;
    bottom: 16px;
    width: auto;
    max-width: none;
  }
}
</style>
