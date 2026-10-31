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

<style scoped src="@/styles/components/CallButtonWidget.css"></style>
