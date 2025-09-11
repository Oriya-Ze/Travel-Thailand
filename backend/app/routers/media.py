from fastapi import APIRouter, Depends
from app.utils.aws import presign_put, presign_get
from app.core.config import settings
from app.deps.auth import get_current_claims


router = APIRouter(prefix="/media", tags=["media"])


@router.post("/presign-put")
async def presign_upload(filename: str, content_type: str, claims=Depends(get_current_claims)):
    key = f"{settings.S3_UPLOAD_PREFIX}{filename}"
    return presign_put(key, content_type)


@router.get("/presign-get")
async def presign_download(key: str, claims=Depends(get_current_claims)):
    return presign_get(key)
