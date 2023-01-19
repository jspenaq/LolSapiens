import argparse
import requests
import json
import pandas as pd

# import numpy as np


def get_languages() -> list:
    url = "https://ddragon.leagueoflegends.com/cdn/languages.json"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers).json()
    return response


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
    if write_output:
        url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/{lang}/runesReforged.json"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers).json()
        data = {}
        for r in response:
            keystones = r["slots"][0]["runes"]
            for i in range(len(keystones)):
                data[keystones[i]["key"]] = keystones[i]["id"]
        file = open("runes_data.json", "w+")
        file.write(json.dumps(data))
        return data
    else:
        file = open("runes_data.json", "r+")
        return json.loads(file.read())


def get_items_data(
    version: str, lang: str = "en_US", write_output: bool = False
) -> dict:
    if write_output:
        url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/{lang}/item.json"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers).json()
        data = response["data"]
        filtered = {key: data[key]["name"] for key in data.keys()}
        file = open("items_data.json", "w+")
        file.write(json.dumps(filtered))
        return data
    else:
        file = open("items_data.json", "r+")
        return json.loads(file.read())


def convert_item_to_lol_jsons(items: list) -> list:
    items_jsons = []
    for i in items:
        items_jsons.append({"id": str(i), "count": 1})
    return items_jsons


def create_build(champion_name: str, lane: str, tier: str, keystone_name: str) -> dict:
    current_patch = get_current_patch()
    champions_data = get_champions_data(current_patch)
    runes_data = get_runes_data(current_patch)
    items_data = get_items_data(current_patch)
    base_url = "https://axe.lolalytics.com/mega"
    patch = ".".join(current_patch.split(".")[:2])
    # champion_name = "Hecarim"
    champion_id = champions_data[champion_name]["key"]
    # lane = "top"  # top, jungle, middle, bottom, support
    # tier = "1trick"  # gold_plus, platinum_plus, diamond_plus, all, 1trick
    region = "all"
    # keystone_name = "GraspOfTheUndying"
    keystone = runes_data[keystone_name]

    print(f"Searching {champion_name} {lane}")
    url = f"{base_url}/?ep=champion&p=d&v=1&patch={patch}&cid={champion_id}&lane={lane}&tier={tier}&queue=420&region={region}&keystone={keystone}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers).json()
    blocks = {
        "startSet": "Starting Set",
        "mythicItem": "Mythic Item",
        "item1": "1st Item",
        "boots": "Boots",
        "item2": "2nd Item",
        "item3": "3rd Item",
        "item4": "4th Item",
        "item5": "5th Item",
    }

    build_json = {}
    build_file = open("builds/recommend_build.txt", "w+")
    build_file.write(f"{champion_name} {lane} - {keystone_name}\n\n")
    build_json["title"] = f"PPC - {lane} {champion_name} - {keystone_name}"
    build_json["associatedMaps"] = [11, 12]
    build_json["associatedChampions"] = [int(champion_id)]
    build_json["blocks"] = []

    skillOrder = response["skills"]["skillOrder"][0][0]
    skillOrder = " > ".join([skill for skill in skillOrder])
    build_file.write(skillOrder)
    build_file.write("\n\n")

    for b in blocks.keys():
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
                    "type": f"{blocks[b]} ({skillOrder})",
                }
            )
        else:
            if "9999" in recommended_sorted["item_id"].values:
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
    args = parser.parse_args()
    champion_name = args.champion_name
    lane = args.lane  # top, jungle, middle, bottom, support
    tier = args.tier  # gold_plus, platinum_plus, diamond_plus, all, 1trick
    keystone_name = args.keystone_name
    print(f"{champion_name} {lane} {tier} {keystone_name}")
    # json_file = create_build(
    #     champion_name=champion_name, lane=lane, tier=tier, keystone_name=keystone_name
    # )
    # file = open(f"builds/{champion_name}_{lane}_{keystone_name}.json", "w+")
    # file.write(json.dumps(json_file))


main()
print("Done")
