from fastapi import APIRouter, HTTPException, Depends, Form, UploadFile, File
from typing import Optional
from pydantic import BaseModel
from app.auth.service import kakao_login, get_user_by_id, update_user
from app.auth.middleware import get_auth_user

router = APIRouter()


class KakaoLoginRequest(BaseModel):
    code: str
    redirect_uri: str


@router.post("/kakao")
async def kakao_auth(body: KakaoLoginRequest):
    try:
        access_token, user = await kakao_login(body.code, body.redirect_uri)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"accessToken": access_token, "user": {"id": user["id"], "nickname": user["nickname"]}}


@router.post("/logout")
def logout():
    return {"message": "로그아웃 성공"}


@router.get("/user")
def get_user(current_user: dict = Depends(get_auth_user)):
    user_id = current_user["sub"]
    user = get_user_by_id(user_id)
    return {"user": user}


@router.put("/user")
async def update_user_profile(
    nickname: str = Form(...),
    profile_image: Optional[UploadFile] = File(None),
    current_user: dict = Depends(get_auth_user),
):
    user_id = current_user["sub"]
    try:
        updated = update_user(user_id, nickname, profile_image)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"user": updated}
