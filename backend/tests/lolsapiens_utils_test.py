from pathlib import Path
import pytest
from backend.api.utils import (
    request_get,
    setup_folders,
    percentage_division,
    create_parser,
)


class TestRequestGet:
    def test_non_json_response(self):
        url = "https://google.com"
        with pytest.raises(ValueError, match="Response is not in JSON format"):
            request_get(url)

    def test_request_get_failed_request(self):
        url = "https://nonexistent.url"
        with pytest.raises(ValueError, match="Failed to make a request"):
            request_get(url)


class TestPercentageDivision:
    def test_division(self):
        assert percentage_division(50, 100) == 50.0
        assert percentage_division(0, 100) == 0

    def test_division_by_zero(self):
        zero = percentage_division(0, 0)
        assert zero == 0


class TestSetupFolders:
    def test_folder_creation(self, tmp_path):
        # Test that the folders are created if they do not exist
        result = setup_folders(tmp_path)
        assert result == True
        for folder_name in ["data", "Champions"]:
            folder = Path(folder_name)
            assert folder.exists() == True

    def test_folder_already_exists(self, tmp_path):
        # Test that the folders are not recreated if they already exist
        data = tmp_path / "data"
        data.mkdir()
        champions = tmp_path / "Champions"
        champions.mkdir()
        result = setup_folders(tmp_path)
        assert result == True
        for folder_name in ["data", "Champions"]:
            folder = Path(folder_name)
            assert folder.exists() == True

    # def test_folder_creation_exception(self, tmp_path):
    #     # Test that an exception is raised if folder creation fails
    #     with pytest.raises(Exception) as e:
    #         setup_folders(tmp_path)
    #     assert str(e.value) == "An exception occurred while creating folder data:"


class TestCreateParser:
    def test_parser_defaults(self):
        """Test if the parser returns the expected defaults"""
        parser = create_parser()

        args = parser.parse_args([])
        assert args.start is False
        assert args.champion_name is None
        assert args.lane is None
        assert args.tier == "platinum_plus"
        assert args.mode == "ranked"
        assert args.keystone_name is None
        assert args.Import is False
