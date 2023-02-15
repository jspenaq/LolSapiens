import datetime
import pandas as pd
from pathlib import Path
from backend.api.lol_scraper import (
    convert_item_to_lol_jsons,
    get_current_patch,
    get_champions_data,
    get_runes_data,
    get_items_data,
)
from backend.api.utils import percentage_division, request_get, setup_folders
from sklearn.preprocessing import MinMaxScaler


class Sapiens:
    def __init__(self):
        print("Initializing Sapiens...")
        setup_folders()
        self.current_patch = get_current_patch()
        self.champions_data = get_champions_data(self.current_patch)
        self.runes_data = get_runes_data(self.current_patch)
        self.keystones = self._get_keystones()
        self.items_data = get_items_data(self.current_patch)
        self.base_url = "https://axe.lolalytics.com"  # LoLalytics
        self.patch = ".".join(self.current_patch.split(".")[:2])
        self.tierlist = self._get_tierlist()

    def _get_keystones(self):
        runes = self.runes_data
        keystones = []
        for i in range(len(runes)):
            slots = runes[i]["slots"][0]["runes"]
            for j in range(len(slots)):
                keystones.append(slots[j]["id"])
        return keystones

    def _get_tierlist(
        self, lane: str = "default", tier: str = "platinum_plus"
    ) -> pd.DataFrame:
        file_name = Path(f"data/tierlist_{lane}_{tier}.csv")
        time_limit = 6 * 60 * 60  # 6 hours (in seconds)
        exists_flag = file_name.exists()
        if exists_flag:
            # Recent data modification
            time_diff = datetime.datetime.now() - datetime.datetime.fromtimestamp(
                file_name.stat().st_mtime
            )
        if not exists_flag or time_diff.total_seconds() > time_limit:
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
                round_ndigits = 6

                for champion_id, value in response["cid"].items():
                    # value:
                    # [0]: rank, [1]: , [2]: , [3]: wins_by_lane, [4]: games_by_lane, [5]: total_games, [6]: ban_rate, [7]: rank_last_days,
                    # [8]: win_rate_last_days, [9]: games_last_days, [10]: , [11]: wins_by_lane_last_days, [12]: games_by_lane_last_days,
                    output = [
                        champion_id,
                        value[0],
                        value[3],
                        value[4],
                        round(percentage_division(value[3], value[4]), round_ndigits),
                        value[5],
                        round(percentage_division(value[4], value[5]), round_ndigits),
                        value[6],
                        round(
                            percentage_division(value[4], total_games_by_tier),
                            round_ndigits,
                        ),
                        value[7],
                        value[8],
                        value[9],
                        value[11],
                        value[12],
                        round(
                            percentage_division(value[3], value[4])
                            - percentage_division(value[11], value[12]),
                            round_ndigits,
                        ),
                    ]
                    output = list(map(str, output))
                    file.write(",".join(output))
                    file.write("\n")

        return pd.read_csv(file_name)

    def _analyze(self, df: pd.DataFrame, spicy: int) -> pd.DataFrame:
        standard = df["games"].std(ddof=0)  # Normalize by N instead of N-1
        mean = df["games"].mean()
        cv = standard / mean
        p10 = df["games"].quantile(0.10)
        p20 = df["games"].quantile(0.20)
        q1 = df["games"].quantile(0.25)
        q2 = df["games"].quantile(0.50)
        p60 = df["games"].quantile(0.60)
        q3 = df["games"].quantile(0.75)
        maximum = df["games"].max()
        iqr = q3 - q1

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
        method = min(method, 8)  # method > 8
        match method:
            case 0:
                df = df[df["games"] >= (maximum - 1 * standard)]
            case 1:
                df = df[df["games"] >= (maximum - 1.5 * standard)]
            case 2:
                df = df[df["games"] >= q3]
            case 3:
                df = df[df["games"] >= p60]
            case 4:
                df = df[df["games"] >= q2]
            case 5:
                df = df[df["games"] >= q1]
            case 6:
                df = df[df["games"] >= p20]
            case 7:
                df = df[df["games"] >= p10]
            case 8:
                pass

        if len(df) == 1:
            recommended = df.copy()
        else:
            weight_1 = 0.6
            weight_2 = 0.4

            scaler = MinMaxScaler()
            df["games_normalized"] = scaler.fit_transform(df[["games"]])
            df["weighted_result"] = (
                df["win_rate"] * weight_1 + df["games_normalized"] * weight_2
            )
            recommended = df.sort_values(by="weighted_result", ascending=False)

        recommended["id"] = recommended["id"].astype(str)
        return recommended.reset_index()

    def _analyze_bans(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Analyze which champions to ban using statistics in the provided data frame.

        Args:
            df (pd.DataFrame): A pandas data frame containing champion statistics.

        Returns:
            pd.DataFrame: Data frame with the top 10 champions to ban.
        """
        mean = df["pick_rate"].mean()
        median = df["pick_rate"].median()
        p20 = df["ban_rate"].quantile(0.20)
        df = df[(df["pick_rate"] > max(mean, median)) & (df["ban_rate"] > p20)]
        df = df.sort_values(by="win_rate", ascending=False)
        return df.head(10)[["id", "win_rate", "pick_rate"]]

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
        ids = self._analyze_bans(df)
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

    def get_spicy_picks(
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
        keystone_id: int,
        spicy: int = 0,
    ) -> dict:
        champion_name = self.champions_data[champion_id]["name"]
        queue_mode = 420
        if mode == "aram":
            queue_mode = 450
            lane = "middle"
        region = "all"

        print(f"Searching {champion_name} {lane}")
        if keystone_id == 0:
            # key_name = f"win_{tier}"
            recommend_runes = self._get_champion_runes(
                champion_id, lane, tier, queue_mode, spicy
            )
            # if not recommend_runes:
            #     print(f"Recommend runes not found for {tier}")
            #     recommend_runes = self._get_champion_runes(champion_id, lane, spicy)
            #     key_name = "win_platinum_plus"

            keystone_id = int(recommend_runes[0])
        url = f"{self.base_url}/mega/?ep=champion&p=d&v=1&patch={self.patch}&cid={champion_id}&lane={lane}&tier={tier}&queue={queue_mode}&region={region}&keystone={keystone_id}"
        # url = f"{self.base_url}/mega/?ep=champion&p=d&v=1&patch={self.patch}&cid={champion_id}&lane={lane}&tier={tier}&queue={queue_mode}&region={region}"
        response = request_get(url)
        return self._get_build_json(
            response, champion_id, lane, tier, keystone_id, spicy
        )

    def _get_champion_runes(
        self,
        champion_id: str,
        lane: str = "default",
        tier: str = "platinum_plus",
        queue_mode: str = "ranked",
        spicy: int = 0,
    ) -> list:
        """Get the runes for a specific champion.

        Args:
            champion_id (str): The ID of the champion for which to retrieve runes.
            lane (str, optional): The lane for which to retrieve runes. Defaults to "default".
            tier (str, optional): The tier for which to retrieve runes. Defaults to "platinum_plus".
            queue_mode (str, optional): The queue mode for which to retrieve runes. Defaults to "ranked".

        Returns:
            dict: A dictionary containing the runes information, with keys in the format "{win/pick}_{tier}" and
            values as dictionaries containing "primary_path", "secondary_path", and "shards".
            If no runes information is available, an empty dictionary is returned.
        """
        region = "all"
        url = f"{self.base_url}/mega/?ep=champion&p=d&v=1&patch={self.patch}&cid={champion_id}&lane={lane}&tier={tier}&queue={queue_mode}&region={region}"
        response = request_get(url)
        if "runes" not in response:
            return {}

        matrix = []
        for key in self.keystones:
            values = response["runes"]["stats"][str(key)][0]
            # values
            # [0]: pick_rate, [1]: win_rate, [2]: games
            matrix.append([key, values[1], values[2]])

        columns = ["id", "win_rate", "games"]
        df = pd.DataFrame(matrix, columns=columns)
        recommend = self._analyze(df, spicy * 2)
        # runes = {}
        # for i in ["win", "pick"]:
        #     primary_path = response["summary"]["runes"][i]["set"]["pri"]
        #     secondary_path = response["summary"]["runes"][i]["set"]["sec"]
        #     shards = response["summary"]["runes"][i]["set"]["mod"]
        #     runes[f"{i}_{tier}"] = {
        #         "primary_path": primary_path,
        #         "secondary_path": secondary_path,
        #         "shards": shards,
        #     }

        return recommend.head(5)["id"].tolist()

    def __get_runes_names(self, keystone_id: int) -> tuple:
        keystone_preffix = keystone_id // 100 * 100
        if keystone_preffix == 9900:  # Hail of Blades
            keystone_preffix = 8100
        for rune in self.runes_data:
            if rune["id"] == keystone_preffix:
                for slot in rune["slots"]:
                    for reforged in slot["runes"]:
                        if reforged["id"] == keystone_id:
                            return reforged["name"], reforged["name_es"]

    def _get_build_json(
        self,
        response: dict,
        champion_id: str,
        lane: str,
        tier: str,
        keystone_id: int,
        spicy: int,
    ):
        blocks = {
            "startSet": "Starting Set",
            "item1": "1st Item",
            # "mythicItem": "Mythic Item",
            "boots": "Boots",
            "item2": "2nd Item",
            "item3": "3rd Item",
            "item4": "4th Item",
            "item5": "5th Item",
        }

        champion_name = self.champions_data[champion_id]["name"]
        print(f"{keystone_id=}")
        (keystone_name, keystone_name_es) = self.__get_runes_names(keystone_id)
        build_txt_path = Path("Champions/recommend_build.txt")
        with open(build_txt_path, "w+", encoding="UTF-8") as build_file:
            build_file.write(
                f"{champion_name} {lane} - {keystone_name} ({keystone_name_es})\n\n"
            )
            build_json = {
                "title": f"LolSapiens - {champion_name} {lane} - {keystone_name} ({keystone_name_es})",
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

                columns = ["id", "win_rate", "pick_rate", "games", "time"]
                if b == "startSet":
                    columns = columns[:4]

                df = pd.DataFrame(items, columns=columns)
                recommended = self._analyze(df, spicy)

                if b == "startSet":
                    # split cases such as: "3850_2003_2003" into [3850, 2003, 2003]
                    recommended["item_name"] = recommended["id"].apply(
                        lambda id: ", ".join(
                            [self.items_data[x]["name_en"] for x in id.split("_")]
                        )
                    )
                    recommended["item_name_es"] = recommended["id"].apply(
                        lambda id: ", ".join(
                            [self.items_data[x]["name_es"] for x in id.split("_")]
                        )
                    )
                    starting_set = recommended["id"][0].split("_")
                    # starting_set.append([]) # todo: add wards, lens
                    build_json["blocks"].append(
                        {
                            "items": convert_item_to_lol_jsons(starting_set),
                            "type": f"{value} ({skillOrder})",
                        }
                    )
                else:
                    if "9999" in recommended["id"].values:  # No boots
                        recommended.drop(
                            recommended[recommended["id"] == "9999"].index,
                            inplace=True,
                        )
                    if recommended.empty:
                        print("EMPTY")
                        continue
                    recommended = recommended.head(5)  # Maximum 5 items by block

                    recommended["item_name"] = recommended["id"].apply(
                        lambda id: self.items_data[id]["name_en"]
                    )
                    recommended["item_name_es"] = recommended["id"].apply(
                        lambda id: self.items_data[id]["name_es"]
                    )
                    build_json["blocks"].append(
                        {
                            "items": convert_item_to_lol_jsons(list(recommended["id"])),
                            "type": blocks[b],
                        }
                    )
                    recommended.drop(columns=["time"], inplace=True)
                recommended.drop(columns=["index"], inplace=True)
                build_file.write(recommended.to_string())
                print(recommended)
                build_file.write("\n\n")

        return build_json
