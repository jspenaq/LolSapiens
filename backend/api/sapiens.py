from abc import abstractmethod
import pandas as pd
from pathlib import Path
from backend.api.lol_scraper import (
    convert_item_to_lol_jsons,
    get_current_patch,
    get_champions_data,
    get_runes_data,
    get_items_data,
)
from backend.api.utils import request_get, setup_folders


class Sapiens:
    def __init__(self):
        print("Init Sapiens...")
        setup_folders()
        self.current_patch = get_current_patch()
        self.champions_data = get_champions_data(self.current_patch)
        self.runes_data = get_runes_data(self.current_patch)
        self.items_data = get_items_data(self.current_patch)
        self.base_url = "https://axe.lolalytics.com/mega"  # LoLalytics
        self.patch = ".".join(self.current_patch.split(".")[:2])

    @abstractmethod
    def analyze(self, df: pd.DataFrame, spicy: int) -> pd.DataFrame:
        standard = df["games"].std(ddof=0)  # Normalize by N instead of N-1
        mean = df["games"].mean()
        cv = standard / mean
        p20 = df["games"].quantile(0.20)
        q1 = df["games"].quantile(0.25)
        q2 = df["games"].quantile(0.50)
        p60 = df["games"].quantile(0.60)
        q3 = df["games"].quantile(0.75)
        maximum = df["games"].max()
        iqr = q3 - q1
        # outliers = df[
        #     ((df["games"] < (q1 - 1.5 * iqr)) | (df["games"] > (q3 + 1.5 * iqr)))
        # ]
        upper_outliers = df[(df["games"] > (q3 + 1.5 * iqr))]
        upper_outliers = len(upper_outliers) > 0

        # Determine method based on CV and presence of upper outliers
        method = 0
        if cv > 1.5:
            method = 0
        elif 1.5 > cv > 1.0:
            method = 2
        elif 1.0 > cv > 0.5:
            method = 4
        elif cv < 0.5:
            method = 6

        method += spicy
        if upper_outliers:
            method -= 1

        method = max(method, 0)  # method < 0
        method = min(method, 6)  # method > 6
        match method:
            case 0:
                recommended = df[df["games"] >= (maximum - 1 * standard)]
            case 1:
                recommended = df[df["games"] >= (maximum - 1.5 * standard)]
            case 2:
                recommended = df[df["games"] >= q3]
            case 3:
                recommended = df[df["games"] >= p60]
            case 4:
                recommended = df[df["games"] >= q2]
            case 5:
                recommended = df[df["games"] >= p60]
            case 6:
                recommended = df[df["games"] >= q1]

        recommended_sorted = recommended.sort_values(by="win_rate", ascending=False)
        recommended_sorted["item_id"] = recommended_sorted["item_id"].astype(str)
        return recommended_sorted.reset_index()

    def generate_build(
        self,
        champion_id: str,
        lane: str,
        tier: str,
        mode: str,
        keystone_id: str,
        spicy: int = 0,
    ) -> dict:
        champion_name = self.champions_data[champion_id]["name"]
        queue_mode = 420
        if mode == "aram":
            queue_mode = 450
            lane = "middle"
        region = "all"
        print(f"Searching {champion_name} {lane}")
        url = f"{self.base_url}/?ep=champion&p=d&v=1&patch={self.patch}&cid={champion_id}&lane={lane}&tier={tier}&queue={queue_mode}&region={region}&keystone={keystone_id}"
        response = request_get(url)
        return self._get_build_json(
            response, champion_id, lane, tier, queue_mode, keystone_id, spicy
        )

    def _get_build_json(
        self,
        response: dict,
        champion_id: str,
        lane: str,
        tier: str,
        queue_mode: str,
        keystone_id: str,
        spicy: int,
    ):
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

        champion_name = self.champions_data[champion_id]["name"]
        keystone_name = self.runes_data[keystone_id]["name_en"]
        build_txt_path = Path("Champions/recommend_build.txt")
        with open(build_txt_path, "w+", encoding="UTF-8") as build_file:
            build_file.write(
                f"{champion_name} {lane} - {self.runes_data[keystone_id]['name_en']} ({self.runes_data[keystone_id]['name_es']})\n\n"
            )
            build_json = {
                "title": f"LolSapiens - {lane} {champion_name} - {self.runes_data[keystone_id]['name_en']} ({self.runes_data[keystone_id]['name_es']})",
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
            try:
                skillOrder = response["skills"]["skillOrder"][0][0]
                skillOrder = " > ".join(list(skillOrder))
                build_file.write(skillOrder)
                build_file.write("\n\n")
            except Exception as e:
                print(e)
                return {}

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
                recommended = self.analyze(df, spicy)

                if b == "startSet":
                    # split cases such as: "3850_2003_2003" into [3850, 2003, 2003]
                    recommended["item_name"] = recommended["item_id"].apply(
                        lambda id: ", ".join(
                            [self.items_data[x]["name_en"] for x in id.split("_")]
                        )
                    )
                    recommended["item_name_es"] = recommended["item_id"].apply(
                        lambda id: ", ".join(
                            [self.items_data[x]["name_es"] for x in id.split("_")]
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
                        lambda id: self.items_data[id]["name_en"]
                    )
                    recommended["item_name_es"] = recommended["item_id"].apply(
                        lambda id: self.items_data[id]["name_es"]
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
