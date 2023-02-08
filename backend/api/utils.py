import argparse
import json
import platform
import requests
from pathlib import Path


def request_get(url: str):
    """Makes a GET request to the specified URL and returns the response in JSON format.

    Args:
        url (str): The URL to make the GET request to.

    Raises:
        ValueError: If the response is not in JSON format or if the request fails.

    Returns:
        Any: The response in JSON format.
    """
    headers = {"accept": "application/json"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        if response.headers.get("Content-Type") == "application/json":
            return response.json()
        else:
            raise ValueError("Response is not in JSON format")
    except requests.exceptions.RequestException as e:
        raise ValueError("Failed to make a request") from e


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--start",
        action="store_true",
        help="Start backend server using fastpi and uvicorn",
    )
    parser.add_argument("-c", "--champion-name", help="Champion name")
    parser.add_argument(
        "-l",
        "--lane",
        choices=["top", "jungle", "middle", "bottom", "support"],
        help="Lane",
    )
    parser.add_argument(
        "-t",
        "--tier",
        default="platinum_plus",
        choices=["gold_plus", "platinum_plus", "diamond_plus", "all", "1trick"],
        help="Tier data",
    )
    parser.add_argument(
        "-m",
        "--mode",
        default="ranked",
        choices=["ranked", "aram"],
        help="Queue mode",
    )
    parser.add_argument(
        "-k",
        "--keystone-name",
        # choices=[],
        help="Keystone id",
    )
    parser.add_argument(
        "--import",
        action="store_true",
        help="Import automatically to League of Legends folder",
        dest="Import",
    )

    return parser


def setup_folders() -> bool:
    folders = ["data", "Champions"]
    for folder_name in folders:
        folder = Path(folder_name)
        if not folder.exists():
            try:
                folder.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                print(f"An exception occurred while creating folder {folder_name}:")
                print(e)
                return False
    return True


def import_build(build_path: Path, json_file: dict) -> bool:
    system = platform.system()
    base_path = ""
    match system:
        case "Windows":
            base_path = "C:\\Riot Games\\League of Legends"
        case "Darwin":
            base_path = "/Applications/League of Legends.app/Contents/LoL"
        case _:
            return False

    system_path = f"{base_path}/Config/" / build_path
    if not system_path.parent.exists():
        system_path.parent.mkdir(parents=True, exist_ok=True)
    with open(system_path, "w+", encoding="UTF-8") as file:
        file.write(json.dumps(json_file, indent=4))
    return True


def percentange_division(value: int, total: int) -> float | int:
    try:
        return value * 100 / total
    except ZeroDivisionError:
        return 0
