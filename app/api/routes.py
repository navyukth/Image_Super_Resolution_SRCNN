from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session

import os
import shutil
import uuid

from app.services.inference import enhance_image
from app.schemas.image import UploadResponse,EnhanceResponse,UpdateResponse,UpdateRequest
from app.core.config import settings

from app.db.deps import get_db
from app.models.job import Job

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
async def enhance(file: UploadFile = File(...), db: Session = Depends(get_db)):
    
    job = Job(
        input_file = file.filename,
        status = "processing"
    )
    
    db.add(job)
    db.commit()
    db.refresh(job)
    try:
        result = enhance_image(file)

        # return{
        #     "message" : "Image enhaned succ",
        #     "output_file": result
        # }

        job.output_file = result
        job.status = "completed"

        db.commit()

        return EnhanceResponse(
            job_id = job.id,
            message ="Image enhanced successful",
            output_file = result
        )
    except Exception:
        job.status = "failed"
        db.commit()
        
        raise HTTPException(
            status_code = 500,
            detail = "Image ench failed"
        ) 

@router.get("/jobs")
def get_jobs(db: Session = Depends(get_db)):
    jobs = db.query(Job).all()
    return jobs

@router.get("/jobs/{job_id}")
def get_job(job_id: int, db: Session = Depends(get_db)):


    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(
            status_code = 404,
            detail = "Job not found"
        )

    return job

@router.delete("/jobs/{job_id}")
def delete_job(job_id:int, db: Session = Depends(get_db)):

    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(
            status_code = 404,
            detail = "Job not found"
        )
    
    db.delete(job)
    db.commit()

    return {
        "message":"deleted successful"
    }

@router.patch("/jobs/{job_id}")

def update_job(job_id:int,payload = UpdateRequest, db:Session = Depends(get_db)):

    job = db.query(Job).filter(Job.id==job_id).first()

    if not job:
        raise HTTPException(
            status_code = 404,
            detail = "Job not found"
        )
    
    job.status = payload.status
    db.commit()
    db.refresh(job)

    return UpdateResponse(
        id = job_id,
        status  = job.status
    )