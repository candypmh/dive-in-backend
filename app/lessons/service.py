from supabase import create_client
from app.config import SUPABASE_URL, SUPABASE_SERVICE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)


def get_lessons():
    result = (
        supabase.table("lessons")
        .select("id, academy_name, academy_image_url, lesson_name, level, keyword, price")
        .execute()
    )
    return result.data


def get_lesson(lesson_id: int):
    result = (
        supabase.table("lessons")
        .select(
            "*, "
            "pools(id, pool_name, pool_address, region, latitude, longitude, pool_images(image_url, rep_image)), "
            "lesson_images(image_url, sort_order)"
        )
        .eq("id", lesson_id)
        .limit(1)
        .execute()
    )
    return result.data[0] if result.data else None
