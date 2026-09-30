# BẢNG PHÂN CÔNG NHIỆM VỤ & NHẬT KÝ TIẾN ĐỘ ĐỒ ÁN 6 TUẦN
## PROJECT 20: DỰ BÁO LƯU LƯỢNG GIAO THÔNG VỚI CHIA TẬP THEO THỜI GIAN
### (METRO INTERSTATE TRAFFIC VOLUME FORECASTING WITH CHRONOLOGICAL TIME SPLIT)

**Học phần**: Học máy cơ bản (Machine Learning Fundamentals) — **Lớp**: 12523W.1  
**Giảng viên hướng dẫn**: PGS. TS. Nguyễn Văn Hậu  
**Khoa Công nghệ Thông tin — Trường Đại học Sư phạm Kỹ thuật Hưng Yên (UTEHY)**  
**Nhóm sinh viên thực hiện**:  
1. **Nguyễn Văn An** — Mã sinh viên: **12523001** (Nhóm trưởng)  
2. **Trần Thị Bình** — Mã sinh viên: **12523002** (Thành viên)  

---

## 👥 1. BẢNG TỔNG QUAN PHÂN CÔNG TRÁCH NHIỆM (TỶ LỆ 50% — 50%)

| Tiêu chí | Nguyễn Văn An (MSV: 12523001 - Nhóm trưởng) | Trần Thị Bình (MSV: 12523002 - Thành viên) |
| :--- | :--- | :--- |
| **Phần Dữ liệu & Tiền xử lý** | - Cấu trúc dữ liệu, kiểm toán lỗi cảm biến & Chia tập thời gian (`src/data.py`)<br>- Lập hồ sơ dữ liệu chuẩn (`data/README.md`) | - Tiếp nhận dữ liệu sạch, thiết kế mô hình đối chuẩn cơ sở (`src/baseline.py`)<br>- Tính toán kỳ vọng Fallback theo lịch trình xã hội |
| **Phần Kỹ nghệ Đặc trưng & Mô hình** | - Thiết kế bộ biến đổi lượng giác $\sin/\cos$ & cờ ngữ cảnh (`src/features.py`)<br>- Tích hợp Transformer chuẩn Scikit-learn | - Xây dựng Scikit-learn Pipeline khép kín & Huấn luyện 4 mô hình (`src/train.py`)<br>- Lựa chọn mô hình tối ưu trên tập Validation & Lưu Artifacts |
| **Phần Thực nghiệm & Đánh giá** | - Cấu hình đồ họa Matplotlib/Seaborn xuất 4 biểu đồ 300 DPI (`reports/figures/`)<br>- Lưu trữ số liệu JSON (`models/experiment_metrics.json`) | - Lập trình thực thi trọn vẹn 4 Thí nghiệm bắt buộc (`src/evaluate.py`)<br>- Phân tích Data Leakage, Benchmark, Data Drift & Sai số dị biệt |
| **Phần Triển khai Phần mềm** | - Xây dựng Backend RESTful API bằng FastAPI (`app/backend.py`)<br>- Thiết kế Pydantic Schemas & Bộ bảo vệ Out-of-Domain Guard | - Xây dựng Giao diện Web Frontend ReactJS 18 Decoupled (`frontend/`)<br>- Thiết kế 3 màn hình, đồng hồ SVG Gauge LOS A-F & What-If Weather |
| **Phần Đảm bảo Chất lượng & Bàn giao**| - Bộ kiểm thử tự động API 9 ca test (`app/test_api.py`)<br>- Kịch bản kiểm toán 6 cổng QA/QC tự động (`check_submission.py`) | - Thiết kế bộ Slide báo cáo 12 trang chuẩn (`slide/SLIDES_PROJECT_20.md`)<br>- Soạn kịch bản thuyết minh chi tiết từng slide (Speaker Notes) |
| **Phần Báo cáo Học thuật UTEHY** | - Soạn thảo Chương 1 (Tổng quan, Bối cảnh, 2 Câu hỏi nghiên cứu)<br>- Soạn thảo Chương 2 (EDA, Kiểm toán lỗi dữ liệu & Chia thời gian)<br>- Soạn thảo Chương 5 (Kiến trúc hệ thống, Backend API & Bảo vệ) | - Soạn thảo Chương 3 (Đặc trưng lượng giác, Baseline & Pipeline)<br>- Soạn thảo Chương 4 (Bảng kết quả & Phân tích sâu 4 Thí nghiệm)<br>- Soạn thảo Chương 6 (Bài học, Đạo đức AI & Trả lời 3 câu hỏi vấn đáp) |
| **Tỷ lệ đóng góp công việc** | **50% (Đóng góp bình đẳng, thực chất)** | **50% (Đóng góp bình đẳng, thực chất)** |
| **Mức tự đánh giá hoàn thành** | **A+ (Xuất sắc — Điểm 10/10)** | **A+ (Xuất sắc — Điểm 10/10)** |

---

## 🔍 2. CHI TIẾT NHIỆM VỤ TỪNG CẤU TRÚC VÀ LUỒNG CHUYỂN GIAO CÔNG VIỆC

### 👨‍💻 A. CHI TIẾT NHIỆM VỤ CỦA NGUYỄN VĂN AN (MSV: 12523001)

#### 1. Phụ trách cấu trúc dữ liệu và tiền xử lý chống rò rỉ (`src/data.py` & `data/README.md`):
* **Nội dung công việc đã thực hiện**:
  * Tiếp nhận dữ liệu thô `Metro_Interstate_Traffic_Volume.csv` (48,204 dòng) từ trạm MN DoT ATR 301 (hướng Tây — Westbound) trên cao tốc I-94.
  * Viết hàm `load_and_clean_traffic_data()` thực hiện kiểm toán và làm sạch:
    * Phát hiện và chuẩn hóa 61 mốc ngày lễ liên bang Hoa Kỳ, gán `'None'` cho các ô trống.
    * Sửa lỗi phần cứng cảm biến: Lọc bỏ/thay thế 10 bản ghi nhiệt độ $0.0\text{ Kelvin}$ (-273.15°C phi vật lý) bằng trung vị nhiệt độ của tháng lịch sử tương ứng.
    * Cắt tỉa (clip) ngoại lệ lượng mưa cực đoan $9,831.3\text{ mm/h}$ ngày 11/07/2016 do tràn cảm biến về ngưỡng an toàn $100.0\text{ mm/h}$.
    * Khử trùng lặp 7,629 mốc giờ bị lặp do trạm khí tượng ghi nhận đa trạng thái thời tiết, giữ lại bản ghi quan trắc đầu tiên, đưa về $40,565$ bản ghi sạch duy nhất.
  * Viết hàm `split_traffic_data()`: Hiện thực hóa chiến lược phân chia theo trục thời gian xuôi dòng (Chronological Time Split) 70% Train ($28,395$ dòng) $\rightarrow$ 15% Validation ($6,085$ dòng) $\rightarrow$ 15% Test ($6,085$ dòng niêm phong), bổ sung assert kiểm tra $\max(\text{Train}) < \min(\text{Val}) < \min(\text{Test})$ để chống rò rỉ dữ liệu tự tương quan (Bài 7).
  * Viết hàm `create_random_split_for_exp1()` xáo trộn ngẫu nhiên phục vụ Thí nghiệm 1 đối chứng.
  * Biên soạn tệp hồ sơ dữ liệu [data/README.md](data/README.md) đầy đủ Data dictionary 9 biến, bản quyền CC BY 4.0, DOI: 10.24432/C5X60B, mã băm SHA-256 và script tải tự động.
* **Xong công việc này thì làm gì tiếp theo?**:
  * Đóng gói bộ dữ liệu sạch và các tập dữ liệu phân chia, chuyển giao cho **Trần Thị Bình** để bạn bắt đầu tính toán mô hình cơ sở lịch sử trong `src/baseline.py`.
  * Đồng thời, An chuyển sang thực hiện nhiệm vụ tiếp theo là thiết kế bộ trích xuất đặc trưng chuỗi thời gian trong `src/features.py`.

---

#### 2. Phụ trách đổi mới trích xuất đặc trưng chu kỳ lượng giác (`src/features.py`):
* **Nội dung công việc đã thực hiện**:
  * Xây dựng lớp tùy biến `TrafficFeatureEngineer(BaseEstimator, TransformerMixin)` tương thích chuẩn Scikit-learn.
  * Giải quyết bài toán đứt gãy biên thời gian giữa 23h đêm và 0h sáng thông qua phép chiếu hình học lượng giác:
    $$\sin\text{\_hour} = \sin\left(\frac{2\pi \cdot \text{hour}}{24}\right), \quad \cos\text{\_hour} = \cos\left(\frac{2\pi \cdot \text{hour}}{24}\right)$$
    $$\sin\text{\_month} = \sin\left(\frac{2\pi \cdot (\text{month}-1)}{12}\right), \quad \cos\text{\_month} = \cos\left(\frac{2\pi \cdot (\text{month}-1)}{12}\right)$$
  * Trích xuất các cờ ngữ cảnh giao thông chuyên ngành (Domain Flags): `is_rush_hour` (giờ cao điểm 7h–9h và 16h–18h các ngày trong tuần), `is_weekend` (thứ Bảy, Chủ Nhật), `is_holiday` (ngày lễ).
  * Phân định rõ 3 danh mục đặc trưng: `NUMERIC_FEATURES`, `CATEGORICAL_FEATURES`, `BINARY_FEATURES`.
* **Xong công việc này thì làm gì tiếp theo?**:
  * Bàn giao module `src/features.py` cho **Trần Thị Bình** tích hợp làm bước biến đổi đầu tiên trong Pipeline Scikit-learn (`src/train.py`).
  * Sau khi chuyển giao, An bắt tay vào thiết kế kiến trúc Backend API phục vụ suy luận thời gian thực trong `app/backend.py`.

---

#### 3. Phụ trách Backend RESTful API & Bộ bảo vệ Out-of-Domain Guard (`app/backend.py`):
* **Nội dung công việc đã thực hiện**:
  * Xây dựng dịch vụ Backend API bằng FastAPI chuẩn công nghiệp với kiến trúc phục vụ suy luận trực tuyến.
  * Ứng dụng cơ chế `lifespan` context manager: nạp sẵn Pipeline mô hình tối ưu (`models/best_traffic_pipeline.pkl`) vào RAM một lần duy nhất khi khởi động, giảm thiểu độ trễ suy luận xuống mức $< 15\text{ ms}$, tách rời hoàn toàn quá trình huấn luyện offline khỏi quá trình phục vụ trực tuyến.
  * Định nghĩa các Pydantic v2 Schemas chặt chẽ: `TrafficForecastRequest`, `TrafficForecastResponse`, `Simulation24hRequest`, `Simulation24hResponse`.
  * Xây dựng bộ lọc bảo vệ dữ liệu lệch miền **Out-of-Domain Guard**: tự động bắt lỗi nhập nhầm độ C thay vì Kelvin ($0 \le \text{temp} \le 50$), cảnh báo mưa cực đoan $> 50\text{ mm/h}$ hoặc bão tuyết $> 15\text{ mm/h}$, trả về cảnh báo minh bạch trong `warnings`.
  * Triển khai hàm `classify_congestion()` phân cấp dịch vụ đường cao tốc (Level of Service: LOS A đến F) theo chuẩn thiết kế đường bộ Hoa Kỳ.
  * Cung cấp các endpoint: `GET /api/health`, `GET /api/model-card`, `GET /api/experiments`, `POST /api/traffic-forecast`, `POST /api/traffic-forecast-24h` và mount phục vụ Frontend tĩnh.
* **Xong công việc này thì làm gì tiếp theo?**:
  * Cung cấp tài liệu Swagger UI (`/docs`) và đặc tả giao diện kết nối API cho **Trần Thị Bình** để bạn đấu nối trực tiếp vào giao diện Web Frontend ReactJS.
  * Đồng thời, An chuyển sang viết bộ kiểm thử tự động API trong `app/test_api.py` và kịch bản QA/QC `check_submission.py`.

---

#### 4. Phụ trách kiểm thử tự động & Kịch bản kiểm toán QA/QC (`app/test_api.py` & `check_submission.py`):
* **Nội dung công việc đã thực hiện**:
  * Viết bộ kiểm thử hồi quy tự động trong `app/test_api.py` gồm 9 ca test toàn diện với `TestClient`: kiểm tra sức khỏe hệ thống, model-card, dự báo hợp lệ, cảnh báo Out-of-Domain, lỗi Pydantic 422, mô phỏng 24h, endpoint thực nghiệm và trang gốc React root (đạt tỷ lệ 100% PASS).
  * Lập trình kịch bản tự động kiểm toán chất lượng đồ án trước khi nộp bài [check_submission.py](check_submission.py) với 6 cổng kiểm soát chất lượng (6 Gates):
    * *Gate 1*: Kiểm tra đầy đủ 25 tệp tin bắt buộc của dự án.
    * *Gate 2*: Quét sạch 100% mã nguồn không để sót đường dẫn cứng tuyệt đối.
    * *Gate 3*: Kiểm toán tính toàn vẹn chuỗi thời gian, xác minh không rò rỉ dữ liệu giữa Train, Val và Test.
    * *Gate 4*: Kiểm định suy luận thực tế của Pipeline mô hình tối ưu.
    * *Gate 5*: Chạy tự động test suite của API Backend.
    * *Gate 6*: Thẩm định các chỉ số thực nghiệm vượt chuẩn học thuật ($R^2 \ge 0.90, MAE \le 300\text{ xe/h}$).
* **Xong công việc này thì làm gì tiếp theo?**:
  * Thực thi kịch bản nghiệm thu kiểm tra chéo toàn bộ mã nguồn của cả hai người.
  * Sau khi đảm bảo hệ sinh thái kỹ thuật hoạt động hoàn hảo, An chuyển sang soạn thảo các chương lý thuyết, bối cảnh và kiến trúc trong Báo cáo học thuật (Chương 1, 2, 5) và hoàn thiện tệp `requirements.txt`, `README.md`.

---

#### 5. Phụ trách Báo cáo học thuật Chương 1, 2, 5 & Hướng dẫn sử dụng (`README.md`, `requirements.txt`):
* **Nội dung công việc đã thực hiện**:
  * Soạn thảo **Chương 1**: Đặt vấn đề trong hệ thống ITS, giới thiệu tuyến cao tốc I-94 tại trạm ATR 301, làm rõ 2 câu hỏi nghiên cứu cốt lõi và phân tích bản chất rò rỉ dữ liệu do tự tương quan.
  * Soạn thảo **Chương 2**: Thống kê cấu trúc bộ dữ liệu, bản quyền CC BY 4.0, DOI, quá trình kiểm toán 3 lỗi cảm biến (0K, mưa, trùng mốc) và chiến lược phân chia theo thời gian 70-15-15.
  * Soạn thảo **Chương 5**: Thiết kế kiến trúc tổng thể Multi-tier, chi tiết Backend FastAPI, Pydantic schemas, cơ chế Out-of-Domain Guard và kết quả chạy Unit Test Suite.
  * Soạn thảo tệp [requirements.txt](requirements.txt) chuẩn hóa môi trường và [README.md](README.md) hướng dẫn khởi chạy nhanh bằng một câu lệnh duy nhất.
* **Xong công việc này thì làm gì tiếp theo?**:
  * Hợp nhất các chương của An với các chương do Bình soạn thảo, kiểm tra tính mạch lạc toàn bài, biên dịch sang tệp Microsoft Word [report/BAO_CAO_PROJECT_20.docx](report/BAO_CAO_PROJECT_20.docx) chuẩn thể thức và cùng Bình chuẩn bị kịch bản phản biện vấn đáp trước Hội đồng chấm thi.

---

### 👩‍💻 B. CHI TIẾT NHIỆM VỤ CỦA TRẦN THỊ BÌNH (MSV: 12523002)

#### 1. Phụ trách Mô hình đối chuẩn cơ sở theo lịch trình (`src/baseline.py`):
* **Nội dung công việc đã thực hiện**:
  * Tiếp nhận dữ liệu sạch và các tập phân chia Train, Validation, Test từ **Nguyễn Văn An**.
  * Xây dựng lớp `HistoricalCalendarBaseline(BaseEstimator, RegressorMixin)` chuẩn Scikit-learn.
  * Lập trình thuật toán học bảng tra cứu kỳ vọng có điều kiện theo lịch sinh hoạt xã hội:
    $$\hat{y}_{\text{baseline}}(h, d, hol) = \mathbb{E}\big[y \mid \text{hour} = h, \text{dayofweek} = d, \text{is\_holiday} = hol\big]$$
    chỉ tính toán thuần túy trên $28,395$ mẫu của tập Train.
  * Thiết kế cơ chế dự phòng phân tầng 4 cấp (Hierarchical Fallback):
    $$\text{Hour}\times\text{Day}\times\text{Holiday} \longrightarrow \text{Hour}\times\text{Day} \longrightarrow \text{Hour} \longrightarrow \text{Global Mean}$$
    đảm bảo không bị lỗi khi gặp các tổ hợp mới chưa từng xuất hiện.
  * Đánh giá mô hình trên tập Validation: đạt MAE ấn tượng $260.77\text{ xe/h}$ và lưu vào `models/calendar_baseline.pkl`.
* **Xong công việc này thì làm gì tiếp theo?**:
  * Xác lập mốc đối chuẩn tối thiểu (Performance Floor) mà các mô hình học máy bắt buộc phải vượt qua.
  * Chuyển sang phối hợp với An để lấy lớp `TrafficFeatureEngineer` và bắt đầu xây dựng Scikit-learn Pipeline trong `src/train.py`.

---

#### 2. Phụ trách Scikit-learn Pipeline, Huấn luyện & Lựa chọn mô hình (`src/train.py`):
* **Nội dung công việc đã thực hiện**:
  * Viết hàm `build_preprocessing_pipeline()`: Kết hợp `StandardScaler` cho các đặc trưng số và biến lượng giác $\sin/\cos$, `OneHotEncoder(handle_unknown='ignore')` cho biến phân loại, và `passthrough` cho biến cờ nhị phân.
  * Viết hàm `build_full_pipeline()` ghép nối hoàn chỉnh: `TrafficFeatureEngineer` $\rightarrow$ `ColumnTransformer` $\rightarrow$ `Model Regressor`.
  * Huấn luyện và theo dõi hiệu năng của 4 trường phái thuật toán trên tập Train:
    1. *Ridge Regression (L2)*: Mô hình tuyến tính điều hòa bậc hai cơ bản.
    2. *Lasso Regression (L1)*: Mô hình tuyến tính điều hòa bậc một thưa hóa trọng số.
    3. *Random Forest Regressor*: Mô hình học tập hợp biểu quyết đa cây Bagging (100 cây, max_depth=15).
    4. *XGBoost Regressor*: Mô hình tăng cường độ dốc Extreme Gradient Boosting (150 cây, max_depth=6).
  * Đo lường bộ 3 chỉ số $MAE, RMSE, R^2$ trên tập Validation độc lập để lựa chọn mô hình tối ưu.
  * Lưu trữ Artifacts: Lưu mô hình tối ưu vào `models/best_traffic_pipeline.pkl` và bảng tổng kết vào `models/validation_summary.json`.
* **Xong công việc này thì làm gì tiếp theo?**:
  * Bàn giao tệp mô hình đã lưu `best_traffic_pipeline.pkl` cho **Nguyễn Văn An** nạp vào dịch vụ Backend API.
  * Bình chuyển sang nhiệm vụ trọng tâm tiếp theo là thiết kế và thực thi 4 thí nghiệm bắt buộc trong `src/evaluate.py`.

---

#### 3. Phụ trách thực thi 4 Thí nghiệm bắt buộc & Xuất biểu đồ 300 DPI (`src/evaluate.py`):
* **Nội dung công việc đã thực hiện**:
  * Lập trình module `src/evaluate.py` thực hiện trọn vẹn 4 thí nghiệm bắt buộc theo Đề cương của Thầy Nguyễn Văn Hậu:
    * **Thí nghiệm 1 (Random Split vs. Time Split)**: Chứng minh việc chia ngẫu nhiên gây rò rỉ dữ liệu qua các giờ liền kề, tạo ảo giác lạc quan; trong khi Time Split phản ánh đúng năng lực dự báo tương lai.
    * **Thí nghiệm 2 (Benchmark Baseline vs. Các mô hình)**: Lập bảng xếp hạng 5 mô hình trên tập Test độc lập; chứng minh Random Forest (MAE $251.64$) và XGBoost (MAE $242.58$) vượt trội hoàn toàn so với Baseline lịch ($260.77$) và Ridge ($636.59$).
    * **Thí nghiệm 3 (Hiện tượng Data Drift theo năm và theo mùa)**: Phân tích sự suy giảm hiệu năng theo thời gian từ 2012 ($156.95\text{ xe/h}$) đến 2018 ($256.64\text{ xe/h}$) do biến đổi mật độ xe; chỉ ra mùa đông có sai số cao nhất ($212.81\text{ xe/h}$) do bão tuyết.
    * **Thí nghiệm 4 (Phân tích sai số dị biệt)**: Bóc tách phân bố phần dư tâm 0; chỉ ra sai số giảm $-77.5\%$ trong ngày lễ do đường vắng và tăng $+34.5\%$ trong bão tuyết do ùn ứ cục bộ.
  * Cấu hình thư viện xuất bản 4 tệp đồ thị học thuật $300\text{ DPI}$ vào `reports/figures/` và xuất toàn bộ số liệu vào `models/experiment_metrics.json`.
* **Xong công việc này thì làm gì tiếp theo?**:
  * Bàn giao số liệu và biểu đồ thực nghiệm cho An đưa vào API `/api/experiments`.
  * Sau đó, Bình chuyển sang hiện thực hóa giao diện Web Frontend ReactJS 18 trong thư mục `frontend/`.

---

#### 4. Phụ trách xây dựng Giao diện Web Frontend ReactJS 18 (`frontend/`):
* **Nội dung công việc đã thực hiện**:
  * Xây dựng ứng dụng Single Page Application (SPA) chuẩn React 18, HTML5, CSS3 và Chart.js.
  * Thiết kế kiến trúc 3 màn hình nghiệp vụ trực quan:
    * **Màn hình 1 (Khám phá dữ liệu EDA & Giới thiệu)**: Thống kê 40,565 bản ghi sạch, biểu đồ tương tác phân bố 2 đỉnh giờ cao điểm, giới thiệu trạm MN DoT ATR 301 hướng Tây.
    * **Màn hình 2 (Thao tác chính & Mô phỏng)**: Form nhập thông số khí tượng, đồng hồ đo bán nguyệt SVG Gauge trực quan phân cấp dịch vụ (LOS A–F), 5 nút kịch bản mẫu nhanh và tính năng **What-If Analysis** đường nét đứt dự báo thay đổi lưu lượng khi có bão tuyết.
    * **Màn hình 3 (Trung tâm đối chuẩn học thuật & Model Card)**: Hiển thị bảng số liệu chi tiết 4 thí nghiệm và nhúng trực tiếp 4 đồ thị học thuật 300 DPI kèm thẻ đặc tả Model Card.
  * Kết nối trực tiếp các REST API từ Backend FastAPI (`/api/health`, `/api/traffic-forecast`, `/api/traffic-forecast-24h`, `/api/experiments`, `/api/model-card`).
* **Xong công việc này thì làm gì tiếp theo?**:
  * Kiểm thử giao diện trên các độ phân giải màn hình, đảm bảo khả năng phản hồi mượt mà dưới $50\text{ ms}$.
  * Sau khi hoàn thành Web, Bình chuyển sang viết các chương học thuật tương ứng trong Báo cáo (Chương 3, 4, 6), soạn câu trả lời vấn đáp và thiết kế Bộ Slide 12 trang.

---

#### 5. Phụ trách Báo cáo Chương 3, 4, 6, Trả lời vấn đáp & Bộ Slide 12 trang (`SLIDES_PROJECT_20.md`):
* **Nội dung công việc đã thực hiện**:
  * Soạn thảo **Chương 3**: Phương pháp mã hóa lượng giác $\sin/\cos$, thuật toán Historical Calendar Baseline với Fallback và kiến trúc Pipeline Scikit-learn.
  * Soạn thảo **Chương 4**: Trình bày chi tiết phương pháp luận, kết quả số liệu và phân tích chuyên môn sâu sắc của 4 thí nghiệm bắt buộc kèm biểu đồ minh họa.
  * Soạn thảo **Chương 6**: Tổng kết kết quả, bài học kinh nghiệm chuỗi thời gian, tuyên bố đạo đức và sử dụng có trách nhiệm (Responsible AI Disclaimer), cùng định hướng MLOps.
  * Biên soạn câu trả lời khoa học chi tiết cho **3 câu hỏi vấn đáp trọng tâm** của Thầy Nguyễn Văn Hậu (Mục 6.5 Báo cáo).
  * Thiết kế Bộ **Slide báo cáo 12 trang chuẩn** trong [slide/SLIDES_PROJECT_20.md](slide/SLIDES_PROJECT_20.md) kèm kịch bản thuyết minh chi tiết cho từng trang slide (Speaker Notes) căn chỉnh thời lượng 8–10 phút thuyết trình.
* **Xong công việc này thì làm gì tiếp theo?**:
  * Ghép nối nội dung với An để xuất bản tệp Báo cáo chính thức [report/BAO_CAO_PROJECT_20.md](report/BAO_CAO_PROJECT_20.md) và [report/BAO_CAO_PROJECT_20.docx](report/BAO_CAO_PROJECT_20.docx).
  * Hai sinh viên cùng tiến hành tổng duyệt (Dry-run rehearsal) toàn bộ bài thuyết trình và chuẩn bị bảo vệ đồ án trước Thầy Nguyễn Văn Hậu.

---

## 📅 3. NHẬT KÝ TIẾN ĐỘ CHI TIẾT THEO TỪNG TUẦN (6-WEEK SPRINT LOG)

```
       QUY TRÌNH PHỐI HỢP LIÊN TỤC 6 TUẦN GIỮA NGUYỄN VĂN AN VÀ TRẦN THỊ BÌNH
TUẦN 1: Nghiên cứu đề tài, khảo sát tự tương quan chuỗi thời gian & chống rò rỉ dữ liệu
TUẦN 2: [An] Kiểm toán làm sạch dữ liệu thô (src/data.py)  ──► [Bình] Thiết kế Time Split 70-15-15
TUẦN 3: [An] Trích xuất lượng giác sin/cos (src/features.py) ──► [Bình] Thiết kế Calendar Baseline (src/baseline.py)
TUẦN 4: [Bình] Huấn luyện Pipeline 4 mô hình (src/train.py)  ──► [An] Đóng gói & Lưu trữ Artifacts (models/)
TUẦN 5: [Bình] Thực thi 4 Thí nghiệm bắt buộc (src/evaluate.py)──► [An] Xuất đồ thị 300 DPI & Đồng bộ JSON
TUẦN 6: [An] FastAPI Backend & 6 Cổng QA/QC (backend.py)   ──► [Bình] React 18 Web & Slide 12 trang (frontend/)
        └──► [Cả 2] Hợp nhất Báo cáo học thuật 6 Chương, Slide thuyết minh & Tổng duyệt đồ án
```

### 🔹 TUẦN 1: TIẾP NHẬN ĐỀ TÀI, PHÂN TÍCH YÊU CẦU & THỐNG NHẤT PHƯƠNG PHÁP
* **Thời gian thực hiện**: Tuần 1 (Ước tính: 15 giờ/người).
* **Công việc của Nguyễn Văn An**:
  * Đọc kỹ tài liệu giao nhiệm vụ `Project_20_du_bao_luu_luong_giao_thong.docx` của PGS.TS. Nguyễn Văn Hậu.
  * Tải và khảo sát sơ bộ tệp dữ liệu thô `Metro_Interstate_Traffic_Volume.csv` từ UCI Repository.
  * Nghiên cứu lý thuyết Bài 7 về nguy cơ rò rỉ dữ liệu (Data Leakage) khi dùng hàm chia ngẫu nhiên thông thường trên chuỗi thời gian.
  * *Làm xong chuyển giao*: Lập biên bản phân tích bài toán và thống nhất kiến trúc tổng thể của đề tài với Bình.
* **Công việc của Trần Thị Bình**:
  * Nghiên cứu các chỉ số đo lường hiệu năng hồi quy chuỗi thời gian: $MAE, RMSE, R^2$.
  * Khảo sát các tài liệu khoa học về tính tự tương quan (Autocorrelation) trong giao thông cao tốc Mỹ.
  * Đề xuất phương án đối chuẩn bằng mô hình lịch trình xã hội thay vì dùng giá trị trung bình phẳng.
  * *Làm xong chuyển giao*: Lập kế hoạch 4 thí nghiệm thực nghiệm bắt buộc cần triển khai theo yêu cầu của Thầy.
* **Khó khăn phát sinh & Cách giải quyết**: Nhận thấy dữ liệu có nhiều mốc giờ bị lặp lại; nhóm thống nhất cần kiểm toán kỹ lưỡng trong Tuần 2 trước khi đưa vào huấn luyện.
* **Sản phẩm đầu ra Tuần 1**: Bản tóm tắt yêu cầu đề tài (Project Brief), danh mục rủi ro rò rỉ dữ liệu và kế hoạch phân công công việc.

---

### 🔹 TUẦN 2: LÀM SẠCH DỮ LIỆU CẢM BIẾN & THIẾT KẾ CHIA TẬP CHUỖI THỜI GIAN
* **Thời gian thực hiện**: Tuần 2 (Ước tính: 18 giờ/người).
* **Công việc của Nguyễn Văn An**:
  * Lập trình module [src/data.py](src/data.py) và hàm `load_and_clean_traffic_data()`.
  * Xử lý 10 lỗi cảm biến nhiệt độ $0.0\text{ K}$, cắt tỉa ngoại lệ mưa cực đoan $9,831.3\text{ mm/h}$ về $100\text{ mm/h}$, và khử trùng lặp 7,629 dòng trùng mốc `date_time`, đưa về $40,565$ bản ghi chuẩn.
  * Soạn thảo hồ sơ dữ liệu [data/README.md](data/README.md) đầy đủ từ điển dữ liệu và giấy phép CC BY 4.0.
  * *Làm xong chuyển giao*: Chuyển giao dữ liệu sạch dạng DataFrame cho Bình thiết lập tỷ lệ phân chia tập dữ liệu.
* **Công việc của Trần Thị Bình**:
  * Hiện thực hóa hàm `split_traffic_data()` theo phương pháp Chronological Time Split: 70% Train ($28,395$ dòng), 15% Validation ($6,085$ dòng) và 15% Test ($6,085$ dòng).
  * Viết mã kiểm tra tính đơn điệu của trục thời gian: bảo đảm không có bất kỳ mốc thời gian nào của Validation hoặc Test xuất hiện trong Train.
  * Niêm phong hoàn toàn tập Test để bảo vệ tính khách quan cho bước nghiệm thu cuối.
  * *Làm xong chuyển giao*: Cung cấp cấu trúc tập Train và Validation cho An để thiết kế các đặc trưng thời gian.
* **Khó khăn phát sinh & Cách giải quyết**: Có tranh luận nên xóa bỏ hay thay thế 10 dòng nhiệt độ 0K; nhóm thống nhất thay bằng trung vị tháng để bảo toàn tính liên tục của chuỗi thời gian.
* **Sản phẩm đầu ra Tuần 2**: Module `src/data.py` hoàn chỉnh, dữ liệu sạch 40,565 bản ghi và hồ sơ `data/README.md`.

---

### 🔹 TUẦN 3: ĐỔI MỚI TRÍCH XUẤT ĐẶC TRƯNG & THIẾT KẾ BASELINE LỊCH SỬ
* **Thời gian thực hiện**: Tuần 3 (Ước tính: 16 giờ/người).
* **Công việc của Nguyễn Văn An**:
  * Lập trình lớp `TrafficFeatureEngineer` trong [src/features.py](src/features.py).
  * Triển khai công thức mã hóa lượng giác $\sin/\cos$ cho giờ ($T=24$) và tháng ($T=12$), xóa bỏ đứt gãy biên giữa 23h và 0h sáng.
  * Tạo các đặc trưng ngữ cảnh giao thông: `is_rush_hour`, `is_weekend`, `is_holiday`.
  * *Làm xong chuyển giao*: Bàn giao bộ Transformer cho Bình tích hợp vào Pipeline học máy Scikit-learn.
* **Công việc của Trần Thị Bình**:
  * Lập trình lớp `HistoricalCalendarBaseline` trong [src/baseline.py](src/baseline.py).
  * Tính toán bảng tra cứu kỳ vọng $\mathbb{E}[y \mid \text{hour}, \text{dayofweek}, \text{is\_holiday}]$ thuần túy từ tập Train.
  * Xây dựng cơ chế dự phòng phân tầng 4 cấp (Fallback) để mô hình không bị lỗi khi gặp dữ liệu chưa từng thấy.
  * Đánh giá mô hình trên tập Validation (đạt MAE $260.77\text{ xe/h}$) và lưu vào `models/calendar_baseline.pkl`.
  * *Làm xong chuyển giao*: Bàn giao artifact Baseline để An dùng kiểm tra đối chuẩn.
* **Khó khăn phát sinh & Cách giải quyết**: Một số ngày lễ trong tập Test không xuất hiện trong tập Train; cơ chế Fallback phân tầng của Bình đã giải quyết triệt để vấn đề này.
* **Sản phẩm đầu ra Tuần 3**: Module `src/features.py`, `src/baseline.py` và tệp mô hình `models/calendar_baseline.pkl`.

---

### 🔹 TUẦN 4: THIẾT KẾ PIPELINE HỌC MÁY & HUẤN LUYỆN ĐỐI CHUẨN
* **Thời gian thực hiện**: Tuần 4 (Ước tính: 20 giờ/người).
* **Công việc của Trần Thị Bình**:
  * Lập trình module [src/train.py](src/train.py): Ghép nối `TrafficFeatureEngineer` $\rightarrow$ `ColumnTransformer` (`StandardScaler` + `OneHotEncoder`) $\rightarrow$ Model Regressor.
  * Huấn luyện 4 thuật toán: Ridge (L2), Lasso (L1), Random Forest và XGBoost.
  * Đánh giá và so sánh trên tập Validation: Random Forest và XGBoost đạt kết quả vượt trội, trong khi các mô hình tuyến tính thất bại trước Baseline.
  * *Làm xong chuyển giao*: Bàn giao pipeline mô hình chiến thắng cho An lưu trữ và tích hợp Backend.
* **Công việc của Nguyễn Văn An**:
  * Lưu trữ các Artifacts học máy vào thư mục `models/` (`best_traffic_pipeline.pkl`, `validation_summary.json`).
  * Kiểm toán Pipeline đảm bảo `StandardScaler` và `OneHotEncoder` chỉ được `.fit()` trên tập Train, hoàn toàn không nhìn trước tập Validation hay Test.
  * *Làm xong chuyển giao*: Chuyển giao cấu trúc Pipeline sạch cho Bình chuẩn bị kịch bản đánh giá 4 thí nghiệm.
* **Khó khăn phát sinh & Cách giải quyết**: Mô hình Random Forest ban đầu tốn nhiều bộ nhớ RAM; An và Bình thống nhất giới hạn `max_depth=15` và `n_estimators=100` để tối ưu tốc độ suy luận mà không giảm độ chính xác.
* **Sản phẩm đầu ra Tuần 4**: Module `src/train.py`, tệp `models/best_traffic_pipeline.pkl` và `models/validation_summary.json`.

---

### 🔹 TUẦN 5: THỰC THI 4 THÍ NGHIỆM BẮT BUỘC & XUẤT ĐỒ THỊ 300 DPI
* **Thời gian thực hiện**: Tuần 5 (Ước tính: 18 giờ/người).
* **Công việc của Trần Thị Bình**:
  * Lập trình module [src/evaluate.py](src/evaluate.py), thực thi trọn vẹn 4 thí nghiệm bắt buộc theo yêu cầu:
    * Thí nghiệm 1: So sánh Random Split vs Time Split.
    * Thí nghiệm 2: Đối chuẩn 5 mô hình trên tập Test độc lập (XGBoost đạt Quán quân với MAE $242.58$, Random Forest đạt MAE $251.64$).
    * Thí nghiệm 3: Đánh giá Data Drift theo năm và mùa.
    * Thí nghiệm 4: Phân tích thặng dư phần dư và sai số dị biệt ngày lễ, bão tuyết.
  * *Làm xong chuyển giao*: Bàn giao toàn bộ số liệu mảng và hàm vẽ cho An cấu hình xuất bản.
* **Công việc của Nguyễn Văn An**:
  * Thiết lập cấu hình trực quan hóa đồ họa học thuật với Matplotlib và Seaborn: Phông chữ chuẩn, tỷ lệ tương phản cao, độ phân giải xuất bản **300 DPI**.
  * Xuất bản 4 đồ thị chất lượng cao vào `reports/figures/` (`exp1_random_vs_time_split.png`, `exp2_models_comparison.png`, `exp3_seasonal_drift.png`, `exp4_holiday_and_weather_errors.png`).
  * Đồng bộ toàn bộ số liệu thống kê vào `models/experiment_metrics.json`.
  * *Làm xong chuyển giao*: Bàn giao các tệp hình ảnh và JSON cho Bình đưa vào giao diện Web và Báo cáo.
* **Khó khăn phát sinh & Cách giải quyết**: Sai số ngày lễ ban đầu bị hiểu nhầm là mô hình thông minh hơn; qua phân tích phần dư, nhóm làm rõ đó là do ngày lễ đường vắng nên biên độ sai số tuyệt đối co nhỏ lại.
* **Sản phẩm đầu ra Tuần 5**: Module `src/evaluate.py`, 4 tệp hình ảnh 300 DPI và tệp số liệu `models/experiment_metrics.json`.

---

### 🔹 TUẦN 6: PHẦN MỀM THỜI GIAN THỰC, BÁO CÁO HỌC THUẬT & NGHIỆM THU QA/QC
* **Thời gian thực hiện**: Tuần 6 (Ước tính: 22 giờ/người).
* **Công việc của Nguyễn Văn An**:
  * Lập trình dịch vụ Backend API bằng FastAPI [app/backend.py](app/backend.py) với `lifespan`, Pydantic v2 schemas và bộ bảo vệ Out-of-Domain Guard.
  * Viết bộ kiểm thử tự động [app/test_api.py](app/test_api.py) (9/9 ca test PASS 100%).
  * Lập trình kịch bản tự động kiểm toán 6 cổng chất lượng [check_submission.py](check_submission.py).
  * Soạn thảo Báo cáo học thuật: Chương 1, 2, 5 trong [report/BAO_CAO_PROJECT_20.md](report/BAO_CAO_PROJECT_20.md).
  * Biên soạn tệp [requirements.txt](requirements.txt) và [README.md](README.md).
  * *Làm xong chuyển giao*: Khởi chạy server API Backend tại port 8000 để Bình kết nối Frontend ReactJS.
* **Công việc của Trần Thị Bình**:
  * Xây dựng ứng dụng Web Frontend React 18 trong thư mục [frontend/](frontend/) với 3 màn hình tương tác cao, tích hợp đồng hồ SVG Gauge LOS A-F và tính năng What-If Weather sensitivity.
  * Đấu nối Frontend trực tiếp với Backend FastAPI qua các REST endpoints.
  * Soạn thảo Báo cáo học thuật: Chương 3, 4, 6 trong [report/BAO_CAO_PROJECT_20.md](report/BAO_CAO_PROJECT_20.md) và biên soạn câu trả lời cho 3 câu hỏi vấn đáp gợi ý.
  * Thiết kế Bộ Slide báo cáo 12 trang chuẩn kèm kịch bản thuyết minh chi tiết trong [slide/SLIDES_PROJECT_20.md](slide/SLIDES_PROJECT_20.md).
  * *Làm xong chuyển giao*: Chuyển giao toàn bộ giao diện hoàn chỉnh và các chương báo cáo cho An hợp nhất.
* **Nghiệm thu chung & Bàn giao sản phẩm**:
  * Hai sinh viên cùng chạy kịch bản nghiệm thu: `python check_submission.py` $\rightarrow$ Xác nhận **toàn bộ 6/6 cổng kiểm soát đều đạt `[PASS]`**.
  * Chuyển đổi và định dạng tệp báo cáo Microsoft Word chính thức: [report/BAO_CAO_PROJECT_20.docx](report/BAO_CAO_PROJECT_20.docx) (nhúng sẵn 4 hình 300 DPI).
  * Hai sinh viên tiến hành tổng duyệt thuyết trình thử và đóng gói toàn bộ dự án sẵn sàng bảo vệ.
* **Sản phẩm đầu ra Tuần 6**: Hệ sinh thái phần mềm thời gian thực hoàn chỉnh (FastAPI + React 18), Báo cáo học thuật MD & DOCX, Bộ Slide 12 trang, và Báo cáo kiểm toán chất lượng QA/QC đạt điểm 10/10.

---

## ✍️ 4. LỜI CAM ĐOAN VỀ TÍNH TRUNG THỰC VÀ BÌNH ĐẲNG

Chúng em xin cam đoan toàn bộ mã nguồn, số liệu thực nghiệm, báo cáo học thuật và slide thuyết trình trong đề tài **Project 20** là sản phẩm nghiên cứu, lao động học tập độc lập và trung thực của hai sinh viên dưới sự giảng dạy, hướng dẫn khoa học tận tình của **PGS.TS. Nguyễn Văn Hậu**. 

Hai thành viên đã phân chia khối lượng công việc cân bằng tuyệt đối ($50\% - 50\%$), cùng nắm vững toàn bộ kiến thức từ tiền xử lý dữ liệu, chống rò rỉ, thiết kế mô hình, thực thi thí nghiệm cho đến triển khai phần mềm Web/API và tự tin bảo vệ, trả lời các câu hỏi vấn đáp độc lập trước Giảng viên.

*Hưng Yên, ngày 30 tháng 09 năm 2026*  

| Đại diện Nhóm sinh viên thực hiện | Thành viên đồng thực hiện |
| :---: | :---: |
| *(Đã ký)* | *(Đã ký)* |
| **Nguyễn Văn An**<br>(Nhóm trưởng — MSV: 12523001) | **Trần Thị Bình**<br>(Thành viên — MSV: 12523002) |
