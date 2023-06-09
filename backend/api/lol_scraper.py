import json
from os.path import exists
from pathlib import Path
import pandas as pd
import requests
from requests.exceptions import RequestException
from backend.api.logger import BackendLogger
from backend.api.utils import create_parser, request_get, setup_folders


logger = BackendLogger.logger

def get_languages() -> list:
    """Fetches the available languages for League of Legends.

    Returns:
        list: The available languages.
    """
    url = "https://ddragon.leagueoflegends.com/cdn/languages.json"
    return request_get(url)


def get_current_patch(position: int = 0) -> str:
    """Fetches the current patch version of League of Legends from the specified URL.

    Returns:
        str: The current patch version of League of Legends or an empty string in case of an error.
    """
    url = "https://ddragon.leagueoflegends.com/api/versions.json"
    try:
        return request_get(url)[position]
    except Exception as e:
        logger.error(e)
        return ""


def get_champions_data(version: str, folder: Path = Path("data")) -> list:
    """Gets champions data from a League of Legends API.
        If the JSON file is not present or write_output flag is set,
        retrieves champion data from API and saves to local file. Else, it loads champion data from the local file.

    Args:
        version (str): The API version (League of Legends patch) on which the data should be retrieved.
        folder (Path, optional): The directory path where the JSON file will be saved/loaded.

    Returns:
        list: A list of dictionaries of champions data.
    """
    file_name = folder / "champions_data.json"
    if not exists(file_name):
        url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json"
        response = request_get(url)["data"]
        data = {}
        for champion in response:
            data[response[champion]["key"]] = {
                "id": response[champion]["key"],
                "key_name": response[champion]["id"],
                "name": response[champion]["name"],
                "title": response[champion]["title"],
                "image": {
                    "full": response[champion]["image"]["full"],
                    "sprite": response[champion]["image"]["sprite"],
                },
                "tags": response[champion]["tags"],
            }

        with open(file_name, "w+", encoding="UTF-8") as file:
            file.write(json.dumps(data, indent=4, ensure_ascii=False))

    with open(file_name, "r+", encoding="UTF-8") as file:
        return json.loads(file.read())


def get_runes_data(version: str, folder: Path = Path("data")) -> list:
    """Gets runes data from a League of Legends API.
        If the JSON file is not present or write_output flag is set,
        retrieves champion data from API and saves to local file. Else, it loads runes data from the local file.

    Args:
        version (str): The API version (League of Legends patch) on which the data should be retrieved.
        folder (Path, optional): The directory path where the JSON file will be saved/loaded.

    Returns:
        list: A list of dictionaries with runes data.
    """
    file_name = folder / "runes_data.json"
    try:
        if not file_name.exists():
            url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/runesReforged.json"
            response = requests.get(url)
            response.raise_for_status()

            url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/es_MX/runesReforged.json"
            response_es = requests.get(url)
            response_es.raise_for_status()

            data = response.json()
            for i in range(len(data)):
                for j in range(len(data[i]["slots"])):
                    runes = data[i]["slots"][j]["runes"]
                    for k in range(len(runes)):
                        current_data = data[i]["slots"][j]["runes"][k]
                        del current_data["shortDesc"]
                        del current_data["longDesc"]
                        current_data["name_es"] = response_es.json()[i]["slots"][j][
                            "runes"
                        ][k]["name"]
                        data[i]["slots"][j]["runes"][k] = current_data
            with open(file_name, "w+", encoding="UTF-8") as file:
                file.write(json.dumps(data, indent=4, ensure_ascii=False))

        with open(file_name, "r+", encoding="UTF-8") as file:
            return json.loads(file.read())

    except (RequestException, IOError, json.JSONDecodeError) as e:
        print(f"Error retrieving runes data: {e}")
        return []


def get_items_data(version: str, folder: Path = Path("data")) -> list:
    """Gets items data from a League of Legends API.
        If the JSON file is not present or write_output flag is set,
        retrieves champion data from API and saves to local file. Else, it loads items data from the local file.

    Args:
        version (str): The API version (League of Legends patch) on which the data should be retrieved.
        folder (Path, optional): The directory path where the JSON file will be saved/loaded.

    Returns:
        list: A list of dictionaries with items data.
    """
    file_name = folder / "items_data.json"
    if not file_name.exists():
        url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/item.json"
        response = request_get(url)["data"]
        url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/es_MX/item.json"
        response_es = request_get(url)["data"]
        data = {}
        for key in response.keys():
            data[key] = {
                "id": key,
                "name": response[key]["name"],
                "name_es": response_es[key]["name"],
                "image": {
                    "full": response[key]["image"]["full"],
                    "sprite": response[key]["image"]["sprite"],
                },
                "tags": response[key]["tags"],
            }

        with open(file_name, "w+", encoding="UTF-8") as file:
            file.write(json.dumps(data, indent=4, ensure_ascii=False))
        # return data
    # else:
    with open(file_name, "r+", encoding="UTF-8") as file:
        return json.loads(file.read())


def convert_item_to_lol_jsons(items: list) -> list:
    """Convert a list of items to list of dictionaries.

    Args:
        items (List[int]): List of item ids we want to convert.

    Returns:
        List[Dict[str, Union[str, int]]]: List of dictionaries containing each item's id as a string and count as 1.
    """
    return [{"id": str(i), "count": 1} for i in items]


def main():
    pass
    # setup_folders()

    # parser = create_parser()
    # args = parser.parse_args()
    # champion_id = args.champion_name
    # # TODO: Fix this:
    # current_patch = get_current_patch()
    # champions_data = get_champions_data(current_patch)
    # champion_name = champions_data[champion_id]["name"]
    # lane = args.lane  # top, jungle, middle, bottom, support
    # tier = args.tier  # gold_plus, platinum_plus, diamond_plus, all, 1trick
    # mode = args.mode  # ranked, aram
    # match mode:
    #     case "ranked":
    #         mode = 420
    #     case "aram":
    #         mode = 450
    #         lane = "middle"
    # keystone_name = args.keystone_name
    # json_file = create_build(
    #     champion_id=champion_id,
    #     lane=lane,
    #     tier=tier,
    #     mode=mode,
    #     keystone_id=keystone_name,
    # )

    # champion_folder_path = Path(f"Champions/{champion_name}/Recommended")
    # if not champion_folder_path.exists():
    #     champion_folder_path.mkdir(parents=True, exist_ok=True)

    # build_path = champion_folder_path / f"{champion_name}_{lane}_{keystone_name}.json"
    # with open(build_path, "w+", encoding="UTF-8") as file:
    #     file.write(json.dumps(json_file, indent=4))

    # if args.Import:
    #     import_build(build_path, json_file)
