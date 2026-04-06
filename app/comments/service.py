from supabase import create_client
from app.config import SUPABASE_URL, SUPABASE_SERVICE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)


def get_comments(post_id: str):
    result = (
        supabase.table("comments")
        .select("*, users(nickname, profile_image)")
        .eq("post_id", post_id)
        .order("created_at", desc=False)
        .execute()
    )
    return result.data


def create_comment(post_id: str, author_id: str, content: str):
    result = (
        supabase.table("comments")
        .insert({"post_id": post_id, "author_id": author_id, "content": content})
        .execute()
    )
    return result.data[0]


def update_comment(comment_id: str, author_id: str, content: str):
    existing = supabase.table("comments").select("author_id").eq("id", comment_id).single().execute()
    if existing.data["author_id"] != author_id:
        raise Exception("수정 권한이 없습니다")

    result = (
        supabase.table("comments")
        .update({"content": content})
        .eq("id", comment_id)
        .execute()
    )
    return result.data[0]


def delete_comment(comment_id: str, author_id: str):
    existing = supabase.table("comments").select("author_id").eq("id", comment_id).single().execute()
    if existing.data["author_id"] != author_id:
        raise Exception("삭제 권한이 없습니다")

    supabase.table("comments").delete().eq("id", comment_id).execute()
