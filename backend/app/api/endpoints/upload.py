from fastapi import APIRouter, UploadFile, File, HTTPException, status, Query
from fastapi.responses import Response
import urllib.request
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
from fastapi import Depends

@router.get("/proxy-image")
async def proxy_image(url: str = Query(..., description="URL của ảnh cần tải qua proxy")):
    """
    Proxy an external image (e.g. from Google Drive) to bypass browser CORS restrictions during cropping.
    Returns the raw image stream with Access-Control-Allow-Origin headers.
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

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        req = urllib.request.Request(target_url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            content_type = resp.headers.get_content_type() or "image/jpeg"
            data = resp.read()
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
                req = urllib.request.Request(alt_url, headers=headers)
                with urllib.request.urlopen(req, timeout=15) as resp:
                    content_type = resp.headers.get_content_type() or "image/jpeg"
                    return Response(
                        content=resp.read(),
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
async def upload_image(
    file: UploadFile = File(...),
    current_user: models.User = Depends(auth.get_current_user)
):
    """
    Upload an image file directly to Cloudinary into the 'Acc Demo' folder.
    Returns the secure URL of the uploaded image.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tệp được tải lên phải là hình ảnh (PNG, JPG, WEBP, GIF, etc.)"
        )
    
    try:
        file_bytes = await file.read()
        # Upload file directly to Cloudinary folder "Acc Demo"
        # Auto-convert to WebP and optimize quality (q_auto:good) to keep file sizes lightweight
        result = cloudinary.uploader.upload(
            file_bytes,
            folder=CLOUDINARY_FOLDER,
            resource_type="image",
            format="webp",
            quality="auto:good"
        )
        
        secure_url = result.get("secure_url") or result.get("url")
        public_id = result.get("public_id")
        
        return {
            "success": True,
            "url": secure_url,
            "public_id": public_id
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi khi tải ảnh lên Cloudinary: {str(e)}"
        )
