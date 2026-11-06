"""
Bộ lọc từ ngữ tục tĩu, chửi bậy và xúc phạm (Profanity Filter)
Bảo vệ hệ thống đánh giá/bình luận khóa học trước các hành vi xấu.
"""
import re
from typing import Tuple, Optional

# Danh sách từ/cụm từ chửi thề, tục tĩu tiếng Việt & tiếng Anh
PROFANITY_PHRASES = [
    # Tiếng Việt có dấu / đầy đủ
    "địt mẹ", "địt mợ", "địt con mẹ", "địt cụ", "địt cha", "đụ má", "đụ mẹ", "đụ cha",
    "đù má", "đù mẹ", "đụ mẹ mày", "chó đẻ", "đồ chó", "óc chó", "súc vật", "súc sinh",
    "ngu lồn", "ngu như chó", "khốn nạn", "mất dạy", "lũ khốn", "mẹ kiếp",
    "con điếm", "con đĩ", "làm đĩ", "đĩ mẹ", "phò phạch", "thằng chó", "thằng rác rưởi",
    "hãm lồn", "cút mẹ mày đi", "bố mày", "mả cha mày", "tổ sư bố", "tổ cha mày",

    # Không dấu ghép cụm
    "dit me", "dit mo", "dit con me", "dit cu", "du ma", "du me", "du cha", "du con me",
    "du me may", "cho de", "do cho", "oc cho", "suc vat", "suc sinh", "ngu lon",
    "ngu nhu cho", "khon nan", "mat day", "lu khon", "me kiep", "con diem", "con di",
    "lam di", "pho phach", "thang cho", "ham lon", "cut me may di", "bo may",

    # Tiếng Anh
    "fuck", "fucking", "fucker", "motherfucker", "shit", "bullshit", "bitch",
    "asshole", "bastard", "cunt", "dick", "pussy", "whore", "slut", "wtf"
]

# Các từ đơn/từ viết tắt cần kiểm tra theo ranh giới từ (\b) để tránh false-positive
# (Ví dụ: 'vl' không được match trong 'vui lòng', 'cl' không match trong 'classic')
PROFANITY_WORDS_EXACT = [
    # Viết tắt phổ biến
    r"đm", r"đkm", r"dkm", r"đcm", r"dcm", r"dm", r"vcl", r"vkl", r"vl", r"vcc",
    r"clgt", r"cl", r"cmm", r"cmn", r"dmm", r"đmm", r"đệt", r"det", r"đíu", r"diu",
    r"đéo", r"deo", r"đệt",

    # Từ đơn tục tĩu
    r"địt", r"dit", r"đụ", r"du", r"lồn", r"lon", r"cặc", r"cak", r"cax",
    r"buồi", r"buoi", r"dái", r"dai", r"chode", r"occho", r"sucvat", r"ngulon",
    r"duma", r"dume", r"ditme", r"đĩ", r"di~", r"phò", r"cave"
]

# Biên dịch regex sẵn để tối ưu hiệu năng
_PHRASE_REGEXES = [
    re.compile(re.escape(phrase), re.IGNORECASE) for phrase in PROFANITY_PHRASES
]

_WORD_REGEXES = [
    re.compile(r"(?:\b|_)" + word + r"(?:\b|_)", re.IGNORECASE) for word in PROFANITY_WORDS_EXACT
]

# Thêm quy tắc biến thể ký tự leetspeak/teencode (ví dụ: đ.m, d-m, d_m, d!t, l0n, c@c)
_LEET_REGEXES = [
    re.compile(r"đ[\.\-_,\s]*m", re.IGNORECASE),
    re.compile(r"d[\.\-_,\s]*k[\.\-_,\s]*m", re.IGNORECASE),
    re.compile(r"d[\.\-_,\s]*c[\.\-_,\s]*m", re.IGNORECASE),
    re.compile(r"v[\.\-_,\s]*c[\.\-_,\s]*l", re.IGNORECASE),
    re.compile(r"d[\.\-_,\s]*i[\.\-_,\s]*t", re.IGNORECASE),
    re.compile(r"đ[\.\-_,\s]*i[\.\-_,\s]*t", re.IGNORECASE),
    re.compile(r"d[!1]t", re.IGNORECASE),
    re.compile(r"l[0o]n", re.IGNORECASE),
    re.compile(r"c[@a]c", re.IGNORECASE),
    re.compile(r"f[\*uck]+ck", re.IGNORECASE),
    re.compile(r"sh[\*i]+t", re.IGNORECASE),
]


def check_profanity(text: str) -> Tuple[bool, Optional[str]]:
    """
    Kiểm tra xem văn bản có chứa từ ngữ chửi bậy, xúc phạm hay không.
    Trả về (True, matched_term) nếu phát hiện, hoặc (False, None) nếu văn bản sạch.
    """
    if not text or not text.strip():
        return False, None

    clean_text = text.strip()

    # 1. Kiểm tra các cụm từ xúc phạm
    for regex in _PHRASE_REGEXES:
        match = regex.search(clean_text)
        if match:
            return True, match.group(0)

    # 2. Kiểm tra các từ viết tắt / từ đơn tục
    for regex in _WORD_REGEXES:
        match = regex.search(clean_text)
        if match:
            return True, match.group(0)

    # 3. Kiểm tra các biến thể leetspeak
    for regex in _LEET_REGEXES:
        match = regex.search(clean_text)
        if match:
            return True, match.group(0)

    return False, None


def censor_profanity(text: str, replacement: str = "***") -> str:
    """
    Thay thế các từ ngữ thô tục bằng ký tự che chắn (***).
    """
    if not text:
        return ""

    censored = text
    for regex in _PHRASE_REGEXES:
        censored = regex.sub(replacement, censored)
    for regex in _WORD_REGEXES:
        censored = regex.sub(replacement, censored)
    for regex in _LEET_REGEXES:
        censored = regex.sub(replacement, censored)

    return censored


# ==================== SPAM DETECTION ====================

SPAM_URL_REGEX = re.compile(
    r"(?:https?://|www\.|t\.me/|zalo\.me/g/|bit\.ly/|tinyurl\.com/|[a-zA-Z0-9\-_]{2,}\.(?:com|vn|net|org|xyz|top|club|site|online|vip|live|bet|ru|cn))\b",
    re.IGNORECASE
)

SPAM_PHONE_REGEX = re.compile(
    r"(?:\+84|0)(?:3[2-9]|5[2689]|7[06-9]|8[1-9]|9[0-9])[\s\.\-_]*\d{3}[\s\.\-_]*\d{4}"
)

SPAM_KEYWORDS = [
    # Cờ bạc, cá cược, game bài
    "cờ bạc", "cá cược", "cá độ", "lô đề", "đánh đề", "nổ hũ", "game bài", "bắn cá",
    "ku bet", "kubet", "thabet", "fun88", "w88", "188bet", "casino", "tai xiu", "tài xỉu",
    "kéo tài xỉu", "đổi thưởng",
    # Cho vay tín dụng đen
    "vay tiền", "vay nóng", "bốc bát họ", "tín dụng đen", "cho vay lãi",
    # Khiêu dâm / 18+
    "gái gọi", "chat sex", "gọi tình", "khiêu dâm", "phim sex",
    # Dịch vụ giả mạo / spam
    "mua bằng", "bằng giả", "chứng chỉ giả", "hack pass", "tool hack"
]

_SPAM_KEYWORD_REGEXES = [
    re.compile(r"(?:\b|_)" + re.escape(kw) + r"(?:\b|_)", re.IGNORECASE) for kw in SPAM_KEYWORDS
]


def detect_spam(*texts: Optional[str]) -> Tuple[bool, Optional[str]]:
    """
    Tự động phát hiện dấu hiệu nghi ngờ spam trong nhận xét / đánh giá:
    - Chứa link/domain quảng cáo trái phép.
    - Chứa số điện thoại chèn trong nội dung nhận xét.
    - Chứa các từ khóa cờ bạc, cá cược, vay nóng, khiêu dâm.
    
    Trả về (True, lý_do_spam) nếu nghi ngờ, hoặc (False, None) nếu bình thường.
    """
    for text in texts:
        if not text or not str(text).strip():
            continue
        clean = str(text).strip()

        # 1. Phát hiện đường link / URL quảng cáo
        if SPAM_URL_REGEX.search(clean):
            return True, "Chứa liên kết / domain quảng cáo"

        # 2. Phát hiện số điện thoại chèn trong nhận xét
        if SPAM_PHONE_REGEX.search(clean):
            return True, "Chứa số điện thoại liên hệ bất thường"

        # 3. Phát hiện từ khóa spam cờ bạc, vay nóng, tệ nạn
        for regex in _SPAM_KEYWORD_REGEXES:
            match = regex.search(clean)
            if match:
                return True, f"Chứa từ khóa nghi ngờ spam ('{match.group(0)}')"

        # 4. Phát hiện ký tự lặp liên tục dị thường (ví dụ: aaaaaaaa, !!!!!!!!)
        if re.search(r"(.)\1{7,}", clean):
            return True, "Ký tự lặp lại bất thường"

    return False, None


