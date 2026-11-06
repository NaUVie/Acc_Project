/**
 * Bộ lọc từ ngữ tục tĩu, chửi bậy và xúc phạm phía Frontend
 * Giúp cảnh báo sớm cho người dùng trước khi gửi form nhận xét
 */

const PROFANITY_PHRASES = [
  "địt mẹ", "địt mợ", "địt con mẹ", "địt cụ", "địt cha", "đụ má", "đụ mẹ", "đụ cha",
  "đù má", "đù mẹ", "đụ mẹ mày", "chó đẻ", "đồ chó", "óc chó", "súc vật", "súc sinh",
  "ngu lồn", "ngu như chó", "khốn nạn", "mất dạy", "lũ khốn", "mẹ kiếp",
  "con điếm", "con đĩ", "làm đĩ", "đĩ mẹ", "phò phạch", "thằng chó", "thằng rác rưởi",
  "hãm lồn", "cút mẹ mày đi", "bố mày", "mả cha mày", "tổ sư bố", "tổ cha mày",
  "dit me", "dit mo", "dit con me", "dit cu", "du ma", "du me", "du cha", "du con me",
  "du me may", "cho de", "do cho", "oc cho", "suc vat", "suc sinh", "ngu lon",
  "ngu nhu cho", "khon nan", "mat day", "lu khon", "me kiep", "con diem", "con di",
  "lam di", "pho phach", "thang cho", "ham lon", "cut me may di", "bo may",
  "fuck", "fucking", "fucker", "motherfucker", "shit", "bullshit", "bitch",
  "asshole", "bastard", "cunt", "dick", "pussy", "whore", "slut", "wtf"
];

const PROFANITY_WORDS_EXACT = [
  "đm", "đkm", "dkm", "đcm", "dcm", "dm", "vcl", "vkl", "vl", "vcc",
  "clgt", "cl", "cmm", "cmn", "dmm", "đmm", "đệt", "det", "đíu", "diu",
  "đéo", "deo", "địt", "dit", "đụ", "du", "lồn", "lon", "cặc", "cak", "cax",
  "buồi", "buoi", "dái", "dai", "chode", "occho", "sucvat", "ngulon",
  "duma", "dume", "ditme", "đĩ", "di~", "phò", "cave"
];

const LEET_PATTERNS = [
  /đ[\.\-_,\s]*m/i,
  /d[\.\-_,\s]*k[\.\-_,\s]*m/i,
  /d[\.\-_,\s]*c[\.\-_,\s]*m/i,
  /v[\.\-_,\s]*c[\.\-_,\s]*l/i,
  /d[\.\-_,\s]*i[\.\-_,\s]*t/i,
  /đ[\.\-_,\s]*i[\.\-_,\s]*t/i,
  /d[!1]t/i,
  /l[0o]n/i,
  /c[@a]c/i,
  /f[\*uck]+ck/i,
  /sh[\*i]+t/i
];

/**
 * Kiểm tra xem chuỗi có chứa từ ngữ thô tục hay không
 * @param {string} text 
 * @returns {{ isProfane: boolean, word?: string }}
 */
export function checkProfanity(text) {
  if (!text || typeof text !== 'string') return { isProfane: false };

  const clean = text.trim();

  // 1. Cụm từ
  for (const phrase of PROFANITY_PHRASES) {
    const idx = clean.toLowerCase().indexOf(phrase);
    if (idx !== -1) {
      return { isProfane: true, word: phrase };
    }
  }

  // 2. Từ đơn có word boundary
  for (const word of PROFANITY_WORDS_EXACT) {
    const regex = new RegExp(`(?:\\b|_)${word}(?:\\b|_)`, 'i');
    const match = regex.exec(clean);
    if (match) {
      return { isProfane: true, word: match[0] };
    }
  }

  // 3. Leetspeak biến thể
  for (const regex of LEET_PATTERNS) {
    const match = regex.exec(clean);
    if (match) {
      return { isProfane: true, word: match[0] };
    }
  }

  return { isProfane: false };
}

