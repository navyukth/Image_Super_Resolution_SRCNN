import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    app_name = os.getenv("APP_NAME", "FastAPI App")
    debug = os.getenv("DEBUG","False") == "True"
    upload_dir = os.getenv("UPLOAD_DIR","uploads")
    output_dir = os.getenv("OUTPUT_DIR","outputs")
    model_path = os.getenv("MODEL_PATH","model_weights.pth")

settings = Settings()