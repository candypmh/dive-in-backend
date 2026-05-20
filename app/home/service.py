from app.db import supabase
from app.community import service as community_service

_LESSON_CARD_COLS = (
    "id, lesson_name, level, keyword, price, "
    "instructor_name, instructor_img_url, lesson_img_url, view_cnt"
)


def get_home_initial():
    top_view_lessons = (
        supabase.table("lessons")
        .select(_LESSON_CARD_COLS)
        .order("view_cnt", desc=True)
        .limit(6)
        .execute()
    ).data

    new_lessons = (
        supabase.table("lessons")
        .select(_LESSON_CARD_COLS)
        .order("created_at", desc=True)
        .limit(6)
        .execute()
    ).data

    return {
        "topViewLessonList": top_view_lessons,
        "newLessonList": new_lessons,
        "topViewPostList": community_service.get_top_view_posts(6),
        "newPostList": community_service.get_new_posts(6),
        "competitionPostList": community_service.get_competition_posts(6),
    }
