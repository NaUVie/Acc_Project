<template>
  <a 
    href="https://zalo.me/0938566700" 
    target="_blank" 
    rel="noopener noreferrer" 
    class="zalo-floating-btn" 
    title="Chat Zalo với ACC Academy (0938 566 700)" 
    aria-label="Chat Zalo hỗ trợ tư vấn"
  >
    <div class="zalo-pulse-ring"></div>
    <div class="zalo-pulse-ring-2"></div>
    <div class="zalo-circle-btn">
      <svg viewBox="0 0 48 48" width="34" height="34" fill="none">
        <circle cx="24" cy="24" r="24" fill="#0068FF"/>
        <path d="M12.5 28.5C12.5 35 18 39.5 24.5 39.5C26.5 39.5 28.5 39 30 38L35.5 39.5L34.2 34.5C36 33 37.5 30.5 37.5 27.5C37.5 21 32 16.5 25.5 16.5C18.5 16.5 12.5 21.5 12.5 28.5Z" fill="#0068FF"/>
        <text x="24" y="29.5" text-anchor="middle" fill="#FFFFFF" font-family="-apple-system, BlinkMacSystemFont, Arial, sans-serif" font-weight="900" font-size="14.5" letter-spacing="-0.5">Zalo</text>
      </svg>
    </div>
    <span class="zalo-label-tooltip">Chat Zalo ACC</span>
  </a>
</template>

<script setup>
</script>

<style scoped>
.zalo-floating-btn {
  position: fixed;
  bottom: 96px;
  left: 21px;
  z-index: 2147483646;
  display: flex;
  align-items: center;
  text-decoration: none;
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
}

/* Base button circle */
.zalo-circle-btn {
  width: 58px;
  height: 58px;
  border-radius: 50%;
  background: #0068FF;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 18px rgba(0, 104, 255, 0.45);
  position: relative;
  z-index: 2;
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.3s ease;
}

.zalo-floating-btn:hover .zalo-circle-btn {
  transform: scale(1.08);
  box-shadow: 0 8px 24px rgba(0, 104, 255, 0.55);
}

/* Pulse rings for attracting attention */
.zalo-pulse-ring,
.zalo-pulse-ring-2 {
  position: absolute;
  top: 0;
  left: 0;
  width: 58px;
  height: 58px;
  border-radius: 50%;
  background-color: rgba(0, 104, 255, 0.5);
  z-index: 1;
  pointer-events: none;
  animation: zaloPulseRings 2.2s infinite cubic-bezier(0.25, 0, 0, 1);
}

.zalo-pulse-ring-2 {
  animation-delay: 0.7s;
}

@keyframes zaloPulseRings {
  0% {
    transform: scale(0.95);
    opacity: 0.8;
  }
  100% {
    transform: scale(1.65);
    opacity: 0;
  }
}

/* Tooltip on desktop */
.zalo-label-tooltip {
  display: none;
  margin-left: 10px;
  background: #ffffff;
  color: #0068FF;
  font-weight: 800;
  font-size: 14px;
  padding: 6px 14px;
  border-radius: 20px;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.1);
  border: 1px solid #bfdbfe;
  white-space: nowrap;
  pointer-events: none;
  opacity: 0;
  transform: translateX(-6px);
  transition: all 0.25s ease;
  z-index: 2;
}

@media (min-width: 769px) {
  .zalo-label-tooltip {
    display: inline-block;
  }
  .zalo-floating-btn:hover .zalo-label-tooltip {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Mobile responsive alignment */
@media (max-width: 768px) {
  .zalo-floating-btn {
    bottom: 148px;
    right: 18px;
    left: auto;
  }
  .zalo-circle-btn,
  .zalo-pulse-ring,
  .zalo-pulse-ring-2 {
    width: 48px;
    height: 48px;
  }
  .zalo-circle-btn svg {
    width: 28px;
    height: 28px;
  }
}
</style>
