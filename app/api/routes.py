from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil
import uuid
from app.services.inference import enhance_image
from app.schemas.image import UploadResponse,EnhanceResponse
from app.core.config import settings

router = APIRouter()

UPLOAD_DIR = settings.upload_dir
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/health")
def health():
    return {"status":"ok"}

ALLOWED_TYPE = ["image/jpeg","image/png"]

@router.post("/upload", response_model = UploadResponse)
async def upload_image(file: UploadFile = File(...)):

    if file.content_type not in ALLOWED_TYPE:
        raise HTTPException(
            status_code = 400,
            detail="Only image pls"
        )
    unique_name = f"upload_{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # return {"message": "Uploaded", "filename": unique_name}
    return UploadResponse(
        message = "Uploaded successful",
        filename = file.filename
    )

@router.post("/enhance", response_model = EnhanceResponse)
async def enhance(file: UploadFile = File(...)):
    try:
        result = enhance_image(file)

        # return{
        #     "message" : "Image enhaned succ",
        #     "output_file": result
        # }
        return EnhanceResponse(
            message ="Image enhanced successful",
            output_file = result
        )
    except Exception:
        raise HTTPException(
            status_code = 500,
            detail = "Image ench failed"
        ) 