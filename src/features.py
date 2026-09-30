"""
Module: src.features
Mô tả: Trích xuất đặc trưng chuỗi thời gian, mã hóa chu kỳ lượng giác (Cyclical encoding)
      và chuẩn bị các thuộc tính phục vụ mô hình học máy theo chuẩn Scikit-learn.
Tác giả: Nhóm sinh viên thực hiện Project 20 - Lớp 12523W.1
"""

from typing import List
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


# Định nghĩa danh sách các nhóm đặc trưng dùng cho ColumnTransformer
NUMERIC_FEATURES: List[str] = [
    "temp",
    "rain_1h",
    "snow_1h",
    "clouds_all",
    "sin_hour",
    "cos_hour",
    "sin_month",
    "cos_month",
    "hour",
    "dayofweek",
    "month",
]

CATEGORICAL_FEATURES: List[str] = [
    "weather_main",
    "holiday",
]

BINARY_FEATURES: List[str] = [
    "is_weekend",
    "is_rush_hour",
    "is_holiday",
]


class TrafficFeatureEngineer(BaseEstimator, TransformerMixin):
    """
    Bộ biến đổi đặc trưng tùy biến (Custom Transformer) chuẩn Scikit-learn.
    Thực hiện trích xuất và biến đổi toàn bộ đặc trưng thời gian và thời tiết:
    1. Trích xuất giờ, thứ trong tuần, tháng, năm từ date_time.
    2. Xác định cờ nhị phân: is_weekend (cuối tuần), is_rush_hour (giờ cao điểm trong tuần).
    3. Mã hóa chu kỳ lượng giác sin/cos cho giờ (chu kỳ 24) và tháng (chu kỳ 12).
    4. Tạo cờ nhị phân is_holiday cho ngày lễ.
    5. Đảm bảo tính độc lập: fit() không học thống kê tập ngoài, transform() hoạt động nhất quán.
    """

    def __init__(self, drop_datetime: bool = True):
        self.drop_datetime = drop_datetime

    def fit(self, X: pd.DataFrame, y=None):
        """Hàm fit không cần học tham số thống kê, chỉ trả về self."""
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Thực hiện biến đổi trên một bản sao của DataFrame đầu vào,
        đảm bảo không làm thay đổi trực tiếp dữ liệu gốc (no side-effects).
        """
        X_out = X.copy()

        # Đảm bảo date_time ở định dạng datetime
        if not pd.api.types.is_datetime64_any_dtype(X_out["date_time"]):
            X_out["date_time"] = pd.to_datetime(X_out["date_time"])

        dt = X_out["date_time"].dt

        # 1. Trích xuất các thành phần thời gian cơ sở
        X_out["hour"] = dt.hour
        X_out["dayofweek"] = dt.dayofweek  # 0: Thứ 2, ..., 6: Chủ Nhật
        X_out["month"] = dt.month
        X_out["year"] = dt.year

        # 2. Tạo cờ nhị phân ngữ cảnh giao thông
        # Cuối tuần: Thứ Bảy (5) hoặc Chủ Nhật (6)
        X_out["is_weekend"] = X_out["dayofweek"].isin([5, 6]).astype(int)

        # Giờ cao điểm các ngày làm việc trong tuần (Thứ 2 - Thứ 6)
        # Sáng: 7h - 9h | Chiều: 16h - 18h
        is_weekday = X_out["dayofweek"] < 5
        is_morning_rush = X_out["hour"].isin([7, 8, 9])
        is_evening_rush = X_out["hour"].isin([16, 17, 18])
        X_out["is_rush_hour"] = (is_weekday & (is_morning_rush | is_evening_rush)).astype(int)

        # 3. Mã hóa chu kỳ lượng giác (Cyclical Encoding)
        # Giúp mô hình hiểu được tính liên tục: giờ 23 và giờ 0 nằm sát cạnh nhau
        X_out["sin_hour"] = np.sin(2 * np.pi * X_out["hour"] / 24.0)
        X_out["cos_hour"] = np.cos(2 * np.pi * X_out["hour"] / 24.0)

        # Chu kỳ 12 tháng: tháng 12 và tháng 1 nằm sát cạnh nhau
        X_out["sin_month"] = np.sin(2 * np.pi * (X_out["month"] - 1) / 12.0)
        X_out["cos_month"] = np.cos(2 * np.pi * (X_out["month"] - 1) / 12.0)

        # 4. Tạo cờ ngày lễ
        X_out["is_holiday"] = (X_out["holiday"] != "None").astype(int)

        # 5. Loại bỏ cột date_time nếu yêu cầu
        if self.drop_datetime and "date_time" in X_out.columns:
            X_out = X_out.drop(columns=["date_time"])

        return X_out
