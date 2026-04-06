from fastapi import APIRouter, Depends, HTTPException
from app.auth.middleware import get_auth_user
from app.community.schema import CommunityCreate, CommunityUpdate
from app.community import service

router = APIRouter()


@router.get("/posts")
def list_communities(category: str = None, page: int = 0):
    posts = service.get_communities(category=category, page=page)
    return {"posts": posts, "hasMore": len(posts) == 10}


@router.get("/posts/{post_id}")
def get_community(post_id: str):
    post = service.get_community(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다")
    return {"post": post}


@router.post("/posts")
def create_community(body: CommunityCreate, current_user: dict = Depends(get_auth_user)):
    post = service.create_community(author_id=current_user["sub"], data=body.model_dump())
    return {"post": post}


@router.put("/posts/{post_id}")
def update_community(post_id: str, body: CommunityUpdate, current_user: dict = Depends(get_auth_user)):
    try:
        post = service.update_community(
            post_id=post_id,
            author_id=current_user["sub"],
            data=body.model_dump(),
        )
        return {"post": post}
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.delete("/posts/{post_id}")
def delete_community(post_id: str, current_user: dict = Depends(get_auth_user)):
    try:
        service.delete_community(post_id=post_id, author_id=current_user["sub"])
        return {"message": "삭제 완료"}
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))
