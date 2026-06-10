import importlib.util
from pathlib import Path
import unittest


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "preview_pool_license_data.py"
SPEC = importlib.util.spec_from_file_location("preview_pool_license_data", SCRIPT_PATH)
preview = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(preview)


class PreviewPoolLicenseDataTest(unittest.TestCase):
    def test_convert_tm_to_wgs84_returns_latitude_and_longitude(self):
        latitude, longitude = preview.convert_tm_to_wgs84(
            "206383.829438022",
            "446030.128073052",
        )

        self.assertAlmostEqual(latitude, 37.516478, places=5)
        self.assertAlmostEqual(longitude, 127.072998, places=5)

    def test_is_active_pool_requires_normal_business_status(self):
        active_row = {"TRDSTATENM": "영업/정상", "DTLSTATENM": "영업중"}
        closed_row = {"TRDSTATENM": "폐업", "DTLSTATENM": "폐업"}

        self.assertTrue(preview.is_active_pool(active_row))
        self.assertFalse(preview.is_active_pool(closed_row))

    def test_normalize_pool_candidate_maps_api_row_to_pool_fields(self):
        row = {
            "OPNSFTEAMCODE": "3230000",
            "MGTNO": "CDFH3301012015000001",
            "BPLCNM": "잠실실내수영장",
            "RDNWHLADDR": "서울특별시 송파구 올림픽로 25 (잠실동, 종합운동장)",
            "SITEWHLADDR": "서울특별시 송파구 잠실동 10",
            "SITETEL": "",
            "TRDSTATENM": "영업/정상",
            "DTLSTATENM": "영업중",
            "APVPERMYMD": "2015-08-03",
            "DCBYMD": "          ",
            "X": "206383.829438022    ",
            "Y": "446030.128073052    ",
        }

        candidate = preview.normalize_pool_candidate(row)

        self.assertEqual(candidate["source"], "seoul-pool-license")
        self.assertEqual(
            candidate["external_id"],
            "3230000:CDFH3301012015000001",
        )
        self.assertEqual(candidate["pool_name"], "잠실실내수영장")
        self.assertEqual(candidate["region"], "서울/송파")
        self.assertAlmostEqual(candidate["latitude"], 37.516478, places=5)
        self.assertAlmostEqual(candidate["longitude"], 127.072998, places=5)

    def test_classify_candidates_updates_exact_address_match(self):
        candidate = {
            "source": "seoul-pool-license",
            "external_id": "public-1",
            "pool_name": "잠실실내수영장",
            "pool_address": "서울특별시 송파구 올림픽로 25 (잠실동, 종합운동장)",
        }
        existing_pool = {
            "id": 1,
            "pool_name": "잠실종합운동장 수영장",
            "pool_address": "서울 송파구 올림픽로 25",
        }

        inserts, updates, reviews, skipped = preview.classify_candidates(
            [candidate],
            [existing_pool],
        )

        self.assertEqual(inserts, [])
        self.assertEqual(len(updates), 1)
        self.assertEqual(updates[0]["match_reason"], "same normalized address")
        self.assertEqual(reviews, [])
        self.assertEqual(skipped, [])

    def test_classify_candidates_matches_existing_external_id_to_pool_id(self):
        candidate = {
            "source": "seoul-pool-license",
            "external_id": "public-1",
            "pool_name": "잠실실내수영장",
            "pool_address": "서울특별시 송파구 올림픽로 25",
        }
        existing_pool = {
            "id": 11,
            "source": "seoul-pool-license",
            "external_id": "public-1",
            "pool_name": "잠실실내수영장",
            "pool_address": "서울특별시 송파구 올림픽로 25",
        }

        inserts, updates, reviews, skipped = preview.classify_candidates(
            [candidate],
            [existing_pool],
        )

        self.assertEqual(inserts, [])
        self.assertEqual(len(updates), 1)
        self.assertEqual(updates[0]["matched_pool_id"], 11)
        self.assertEqual(updates[0]["match_reason"], "same external_id")
        self.assertEqual(reviews, [])
        self.assertEqual(skipped, [])

    def test_classify_candidates_reviews_same_name_with_different_address(self):
        candidate = {
            "source": "seoul-pool-license",
            "external_id": "public-2",
            "pool_name": "마린 스포츠센터",
            "pool_address": "서울특별시 노원구 한글비석로 145",
        }
        existing_pool = {
            "id": 5,
            "pool_name": "마린스포츠센터",
            "pool_address": "서울 강서구 공항대로 200",
        }

        inserts, updates, reviews, skipped = preview.classify_candidates(
            [candidate],
            [existing_pool],
        )

        self.assertEqual(inserts, [])
        self.assertEqual(updates, [])
        self.assertEqual(len(reviews), 1)
        self.assertEqual(reviews[0]["match_reason"], "similar name/address")
        self.assertEqual(skipped, [])

    def test_classify_candidates_applies_manual_update_decision(self):
        candidate = {
            "source": "seoul-pool-license",
            "external_id": "3230000:CDFH3301011190000001",
            "pool_name": "잠실실내수영장",
            "pool_address": "서울특별시 송파구 올림픽로 25 (잠실동, 종합운동장)",
        }
        existing_pool = {
            "id": 1,
            "pool_name": "잠실종합운동장 수영장",
            "pool_address": "서울 송파구 올림픽로 25",
        }

        inserts, updates, reviews, skipped = preview.classify_candidates(
            [candidate],
            [existing_pool],
        )

        self.assertEqual(inserts, [])
        self.assertEqual(len(updates), 1)
        self.assertEqual(updates[0]["matched_pool_id"], 1)
        self.assertEqual(updates[0]["match_reason"], "manual decision: same facility")
        self.assertEqual(reviews, [])
        self.assertEqual(skipped, [])

    def test_classify_candidates_applies_manual_insert_decisions(self):
        separate_facilities = [
            ("3230000:CDFH3301011994000001", "한강공원 잠실수영장"),
            ("3140000:CDFH3301012025000001", "국가대표 어린이 수영클럽 목동역점"),
            ("3230000:CDFH3301012022000003", "아쿠아랩 잠실 롯데월드점"),
            ("3150000:CDFH3301012001000001", "강서구민올림픽체육센터"),
            ("3100000:CDFH3301012002000001", "마린 스포츠센터"),
            ("3140000:CDFH3301011989000002", "시립목동청소년센터"),
        ]
        existing_pools = [
            {
                "id": 1,
                "pool_name": "잠실종합운동장 수영장",
                "pool_address": "서울 송파구 올림픽로 25",
            },
            {
                "id": 2,
                "pool_name": "올림픽수영장",
                "pool_address": "서울 송파구 방이동 88",
            },
            {
                "id": 3,
                "pool_name": "목동실내수영장",
                "pool_address": "서울 양천구 목동서로 225",
            },
            {
                "id": 5,
                "pool_name": "마린스포츠센터",
                "pool_address": "서울 강서구 공항대로 200",
            },
        ]
        candidates = [
            {
                "source": "seoul-pool-license",
                "external_id": external_id,
                "pool_name": pool_name,
                "pool_address": f"서울특별시 테스트구 {index}",
            }
            for index, (external_id, pool_name) in enumerate(separate_facilities)
        ]

        inserts, updates, reviews, skipped = preview.classify_candidates(
            candidates,
            existing_pools,
        )

        self.assertEqual(len(inserts), 6)
        self.assertTrue(
            all(
                row["match_reason"] == "manual decision: separate facility"
                for row in inserts
            )
        )
        self.assertEqual(updates, [])
        self.assertEqual(reviews, [])
        self.assertEqual(skipped, [])


if __name__ == "__main__":
    unittest.main()
