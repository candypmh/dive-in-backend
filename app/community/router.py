from fastapi import APIRouter, Depends, HTTPException
from app.auth.middleware import get_auth_user
from app.community.schema import CommunityCreate, CommunityUpdate
from app.community import service
from app.comments import service as comments_service


router = APIRouter()


def _transform_post(post: dict) -> dict:
    users = post.get("users") or {}
    images = post.get("images") or []
    profile_image = users.get("profile_image") or None
    first_image = {"repImage": True, "imageUrl": images[0]} if images else None

    return {
        "postId": post["id"],
        "categoryName": post.get("category", "COMMUNICATION"),
        "title": post.get("title", ""),
        "content": post.get("content", ""),
        "image": first_image,
        "likesCnt": 0,
        "cmntCnt": 0,
        "viewCnt": 0,
        "writer": users.get("nickname", ""),
        "writerProfile": profile_image,
        "createdAt": post.get("created_at", ""),
        "updatedAt": post.get("updated_at"),
        "isPopular": False,
    }


def _transform_post_detail(post: dict, comments: list, like_info: dict = None) -> dict:
    users = post.get("users") or {}
    images = post.get("images") or []
    profile_image = users.get("profile_image") or None
    like_info = like_info or {"likesCnt": 0, "isLiked": False}

    transformed_images = [{"repImage": i == 0, "imageUrl": url} for i, url in enumerate(images)]
    transformed_comments = [_transform_comment(c) for c in comments]

    return {
        "postId": post["id"],
        "categoryName": post.get("category", "COMMUNICATION"),
        "title": post.get("title", ""),
        "content": post.get("content", ""),
        "images": transformed_images,
        "likesCnt": like_info["likesCnt"],
        "cmntCnt": len(transformed_comments),
        "viewCnt": 0,
        "writer": users.get("nickname", ""),
        "writerId": post.get("author_id", ""),
        "writerProfile": profile_image,
        "createdAt": post.get("created_at", ""),
        "updatedAt": post.get("updated_at"),
        "isPopular": False,
        "isLiked": like_info["isLiked"],
        "commentList": transformed_comments,
    }


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


@router.get("/posts")
def list_communities(category: str = None, page: int = 0):
    posts, total = service.get_communities(category=category, page=page)
    page_size = 10
    transformed = [_transform_post(p) for p in posts]
    return {
        "success": True,
        "message": None,
        "data": {
            "posts": transformed,
            "totalPosts": total or 0,
            "hasMore": len(posts) == page_size,
        },
    }


@router.get("/posts/{post_id}")
def get_community(post_id: str):
    post = service.get_community(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다")
    comments = comments_service.get_comments(post_id)
    like_info = service.get_like_info(post_id)
    return {"data": _transform_post_detail(post, comments, like_info)}


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


@router.post("/posts/{post_id}/like")
def like_post(post_id: str, current_user: dict = Depends(get_auth_user)):
    try:
        service.add_like(post_id=post_id, user_id=current_user["sub"])
    except Exception:
        pass  # 이미 좋아요한 경우 무시
    like_info = service.get_like_info(post_id=post_id, user_id=current_user["sub"])
    return {"isLiked": like_info["isLiked"], "likesCnt": like_info["likesCnt"]}


@router.delete("/posts/{post_id}/like")
def unlike_post(post_id: str, current_user: dict = Depends(get_auth_user)):
    service.remove_like(post_id=post_id, user_id=current_user["sub"])
    like_info = service.get_like_info(post_id=post_id, user_id=current_user["sub"])
    return {"isLiked": like_info["isLiked"], "likesCnt": like_info["likesCnt"]}
