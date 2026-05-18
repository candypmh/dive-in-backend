from fastapi import APIRouter, HTTPException
from app.pools import service

router = APIRouter()


def _transform_pool_list(pool: dict) -> dict:
    images = pool.get("pool_images") or []
    rep_image_url = next(
        (img["image_url"] for img in images if img.get("rep_image")),
        None
    )
    return {
        "id": pool["id"],
        "poolName": pool["pool_name"],
        "poolAddress": pool.get("pool_address"),
        "region": pool["region"],
        "imageUrl": rep_image_url,
        "latitude": pool["latitude"],
        "longitude": pool["longitude"],
    }


def _transform_pool_detail(pool: dict, lessons: list) -> dict:
    images = pool.get("pool_images") or []
    sorted_images = sorted(images, key=lambda x: x.get("sort_order", 0))
    return {
        "id": pool["id"],
        "poolName": pool["pool_name"],
        "poolAddress": pool.get("pool_address"),
        "region": pool["region"],
        "operatingHours": pool.get("operating_hours", ""),
        "closingDays": pool.get("closing_days", ""),
        "contact": pool.get("contact", ""),
        "laneLength": pool.get("lane_length"),
        "laneCount": pool.get("lane_count"),
        "maxDepth": pool.get("max_depth"),
        "minDepth": pool.get("min_depth"),
        "facilities": pool.get("facilities", ""),
        "latitude": pool["latitude"],
        "longitude": pool["longitude"],
        "poolImages": [
            {"repImage": img.get("rep_image", False), "imageUrl": img["image_url"]}
            for img in sorted_images
        ],
        "lessons": [_transform_lesson_brief(l) for l in lessons],
    }


def _transform_lesson_brief(lesson: dict) -> dict:
    return {
        "id": lesson["id"],
        "academyName": lesson["academy_name"],
        "academyImageUrl": lesson.get("academy_image_url"),
        "keyword": lesson.get("keyword", ""),
        "lessonName": lesson["lesson_name"],
        "level": lesson.get("level", ""),
        "price": lesson.get("price"),
    }


@router.get("")
def list_pools():
    pools = service.get_pools()
    return {
        "success": True,
        "message": None,
        "data": [_transform_pool_list(p) for p in pools],
    }


@router.get("/{pool_id}")
def get_pool(pool_id: int):
    pool, lessons = service.get_pool(pool_id)
    if not pool:
        raise HTTPException(status_code=404, detail="수영장을 찾을 수 없습니다")
    return {
        "success": True,
        "message": None,
        "data": _transform_pool_detail(pool, lessons),
    }
