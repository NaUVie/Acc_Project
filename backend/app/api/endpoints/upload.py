from fastapi import APIRouter, UploadFile, File, HTTPException, status, Query, Depends, BackgroundTasks
from fastapi.responses import Response
from starlette.concurrency import run_in_threadpool
from pydantic import BaseModel
from typing import Optional, List
import urllib.request
import urllib.parse
import re
import cloudinary
import cloudinary.uploader
from ...config import (
    CLOUDINARY_CLOUD_NAME,
    CLOUDINARY_API_KEY,
    CLOUDINARY_API_SECRET,
    CLOUDINARY_FOLDER
)

router = APIRouter()

# Configure Cloudinary SDK
cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
    secure=True
)

from ... import auth, models
from ...rate_limit import rate_limit

ALLOWED_IMAGE_TYPES = {"image/png", "image/jpeg", "image/jpg", "image/webp", "image/gif"}
ALLOWED_VIDEO_TYPES = {"video/mp4", "video/webm"}
MAX_IMAGE_SIZE = 15 * 1024 * 1024  # 15 MB
MAX_VIDEO_SIZE = 50 * 1024 * 1024  # 50 MB


def extract_cloudinary_public_id(url_or_id: str, folder_name: str = CLOUDINARY_FOLDER) -> Optional[str]:
    """
    Robustly extract the Cloudinary public_id from a URL or raw ID string.
    Handles versions (/v12345/), transformations (/c_scale,w_800/), query params (?v=1),
    and URL encoding (%20 -> space).
    """
    if not url_or_id:
        return None
    clean = urllib.parse.unquote(url_or_id.strip()).split('?')[0]
    folder = folder_name.strip() if folder_name else ''
    
    if not ('cloudinary.com' in clean or (folder and folder in clean)):
        return None

    # If already a public_id (e.g. 'Acc Demo/filename')
    if not clean.startswith('http://') and not clean.startswith('https://'):
        return re.sub(r'\.[a-zA-Z0-9]+$', '', clean)

    # If folder name is present in URL (e.g. ".../Acc Demo/filename.webp")
    if folder and f'/{folder}/' in clean:
        idx = clean.find(f'/{folder}/')
        rel = clean[idx + 1:]
        return re.sub(r'\.[a-zA-Z0-9]+$', '', rel)

    # If /v\d+/ version exists
    m = re.search(r'/v\d+/(.+?)(?:\.[a-zA-Z0-9]+)?$', clean)
    if m:
        return m.group(1)

    # Fallback: segment after /upload/
    m = re.search(r'/upload/(?:[^/]+/)*(?:v\d+/)?(.+?)(?:\.[a-zA-Z0-9]+)?$', clean)
    if m:
        return m.group(1)

    return None


def _delete_cloudinary_sync(public_id: str):
    """Synchronous worker function to delete an asset from Cloudinary."""
    try:
        cloudinary.uploader.destroy(public_id, resource_type="image", invalidate=True)
    except Exception as e:
        print(f"Background Cloudinary delete error for '{public_id}': {e}")


@router.get(
    "/proxy-image",
    dependencies=[Depends(rate_limit(max_requests=30, window_seconds=60, scope="proxy_image"))]
)
async def proxy_image(url: str = Query(..., description="URL của ảnh cần tải qua proxy")):
    """
    Proxy an external image (e.g. from Google Drive) to bypass browser CORS restrictions during cropping.
    Returns the raw image stream with Access-Control-Allow-Origin headers.
    Protected against SSRF by validating allowed domains and schemes.
    """
    if not url:
        raise HTTPException(status_code=400, detail="URL không hợp lệ")

    clean_url = url.strip()
    
    # Check if it's a Google Drive link
    drive_match = re.search(r'(?:drive\.google\.com/(?:file/d/|open\?id=|uc\?id=|thumbnail\?id=)|lh3\.googleusercontent\.com/d/)([a-zA-Z0-9_-]+)', clean_url, re.IGNORECASE)
    target_url = clean_url
    if drive_match and drive_match.group(1):
        file_id = drive_match.group(1)
        target_url = f"https://drive.google.com/thumbnail?id={file_id}&sz=w1600"

    # Validate scheme and domain to prevent SSRF
    parsed = urllib.parse.urlparse(target_url)
    if parsed.scheme not in ("http", "https"):
        raise HTTPException(status_code=400, detail="Giao thức URL không được hỗ trợ!")
        
    hostname = (parsed.hostname or "").lower()
    allowed_domains = (
        "drive.google.com",
        "googleusercontent.com",
        "cloudinary.com",
    )
    is_allowed = any(hostname == d or hostname.endswith("." + d) for d in allowed_domains)
    if not is_allowed:
        raise HTTPException(
            status_code=400, 
            detail="Chỉ hỗ trợ tải ảnh từ Google Drive hoặc Cloudinary!"
        )

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    def fetch_proxy_data(url_to_fetch):
        req = urllib.request.Request(url_to_fetch, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            content_type = resp.headers.get_content_type() or "image/jpeg"
            data = resp.read(15 * 1024 * 1024) # Cap max read at 15MB
            return data, content_type

    try:
        data, content_type = await run_in_threadpool(fetch_proxy_data, target_url)
        return Response(
            content=data,
            media_type=content_type,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Cache-Control": "public, max-age=86400"
            }
        )
    except Exception as e:
        # Fallback: if drive.google.com/thumbnail failed, try lh3 edge link
        if drive_match and drive_match.group(1):
            try:
                alt_url = f"https://lh3.googleusercontent.com/d/{drive_match.group(1)}=s1600"
                data, content_type = await run_in_threadpool(fetch_proxy_data, alt_url)
                return Response(
                    content=data,
                    media_type=content_type,
                    headers={
                        "Access-Control-Allow-Origin": "*",
                        "Cache-Control": "public, max-age=86400"
                    }
                )
            except Exception:
                pass
        raise HTTPException(status_code=500, detail=f"Không thể tải ảnh qua proxy: {str(e)}")


@router.post("/image")
@router.post("")
async def upload_image(
    file: UploadFile = File(...),
    current_user: models.User = Depends(auth.get_current_admin)
):
    """
    Upload an image or video file directly to Cloudinary into the configured folder.
    Returns the secure URL of the uploaded asset.
    Offloaded to worker threadpool to keep the asyncio event loop completely unblocked.
    """
    content_type = (file.content_type or "").lower().strip()
    is_video = content_type in ALLOWED_VIDEO_TYPES
    is_image = content_type in ALLOWED_IMAGE_TYPES

    if not is_image and not is_video:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tệp được tải lên phải là hình ảnh (PNG, JPG, WEBP, GIF - không hỗ trợ SVG) hoặc video (MP4, WebM)."
        )

    try:
        max_allowed = MAX_VIDEO_SIZE if is_video else MAX_IMAGE_SIZE
        file_bytes = await file.read(max_allowed + 1)
        if len(file_bytes) > max_allowed:
            max_mb = max_allowed // (1024 * 1024)
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"Tệp tải lên vượt quá dung lượng tối đa cho phép ({max_mb}MB)!"
            )
        
        upload_kwargs = {
            "folder": CLOUDINARY_FOLDER,
            "resource_type": "video" if is_video else "image"
        }
        
        if is_image:
            # Auto format to webp with high visual quality (auto:best) and cap max dimension at 2560 for crisp 2K banners
            upload_kwargs.update({
                "format": "webp",
                "quality": "auto:best",
                "transformation": [{"width": 2560, "height": 2560, "crop": "limit"}]
            })

        # Offload synchronous Cloudinary API call to worker thread
        result = await run_in_threadpool(
            cloudinary.uploader.upload,
            file_bytes,
            **upload_kwargs
        )

        secure_url = result.get("secure_url") or result.get("url")
        public_id = result.get("public_id")

        return {
            "success": True,
            "url": secure_url,
            "public_id": public_id
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi khi tải tệp lên Cloudinary: {str(e)}"
        )


class DeleteImageRequest(BaseModel):
    url: Optional[str] = None
    public_id: Optional[str] = None
    urls: Optional[List[str]] = None


@router.post("/delete-image")
async def delete_image(
    req: DeleteImageRequest,
    background_tasks: BackgroundTasks,
    current_user: models.User = Depends(auth.get_current_admin)
):
    """
    Safely delete old image(s) from Cloudinary in the background.
    Responds immediately so the frontend never freezes.
    """
    targets = []
    if req.urls:
        targets.extend(req.urls)
    if req.url:
        targets.append(req.url)
    if req.public_id:
        targets.append(req.public_id)

    queued_count = 0
    for target in targets:
        pid = extract_cloudinary_public_id(target, CLOUDINARY_FOLDER)
        if pid:
            background_tasks.add_task(run_in_threadpool, _delete_cloudinary_sync, pid)
            queued_count += 1

    return {
        "success": True,
        "message": f"Đã xếp hàng xóa {queued_count} ảnh Cloudinary.",
        "queued": queued_count
    }
