/**
 * Convert any Google Drive view/open link to a direct high-res thumbnail image URL.
 * Also works if the URL is from Cloudinary, local /images, or standard HTTP URLs.
 * 
 * Supports:
 * - https://drive.google.com/file/d/FILE_ID/view...
 * - https://drive.google.com/open?id=FILE_ID
 * - https://drive.google.com/uc?id=FILE_ID
 * - Already converted thumbnail links
 */
export function formatImageUrl(url, size = 'w1600') {
  if (!url || typeof url !== 'string') return '';
  const cleanUrl = url.trim();

  // If already a Google Drive thumbnail or direct uc link, adjust size if needed
  if (cleanUrl.includes('drive.google.com/thumbnail')) {
    return cleanUrl;
  }

  // Check if it's a Google Drive file link
  const driveMatch = cleanUrl.match(/drive\.google\.com\/(?:file\/d\/([a-zA-Z0-9_-]+)|open\?id=([a-zA-Z0-9_-]+)|uc\?id=([a-zA-Z0-9_-]+))/i);
  if (driveMatch) {
    const fileId = driveMatch[1] || driveMatch[2] || driveMatch[3];
    if (fileId) {
      return `https://drive.google.com/thumbnail?id=${fileId}&sz=${size}`;
    }
  }

  return cleanUrl;
}
