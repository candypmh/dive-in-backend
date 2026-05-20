import uuid
from app.db import supabase


def get_communities(category: str = None, page: int = 0, page_size: int = 10):
    query = supabase.table("communities").select(
        "*, users(nickname, profile_image)", count="exact")

    if category and category != "none":
        query = query.eq("category", category)

    result = (
        query.order("created_at", desc=True)
        .range(page * page_size, (page + 1) * page_size - 1)
        .execute()
    )
    return result.data, result.count


def get_community(post_id: str):
    result = (
        supabase.table("communities")
        .select("*, users(nickname, profile_image)")
        .eq("id", post_id)
        .limit(1).execute()
    )
    return result.data[0] if result.data else None


def create_community(author_id: str, data: dict):
    result = (
        supabase.table("communities")
        .insert({
            "author_id": author_id,
            "category": data["category"],
            "title": data["title"],
            "content": data["content"],
            "images": data.get("images", []),
        })
        .execute()
    )
    return result.data[0]

# supabase storage에 이미지 업로드
async def upload_image(file) -> str:
    content = await file.read()
    ext = file.filename.split(".")[-1]
    path = f"{uuid.uuid4()}.{ext}"

    supabase.storage.from_("community-images").upload(
        path=path,
        file=content,
        file_options={"content-type": file.content_type}
    )
    public_url = supabase.storage.from_(
        "community-images").get_public_url(path)
    return public_url


def update_community(post_id: str, author_id: str, data: dict):
    existing = supabase.table("communities").select(
        "author_id").eq("id", post_id).limit(1).execute()
    if not existing.data:
        raise Exception("게시글을 찾을 수 없습니다")
    if existing.data[0]["author_id"] != author_id:
        raise Exception("수정 권한이 없습니다")

    update_data = {k: v for k, v in data.items() if v is not None}
    result = (
        supabase.table("communities")
        .update(update_data)
        .eq("id", post_id)
        .execute()
    )
    return result.data[0]


def delete_community(post_id: str, author_id: str):
    existing = supabase.table("communities").select(
        "author_id").eq("id", post_id).limit(1).execute()
    if not existing.data:
        raise Exception("게시글을 찾을 수 없습니다")
    if existing.data[0]["author_id"] != author_id:
        raise Exception("삭제 권한이 없습니다")

    supabase.table("communities").delete().eq("id", post_id).execute()


def add_like(post_id: str, user_id: str):
    supabase.table("likes").insert(
        {"post_id": post_id, "user_id": user_id}).execute()


def remove_like(post_id: str, user_id: str):
    supabase.table("likes").delete().eq(
        "post_id", post_id).eq("user_id", user_id).execute()


def get_like_info(post_id: str, user_id: str = None):
    count_result = (
        supabase.table("likes")
        .select("id", count="exact")
        .eq("post_id", post_id)
        .execute()
    )
    likes_cnt = count_result.count or 0

    is_liked = False
    if user_id:
        liked_result = (
            supabase.table("likes")
            .select("id")
            .eq("post_id", post_id)
            .eq("user_id", user_id)
            .execute()
        )
        is_liked = len(liked_result.data) > 0

    return {"likesCnt": likes_cnt, "isLiked": is_liked}


def search_posts(keyword: str, limit: int = 20):
    result = (
        supabase.table("communities")
        .select("*, users(nickname, profile_image)")
        .or_(f"title.ilike.%{keyword}%,content.ilike.%{keyword}%")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    return result.data


def get_top_view_posts(limit: int = 6):
    result = (
        supabase.table("communities")
        .select("*, users(nickname, profile_image)")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    return result.data


def get_new_posts(limit: int = 6):
    result = (
        supabase.table("communities")
        .select("*, users(nickname, profile_image)")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    return result.data


def get_competition_posts(limit: int = 6):
    result = (
        supabase.table("communities")
        .select("*, users(nickname, profile_image)")
        .eq("category", "COMPETITION")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    return result.data
