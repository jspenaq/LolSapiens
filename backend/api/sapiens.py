from abc import abstractmethod
import pandas as pd
from pathlib import Path
from backend.api.lol_scraper import (
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
    def analyze(self, df: pd.DataFrame) -> pd.DataFrame:
        standard = df["games"].std(ddof=0)  # Normalize by N instead of N-1
        mean = df["games"].mean()
        cv = standard / mean
        q1 = df["games"].quantile(0.25)
        q2 = df["games"].quantile(0.50)
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
            method = 1
        elif 1.5 > cv > 1.0:
            method = 2
        elif 1.0 > cv > 0.5:
            method = 3
        elif cv < 0.5:
            method = 4

        if upper_outliers:
            method -= 1

        match method:
            case 0 | 1:
                recommended = df[df["games"] >= (maximum - 1 * standard)]
            case 2:
                recommended = df[df["games"] >= q3]
            case 3:
                recommended = df[df["games"] >= q2]
            case 4:
                recommended = df[df["games"] >= q1]

        recommended_sorted = recommended.sort_values(by="win_rate", ascending=False)
        recommended_sorted["item_id"] = recommended_sorted["item_id"].astype(str)
        return recommended_sorted.reset_index()

    def generate_build(
        self, champion_id: str, lane: str, tier: str, mode: str, keystone_id: str
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
        return response

    def _get_build_json(
        response,
        champion_id,
        champion_name,
        lane,
        runes_data,
        items_data,
        keystone_id,
        blocks,
    ):
        pass
