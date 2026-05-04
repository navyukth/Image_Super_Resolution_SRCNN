from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session


from app.schemas.user import UserCreate,UserResponse
from app.services.user_service import create_user
from app.models.user import User
from app.db.deps import get_db

from app.schemas.user import UserLogin, Token
from app.core.security import create_access_token
from app.services.user_service import authenticate_user

from app.core.security import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db:Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    return create_user(db, user)

@router.post("/login", response_model = Token)
def login(user: UserLogin, db:Session = Depends(get_db)):

    db_user = authenticate_user(db,user.email,user.password)

    if not db_user :
         raise HTTPException(status_code=401, detail="Invaild credentials")

    token = create_access_token({"user_id":db_user.id})

    return{
        "access_token" : token,
        "token_type": "bearer"
    }

@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return{
        "message" : "Authenticated user",
        "user_id": current_user
    }