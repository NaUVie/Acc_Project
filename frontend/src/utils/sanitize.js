const FORBIDDEN_TAGS = new Set([
  'SCRIPT', 'OBJECT', 'EMBED', 'APPLET', 'FORM', 'INPUT',
  'BUTTON', 'TEXTAREA', 'SELECT', 'OPTION', 'META', 'LINK',
  'STYLE', 'BASE', 'SVG', 'MATH', 'TEMPLATE', 'NOSCRIPT'
]);

const SAFE_IFRAME_HOSTS = [
  'www.youtube.com',
  'youtube.com',
  'www.youtube-nocookie.com',
  'player.vimeo.com',
  'drive.google.com'
];

const URL_ATTRIBUTES = new Set(['href', 'src', 'xlink:href', 'action', 'formaction', 'poster']);

function isSafeUrl(val) {
  const cleaned = String(val || '').replace(/[\u0000-\u0020]+/g, '').toLowerCase();
  if (
    cleaned.startsWith('javascript:') ||
    cleaned.startsWith('vbscript:') ||
    cleaned.startsWith('data:text/') ||
    cleaned.startsWith('data:application/')
  ) {
    return false;
  }
  return true;
}

/**
 * Sanitizes rich HTML strings before rendering with v-html to prevent XSS attacks.
 * @param {string} dirtyHtml
 * @returns {string}
 */
export function sanitizeHtml(dirtyHtml) {
  if (!dirtyHtml || typeof dirtyHtml !== 'string') {
    return '';
  }

  // Fallback for non-DOM environments
  if (typeof window === 'undefined' || typeof DOMParser === 'undefined') {
    return dirtyHtml
      .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
      .replace(/\son\w+\s*=\s*(?:"[^"]*"|'[^']*'|[^\s>]+)/gi, '')
      .replace(/javascript\s*:/gi, '');
  }

  const parser = new DOMParser();
  const doc = parser.parseFromString(dirtyHtml, 'text/html');

  const elements = Array.from(doc.body.querySelectorAll('*'));
  for (const el of elements) {
    const tag = el.tagName.toUpperCase();

    if (FORBIDDEN_TAGS.has(tag)) {
      el.remove();
      continue;
    }

    if (tag === 'IFRAME') {
      const src = el.getAttribute('src') || '';
      try {
        const parsed = new URL(src, window.location.origin);
        const allowed = SAFE_IFRAME_HOSTS.some(
          host => parsed.hostname === host || parsed.hostname.endsWith('.' + host)
        );
        if (!allowed || !['http:', 'https:'].includes(parsed.protocol)) {
          el.remove();
          continue;
        }
      } catch {
        el.remove();
        continue;
      }
    }

    // Inspect and clean attributes
    const attrs = Array.from(el.attributes);
    for (const attr of attrs) {
      const name = attr.name.toLowerCase();
      const val = attr.value || '';

      // Strip all event handlers (onclick, onerror, onload, etc.)
      if (name.startsWith('on') || name === 'srcdoc') {
        el.removeAttribute(attr.name);
        continue;
      }

      if (URL_ATTRIBUTES.has(name) && !isSafeUrl(val)) {
        el.removeAttribute(attr.name);
        continue;
      }

      if (name === 'style') {
        if (/expression\s*\(|javascript\s*:|vbscript\s*:|-moz-binding/i.test(val)) {
          el.removeAttribute('style');
        }
      }
    }
  }

  return doc.body.innerHTML;
}

