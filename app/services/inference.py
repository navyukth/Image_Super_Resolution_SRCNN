import os
import shutil
import uuid
from app.core.config import settings

OUTPUT_DIR = settings.output_dir
os.makedirs(OUTPUT_DIR,exist_ok = True)

def enhance_image(upload_file):
    output_name = f"enchance_{uuid.uuid4()}_{upload_file.filename}"
    output_path = os.path.join(OUTPUT_DIR,output_name)


    with open(output_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    return output_name