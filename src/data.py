"""
Module: src.data
Mô tả: Nạp dữ liệu, làm sạch các lỗi cảm biến/ngoại lai và chia tập dữ liệu
      chuỗi thời gian theo đúng nguyên tắc phương pháp luận Bài 07 (PGS.TS. Nguyễn Văn Hậu).
Tác giả: Nhóm sinh viên thực hiện Project 20 - Lớp 12523W.1
"""

import sys
from pathlib import Path
from typing import Tuple, Dict, Any
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

# Đảm bảo in tiếng Việt không bị lỗi encoding trên Windows console
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass



def load_and_clean_traffic_data(filepath: str | Path) -> pd.DataFrame:
    """
    Đọc tệp dữ liệu giao thông Metro Interstate và thực hiện các bước làm sạch chuẩn mực:
    1. Điền giá trị khuyết thiếu cột holiday (NaN -> 'None').
    2. Lọc bỏ lỗi cảm biến nhiệt độ 0 Kelvin (-273.15°C).
    3. Cắt gọt ngoại lệ lượng mưa cực đoan (9831.3 mm về 100.0 mm).
    4. Xử lý trùng lặp mốc thời gian date_time (giữ bản ghi đầu tiên).
    5. Sắp xếp thứ tự thời gian tăng dần và thiết lập lại chỉ mục.

    Tham số:
        filepath (str | Path): Đường dẫn tới tệp CSV dữ liệu.

    Trả về:
        pd.DataFrame: Bảng dữ liệu sạch đã được sắp xếp theo thời gian.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Không tìm thấy tệp dữ liệu tại đường dẫn: {path}")

    # Đọc dữ liệu, giữ nguyên chuỗi 'None' ở cột holiday không để pandas tự ép thành NaN
    df = pd.read_csv(path, keep_default_na=False)

    initial_rows = len(df)
    print(f"[DATA] Số lượng bản ghi ban đầu: {initial_rows:,} dòng.")

    # 1. Xử lý cột holiday: Các dòng rỗng hoặc NaN được gán thành 'None'
    df["holiday"] = df["holiday"].replace({"": "None", np.nan: "None"})
    num_holidays = (df["holiday"] != "None").sum()
    print(f"[DATA] Cột 'holiday': Đã chuẩn hóa {num_holidays} bản ghi ngày lễ thực tế, còn lại là 'None'.")

    # 2. Xử lý lỗi cảm biến nhiệt độ 0 Kelvin (-273.15°C, điều kiện phi vật lý tại Minnesota)
    zero_temp_count = (df["temp"] <= 0.0).sum()
    if zero_temp_count > 0:
        df = df[df["temp"] > 0.0].copy()
        print(f"[DATA] Cột 'temp': Đã loại bỏ {zero_temp_count} bản ghi có nhiệt độ phi vật lý (0.0 Kelvin).")

    # 3. Xử lý ngoại lệ lượng mưa cực đoan (bản ghi 9831.3 mm ngày 11/07/2016 do tràn cảm biến)
    rain_outliers = (df["rain_1h"] > 100.0).sum()
    if rain_outliers > 0:
        df["rain_1h"] = df["rain_1h"].clip(upper=100.0)
        print(f"[DATA] Cột 'rain_1h': Đã cắt gọt (clip) {rain_outliers} bản ghi vượt ngưỡng 100mm về đúng 100.0mm.")

    # 4. Xử lý trùng lặp mốc thời gian date_time (giữ quan sát đầu tiên của mỗi giờ)
    dup_count = df.duplicated(subset=["date_time"]).sum()
    if dup_count > 0:
        df = df.drop_duplicates(subset=["date_time"], keep="first").copy()
        print(f"[DATA] Cột 'date_time': Đã loại bỏ {dup_count:,} mốc giờ bị lặp do đa trạng thái thời tiết.")

    # 5. Chuyển đổi sang datetime và sắp xếp tăng dần tuyệt đối theo trục thời gian
    df["date_time"] = pd.to_datetime(df["date_time"])
    df = df.sort_values(by="date_time").reset_index(drop=True)

    final_rows = len(df)
    min_date = df["date_time"].min()
    max_date = df["date_time"].max()
    print(f"[DATA] Dữ liệu sau khi làm sạch: {final_rows:,} dòng (từ {min_date} đến {max_date}).\n")

    return df


def split_traffic_data(
    df: pd.DataFrame,
    target_col: str = "traffic_volume",
    train_ratio: float = 0.70,
    val_ratio: float = 0.15,
    test_ratio: float = 0.15,
) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
    """
    Phân chia tập dữ liệu theo thứ tự thời gian TUYỆT ĐỐI (Time-based Split):
    - Train: 70% đầu tiên (Quá khứ)
    - Validation: 15% tiếp theo (Hiện tại gần) - Dùng chọn siêu tham số & mô hình
    - Test: 15% cuối cùng (Tương lai) - ĐÓNG BĂNG, chỉ đánh giá 1 lần duy nhất

    Tuyệt đối không xáo trộn ngẫu nhiên để chống rò rỉ dữ liệu tự tương quan (Bài 07).
    """
    assert np.isclose(train_ratio + val_ratio + test_ratio, 1.0), "Tổng các tỷ lệ chia phải bằng 1.0"

    n = len(df)
    train_end = int(n * train_ratio)
    val_end = int(n * (train_ratio + val_ratio))

    train_df = df.iloc[:train_end].copy()
    val_df = df.iloc[train_end:val_end].copy()
    test_df = df.iloc[val_end:].copy()

    X_train = train_df.drop(columns=[target_col])
    y_train = train_df[target_col]

    X_val = val_df.drop(columns=[target_col])
    y_val = val_df[target_col]

    X_test = test_df.drop(columns=[target_col])
    y_test = test_df[target_col]

    print("=" * 70)
    print("PHÂN CHIA DỮ LIỆU CHUỖI THỜI GIAN (TIME-BASED SPLIT - BÀI 07)")
    print("=" * 70)
    print(f"1. Tập TRAIN ({train_ratio*100:.0f}%): {len(train_df):,} mẫu | Từ {X_train['date_time'].min()} đến {X_train['date_time'].max()}")
    print(f"2. Tập VALIDATION ({val_ratio*100:.0f}%): {len(val_df):,} mẫu | Từ {X_val['date_time'].min()} đến {X_val['date_time'].max()}")
    print(f"3. Tập TEST ĐÓNG BĂNG ({test_ratio*100:.0f}%): {len(test_df):,} mẫu | Từ {X_test['date_time'].min()} đến {X_test['date_time'].max()}")
    print("=" * 70)

    # Kiểm tra tính toàn vẹn thời gian: train_max < val_min < test_min
    assert X_train["date_time"].max() < X_val["date_time"].min(), "Lỗi rò rỉ: Train chồng lấn Validation!"
    assert X_val["date_time"].max() < X_test["date_time"].min(), "Lỗi rò rỉ: Validation chồng lấn Test!"

    return X_train, y_train, X_val, y_val, X_test, y_test


def create_random_split_for_exp1(
    df: pd.DataFrame,
    target_col: str = "traffic_volume",
    test_size: float = 0.15,
    random_state: int = 42,
) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
    """
    Tạo phân chia xáo trộn ngẫu nhiên (Random Shuffle Split) với mục đích đối chứng:
    Phục vụ riêng cho THÍ NGHIỆM 1 nhằm vạch trần sai lầm rò rỉ ngữ cảnh tự tương quan
    (Look-ahead bias) khi người làm học máy áp dụng bừa bãi chia ngẫu nhiên vào chuỗi thời gian.
    """
    X = df.drop(columns=[target_col])
    y = df[target_col]

    X_train_rnd, X_test_rnd, y_train_rnd, y_test_rnd = train_test_split(
        X, y, test_size=test_size, random_state=random_state, shuffle=True
    )

    print(f"[EXP 1] Đã tạo Random Shuffle Split: Train={len(X_train_rnd):,} mẫu, Test={len(X_test_rnd):,} mẫu.")
    return X_train_rnd, y_train_rnd, X_test_rnd, y_test_rnd
