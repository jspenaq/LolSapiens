import json
import pandas as pd
from os.path import exists
from pathlib import Path
from backend.lolsapiens.sapiens import Sapiens
from backend.lolsapiens.utils import (
    create_parser,
    import_build,
    setup_folders,
    request_get,
)


def get_languages() -> list:
    url = "https://ddragon.leagueoflegends.com/cdn/languages.json"
    return request_get(url)


def get_current_patch() -> str:
    url = "https://ddragon.leagueoflegends.com/api/versions.json"
    return request_get(url)[0]


def get_champions_data(version: str, write_output: bool = False) -> dict:
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
        # return data
    # else:
    with open(file_name, "r+", encoding="UTF-8") as file:
        return json.loads(file.read())


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
        # return data
    # else:
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
        # return data
    # else:
    with open(file_name, "r+", encoding="UTF-8") as file:
        return json.loads(file.read())


def convert_item_to_lol_jsons(items: list) -> list:
    return [{"id": str(i), "count": 1} for i in items]


def create_build(champion_id: str, lane: str, tier: str, mode: int, keystone_id: str) -> dict:
    current_patch = get_current_patch()
    champions_data = get_champions_data(current_patch)
    runes_data = get_runes_data(current_patch)
    items_data = get_items_data(current_patch)
    base_url = "https://axe.lolalytics.com/mega"
    patch = ".".join(current_patch.split(".")[:2])
    champion_name = champions_data[champion_id]["name"]
    region = "all"
    # keystone = runes_data[keystone_id]["key"]
    keystone = keystone_id

    print(f"Searching {champion_name} {lane}")
    url = f"{base_url}/?ep=champion&p=d&v=1&patch={patch}&cid={champion_id}&lane={lane}&tier={tier}&queue={mode}&region={region}&keystone={keystone}"
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

    build_txt_path = Path("Champions/recommend_build.txt")
    with open(build_txt_path, "w+", encoding="UTF-8") as build_file:
        build_file.write(
            f"{champion_name} {lane} - {runes_data[keystone_id]['name_en']} ({runes_data[keystone_id]['name_es']})\n\n"
        )
        build_json = {
            "title": f"LolSapiens - {lane} {champion_name} - {runes_data[keystone_id]['name_en']} ({runes_data[keystone_id]['name_es']})",
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
                    lambda id: ", ".join(
                        [items_data[x]["name_en"] for x in id.split("_")]
                    )
                )
                recommended["item_name_es"] = recommended["item_id"].apply(
                    lambda id: ", ".join(
                        [items_data[x]["name_es"] for x in id.split("_")]
                    )
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
                    recommended.drop(
                        recommended[recommended["item_id"] == "9999"].index,
                        inplace=True,
                    )
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
    champion_id = args.champion_name
    # TODO: Fix this:
    current_patch = get_current_patch()
    champions_data = get_champions_data(current_patch)
    champion_name = champions_data[champion_id]["name"]
    lane = args.lane  # top, jungle, middle, bottom, support
    tier = args.tier  # gold_plus, platinum_plus, diamond_plus, all, 1trick
    mode = args.mode  # ranked, aram
    match mode:
        case "ranked":
            mode = 420
        case "aram":
            mode = 450
            lane = "middle"
    keystone_name = args.keystone_name
    json_file = create_build(
        champion_id=champion_id, lane=lane, tier=tier, mode=mode, keystone_id=keystone_name
    )

    champion_folder_path = Path(f"Champions/{champion_name}/Recommended")
    if not champion_folder_path.exists():
        champion_folder_path.mkdir(parents=True, exist_ok=True)

    build_path = champion_folder_path / f"{champion_name}_{lane}_{keystone_name}.json"
    with open(build_path, "w+", encoding="UTF-8") as file:
        file.write(json.dumps(json_file, indent=4))

    if args.Import:
        import_build(build_path, json_file)
