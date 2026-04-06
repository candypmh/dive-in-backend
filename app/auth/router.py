from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.auth.service import kakao_login
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

    response = JSONResponse(
        content={"message": "로그인 성공", "user": {"id": user["id"], "nickname": user["nickname"]}}
    )
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",
        max_age=60 * 60 * 8,  # 8시간
    )
    return response


@router.post("/logout")
def logout():
    response = JSONResponse(content={"message": "로그아웃 성공"})
    response.delete_cookie("access_token")
    return response


@router.get("/user")
def get_user(current_user: dict = Depends(get_auth_user)):
    return {"user": current_user}
