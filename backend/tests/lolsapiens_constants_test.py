from backend.api.constants import champion_id_param
from fastapi import Query


class TestConstants:
    def test_champion_id_param(self):
        value = champion_id_param
        assert value.title == "champion_id"
        assert value.description != ""
        assert value.example is not None
 