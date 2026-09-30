"""
Module: src.evaluate
Mô tả: Thực thi 4 Thí nghiệm bắt buộc theo Đề tài Project 20 (PGS.TS. Nguyễn Văn Hậu),
      xuất biểu đồ trực quan khoa học (300 DPI) và lưu trữ số liệu vào models/experiment_metrics.json.
Tác giả: Nhóm sinh viên thực hiện Project 20 - Lớp 12523W.1
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any, List
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cấu hình in tiếng Việt trên console Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Đảm bảo thư mục gốc của project luôn nằm trong sys.path để chạy được 'python src/evaluate.py'
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Cấu hình phong cách biểu đồ khoa học
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Calibri"]
plt.rcParams["axes.unicode_minus"] = False
sns.set_theme(style="whitegrid", font_scale=1.1)

from src.data import (
    load_and_clean_traffic_data,
    split_traffic_data,
    create_random_split_for_exp1,
)
from src.features import TrafficFeatureEngineer
from src.baseline import HistoricalCalendarBaseline
from src.train import (
    build_full_pipeline,
    compute_metrics,
)
from sklearn.linear_model import Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor


def run_all_experiments(data_path: str | Path, models_dir: str | Path, figures_dir: str | Path):
    """
    Thực hiện lần lượt 4 thí nghiệm bắt buộc và lưu toàn bộ kết quả.
    """
    models_path = Path(models_dir)
    figures_path = Path(figures_dir)
    models_path.mkdir(parents=True, exist_ok=True)
    figures_path.mkdir(parents=True, exist_ok=True)

    print("=" * 75)
    print("BẮT ĐẦU CHẠY 4 THÍ NGHIỆM THỰC NGHIỆM BẮT BUỘC (PROJECT 20 - BÀI 07)")
    print("=" * 75)

    # 1. Nạp dữ liệu
    df = load_and_clean_traffic_data(data_path)
    X_train, y_train, X_val, y_val, X_test, y_test = split_traffic_data(df)

    # Nạp mô hình đã train từ trước hoặc tạo mới
    best_pipeline_path = models_path / "best_traffic_pipeline.pkl"
    baseline_path = models_path / "calendar_baseline.pkl"

    if best_pipeline_path.exists():
        best_pipeline = joblib.load(best_pipeline_path)
    else:
        best_pipeline = build_full_pipeline(RandomForestRegressor(n_estimators=100, max_depth=15, n_jobs=-1, random_state=42))
        best_pipeline.fit(X_train, y_train)

    if baseline_path.exists():
        baseline = joblib.load(baseline_path)
    else:
        baseline = HistoricalCalendarBaseline()
        baseline.fit(X_train, y_train)

    experiment_metrics: Dict[str, Any] = {}

    # =========================================================================
    # THÍ NGHIỆM 1: RANDOM SPLIT VS TIME-BASED SPLIT (VẠCH TRẦN RÒ RỈ DỮ LIỆU)
    # =========================================================================
    print("\n" + "=" * 70)
    print("THÍ NGHIỆM 1: RANDOM SPLIT VS. TIME-BASED SPLIT")
    print("=" * 70)

    # Huấn luyện Random Forest trên Random Split
    X_tr_rnd, y_tr_rnd, X_te_rnd, y_te_rnd = create_random_split_for_exp1(df, test_size=0.15, random_state=42)
    rf_random_split = build_full_pipeline(RandomForestRegressor(n_estimators=50, max_depth=15, n_jobs=-1, random_state=42))
    rf_random_split.fit(X_tr_rnd, y_tr_rnd)
    y_pred_rnd = rf_random_split.predict(X_te_rnd)
    metrics_random_split = compute_metrics(y_te_rnd, y_pred_rnd)

    # Đánh giá Random Forest trên Time-based Split Test (Mô hình huấn luyện trên Train 70%, test trên 15% tương lai)
    y_pred_time = best_pipeline.predict(X_test)
    metrics_time_split = compute_metrics(y_test, y_pred_time)

    print(f"-> Random Split Test Metrics (BỊ RÒ RỈ NGỮ CẢNH): {metrics_random_split}")
    print(f"-> Time-based Split Test Metrics (CHUẨN MỰC TƯƠNG LAI): {metrics_time_split}")

    experiment_metrics["Experiment_1_Data_Split"] = {
        "Random_Split": metrics_random_split,
        "Time_based_Split": metrics_time_split,
        "Conclusion": "Random Split đạt R2 cao ảo do các giờ liền kề bị rò rỉ qua lại giữa train và test. Time-based Split phản ánh đúng năng lực triển khai thực tế trên dữ liệu tương lai.",
    }

    # Vẽ biểu đồ Thí nghiệm 1
    fig, axes = plt.subplots(1, 2, figsize=(14, 5), dpi=300)
    splits = ["Random Split\n(Rò rỉ tự tương quan)", "Time-based Split\n(Chuẩn mực Bài 07)"]
    mae_vals = [metrics_random_split["MAE"], metrics_time_split["MAE"]]
    r2_vals = [metrics_random_split["R2"], metrics_time_split["R2"]]

    bars1 = axes[0].bar(splits, mae_vals, color=["#e74c3c", "#2ecc71"], width=0.45)
    axes[0].set_title("So sánh Sai số Tuyệt đối Trung bình (MAE)", fontsize=13, fontweight="bold", pad=10)
    axes[0].set_ylabel("MAE (xe/giờ)", fontsize=11)
    for bar in bars1:
        yval = bar.get_height()
        axes[0].text(bar.get_x() + bar.get_width() / 2.0, yval + 5, f"{yval:.1f} xe/h", ha="center", va="bottom", fontweight="bold")

    bars2 = axes[1].bar(splits, r2_vals, color=["#e74c3c", "#2ecc71"], width=0.45)
    axes[1].set_title("So sánh Hệ số Xác định (R² Score)", fontsize=13, fontweight="bold", pad=10)
    axes[1].set_ylabel("R² Score", fontsize=11)
    axes[1].set_ylim(0, 1.05)
    for bar in bars2:
        yval = bar.get_height()
        axes[1].text(bar.get_x() + bar.get_width() / 2.0, yval + 0.02, f"{yval:.4f}", ha="center", va="bottom", fontweight="bold")

    plt.suptitle("THÍ NGHIỆM 1: ĐỐI CHỨNG RANDOM SPLIT VS TIME SPLIT TRÊN CAO TỐC I-94", fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    fig1_path = figures_path / "exp1_random_vs_time_split.png"
    plt.savefig(fig1_path, bbox_inches="tight")
    plt.close()
    print(f"-> Đã xuất biểu đồ Thí nghiệm 1 vào: {fig1_path}")

    # =========================================================================
    # THÍ NGHIỆM 2: SO SÁNH BASELINE LỊCH VS CÁC MÔ HÌNH HỌC MÁY
    # =========================================================================
    print("\n" + "=" * 70)
    print("THÍ NGHIỆM 2: BENCHMARK BASELINE LỊCH VS CÁC MÔ HÌNH HỌC MÁY")
    print("=" * 70)

    # Huấn luyện các mô hình để so sánh trực tiếp
    pipe_ridge = build_full_pipeline(Ridge(alpha=1.0, random_state=42)).fit(X_train, y_train)
    pipe_lasso = build_full_pipeline(Lasso(alpha=1.0, max_iter=2000, random_state=42)).fit(X_train, y_train)
    pipe_rf = build_full_pipeline(RandomForestRegressor(n_estimators=100, max_depth=15, n_jobs=-1, random_state=42)).fit(X_train, y_train)
    pipe_xgb = build_full_pipeline(XGBRegressor(n_estimators=150, max_depth=6, learning_rate=0.08, n_jobs=-1, random_state=42)).fit(X_train, y_train)

    models_eval = {
        "Calendar Baseline": baseline,
        "Ridge Regression (L2)": pipe_ridge,
        "Lasso Regression (L1)": pipe_lasso,
        "Random Forest": pipe_rf,
        "XGBoost": pipe_xgb,
    }

    test_benchmark = {}
    for name, m in models_eval.items():
        preds = m.predict(X_test)
        metrics = compute_metrics(y_test, preds)
        test_benchmark[name] = metrics
        print(f"-> [{name}] Test Set: {metrics}")

    experiment_metrics["Experiment_2_Model_Benchmark"] = test_benchmark

    # Vẽ biểu đồ Thí nghiệm 2
    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    model_names = list(test_benchmark.keys())
    maes = [test_benchmark[m]["MAE"] for m in model_names]
    rmses = [test_benchmark[m]["RMSE"] for m in model_names]

    x = np.arange(len(model_names))
    width = 0.35

    rects1 = ax.bar(x - width / 2, maes, width, label="MAE (Sai số tuyệt đối)", color="#3498db")
    rects2 = ax.bar(x + width / 2, rmses, width, label="RMSE (Căn bậc hai bình phương)", color="#e67e22")

    ax.set_title("THÍ NGHIỆM 2: ĐỐI CHỨNG BASELINE VÀ CÁC MÔ HÌNH TRÊN TẬP TEST ĐỘC LẬP", fontsize=13, fontweight="bold", pad=15)
    ax.set_ylabel("Sai số (xe/giờ)", fontsize=11)
    ax.set_xticks(x)
    ax.set_xticklabels(model_names, fontsize=10, fontweight="bold")
    ax.legend(frameon=True)

    for bar in rects1:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 10, f"{bar.get_height():.0f}", ha="center", va="bottom", fontsize=9)
    for bar in rects2:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 10, f"{bar.get_height():.0f}", ha="center", va="bottom", fontsize=9)

    plt.tight_layout()
    fig2_path = figures_path / "exp2_models_comparison.png"
    plt.savefig(fig2_path, bbox_inches="tight")
    plt.close()
    print(f"-> Đã xuất biểu đồ Thí nghiệm 2 vào: {fig2_path}")

    # =========================================================================
    # THÍ NGHIỆM 3: ĐÁNH GIÁ TRÔI DẠT DỮ LIỆU (TEMPORAL & SEASONAL DRIFT)
    # =========================================================================
    print("\n" + "=" * 70)
    print("THÍ NGHIỆM 3: ĐÁNH GIÁ TRÔI DẠT DỮ LIỆU (DATA DRIFT THEO NĂM VÀ MÙA)")
    print("=" * 70)

    # Dự đoán trên toàn bộ tập dữ liệu đã làm sạch để theo dõi độ ổn định
    all_preds = best_pipeline.predict(df.drop(columns=["traffic_volume"]))
    df_analysis = df.copy()
    df_analysis["pred"] = all_preds
    df_analysis["error"] = np.abs(df_analysis["traffic_volume"] - df_analysis["pred"])
    df_analysis["year"] = df_analysis["date_time"].dt.year
    df_analysis["month"] = df_analysis["date_time"].dt.month

    # Phân nhóm mùa (Season) tại Minnesota
    def get_season(m):
        if m in [12, 1, 2]:
            return "Winter (Mùa đông)"
        elif m in [3, 4, 5]:
            return "Spring (Mùa xuân)"
        elif m in [6, 7, 8]:
            return "Summer (Mùa hè)"
        else:
            return "Autumn (Mùa thu)"

    df_analysis["season"] = df_analysis["month"].apply(get_season)

    year_mae = df_analysis.groupby("year")["error"].mean().round(2).to_dict()
    season_mae = df_analysis.groupby("season")["error"].mean().round(2).to_dict()

    print(f"-> Sai số MAE theo từng năm: {year_mae}")
    print(f"-> Sai số MAE theo từng mùa: {season_mae}")

    experiment_metrics["Experiment_3_Data_Drift"] = {
        "MAE_by_Year": year_mae,
        "MAE_by_Season": season_mae,
    }

    # Vẽ biểu đồ Thí nghiệm 3
    fig, axes = plt.subplots(1, 2, figsize=(14, 5), dpi=300)
    years = list(year_mae.keys())
    y_vals = [year_mae[yr] for yr in years]
    axes[0].plot(years, y_vals, marker="o", linewidth=2.5, color="#8e44ad", markersize=8)
    axes[0].set_title("Biến thiên Sai số MAE theo Năm (2012 - 2018)", fontsize=12, fontweight="bold")
    axes[0].set_xlabel("Năm quan sát", fontsize=11)
    axes[0].set_ylabel("MAE (xe/giờ)", fontsize=11)
    for i, v in enumerate(y_vals):
        axes[0].text(years[i], v + 3, f"{v:.1f}", ha="center", va="bottom", fontweight="bold")

    seasons = list(season_mae.keys())
    s_vals = [season_mae[sn] for sn in seasons]
    bars_s = axes[1].bar(seasons, s_vals, color=["#1abc9c", "#f39c12", "#e74c3c", "#34495e"], width=0.5)
    axes[1].set_title("Biến thiên Sai số MAE theo Mùa", fontsize=12, fontweight="bold")
    axes[1].set_ylabel("MAE (xe/giờ)", fontsize=11)
    for bar in bars_s:
        axes[1].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 3, f"{bar.get_height():.1f}", ha="center", va="bottom", fontweight="bold")

    plt.suptitle("THÍ NGHIỆM 3: PHÂN TÍCH HIỆN TƯỢNG DATA DRIFT THEO THỜI GIAN VÀ KHÍ HẬU", fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    fig3_path = figures_path / "exp3_seasonal_drift.png"
    plt.savefig(fig3_path, bbox_inches="tight")
    plt.close()
    print(f"-> Đã xuất biểu đồ Thí nghiệm 3 vào: {fig3_path}")

    # =========================================================================
    # THÍ NGHIỆM 4: PHÂN TÍCH LỖI (ERROR ANALYSIS) THEO DỊP LỄ VÀ THỜI TIẾT
    # =========================================================================
    print("\n" + "=" * 70)
    print("THÍ NGHIỆM 4: PHÂN TÍCH LỖI NGOẠI LỆ (NGÀY LỄ VÀ THỜI TIẾT CỰC ĐOAN)")
    print("=" * 70)

    # Đánh giá thặng dư trên tập Test
    test_eval_df = X_test.copy()
    test_eval_df["y_true"] = y_test.values
    test_eval_df["y_pred"] = y_pred_time
    test_eval_df["residual"] = test_eval_df["y_true"] - test_eval_df["y_pred"]
    test_eval_df["abs_error"] = np.abs(test_eval_df["residual"])

    # Phân nhóm ngày lễ vs ngày thường
    holiday_mask = test_eval_df["holiday"] != "None"
    holiday_mae = float(test_eval_df[holiday_mask]["abs_error"].mean()) if holiday_mask.sum() > 0 else 0.0
    regular_mae = float(test_eval_df[~holiday_mask]["abs_error"].mean())

    # Phân nhóm thời tiết xấu (Tuyết rơi hoặc Mưa to > 5mm) vs Thời tiết bình thường
    bad_weather_mask = (test_eval_df["snow_1h"] > 0) | (test_eval_df["rain_1h"] > 5.0)
    bad_weather_mae = float(test_eval_df[bad_weather_mask]["abs_error"].mean()) if bad_weather_mask.sum() > 0 else 0.0
    clear_weather_mask = test_eval_df["weather_main"] == "Clear"
    clear_weather_mae = float(test_eval_df[clear_weather_mask]["abs_error"].mean())

    print(f"-> MAE Ngày thường: {regular_mae:.2f} xe/h | MAE Ngày lễ: {holiday_mae:.2f} xe/h")
    print(f"-> MAE Trời quang (Clear): {clear_weather_mae:.2f} xe/h | MAE Thời tiết cực đoan (Bão/Tuyết): {bad_weather_mae:.2f} xe/h")

    experiment_metrics["Experiment_4_Error_Analysis"] = {
        "Holiday_MAE": round(holiday_mae, 2),
        "Regular_Day_MAE": round(regular_mae, 2),
        "Extreme_Weather_MAE": round(bad_weather_mae, 2),
        "Clear_Weather_MAE": round(clear_weather_mae, 2),
    }

    # Vẽ biểu đồ Thí nghiệm 4
    fig, axes = plt.subplots(1, 2, figsize=(14, 5), dpi=300)

    # Biểu đồ phân bố phần dư (Residual distribution)
    sns.histplot(test_eval_df["residual"], kde=True, ax=axes[0], color="#2980b9", bins=50)
    axes[0].set_title("Phân bố Phần dư Sai số trên Tập Test (y_true - y_pred)", fontsize=12, fontweight="bold")
    axes[0].set_xlabel("Thặng dư (xe/giờ)", fontsize=11)
    axes[0].set_ylabel("Số lượng mẫu", fontsize=11)
    axes[0].axvline(0, color="red", linestyle="--", linewidth=1.5, label="Trung tâm sai số = 0")
    axes[0].legend()

    # So sánh MAE các tình huống biên
    categories = ["Ngày thường", "Ngày Lễ", "Trời quang", "Bão / Tuyết"]
    cat_maes = [regular_mae, holiday_mae, clear_weather_mae, bad_weather_mae]
    cat_colors = ["#2ecc71", "#e74c3c", "#3498db", "#9b59b6"]
    bars_c = axes[1].bar(categories, cat_maes, color=cat_colors, width=0.5)
    axes[1].set_title("So sánh Sai số MAE trong các Tình huống Đặc biệt", fontsize=12, fontweight="bold")
    axes[1].set_ylabel("MAE (xe/giờ)", fontsize=11)
    for bar in bars_c:
        axes[1].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5, f"{bar.get_height():.1f}", ha="center", va="bottom", fontweight="bold")

    plt.suptitle("THÍ NGHIỆM 4: BÓC TÁCH PHẦN DƯ VÀ PHÂN TÍCH SAI SỐ NGOẠI LỆ TRÊN TẬP TEST", fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    fig4_path = figures_path / "exp4_holiday_and_weather_errors.png"
    plt.savefig(fig4_path, bbox_inches="tight")
    plt.close()
    print(f"-> Đã xuất biểu đồ Thí nghiệm 4 vào: {fig4_path}")

    # Lưu toàn bộ metrics vào models/experiment_metrics.json
    metrics_file = models_path / "experiment_metrics.json"
    with open(metrics_file, "w", encoding="utf-8") as f:
        json.dump(experiment_metrics, f, ensure_ascii=False, indent=2)
    print(f"\n-> [THÀNH CÔNG] Đã lưu kết quả 4 thí nghiệm vào: {metrics_file}")
    print("=" * 75)


if __name__ == "__main__":
    current_dir = Path(__file__).resolve().parent.parent
    data_file = current_dir / "data" / "Metro_Interstate_Traffic_Volume.csv"
    models_dir = current_dir / "models"
    figures_dir = current_dir / "reports" / "figures"
    run_all_experiments(data_file, models_dir, figures_dir)
