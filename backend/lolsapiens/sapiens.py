from abc import abstractmethod
import pandas as pd


class Sapiens:
    def __init__(self, config: str = ""):
        self.config = config

    @abstractmethod
    def analyze(self, df: pd.DataFrame) -> pd.DataFrame:
        # percentile = df["games"].quantile(0.60)
        # recommended = df[df["games"] >= percentile]
        # recommended_sorted = recommended.sort_values(by="win_rate", ascending=False)
        # recommended_sorted["item_id"] = recommended_sorted["item_id"].astype(str)
        # return recommended_sorted.reset_index()

        standard = df["games"].std(ddof=0)  # Normalize by N instead of N-1
        mean = df["games"].mean()
        cv = standard / mean
        q1 = df["games"].quantile(0.25)
        q2 = df["games"].quantile(0.50)
        q3 = df["games"].quantile(0.75)
        max = df["games"].max()
        iqr = q3 - q1
        # outliers = df[
        #     ((df["games"] < (q1 - 1.5 * iqr)) | (df["games"] > (q3 + 1.5 * iqr)))
        # ]
        upper_outliers = df[(df["games"] > (q3 + 1.5 * iqr))]
        upper_outliers = len(upper_outliers) > 0

        method = 0
        if cv > 1.5:
            method = 1
        elif 1.5 > cv and cv > 1.0:
            method = 2
        elif 1.0 > cv and cv > 0.5:
            method = 3
        elif cv < 0.5:
            method = 4

        if upper_outliers:
            method -= 1

        match method:
            case 0 | 1:
                recommended = df[df["games"] >= (max - 1 * standard)]
            case 2:
                recommended = df[df["games"] >= q3]
            case 3:
                recommended = df[df["games"] >= q2]
            case 4:
                recommended = df[df["games"] >= q1]
        
        recommended_sorted = recommended.sort_values(by="win_rate", ascending=False)
        recommended_sorted["item_id"] = recommended_sorted["item_id"].astype(str)
        return recommended_sorted.reset_index()
