"""
Chương trình: app/test_api.py
Mô tả: Bộ kiểm thử tự động (Unit Test Suite) cho Backend API FastAPI của Project 20.
       Kiểm tra tính đúng đắn của các endpoint: /api/health, /api/model-card,
       /api/traffic-forecast, /api/traffic-forecast-24h, và cơ chế Out-of-Domain Guard.
Tác giả: Nhóm sinh viên thực hiện Project 20 - Lớp 12523W.1
"""

import sys
from pathlib import Path
import unittest

# Đảm bảo đường dẫn gốc của project được nạp vào sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

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

from fastapi.testclient import TestClient
from app.backend import app


class TestTrafficForecastAPI(unittest.TestCase):
    """
    Tập hợp các ca kiểm thử hồi quy cho API Backend.
    Sử dụng TestClient mô phỏng gọi HTTP Request mà không cần khởi động server Uvicorn thật.
    """

    @classmethod
    def setUpClass(cls):
        """Khởi tạo TestClient với Lifespan Context."""
        cls.client = TestClient(app)

    def test_01_health_check(self):
        """Kiểm tra Endpoint /api/health trả về HTTP 200 và mô hình đã được nạp."""
        with TestClient(app) as client:
            response = client.get("/api/health")
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["status"], "healthy")
            self.assertTrue(data["model_loaded"])
            self.assertTrue(any(name in data["model_name"] for name in ["XGBRegressor", "RandomForestRegressor", "Pipeline"]))

    def test_02_model_card(self):
        """Kiểm tra Endpoint /api/model-card cung cấp đầy đủ thông tin đặc tả học thuật."""
        with TestClient(app) as client:
            response = client.get("/api/model-card")
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("anti_leakage_guarantee", data)
            self.assertIn("test_performance", data)
            self.assertIn("MAE", data["test_performance"])
            self.assertIn("R2", data["test_performance"])

    def test_03_forecast_valid_input(self):
        """Kiểm tra dự báo thành công với dữ liệu đầu vào hợp lệ vào giờ cao điểm buổi sáng."""
        payload = {
            "date_time": "2018-10-01 08:00:00",  # Thứ 2, 8 giờ sáng (Rush hour)
            "temp": 288.15,                      # 15°C
            "rain_1h": 0.0,
            "snow_1h": 0.0,
            "clouds_all": 20,
            "weather_main": "Clear",
            "holiday": "None"
        }
        with TestClient(app) as client:
            response = client.post("/api/traffic-forecast", json=payload)
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertGreater(data["predicted_traffic_volume"], 0)
            self.assertTrue(data["is_rush_hour"])
            self.assertFalse(data["is_weekend"])
            self.assertFalse(data["is_holiday"])
            self.assertIn("congestion_level", data)
            self.assertIn("congestion_color", data)
            self.assertEqual(len(data["warnings"]), 0)

    def test_04_forecast_out_of_domain_warning(self):
        """Kiểm tra cơ chế cảnh báo Out-of-Domain khi nhập sai độ C thay vì Kelvin hoặc mưa cực đoan."""
        payload = {
            "date_time": "2018-10-01 12:00:00",
            "temp": 25.0,     # Nhập nhầm 25 độ C thay vì Kelvin (298.15)
            "rain_1h": 65.0,  # Mưa bão cực đoan > 50mm
            "snow_1h": 0.0,
            "clouds_all": 100,
            "weather_main": "Rain",
            "holiday": "None"
        }
        with TestClient(app) as client:
            response = client.post("/api/traffic-forecast", json=payload)
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertGreater(len(data["warnings"]), 0)
            # Kiểm tra có cảnh báo độ C
            has_celsius_warning = any("Celsius" in w for w in data["warnings"])
            self.assertTrue(has_celsius_warning, "Phải có cảnh báo nhập nhầm nhiệt độ Celsius.")
            # Kiểm tra có cảnh báo mưa lớn
            has_rain_warning = any("mưa dông cực đoan" in w for w in data["warnings"])
            self.assertTrue(has_rain_warning, "Phải có cảnh báo mưa cực đoan.")

    def test_05_forecast_invalid_schema(self):
        """Kiểm tra hệ thống trả về mã lỗi HTTP 422 khi dữ liệu sai định dạng Pydantic."""
        payload = {
            "date_time": "sai-dinh-dang-gio",  # Sai định dạng datetime
            "temp": "chu_khong_phai_so",      # Sai kiểu dữ liệu
            "clouds_all": 150                 # Vượt quá 100%
        }
        with TestClient(app) as client:
            response = client.post("/api/traffic-forecast", json=payload)
            self.assertEqual(response.status_code, 422)

    def test_06_simulation_24h(self):
        """Kiểm tra Endpoint mô phỏng 24 giờ /api/traffic-forecast-24h."""
        payload = {
            "date": "2018-10-02",
            "temp": 285.0,
            "rain_1h": 0.0,
            "snow_1h": 0.0,
            "clouds_all": 10,
            "weather_main": "Clear",
            "holiday": "None"
        }
        with TestClient(app) as client:
            response = client.post("/api/traffic-forecast-24h", json=payload)
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["target_date"], "2018-10-02")
            self.assertEqual(len(data["hourly_forecasts"]), 24)
            self.assertGreater(data["peak_traffic_volume"], 0)
            self.assertTrue(0 <= data["peak_hour"] <= 23)
            self.assertGreater(data["average_traffic_volume"], 0)

    def test_07_experiments(self):
        """Kiểm tra Endpoint /api/experiments trả về dữ liệu 4 thực nghiệm học thuật."""
        with TestClient(app) as client:
            response = client.get("/api/experiments")
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("Experiment_1_Data_Split", data)
            self.assertIn("Experiment_2_Model_Benchmark", data)
            self.assertIn("Experiment_3_Data_Drift", data)
            self.assertIn("Experiment_4_Error_Analysis", data)

    def test_08_react_root(self):
        """Kiểm tra Endpoint Root '/' phục vụ file HTML giao diện ReactJS."""
        with TestClient(app) as client:
            response = client.get("/")
            self.assertEqual(response.status_code, 200)
            self.assertIn("text/html", response.headers.get("content-type", ""))
            self.assertIn("Dự Báo Lưu Lượng Giao Thông", response.text)

    def test_09_option_b_endpoint(self):
        """Kiểm tra Endpoint '/option-b' phục vụ giao diện Phương án B: 3D Three.js."""
        with TestClient(app) as client:
            response = client.get("/option-b")
            self.assertEqual(response.status_code, 200)
            self.assertIn("text/html", response.headers.get("content-type", ""))


if __name__ == "__main__":
    unittest.main()
