from pathlib import Path
import pytest
from backend.api.utils import request_get, setup_folders


class TestRequestGet:
    def test_non_json_response(self):
        url = "https://google.com"
        with pytest.raises(ValueError, match="Response is not in JSON format"):
            request_get(url)

    def test_request_get_failed_request(self):
        url = "https://nonexistent.url"
        with pytest.raises(ValueError, match="Failed to make a request"):
            request_get(url)


# class TestSetupFolders:
#     def test_folder_creation(self):
#         # Test that the folders are created if they do not exist
#         result = setup_folders()
#         assert result == True
#         for folder_name in ["data", "Champions"]:
#             folder = Path(folder_name)
#             assert folder.exists() == True

#     def test_folder_already_exists(self):
#         # Test that the folders are not recreated if they already exist
#         os.mkdir("data")
#         os.mkdir("Champions")
#         result = setup_folders()
#         assert result == True
#         for folder_name in ["data", "Champions"]:
#             folder = Path(folder_name)
#             assert folder.exists() == True

#     def test_folder_creation_exception(self):
#         # Test that an exception is raised if folder creation fails
#         with pytest.raises(Exception) as e:
#             setup_folders()
#         assert str(e.value) == "An exception occurred while creating folder data:"
