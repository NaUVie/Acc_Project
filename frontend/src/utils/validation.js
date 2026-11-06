/**
 * Bộ kiểm tra tính hợp lệ (Validation utilities) cho Số điện thoại & Email Việt Nam
 */

/**
 * Chuẩn hóa số điện thoại:
 * - Loại bỏ khoảng trắng, dấu chấm, dấu gạch nối, dấu ngoặc
 * - Chuyển mã quốc gia +84 hoặc 84 về đầu số 0
 * @param {string} phone
 * @returns {string}
 */
export function normalizeVietnamesePhone(phone) {
  if (!phone) return '';
  let clean = String(phone).trim().replace(/[\s.\-()]/g, '');
  if (clean.startsWith('+84')) {
    clean = '0' + clean.slice(3);
  } else if (clean.startsWith('84') && clean.length >= 11) {
    clean = '0' + clean.slice(2);
  }
  return clean;
}

/**
 * Kiểm tra tính hợp lệ của số điện thoại Việt Nam
 * Hỗ trợ:
 * - Số di động 10 số: bắt đầu bằng 03, 05, 07, 08, 09 (Viettel, Vina, Mobi, Vietnamobile, Wintel, Itelecom...)
 * - Số bàn cố định 11 số: bắt đầu bằng 02 (024, 028...)
 * @param {string} phone
 * @returns {{ isValid: boolean, error?: string, normalized?: string }}
 */
export function validateVietnamesePhone(phone) {
  if (!phone || !String(phone).trim()) {
    return { isValid: false, error: 'Vui lòng nhập số điện thoại liên hệ' };
  }

  const clean = normalizeVietnamesePhone(phone);

  if (!/^\d+$/.test(clean)) {
    return { isValid: false, error: 'Số điện thoại chỉ được chứa các chữ số' };
  }

  // Mobile: 10 chữ số (03x, 05x, 07x, 08x, 09x)
  const isMobile = /^0[35789]\d{8}$/.test(clean);
  // Landline: 11 chữ số (02x)
  const isLandline = /^02\d{9}$/.test(clean);

  if (isMobile || isLandline) {
    return { isValid: true, normalized: clean };
  }

  if (clean.length < 10) {
    return {
      isValid: false,
      error: `Số điện thoại quá ngắn (cần 10 chữ số, hiện có ${clean.length} số)`
    };
  }

  if (clean.length > 11) {
    return {
      isValid: false,
      error: `Số điện thoại quá dài (tối đa 10 chữ số di động, hiện có ${clean.length} số)`
    };
  }

  return {
    isValid: false,
    error: 'Đầu số không hợp lệ (Vui lòng dùng đầu số 03, 05, 07, 08, 09 hoặc 02)'
  };
}

/**
 * Kiểm tra tính hợp lệ của địa chỉ Email
 * @param {string} email
 * @returns {{ isValid: boolean, error?: string, email?: string }}
 */
export function validateEmail(email) {
  if (!email || !String(email).trim()) {
    return { isValid: false, error: 'Vui lòng nhập địa chỉ email' };
  }

  const clean = String(email).trim();

  // Chuẩn regex RFC 5322 cơ bản: tên + @ + tên miền + .đuôi miền ít nhất 2 ký tự
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

  if (!emailRegex.test(clean)) {
    return {
      isValid: false,
      error: 'Địa chỉ email không đúng định dạng (Ví dụ: hotro@acc-edu.vn hoặc name@gmail.com)'
    };
  }

  return { isValid: true, email: clean.toLowerCase() };
}

