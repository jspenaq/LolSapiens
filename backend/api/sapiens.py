import datetime
from pathlib import Path

import pandas as pd
from numpy import average
from sklearn.preprocessing import MinMaxScaler

from backend.api.lol_scraper import (
    convert_item_to_lol_jsons,
    get_champions_data,
    get_current_patch,
    get_items_data,
    get_runes_data,
)
from backend.api.utils import (
    percentage_division,
    request_get,
    setup_folders,
)


class Sapiens:
    def __init__(self):
        print("Initializing Sapiens...")
        setup_folders()

        self.current_patch = get_current_patch()
        self.patch = ".".join(self.current_patch.split(".")[:2])
        self.base_url = "https://axe.lolalytics.com"  # LoLalytics
        self.tierlist = self._get_tierlist()
        if self.tierlist.empty:
            print("Using previous patch...")
            self.current_patch = get_current_patch(1)
            self.patch = ".".join(self.current_patch.split(".")[:2])

        self.champions_data = get_champions_data(self.current_patch)
        self.runes_data = get_runes_data(self.current_patch)
        self.keystones, self.all_runes = self._get_keystones()
        self.items_data = get_items_data(self.current_patch)

        self.current_champion_data = {}
        print("Sapiens is ready.")

    def get_initial_data(self) -> dict:
        """Return the initial data related to champions, runes, items, and patch.

        Returns:
            dict: A dictionary containing champions data, runes data, items data, and current patch.
        """
        return {
            "champions_data": self.champions_data,
            "runes_data": self.runes_data,
            "items_data": self.items_data,
            "patch": self.current_patch,
        }

    def _get_keystones(self) -> tuple:
        """Gets the keystone runes from the runes data and returns a dictionary with their names and IDs, and another dictionary containing all the rune paths
        and slots with their respective rune IDs, names and translations.

        Returns:
            tuple(dict, dict): A tuple of two dictionaries. The first dictionary contains the keystone runes, with their IDs as keys and their names and translations as values.
            The second dictionary contains all the rune paths and slots with their respective rune IDs, names and translations.
        """
        runes = self.runes_data
        keystones = {}
        all_runes = {}
        for i in range(len(runes)):
            rune_path = runes[i]["id"]
            all_runes[rune_path] = {"name": runes[i]["key"], "slots": {}}
            slots = runes[i]["slots"]
            for level in range(len(slots)):
                all_runes[rune_path]["slots"][level] = {}
                runes_by_level = slots[level]["runes"]
                for k in range(len(runes_by_level)):
                    id_rune = str(runes_by_level[k]["id"])
                    name_english = runes_by_level[k]["name"]
                    name_spanish = runes_by_level[k]["name_es"]
                    if level == 0:  # Keystones
                        keystones[id_rune] = {
                            "name": name_english,
                            "name_es": name_spanish,
                        }
                    all_runes[rune_path]["slots"][level][id_rune] = {
                        "name": name_english,
                        "name_es": name_spanish,
                    }

        return keystones, all_runes

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
        print(f"{method=}")
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

        recommended = self._get_weighted_score(df)
        return recommended.reset_index()

    def _get_weighted_score(self, df: pd.DataFrame) -> pd.DataFrame:
        """This method calculates a weighted score for each row in the input pandas DataFrame
        based on win rate and number of games played. If the length of the input DataFrame is 1, the function returns a copy of the input DataFrame.
        If the length of the input DataFrame is greater than 1, the function first normalizes the "games" column using the MinMaxScaler,
        then calculates the weighted score using the specified weights of 0.6 for win rate and 0.4 for number of games played.
        The resulting DataFrame is then sorted in descending order by the weighted score.
        Finally, the "id" column is converted to string type, and the resulting DataFrame is returned.

        Args:
            df (pd.DataFrame): DataFrame containing columns "id", "win_rate", and "games".

        Returns:
            pd.DataFrame: A DataFrame with columns "id", "win_rate", "games", "games_normalized",
            and "weighted_result" containing the original data along with the normalized games column and the calculated weighted result.
            The DataFrame is sorted in descending order by the weighted result.
        """
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
        return recommended

    def _analyze_bans(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Analyze which champions to ban using statistics in the provided data frame.

        Args:
            df (pd.DataFrame): A pandas data frame containing champion statistics.

        Returns:
            pd.DataFrame: Data frame with the top 10 champions to ban.
        """
        value_pick_rate = max(df["pick_rate"].mean(), df["pick_rate"].median())
        value_win_rate = max(df["win_rate"].mean(), df["win_rate"].median())

        df = df[
            (df["pick_rate"] > value_pick_rate)
            & (df["win_rate"] > value_win_rate)
            # & (df["ban_rate"] > p30_ban_rate)
        ]
        df = df.rename(columns={"games_by_lane": "games"})
        df = self._analyze(df, 0)
        # df = df[(df["pick_rate"] > max(mean, median)) & (df["ban_rate"] > p20)]
        # df = df.sort_values(by="win_rate", ascending=False)
        return df.head(10)[["id", "win_rate", "pick_rate"]]

    def _analyze_picks(self, df: pd.DataFrame) -> pd.DataFrame:
        value_pick_rate = max(df["pick_rate"].mean(), df["pick_rate"].median())
        value_win_rate = max(df["win_rate"].mean(), df["win_rate"].median())
        df = df[
            (df["pick_rate"] < value_pick_rate)
            & (df["win_rate"] > value_win_rate)
            # & (df["games_by_lane"] >= 5)
        ]
        df = df.rename(columns={"games_by_lane": "games"})
        df = self._analyze(df, 8)
        # df = df.sort_values(by="win_rate", ascending=False).reset_index()
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
            champion_id = row["id"]
            data.append(
                {
                    "id": int(champion_id),
                    "name": self.champions_data[champion_id]["name"],
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
                    "name": self.champions_data[str(champion_id)]["name"],
                    "win_rate": row["win_rate"],
                    "pick_rate": row["pick_rate"],
                }
            )
        return data

    def generate_build(
        self,
        champion_id: str,
        lane: str = "default",
        tier: str = "platinum_plus",
        queue_mode: int = 420,
        keystone_id: int = 0,
        spicy: int = 0,
    ) -> dict:
        build_response = {
            "keystones": "",
            "runes": "",
            "summoner_spells": "",
            "items": "",
            "skills": "",
        }

        # Get keystones
        if keystone_id == 0:
            keystones = self._get_champion_keystones(
                champion_id, lane, tier, queue_mode, spicy
            )

            build_response["keystones"] = keystones
            keystone_id = int(keystones[0]["id"])

        # Update current_champion_data
        region = "all"
        url = f"{self.base_url}/mega/?ep=champion&p=d&v=1&patch={self.patch}&cid={champion_id}&lane={lane}&tier={tier}&queue={queue_mode}&region={region}&keystone={keystone_id}"
        self.current_champion_data = request_get(url)
        if "runes" not in self.current_champion_data:
            # No data
            self.current_champion_data = {}
            return build_response

        # Get runes
        runes = self._get_champion_runes(
            champion_id, lane, tier, queue_mode, keystone_id, spicy
        )
        build_response["runes"] = runes

        # Get summoner spells

        # Get items
        items = self._get_items(champion_id, lane, tier, queue_mode, keystone_id, spicy)
        build_response["items"] = items

        # Get skills

        self.current_champion_data = {}  # Reset data
        return build_response

    def _get_items(
        self,
        champion_id: str,
        lane: str = "default",
        tier: str = "platinum_plus",
        queue_mode: int = 420,
        keystone_id: int = 0,
        spicy: int = 0,
    ) -> dict:
        champion_name = self.champions_data[champion_id]["name"]

        print(f"Searching {champion_name} {lane}")
        if keystone_id == 0:
            recommend_runes = self._get_champion_keystones(
                champion_id, lane, tier, queue_mode, spicy
            )

            keystone_id = int(recommend_runes[0]["id"])
        region = "all"
        url = f"{self.base_url}/mega/?ep=champion&p=d&v=1&patch={self.patch}&cid={champion_id}&lane={lane}&tier={tier}&queue={queue_mode}&region={region}&keystone={keystone_id}"
        response = request_get(url)
        # TODO: Fix Desktop app bug (double request)
        # if not self.current_champion_data:
        #     return {}

        return self._get_build_json(
            response, champion_id, lane, tier, keystone_id, spicy
        )

    def _get_champion_keystones(
        self,
        champion_id: str,
        lane: str = "default",
        tier: str = "platinum_plus",
        queue_mode: int = 420,
        spicy: int = 0,
    ) -> dict:
        """Get the keystones for a specific champion.

        Args:
            champion_id (str): The ID of the champion for which to retrieve runes.
            lane (str, optional): The lane for which to retrieve runes. Defaults to "default".
            tier (str, optional): The tier for which to retrieve runes. Defaults to "platinum_plus".
            queue_mode (int, optional): The queue mode for which to retrieve runes. Defaults to 420.

        Returns:
            dict: A dictionary containing the runes information, with keys in the format "{win/pick}_{tier}" and
            values as dictionaries containing "primary_path", "secondary_path", and "shards".
            If no runes information is available, an empty dictionary is returned.
        """
        # TODO: Fix Desktop app bug (double request)
        # if not self.current_champion_data:
        #     # region = "all"
        #     url = f"{self.base_url}/mega/?ep=champion&p=d&v=1&patch={self.patch}&cid={champion_id}&lane={lane}&tier={tier}&queue={queue_mode}&region={region}"
        #     response = request_get(url)
        #     if "runes" not in response:
        #         return {}
        region = "all"
        url = f"{self.base_url}/mega/?ep=champion&p=d&v=1&patch={self.patch}&cid={champion_id}&lane={lane}&tier={tier}&queue={queue_mode}&region={region}"
        response = request_get(url)
        if "runes" not in response:
            return {}

        matrix = []
        for key in self.keystones:
            values = response["runes"]["stats"][key][0]
            # values
            # [0]: pick_rate, [1]: win_rate, [2]: games
            matrix.append([key, values[1], values[2]])

        columns = ["id", "win_rate", "games"]
        df = pd.DataFrame(matrix, columns=columns)
        recommend = self._analyze(df, spicy * 2)
        recommend = recommend.head(5).drop(columns=["index"]).reset_index(drop=True)
        recommend = recommend[["id", "win_rate", "games"]]
        name_column = recommend["id"].apply(lambda x: self.keystones[x]["name"])
        recommend.insert(1, "name", name_column)

        return recommend.to_dict(orient="records")

    def _get_champion_runes(
        self,
        champion_id: str,
        lane: str = "default",
        tier: str = "platinum_plus",
        queue_mode: int = 420,
        keystone_id: int = 0,
        spicy: int = 0,
    ) -> dict:
        """Get the runes for a specific champion.

        Args:
            champion_id (str): The ID of the champion for which to retrieve runes.
            lane (str, optional): The lane for which to retrieve runes. Defaults to "default".
            tier (str, optional): The tier for which to retrieve runes. Defaults to "platinum_plus".
            keystone_id (int, optional):
            queue_mode (str, optional): The queue mode for which to retrieve runes. Defaults to "ranked".

        Returns:
            dict: A dictionary containing the runes information, with keys in the format "{win/pick}_{tier}" and
            values as dictionaries containing "primary_path", "secondary_path", and "shards".
            If no runes information is available, an empty dictionary is returned.
        """
        region = "all"
        url = f"{self.base_url}/mega/?ep=champion&p=d&v=1&patch={self.patch}&cid={champion_id}&lane={lane}&tier={tier}&queue={queue_mode}&region={region}&keystone={keystone_id}"
        response = request_get(url)
        if "runes" not in response:
            return {}

        rune_path = (
            keystone_id // 100 * 100 if keystone_id != 9923 else 8100
        )  # Hail of Blades

        columns = ["id", "win_rate", "games"]
        slots = self.all_runes[rune_path]["slots"]

        # Primary path
        primary_path_id = rune_path
        primary_path = pd.DataFrame(columns=columns)
        for i in range(len(slots)):
            matrix = []
            for key in slots[i].keys():
                values = response["runes"]["stats"][key][0]
                # values
                # [0]: pick_rate, [1]: win_rate, [2]: games
                matrix.append([key, values[1], values[2]])
            df = pd.DataFrame(matrix, columns=columns)
            recommend = self._analyze(df, spicy * 2)
            recommend = recommend.head(1).drop(columns=["index"]).reset_index(drop=True)
            recommend = recommend[["id", "win_rate", "games"]]
            primary_path = pd.concat([primary_path, recommend])
            # name_column = recommend["id"].apply(lambda x: self.all_runes[x]["name"])
            # recommend.insert(1, "name", name_column)

        # Secondary path
        secondary_path_id = self.all_runes[rune_path]["name"]
        secondary_path = pd.DataFrame(columns=columns)
        averages = []

        matrix_all_paths = {}  # For later use
        for id in self.all_runes:
            if id != rune_path:
                print(self.all_runes[id]["name"])
                runes_by_path = {"data": [], "weights": []}  # All 9 runes by path.
                matrix_all_paths[id] = {}
                slots = self.all_runes[id]["slots"]
                for i in range(1, len(slots)):
                    matrix_all_paths[id][i] = []
                    for key in slots[i].keys():
                        values = response["runes"]["stats"][key][1]
                        # values
                        # [0]: pick_rate, [1]: win_rate, [2]: games
                        runes_by_path["data"].append(values[1])
                        runes_by_path["weights"].append(values[2])
                        matrix_all_paths[id][i].append([key, values[1], values[2]])
                avg_mean = round(
                    average(runes_by_path["data"], weights=runes_by_path["weights"]), 4
                )
                averages.append([id, avg_mean, sum(runes_by_path["weights"])])
                print("=======")

        best_path = self._analyze(pd.DataFrame(averages, columns=columns), spicy)
        print(best_path)
        best_path = best_path.head(1)["id"]
        secondary_path_id = int(best_path.values[0])
        print(f"{matrix_all_paths[secondary_path_id]}")
        secondary_path = matrix_all_paths[int(best_path.values[0])]

        top_runes_secondary = pd.DataFrame(columns=columns)
        for k in secondary_path:
            df_secondary = self._analyze(
                pd.DataFrame(secondary_path[k], columns=columns), spicy
            )[["id", "win_rate", "games"]].head(1)
            print(df_secondary)
            top_runes_secondary = pd.concat([top_runes_secondary, df_secondary])
        secondary_path = self._get_weighted_score(top_runes_secondary).head(2)
        print(f"{secondary_path}")

        # Shards
        ids_shards = {
            "0": ["5008", "5005", "5007"],
            "1": ["5008f", "5002f", "5003f"],
            "2": ["5001", "5002", "5003"],
        }
        shards = pd.DataFrame(columns=columns)
        for i in range(len(ids_shards)):
            matrix = []
            for key in ids_shards[str(i)]:
                values = response["runes"]["stats"][key][0]
                # values
                # [0]: pick_rate, [1]: win_rate, [2]: games
                matrix.append([key, values[1], values[2]])
            df = pd.DataFrame(matrix, columns=columns)
            recommend = self._analyze(df, spicy * 2)
            recommend = recommend.head(1).drop(columns=["index"]).reset_index(drop=True)
            recommend = recommend[["id", "win_rate", "games"]]
            shards = pd.concat([shards, recommend])

        return {
            "primary_path": self.all_runes[primary_path_id]["name"],
            "secondary_path": self.all_runes[secondary_path_id]["name"],
            "primary_path_runes": primary_path.to_dict(orient="records"),
            "secondary_path_runes": secondary_path.to_dict(orient="records"),
            "shards_runes": shards.to_dict(orient="records"),
        }

    def _get_build_json(
        self,
        response: dict,
        champion_id: str,
        lane: str,
        tier: str,
        keystone_id: int,
        spicy: int,
    ):
        # response = self.current_champion_data
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
        keystone_name = self.keystones[str(keystone_id)]["name"]
        keystone_name_es = self.keystones[str(keystone_id)]["name_es"]
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
                    starting_set = recommended["id"][0].split("_")
                    # starting_set.append([]) # TODO: add wards, lens
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
