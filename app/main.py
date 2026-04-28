import time
from fastapi import FastAPI, Request
from app.api.routes import router
from app.core.config import settings
from app.core.logger import logger


app = FastAPI(
    title = settings.app_name,
    version = "1.0.0",
    debug = settings.debug
)

app.include_router(router)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    logger.info(f"Request started:{request.method} {request.url.path}")
    
    response  = await call_next(request)
    
    process_time = round((time.time() - start_time)*1000,2)
    
    logger.info(
        f"Request completed: {request.method} {request.url.path}"
        f"Status = {response .status_code} Time = {process_time}ms"
    )    
    
    return response 

@app.get("/home")
def home():
    return {"message":"Backend Running"}