<template>
  <!-- Zalo Chat Widget wrapper -->
  <div class="zalo-chat-widget-container"></div>
</template>

<script setup>
import { onMounted } from 'vue';

onMounted(() => {
  if (!window.roarJs) {
    window.roarJs = {};
  }
  
  window.roarJs.ZaloConfig = {
    metafields: {
      shop: "skillsbridgevn.myshopify.com",
      settings: {
        "enabled": "1",
        "param": {
          "type": "oaid",
          "oaid": "2007401187233041513",
          "number": "+84902335354",
          "message": "Bạn cần Skills Bridge hỗ trợ thông tin nào?",
          "autopopup": "0"
        },
        "position": {
          "horizontal": { "value": "left", "unit": "px", "offset": 21 },
          "vertical": { "value": "bottom", "unit": "px", "offset": 100 }
        },
        "style": {
          "gradient": "custom",
          "pattern": "0",
          "custom": { "color": "#ffffff", "background": "#008fe5" },
          "width": "64",
          "avatar": "0",
          "avatar_url": "https://cdn.shopify.com/s/files/1/0184/4255/1360/files/whatsapp_avatar-1.png?v=1565171330"
        },
        "pending": { "enabled": "1", "number": "1", "color": "#ffffff", "background": "#25cac2" },
        "mobile": {
          "enabled": "1",
          "horizontal": { "value": "right", "unit": "px", "offset": "20" },
          "vertical": { "value": "bottom", "unit": "px", "offset": 152 },
          "width": "46"
        },
        "only1": "true"
      },
      moneyFormat: "{{amount_no_decimals_with_comma_separator}}₫"
    }
  };

  // If the zalo script is already loaded, we might need to trigger it
  // Since Zalo live chat initializes itself on page load, let's load it if not loaded
  if (!document.getElementById('zalo-chat-script')) {
    const script = document.createElement('script');
    script.id = 'zalo-chat-script';
    script.src = "/js/zalo.js";
    script.defer = true;
    document.body.appendChild(script);
  }
});
</script>
