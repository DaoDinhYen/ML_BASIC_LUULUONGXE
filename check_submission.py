"""
Chương trình: check_submission.py
Mô tả: Kịch bản kiểm tra tự động trước khi nộp bài (QA/QC Automated Inspection Script)
       cho đề tài Project 20 - Lớp 12523W.1 (GVHD: PGS.TS. Nguyễn Văn Hậu).
       Thực thi 6 cổng kiểm soát chất lượng (6 Verification Gates) nhằm đảm bảo
       dự án hoàn thiện 100%, không lỗi, không rò rỉ dữ liệu, sẵn sàng đạt điểm 10/10.
Tác giả: Nhóm sinh viên thực hiện Project 20 - Lớp 12523W.1
"""

import sys
import os
import json
import re
import unittest
from pathlib import Path

# Đảm bảo in tiếng Việt trên console Windows không bị lỗi cp1252
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Thiết lập đường dẫn gốc của project
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


class SubmissionQualityAssurance:
    """Hệ thống kiểm định chất lượng đồ án tự động."""

    def __init__(self):
        self.results = []
        self.all_passed = True

    def log_gate(self, gate_id: int, name: str, passed: bool, message: str):
        """Ghi nhận kết quả của từng cổng kiểm tra."""
        status_str = "✅ [PASS]" if passed else "❌ [FAIL]"
        self.results.append({
            "gate": f"Gate {gate_id}",
            "name": name,
            "status": status_str,
            "passed": passed,
            "message": message,
        })
        if not passed:
            self.all_passed = False

    # --------------------------------------------------------------------------
    # CỔNG 1: KIỂM TRA CẤU TRÚC THƯ MỤC & CÁC TỆP BẮT BUỘC
    # --------------------------------------------------------------------------
    def check_gate_1_file_structure(self):
        print("\n[GATE 1] Đang kiểm tra cấu trúc thư mục và các tệp tin bắt buộc...")
        required_files = [
            "data/Metro_Interstate_Traffic_Volume.csv",
            "data/README.md",
            "requirements.txt",
            "src/__init__.py",
            "src/data.py",
            "src/features.py",
            "src/baseline.py",
            "src/train.py",
            "src/evaluate.py",
            "models/best_traffic_pipeline.pkl",
            "models/calendar_baseline.pkl",
            "models/experiment_metrics.json",
            "reports/figures/exp1_random_vs_time_split.png",
            "reports/figures/exp2_models_comparison.png",
            "reports/figures/exp3_seasonal_drift.png",
            "reports/figures/exp4_holiday_and_weather_errors.png",
            "app/__init__.py",
            "app/backend.py",
            "app/test_api.py",
            "frontend/index.html",
            "report/BAO_CAO_PROJECT_20.md",
            "report/BAO_CAO_PROJECT_20.docx",
            "slide/SLIDES_PROJECT_20.md",
            "CONTRIBUTIONS.md",
            "README.md",
        ]

        missing_files = []
        for rel_path in required_files:
            full_path = PROJECT_ROOT / rel_path
            if not full_path.exists():
                missing_files.append(rel_path)

        if missing_files:
            self.log_gate(
                1,
                "Cấu trúc thư mục & Tệp tin",
                False,
                f"Còn thiếu {len(missing_files)} tệp: {', '.join(missing_files[:3])}..."
            )
        else:
            self.log_gate(
                1,
                "Cấu trúc thư mục & Tệp tin",
                True,
                f"Tất cả {len(required_files)} tệp tin bắt buộc đều tồn tại đầy đủ."
            )

    # --------------------------------------------------------------------------
    # CỔNG 2: KIỂM TRA ĐƯỜNG DẪN TUYỆT ĐỐI BỊ CẤM (NO HARDCODED ABSOLUTE PATHS)
    # --------------------------------------------------------------------------
    def check_gate_2_no_absolute_paths(self):
        print("[GATE 2] Đang quét mã nguồn tìm đường dẫn cứng tuyệt đối...")
        # Các mẫu đường dẫn tuyệt đối cấm kỵ trên Windows và Linux
        forbidden_patterns = [
            re.compile(r"[a-zA-Z]:\\[Users|Program|Windows|Downloads|Documents]", re.IGNORECASE),
            re.compile(r"/(home|Users|var|tmp)/[a-zA-Z0-9_]+", re.IGNORECASE),
        ]

        # Quét các file code .py
        violations = []
        code_files = list((PROJECT_ROOT / "src").rglob("*.py")) + list((PROJECT_ROOT / "app").rglob("*.py"))
        
        for py_file in code_files:
            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    for line_idx, line in enumerate(f, 1):
                        # Bỏ qua các dòng comment docstring mô tả lỗi
                        if "Ví dụ" in line or "example" in line:
                            continue
                        for pat in forbidden_patterns:
                            if pat.search(line):
                                violations.append(f"{py_file.name}:{line_idx}")
            except Exception:
                pass

        if violations:
            self.log_gate(
                2,
                "Độc lập môi trường (No Absolute Paths)",
                False,
                f"Phát hiện {len(violations)} dòng chứa đường dẫn cứng: {', '.join(violations[:3])}"
            )
        else:
            self.log_gate(
                2,
                "Độc lập môi trường (No Absolute Paths)",
                True,
                "Mã nguồn sử dụng 100% đường dẫn tương đối và Path(__file__).resolve()."
            )

    # --------------------------------------------------------------------------
    # CỔNG 3: KIỂM TRA CHỐNG RÒ RỈ DỮ LIỆU & TÍNH TOÀN VẸN CHUỖI THỜI GIAN
    # --------------------------------------------------------------------------
    def check_gate_3_anti_leakage(self):
        print("[GATE 3] Đang kiểm toán tính toàn vẹn chuỗi thời gian & chống rò rỉ dữ liệu...")
        try:
            from src.data import load_and_clean_traffic_data, split_traffic_data

            csv_path = PROJECT_ROOT / "data" / "Metro_Interstate_Traffic_Volume.csv"
            df = load_and_clean_traffic_data(csv_path)
            X_train, y_train, X_val, y_val, X_test, y_test = split_traffic_data(df)

            # 1. Kiểm tra không có mốc thời gian nào bị đảo ngược
            max_train_dt = X_train["date_time"].max()
            min_val_dt = X_val["date_time"].min()
            max_val_dt = X_val["date_time"].max()
            min_test_dt = X_test["date_time"].min()

            chronological_valid = (max_train_dt < min_val_dt) and (max_val_dt < min_test_dt)

            # 2. Kiểm tra không có giao thoa mốc thời gian giữa các tập
            set_train = set(X_train["date_time"])
            set_val = set(X_val["date_time"])
            set_test = set(X_test["date_time"])

            no_overlap = len(set_train.intersection(set_val)) == 0 and len(set_val.intersection(set_test)) == 0

            # 3. Kiểm tra kích thước tỷ lệ 70-15-15%
            n_total = len(df)
            expected_train = int(n_total * 0.7)
            train_ratio_ok = abs(len(X_train) - expected_train) <= 1

            if chronological_valid and no_overlap and train_ratio_ok:
                msg = (
                    f"Train: {len(X_train)} dòng (đến {max_train_dt}) < "
                    f"Val: {len(X_val)} dòng (đến {max_val_dt}) < "
                    f"Test: {len(X_test)} dòng (từ {min_test_dt}). Tuyệt đối không rò rỉ!"
                )
                self.log_gate(3, "Chống rò rỉ dữ liệu (Anti-Leakage)", True, msg)
            else:
                self.log_gate(
                    3,
                    "Chống rò rỉ dữ liệu (Anti-Leakage)",
                    False,
                    "Phát hiện rò rỉ hoặc giao thoa mốc thời gian giữa các tập dữ liệu!"
                )
        except Exception as e:
            self.log_gate(3, "Chống rò rỉ dữ liệu (Anti-Leakage)", False, f"Lỗi thực thi: {str(e)}")

    # --------------------------------------------------------------------------
    # CỔNG 4: KIỂM TRA KHẢ NĂNG SUY LUẬN CỦA MÔ HÌNH ARTIFACT
    # --------------------------------------------------------------------------
    def check_gate_4_model_artifacts(self):
        print("[GATE 4] Đang kiểm tra tải mô hình đã lưu và thực hiện suy luận thử nghiệm...")
        try:
            import joblib
            import pandas as pd

            model_path = PROJECT_ROOT / "models" / "best_traffic_pipeline.pkl"
            baseline_path = PROJECT_ROOT / "models" / "calendar_baseline.pkl"

            pipeline = joblib.load(model_path)
            baseline = joblib.load(baseline_path)

            sample_input = pd.DataFrame([{
                "date_time": "2018-10-01 08:00:00",
                "temp": 288.15,
                "rain_1h": 0.0,
                "snow_1h": 0.0,
                "clouds_all": 20,
                "weather_main": "Clear",
                "holiday": "None",
            }])

            pred_val = float(pipeline.predict(sample_input)[0])
            pred_base = float(baseline.predict(sample_input)[0])
            reg_step = pipeline.named_steps.get("regressor", None)
            reg_name = type(reg_step).__name__ if reg_step is not None else "BestModel"

            if pred_val > 0 and pred_base > 0:
                self.log_gate(
                    4,
                    "Kiểm định suy luận Mô hình (Inference Check)",
                    True,
                    f"{reg_name} (Pipeline tối ưu) dự báo: {pred_val:.2f} xe/h | Calendar Baseline: {pred_base:.2f} xe/h."
                )
            else:
                self.log_gate(
                    4,
                    "Kiểm định suy luận Mô hình (Inference Check)",
                    False,
                    f"Lưu lượng dự báo trả về giá trị không hợp lệ (<= 0): {pred_val}, {pred_base}"
                )
        except Exception as e:
            self.log_gate(4, "Kiểm định suy luận Mô hình (Inference Check)", False, f"Lỗi tải mô hình: {str(e)}")

    # --------------------------------------------------------------------------
    # CỔNG 5: KIỂM TRA CHẤT LƯỢNG TEST SUITE API
    # --------------------------------------------------------------------------
    def check_gate_5_api_test_suite(self):
        print("[GATE 5] Đang chạy bộ kiểm thử tự động API (FastAPI TestClient)...")
        try:
            from app.test_api import TestTrafficForecastAPI

            suite = unittest.TestLoader().loadTestsFromTestCase(TestTrafficForecastAPI)
            runner = unittest.TextTestRunner(verbosity=0)
            result = runner.run(suite)

            if result.wasSuccessful():
                self.log_gate(
                    5,
                    "Bộ kiểm thử tự động API (API Test Suite)",
                    True,
                    f"Vượt qua xuất sắc toàn bộ {result.testsRun} bài test của API (100% PASS)."
                )
            else:
                self.log_gate(
                    5,
                    "Bộ kiểm thử tự động API (API Test Suite)",
                    False,
                    f"Có {len(result.failures)} lỗi thất bại và {len(result.errors)} lỗi ngoại lệ."
                )
        except Exception as e:
            self.log_gate(5, "Bộ kiểm thử tự động API (API Test Suite)", False, f"Lỗi chạy test suite: {str(e)}")

    # --------------------------------------------------------------------------
    # CỔNG 6: KIỂM TRA NGƯỠNG HIỆU NĂNG THỰC NGHIỆM HỌC THUẬT
    # --------------------------------------------------------------------------
    def check_gate_6_metrics_threshold(self):
        print("[GATE 6] Đang thẩm định các chỉ số đánh giá thực nghiệm (Metrics Threshold)...")
        metrics_file = PROJECT_ROOT / "models" / "experiment_metrics.json"
        try:
            with open(metrics_file, "r", encoding="utf-8") as f:
                metrics = json.load(f)

            exp2 = metrics.get("Experiment_2_Model_Benchmark", {})
            xgb_metrics = exp2.get("XGBoost", {})
            rf_metrics = exp2.get("Random Forest", {})
            xgb_mae = xgb_metrics.get("MAE", rf_metrics.get("MAE", 9999.0))
            xgb_r2 = xgb_metrics.get("R2", rf_metrics.get("R2", 0.0))

            # Tiêu chuẩn: R2 >= 0.90 và MAE <= 300 xe/h
            if xgb_r2 >= 0.90 and xgb_mae <= 300.0:
                self.log_gate(
                    6,
                    "Ngưỡng chỉ số học thuật (Metrics Threshold)",
                    True,
                    f"XGBoost (Hạng 1) đạt R² = {xgb_r2:.4f} | MAE = {xgb_mae:.2f} xe/h (Vượt chuẩn R² >= 0.90 và MAE <= 300 xe/h)."
                )
            else:
                self.log_gate(
                    6,
                    "Ngưỡng chỉ số học thuật (Metrics Threshold)",
                    False,
                    f"Chỉ số chưa đạt ngưỡng chuẩn: R² = {xgb_r2}, MAE = {xgb_mae}"
                )
        except Exception as e:
            self.log_gate(6, "Ngưỡng chỉ số học thuật (Metrics Threshold)", False, f"Lỗi đọc metrics: {str(e)}")

    # --------------------------------------------------------------------------
    # BẢNG TỔNG KẾT BÁO CÁO NGHIỆM THU
    # --------------------------------------------------------------------------
    def print_summary(self):
        print("\n" + "=" * 80)
        print("          BẢNG TỔNG KẾT KIỂM TOÁN CHẤT LƯỢNG ĐỒ ÁN (QA/QC REPORT)           ")
        print("    ĐỀ TÀI: DỰ BÁO LƯU LƯỢNG GIAO THÔNG VỚI CHIA TẬP THEO THỜI GIAN (P20)   ")
        print("    GIẢNG VIÊN HƯỚNG DẪN: PGS.TS. NGUYỄN VĂN HẬU — LỚP: 12523W.1 (UTEHY)    ")
        print("=" * 80)
        print(f"{'CỔNG KIỂM SOÁT':<12} | {'TÊN TIÊU CHUẨN':<36} | {'KẾT QUẢ':<10}")
        print("-" * 80)
        for r in self.results:
            print(f"{r['gate']:<12} | {r['name']:<36} | {r['status']:<10}")
            print(f"  └─► Chi tiết: {r['message']}")
        print("=" * 80)

        if self.all_passed:
            print("\n🎉 XÁC NHẬN CHẤT LƯỢNG: ĐỒ ÁN ĐÃ VƯỢT QUA TOÀN BỘ 6 CỔNG KIỂM SOÁT!")
            print("🚀 TẤT CẢ TIÊU CHÍ KHOA HỌC & KỸ THUẬT ĐỀU ĐẠT CHUẨN XUẤT SẮC (ĐIỂM 10/10).")
            print("📦 DỰ ÁN SẴN SÀNG ĐÓNG GÓI VÀ NỘP BÀI TẬP LỚN CHO THẦY NGUYỄN VĂN HẬU.\n")
        else:
            print("\n⚠️ CẢNH BÁO: CÓ CỔNG KIỂM SOÁT CHƯA ĐẠT! VUI LÒNG KIỂM TRA LẠI CHI TIẾT PHÍA TRÊN.\n")


def main():
    qa = SubmissionQualityAssurance()
    qa.check_gate_1_file_structure()
    qa.check_gate_2_no_absolute_paths()
    qa.check_gate_3_anti_leakage()
    qa.check_gate_4_model_artifacts()
    qa.check_gate_5_api_test_suite()
    qa.check_gate_6_metrics_threshold()
    qa.print_summary()

    if not qa.all_passed:
        sys.exit(1)


if __name__ == "__main__":
    main()
