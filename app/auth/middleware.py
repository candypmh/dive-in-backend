from fastapi import Cookie, Header, HTTPException
from jose import JWTError
from app.auth.service import get_current_user


def get_auth_user(
    accessToken: str = Cookie(default=None),
    authorization: str = Header(default=None),
) -> dict:
    token = accessToken
    if not token and authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
    if not token:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다")
    try:
        return get_current_user(token)
    except JWTError:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다")
