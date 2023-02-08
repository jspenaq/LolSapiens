from abc import abstractmethod
import json
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
        print("Initializing Sapiens...")
        setup_folders()
        self.current_patch = get_current_patch()
        self.champions_data = get_champions_data(self.current_patch)
        self.runes_data = get_runes_data(self.current_patch)
        self.items_data = get_items_data(self.current_patch)
        self.base_url = "https://axe.lolalytics.com"  # LoLalytics
        self.patch = ".".join(self.current_patch.split(".")[:2])
        self.tierlist = self._get_tierlist()

    def _get_tierlist(
        self, lane: str = "default", tier: str = "platinum_plus"
    ) -> pd.DataFrame:
        file_name = Path(f"data/tierlist_{lane}_{tier}.csv")
        if not file_name.exists():
            url = f"{self.base_url}/tierlist/2/?lane={lane}&patch={self.patch}&tier={tier}&queue=420&region=all"
            response = request_get(url)
            with open(file_name, "w+", encoding="UTF-8") as file:
                columns = [
                    "id",
                    "rank",
                    "wins_by_lane",
                    "games_by_lane",
                    "win_rate",
                    "total_games",
                    "pick_by_lane",
                    "ban_rate",
                    "pick_rate",
                    "rank_last_days",
                    "win_rate_last_days",
                    "games_last_days",
                    "wins_by_lane_last_days",
                    "games_by_lane_last_days",
                    "delta_pick_lane",
                ]
                file.write(",".join(columns))
                file.write("\n")
                total_games_by_tier = response["pick"]
                round_ndigits = 4

                for champion_id, value in response["cid"].items():
                    # value:
                    # [0]: rank, [1]: , [2]: , [3]: wins_by_lane, [4]: games_by_lane, [5]: total_games, [6]: ban_rate, [7]: rank_last_days,
                    # [8]: win_rate_last_days, [9]: games_last_days, [10]: , [11]: wins_by_lane_last_days, [12]: games_by_lane_last_days,
                    output = [
                        champion_id,
                        value[0],
                        value[3],
                        value[4],
                        round(value[3] * 100 / value[4], round_ndigits),
                        value[5],
                        round(value[4] * 100 / value[5], round_ndigits),
                        value[6],
                        round(value[4] * 100 / total_games_by_tier, round_ndigits),
                        value[7],
                        value[8],
                        value[9],
                        value[11],
                        value[12],
                        round(
                            value[3] * 100 / value[4] - value[11] * 100 / value[12],
                            round_ndigits,
                        ),
                    ]
                    output = list(map(str, output))
                    file.write(",".join(output))
                    file.write("\n")

        return pd.read_csv(file_name)

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

    def analyze_bans(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Analyze which champions to ban using statistics in the provided data frame.

        Args:
            df (pd.DataFrame): A pandas data frame containing champion statistics.

        Returns:
            pd.DataFrame: Data frame with the top 10 champions to ban.
        """
        mean = df["pick_rate"].mean()
        median = df["pick_rate"].median()
        df = df[df["pick_rate"] > max(mean, median)]
        df = df.sort_values(by="win_rate", ascending=False)
        return df.head(10)[["id", "win_rate", "pick_rate"]]

    def get_top10_bans(
        self,
        lane: str = "default",
        tier: str = "platinum_plus",
    ) -> list:
        """Fetches the top ten banned champions in the given lane and tier.

        Args:
            lane (str, optional): the name of the lane to filter the tier list by.
            tier (str, optional): the tier to filter the tier list by.

        Returns:
            list: A dictionaries list with the following format:
            {
                "id": champion id,
                "value": value for the specified champion,
                "name": name for the specified champion,
                "win_rate": win rate for the specified champion,
                "pick_rate": pick rate for the specified champion,
            }
        """
        df = self._get_tierlist(lane, tier)
        ids = self.analyze_bans(df)
        data = []
        for _, row in ids.iterrows():
            champion_id = int(row["id"])
            data.append(
                {
                    "id": champion_id,
                    "value": self.champions_data[str(champion_id)]["id"],
                    "name": self.champions_data[str(champion_id)]["name"],
                    "win_rate": row["win_rate"],
                    "pick_rate": row["pick_rate"],
                }
            )
        return data

    def _analyze_picks(self, df: pd.DataFrame) -> pd.DataFrame:

        mean_pickrate = df["pick_rate"].mean()
        median_pickrate = df["pick_rate"].median()
        mean_winrate = df["win_rate"].mean()
        median_winrate = df["win_rate"].median()
        df = df[
            (df["pick_rate"] < max(mean_pickrate, median_pickrate))
            & (df["win_rate"] > max(mean_winrate, median_winrate))
            & (df["games_by_lane"] >= 5)
        ]
        df = df.sort_values(by="win_rate", ascending=False).reset_index()
        return df[["id", "win_rate", "pick_rate"]]

    def get_top10_picks(
        self,
        lane: str = "default",
        tier: str = "platinum_plus",
        limit: int = 10,
        random: int = 0,
    ) -> list:
        """Fetches the top ten spicy champions picks in the given lane and tier.

        Args:
            lane (str, optional): the name of the lane to filter the tier list by.
            tier (str, optional): the tier to filter the tier list by.
            limit (int, optional):
            random (int, optional):

        Returns:
            list: A dictionaries list with the following format:
            {
                "id": champion id,
                "value": value for the specified champion,
                "name": name for the specified champion,
                "win_rate": win rate for the specified champion,
                "pick_rate": pick rate for the specified champion,
            }
        """
        df = self._get_tierlist(lane, tier)
        ids = self._analyze_picks(df)
        limit = min(limit, 20)
        ids = ids.head(limit)
        if random > 0:
            random = min(random, len(ids))
            ids = ids.sample(random)
        data = []
        for _, row in ids.iterrows():
            champion_id = int(row["id"])
            data.append(
                {
                    "id": champion_id,
                    "value": self.champions_data[str(champion_id)]["id"],
                    "name": self.champions_data[str(champion_id)]["name"],
                    "win_rate": row["win_rate"],
                    "pick_rate": row["pick_rate"],
                }
            )
        return data

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
        url = f"{self.base_url}/mega/?ep=champion&p=d&v=1&patch={self.patch}&cid={champion_id}&lane={lane}&tier={tier}&queue={queue_mode}&region={region}&keystone={keystone_id}"
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
