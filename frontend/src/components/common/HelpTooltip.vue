<template>
  <span 
    ref="triggerRef"
    class="help-tooltip-container" 
    @mouseenter="handleMouseEnter" 
    @mouseleave="handleMouseLeave"
    @click.stop="handleClick"
    title=""
  >
    <span 
      class="help-tooltip-icon" 
      :class="{ 'is-active': isVisible }"
      aria-label="Giải thích tính năng" 
      role="button" 
      tabindex="0"
    >
      <svg class="help-svg" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="8" cy="8" r="7" stroke="currentColor" stroke-width="1.3" />
        <path d="M6.2 6.2a2 2 0 0 1 3.7.6c0 1.2-1.9 1.6-1.9 2.7M8 12h.01" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </span>
    
    <teleport to="body" :disabled="!useTeleport">
      <transition name="tooltip-pop">
        <div 
          v-if="isVisible" 
          ref="bubbleRef"
          class="help-tooltip-bubble" 
          :style="floatingStyle"
          @click.stop
        >
          <div class="tooltip-header">
            <span class="tooltip-header-dot"></span>
            <span class="tooltip-header-text">ACC Trợ Giúp</span>
          </div>
          <div class="tooltip-desc">{{ desc }}</div>
          <div v-if="impact" class="tooltip-impact">
            <div class="impact-badge">
              <svg width="11" height="11" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="8" cy="8" r="6.5" stroke="currentColor" stroke-width="1.3"/>
                <path d="M8 1.5v13M1.5 8h13M3 4.5c2 1 8 1 10 0M3 11.5c2-1 8-1 10 0" stroke="currentColor" stroke-width="1.2"/>
              </svg>
              <span>Vị trí trên Web</span>
            </div>
            <div class="impact-text">{{ impact }}</div>
          </div>
          <span class="tooltip-arrow" :class="'arrow-' + resolvedPosition"></span>
        </div>
      </transition>
    </teleport>
  </span>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue';

const props = defineProps({
  desc: {
    type: String,
    required: true
  },
  impact: {
    type: String,
    default: ''
  },
  position: {
    type: String,
    default: 'top' // 'top', 'bottom', 'left', 'right'
  },
  useTeleport: {
    type: Boolean,
    default: true
  }
});

const isVisible = ref(false);
const triggerRef = ref(null);
const bubbleRef = ref(null);
const resolvedPosition = ref(props.position || 'top');
const coords = ref({ top: 0, left: 0 });

let hoverTimer = null;

const updateCoords = () => {
  if (!triggerRef.value) return;
  const rect = triggerRef.value.getBoundingClientRect();
  const scrollX = window.scrollX || window.pageXOffset || 0;
  const scrollY = window.scrollY || window.pageYOffset || 0;

  const bubbleW = 260; // Max bubble width
  let targetTop = rect.top + scrollY;
  let targetLeft = rect.left + scrollX + rect.width / 2;

  // Auto flip if near top edge of window
  if (props.position === 'top' && rect.top < 110) {
    resolvedPosition.value = 'bottom';
  } else if (props.position === 'bottom' && window.innerHeight - rect.bottom < 110) {
    resolvedPosition.value = 'top';
  } else {
    resolvedPosition.value = props.position || 'top';
  }

  if (resolvedPosition.value === 'top') {
    targetTop = rect.top + scrollY - 9;
  } else if (resolvedPosition.value === 'bottom') {
    targetTop = rect.bottom + scrollY + 9;
  }

  // Prevent right and left screen overflow
  const maxLeft = window.innerWidth + scrollX - bubbleW / 2 - 16;
  const minLeft = scrollX + bubbleW / 2 + 16;
  targetLeft = Math.max(minLeft, Math.min(targetLeft, maxLeft));

  coords.value = {
    top: Math.round(targetTop),
    left: Math.round(targetLeft)
  };
};

const show = () => {
  if (hoverTimer) clearTimeout(hoverTimer);
  updateCoords();
  isVisible.value = true;
  nextTick(() => {
    updateCoords();
  });
};

const hide = () => {
  hoverTimer = setTimeout(() => {
    isVisible.value = false;
  }, 100);
};

const handleMouseEnter = () => {
  show();
};

const handleMouseLeave = () => {
  hide();
};

const handleClick = () => {
  if (isVisible.value) {
    hide();
  } else {
    show();
  }
};

const handleDocumentClick = (e) => {
  if (triggerRef.value && !triggerRef.value.contains(e.target)) {
    isVisible.value = false;
  }
};

const handleScrollOrResize = () => {
  if (isVisible.value) {
    updateCoords();
  }
};

onMounted(() => {
  document.addEventListener('click', handleDocumentClick, { passive: true });
  window.addEventListener('resize', handleScrollOrResize, { passive: true });
  window.addEventListener('scroll', handleScrollOrResize, { passive: true });
});

onUnmounted(() => {
  if (hoverTimer) clearTimeout(hoverTimer);
  document.removeEventListener('click', handleDocumentClick);
  window.removeEventListener('resize', handleScrollOrResize);
  window.removeEventListener('scroll', handleScrollOrResize);
});

const floatingStyle = computed(() => {
  if (!props.useTeleport) return {};
  const isTop = resolvedPosition.value === 'top';
  return {
    top: `${coords.value.top}px`,
    left: `${coords.value.left}px`,
    transform: isTop ? 'translate(-50%, -100%)' : 'translate(-50%, 0)'
  };
});
</script>

<style scoped>
.help-tooltip-container {
  display: inline-flex;
  align-items: center;
  position: relative;
  vertical-align: middle;
  line-height: 1;
  margin-left: 6px;
  cursor: pointer;
  user-select: none;
}

/* Icon tròn mang nhận diện ACC Academy: Nền xanh lam nhạt, viền thanh mảnh, icon xanh dương hoàng gia */
.help-tooltip-icon {
  width: 17px;
  height: 17px;
  border-radius: 50%;
  background: #eef4ff; /* Xanh nhạt sang trọng */
  color: #022B9F;     /* ACC Royal Blue */
  border: 1px solid #bfdbfe;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 1px 2px rgba(2, 43, 159, 0.08);
  flex-shrink: 0;
  box-sizing: border-box;
}

.help-svg {
  width: 11.5px;
  height: 11.5px;
  display: block;
  transition: transform 0.22s ease;
}

/* Hiệu ứng rê chuột: Đổi gradient thương hiệu xanh ACC, tỏa sáng nhẹ */
.help-tooltip-container:hover .help-tooltip-icon,
.help-tooltip-icon.is-active {
  background: linear-gradient(135deg, #022B9F 0%, #1e40af 100%);
  color: #ffffff;
  border-color: #022B9F;
  box-shadow: 0 3px 10px rgba(2, 43, 159, 0.35);
  transform: scale(1.12);
}

.help-tooltip-container:hover .help-svg {
  transform: rotate(12deg);
}

/* Khung pop-up giải thích: Thẻ trắng sang trọng, đường line thương hiệu ACC Royal Blue trên cùng, bóng mờ cao cấp */
.help-tooltip-bubble {
  position: absolute;
  background: #ffffff;
  color: #0f172a;
  padding: 10px 14px 12px;
  border-radius: 10px;
  font-size: 12px;
  line-height: 1.5;
  width: max-content;
  max-width: 260px;
  box-shadow: 0 14px 32px -4px rgba(2, 43, 159, 0.16), 0 4px 14px rgba(15, 23, 42, 0.06);
  border: 1px solid #e2e8f0;
  border-top: 3px solid #022B9F;
  z-index: 999999;
  text-align: left;
  pointer-events: none;
  font-family: 'Mulish', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  box-sizing: border-box;
}

/* Header nhỏ chỉ định */
.tooltip-header {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 10px;
  font-weight: 800;
  color: #022B9F;
  text-transform: uppercase;
  letter-spacing: 0.6px;
  margin-bottom: 5px;
  font-family: 'Manrope', -apple-system, sans-serif;
}

.tooltip-header-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: #022B9F;
  display: inline-block;
}

/* Mô tả tính năng */
.tooltip-desc {
  display: block;
  color: #334155;
  font-size: 12px;
  line-height: 1.5;
  font-weight: 500;
}

/* Khối thông tin tác động ra ngoài website */
.tooltip-impact {
  display: flex;
  flex-direction: column;
  gap: 3px;
  margin-top: 8px;
  padding: 7px 9px;
  background: #f0f7ff;
  border-left: 2.5px solid #022B9F;
  border-radius: 4px;
}

.impact-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: #022B9F;
  font-weight: 800;
  font-size: 9.5px;
  text-transform: uppercase;
  letter-spacing: 0.4px;
  font-family: 'Manrope', -apple-system, sans-serif;
}

.impact-text {
  color: #1e3a8a;
  font-size: 11px;
  line-height: 1.4;
  font-weight: 500;
}

/* Mũi tên chỉ hướng */
.tooltip-arrow {
  position: absolute;
  width: 9px;
  height: 9px;
  box-sizing: border-box;
}

.tooltip-arrow.arrow-top {
  bottom: -5px;
  left: 50%;
  margin-left: -5px;
  background: #ffffff;
  border-right: 1px solid #e2e8f0;
  border-bottom: 1px solid #e2e8f0;
  transform: rotate(45deg);
}

.tooltip-arrow.arrow-bottom {
  top: -5px;
  left: 50%;
  margin-left: -5px;
  background: #022B9F;
  transform: rotate(45deg);
}

/* Animation mở mượt */
.tooltip-pop-enter-active,
.tooltip-pop-leave-active {
  transition: opacity 0.16s ease, transform 0.16s cubic-bezier(0.16, 1, 0.3, 1);
}

.tooltip-pop-enter-from,
.tooltip-pop-leave-to {
  opacity: 0;
}
</style>
