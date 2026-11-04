/**
 * Hybrid Google Translate Helper for ACC Academy
 * Combines curated vue-i18n manual translations with Google Translate
 * for all dynamic/untranslated content (Courses, Roadmaps, Blogs, Admissions, etc.)
 */

export function clearGoogleTranslate() {
  if (typeof window === 'undefined' || typeof document === 'undefined') return;

  const hostname = window.location.hostname;
  const domainParts = hostname.split('.');
  const domains = [
    '', // host-only cookie
    hostname,
    '.' + hostname
  ];
  if (domainParts.length > 2) {
    domains.push('.' + domainParts.slice(-2).join('.'));
  }

  const paths = ['/', '', window.location.pathname];

  domains.forEach(d => {
    paths.forEach(p => {
      const dAttr = d ? `domain=${d};` : '';
      const pAttr = p ? `path=${p};` : '';
      document.cookie = `googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; ${pAttr} ${dAttr}`;
    });
  });

  try {
    localStorage.removeItem('googtrans');
    sessionStorage.removeItem('googtrans');
  } catch (e) {}

  // Remove styling classes and inline styles added by Google Translate
  try {
    document.documentElement.classList.remove('translated-ltr', 'translated-rtl');
    document.body.classList.remove('translated-ltr', 'translated-rtl');
    document.body.style.top = '0px';
    document.body.style.position = '';
  } catch (e) {}
}

export function applyGoogleTranslate(lang) {
  if (typeof window === 'undefined' || typeof document === 'undefined') return;

  // IMPORTANT: Vietnamese is the native authoring language of ACC Academy.
  // We MUST NEVER ask Google Translate to translate back to Vietnamese because:
  // 1) The DOM is already translated to English.
  // 2) Google Translate would machine reverse-translate English -> Vietnamese, corrupting original texts!
  // Instead, switching to 'vi' completely purges Google Translate cookies.
  if (lang === 'vi') {
    clearGoogleTranslate();
    return;
  }

  if (lang === 'en') {
    const target = '/vi/en';
    const hostname = window.location.hostname;
    const domains = [
      '',
      hostname,
      '.' + hostname
    ];
    const hostParts = hostname.split('.');
    if (hostParts.length > 2) {
      domains.push('.' + hostParts.slice(-2).join('.'));
    }

    // Set cookie for English translation
    domains.forEach(d => {
      const dAttr = d ? `domain=${d};` : '';
      document.cookie = `googtrans=${target}; path=/; ${dAttr}`;
    });

    // Trigger Google Translate combo dropdown to 'en'
    const triggerSelect = () => {
      const select = document.querySelector('.goog-te-combo');
      if (select) {
        if (select.value !== 'en') {
          select.value = 'en';
          select.dispatchEvent(new Event('change'));
        }
        return true;
      }
      return false;
    };

    if (!triggerSelect()) {
      setTimeout(triggerSelect, 300);
      setTimeout(triggerSelect, 800);
      setTimeout(triggerSelect, 1600);
    }
  }
}
