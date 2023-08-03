import argparse
import json
import platform
import re
from pathlib import Path
import requests
from backend.api.logger import BackendLogger
from numpy import average
from bs4 import BeautifulSoup

logger = BackendLogger().logger


def request_get(url: str, useHTML: bool = False):
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
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()

        if useHTML:
            return response.text
        if "application/json" in response.headers.get("Content-Type"):
            return response.json()
        else:
            raise ValueError("Response is not in JSON format")
    except requests.exceptions.RequestException as e:
        raise ValueError("Failed to make a request") from e


def transform_data_from_lolsociety(lolsociety_data: dict) -> dict:
    # soup = BeautifulSoup(html)
    # divs = soup.find_all("div", class_="flex row flex-wrap items-center gap-6 mt-4")
    data = {
        "skills": [],
        "startSet": [],
        "boots": [],
        "item1": [],
        "item2": [],
        "item3": [],
    }

    # [0]: item_id, [1]: win_rate, [2]: pick_rate, [3]: games, [4]: time
    # startSet example:
    # [['3850_2003_2003', 51.69, 92.13, 7120],
    # ['3858_2003_2003', 46.51, 2.78, 215],
    # ['3862_2003_2003', 100, 0.03, 2],
    # [2033, 50, 0.03, 2],
    # ['2003_2003_2003']]
    def inner_transform(key_src, key_dst):
        for item in lolsociety_data[key_src]:
            if "id" in item:
                item_id = item["id"]
            else:
                # Skills
                skills = {"Q": item["skill1"], "W": item["skill2"], "E": item["skill3"]}
                if 0 in skills.values():
                    continue
                sorted_skills = sorted(skills.keys(), key=lambda x: skills[x])
                item_id = "".join(sorted_skills)
            if item_id == 0:
                continue
            win_rate = round(((item["avgPlacement"] - 4) / -3) * 100, 2)
            pick_rate = item["games"]
            games = item["games"]
            data[key_dst].append([item_id, win_rate, pick_rate, games])

    inner_transform("skillOrder", "skills")
    inner_transform("startingItems", "startSet")
    inner_transform("boots", "boots")
    inner_transform("firstItems", "item1")
    inner_transform("midItems", "item2")
    inner_transform("lateItems", "item3")
    # boots example:
    # [[3158, 53.14, 60.29, 4659, 13],
    # [3020, 51.56, 26.88, 2077, 16],
    # [1001, 30.88, 5.45, 421, 7],
    # [3111, 53.3, 2.74, 212, 17]]

    # win_rate = ((score - 4) / -3) * 100

    # Starting Items, Boots, First Item, Other Items
    # if len(divs) == 4:
    #     starting_items, boots, first_item, other_items = divs
    # items = starting_items.findAll(
    #     "div", class_="flex row px-4 py-2 bg-blue-xbold rounded-lg"
    # )
    # for item in items:
    #     print(item.img.get("alt"))  # item name
    #     src = item.img.get("src")
    #     id = re.search(r"\w(\d+)\.png", src)
    #     print(id.group(1))  # item id
    #     print(item.div.contents[0].text)  # Win rate (Average Placement)
    #     print(item.div.contents[1].text)  # Games
    #     print("===")
    # print(items)
    # print(html)

    return data


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
        choices=[
            "gold_plus",
            "platinum_plus",
            "emerald_plus",
            "diamond_plus",
            "all",
            "1trick",
        ],
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


def setup_folders(path: Path = Path("")) -> bool:
    """Create necessary folders and files in the given path.

    Args:
        path (Path, optional): The directory path where the folders should be created. Defaults to Path("").

    Returns:
         bool: True if all folders were successfully created, False otherwise.
    """
    folders = ["data", "Champions"]
    for folder_name in folders:
        folder = path / Path(folder_name)
        if not folder.exists():
            try:
                folder.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                logger.error(
                    f"An exception occurred while creating folder {folder_name}:"
                )
                logger.error(e)
                return False
    return True


# def import_build(build_path: Path, json_file: dict) -> bool:
#     system = platform.system()
#     base_path = ""
#     match system:
#         case "Windows":
#             base_path = "C:\\Riot Games\\League of Legends"
#         case "Darwin":
#             base_path = "/Applications/League of Legends.app/Contents/LoL"
#         case _:
#             return False

#     system_path = f"{base_path}/Config/" / build_path
#     if not system_path.parent.exists():
#         system_path.parent.mkdir(parents=True, exist_ok=True)
#     with open(system_path, "w+", encoding="UTF-8") as file:
#         file.write(json.dumps(json_file, indent=4))
#     return True


def percentage_division(value: int, total: int) -> float | int:
    """Calculates the percentage of a value out of a total, and returns the result as a float or a zero.

    Args:
        value (int): The value to be converted to a percentage.
        total (int): The total value to be used as the denominator in the percentage calculation.

    Returns:
        float | int: The function returns the percentage of value out of total as a float.
        If division raises ZeroDivisionError, the function returns 0.
    """
    try:
        return value * 100 / total
    except ZeroDivisionError:
        return 0


def weighted_average(data: list, weights: list) -> float | int:
    """Calculates the weighted average of a list of data values.

    Args:
        data (list): A list of numeric values to be averaged.
        weights (list): A list of weights to be used in the weighted average calculation.

    Returns:
        float | int: The weighted average of the data values, or 0 if raises ZeroDivisionError.
    """
    try:
        return average(data, weights=weights)
    except ZeroDivisionError:
        return 0


def convert_queue_mode(queue_mode: str) -> int:
    """If queue_mode is equal to "aram", the function returns 450, otherwise, it returns 420.

    Args:
        queue_mode (str): The queue mode to be converted. It should be either "aram" or some other string (example: "ranked").

    Returns:
        int: An integer representing the converted queue mode.
    """
    queue = 420  # ranked
    match queue_mode:
        case "aram":
            queue = 450
        case "arena":
            queue = 1500
    return queue
