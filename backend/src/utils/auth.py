from fastapi.security import APIKeyHeader
from fastapi import Security, HTTPException
from sqlalchemy.orm import Session
from jose import jwt
from ..core.database import get_db
from ..core.models import User

api_key_header = APIKeyHeader(name="X-API-Key")

def get_current_user(
    api_key: str = Security(api_key_header),
    db: Session = Depends(get_db)
):
    if not api_key:
        raise HTTPException(status_code=401, detail="API key missing")
    
    user = db.query(User).filter(User.api_key == api_key).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return user