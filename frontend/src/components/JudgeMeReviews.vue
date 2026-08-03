<template>
  <div class="judgeme-reviews-wrapper">
    <div 
      class="jdgm-widget jdgm-review-widget" 
      :data-id="productId || 'shopify-default'" 
      :data-product-title="productTitle"
      :data-product-type="productType"
    ></div>
  </div>
</template>

<script setup>
import { onMounted, defineProps } from 'vue';

const props = defineProps({
  productId: String,
  productTitle: String,
  productType: String
});

onMounted(() => {
  // Check if Judge.me settings are set
  if (!window.jdgmSettings) {
    window.jdgmSettings = {
      pagination: 5,
      disable_web_reviews: false,
      badge_no_review_text: "5",
      widget_title: "Đánh giá của Khách hàng",
      platform: "shopify",
      locale: "vi",
      shop_currency: "VND",
      widget_version: "3.0"
    };
  }

  // Load Judge.me core script if not loaded
  if (!window.jdgm) {
    window.jdgm = window.jdgm || {};
    window.jdgm.CDN_HOST = "https://cdnwidget.judge.me/";
    window.jdgm.API_HOST = "https://api.judge.me/";
    window.jdgm.CDN_BASE_URL = "https://cdn.shopify.com/extensions/019fa440-b46f-7094-9ecf-aac8c6e13872/judgeme-657/assets/";
    
    const script = document.createElement('script');
    script.src = "https://cdn.shopify.com/extensions/019fa440-b46f-7094-9ecf-aac8c6e13872/judgeme-657/assets/shopify_v2.js";
    script.async = true;
    document.head.appendChild(script);
  } else if (window.jdgm && typeof window.jdgm.customizeWidgets === 'function') {
    try {
      window.jdgm.customizeWidgets();
    } catch (e) {
      console.warn("Error calling customizeWidgets:", e);
    }
  }
});
</script>

<style src="@/styles/components/JudgeMeReviews.css"></style>
