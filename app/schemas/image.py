from pydantic import BaseModel

class UploadResponse(BaseModel):
    message: str
    filename: str

class EnhanceResponse(BaseModel):
    message: str
    output_file: str
