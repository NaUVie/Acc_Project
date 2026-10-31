import { createI18n } from 'vue-i18n';
import vi from '@/locales/vi.json';
import en from '@/locales/en.json';

let initialLang = 'vi';
if (typeof window !== 'undefined') {
  if (window.location.pathname === '/en' || window.location.pathname.startsWith('/en/')) {
    initialLang = 'en';
  } else {
    initialLang = localStorage.getItem('acc_lang') || 'vi';
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
    }
  }
};

export default i18n;
