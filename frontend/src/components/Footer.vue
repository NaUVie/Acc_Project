<template>
  <footer class="custom-footer">
    <div class="custom-footer-container">
      <div class="custom-footer-top">
        <!-- Col 1: Brand & Doanh nghiệp -->
        <div class="custom-footer-col brand-col">
          <router-link to="/" class="custom-footer-logo" aria-label="Trang chủ ACC Academy">
            <img src="/images/logo3.png" alt="ACC Academy" class="footer-logo-img" loading="lazy">
          </router-link>
          <p class="custom-footer-company">
            <strong>CÔNG TY CỔ PHẦN KẾT NỐI TRI THỨC ACC</strong>
          </p>
          <p class="custom-footer-slogan">
            {{ $t('footer.aboutText') }}
          </p>
          <div class="contact-compact-list">
            <div class="compact-row" v-if="contactInfo.taxCode">
              <span class="compact-label">MST:</span>
              <span class="compact-text">{{ contactInfo.taxCode }}</span>
            </div>
            <div class="compact-row">
              <span class="compact-label">{{ $t('footer.address') }}:</span>
              <span class="compact-text">{{ contactInfo.address }}</span>
            </div>
            <div class="compact-row">
              <span class="compact-label">Hotline:</span>
              <span class="compact-text"><a :href="'tel:' + rawPhone">{{ contactInfo.hotline }}</a></span>
            </div>
            <div class="compact-row">
              <span class="compact-label">Email:</span>
              <span class="compact-text"><a :href="'mailto:' + contactInfo.email">{{ contactInfo.email }}</a></span>
            </div>
          </div>
        </div>

        <!-- Col 2: Về ACC & Đào tạo -->
        <div class="custom-footer-col nav-col">
          <h4 class="custom-footer-heading">{{ $t('footer.trainingPrograms') }}</h4>
          <ul class="custom-footer-linklist">
            <li v-for="cat in footerCategories" :key="cat.slug">
              <router-link :to="'/courses/category/' + cat.slug">{{ cat.name }}</router-link>
            </li>
            <li><router-link to="/admissions">{{ $t('footer.andrewsMba') }}</router-link></li>
                        <li><router-link to="/lecturers">{{ $t('footer.lecturersTeam') }}</router-link></li>
          </ul>
        </div>

        <!-- Col 3: Chính sách & Pháp lý (Chuẩn VNPAY) -->
        <div class="custom-footer-col nav-col">
          <h4 class="custom-footer-heading">{{ $t('footer.policies') }}</h4>
          <ul class="custom-footer-linklist">
            <li><router-link to="/terms-of-service">{{ $t('footer.termsOfService') }}</router-link></li>
            <li><router-link to="/privacy-policy">{{ $t('footer.privacyPolicy') }}</router-link></li>
            <li><router-link to="/refund-policy">{{ $t('footer.refundPolicy') }}</router-link></li>
            <li><router-link to="/payment-guide">{{ $t('footer.paymentGuide') }}</router-link></li>
            <li><router-link to="/delivery-policy">{{ $t('footer.deliveryPolicy') }}</router-link></li>
          </ul>
        </div>

        <!-- Col 4: Kết nối Zalo OA & Hỗ trợ -->
        <div class="custom-footer-col connect-col">
          <h4 class="custom-footer-heading">{{ $t('footer.support') }}</h4>
          
          <div class="footer-qr-zalo">
            <div class="qr-zalo-img-wrapper">
              <img src="/images/QR_Zalo.jpg" alt="QR Zalo ACC Academy" class="qr-zalo-img" loading="lazy" />
            </div>
            <div class="qr-zalo-info">
              <span class="qr-zalo-title">Zalo Official Account</span>
              <span class="qr-zalo-desc">{{ $t('footer.support247') }}</span>
              <a :href="contactInfo.zalo" target="_blank" rel="noopener" class="btn-chat-zalo" style="display: inline-flex; align-items: center; gap: 6px;">
                <span>{{ $t('footer.chatZalo') }}</span>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="5" y1="12" x2="19" y2="12"></line>
                  <polyline points="12 5 19 12 12 19"></polyline>
                </svg>
              </a>
            </div>
          </div>


        </div>
      </div>

      <!-- Bottom Bar -->
      <div class="custom-footer-bottom">
        <p class="copyright-text">
          &copy; 2026 <strong>ACC Academy</strong>. {{ $t('footer.copyright') }}
        </p>
        <div class="footer-bottom-links">
          <router-link to="/privacy-policy">{{ $t('footer.privacy') }}</router-link>
          <span class="dot">•</span>
          <router-link to="/terms-of-service">{{ $t('footer.terms') }}</router-link>
          <span class="dot">•</span>
          <router-link to="/contact">{{ $t('nav.contact') }}</router-link>
          <span class="dot">•</span>
          <button type="button" class="footer-lang-btn" @click="toggleLang" :title="currentLang === 'vi' ? 'Switch to English' : 'Chuyển sang Tiếng Việt'">
            <span class="footer-lang-flag">{{ currentLang === 'vi' ? '🇻🇳' : '🇬🇧' }}</span>
            <span class="footer-lang-name">{{ currentLang === 'vi' ? 'Tiếng Việt' : 'English' }}</span>
          </button>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { setLanguage } from '@/i18n';
import { clearGoogleTranslate } from '@/utils/googleTranslate';
import { useCourseStore } from '@/stores/courses';

const router = useRouter();
const { locale } = useI18n();

const isEnActive = () => {
  if (locale.value === 'en') return true;
  if (typeof document !== 'undefined') {
    if (document.cookie.includes('googtrans=/vi/en') || document.documentElement.classList.contains('translated-ltr')) {
      return true;
    }
  }
  if (typeof window !== 'undefined' && localStorage.getItem('acc_lang') === 'en') {
    return true;
  }
  return false;
};

const currentLang = computed(() => isEnActive() ? 'en' : 'vi');

const toggleLang = () => {
  const route = router.currentRoute.value;
  const isEnCurrently = isEnActive();

  // Functional / admin pages have no /en version: just switch the UI language in place
  if ((route.meta && route.meta.noLocale) || route.path.startsWith('/admin')) {
    const nextLang = isEnCurrently ? 'vi' : 'en';
    if (nextLang === 'vi') {
      clearGoogleTranslate();
      setLanguage('vi');
    } else {
      setLanguage('en');
    }
    window.location.reload();
    return;
  }
  const currentPath = route.fullPath;
  if (!isEnCurrently) {
    setLanguage('en');
    let newPath = '/en' + (currentPath === '/' ? '' : currentPath);
    if (!newPath) newPath = '/en';
    window.location.href = newPath;
  } else {
    clearGoogleTranslate();
    setLanguage('vi');
    let newPath = currentPath.replace(/^\/en(\/|$)/, '/');
    if (!newPath) newPath = '/';
    window.location.href = newPath;
  }
};

const courseStore = useCourseStore();
const footerCategories = computed(() => {
  return (courseStore.categories || []).filter(c => c.slug !== 'bundles');
});

onMounted(() => {
  if (!courseStore.contactSettings) {
    courseStore.fetchContactSettings();
  }
});

const contactInfo = computed(() => {
  const s = courseStore.contactSettings;
  return {
    taxCode: s?.taxCode || '0317696611',
    address: s?.address || '156 Nam Kỳ Khởi Nghĩa, Phường Bến Nghé, Quận 1, TP. HCM',
    hotline: s?.hotline || '0938 566 700',
    email: s?.email || 'info@acc-edu.vn',
    zalo: s?.zalo || 'https://zalo.me/0938566700'
  };
});

const rawPhone = computed(() => {
  return contactInfo.value.hotline.replace(/\s+/g, '');
});
</script>

<style scoped src="@/styles/components/Footer.css"></style>
