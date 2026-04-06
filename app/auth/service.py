import httpx
from datetime import datetime, timedelta
from jose import jwt
from supabase import create_client

from app.config import (
    SUPABASE_URL,
    SUPABASE_SERVICE_KEY,
    KAKAO_APP_KEY,
    KAKAO_CLIENT_SECRET,
    KAKAO_REDIRECT_URI,
    JWT_SECRET_KEY,
    JWT_ALGORITHM,
)

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

KAKAO_TOKEN_URL = "https://kauth.kakao.com/oauth/token"
KAKAO_USER_URL = "https://kapi.kakao.com/v2/user/me"


async def kakao_login(code: str):
    # 1. code → 카카오 access_token 교환
    async with httpx.AsyncClient() as client:
        token_res = await client.post(
            KAKAO_TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "client_id": KAKAO_APP_KEY,
                "redirect_uri": KAKAO_REDIRECT_URI,
                "code": code,
                "client_secret": KAKAO_CLIENT_SECRET,
            },
        )
        token_data = token_res.json()

    kakao_access_token = token_data.get("access_token")
    if not kakao_access_token:
        raise Exception("카카오 토큰 발급 실패")

    # 2. access_token → 카카오 유저 정보 조회
    async with httpx.AsyncClient() as client:
        user_res = await client.get(
            KAKAO_USER_URL,
            headers={"Authorization": f"Bearer {kakao_access_token}"},
        )
        user_data = user_res.json()

    kakao_id = user_data["id"]
    profile = user_data.get("kakao_account", {}).get("profile", {})
    nickname = profile.get("nickname", "")
    profile_image = profile.get("profile_image_url", "")

    # 3. Supabase users upsert
    result = (
        supabase.table("users")
        .upsert(
            {
                "kakao_id": kakao_id,
                "nickname": nickname,
                "profile_image": profile_image,
            },
            on_conflict="kakao_id",
        )
        .execute()
    )
    user = result.data[0]

    # 4. JWT 발급
    access_token = _create_access_token(
        {"sub": str(user["id"]), "nickname": user["nickname"]}
    )

    return access_token, user


def _create_access_token(data: dict, expires_hours: int = 8) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=expires_hours)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def get_current_user(token: str) -> dict:
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    return payload
