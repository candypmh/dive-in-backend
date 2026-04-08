from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.auth.service import kakao_login, supabase
from app.auth.middleware import get_auth_user

router = APIRouter()


class KakaoLoginRequest(BaseModel):
    code: str


@router.post("/kakao")
async def kakao_auth(body: KakaoLoginRequest):
    try:
        access_token, user = await kakao_login(body.code)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"accessToken": access_token, "user": {"id": user["id"], "nickname": user["nickname"]}}


@router.post("/logout")
def logout():
    return {"message": "로그아웃 성공"}


@router.get("/user")
def get_user(current_user: dict = Depends(get_auth_user)):
    user_id = current_user["sub"]
    result = supabase.table("users").select("id, nickname, profile_image").eq("id", user_id).single().execute()
    return {"user": result.data}
