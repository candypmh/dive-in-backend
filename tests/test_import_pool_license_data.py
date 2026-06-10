import importlib.util
from pathlib import Path
import unittest


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "import_pool_license_data.py"
SPEC = importlib.util.spec_from_file_location("import_pool_license_data", SCRIPT_PATH)
pool_import = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pool_import)


class FakeQuery:
    def __init__(self, calls, operation, payload=None):
        self.calls = calls
        self.operation = operation
        self.payload = payload
        self.pool_id = None

    def eq(self, column, value):
        self.pool_id = value
        return self

    def execute(self):
        self.calls.append(
            {
                "operation": self.operation,
                "payload": self.payload,
                "pool_id": self.pool_id,
            }
        )
        return type("Result", (), {"data": self.payload})()


class FakeTable:
    def __init__(self, calls):
        self.calls = calls

    def insert(self, payload):
        return FakeQuery(self.calls, "insert", payload)

    def update(self, payload):
        return FakeQuery(self.calls, "update", payload)


class FakeSupabase:
    def __init__(self):
        self.calls = []

    def table(self, table_name):
        if table_name != "pools":
            raise AssertionError(f"unexpected table: {table_name}")
        return FakeTable(self.calls)


class ImportPoolLicenseDataTest(unittest.TestCase):
    def test_to_pool_payload_removes_preview_metadata(self):
        candidate = {
            "source": "seoul-pool-license",
            "external_id": "public-1",
            "pool_name": "잠실실내수영장",
            "pool_address": "서울특별시 송파구 올림픽로 25",
            "latitude": 37.5,
            "longitude": 127.0,
            "match_reason": "manual decision: same facility",
            "matched_pool_id": 1,
            "matched_pool_name": "잠실종합운동장 수영장",
        }

        payload = pool_import.to_pool_payload(candidate)

        self.assertNotIn("match_reason", payload)
        self.assertNotIn("matched_pool_id", payload)
        self.assertNotIn("matched_pool_name", payload)
        self.assertEqual(payload["external_id"], "public-1")

    def test_to_pool_payload_omits_null_values(self):
        candidate = {
            "source": "seoul-pool-license",
            "external_id": "public-1",
            "pool_name": "전화번호 없는 수영장",
            "pool_address": "서울특별시 송파구 테스트로 1",
            "contact": None,
            "closed_date": None,
        }

        payload = pool_import.to_pool_payload(candidate)

        self.assertNotIn("contact", payload)
        self.assertNotIn("closed_date", payload)

    def test_to_insert_payload_defaults_missing_contact_to_empty_string(self):
        candidate = {
            "source": "seoul-pool-license",
            "external_id": "public-1",
            "pool_name": "전화번호 없는 수영장",
            "pool_address": "서울특별시 송파구 테스트로 1",
            "contact": None,
        }

        payload = pool_import.to_insert_payload(candidate)

        self.assertEqual(payload["contact"], "")

    def test_import_candidates_inserts_and_updates_expected_rows(self):
        client = FakeSupabase()
        insert_candidate = {
            "source": "seoul-pool-license",
            "external_id": "public-new",
            "pool_name": "신규 수영장",
            "pool_address": "서울특별시 송파구 신규로 1",
        }
        update_candidate = {
            "source": "seoul-pool-license",
            "external_id": "public-existing",
            "pool_name": "기존 수영장",
            "pool_address": "서울특별시 송파구 기존로 1",
            "matched_pool_id": 7,
            "match_reason": "same external_id",
        }

        result = pool_import.import_candidates(
            client,
            [insert_candidate],
            [update_candidate],
            [],
        )

        self.assertEqual(result, {"inserted": 1, "updated": 1})
        self.assertEqual(client.calls[0]["operation"], "insert")
        self.assertEqual(client.calls[1]["operation"], "update")
        self.assertEqual(client.calls[1]["pool_id"], 7)

    def test_import_candidates_rejects_unresolved_reviews(self):
        client = FakeSupabase()

        with self.assertRaisesRegex(RuntimeError, "manual review"):
            pool_import.import_candidates(
                client,
                [],
                [],
                [{"external_id": "review-1"}],
            )

        self.assertEqual(client.calls, [])


if __name__ == "__main__":
    unittest.main()
