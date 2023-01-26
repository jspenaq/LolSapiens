import requests
import json
import pandas as pd
from os import makedirs
from os.path import exists, dirname
from lolsapiens.utils import create_parser, setup_folders
import platform


def get_languages() -> list:
    url = "https://ddragon.leagueoflegends.com/cdn/languages.json"
    headers = {"accept": "application/json"}
    return requests.get(url, headers=headers).json()


def get_current_patch() -> str:
    url = "https://ddragon.leagueoflegends.com/api/versions.json"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers).json()
    return response[0]


def get_champions_data(
    version: str, lang: str = "en_US", write_output: bool = False
) -> dict:
    url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/{lang}/champion.json"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers).json()
    return response["data"]


def get_runes_data(
    version: str, lang: str = "en_US", write_output: bool = False
) -> dict:
    file_name = "data/runes_data.json"
    if not exists(file_name) or write_output:
        url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/{lang}/runesReforged.json"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers).json()
        data = {}
        for r in response:
            keystones = r["slots"][0]["runes"]
            for i in range(len(keystones)):
                data[keystones[i]["key"]] = keystones[i]["id"]
        file = open(file_name, "w+")
        file.write(json.dumps(data, indent=4))
        return data
    else:
        file = open(file_name, "r+")
        return json.loads(file.read())


def get_items_data(
    version: str, lang: str = "en_US", write_output: bool = False
) -> dict:
    file_name = "data/items_data.json"
    if not exists(file_name) or write_output:
        url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/{lang}/item.json"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers).json()
        data = response["data"]
        filtered = {key: data[key]["name"] for key in data.keys()}
        file = open(file_name, "w+")
        file.write(json.dumps(filtered, indent=4))
        return filtered
    else:
        file = open(file_name, "r+")
        return json.loads(file.read())


def convert_item_to_lol_jsons(items: list) -> list:
    return [{"id": str(i), "count": 1} for i in items]


def create_build(champion_name: str, lane: str, tier: str, keystone_name: str) -> dict:
    current_patch = get_current_patch()
    champions_data = get_champions_data(current_patch)
    runes_data = get_runes_data(current_patch)
    items_data = get_items_data(current_patch)
    base_url = "https://axe.lolalytics.com/mega"
    patch = ".".join(current_patch.split(".")[:2])
    champion_id = champions_data[champion_name]["key"]
    region = "all"
    keystone = runes_data[keystone_name]

    print(f"Searching {champion_name} {lane}")
    url = f"{base_url}/?ep=champion&p=d&v=1&patch={patch}&cid={champion_id}&lane={lane}&tier={tier}&queue=420&region={region}&keystone={keystone}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers).json()
    blocks = {
        "startSet": "Starting Set",
        "item1": "1st Item",
        "mythicItem": "Mythic Item",
        "boots": "Boots",
        "item2": "2nd Item",
        "item3": "3rd Item",
        "item4": "4th Item",
        "item5": "5th Item",
    }

    build_file = open("Champions/recommend_build.txt", "w+")
    build_file.write(f"{champion_name} {lane} - {keystone_name}\n\n")
    build_json = {
        "title": f"LolSapiens - {lane} {champion_name} - {keystone_name}",
        "type": "custom",
        "associatedMaps": [11, 12],
        "associatedChampions": [int(champion_id)],
        "map": "any",
        "mode": "any",
        "preferredItemSlots": [],
        "sortrank": 1,
        "startedFrom": "blank",
        "blocks": [],
    }
    skillOrder = response["skills"]["skillOrder"][0][0]
    skillOrder = " > ".join(list(skillOrder))
    build_file.write(skillOrder)
    build_file.write("\n\n")

    for b, value in blocks.items():
        print(f"=== {b} ===")
        build_file.write(f"=== {b} ===\n")
        if b not in response.keys():
            continue

        items = response[b]
        # [0]: item_id, [1]: win_rate, [2]: pick_rate, [3]: games, [4]: time,
        if len(items) > 7:
            items = items[:7]

        columns = ["item_id", "win_rate", "pick_rate", "games", "time"]
        if b == "startSet":
            columns = columns[:4]

        df = pd.DataFrame(items, columns=columns)
        print(df)
        percentile = df["games"].quantile(0.60)
        print(f"{percentile=}")
        recommended = df[df["games"] >= percentile]
        recommended_sorted = recommended.sort_values(by="win_rate", ascending=False)
        recommended_sorted["item_id"] = recommended_sorted["item_id"].astype(str)
        recommended_sorted = recommended_sorted.reset_index()
        if b == "startSet":
            recommended_sorted["item_name"] = recommended_sorted["item_id"].apply(
                lambda id: ", ".join([items_data[x] for x in id.split("_")])
            )
            starting_set = recommended_sorted["item_id"][0].split("_")
            # starting_set.append([]) # todo: add wards, lens
            build_json["blocks"].append(
                {
                    "items": convert_item_to_lol_jsons(starting_set),
                    "type": f"{value} ({skillOrder})",
                }
            )
        else:
            if "9999" in recommended_sorted["item_id"].values:  # No boots
                continue
            recommended_sorted["item_name"] = recommended_sorted["item_id"].apply(
                lambda id: items_data[id]
            )
            build_json["blocks"].append(
                {
                    "items": convert_item_to_lol_jsons(
                        list(recommended_sorted["item_id"])
                    ),
                    "type": blocks[b],
                }
            )
        build_file.write(recommended_sorted.to_string())
        print(recommended_sorted)
        build_file.write("\n\n")

    return build_json


def main():
    setup_folders()

    parser = create_parser()
    args = parser.parse_args()
    champion_name = args.champion_name
    lane = args.lane  # top, jungle, middle, bottom, support
    tier = args.tier  # gold_plus, platinum_plus, diamond_plus, all, 1trick
    keystone_name = args.keystone_name
    json_file = create_build(
        champion_name=champion_name, lane=lane, tier=tier, keystone_name=keystone_name
    )

    if not exists(f"Champions\\{champion_name}\\Recommended"):
        makedirs(f"Champions\\{champion_name}\\Recommended")

    build_file_name = f"Champions\\{champion_name}\\Recommended\\{champion_name}_{lane}_{keystone_name}.json"
    file = open(
        build_file_name,
        "w+",
    )
    file.write(json.dumps(json_file, indent=4))

    if args.Import:
        system = platform.system()
        base_path = ""
        if system == "Windows":
            base_path = "C:\\Riot Games\\League of Legends"
        elif system == "Darwin":
            pass
        elif system == "Linux":
            pass
        else:
            pass

        system_path = f"{base_path}\\Config\\{build_file_name}"
        if not exists(dirname(system_path)):
            makedirs(dirname(system_path))
        file = open(
            system_path,
            "w+",
        )
        file.write(json.dumps(json_file, indent=4))
