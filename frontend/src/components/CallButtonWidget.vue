<template>
  <a 
    href="tel:0938566700" 
    class="phone-call-floating-btn" 
    title="Gọi ngay hotline 0938 566 700" 
    aria-label="Gọi ngay hotline tư vấn"
  >
    <div class="phone-pulse-ring"></div>
    <div class="phone-pulse-ring-2"></div>
    <div class="phone-circle-btn">
      <svg class="phone-svg-icon" viewBox="0 0 24 24" width="28" height="28" fill="currentColor">
        <path d="M6.62 10.79a15.053 15.053 0 006.59 6.59l2.2-2.2a1 1 0 011.01-.24c1.12.37 2.33.57 3.58.57a1 1 0 011 1V20a1 1 0 01-1 1A17 17 0 013 4a1 1 0 011-1h3.5a1 1 0 011 1c0 1.25.2 2.45.57 3.57a1 1 0 01-.25 1.02l-2.2 2.2z"/>
      </svg>
    </div>
    <span class="phone-label-tooltip">0938 566 700</span>
  </a>
</template>

<script setup>
</script>

<style scoped>
.phone-call-floating-btn {
  position: fixed;
  bottom: 24px;
  left: 21px;
  z-index: 2147483646;
  display: flex;
  align-items: center;
  text-decoration: none;
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
}

/* Base button circle */
.phone-circle-btn {
  width: 58px;
  height: 58px;
  border-radius: 50%;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 18px rgba(16, 185, 129, 0.45);
  position: relative;
  z-index: 2;
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.3s ease;
}

.phone-call-floating-btn:hover .phone-circle-btn {
  transform: scale(1.08);
  box-shadow: 0 8px 24px rgba(16, 185, 129, 0.55);
}

.phone-svg-icon {
  animation: phoneVibrate 2.4s infinite ease-in-out;
  transform-origin: center;
}

/* Pulse rings for lively attracting effect */
.phone-pulse-ring,
.phone-pulse-ring-2 {
  position: absolute;
  top: 0;
  left: 0;
  width: 58px;
  height: 58px;
  border-radius: 50%;
  background-color: rgba(16, 185, 129, 0.5);
  z-index: 1;
  pointer-events: none;
  animation: pulseRings 2.2s infinite cubic-bezier(0.25, 0, 0, 1);
}

.phone-pulse-ring-2 {
  animation-delay: 0.7s;
}

@keyframes pulseRings {
  0% {
    transform: scale(0.95);
    opacity: 0.8;
  }
  100% {
    transform: scale(1.65);
    opacity: 0;
  }
}

@keyframes phoneVibrate {
  0%, 100% {
    transform: rotate(0deg);
  }
  10%, 30% {
    transform: rotate(-16deg);
  }
  20%, 40% {
    transform: rotate(16deg);
  }
  50% {
    transform: rotate(0deg);
  }
}

/* Tooltip on desktop */
.phone-label-tooltip {
  display: none;
  margin-left: 10px;
  background: #ffffff;
  color: #065f46;
  font-weight: 800;
  font-size: 14px;
  padding: 6px 14px;
  border-radius: 20px;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.1);
  border: 1px solid #d1fae5;
  white-space: nowrap;
  pointer-events: none;
  opacity: 0;
  transform: translateX(-6px);
  transition: all 0.25s ease;
  z-index: 2;
}

@media (min-width: 769px) {
  .phone-label-tooltip {
    display: inline-block;
  }
  .phone-call-floating-btn:hover .phone-label-tooltip {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Mobile responsive alignment */
@media (max-width: 768px) {
  .phone-call-floating-btn {
    bottom: 86px;
    right: 18px;
    left: auto;
  }
  .phone-circle-btn,
  .phone-pulse-ring,
  .phone-pulse-ring-2 {
    width: 48px;
    height: 48px;
  }
  .phone-svg-icon {
    width: 22px;
    height: 22px;
  }
}
</style>
