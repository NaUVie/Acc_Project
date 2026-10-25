<template>
  <div 
    ref="widgetRef"
    class="contact-speeddial-widget"
    :class="{ 
      'is-open': isOpen, 
      'is-dragging': isDragging,
      'is-snapped-left': snapSide === 'left',
      'is-snapped-right': snapSide === 'right'
    }"
    :style="positionStyle"
    @mouseenter="onMouseEnter"
    @mouseleave="onMouseLeave"
    @mousedown="onMouseDown"
    @touchstart.passive="onTouchStart"
  >
    <!-- Cầu nối vô hình chống rớt chuột giữa nút và danh sách popup -->
    <div v-show="isOpen" class="hover-bridge"></div>

    <!-- Danh sách nút con mở rộng (Zalo & Gọi điện) -->
    <div class="speeddial-actions" :class="{ 'show': isOpen }">
      <!-- 1. Nút Gọi Điện -->
      <a 
        href="tel:0938566700" 
        class="action-item call-action" 
        title="Gọi hotline: 0938 566 700"
        aria-label="Gọi hotline tư vấn"
        @click.stop
      >
        <div class="action-icon call-bg">
          <svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor">
            <path d="M6.62 10.79a15.053 15.053 0 006.59 6.59l2.2-2.2a1 1 0 011.01-.24c1.12.37 2.33.57 3.58.57a1 1 0 011 1V20a1 1 0 01-1 1A17 17 0 013 4a1 1 0 011-1h3.5a1 1 0 011 1c0 1.25.2 2.45.57 3.57a1 1 0 01-.25 1.02l-2.2 2.2z"/>
          </svg>
        </div>
        <span class="action-label">0938 566 700</span>
      </a>

      <!-- 2. Nút Zalo -->
      <a 
        href="https://zalo.me/0938566700" 
        target="_blank" 
        rel="noopener noreferrer" 
        class="action-item zalo-action" 
        title="Chat Zalo ACC Academy"
        aria-label="Chat Zalo"
        @click.stop
      >
        <div class="action-icon zalo-bg">
          <svg viewBox="0 0 48 48" width="26" height="26" fill="none">
            <circle cx="24" cy="24" r="24" fill="#0068FF"/>
            <path d="M12.5 28.5C12.5 35 18 39.5 24.5 39.5C26.5 39.5 28.5 39 30 38L35.5 39.5L34.2 34.5C36 33 37.5 30.5 37.5 27.5C37.5 21 32 16.5 25.5 16.5C18.5 16.5 12.5 21.5 12.5 28.5Z" fill="#0068FF"/>
            <text x="24" y="29.5" text-anchor="middle" fill="#FFFFFF" font-family="-apple-system, BlinkMacSystemFont, Arial, sans-serif" font-weight="900" font-size="14" letter-spacing="-0.5">Zalo</text>
          </svg>
        </div>
        <span class="action-label">Chat Zalo ACC</span>
      </a>
    </div>

    <!-- Nút chính kích hoạt (Floating trigger) -->
    <button 
      type="button"
      class="speeddial-trigger" 
      aria-label="Mở tiện ích liên hệ nhanh"
      @click="onTriggerClick"
    >
      <div class="pulse-ring"></div>
      <div class="pulse-ring-2"></div>
      
      <div class="trigger-inner">
        <!-- Icon Chat khi đóng -->
        <svg v-if="!isOpen" class="trigger-icon chat-icon" viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
          <path d="M8 10h.01M12 10h.01M16 10h.01" stroke-width="3"></path>
        </svg>
        <!-- Icon đóng khi mở -->
        <svg v-else class="trigger-icon close-icon" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </div>
      <span class="trigger-tooltip" v-if="!isOpen && !isDragging">Tư vấn ngay</span>
    </button>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';

const widgetRef = ref(null);
const isOpen = ref(false);
const isDragging = ref(false);
const hasMoved = ref(false);

let closeTimer = null;

// Vị trí mặc định ở bên phải cách mép phải 24px, cách đáy 170px
const posX = ref(window.innerWidth - 82);
const posY = ref(window.innerHeight - 170);
const snapSide = ref('right'); // 'left' hoặc 'right'

const dragStartX = ref(0);
const dragStartY = ref(0);
const initialPosX = ref(0);
const initialPosY = ref(0);

const isMobile = ref(false);
const checkMobile = () => {
  isMobile.value = window.innerWidth <= 768;
};

const positionStyle = computed(() => {
  return {
    top: `${posY.value}px`,
    left: `${posX.value}px`
  };
});

// Laptop: Hover vào mở ra ngay lập tức
const onMouseEnter = () => {
  if (closeTimer) {
    clearTimeout(closeTimer);
    closeTimer = null;
  }
  if (!isMobile.value && !isDragging.value) {
    isOpen.value = true;
  }
};

// Laptop: Hover ra ngoài có độ trễ 400ms để người dùng thoải mái di chuột không bị tắt ngang
const onMouseLeave = () => {
  if (!isMobile.value && !isDragging.value) {
    closeTimer = setTimeout(() => {
      isOpen.value = false;
    }, 400);
  }
};

// Click nút trigger (Trên Mobile hoặc Click cố định trên Laptop)
const onTriggerClick = (e) => {
  if (hasMoved.value) {
    hasMoved.value = false;
    return;
  }
  isOpen.value = !isOpen.value;
};

// Kéo thả bằng chuột trên PC/Laptop
const onMouseDown = (e) => {
  if (e.button !== 0) return;
  startDrag(e.clientX, e.clientY);
  window.addEventListener('mousemove', onMouseMove);
  window.addEventListener('mouseup', onMouseUp);
};

const onMouseMove = (e) => {
  updateDrag(e.clientX, e.clientY);
};

const onMouseUp = () => {
  endDrag();
  window.removeEventListener('mousemove', onMouseMove);
  window.removeEventListener('mouseup', onMouseUp);
};

// Kéo thả bằng cảm ứng trên Mobile / Tablet
const onTouchStart = (e) => {
  const touch = e.touches[0];
  startDrag(touch.clientX, touch.clientY);
  window.addEventListener('touchmove', onTouchMove, { passive: true });
  window.addEventListener('touchend', onTouchEnd);
};

const onTouchMove = (e) => {
  const touch = e.touches[0];
  updateDrag(touch.clientX, touch.clientY);
};

const onTouchEnd = () => {
  endDrag();
  window.removeEventListener('touchmove', onTouchMove);
  window.removeEventListener('touchend', onTouchEnd);
};

const startDrag = (clientX, clientY) => {
  dragStartX.value = clientX;
  dragStartY.value = clientY;
  initialPosX.value = posX.value;
  initialPosY.value = posY.value;
  hasMoved.value = false;
  isDragging.value = true;
};

const updateDrag = (clientX, clientY) => {
  const deltaX = clientX - dragStartX.value;
  const deltaY = clientY - dragStartY.value;
  
  if (Math.abs(deltaX) > 6 || Math.abs(deltaY) > 6) {
    hasMoved.value = true;
  }

  const widgetSize = 58;
  const margin = 12;
  const newX = Math.max(margin, Math.min(window.innerWidth - widgetSize - margin, initialPosX.value + deltaX));
  const newY = Math.max(margin + 60, Math.min(window.innerHeight - widgetSize - margin, initialPosY.value + deltaY));

  posX.value = newX;
  posY.value = newY;
};

const endDrag = () => {
  isDragging.value = false;
  const widgetSize = 58;
  const margin = 20;
  const screenCenter = window.innerWidth / 2;

  if (posX.value + widgetSize / 2 < screenCenter) {
    posX.value = margin;
    snapSide.value = 'left';
  } else {
    posX.value = window.innerWidth - widgetSize - margin;
    snapSide.value = 'right';
  }
};

const handleResize = () => {
  checkMobile();
  const widgetSize = 58;
  const margin = 20;
  if (snapSide.value === 'right') {
    posX.value = window.innerWidth - widgetSize - margin;
  } else {
    posX.value = margin;
  }
  if (posY.value > window.innerHeight - 80) {
    posY.value = window.innerHeight - 150;
  }
};

onMounted(() => {
  checkMobile();
  window.addEventListener('resize', handleResize);
  posX.value = window.innerWidth - 78;
  posY.value = window.innerHeight - 170;
});

onBeforeUnmount(() => {
  if (closeTimer) clearTimeout(closeTimer);
  window.removeEventListener('resize', handleResize);
});
</script>

<style scoped>
.contact-speeddial-widget {
  position: fixed;
  z-index: 2147483646;
  user-select: none;
  touch-action: none;
  /* Padding đệm rộng hơn để chuột không bao giờ bị rơi ra ngoài khi di chuyển */
  padding: 10px;
  margin: -10px;
}

.contact-speeddial-widget:not(.is-dragging) {
  transition: top 0.25s cubic-bezier(0.2, 0.9, 0.4, 1), left 0.3s cubic-bezier(0.2, 0.9, 0.4, 1);
}

/* Cầu nối vô hình bao phủ khoảng trống giữa nút bấm và 2 nút Zalo/Phone */
.hover-bridge {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 200px;
  height: 220px;
  background: transparent;
  pointer-events: auto;
  z-index: 1;
}

.contact-speeddial-widget.is-snapped-left .hover-bridge {
  right: auto;
  left: 0;
}

/* NÚT CHÍNH TRIGGER */
.speeddial-trigger {
  width: 58px;
  height: 58px;
  border-radius: 50%;
  border: none;
  background: transparent;
  cursor: grab;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  outline: none;
  -webkit-tap-highlight-color: transparent;
}

.contact-speeddial-widget.is-dragging .speeddial-trigger {
  cursor: grabbing;
}

.trigger-inner {
  width: 58px;
  height: 58px;
  border-radius: 50%;
  background: linear-gradient(135deg, #022b9f 0%, #1e40af 50%, #2563eb 100%);
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 6px 20px rgba(2, 43, 159, 0.45);
  position: relative;
  z-index: 3;
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.3s ease;
}

.speeddial-trigger:hover .trigger-inner,
.contact-speeddial-widget.is-open .trigger-inner {
  transform: scale(1.08);
  box-shadow: 0 8px 26px rgba(2, 43, 159, 0.6);
}

.trigger-icon {
  animation: floatBounce 3s infinite ease-in-out;
}

.contact-speeddial-widget.is-open .trigger-icon {
  animation: none;
}

/* Sóng xung kích Pulse */
.pulse-ring,
.pulse-ring-2 {
  position: absolute;
  top: 0;
  left: 0;
  width: 58px;
  height: 58px;
  border-radius: 50%;
  background-color: rgba(37, 99, 235, 0.5);
  z-index: 1;
  pointer-events: none;
  animation: speeddialPulse 2.4s infinite cubic-bezier(0.25, 0, 0, 1);
}

.pulse-ring-2 {
  animation-delay: 0.8s;
}

.contact-speeddial-widget.is-open .pulse-ring,
.contact-speeddial-widget.is-open .pulse-ring-2 {
  display: none;
}

/* Tooltip gợi ý trên laptop */
.trigger-tooltip {
  position: absolute;
  right: 68px;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(15, 23, 42, 0.9);
  backdrop-filter: blur(8px);
  color: #ffffff;
  font-size: 13px;
  font-weight: 600;
  padding: 6px 14px;
  border-radius: 20px;
  white-space: nowrap;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.25s ease, transform 0.25s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.contact-speeddial-widget.is-snapped-left .trigger-tooltip {
  right: auto;
  left: 68px;
}

.speeddial-trigger:hover .trigger-tooltip {
  opacity: 1;
  transform: translateY(-50%) translateX(-4px);
}

.contact-speeddial-widget.is-snapped-left .speeddial-trigger:hover .trigger-tooltip {
  transform: translateY(-50%) translateX(4px);
}

/* DANH SÁCH NÚT CON (ACTIONS) */
.speeddial-actions {
  position: absolute;
  bottom: 74px;
  right: 10px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  pointer-events: none;
  opacity: 0;
  transform: translateY(12px) scale(0.92);
  transition: opacity 0.25s cubic-bezier(0.4, 0, 0.2, 1), transform 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 2;
}

.contact-speeddial-widget.is-snapped-left .speeddial-actions {
  right: auto;
  left: 10px;
}

.speeddial-actions.show {
  opacity: 1;
  pointer-events: auto;
  transform: translateY(0) scale(1);
}

.action-item {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  cursor: pointer;
  background: #ffffff;
  padding: 6px 16px 6px 6px;
  border-radius: 32px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.18);
  border: 1px solid rgba(226, 232, 240, 0.9);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.contact-speeddial-widget.is-snapped-left .action-item {
  flex-direction: row-reverse;
  padding: 6px 6px 6px 16px;
}

.action-item:hover {
  transform: scale(1.06) translateX(-3px);
  box-shadow: 0 10px 28px rgba(0, 0, 0, 0.26);
}

.contact-speeddial-widget.is-snapped-left .action-item:hover {
  transform: scale(1.06) translateX(3px);
}

.action-icon {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  flex-shrink: 0;
}

.call-bg {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.45);
}

.zalo-bg {
  background: #0068FF;
  box-shadow: 0 4px 12px rgba(0, 104, 255, 0.45);
}

.action-label {
  font-size: 14px;
  font-weight: 700;
  color: #0f172a;
  white-space: nowrap;
}

@keyframes speeddialPulse {
  0% {
    transform: scale(0.95);
    opacity: 0.8;
  }
  70% {
    transform: scale(1.45);
    opacity: 0;
  }
  100% {
    transform: scale(1.45);
    opacity: 0;
  }
}

@keyframes floatBounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-3px); }
}

@media (max-width: 768px) {
  .trigger-tooltip {
    display: none !important;
  }
}
</style>
