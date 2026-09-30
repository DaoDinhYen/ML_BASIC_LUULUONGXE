# HƯỚNG DẪN GIAO DIỆN WEB FRONTEND REACTJS (PROJECT 20)

Dự án: **Hệ thống Dự báo Lưu lượng Giao thông Cao tốc Liên bang I-94**  
Học phần: **Học máy cơ bản** — GVHD: **PGS.TS. Nguyễn Văn Hậu**  
Lớp: **12523W.1** — Đại học Sư phạm Kỹ thuật Hưng Yên (UTEHY)

---

## 1. Kiến trúc Hệ thống Decoupled Chuẩn Công Nghiệp
Theo đúng yêu cầu tại Đề cương BTL (mục `project_20_content.txt` dòng 112: *"Stack khuyến nghị: Python + pandas + scikit-learn; Flask/FastAPI; HTML/CSS/JS hoặc React/Vue"*), hệ thống được kiến trúc tách bạch hoàn toàn:

```
[ Người dùng / Trình duyệt ]
           │
           │  (HTTP / JSON REST API)
           ▼
[ Frontend: ReactJS 18 + HTML5 + CSS3 + Chart.js ] ── (Port 8000 hoặc 3000)
           │
           │  /api/traffic-forecast
           │  /api/traffic-forecast-24h
           │  /api/model-card
           │  /api/experiments
           ▼
[ Backend: FastAPI Server + Pydantic + Uvicorn ] ────── (Port 8000)
           │
           │  (Inference Pipeline)
           ▼
[ Machine Learning Engine: XGBoost Regressor Pipeline ]
```

---

## 2. Cách Khởi Chạy Giao Diện

### Cách 1: Khởi chạy Trực tiếp qua FastAPI (Khuyên Dùng — Không Cần Cài Node/NPM)
FastAPI Backend đã được tích hợp sẵn Static Files Server phục vụ trực tiếp bản ReactJS SPA:
1. Mở Terminal tại thư mục gốc `Project_20_Traffic_Volume`:
   ```bash
   python app/backend.py
   ```
2. Mở trình duyệt truy cập:
   ```
   http://127.0.0.1:8000/
   ```
   *Giao diện ReactJS sẽ hiển thị ngay lập tức với đầy đủ 3 màn hình và biểu đồ tương tác.*

### Cách 2: Khởi chạy Độc lập với Vite Dev Server (Dành cho Lập trình viên React)
1. Mở Terminal tại thư mục `frontend`:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
2. Mở trình duyệt truy cập:
   ```
   http://localhost:3000/
   ```
   *Vite sẽ tự động proxy toàn bộ lượt gọi `/api` sang FastAPI Backend tại `http://127.0.0.1:8000`.*

---

## 3. Cấu Trúc Mã Nguồn Frontend
```
frontend/
├── index.html          # Bản React 18 SPA độc lập, tự tải Babel & Chart.js, FastAPI serve trực tiếp
├── package.json        # Cấu hình dự án npm (React 18, Vite, Chart.js)
├── vite.config.js      # Cấu hình Vite Dev Server kèm Reverse Proxy kết nối FastAPI
├── README.md           # Tài liệu hướng dẫn chi tiết
└── src/
    ├── main.jsx        # Điểm gắn kết React DOM (ReactDOM.createRoot)
    ├── App.jsx         # Component gốc quản lý 3 Màn hình, State & REST API calls
    └── index.css       # Toàn bộ CSS giao diện theo bảng màu thiết kế hiện đại
```

---

## 4. Các Màn Hình Chức Năng
1. **Màn hình 1: Khám phá Dữ liệu (EDA & Data Integrity)**
   - 4 Thẻ KPI thống kê: 40,565 bản ghi sạch, khử 7,629 bản ghi trùng lặp và 10 dị biệt 0 Kelvin.
   - Cơ chế chia tập chuỗi thời gian 70% - 15% - 15% chống rò rỉ dữ liệu tuyệt đối (Anti-leakage).
   - Biểu đồ chu kỳ ngày đêm (Diurnal Cycle) và tác động của thời tiết bất lợi.
2. **Màn hình 2: Mô phỏng 24h & Dự báo Trực tuyến (Real-time What-If & Gauge Meter)**
   - Đồng hồ đo bán nguyệt (SVG Semi-circle Gauge Meter) với mã màu phân loại Cấp độ Dịch vụ giao thông (LOS A đến F).
   - 5 Nút kịch bản chọn nhanh (Quick Presets): Sáng T2 Cao điểm, Chiều T6 Mưa to, Bão tuyết, Lễ Quốc khánh, Đêm khuya.
   - Phân tích độ nhạy tình huống giả định (What-If Analysis) hiển thị đường nét đứt so sánh tức thời.
   - Out-of-Domain Guard: Tự động cảnh báo khi người dùng nhập nhầm độ C thay vì Kelvin hoặc mưa dông cực đoan.
3. **Màn hình 3: Đánh giá Học thuật & 4 Thí nghiệm Chuyên sâu**
   - **TN1**: Chứng minh hiện tượng rò rỉ dữ liệu khi chia ngẫu nhiên (Random Split) so với Time-based Split.
   - **TN2**: Bảng xếp hạng 5 mô hình trên tập Test độc lập: Quán quân XGBoost ($R^2 = 0.9540$, $\text{MAE} = 242.58$), Random Forest, Calendar Baseline, Ridge (L2), Lasso (L1).
   - **TN3**: Khảo sát hiện tượng Trôi dạt Dữ liệu theo Năm (2012 - 2018) và theo Mùa.
   - **TN4**: Phân tích sai số dị biệt (Edge Cases): Ngày lễ và Thời tiết cực đoan.
