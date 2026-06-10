from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv
from pyproj import Transformer


BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

SEOUL_API_SERVICE = "LOCALDATA_103501"
SEOUL_API_BASE_URL = "http://openapi.seoul.go.kr:8088"
SOURCE = "seoul-pool-license"
PAGE_SIZE = 1000
REQUEST_TIMEOUT_SECONDS = 10

_transformer = Transformer.from_crs("EPSG:5174", "EPSG:4326", always_xy=True)

MANUAL_MATCH_DECISIONS = {
    "3230000:CDFH3301011190000001": {"action": "update", "matched_pool_id": 1},
    "3230000:CDFH3301011994000001": {"action": "insert"},
    "3140000:CDFH3301012025000001": {"action": "insert"},
    "3230000:CDFH3301012022000003": {"action": "insert"},
    "3150000:CDFH3301012001000001": {"action": "insert"},
    "3100000:CDFH3301012002000001": {"action": "insert"},
    "3140000:CDFH3301011989000002": {"action": "insert"},
}


def clean_value(value: Any) -> str | None:
    if value is None:
        return None

    text = str(value).strip()
    return text or None


def build_external_id(row: dict[str, Any]) -> str | None:
    team_code = clean_value(row.get("OPNSFTEAMCODE"))
    management_number = clean_value(row.get("MGTNO"))
    if not team_code or not management_number:
        return None
    return f"{team_code}:{management_number}"


def get_seoul_open_api_key() -> str:
    load_dotenv(BACKEND_ROOT / ".env")
    api_key = os.getenv("SEOUL_OPEN_API_KEY")
    if not api_key:
        raise RuntimeError("SEOUL_OPEN_API_KEY 환경변수가 필요합니다.")
    return api_key


def fetch_license_rows(api_key: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    start = 1

    while True:
        end = start + PAGE_SIZE - 1
        url = f"{SEOUL_API_BASE_URL}/{api_key}/json/{SEOUL_API_SERVICE}/{start}/{end}/"
        response = requests.get(url, timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
        payload = response.json()

        data = payload.get(SEOUL_API_SERVICE)
        if not data:
            raise RuntimeError(f"서울 OpenAPI 응답에 {SEOUL_API_SERVICE} 데이터가 없습니다.")

        batch = data.get("row") or []
        rows.extend(batch)

        total_count = int(data.get("list_total_count") or len(rows))
        if len(rows) >= total_count or not batch:
            return rows

        start = end + 1


def is_active_pool(row: dict[str, Any]) -> bool:
    return (
        clean_value(row.get("TRDSTATENM")) == "영업/정상"
        and clean_value(row.get("DTLSTATENM")) == "영업중"
    )


def convert_tm_to_wgs84(x_value: Any, y_value: Any) -> tuple[float, float]:
    x = float(str(x_value).strip())
    y = float(str(y_value).strip())
    longitude, latitude = _transformer.transform(x, y)
    return latitude, longitude


def extract_region(address: str | None) -> str | None:
    if not address:
        return None

    match = re.search(r"서울특별시\s+([가-힣]+구)", address)
    if not match:
        match = re.search(r"서울\s+([가-힣]+구)", address)
    if not match:
        return "서울"

    district = match.group(1).removesuffix("구")
    return f"서울/{district}"


def normalize_pool_candidate(row: dict[str, Any]) -> dict[str, Any]:
    road_address = clean_value(row.get("RDNWHLADDR"))
    lot_address = clean_value(row.get("SITEWHLADDR"))
    pool_address = road_address or lot_address
    latitude, longitude = convert_tm_to_wgs84(row.get("X"), row.get("Y"))

    return {
        "source": SOURCE,
        "external_id": build_external_id(row),
        "pool_name": clean_value(row.get("BPLCNM")),
        "pool_address": pool_address,
        "region": extract_region(pool_address),
        "contact": clean_value(row.get("SITETEL")),
        "latitude": latitude,
        "longitude": longitude,
        "license_status": clean_value(row.get("DTLSTATENM")),
        "license_date": clean_value(row.get("APVPERMYMD")),
        "closed_date": clean_value(row.get("DCBYMD")),
        "road_address": road_address,
        "lot_address": lot_address,
    }


def normalize_for_match(value: str | None) -> str:
    if not value:
        return ""
    return re.sub(r"[\s()·._-]|수영장|실내|센터|구민|종합운동장", "", value)


def normalize_address_for_match(value: str | None) -> str:
    if not value:
        return ""

    without_parentheses = re.sub(r"\([^)]*\)", "", value)
    without_seoul_prefix = re.sub(r"서울특별시|서울", "", without_parentheses)
    return re.sub(r"[\s,._-]", "", without_seoul_prefix)


def has_coordinate(row: dict[str, Any]) -> bool:
    return bool(clean_value(row.get("X")) and clean_value(row.get("Y")))


def fetch_existing_pools() -> list[dict[str, Any]]:
    from app.db import supabase

    result = supabase.table("pools").select("*").execute()
    return result.data or []


def classify_candidates(
    candidates: list[dict[str, Any]],
    existing_pools: list[dict[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    insert_candidates: list[dict[str, Any]] = []
    update_candidates: list[dict[str, Any]] = []
    review_candidates: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []

    existing_pools_by_external_id = {
        clean_value(pool.get("external_id")): pool
        for pool in existing_pools
        if clean_value(pool.get("source")) == SOURCE and clean_value(pool.get("external_id"))
    }
    existing_pools_by_id = {pool.get("id"): pool for pool in existing_pools}
    existing_match_values = [
        (
            normalize_for_match(pool.get("pool_name")),
            normalize_address_for_match(pool.get("pool_address")),
            pool,
        )
        for pool in existing_pools
    ]

    for candidate in candidates:
        if not candidate.get("pool_name") or not candidate.get("pool_address"):
            skipped.append({**candidate, "skip_reason": "missing name or address"})
            continue

        external_id = clean_value(candidate.get("external_id"))
        external_id_match = existing_pools_by_external_id.get(external_id)
        if external_id_match:
            update_candidates.append(
                {
                    **candidate,
                    "match_reason": "same external_id",
                    "matched_pool_id": external_id_match.get("id"),
                    "matched_pool_name": external_id_match.get("pool_name"),
                }
            )
            continue

        manual_decision = MANUAL_MATCH_DECISIONS.get(external_id)
        if manual_decision:
            if manual_decision["action"] == "insert":
                insert_candidates.append(
                    {
                        **candidate,
                        "match_reason": "manual decision: separate facility",
                    }
                )
                continue

            matched_pool = existing_pools_by_id.get(manual_decision["matched_pool_id"])
            if matched_pool:
                update_candidates.append(
                    {
                        **candidate,
                        "match_reason": "manual decision: same facility",
                        "matched_pool_id": matched_pool.get("id"),
                        "matched_pool_name": matched_pool.get("pool_name"),
                    }
                )
            else:
                review_candidates.append(
                    {
                        **candidate,
                        "match_reason": "manual decision target not found",
                        "matched_pool_id": manual_decision["matched_pool_id"],
                    }
                )
            continue

        candidate_name = normalize_for_match(candidate.get("pool_name"))
        candidate_address = normalize_address_for_match(candidate.get("pool_address"))
        exact_address_match = next(
            (
                pool
                for _, address, pool in existing_match_values
                if candidate_address and address and candidate_address == address
            ),
            None,
        )

        if exact_address_match:
            update_candidates.append(
                {
                    **candidate,
                    "match_reason": "same normalized address",
                    "matched_pool_id": exact_address_match.get("id"),
                    "matched_pool_name": exact_address_match.get("pool_name"),
                }
            )
            continue

        possible_match = next(
            (
                pool
                for name, address, pool in existing_match_values
                if (
                    candidate_name
                    and name
                    and (candidate_name in name or name in candidate_name)
                )
                or (
                    candidate_address
                    and address
                    and (candidate_address in address or address in candidate_address)
                )
            ),
            None,
        )

        if possible_match:
            review_candidates.append(
                {
                    **candidate,
                    "match_reason": "similar name/address",
                    "matched_pool_id": possible_match.get("id"),
                    "matched_pool_name": possible_match.get("pool_name"),
                }
            )
        else:
            insert_candidates.append(candidate)

    return insert_candidates, update_candidates, review_candidates, skipped


def print_sample(title: str, rows: list[dict[str, Any]], limit: int = 10) -> None:
    print(f"\n{title}")
    if not rows:
        print("- none")
        return

    for row in rows[:limit]:
        print(
            "- "
            f"{row.get('pool_name')} / "
            f"{row.get('pool_address')} / "
            f"lat={row.get('latitude'):.6f} / "
            f"lng={row.get('longitude'):.6f}"
        )
        if row.get("matched_pool_name"):
            print(f"  match: {row.get('matched_pool_name')} ({row.get('match_reason')})")


def main() -> None:
    api_key = get_seoul_open_api_key()
    rows = fetch_license_rows(api_key)
    active_rows = [row for row in rows if is_active_pool(row)]
    rows_with_coordinates = [row for row in active_rows if has_coordinate(row)]
    rows_without_coordinates = [row for row in active_rows if not has_coordinate(row)]

    candidates: list[dict[str, Any]] = []
    conversion_failed: list[dict[str, Any]] = []
    for row in rows_with_coordinates:
        try:
            candidates.append(normalize_pool_candidate(row))
        except (TypeError, ValueError) as error:
            conversion_failed.append(
                {
                    "pool_name": clean_value(row.get("BPLCNM")),
                    "reason": f"coordinate conversion failed: {error}",
                }
            )

    existing_pools = fetch_existing_pools()
    insert_candidates, update_candidates, review_candidates, skipped = classify_candidates(
        candidates,
        existing_pools,
    )

    print("[Seoul Pool License Preview]")
    print(f"total rows: {len(rows)}")
    print(f"active rows: {len(active_rows)}")
    print(f"active rows with EPSG:5174 coordinates: {len(rows_with_coordinates)}")
    print(f"active rows without coordinates: {len(rows_without_coordinates)}")
    print(f"coordinate conversion failed: {len(conversion_failed)}")
    print(f"existing pools: {len(existing_pools)}")
    print(f"insert candidates: {len(insert_candidates)}")
    print(f"update candidates: {len(update_candidates)}")
    print(f"manual review candidates: {len(review_candidates)}")
    print(f"skipped candidates: {len(skipped)}")

    print_sample("Sample insert candidates:", insert_candidates)
    print_sample("Sample update candidates:", update_candidates)
    print_sample("Sample manual review candidates:", review_candidates)

    if rows_without_coordinates:
        print("\nRows without coordinates:")
        for row in rows_without_coordinates[:10]:
            print(f"- {clean_value(row.get('BPLCNM'))} / {clean_value(row.get('RDNWHLADDR'))}")

    if conversion_failed:
        print("\nCoordinate conversion failures:")
        for row in conversion_failed[:10]:
            print(f"- {row.get('pool_name')} / {row.get('reason')}")


if __name__ == "__main__":
    main()
