/**
 * Convert any Google Drive view/open/thumbnail link to Google's fast edge CDN (lh3.googleusercontent.com).
 * This eliminates Google Drive rate limiting (429 / 403) and third-party cookie issues.
 * Also works if the URL is from Cloudinary, local /images, or standard HTTP URLs.
 */
export function formatImageUrl(url, size = 's1600') {
  if (!url || typeof url !== 'string') return '';
  const cleanUrl = url.trim();

  // Normalize size parameter (e.g. 'w400' -> 's400', 'w1600' -> 's1600')
  const normSize = (size.startsWith('w') || size.startsWith('h')) ? `s${size.slice(1)}` : size;

  // Check if it's any Google Drive link (file/d, open?id=, uc?id=, thumbnail?id=) or lh3 link
  const driveMatch = cleanUrl.match(/(?:drive\.google\.com\/(?:file\/d\/|open\?id=|uc\?id=|thumbnail\?id=)|lh3\.googleusercontent\.com\/d\/)([a-zA-Z0-9_-]+)/i);
  if (driveMatch && driveMatch[1]) {
    const fileId = driveMatch[1];
    return `https://lh3.googleusercontent.com/d/${fileId}=${normSize}`;
  }

  return cleanUrl;
}
