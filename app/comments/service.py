from app.db import supabase


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
    comment_id = result.data[0]["id"]
    full_result = (
        supabase.table("comments")
        .select("*, users(nickname, profile_image)")
        .eq("id", comment_id)
        .limit(1).execute()
    )
    return full_result.data[0] if full_result.data else None


def update_comment(comment_id: str, author_id: str, content: str):
    existing = supabase.table("comments").select("author_id").eq("id", comment_id).limit(1).execute()
    if not existing.data:
        raise Exception("댓글을 찾을 수 없습니다")
    if existing.data[0]["author_id"] != author_id:
        raise Exception("수정 권한이 없습니다")

    supabase.table("comments").update({"content": content}).eq("id", comment_id).execute()

    result = (
        supabase.table("comments")
        .select("*, users(nickname, profile_image)")
        .eq("id", comment_id)
        .limit(1).execute()
    )
    return result.data[0] if result.data else None


def delete_comment(comment_id: str, author_id: str):
    existing = supabase.table("comments").select("author_id").eq("id", comment_id).limit(1).execute()
    if not existing.data:
        raise Exception("댓글을 찾을 수 없습니다")
    if existing.data[0]["author_id"] != author_id:
        raise Exception("삭제 권한이 없습니다")

    supabase.table("comments").delete().eq("id", comment_id).execute()
