import pytest
import json
import re
from backend.api.lol_scraper import (
    get_languages,
    get_current_patch,
    convert_item_to_lol_jsons,
    get_runes_data,
)


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


class TestGetRunesData:
    def test_get_runes_data_returns_list(self, tmp_path):
        data = get_runes_data("13.1.1", tmp_path)
        assert isinstance(data, list)
        assert isinstance(data[0], dict)

    # def test_get_runes_data_loads_data_from_file(self, tmp_path):
    #     file_name = tmp_path / "runes_data.json"
    #     expected_data = {"test": 123}
    #     with open(file_name, "w") as file:
    #         json.dump(expected_data, file)
    #     data = get_runes_data("13.1.1")
    #     assert data == expected_data
