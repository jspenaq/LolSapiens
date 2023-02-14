import pytest
import re
from backend.api.lol_scraper import get_languages, get_current_patch, convert_item_to_lol_jsons


class TestGetLanguages:
    def test_languages_type(self):
        languages = get_languages()
        assert isinstance(languages, list)

    def test_languages_content(self):
        languages = get_languages()
        assert len(languages) > 0


class TestGetCurrentPatch:
    def test_patch_type(self):
        current_patch = get_current_patch()
        assert isinstance(current_patch, str)

    def test_patch_value(self):
        current_patch = get_current_patch()
        assert current_patch != ""

    def test_patch_format(self):
        current_patch = get_current_patch()
        assert re.match(r"^\d+\.\d+\.\d+$", current_patch) is not None


class TestConvertItemToLolJsons:
    def test_empty_list(self):
        items = []
        assert convert_item_to_lol_jsons(items) == []

    def test_list_conversion(self):
        items = [1001, 1004, 1006]
        expected_output = [
            {"id": "1001", "count": 1},
            {"id": "1004", "count": 1},
            {"id": "1006", "count": 1},
        ]
        assert convert_item_to_lol_jsons(items) == expected_output
