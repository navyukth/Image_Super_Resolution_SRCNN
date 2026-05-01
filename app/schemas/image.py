from pydantic import BaseModel

class UploadResponse(BaseModel):
    message: str
    filename: str

class EnhanceResponse(BaseModel):
    job_id : int
    message: str
    output_file: str
