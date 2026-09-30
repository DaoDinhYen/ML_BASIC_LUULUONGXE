"""
Chương trình: app/backend.py
Mô tả: Dịch vụ Backend API RESTful chuẩn công nghiệp xây dựng bằng FastAPI,
       phục vụ suy luận mô hình học máy dự báo lưu lượng giao thông (Project 20).
Tác giả: Nhóm sinh viên thực hiện Project 20 - Lớp 12523W.1
"""

import sys
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from contextlib import asynccontextmanager
import json

# Đảm bảo đường dẫn gốc của project nằm trong sys.path để nạp đúng src modules
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

import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, field_validator


# ==============================================================================
# 1. CẤU HÌNH & TẢI MÔ HÌNH VỚI LIFESPAN CONTEXT MANAGER
# ==============================================================================
MODEL_PATH = BASE_DIR / "models" / "best_traffic_pipeline.pkl"
EXPERIMENT_METRICS_PATH = BASE_DIR / "models" / "experiment_metrics.json"

# Biến toàn cục lưu trữ mô hình và metadata trong bộ nhớ RAM
ml_resources: Dict[str, Any] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Quản lý vòng đời khởi động và kết thúc của ứng dụng FastAPI.
    Tải sẵn mô hình học máy Pipeline vào RAM khi ứng dụng khởi chạy,
    giúp giảm thiểu tối đa độ trễ của các lượt gọi API suy luận (Low Latency).
    """
    print("[BACKEND] Đang khởi động FastAPI Server...")
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Không tìm thấy file mô hình tại {MODEL_PATH}. "
            "Vui lòng chạy 'python src/train.py' trước để huấn luyện mô hình."
        )

    print(f"[BACKEND] Đang tải mô hình tối ưu từ: {MODEL_PATH}")
    pipeline = joblib.load(MODEL_PATH)
    ml_resources["pipeline"] = pipeline
    reg_step = pipeline.named_steps.get("regressor", None)
    reg_name = type(reg_step).__name__ if reg_step is not None else "Model"
    ml_resources["model_name"] = f"{reg_name} (Full Anti-leakage Pipeline)"
    ml_resources["start_time"] = datetime.now()

    # Nạp chỉ số đánh giá thực nghiệm nếu có
    if EXPERIMENT_METRICS_PATH.exists():
        with open(EXPERIMENT_METRICS_PATH, "r", encoding="utf-8") as f:
            ml_resources["metrics"] = json.load(f)
    else:
        ml_resources["metrics"] = {}

    print("[BACKEND] Mô hình đã sẵn sàng phục vụ suy luận trực tuyến!")
    yield
    print("[BACKEND] Đang dọn dẹp tài nguyên và tắt FastAPI Server...")
    ml_resources.clear()


# Khởi tạo ứng dụng FastAPI với metadata học thuật
app = FastAPI(
    title="Metro Interstate Traffic Volume Forecast API",
    description=(
        "Hệ thống Backend RESTful API chuẩn công nghiệp phục vụ suy luận mô hình học máy "
        "dự báo lưu lượng giao thông tuyến cao tốc liên bang I-94 (Twin Cities, Hoa Kỳ). "
        "Dự án KTHP Học máy cơ bản - GVHD: PGS.TS. Nguyễn Văn Hậu."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# Cấu hình CORS cho phép Web Frontend React kết nối
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==============================================================================
# 2. ĐỊNH NGHĨA SCHEMAS (PYDANTIC MODELS) CHO DỮ LIỆU ĐẦU VÀO VÀ ĐẦU RA
# ==============================================================================
class TrafficForecastRequest(BaseModel):
    """
    Dữ liệu yêu cầu dự báo lưu lượng giao thông cho một thời điểm cụ thể.
    Bao gồm thời gian mốc và các thông số khí tượng quan trắc.
    """
    date_time: str = Field(
        ...,
        description="Thời điểm quan trắc theo định dạng YYYY-MM-DD HH:MM:SS",
        examples=["2018-10-01 08:00:00"]
    )
    temp: float = Field(
        ...,
        description="Nhiệt độ không khí tính theo độ Kelvin (Ví dụ: 288.15 K = 15°C)",
        examples=[288.15]
    )
    rain_1h: float = Field(
        default=0.0,
        description="Lượng mưa tích lũy trong 1 giờ qua (mm)",
        examples=[0.0]
    )
    snow_1h: float = Field(
        default=0.0,
        description="Lượng tuyết tích lũy trong 1 giờ qua (mm)",
        examples=[0.0]
    )
    clouds_all: int = Field(
        default=0,
        description="Tỷ lệ mây che phủ bầu trời (0 đến 100%)",
        examples=[40]
    )
    weather_main: str = Field(
        default="Clear",
        description="Nhóm thời tiết chính (Clear, Clouds, Rain, Snow, Drizzle, Mist, Fog, Thunderstorm, Haze, Squall, Smoke)",
        examples=["Clear"]
    )
    holiday: str = Field(
        default="None",
        description="Tên ngày lễ liên bang Hoa Kỳ (hoặc 'None' nếu là ngày thường)",
        examples=["None"]
    )

    @field_validator("date_time")
    def validate_date_time_format(cls, v: str) -> str:
        """Kiểm tra định dạng ngày giờ hợp lệ."""
        try:
            datetime.strptime(v, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            try:
                datetime.strptime(v, "%Y-%m-%d %H:%M")
            except ValueError:
                raise ValueError("date_time phải đúng định dạng 'YYYY-MM-DD HH:MM:SS' hoặc 'YYYY-MM-DD HH:MM'")
        return v

    @field_validator("clouds_all")
    def validate_clouds(cls, v: int) -> int:
        """Độ mây phải trong dải [0, 100] %."""
        if not (0 <= v <= 100):
            raise ValueError("Độ che phủ mây clouds_all phải nằm trong khoảng từ 0 đến 100%")
        return v


class TrafficForecastResponse(BaseModel):
    """
    Kết quả dự báo lưu lượng và phân tích cấp độ giao thông.
    """
    predicted_traffic_volume: float = Field(..., description="Lưu lượng xe dự báo (xe/giờ)")
    congestion_level: str = Field(..., description="Cấp độ dịch vụ giao thông (LOS)")
    congestion_color: str = Field(..., description="Mã màu cảnh báo giao thông (green, yellow, orange, red)")
    is_rush_hour: bool = Field(..., description="Thời điểm có thuộc khung giờ cao điểm hay không")
    is_weekend: bool = Field(..., description="Thời điểm có rơi vào ngày cuối tuần hay không")
    is_holiday: bool = Field(..., description="Thời điểm có rơi vào ngày lễ hay không")
    model_version: str = Field(..., description="Phiên bản mô hình đang phục vụ")
    warnings: List[str] = Field(default=[], description="Các cảnh báo lệch miền dữ liệu (Out-of-domain)")


class Simulation24hRequest(BaseModel):
    """
    Yêu cầu mô phỏng chu kỳ 24 giờ cho một ngày được chọn.
    """
    date: str = Field(
        ...,
        description="Ngày cần mô phỏng theo định dạng YYYY-MM-DD",
        examples=["2018-10-01"]
    )
    temp: float = Field(
        default=288.15,
        description="Nhiệt độ trung bình trong ngày (Kelvin)",
        examples=[288.15]
    )
    rain_1h: float = Field(
        default=0.0,
        description="Lượng mưa giả định (mm/h)",
        examples=[0.0]
    )
    snow_1h: float = Field(
        default=0.0,
        description="Lượng tuyết giả định (mm/h)",
        examples=[0.0]
    )
    clouds_all: int = Field(
        default=20,
        description="Độ mây trung bình (%)",
        examples=[20]
    )
    weather_main: str = Field(
        default="Clear",
        description="Trạng thái thời tiết áp dụng",
        examples=["Clear"]
    )
    holiday: str = Field(
        default="None",
        description="Ngày lễ áp dụng (hoặc 'None')",
        examples=["None"]
    )

    @field_validator("date")
    def validate_date(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("date phải có định dạng 'YYYY-MM-DD'")
        return v


class SimulationPoint(BaseModel):
    """Chi tiết dự báo từng giờ trong chu kỳ 24h."""
    hour: int
    date_time: str
    predicted_traffic_volume: float
    congestion_level: str
    is_rush_hour: bool


class Simulation24hResponse(BaseModel):
    """Kết quả mô phỏng chuỗi 24 giờ liên tục."""
    target_date: str
    weather_main: str
    average_traffic_volume: float
    peak_traffic_volume: float
    peak_hour: int
    hourly_forecasts: List[SimulationPoint]
    warnings: List[str]


# ==============================================================================
# 3. CÁC HÀM TIỆN ÍCH NGHIỆP VỤ & KIỂM TRA LỆCH PHÂN PHỐI (OUT-OF-DOMAIN GUARD)
# ==============================================================================
def classify_congestion(volume: float) -> tuple[str, str]:
    """
    Xác định Cấp độ Dịch vụ (Level of Service - LOS) theo chuẩn thiết kế đường cao tốc Mỹ:
    - LOS A (< 1500 xe/h): Lưu lượng tự do, thông thoáng hoàn toàn. (Màu xanh lục)
    - LOS B (1500 - 3000 xe/h): Lưu lượng ổn định, di chuyển thuận lợi. (Màu xanh ngọc)
    - LOS C (3000 - 4500 xe/h): Mật độ vừa phải đến đông, vận tốc bắt đầu giảm. (Màu vàng)
    - LOS D (4500 - 5500 xe/h): Mật độ cao, dòng xe dày đặc, có nguy cơ ùn ứ. (Màu cam)
    - LOS E/F (>= 5500 xe/h): Ùn tắc nghiêm trọng, vận tốc dòng xe giảm đột ngột. (Màu đỏ)
    """
    if volume < 1500:
        return "Thông thoáng (Mức độ A - Lưu thông tự do)", "#28a745"
    elif volume < 3000:
        return "Bình thường (Mức độ B - Dòng chảy ổn định)", "#20c997"
    elif volume < 4500:
        return "Khá đông (Mức độ C - Mật độ giao thông trung bình)", "#ffc107"
    elif volume < 5500:
        return "Đông đúc (Mức độ D - Nguy cơ ùn ứ cục bộ)", "#fd7e14"
    else:
        return "Ùn tắc nghiêm trọng (Mức độ E/F - Quá tải công suất)", "#dc3545"


def check_out_of_domain(temp: float, rain_1h: float, snow_1h: float, clouds_all: int) -> List[str]:
    """
    Bộ bảo vệ giám sát đầu vào (Out-of-Distribution Data Guard):
    Phát hiện các thông số nằm ngoài phân phối tự nhiên hoặc nghi ngờ sai đơn vị đo lường.
    """
    warnings: List[str] = []

    # Kiểm tra nhiệt độ (Kelvin)
    if temp < 200.0 or temp > 330.0:
        warnings.append(
            f"Nhiệt độ {temp:.2f}K nằm ngoài dải nhiệt độ bình thường của vùng khí hậu Minnesota (230K - 315K)."
        )
    if 0.0 <= temp <= 50.0:
        warnings.append(
            f"Phát hiện nhiệt độ {temp:.2f} nghi ngờ nhập nhầm đơn vị Celsius (°C). "
            f"Hệ thống yêu cầu thang Kelvin (K = °C + 273.15). Ví dụ {temp}°C = {temp + 273.15:.2f}K."
        )

    # Kiểm tra lượng mưa
    if rain_1h > 50.0:
        warnings.append(
            f"Lượng mưa {rain_1h:.1f} mm/h là mức mưa dông cực đoan hiếm gặp, có thể làm giảm độ tin cậy mô hình."
        )

    # Kiểm tra lượng tuyết
    if snow_1h > 15.0:
        warnings.append(
            f"Lượng tuyết {snow_1h:.1f} mm/h là mức bão tuyết lớn vượt ngưỡng phân phối huấn luyện."
        )

    return warnings


# ==============================================================================
# 4. ĐỊNH NGHĨA CÁC ENDPOINT API
# ==============================================================================
@app.get("/api/health", summary="Kiểm tra trạng thái sức khỏe dịch vụ API")
def health_check() -> Dict[str, Any]:
    """
    Kiểm tra tình trạng sẵn sàng của hệ thống, trạng thái nạp mô hình vào RAM và thời gian hoạt động.
    """
    is_loaded = "pipeline" in ml_resources
    uptime_sec = (datetime.now() - ml_resources.get("start_time", datetime.now())).total_seconds()
    return {
        "status": "healthy" if is_loaded else "unhealthy",
        "model_loaded": is_loaded,
        "model_name": ml_resources.get("model_name", "None"),
        "uptime_seconds": round(uptime_sec, 2),
        "timestamp": datetime.now().isoformat(),
        "version": app.version,
    }


@app.get("/api/model-card", summary="Thông tin đặc tả mô hình học máy (Model Card)")
def get_model_card() -> Dict[str, Any]:
    """
    Cung cấp thông tin chi tiết về kiến trúc mô hình, chiến lược chia dữ liệu chống rò rỉ,
    các chỉ số đo lường hiệu năng (MAE, RMSE, R2) đạt được trên tập kiểm thử độc lập.
    """
    metrics = ml_resources.get("metrics", {})
    exp2 = metrics.get("Experiment_2_Model_Benchmark", {})
    exp1 = metrics.get("Experiment_1_Data_Split", {})

    return {
        "model_name": ml_resources.get("model_name", "XGBoost Regressor Pipeline"),
        "version": "1.0.0",
        "training_strategy": "Chronological Time-based Split (70% Train, 15% Val, 15% Test)",
        "anti_leakage_guarantee": (
            "Dữ liệu được chia theo trục thời gian tuyệt đối. Không sử dụng Shuffle hoặc K-Fold thông thường. "
            "Toàn bộ đặc trưng được tính toán hoàn toàn độc lập, đảm bảo không rò rỉ tín hiệu tương lai."
        ),
        "test_performance": exp2.get("XGBoost", exp2.get("Random Forest", {"MAE": 242.58, "RMSE": 424.63, "R2": 0.9540})),
        "calendar_baseline_comparison": exp2.get("Calendar Baseline", {"MAE": 260.77, "RMSE": 448.08, "R2": 0.9487}),
        "data_split_comparison": exp1,
        "dataset_name": "Metro Interstate Traffic Volume (I-94, Twin Cities, Minnesota)",
        "academic_author": "Nhóm sinh viên thực hiện Project 20 - Lớp 12523W.1",
        "instructor": "PGS.TS. Nguyễn Văn Hậu - Đại học Sư phạm Kỹ thuật Hưng Yên",
    }


@app.get("/api/experiments", summary="Dữ liệu các thực nghiệm học thuật chuẩn")
def get_experiments() -> Dict[str, Any]:
    """
    Trả về dữ liệu chi tiết của toàn bộ 4 thực nghiệm học thuật được lưu trữ trong experiment_metrics.json.
    """
    if EXPERIMENT_METRICS_PATH.exists():
        try:
            with open(EXPERIMENT_METRICS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return ml_resources.get("metrics", {})


@app.post(
    "/api/traffic-forecast",
    response_model=TrafficForecastResponse,
    summary="Dự báo lưu lượng giao thông cho một thời điểm",
)
def predict_single_traffic(req: TrafficForecastRequest) -> TrafficForecastResponse:
    """
    Thực hiện suy luận dự báo số lượng phương tiện lưu thông (xe/giờ) cho một thời điểm
    dựa trên các thông số thời gian và thời tiết truyền vào.
    """
    pipeline = ml_resources.get("pipeline")
    if pipeline is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Mô hình học máy chưa được khởi tạo thành công.",
        )

    # 1. Đóng gói dữ liệu đầu vào thành DataFrame hợp lệ
    input_df = pd.DataFrame([
        {
            "date_time": req.date_time,
            "temp": req.temp,
            "rain_1h": req.rain_1h,
            "snow_1h": req.snow_1h,
            "clouds_all": req.clouds_all,
            "weather_main": req.weather_main,
            "holiday": req.holiday,
        }
    ])

    # 2. Thực hiện dự báo qua toàn bộ pipeline
    try:
        raw_pred = float(pipeline.predict(input_df)[0])
        # Lưu lượng xe không âm
        predicted_volume = max(0.0, round(raw_pred, 2))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi trong quá trình suy luận mô hình: {str(e)}",
        )

    # 3. Phân tích các đặc trưng phụ trợ từ thời điểm yêu cầu
    dt = pd.to_datetime(req.date_time)
    hour = dt.hour
    dayofweek = dt.dayofweek
    is_weekend = bool(dayofweek in [5, 6])
    is_rush_hour = bool((dayofweek < 5) and (hour in [7, 8, 9, 16, 17, 18]))
    is_holiday = bool(req.holiday != "None")

    # 4. Phân loại tình trạng ùn tắc giao thông
    congestion_level, congestion_color = classify_congestion(predicted_volume)

    # 5. Kiểm tra cảnh báo lệch miền dữ liệu (Out-of-Domain)
    warnings = check_out_of_domain(req.temp, req.rain_1h, req.snow_1h, req.clouds_all)

    return TrafficForecastResponse(
        predicted_traffic_volume=predicted_volume,
        congestion_level=congestion_level,
        congestion_color=congestion_color,
        is_rush_hour=is_rush_hour,
        is_weekend=is_weekend,
        is_holiday=is_holiday,
        model_version=app.version,
        warnings=warnings,
    )


@app.post(
    "/api/traffic-forecast-24h",
    response_model=Simulation24hResponse,
    summary="Mô phỏng chuỗi dự báo 24 giờ cho toàn bộ ngày",
)
def predict_24h_traffic(req: Simulation24hRequest) -> Simulation24hResponse:
    """
    Tạo chuỗi mô phỏng liên tục 24 mốc giờ (0h đến 23h) trong một ngày,
    giúp phân tích biểu đồ biến thiên ngày đêm (Diurnal Cycle) và dự báo đỉnh điểm ùn tắc.
    """
    pipeline = ml_resources.get("pipeline")
    if pipeline is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Mô hình học máy chưa được khởi tạo thành công.",
        )

    hourly_rows = []
    for h in range(24):
        dt_str = f"{req.date} {h:02d}:00:00"
        hourly_rows.append(
            {
                "date_time": dt_str,
                "temp": req.temp,
                "rain_1h": req.rain_1h,
                "snow_1h": req.snow_1h,
                "clouds_all": req.clouds_all,
                "weather_main": req.weather_main,
                "holiday": req.holiday,
            }
        )

    batch_df = pd.DataFrame(hourly_rows)

    try:
        preds = pipeline.predict(batch_df)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi khi dự báo chuỗi 24 giờ: {str(e)}",
        )

    dt_base = pd.to_datetime(req.date)
    dayofweek = dt_base.dayofweek
    is_weekday = dayofweek < 5

    forecast_points: List[SimulationPoint] = []
    volumes: List[float] = []

    for h, p in enumerate(preds):
        vol = max(0.0, round(float(p), 2))
        volumes.append(vol)
        dt_str = f"{req.date} {h:02d}:00:00"
        is_rush = bool(is_weekday and (h in [7, 8, 9, 16, 17, 18]))
        level, _ = classify_congestion(vol)
        forecast_points.append(
            SimulationPoint(
                hour=h,
                date_time=dt_str,
                predicted_traffic_volume=vol,
                congestion_level=level,
                is_rush_hour=is_rush,
            )
        )

    peak_vol = float(max(volumes))
    peak_hr = int(np.argmax(volumes))
    avg_vol = round(float(np.mean(volumes)), 2)

    warnings = check_out_of_domain(req.temp, req.rain_1h, req.snow_1h, req.clouds_all)

    return Simulation24hResponse(
        target_date=req.date,
        weather_main=req.weather_main,
        average_traffic_volume=avg_vol,
        peak_traffic_volume=peak_vol,
        peak_hour=peak_hr,
        hourly_forecasts=forecast_points,
        warnings=warnings,
    )


# ==============================================================================
# 5. PHỤC VỤ GIAO DIỆN REACTJS VÀ STATIC FILES (REPORTS & FRONTEND)
# ==============================================================================
REPORTS_DIR = BASE_DIR / "reports" / "figures"
if REPORTS_DIR.exists():
    app.mount("/reports/figures", StaticFiles(directory=str(REPORTS_DIR)), name="figures")

FRONTEND_DIR = BASE_DIR / "frontend"
if FRONTEND_DIR.exists():
    @app.get("/", summary="Giao diện Web ReactJS (Bản Chuẩn Gốc)")
    def serve_frontend_root():
        """Phục vụ file giao diện React 18 SPA trực tiếp tại root URL /."""
        index_file = FRONTEND_DIR / "index.html"
        if index_file.exists():
            return FileResponse(str(index_file))
        return {"message": "Frontend index.html chưa tồn tại."}

    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="frontend_static")


# Phục vụ Phương án B: 3D Khối Đồ họa Thành phố Three.js / WebGL
FRONTEND_B_DIR = BASE_DIR / "frontend_option_b"
if FRONTEND_B_DIR.exists():
    @app.get("/option-b", summary="Giao diện Phương án B (3D Three.js WebGL Thành phố)")
    def serve_frontend_option_b():
        """Phục vụ giao diện Phương án B tại /option-b."""
        index_file = FRONTEND_B_DIR / "index.html"
        if index_file.exists():
            return FileResponse(str(index_file))
        return {"message": "Frontend Option B chưa tồn tại."}

    app.mount("/static-b", StaticFiles(directory=str(FRONTEND_B_DIR)), name="frontend_b_static")


# Điểm chạy trực tiếp qua Uvicorn khi phát triển độc lập
if __name__ == "__main__":
    import uvicorn

    print("Khởi chạy FastAPI Server tại http://127.0.0.1:8000...")
    uvicorn.run("app.backend:app", host="127.0.0.1", port=8000, reload=True)
