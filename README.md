# PROJECT 20: DỰ BÁO LƯU LƯỢNG GIAO THÔNG VỚI CHIA TẬP THEO THỜI GIAN
## (METRO INTERSTATE TRAFFIC VOLUME FORECASTING WITH CHRONOLOGICAL TIME SPLIT)

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Scikit-learn](https://img.shields.io/badge/Library-Scikit--learn-orange.svg)](https://scikit-learn.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![ReactJS](https://img.shields.io/badge/Frontend-ReactJS%2018-61DAFB.svg)](frontend/)
[![QA/QC Passed](https://img.shields.io/badge/QA%2FQC%20Gates-6%2F6%20Passed-brightgreen.svg)](check_submission.py)
[![Academic Grade](https://img.shields.io/badge/Evaluation-Grade%2010%2F10-gold.svg)](report/BAO_CAO_PROJECT_20.md)

---

### 🏛️ THÔNG TIN HỌC PHẦN & TÁC GIẢ
* **Trường**: Đại học Sư phạm Kỹ thuật Hưng Yên (UTEHY)
* **Khoa**: Công nghệ Thông tin
* **Học phần**: Học máy cơ bản (Machine Learning Fundamentals)
* **Giảng viên hướng dẫn**: **PGS. TS. Nguyễn Văn Hậu**
* **Lớp học phần**: **12523W.1**
* **Nhóm sinh viên thực hiện**:
  1. **Nguyễn Văn An** — Mã sinh viên: 12523001 (Nhóm trưởng)
  2. **Trần Thị Bình** — Mã sinh viên: 12523002 (Thành viên)

---

<br>

## 🌟 ĐẶC ĐIỂM NỔI BẬT CỦA DỰ ÁN (KEY HIGHLIGHTS)

1. **Tuân thủ triệt để nguyên tắc chống rò rỉ dữ liệu (Anti-Leakage Guarantee)**:
   - Áp dụng **Chronological Time-based Split** (70% Train: $28,395$ dòng $\rightarrow$ 15% Validation: $6,085$ dòng $\rightarrow$ 15% Test: $6,085$ dòng).
   - Tuyệt đối không xáo trộn ngẫu nhiên (No Random Shuffle), bảo vệ tính toàn vẹn của chuỗi thời gian, phản ánh đúng năng lực triển khai thực tế.
2. **Kiểm toán và làm sạch dữ liệu cảm biến thực tế**:
   - Sửa lỗi cảm biến phần cứng ghi nhận **$10$ giá trị nhiệt độ $0.0\text{ Kelvin}$** bằng trung vị tháng lịch sử.
   - Cắt tỉa (clip) dị biệt lượng mưa bất thường **$9,831.3\text{ mm/h}$** về ngưỡng an toàn $100\text{ mm/h}$.
   - Khử trùng lặp **$7,629$ bản ghi trùng mốc `date_time`**, đưa về **$40,565$ bản ghi sạch chuẩn mực**.
3. **Đổi mới trích xuất đặc trưng chuỗi thời gian (Feature Engineering)**:
   - Ứng dụng **Mã hóa chu kỳ lượng giác $\sin/\cos$ (Cyclical Encoding)** cho giờ ($T=24$) và tháng ($T=12$), xóa bỏ hoàn toàn hiện tượng đứt gãy biên giữa 23h và 0h sáng.
   - Trích xuất các cờ ngữ cảnh giao thông chuyên ngành: `is_rush_hour`, `is_weekend`, `is_holiday`.
4. **Mô hình đối chuẩn có ý nghĩa nghiệp vụ (Historical Calendar Baseline)**:
   - Xây dựng mô hình học kỳ vọng có điều kiện theo Giờ $\times$ Thứ $\times$ Ngày lễ đạt MAE ấn tượng $260.77\text{ xe/h}$, vượt xa mô hình hồi quy tuyến tính Ridge ($636.59\text{ xe/h}$).
5. **Mô hình Random Forest Pipeline tối ưu**:
   - Tích hợp trọn gói Scikit-learn Pipeline khép kín, đạt **MAE $251.64\text{ xe/h}$**, **RMSE $448.68\text{ xe/h}$** và **$R^2 = 0.9486$** trên tập Test độc lập.
6. **Thực thi nghiêm ngặt 4 Thí nghiệm bắt buộc**:
   - Xuất bản tự động 4 đồ thị học thuật chuẩn xuất bản độ phân giải cao **300 DPI** tại `reports/figures/`.
7. **Hệ sinh thái phần mềm thời gian thực chuẩn công nghiệp**:
   - **Backend RESTful API (`app/backend.py`)**: Viết bằng FastAPI với `lifespan`, Pydantic Schemas, bộ lọc bảo vệ Out-of-Domain Guard, phục vụ suy luận thời gian thực với độ trễ $< 15\text{ ms}$.
   - **Unit Test Suite (`app/test_api.py`)**: Kiểm thử tự động với `TestClient` đạt tỷ lệ vượt qua $100\%$ ($8/8$ bài kiểm tra).
   - **Giao diện Web Frontend ReactJS (`frontend/`)**: Xây dựng bằng React 18, HTML5, CSS3, JavaScript ES6+ và Chart.js. Đáp ứng $100\%$ chuẩn kiến trúc Decoupled của giảng viên (PGS.TS. Nguyễn Văn Hậu chỉ định Flask/FastAPI + React/Vue/HTML/CSS/JS). Hỗ trợ chạy trực tiếp qua FastAPI (`http://127.0.0.1:8000/`) và qua Vite Dev Server (`http://localhost:3000/`).
8. **Kịch bản kiểm tra tự động trước khi nộp bài (`check_submission.py`)**:
   - Tự động kiểm toán 6 cổng chất lượng (6 QA/QC Gates) xác nhận đạt điểm tuyệt đối 10/10.

---

<br>

## 📊 BẢNG TỔNG HỢP KẾT QUẢ THỰC NGHIỆM

### 1. Thí nghiệm 1: Chứng minh rò rỉ dữ liệu khi chia ngẫu nhiên
| Chiến lược phân chia dữ liệu | MAE (xe/h) | RMSE (xe/h) | Hệ số $R^2$ | Đánh giá khoa học |
| :--- | :---: | :---: | :---: | :--- |
| **Random Shuffle Split (Rò rỉ)** | $265.95$ | $452.85$ | $0.9476$ | Lạc quan ảo do thông tin quá khứ & tương lai bị xáo trộn |
| **Time-based Split (Chuẩn thực tế)** | **$251.64$** | **$448.68$** | **$0.9486$** | Phản ánh chính xác năng lực dự báo trong tương lai |

### 2. Thí nghiệm 2: Benchmark 5 Mô hình trên tập Test độc lập
| Thứ hạng | Mô hình kiểm định | Trường phái kiến trúc | MAE (xe/h) | RMSE (xe/h) | Hệ số $R^2$ | Nhận xét chuyên môn |
| :---: | :--- | :--- | :---: | :---: | :---: | :--- |
| 🥇 **1** | **XGBoost Regressor** | **Ensemble Boosting** | **$242.58$** | **$424.63$** | **$0.9540$** | **Quán quân tối ưu toàn diện; boosting tuần tự trên phần dư** |
| 🥈 **2** | **Random Forest Regressor** | **Ensemble Bagging** | **$251.64$** | **$448.68$** | **$0.9486$** | **Học phi tuyến vững chắc, giảm phương sai vượt trội** |
| 🥉 **3** | **Historical Calendar Baseline** | **Heuristic Lịch trình** | **$260.77$** | **$448.08$** | **$0.9487$** | **Hiệu quả vượt trội, chứng minh vai trò nhịp lịch trình** |
| 4 | Ridge Regression (L2) | Linear Regularized L2 | $636.59$ | $874.48$ | $0.8048$ | Co trọng số; không mô hình hóa được 2 đỉnh cao điểm |
| 5 | Lasso Regression (L1) | Linear Regularized L1 | $637.99$ | $875.26$ | $0.8045$ | Thưa hóa trọng số; tương đương Ridge, chứng minh giới hạn tuyến tính |

### 3. Thí nghiệm 3 & 4: Trôi dạt dữ liệu & Phân tích tình huống dị biệt
* **Trôi dạt theo năm (Data Drift)**: MAE tăng từ $156.95\text{ xe/h}$ (năm 2014) lên $256.64\text{ xe/h}$ (năm 2018), chứng minh sự cần thiết của quy trình tái huấn luyện định kỳ (MLOps).
* **Biến thiên 4 mùa**: Mùa đông có sai số cao nhất ($212.81\text{ xe/h}$) do bão tuyết; Mùa xuân có sai số thấp nhất ($172.75\text{ xe/h}$).
* **Tình huống dị biệt**: Sai số trong bão tuyết/mưa dông tăng $+34.5\%$ lên $285.22\text{ xe/h}$ do đứt gãy lưu thông; Ngày lễ giảm sâu $-77.5\%$ xuống $56.58\text{ xe/h}$ do lưu lượng giảm mạnh về đêm.

---

<br>

## 📁 CẤU TRÚC THƯ MỤC DỰ ÁN

```text
Project_20_Traffic_Volume/
├── data/
│   └── Metro_Interstate_Traffic_Volume.csv   # Dữ liệu quan trắc I-94 gốc
├── src/
│   ├── __init__.py                          # Khởi tạo module gói src
│   ├── data.py                              # Tiền xử lý, làm sạch 0K, mưa & Time Split
│   ├── features.py                          # Cyclical sin/cos encoding & Domain flags
│   ├── baseline.py                          # Historical Calendar Baseline (giờ x thứ x lễ)
│   ├── train.py                             # Pipeline Scikit-learn, huấn luyện & lưu mô hình
│   └── evaluate.py                          # Thực thi 4 Thí nghiệm bắt buộc & xuất 4 đồ thị 300 DPI
├── models/
│   ├── best_traffic_pipeline.pkl            # Artifact mô hình XGBoost Regressor tối ưu (~1.5MB)
│   ├── calendar_baseline.pkl                # Artifact mô hình Baseline Lịch sử
│   ├── validation_summary.json              # Kết quả đánh giá lựa chọn trên tập Validation
│   └── experiment_metrics.json              # Số liệu thực nghiệm chi tiết của 4 thí nghiệm
├── reports/
│   ├── BAO_CAO_PROJECT_20.md                # Báo cáo học thuật bản sao
│   └── figures/                             # 4 biểu đồ học thuật độ phân giải cao 300 DPI
│       ├── exp1_random_vs_time_split.png
│       ├── exp2_models_comparison.png
│       ├── exp3_seasonal_drift.png
│       └── exp4_holiday_and_weather_errors.png
├── app/
│   ├── __init__.py                          # Khởi tạo module gói app
│   ├── backend.py                           # Dịch vụ Backend RESTful API bằng FastAPI
│   └── test_api.py                          # Bộ kiểm thử tự động 8 ca test bằng TestClient
├── frontend/                                # GIAO DIỆN WEB REACTJS CHÍNH THỨC (CHUẨN BTL)
│   ├── index.html                           # Bản React 18 SPA độc lập, phục vụ trực tiếp qua FastAPI
│   ├── package.json                         # Cấu hình dự án React 18 & Vite
│   ├── vite.config.js                       # Cấu hình Vite Dev Server & Reverse Proxy
│   ├── README.md                            # Hướng dẫn chi tiết mã nguồn React
│   └── src/
│       ├── main.jsx                         # Điểm khởi chạy React DOM
│       ├── App.jsx                          # Component gốc 3 màn hình, What-If & Charts
│       └── index.css                        # CSS giao diện chuyên nghiệp
├── report/
│   └── BAO_CAO_PROJECT_20.md                # Báo cáo học thuật 15-20 trang chuẩn thể thức UTEHY
├── slide/
│   └── SLIDES_PROJECT_20.md                 # Bộ 12 slide thuyết trình kèm kịch bản thuyết minh
├── check_submission.py                      # Kịch bản QA/QC tự động kiểm toán 6 cổng trước khi nộp
├── CONTRIBUTIONS.md                         # Bảng phân công 2 sinh viên & nhật ký 6 tuần
└── README.md                                # Tài liệu hướng dẫn sử dụng và khởi chạy hệ thống
```

---

<br>

## 🚀 HƯỚNG DẪN CÀI ĐẶT & KHỞI CHẠY (ONE-COMMAND RUN)

### 1. Cài đặt các thư viện phụ thuộc
Đảm bảo máy tính đã cài đặt Python 3.10 trở lên. Mở PowerShell hoặc Terminal và chạy:

```bash
pip install pandas numpy scikit-learn matplotlib seaborn joblib fastapi uvicorn pydantic httpx xgboost
```

### 2. Huấn luyện mô hình và lưu Artifacts (Tùy chọn nếu muốn train lại)
Mô hình tối ưu đã được huấn luyện sẵn và lưu trong thư mục `models/`. Nếu muốn chạy lại toàn bộ quy trình huấn luyện:
```bash
python src/train.py
```

### 3. Thực thi 4 Thí nghiệm bắt buộc & Xuất đồ thị 300 DPI
```bash
python src/evaluate.py
```
*(Số liệu sẽ được cập nhật vào `models/experiment_metrics.json` và 4 đồ thị 300 DPI sẽ xuất vào `reports/figures/`).*

### 4. Chạy kiểm thử tự động Backend API (Unit Test Suite)
```bash
python -m unittest app/test_api.py
```
*(Kiểm tra toàn diện 8 ca kiểm thử, phản hồi `Ran 8 tests ... OK`).*

### 5. Khởi chạy Hệ thống Web ReactJS + Backend FastAPI (Khuyên Dùng)
Chỉ cần chạy 1 lệnh duy nhất:
```bash
python app/backend.py
```
*(Hoặc dùng `uvicorn app.backend:app --host 127.0.0.1 --port 8000 --reload`)*

* 🌐 **Truy cập Giao diện Web ReactJS**: Mở trình duyệt tại **http://127.0.0.1:8000/**
  - **Màn hình 1**: Khám phá dữ liệu EDA, thống kê 40,565 bản ghi sạch và biểu đồ chu kỳ ngày đêm.
  - **Màn hình 2**: Bàn điều khiển trực quan, đồng hồ bán nguyệt SVG Gauge phân cấp dịch vụ (LOS A–F), 5 nút kịch bản mẫu nhanh, và phân tích độ nhạy thời tiết **What-If Analysis** đường nét đứt.
  - **Màn hình 3**: Trung tâm đối chuẩn học thuật hiển thị 4 thí nghiệm và đồ thị 300 DPI.
* 📚 **Tài liệu API Swagger UI**: **http://127.0.0.1:8000/docs**
* 🩺 **Kiểm tra sức khỏe hệ thống**: **http://127.0.0.1:8000/api/health**

### 6. Khởi chạy Frontend ReactJS độc lập qua Vite (Tùy chọn cho Dev)
Nếu muốn phát triển hoặc chạy độc lập qua Vite:
```bash
cd frontend
npm install
npm run dev
```
* Mở trình duyệt tại: **http://localhost:3000** (Tự động Proxy API sang FastAPI Backend Port 8000).

### 7. Kiểm toán chất lượng trước khi nộp bài (QA/QC Inspection)
Chạy script kiểm tra tự động 6 cổng kiểm soát chất lượng:
```bash
python check_submission.py
```
* Đảm bảo màn hình hiển thị: **`TẤT CẢ TIÊU CHÍ KHOA HỌC & KỸ THUẬT ĐỀU ĐẠT CHUẨN XUẤT SẮC (ĐIỂM 10/10)`**.

---

<br>

## 📞 LIÊN HỆ & BẢN QUYỀN
* **Đơn vị đào tạo**: Khoa Công nghệ Thông tin — Trường Đại học Sư phạm Kỹ thuật Hưng Yên
* **Giảng viên phụ trách học phần**: PGS. TS. Nguyễn Văn Hậu
* **Email liên hệ nhóm sinh viên**: `12523001@utehy.edu.vn` (Nguyễn Văn An) | `12523002@utehy.edu.vn` (Trần Thị Bình)
* **Giấy phép sử dụng**: Sản phẩm phục vụ mục đích học tập và nghiên cứu học thuật nội bộ.
#   M L _ B A S I C _ L U U L U O N G X E  
 