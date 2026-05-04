from app.models.user import User

from app.core.security import hash_password
from app.core.security import verify_password

def create_user(db,user_data):
    user = User(
        username = user_data.username,
        email = user_data.email,
        hashed_pass = hash_password(user_data.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db,email,password):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    
    if not verify_password(password,user.hashed_pass):
        return None

    return user