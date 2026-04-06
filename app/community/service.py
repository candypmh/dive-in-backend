from supabase import create_client
from app.config import SUPABASE_URL, SUPABASE_SERVICE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)


def get_communities(category: str = None, page: int = 0, page_size: int = 10):
    query = supabase.table("communities").select("*, users(nickname, profile_image)")

    if category and category != "none":
        query = query.eq("category", category)

    result = (
        query.order("created_at", desc=True)
        .range(page * page_size, (page + 1) * page_size - 1)
        .execute()
    )
    return result.data


def get_community(post_id: str):
    result = (
        supabase.table("communities")
        .select("*, users(nickname, profile_image)")
        .eq("id", post_id)
        .single()
        .execute()
    )
    return result.data


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


def update_community(post_id: str, author_id: str, data: dict):
    # 작성자 검증
    existing = supabase.table("communities").select("author_id").eq("id", post_id).single().execute()
    if existing.data["author_id"] != author_id:
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
    # 작성자 검증
    existing = supabase.table("communities").select("author_id").eq("id", post_id).single().execute()
    if existing.data["author_id"] != author_id:
        raise Exception("삭제 권한이 없습니다")

    supabase.table("communities").delete().eq("id", post_id).execute()
