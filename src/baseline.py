"""
Module: src.baseline
Mô tả: Định nghĩa mô hình Baseline Lịch sử (Historical Calendar Baseline)
      dự báo lưu lượng giao thông theo giờ trong ngày, thứ trong tuần và ngày lễ.
Tác giả: Nhóm sinh viên thực hiện Project 20 - Lớp 12523W.1
"""

from typing import Dict, Tuple, Any
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, RegressorMixin


class HistoricalCalendarBaseline(BaseEstimator, RegressorMixin):
    """
    Mô hình chuẩn đối chứng (Baseline) theo lịch sử:
    - Học bảng tra cứu giá trị trung bình của traffic_volume theo từng nhóm
      (hour, dayofweek, is_holiday) từ tập Train.
    - Không học bất kỳ thông tin nào từ tập Validation hay Test.
    - Nếu gặp tổ hợp mới chưa từng có trong tập Train, trả về giá trị trung bình toàn cục (global_mean).
    """

    def __init__(self):
        self.lookup_table_: Dict[Tuple[int, int, int], float] = {}
        self.global_mean_: float = 0.0

    def fit(self, X: pd.DataFrame, y: pd.Series):
        """
        Huấn luyện Baseline: gom nhóm và tính giá trị trung bình lưu lượng xe trên tập Train.
        """
        X_df = X.copy()
        # Đảm bảo các cột cần thiết có mặt
        if "hour" not in X_df.columns or "dayofweek" not in X_df.columns:
            if not pd.api.types.is_datetime64_any_dtype(X_df["date_time"]):
                X_df["date_time"] = pd.to_datetime(X_df["date_time"])
            dt = X_df["date_time"].dt
            X_df["hour"] = dt.hour
            X_df["dayofweek"] = dt.dayofweek
            X_df["is_holiday"] = (X_df["holiday"] != "None").astype(int)

        self.global_mean_ = float(y.mean())

        # Gom nhóm và tính trung bình theo (hour, dayofweek, is_holiday)
        df_merged = X_df[["hour", "dayofweek", "is_holiday"]].copy()
        df_merged["target"] = y.values

        grouped = df_merged.groupby(["hour", "dayofweek", "is_holiday"])["target"].mean()
        self.lookup_table_ = grouped.to_dict()

        return self

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Dự báo lưu lượng xe dựa trên bảng tra cứu lịch sử.
        """
        X_df = X.copy()
        if "hour" not in X_df.columns or "dayofweek" not in X_df.columns:
            if not pd.api.types.is_datetime64_any_dtype(X_df["date_time"]):
                X_df["date_time"] = pd.to_datetime(X_df["date_time"])
            dt = X_df["date_time"].dt
            X_df["hour"] = dt.hour
            X_df["dayofweek"] = dt.dayofweek
            X_df["is_holiday"] = (X_df["holiday"] != "None").astype(int)

        preds = []
        for _, row in X_df.iterrows():
            key = (int(row["hour"]), int(row["dayofweek"]), int(row["is_holiday"]))
            pred = self.lookup_table_.get(key, self.global_mean_)
            preds.append(pred)

        return np.array(preds)
