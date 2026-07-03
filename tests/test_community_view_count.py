import unittest
from unittest.mock import patch

from fastapi import HTTPException

from app.community import router as community_router
from app.community import service as community_service


class FakeResult:
    def __init__(self, data):
        self.data = data


class FakeRPC:
    def __init__(self, client):
        self.client = client

    def execute(self):
        return FakeResult(self.client.rpc_result)


class FakeQuery:
    def __init__(self, client):
        self.client = client

    def select(self, *_args, **_kwargs):
        return self

    def order(self, column, desc=False):
        self.client.orders.append((column, desc))
        return self

    def limit(self, _limit):
        return self

    def execute(self):
        return FakeResult([])


class FakeSupabase:
    def __init__(self):
        self.rpc_result = 13
        self.rpc_calls = []
        self.orders = []

    def rpc(self, function_name, params):
        self.rpc_calls.append((function_name, params))
        return FakeRPC(self)

    def table(self, table_name):
        if table_name != "communities":
            raise AssertionError(f"unexpected table: {table_name}")
        return FakeQuery(self)


class CommunityViewCountTest(unittest.TestCase):
    def setUp(self):
        self.fake_supabase = FakeSupabase()
        self.original_supabase = community_service.supabase
        community_service.supabase = self.fake_supabase

    def tearDown(self):
        community_service.supabase = self.original_supabase

    def test_transform_post_uses_database_view_count(self):
        post = {
            "id": 1,
            "view_cnt": 12,
            "users": {},
            "images": [],
        }

        transformed = community_router._transform_post(post)

        self.assertEqual(transformed["viewCnt"], 12)

    def test_transform_post_detail_uses_database_view_count(self):
        post = {
            "id": 1,
            "view_cnt": 15,
            "users": {},
            "images": [],
        }

        transformed = community_router._transform_post_detail(post, [], None)

        self.assertEqual(transformed["viewCnt"], 15)

    def test_increment_community_view_count_normalizes_scalar_result(self):
        result = community_service.increment_community_view_count(7)

        self.assertEqual(result, 13)
        self.assertEqual(
            self.fake_supabase.rpc_calls,
            [("increment_community_view_count", {"p_post_id": 7})],
        )

    def test_increment_community_view_count_normalizes_list_result(self):
        self.fake_supabase.rpc_result = [13]

        result = community_service.increment_community_view_count(7)

        self.assertEqual(result, 13)

    def test_increment_community_view_count_returns_none_for_missing_post(self):
        self.fake_supabase.rpc_result = None

        result = community_service.increment_community_view_count(999)

        self.assertIsNone(result)

    def test_get_top_view_posts_orders_by_views_then_created_at(self):
        community_service.get_top_view_posts(6)

        self.assertEqual(
            self.fake_supabase.orders,
            [("view_cnt", True), ("created_at", True)],
        )

    def test_get_community_increments_after_detail_dependencies_succeed(self):
        with (
            patch.object(community_router.service, "get_community", return_value={"id": 7, "users": {}, "images": []}),
            patch.object(community_router.comments_service, "get_comments", return_value=[]),
            patch.object(community_router.service, "get_like_info", return_value={"likesCnt": 0, "isLiked": False}),
            patch.object(community_router.service, "increment_community_view_count", return_value=13) as increment,
        ):
            result = community_router.get_community("7")

        increment.assert_called_once_with(7)
        self.assertEqual(result["data"]["viewCnt"], 13)

    def test_get_community_does_not_increment_when_comments_fail(self):
        with (
            patch.object(community_router.service, "get_community", return_value={"id": 7, "users": {}, "images": []}),
            patch.object(community_router.comments_service, "get_comments", side_effect=RuntimeError("comments failed")),
            patch.object(community_router.service, "increment_community_view_count") as increment,
        ):
            with self.assertRaisesRegex(RuntimeError, "comments failed"):
                community_router.get_community("7")

        increment.assert_not_called()

    def test_get_community_for_edit_does_not_increment(self):
        post = {"id": 7, "author_id": "user-1", "users": {}, "images": []}
        with (
            patch.object(community_router.service, "get_community", return_value=post),
            patch.object(community_router.service, "increment_community_view_count") as increment,
        ):
            result = community_router.get_community_for_edit(
                "7",
                {"sub": "user-1"},
            )

        increment.assert_not_called()
        self.assertEqual(result["data"]["postId"], 7)

    def test_get_community_for_edit_rejects_non_author(self):
        post = {"id": 7, "author_id": "user-1", "users": {}, "images": []}
        with patch.object(community_router.service, "get_community", return_value=post):
            with self.assertRaises(HTTPException) as context:
                community_router.get_community_for_edit(
                    "7",
                    {"sub": "user-2"},
                )

        self.assertEqual(context.exception.status_code, 403)


if __name__ == "__main__":
    unittest.main()
