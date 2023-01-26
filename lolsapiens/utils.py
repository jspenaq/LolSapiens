import argparse
from os import makedirs
from os.path import exists, dirname
import platform
import shutil


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
        "-k",
        "--keystone-name",
        # choices=[],
        help="Keystone name",
    )
    parser.add_argument(
        "--import",
        action="store_true",
        help="Import automatically to League of Legends folder",
        dest="Import",
    )

    return parser


def import_build(build_file_name: str):
    os = platform.system()
    base_path = ""
    if os == "Windows":
        base_path = "C:\\Riot Games\\League of Legends"
    elif os == "Darwin":
        pass
    elif os == "Linux":
        pass
    else:
        return

    path = f"{base_path}\\Config\\{build_file_name}"
    if not exists(dirname(path)):
        makedirs(dirname(path))
    shutil.copy(build_file_name, path)


def setup_folders() -> bool:
    try:
        if not exists("data"):
            makedirs("data")

        if not exists("Champions"):
            makedirs("Champions")

    except Exception as e:
        print("An exception occurred:")
        print(e)
        return False

    return True
