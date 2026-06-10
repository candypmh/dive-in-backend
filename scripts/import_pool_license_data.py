from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any


BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

POOL_COLUMNS = {
    "source",
    "external_id",
    "pool_name",
    "pool_address",
    "region",
    "contact",
    "latitude",
    "longitude",
    "license_status",  
    "license_date",
    "closed_date",
    "road_address",
    "lot_address",
}


def to_pool_payload(candidate: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in candidate.items()
        if key in POOL_COLUMNS and value is not None
    }


def to_insert_payload(candidate: dict[str, Any]) -> dict[str, Any]:
    payload = to_pool_payload(candidate)
    payload.setdefault("contact", "")
    return payload


def import_candidates(
    client: Any,
    insert_candidates: list[dict[str, Any]],
    update_candidates: list[dict[str, Any]],
    review_candidates: list[dict[str, Any]],
) -> dict[str, int]:
    if review_candidates:
        raise RuntimeError(
            f"{len(review_candidates)} manual review candidates must be resolved before import."
        )

    inserted = 0
    updated = 0

    if insert_candidates:
        payloads = [to_insert_payload(candidate) for candidate in insert_candidates]
        client.table("pools").insert(payloads).execute()
        inserted = len(payloads)

    for candidate in update_candidates:
        pool_id = candidate.get("matched_pool_id")
        if pool_id is None:
            raise RuntimeError(
                f"Update candidate has no matched_pool_id: {candidate.get('external_id')}"
            )

        client.table("pools").update(to_pool_payload(candidate)).eq("id", pool_id).execute()
        updated += 1

    return {"inserted": inserted, "updated": updated}


def build_import_plan() -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    from scripts.preview_pool_license_data import (
        classify_candidates,
        fetch_existing_pools,
        fetch_license_rows,
        get_seoul_open_api_key,
        has_coordinate,
        is_active_pool,
        normalize_pool_candidate,
    )

    rows = fetch_license_rows(get_seoul_open_api_key())
    candidates = [
        normalize_pool_candidate(row)
        for row in rows
        if is_active_pool(row) and has_coordinate(row)
    ]
    return classify_candidates(candidates, fetch_existing_pools())


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Import Seoul pool license data into Supabase pools."
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Write candidates to Supabase. Without this flag, only print the plan.",
    )
    args = parser.parse_args()

    insert_candidates, update_candidates, review_candidates, skipped = build_import_plan()
    print("[Seoul Pool License Import]")
    print(f"insert candidates: {len(insert_candidates)}")
    print(f"update candidates: {len(update_candidates)}")
    print(f"manual review candidates: {len(review_candidates)}")
    print(f"skipped candidates: {len(skipped)}")

    if not args.execute:
        print("dry-run only: rerun with --execute after applying the reviewed schema SQL.")
        return

    from app.db import supabase

    result = import_candidates(
        supabase,
        insert_candidates,
        update_candidates,
        review_candidates,
    )
    print(f"inserted: {result['inserted']}")
    print(f"updated: {result['updated']}")


if __name__ == "__main__":
    main()
