from backend.api.constants import (
    champion_id_param,
    lane_param,
    tier_param,
    queue_mode_param,
    keystone_id_param,
    spicy_param,
)
from fastapi import Query


class TestConstants:
    def test_champion_id_param(self):
        value = champion_id_param
        assert value.title == "champion_id"
        assert value.description != ""
        assert value.example != ""

    def test_lane_param(self):
        value = lane_param
        assert value.default == "default"
        assert value.title == "lane"
        assert value.description != ""
        assert value.example != ""

    def test_tier_param(self):
        value = tier_param
        assert value.default == "platinum_plus"
        assert value.title == "tier"
        assert isinstance(value.description, str)
        assert isinstance(value.example, str)

    def test_queue_mode_param(self):
        value = queue_mode_param
        assert value.default == "ranked"
        assert value.title == "queue_mode"
        assert isinstance(value.description, str)
        assert isinstance(value.example, str)

    def test_keystone_id_param(self):
        value = keystone_id_param
        assert value.default == 0
        assert value.title == "keystone_id"
        assert isinstance(value.description, str)
        assert isinstance(value.example, int)

    def test_spicy_param(self):
        value = spicy_param
        assert value.default == 0
        assert value.title == "spicy_factor"
        assert isinstance(value.description, str)
        assert isinstance(value.example, int)
