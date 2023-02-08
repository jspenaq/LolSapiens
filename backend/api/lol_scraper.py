import json
import pandas as pd
from os.path import exists
from pathlib import Path
from backend.api.utils import (
    create_parser,
    import_build,
    setup_folders,
    request_get,
)


def get_languages() -> list:
    """Fetches the available languages for League of Legends.

    Returns:
        list: The available languages.
    """
    url = "https://ddragon.leagueoflegends.com/cdn/languages.json"
    return request_get(url)


def get_current_patch() -> str:
    """Fetches the current patch version of League of Legends from the specified URL.

    Returns:
        str: The current patch version of League of Legends or an empty string in case of an error.
    """
    url = "https://ddragon.leagueoflegends.com/api/versions.json"
    try:
        return request_get(url)[0]
    except Exception as e:
        print(e)
        return ""


def get_champions_data(version: str, write_output: bool = False) -> dict:
    """Gets champions data from a League of Legends API.
        If the JSON file is not present or write_output flag is set,
        retrieves champion data from API and saves to local file. Else, it loads champion data from the local file.

    Args:
        version (str): The API version (League of Legends patch) on which the data should be retrieved.
        write_output (bool, optional): True if output should be written to a file. Defaults to False.

    Returns:
        dict: Dictionary of champions data.
    """
    file_name = "data/champions_data.json"
    if not exists(file_name) or write_output:
        url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json"
        response = request_get(url)["data"]
        data = {}
        for champion in response:
            champion_data = response[champion]
            data[champion_data["key"]] = {
                "id": champion_data["id"],
                "name": champion_data["name"],
            }
        with open(file_name, "w+", encoding="UTF-8") as file:
            file.write(json.dumps(data, indent=4, ensure_ascii=False))

    with open(file_name, "r+", encoding="UTF-8") as file:
        return json.loads(file.read())


def get_runes_data(version: str, write_output: bool = False) -> dict:
    """Gets runes data from a League of Legends API.
        If the JSON file is not present or write_output flag is set,
        retrieves champion data from API and saves to local file. Else, it loads runes data from the local file.

    Args:
        version (str): The API version (League of Legends patch) on which the data should be retrieved.
        write_output (bool, optional): True if output should be written to a file. Defaults to False.

    Returns:
        dict: Dictionary of runes data.
    """
    file_name = "data/runes_data.json"
    if not exists(file_name) or write_output:
        url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/runesReforged.json"
        response = request_get(url)
        url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/es_MX/runesReforged.json"
        response_es = request_get(url)
        # data = {}
        for i in range(len(response)):
            for j in range(len(response[i]["slots"])):
                runes = response[i]["slots"][j]["runes"]
                for k in range(len(runes)):
                    # data[runes[k]["id"]] = {
                    #     "key": response[i]["slots"][j]["runes"][k]["key"],
                    #     "name_en": response[i]["slots"][j]["runes"][k]["name"],
                    #     "name_es": response_es[i]["slots"][j]["runes"][k]["name"],
                    # }
                    del response[i]["slots"][j]["runes"][k]["shortDesc"]
                    del response[i]["slots"][j]["runes"][k]["longDesc"]
                    response[i]["slots"][j]["runes"][k]["name_es"] = response_es[i][
                        "slots"
                    ][j]["runes"][k]["name"]
        with open(file_name, "w+", encoding="UTF-8") as file:
            file.write(json.dumps(response, indent=4, ensure_ascii=False))

    with open(file_name, "r+", encoding="UTF-8") as file:
        return json.loads(file.read())


def get_items_data(version: str, write_output: bool = False) -> dict:
    """Gets items data from a League of Legends API.
        If the JSON file is not present or write_output flag is set,
        retrieves champion data from API and saves to local file. Else, it loads items data from the local file.

    Args:
        version (str): The API version (League of Legends patch) on which the data should be retrieved.
        write_output (bool, optional): True if output should be written to a file. Defaults to False.

    Returns:
        dict: Dictionary of items data.
    """
    file_name = "data/items_data.json"
    if not exists(file_name) or write_output:
        url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/item.json"
        response = request_get(url)["data"]
        url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/es_MX/item.json"
        response_es = request_get(url)["data"]
        data = {}
        for key in response.keys():
            data[key] = {
                "name_en": response[key]["name"],
                "name_es": response_es[key]["name"],
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
    setup_folders()

    parser = create_parser()
    args = parser.parse_args()
    champion_id = args.champion_name
    # TODO: Fix this:
    current_patch = get_current_patch()
    champions_data = get_champions_data(current_patch)
    champion_name = champions_data[champion_id]["name"]
    lane = args.lane  # top, jungle, middle, bottom, support
    tier = args.tier  # gold_plus, platinum_plus, diamond_plus, all, 1trick
    mode = args.mode  # ranked, aram
    # match mode:
    #     case "ranked":
    #         mode = 420
    #     case "aram":
    #         mode = 450
    #         lane = "middle"
    keystone_name = args.keystone_name
    json_file = create_build(
        champion_id=champion_id,
        lane=lane,
        tier=tier,
        mode=mode,
        keystone_id=keystone_name,
    )

    champion_folder_path = Path(f"Champions/{champion_name}/Recommended")
    if not champion_folder_path.exists():
        champion_folder_path.mkdir(parents=True, exist_ok=True)

    build_path = champion_folder_path / f"{champion_name}_{lane}_{keystone_name}.json"
    with open(build_path, "w+", encoding="UTF-8") as file:
        file.write(json.dumps(json_file, indent=4))

    if args.Import:
        import_build(build_path, json_file)
