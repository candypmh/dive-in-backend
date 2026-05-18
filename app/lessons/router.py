from fastapi import APIRouter, HTTPException
from app.lessons import service

router = APIRouter()


def _transform_lesson_list(lesson: dict) -> dict:
    return {
        "id": lesson["id"],
        "academyName": lesson["academy_name"],
        "academyImageUrl": lesson.get("academy_image_url"),
        "lessonName": lesson["lesson_name"],
        "level": lesson.get("level", ""),
        "keyword": lesson.get("keyword", ""),
        "price": lesson.get("price"),
    }


def _transform_lesson_detail(lesson: dict) -> dict:
    pool_raw = lesson.get("pools")
    pool = None
    if pool_raw:
        pool_images = pool_raw.get("pool_images") or []
        rep_image_url = next(
            (img["image_url"] for img in pool_images if img.get("rep_image")),
            None
        )
        pool = {
            "id": pool_raw["id"],
            "poolName": pool_raw["pool_name"],
            "poolAddress": pool_raw.get("pool_address"),
            "region": pool_raw["region"],
            "imageUrl": rep_image_url,
            "latitude": pool_raw["latitude"],
            "longitude": pool_raw["longitude"],
        }

    lesson_images_raw = lesson.get("lesson_images") or []
    sorted_images = sorted(lesson_images_raw, key=lambda x: x.get("sort_order", 0))

    return {
        "id": lesson["id"],
        "lessonName": lesson["lesson_name"],
        "level": lesson.get("level", ""),
        "capacity": lesson.get("capacity"),
        "price": lesson.get("price"),
        "keyword": lesson.get("keyword", ""),
        "lessonDetail": lesson.get("lesson_detail", {}),
        "lessonSchedule": lesson.get("lesson_schedule"),
        "lessonStatus": lesson.get("lesson_status", "OPEN"),
        "academy": {
            "id": lesson["academy_id"],
            "academyName": lesson["academy_name"],
            "academyInfo": lesson.get("academy_info"),
            "profileImageUrl": lesson.get("academy_image_url"),
        },
        "pool": pool,
        "images": [{"imageUrl": img["image_url"]} for img in sorted_images],
    }


@router.get("")
def list_lessons():
    lessons = service.get_lessons()
    return {
        "success": True,
        "message": None,
        "data": [_transform_lesson_list(l) for l in lessons],
    }


@router.get("/{lesson_id}")
def get_lesson(lesson_id: int):
    lesson = service.get_lesson(lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="수업을 찾을 수 없습니다")
    return {
        "success": True,
        "message": None,
        "data": _transform_lesson_detail(lesson),
    }
