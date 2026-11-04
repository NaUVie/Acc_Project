import { createI18n } from 'vue-i18n';
import vi from '@/locales/vi.json';
import en from '@/locales/en.json';
import { applyGoogleTranslate } from '@/utils/googleTranslate';

let initialLang = 'vi';
if (typeof window !== 'undefined') {
  if (window.location.pathname === '/en' || window.location.pathname.startsWith('/en/')) {
    initialLang = 'en';
  } else {
    initialLang = 'vi';
  }
}

export const i18n = createI18n({
  legacy: false, // Use Composition API mode
  locale: initialLang,
  fallbackLocale: 'vi',
  messages: {
    vi,
    en
  }
});

export const setLanguage = (lang) => {
  if (['vi', 'en'].includes(lang)) {
    i18n.global.locale.value = lang;
    localStorage.setItem('acc_lang', lang);
    if (typeof document !== 'undefined') {
      document.documentElement.lang = lang;
      // Auto Google Translate fallback for anything not covered by en.json
      applyGoogleTranslate(lang);
    }
  }
};

export default i18n;
