from fastapi import APIRouter, UploadFile, File, HTTPException, status
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

@router.post("/image")
async def upload_image(file: UploadFile = File(...)):
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
        result = cloudinary.uploader.upload(
            file_bytes,
            folder=CLOUDINARY_FOLDER,
            resource_type="image"
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
