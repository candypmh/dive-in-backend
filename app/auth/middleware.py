from fastapi import Cookie, HTTPException
from jose import JWTError
from app.auth.service import get_current_user


def get_auth_user(access_token: str = Cookie(default=None)) -> dict:
    if not access_token:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다")
    try:
        return get_current_user(access_token)
    except JWTError:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다")
