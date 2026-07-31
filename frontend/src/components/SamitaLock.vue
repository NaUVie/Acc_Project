<template>
  <!-- Samita Lock Wrapper -->
  <div class="samita-lock-container"></div>
</template>

<script setup>
import { onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();

const initSamita = () => {
  if (!window.Samita) {
    window.Samita = {};
  }
  
  if (!window.Samita.SamitaLocksAccessParams) {
    window.Samita.SamitaLocksAccessParams = {
      cart: { item_count: 0, total_price: 0, currency: "VND", items: [] },
      settings: {
        "general": {
          "customcss": "img[alt=\"smtImage\"] {\r\n content:url(https://cdn.shopify.com/s/files/1/0672/5605/8167/files/Illustration.png?v=1775189541) !important;\r\n    object-fit: contain !important;\r\n    }\r\n    \r\nhtml body .lock__notificationTemplateWrapper img[alt=\"smtImage\"] {\r\n     width:300px !important;\r\n     height:auto !important;\r\n }",
          "price_atc": "plain_text",
          "effect_button": "ripple",
          "collectFeedback": true,
          "placeholder_message": true,
          "placeholder_templateLock": true
        },
        "template": {
          "text_color": "#000",
          "btn_bg_color": "#098f9e",
          "bg_placeholder": "#f3f3f3",
          "btn_text_color": "#ffffff",
          "bg_notification": "#fff",
          "input_box_shadow": "#ccc",
          "plain_text_color": "#230d0d",
          "color_placeholder": "#000",
          "button_priceAtc_bg": "#5487a0",
          "input_passcode_color": "#000",
          "button_priceAtc_color": "#fff",
          "input_passcode_background": "#ffffff"
        }
      },
      locks: [
        {
          "access": 1,
          "id": 41935,
          "resources_conditional": {
            "ip": { "type": "whitelist", "message": "This content is not available in your country", "countries": [] },
            "type": ["passcode"],
            "customer": { "logic": [[{ "type": "tagged_with", "value": null }]], "source": "rules", "listManual": [] },
            "passcode": { "code": null, "message": "Vui lòng nhập mật khẩu", "listCode": [] },
            "redirect": { "type": "login", "modal": { "title": "Restricted Page", "button": "Go to login", "buttonUrl": "/account/login", "description": "You need to log in to access this page" } },
            "secretLink": { "code": [], "links": [], "message": null, "resources": "products" }
          },
          "resources_lock": {
            "url": "/pages/6-khoa-ai-hoc-thu",
            "page": [],
            "type": "url",
            "setting": ["all"],
            "allowHomePage": true
          },
          "status": 1
        },
        {
          "access": 1,
          "id": 40032,
          "resources_conditional": {
            "ip": { "type": "whitelist", "message": "This content is not available in your country", "countries": [] },
            "type": ["passcode"],
            "passcode": { "code": null, "message": "✨ Chào mừng bạn! Hãy nhập mật mã đã nhận để mở khóa nội dung đặc biệt này. Quyền truy cập của bạn sẽ kéo dài trong 3 ngày." },
            "redirect": { "type": "login" }
          },
          "resources_lock": {
            "url": null,
            "page": ["/pages/cach-viet-va-toi-uu-prompt-cho-cau-tra-loi-chat-luong"],
            "type": "page",
            "setting": ["all"],
            "allowHomePage": true
          },
          "status": 1
        },
        {
          "access": 1,
          "id": 20817,
          "resources_conditional": {
            "type": ["passcode"],
            "passcode": { "code": null, "message": "Nắm vững nghệ thuật giao việc hiệu quả để tối ưu hóa năng suất đội ngũ, nâng cao hiệu quả quản lý và đạt được mục tiêu chung." }
          },
          "resources_lock": {
            "url": "/pages/free-course-03-intro",
            "page": [],
            "type": "url",
            "allowHomePage": true
          },
          "status": 1
        },
        {
          "access": 1,
          "id": 20816,
          "resources_conditional": {
            "type": ["passcode"],
            "passcode": { "code": null, "message": "Xây dựng thương hiệu cá nhân vững chắc nhằm nâng cao uy tín và tạo dấu ấn riêng, giúp bạn trở thành lựa chọn hàng đầu trong mọi tình huống công việc." }
          },
          "resources_lock": {
            "url": "/pages/free-course-02-intro",
            "page": [],
            "type": "url",
            "allowHomePage": true
          },
          "status": 1
        },
        {
          "access": 1,
          "id": 20750,
          "resources_conditional": {
            "type": ["passcode"],
            "passcode": { "code": null, "message": "Trang bị kỹ năng thuyết trình chuyên nghiệp để truyền đạt thông điệp một cách thuyết phục, tạo ấn tượng sâu sắc và xây dựng uy tín cá nhân." }
          },
          "resources_lock": {
            "url": "/pages/free-course-01-intro",
            "page": [],
            "type": "url",
            "allowHomePage": true
          },
          "status": 1
        },
        {
          "access": 1,
          "id": 20577,
          "resources_conditional": {
            "type": ["passcode"],
            "passcode": { "code": null, "message": "Khám phá 3 khoá học chuyên sâu: Kỹ năng thuyết trình - nâng cao kỹ thuật thuyết phục và kết nối với khán giả; Xây dựng thương hiệu cá nhân - trở thành người lãnh đạo uy tín và đáng tin cậy; Giao việc hiệu quả - tối ưu hoá năng lực đội ngũ thông qua quản lý nhiệm vụ thông minh." }
          },
          "resources_lock": {
            "url": "/pages/free-course-tat-ca-cac-khoa",
            "page": [],
            "type": "url",
            "allowHomePage": true
          },
          "status": 1
        }
      ],
      appUrl: "https://lock.samita.io",
      translation: {
        "default": {
          "general": {
            "Back": "Back",
            "Submit": "Submit",
            "Enter_passcode": "Nhập passcode",
            "Passcode_empty": "Passcode cant be empty !!",
            "Passcode_incorrect": "Passcode is incorrect !!",
            "This_resource_has_been_locked": "Nội dung này đã được khóa lại",
            "please_enter_passcode_to_unlock": "Vui lòng nhập mật mã để mở khóa nội dung này"
          }
        }
      },
      statusTrial: {},
      current_locale: "vi",
      shopTimezoneOffset: "+0700",
      ListHandle: [],
      ProductsLoad: [],
      proxy_url: "/apps/samita-lock",
      cloudFrontUrl: 'https://d2xaufd1493mkv.cloudfront.net',
      tokenStorefrontSamiLock: "4dfabf6b57a28fc4e013c7fcd24ccf7e",
      pageType: "page"
    };
  }
};

const triggerSamitaCheck = () => {
  if (window.Samita && window.Samita.LockAccess && typeof window.Samita.LockAccess.start === 'function') {
    if (window.Samita.SamitaLocksAccessParams) {
      window.Samita.SamitaLocksAccessParams.pageType = route.path === '/' ? 'index' : 'page';
    }
    
    try {
      window.Samita.LockAccess.start();
    } catch (e) {
      console.warn("Error starting Samita Lock check:", e);
    }
  }
};

onMounted(() => {
  initSamita();

  if (!document.getElementById('samita-lock-script')) {
    const script = document.createElement('script');
    script.id = 'samita-lock-script';
    script.src = "/js/samitaLock.js";
    script.defer = true;
    document.body.appendChild(script);
  } else {
    triggerSamitaCheck();
  }
});

watch(() => route.path, () => {
  triggerSamitaCheck();
});
</script>
