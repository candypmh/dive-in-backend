from fastapi import APIRouter
from app.home import service
from app.community.router import _transform_post

router = APIRouter()


def _transform_lesson_card(lesson: dict) -> dict:
    return {
        "id": lesson["id"],
        "lessonName": lesson["lesson_name"],
        "level": lesson.get("level", ""),
        "keyword": lesson.get("keyword", ""),
        "price": lesson.get("price"),
        "instructorName": lesson.get("instructor_name", ""),
        "instructorImgUrl": lesson.get("instructor_img_url"),
        "lessonImgUrl": lesson["lesson_img_url"],
        "viewCnt": lesson.get("view_cnt", 0),
    }


def _transform_competition_post(post: dict) -> dict:
    base = _transform_post(post)
    base["period"] = None
    base["dDay"] = None
    return base


@router.get("/initial")
def get_home_initial():
    data = service.get_home_initial()
    return {
        "success": True,
        "message": None,
        "data": {
            "topViewLessonList": [_transform_lesson_card(l) for l in data["topViewLessonList"]],
            "newLessonList": [_transform_lesson_card(l) for l in data["newLessonList"]],
            "topViewPostList": [_transform_post(p) for p in data["topViewPostList"]],
            "newPostList": [_transform_post(p) for p in data["newPostList"]],
            "competitionPostList": [_transform_competition_post(p) for p in data["competitionPostList"]],
        },
    }
