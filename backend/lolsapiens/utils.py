import argparse
import json
import platform
import requests
from pathlib import Path


def request_get(url: str):
    headers = {"accept": "application/json"}
    return requests.get(url, headers=headers).json()


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
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
    try:
        folder = Path("data")
        if not folder.exists():
            folder.mkdir(parents=True, exist_ok=True)

        folder = Path("Champions")
        if not folder.exists():
            folder.mkdir(parents=True, exist_ok=True)

    except Exception as e:
        print("An exception occurred:")
        print(e)
        return False

    return True


def import_build(build_path: Path, json_file: dict) -> bool:
    system = platform.system()
    base_path = ""
    if system == "Windows":
        base_path = "C:\\Riot Games\\League of Legends"
    elif system == "Darwin":
        base_path = "/Applications/League of Legends.app/Contents/LoL"
    elif system == "Linux":
        pass
    else:
        pass

    system_path = f"{base_path}/Config/" / build_path
    if not system_path.parent.exists():
        system_path.parent.mkdir(parents=True, exist_ok=True)
    with open(system_path, "w+", encoding="UTF-8") as file:
        file.write(json.dumps(json_file, indent=4))
