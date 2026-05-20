from app.db import supabase


def get_pools():
    result = (
        supabase.table("pools")
        .select("*, pool_images(image_url, rep_image)")
        .execute()
    )
    return result.data


def get_pool(pool_id: int):
    pool_result = (
        supabase.table("pools")
        .select("*, pool_images(image_url, rep_image, sort_order)")
        .eq("id", pool_id)
        .limit(1)
        .execute()
    )
    pool = pool_result.data[0] if pool_result.data else None
    if not pool:
        return None, []

    lessons_result = (
        supabase.table("lessons")
        .select("id, academy_name, academy_image_url, keyword, lesson_name, level, price")
        .eq("pool_id", pool_id)
        .execute()
    )
    return pool, lessons_result.data
