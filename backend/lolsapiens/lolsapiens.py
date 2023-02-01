import requests
import json
import pandas as pd
from os import makedirs
from os.path import exists, dirname
from backend.lolsapiens.sapiens import Sapiens
from backend.lolsapiens.utils import create_parser, setup_folders, request_get
import platform


def get_languages() -> list:
    url = "https://ddragon.leagueoflegends.com/cdn/languages.json"
    return request_get(url)


def get_current_patch() -> str:
    url = "https://ddragon.leagueoflegends.com/api/versions.json"
    return request_get(url)[0]


def get_champions_data(
    version: str, lang: str = "en_US", write_output: bool = False
) -> dict:
    url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/{lang}/champion.json"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers).json()
    return response["data"]


def get_runes_data(version: str, write_output: bool = False) -> dict:
    file_name = "data/runes_data.json"
    if not exists(file_name) or write_output:
        url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/runesReforged.json"
        response = request_get(url)
        url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/es_MX/runesReforged.json"
        response_es = request_get(url)
        data = {}
        for i in range(len(response)):
            for j in range(len(response[i]["slots"])):
                runes = response[i]["slots"][j]["runes"]
                for k in range(len(runes)):
                    data[runes[k]["id"]] = {
                        "key": response[i]["slots"][j]["runes"][k]["key"],
                        "name_en": response[i]["slots"][j]["runes"][k]["name"],
                        "name_es": response_es[i]["slots"][j]["runes"][k]["name"],
                    }
        with open(file_name, "w+", encoding="UTF-8") as file:
            file.write(json.dumps(data, indent=4, ensure_ascii=False))
        return data
    else:
        with open(file_name, "r+", encoding="UTF-8") as file:
            return json.loads(file.read())


def get_items_data(version: str, write_output: bool = False) -> dict:
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
        return data
    else:
        with open(file_name, "r+", encoding="UTF-8") as file:
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
    # keystone = runes_data[keystone_name]["key"]
    keystone = keystone_name

    print(f"Searching {champion_name} {lane}")
    url = f"{base_url}/?ep=champion&p=d&v=1&patch={patch}&cid={champion_id}&lane={lane}&tier={tier}&queue=420&region={region}&keystone={keystone}"
    response = request_get(url)
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
        s = Sapiens()
        recommended = s.analyze(df)
        
        if b == "startSet":
            # split cases such as: "3850_2003_2003" into [3850, 2003, 2003] 
            recommended["item_name"] = recommended["item_id"].apply(
                lambda id: ", ".join([items_data[x]["name_en"] for x in id.split("_")])
            )
            recommended["item_name_es"] = recommended["item_id"].apply(
                lambda id: ", ".join([items_data[x]["name_es"] for x in id.split("_")])
            )
            starting_set = recommended["item_id"][0].split("_")
            # starting_set.append([]) # todo: add wards, lens
            build_json["blocks"].append(
                {
                    "items": convert_item_to_lol_jsons(starting_set),
                    "type": f"{value} ({skillOrder})",
                }
            )
        else:
            if "9999" in recommended["item_id"].values:  # No boots
                recommended.drop(recommended[recommended['item_id'] == "9999"].index, inplace = True)
            if recommended.empty:
                print("EMPTY")
                continue
            recommended["item_name"] = recommended["item_id"].apply(
                lambda id: items_data[id]["name_en"]
            )
            recommended["item_name_es"] = recommended["item_id"].apply(
                lambda id: items_data[id]["name_es"]
            )
            build_json["blocks"].append(
                {
                    "items": convert_item_to_lol_jsons(
                        list(recommended["item_id"])
                    ),
                    "type": blocks[b],
                }
            )
            recommended.drop(columns=["time"], inplace=True)
        recommended.drop(columns=["index"], inplace=True)
        build_file.write(recommended.to_string())
        print(recommended)
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
