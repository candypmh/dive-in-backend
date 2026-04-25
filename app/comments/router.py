from fastapi import APIRouter, Depends, HTTPException
from app.auth.middleware import get_auth_user
from app.comments.schema import CommentCreate, CommentUpdate
from app.comments import service

router = APIRouter()


def _transform_comment(comment: dict) -> dict:
    users = comment.get("users") or {}
    profile_image = users.get("profile_image") or None
    return {
        "cmntId": comment["id"],
        "content": comment.get("content", ""),
        "groupName": 0,
        "orderNumber": 0,
        "cmntClass": 0,
        "writer": users.get("nickname", ""),
        "writerId": comment.get("author_id", ""),
        "writerProfile": profile_image,
        "likeCnt": 0,
        "createdAt": comment.get("created_at", ""),
    }


@router.get("/posts/{post_id}/comments")
def list_comments(post_id: str):
    comments = service.get_comments(post_id)
    return {"comments": [_transform_comment(c) for c in comments]}


@router.post("/posts/{post_id}/comments")
def create_comment(post_id: str, body: CommentCreate, current_user: dict = Depends(get_auth_user)):
    comment = service.create_comment(
        post_id=post_id,
        author_id=current_user["sub"],
        content=body.content,
    )
    return {"comment": _transform_comment(comment)}


@router.put("/posts/{post_id}/comments/{comment_id}")
def update_comment(post_id: str, comment_id: str, body: CommentUpdate, current_user: dict = Depends(get_auth_user)):
    try:
        comment = service.update_comment(
            comment_id=comment_id,
            author_id=current_user["sub"],
            content=body.content,
        )
        return {"comment": _transform_comment(comment)}
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.delete("/posts/{post_id}/comments/{comment_id}")
def delete_comment(post_id: str, comment_id: str, current_user: dict = Depends(get_auth_user)):
    try:
        service.delete_comment(comment_id=comment_id, author_id=current_user["sub"])
        return {"message": "삭제 완료"}
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))
