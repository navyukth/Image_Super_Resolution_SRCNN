import time
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routes import router
from app.core.config import settings
from app.core.logger import logger


from app.db.database import engine
from app.db.base import Base
from app.models.job import Job

from app.api import auth

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title = settings.app_name,
    version = "1.0.0",
    debug = settings.debug
)

app.include_router(router)
app.include_router(auth.router)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code = 500,
        content = {
            "error" : "Something went wrong",
            "path":request.url.path
        }
    )

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