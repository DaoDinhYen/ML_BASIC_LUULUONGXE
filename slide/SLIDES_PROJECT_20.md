# BỘ SLIDE BÁO CÁO BẢO VỆ BÀI TẬP LỚN HỌC MÁY CƠ BẢN
## DỰ BÁO LƯU LƯỢNG GIAO THÔNG VỚI CHIA TẬP THEO THỜI GIAN
### (METRO INTERSTATE TRAFFIC VOLUME FORECASTING)
**Mã đề tài: Project 20**

---

<br>

## 📋 THÔNG TIN CHUNG
* **Học phần**: Học máy cơ bản (Machine Learning Fundamentals)
* **Giảng viên hướng dẫn**: PGS. TS. Nguyễn Văn Hậu
* **Lớp học phần**: 12523W.1 — Khoa Công nghệ Thông tin — Trường ĐH Sư phạm Kỹ thuật Hưng Yên (UTEHY)
* **Nhóm sinh viên thực hiện**:
  1. Nguyễn Văn An — MSV: 12523001
  2. Trần Thị Bình — MSV: 12523002
* **Thời lượng thuyết trình mục tiêu**: 8 – 10 phút

---

<br>

---

# SLIDE 1: TRANG TIÊU ĐỀ (TITLE SLIDE)

## DỰ BÁO LƯU LƯỢNG GIAO THÔNG VỚI CHIA TẬP THEO THỜI GIAN
### Nghiên cứu thực nghiệm trên tuyến cao tốc liên bang I-94 (Minnesota, Hoa Kỳ)
**Học phần: Học máy cơ bản | Mã đề tài: Project 20**

* **Giảng viên hướng dẫn**: PGS. TS. Nguyễn Văn Hậu
* **Nhóm sinh viên thực hiện**: Nguyễn Văn An & Trần Thị Bình (Lớp 12523W.1 - UTEHY)
* **Thời gian báo cáo**: Học kỳ II — Năm học 2025 – 2026

> 🎙️ **KỊCH BẢN THUYẾT MINH (SPEAKER NOTES - 45 GIÂY):**  
> *"Kính thưa thầy PGS.TS. Nguyễn Văn Hậu và toàn thể các bạn sinh viên trong lớp 12523W.1. Em tên là Nguyễn Văn An, đại diện cho nhóm sinh viên thực hiện Project 20, hôm nay xin phép được báo cáo kết quả nghiên cứu bài tập lớn với đề tài: 'Dự báo lưu lượng giao thông với chia tập theo thời gian'. Mục tiêu của đề tài là giải quyết bài toán cốt lõi trong hệ thống giao thông thông minh, bảo đảm tính toàn vẹn của chuỗi thời gian, loại bỏ hoàn toàn hiện tượng rò rỉ dữ liệu và triển khai một giải pháp phần mềm hoàn chỉnh từ API Backend đến Dashboard mô phỏng. Sau đây, em xin phép bắt đầu phần trình bày."*

---

<br>

---

# SLIDE 2: ĐẶT VẤN ĐỀ & BỐI CẢNH NGHIÊN CỨU

## Tính cấp thiết trong Hệ thống Giao thông Thông minh (ITS)

* **Thách thức ùn tắc giao thông**:
  - Gây lãng phí hàng trăm tỷ USD chi phí nhiên liệu và phát thải khí nhà kính mỗi năm.
  - Tuyến cao tốc **Interstate 94 (I-94)** kết nối Minneapolis và St. Paul (Twin Cities, Minnesota) là huyết mạch giao thông chịu tải trọng cực lớn với lưu lượng đỉnh vượt **7,000 xe/giờ**.
* **Đặc thù khí hậu Minnesota**:
  - Biên độ nhiệt khắc nghiệt từ $-25^\circ\text{C}$ (mùa đông bão tuyết đóng băng) đến $+35^\circ\text{C}$ (mùa hè oi bức).
  - Tác động phi tuyến kép: Nhịp sinh học đi làm/tan tầm + Các cú sốc thời tiết cực đoan.
* **Mục tiêu nghiên cứu**:
  1. Xây dựng mô hình học máy có khả năng dự báo chính xác lưu lượng theo giờ.
  2. Cung cấp công cụ hỗ trợ Trung tâm Quản lý Giao thông (TMC) điều tiết từ xa.

> 🎙️ **KỊCH BẢN THUYẾT MINH (SPEAKER NOTES - 45 GIÂY):**  
> *"Thưa thầy, I-94 là tuyến cao tốc huyết mạch tại miền bắc nước Mỹ. Tại đoạn qua vùng đô thị Twin Cities, lưu lượng xe có thể đạt trên 7,000 xe mỗi giờ vào giờ tan tầm. Điểm đặc biệt khiến đề tài này trở nên thách thức là vùng Minnesota có khí hậu mùa đông cực kỳ khắc nghiệt với những trận bão tuyết làm tê liệt mặt đường. Một hệ thống giao thông thông minh (ITS) nếu chỉ dựa vào cảm tính sẽ không thể dự báo kịp thời. Chúng ta cần một mô hình học máy vừa học được nhịp sinh học thường nhật, vừa phản ứng linh hoạt trước các biến đổi thời tiết khắt khe."*

---

<br>

---

# SLIDE 3: BẪY RÒ RỈ DỮ LIỆU TRONG CHUỖI THỜI GIAN

## Tại sao phân chia ngẫu nhiên (Random Shuffle) là sai lầm chết người?

* **Tính tự tương quan (Autocorrelation)**:
  $$\text{Corr}(y_t, y_{t-1}) \approx 0.95$$
  Lưu lượng của giờ hiện tại phụ thuộc chặt chẽ vào giờ liền kề trước đó.
* **Cơ chế rò rỉ (Data Leakage)**:
  - Khi dùng `train_test_split(..., shuffle=True)`: Giờ 7h và 9h nằm trong tập Train, nhưng 8h lại nằm trong tập Test!
  - Mô hình học máy thực chất đang làm bài toán **nội suy điểm khuyết** (Interpolation) chứ không phải **dự báo tương lai** (Forecasting).
  - **Hệ quả**: Điểm số $R^2$ cao ảo, khi mang ra chạy thực tế ngoài đường cao tốc thì sai số bùng nổ (Catastrophic Failure).
* **Cam kết phương pháp luận**:
  - Tuân thủ nghiêm ngặt **Chronological Time-based Split** (Tuyệt đối không xáo trộn).

> 🎙️ **KỊCH BẢN THUYẾT MINH (SPEAKER NOTES - 50 GIÂY):**  
> *"Thưa thầy, đây là nội dung quan trọng nhất mà nhóm thấm nhuần từ bài giảng của thầy. Trong dữ liệu bảng độc lập, xáo trộn ngẫu nhiên là chuẩn mực. Nhưng trong chuỗi thời gian, các giờ liền kề có sự tự tương quan cực mạnh. Nếu ta dùng lệnh shuffle ngẫu nhiên thông thường, dữ liệu 7 giờ sáng và 9 giờ sáng sẽ vào tập Train, còn 8 giờ sáng lại rơi vào tập Test. Khi đó mô hình thực chất chỉ đang 'nhìn lén bài tập' của tương lai và nội suy điểm ở giữa, tạo ra ảo tưởng về một mô hình hoàn hảo. Khi đem ra vận hành thực tế ở trạm quan sát, mô hình sẽ hoàn toàn thất bại. Vì vậy, nhóm cam kết chia tập nghiêm ngặt theo trục thời gian xuôi dòng."*

---

<br>

---

# SLIDE 4: DỮ LIỆU THỰC TẾ & QUY TRÌNH LÀM SẠCH

## Khắc phục 3 lỗi chất lượng cảm biến (Sensor Quality Auditing)

```
[48,204 bản ghi thô ban đầu (2012 - 2018)]
   ├── 1. Khử trùng lặp: Loại bỏ 7,629 bản ghi trùng mốc date_time (giữ first)
   ├── 2. Sửa lỗi phần cứng: 10 bản ghi 0.0 Kelvin -> Gán trung vị tháng
   └── 3. Cắt tỉa dị biệt: Mưa 9,831.3 mm/h -> Cắt tỉa (clip) tại ngưỡng 100 mm/h
         │
         ▼
[40,565 bản ghi sạch chuẩn mực phục vụ huấn luyện]
```

* **Quy luật khám phá qua EDA**:
  - **Đường cong 2 đỉnh ngày làm việc (Bimodal)**: Đỉnh sáng 7h–9h ($5,500\text{ xe/h}$), Đỉnh chiều 16h–18h ($6,000\text{ xe/h}$).
  - **Đường cong đơn đỉnh cuối tuần (Unimodal)**: Đỉnh thoai thoải vào giữa trưa ($4,000\text{ xe/h}$).
  - **Đêm khuya (0h–4h)**: Lưu lượng chạm đáy dưới $1,000\text{ xe/h}$.

> 🎙️ **KỊCH BẢN THUYẾT MINH (SPEAKER NOTES - 45 GIÂY):**  
> *"Trước khi đưa vào mô hình, nhóm đã thực hiện kiểm toán dữ liệu và phát hiện 3 dị biệt lớn từ cảm biến: Thứ nhất, có 7,629 dòng bị trùng mốc giờ do trạm thời tiết ghi nhận nhiều hiện tượng phụ. Nhóm đã khử trùng lặp đưa về 40,565 bản ghi duy nhất. Thứ hai, phát hiện 10 bản ghi nhiệt độ bằng đúng 0 Kelvin - tức độ không tuyệt đối phi lý trong khí quyển - nhóm đã xử lý bằng trung vị nhiệt độ của tháng đó. Thứ ba, có một mốc mưa đo nhầm lên tới hơn 9,800 mm, nhóm đã cắt tỉa về 100 mm. Sau khi làm sạch, dữ liệu thể hiện rõ nét chu kỳ 2 đỉnh giờ cao điểm kinh điển của các ngày làm việc."*

---

<br>

---

# SLIDE 5: CHIẾN LƯỢC PHÂN CHIA THEO THỜI GIAN

## Phân bổ 70% Train – 15% Validation – 15% Test

```
2012-10-02                                2017-05-10              2018-01-19          2018-09-30
 ├── [====== TẬP TRAIN (70%) ======] ──┤   ├── [= VAL (15%) =] ──┤   ├── [= TEST (15%) =] ──┤
 │      28,395 bản ghi sạch            │   │   6,085 bản ghi     │   │   6,085 bản ghi      │
 └── Huấn luyện trọng số & Transformer ─┘   └── Tinh chỉnh mô hình┘   └── Khóa niêm phong    ┘
```

* **Nguyên tắc đóng băng tập kiểm thử (Test Set Vaulting)**:
  - Toàn bộ việc tiền xử lý, chuẩn hóa `StandardScaler`, mã hóa `OneHotEncoder` chỉ được tính toán trên $28,395$ dòng của tập Train.
  - Tập Test gồm $6,085$ dòng (toàn bộ 8 tháng của năm 2018) được khóa kín, chỉ dùng để chấm điểm một lần duy nhất.

> 🎙️ **KỊCH BẢN THUYẾT MINH (SPEAKER NOTES - 45 GIÂY):**  
> *"Trên màn hình là chiến lược phân chia thời gian chuẩn mực của đề tài. Nhóm chia theo tỷ lệ 70% Train, 15% Validation và 15% Test. Tập Train gồm gần 28,400 dòng từ tháng 10/2012 đến tháng 5/2017. Tập Validation gồm hơn 6,000 dòng dùng để lựa chọn mô hình. Và quan trọng nhất, tập Test độc lập gồm hơn 6,000 dòng kéo dài đến hết tháng 9/2018 được niêm phong hoàn toàn. Mọi phép chuẩn hóa trung bình và độ lệch chuẩn đều chỉ học trên tập Train, đảm bảo mô hình không hề biết trước tương lai dù chỉ là một con số thống kê."*

---

<br>

---

# SLIDE 6: ĐỔI MỚI TRÍCH XUẤT ĐẶC TRƯNG

## Mã hóa chu kỳ lượng giác (Cyclical Feature Encoding) & Ngữ cảnh

* **Bài toán đứt gãy biên**: Giờ 23h và 0h sáng thực tế cách nhau 1 tiếng, nhưng về số học $|23 - 0| = 23$!
* **Giải pháp hình chiếu tròn lượng giác**:
  $$\sin\text{\_hour} = \sin\left(\frac{2\pi \cdot \text{hour}}{24}\right), \quad \cos\text{\_hour} = \cos\left(\frac{2\pi \cdot \text{hour}}{24}\right)$$
  $$\sin\text{\_month} = \sin\left(\frac{2\pi \cdot (\text{month}-1)}{12}\right), \quad \cos\text{\_month} = \cos\left(\frac{2\pi \cdot (\text{month}-1)}{12}\right)$$
  $\Rightarrow$ Khoảng cách Euclid giữa 23h và 0h sáng được thu hẹp mượt mà về đúng $0.261$.
* **Đặc trưng ngữ cảnh chuyên ngành (Domain Flags)**:
  - `is_rush_hour`: Giờ cao điểm sáng (7-9h) và chiều (16-18h) trong các ngày trong tuần.
  - `is_weekend`: Nhận diện ngày Thứ Bảy và Chủ Nhật.
  - `is_holiday`: Nhận diện ngày lễ liên bang Hoa Kỳ.

> 🎙️ **KỊCH BẢN THUYẾT MINH (SPEAKER NOTES - 50 GIÂY):**  
> *"Một đóng góp kỹ thuật quan trọng của nhóm là giải quyết bài toán đứt gãy biên thời gian. Nếu ta đưa biến giờ từ 0 đến 23 vào mô hình, khoảng cách giữa 23 giờ đêm và 0 giờ sáng hôm sau bị hiểu là 23 đơn vị, tạo nên bước nhảy phi thực tế. Nhóm đã sử dụng phép chiếu hình học lượng giác sin và cos cho cả giờ và tháng. Nhờ đó, 23h và 0h nằm sát cạnh nhau trên vòng tròn lượng giác đơn vị. Kết hợp với các biến cờ chuyên ngành như cờ giờ cao điểm, cờ cuối tuần và cờ ngày lễ, mô hình có thể nắm bắt nhịp sống đô thị một cách tự nhiên và trọn vẹn nhất."*

---

<br>

---

# SLIDE 7: MÔ HÌNH CƠ SỞ LỊCH SỬ (HISTORICAL BASELINE)

## Chuẩn mực đối sánh thực tế (Không dùng trung bình đơn giản)

* **Công thức kỳ vọng có điều kiện**:
  $$\hat{y}_{\text{baseline}}(h, d, hol) = \mathbb{E}\big[y \mid \text{hour} = h, \text{dayofweek} = d, \text{is\_holiday} = hol\big]$$
  Học bảng tra cứu gồm $24 \times 7 \times 2 = 336$ ô giá trị lịch sử từ tập Train.
* **Cơ chế dự phòng phân tầng (Hierarchical Fallback)**:
  $$\text{Hour} \times \text{Day} \times \text{Holiday} \longrightarrow \text{Hour} \times \text{Day} \longrightarrow \text{Hour} \longrightarrow \text{Global Mean}$$
* **Ý nghĩa phương pháp luận**:
  - Đóng vai trò là đối chuẩn tối thiểu (Benchmark Floor) mà bất kỳ mô hình Machine Learning nào muốn được chấp nhận đều bắt buộc phải vượt qua.

> 🎙️ **KỊCH BẢN THUYẾT MINH (SPEAKER NOTES - 45 GIÂY):**  
> *"Theo hướng dẫn của thầy, một nghiên cứu học máy nghiêm túc không thể lấy giá trị trung bình phẳng làm baseline. Nhóm đã xây dựng lớp Historical Calendar Baseline. Mô hình này tra cứu kỳ vọng lưu lượng theo đúng tổ hợp: Giờ nào, Thứ mấy, và Có phải ngày lễ hay không. Với cơ chế fallback đa tầng, mô hình này không cần huấn luyện phức tạp nhưng đã tóm lược được toàn bộ nhịp sinh hoạt của người dân Minnesota. Đây chính là cột mốc đối chuẩn khắt khe để kiểm định xem các thuật toán như Random Forest có thực sự học được thêm điều gì từ dữ liệu thời tiết hay không."*

---

<br>

---

# SLIDE 8: KẾT QUẢ THÍ NGHIỆM 1 & 2

## Bằng chứng Data Leakage & Bảng đối chuẩn Benchmark

### Thí nghiệm 1: Bằng chứng rò rỉ dữ liệu (Data Leakage)
| Phương pháp chia tập | MAE (xe/h) | RMSE (xe/h) | $R^2$ | Đánh giá |
| :--- | :---: | :---: | :---: | :--- |
| **Random Split (Rò rỉ)** | $265.95$ | $452.85$ | $0.9476$ | Lạc quan ảo do các giờ liền kề bị rò rỉ |
| **Time Split (Chuẩn)** | **$251.64$** | **$448.68$** | **$0.9486$** | Phản ánh đúng năng lực triển khai thực tế |

### Thí nghiệm 2: Benchmark 5 Mô hình trên tập Test độc lập
| Thứ hạng | Mô hình kiểm định | Trường phái kiến trúc | MAE (xe/h) | RMSE (xe/h) | Hệ số $R^2$ |
| :---: | :--- | :--- | :---: | :---: | :---: |
| 🥇 **1** | **XGBoost Regressor** | **Ensemble Boosting (Quán quân)** | **$242.58$** | **$424.63$** | **$0.9540$** |
| 🥈 **2** | **Random Forest Regressor** | **Ensemble Bagging (Gợi ý đề bài)** | **$251.64$** | **$448.68$** | **$0.9486$** |
| 🥉 **3** | **Historical Calendar Baseline** | **Heuristic Lịch (Bắt buộc)** | **$260.77$** | **$448.08$** | **$0.9487$** |
| 4 | Ridge Regression (L2) | Linear Regularized L2 | $636.59$ | $874.48$ | $0.8048$ |
| 5 | Lasso Regression (L1) | Linear Regularized L1 | $637.99$ | $875.26$ | $0.8045$ |

> 🎙️ **KỊCH BẢN THUYẾT MINH (SPEAKER NOTES - 55 GIÂY):**  
> *"Kính thưa thầy, ở Thí nghiệm 2 trên tập Test độc lập, kết quả thể hiện một sự đối sánh hoàn hảo theo đúng lý thuyết Học máy cơ bản: Thứ nhất, cặp đôi mô hình tuyến tính có điều hòa Lasso (L1) và Ridge (L2) đều có sai số cao quanh mức 637 xe/h, chứng minh rằng dù dùng hàm phạt bình phương L2 hay trị tuyệt đối L1 thì các mô hình tuyến tính đều bất lực trước quy luật 2 đỉnh cao điểm uốn lượn ngày đêm. Thứ hai, mô hình Calendar Baseline đạt MAE ấn tượng 260.77 xe/h, vượt trội hoàn toàn so với mô hình tuyến tính, chứng minh nhịp làm việc xã hội đóng vai trò nền tảng. Và cuối cùng, ở nhóm mô hình Ensemble cây phi tuyến, Random Forest đạt kết quả xuất sắc 251.64 xe/h, và Quán quân số 1 thuộc về XGBoost Regressor với MAE kỷ lục 242.58 xe/h cùng R² vượt mốc 0.9540 nhờ khả năng học tuần tự sửa sai trên phần dư kết hợp điều hòa chặt chẽ."*

---

<br>

---

# SLIDE 9: THÍ NGHIỆM 3: HIỆN TƯỢNG TRÔI DẠT DỮ LIỆU

## Sự suy giảm hiệu năng theo năm và theo mùa (Data Drift)

* **Trôi dạt theo trục năm (Yearly Drift)**:
  - Giai đoạn huấn luyện (2012–2016): Sai số MAE duy trì rất tốt ở mức $156 – 179\text{ xe/h}$.
  - Năm 2017 (Tập Val): MAE tăng lên **$226.90\text{ xe/h}$** ($+31.7\%$).
  - Năm 2018 (Tập Test): MAE tăng lên **$256.64\text{ xe/h}$** ($+48.9\%$).
  - $\Rightarrow$ *Nguyên nhân*: Tăng trưởng kinh tế vùng đô thị làm gia tăng mật độ xe tổng thể và các công trình sửa chữa mở rộng làn đường.
* **Biến thiên sai số theo 4 mùa (Seasonal Drift)**:
  - **Mùa xuân (Spring)**: Đạt sai số thấp nhất (**MAE $172.75\text{ xe/h}$**) do thời tiết mát mẻ, tan băng, giao thông ổn định.
  - **Mùa đông (Winter)**: Đạt sai số cao nhất (**MAE $212.81\text{ xe/h}$**) do bão tuyết và mặt đường đóng băng trơn trượt.

> 🎙️ **KỊCH BẢN THUYẾT MINH (SPEAKER NOTES - 50 GIÂY):**  
> *"Sang Thí nghiệm 3, nhóm phân tích hiện tượng trôi dạt dữ liệu (Data Drift). Khi nhìn vào sai số theo năm, ta thấy một xu hướng rất rõ: Trong các năm tập Train từ 2012 đến 2016, sai số chỉ quanh mức 160-170 xe/h. Nhưng khi sang năm 2017 và 2018, sai số tăng lên mức 256 xe/h. Đây là minh chứng thực tế cho thấy lưu lượng giao thông có sự dịch chuyển phân phối theo thời gian. Về yếu tố mùa, mùa đông Minnesota có sai số cao nhất đạt 212 xe/h do sự bất định của bão tuyết. Kết quả này gợi mở một khuyến nghị kỹ thuật quan trọng: Trong thực tế, hệ thống bắt buộc phải có cơ chế tái huấn luyện tự động định kỳ 6 tháng một lần."*

---

<br>

---

# SLIDE 10: THÍ NGHIỆM 4: PHÂN TÍCH SAI SỐ ĐẶC BIỆT

## Động lực học dòng xe trong Ngày lễ & Thời tiết cực đoan

```
┌──────────────────────────────────────┬──────────────────────────────────────┐
│        NGÀY LỄ LIÊN BANG HOÀ KỲ       │        THỜI TIẾT CỰC ĐOAN (BÃO)      │
│  - MAE Ngày lễ: 56.58 xe/h           │  - MAE Trời quang: 212.00 xe/h       │
│  - MAE Ngày thường: 251.80 xe/h      │  - MAE Mưa bão/Tuyết: 285.22 xe/h    │
│  $\Rightarrow$ Giảm sâu -77.5% sai số tuyệt đối │  $\Rightarrow$ Tăng vọt +34.5% biên độ sai số   │
└──────────────────────────────────────┴──────────────────────────────────────┘
```

* **Nghịch lý ngày lễ**: Không phải mô hình thông minh hơn trong ngày lễ, mà vì vào các ngày lễ lớn (Giáng sinh, Quốc khánh), đường cao tốc vắng vẻ, lưu lượng xe giảm về gần 0, khiến sai số tuyệt đối co nhỏ lại.
* **Cú sốc thời tiết cực đoan**: Khi mưa dông lớn hoặc tuyết dày, xe cộ buộc phải giãn cách và giảm tốc độ đột ngột, dung lượng khai thác của tuyến đường (Road Capacity) sụt giảm phi tuyến, gây nên ùn tắc cục bộ mà dữ liệu thời tiết đơn thuần khó dự đoán hết.

> 🎙️ **KỊCH BẢN THUYẾT MINH (SPEAKER NOTES - 50 GIÂY):**  
> *"Ở Thí nghiệm 4, nhóm đi sâu vào hai tình huống dị biệt của thực tế giao thông: Ngày lễ và Thời tiết cực đoan. Với ngày lễ liên bang, sai số MAE giảm sâu xuống chỉ còn 56 xe/h. Bản chất là do ngày lễ người dân nghỉ ở nhà, đường vắng, biên độ lưu lượng thấp nên sai số tuyệt đối co lại. Ngược lại, khi gặp bão tuyết hoặc mưa dông lớn, sai số tăng vọt thêm 34.5% lên mức 285 xe/h. Lý do là thời tiết xấu làm giảm tốc độ lưu thông và năng lực thông hành của đường cao tốc, tạo ra các điểm nghẽn cục bộ. Điều này cho thấy nếu trong tương lai ta bổ sung thêm camera giám sát tốc độ tức thời thì mô hình sẽ còn chính xác hơn nữa."*

---

<br>

---

# SLIDE 11: DEMO HỆ THỐNG PHẦN MỀM THỜI GIAN THỰC

## Kiến trúc Decoupled: FastAPI Backend & Frontend ReactJS 18

* **Backend RESTful API (`app/backend.py`)**:
  - Quản lý bộ nhớ qua `lifespan`: Nạp mô hình vào RAM một lần duy nhất, độ trễ suy luận **$< 15\text{ ms}$**.
  - Pydantic v2 Schema validation + **Out-of-Domain Guard** (bắt lỗi nhập độ C thay vì Kelvin, cảnh báo bão vượt ngưỡng).
  - Tự động hóa kiểm thử hồi quy với 8 bài test đạt tỷ lệ vượt qua $100\%$ (`app/test_api.py`).
  - Tự động phục vụ trực tiếp Web Single Page Application tại root `http://127.0.0.1:8000/`.
* **Giao diện Web Frontend ReactJS 18 (`frontend/`)**:
  - **Màn hình 1**: Khám phá dữ liệu EDA, thống kê 40,565 bản ghi sạch và biểu đồ chu kỳ ngày đêm.
  - **Màn hình 2**: Bàn điều khiển trực quan, đồng hồ bán nguyệt SVG Gauge phân cấp dịch vụ (LOS A–F), 5 nút kịch bản mẫu nhanh, và phân tích độ nhạy thời tiết **What-If Analysis** đường nét đứt.
  - **Màn hình 3**: Trung tâm đối chuẩn học thuật hiển thị trọn vẹn số liệu và 4 đồ thị 300 DPI của 4 thí nghiệm.
  - **Chuẩn kiến trúc**: Tuân thủ triệt để yêu cầu kiến trúc Decoupled của giảng viên (FastAPI + React 18).

> 🎙️ **KỊCH BẢN THUYẾT MINH (SPEAKER NOTES - 50 GIÂY):**  
> *"Không chỉ dừng lại ở lý thuyết và mô hình tĩnh, nhóm đã hiện thực hóa trọn vẹn thành một sản phẩm phần mềm thực tế. Tầng Backend được xây dựng bằng FastAPI chuẩn công nghiệp, có cơ chế nạp mô hình vào RAM giúp phản hồi dưới 15 mili-giây, kèm bộ lọc bảo vệ Out-of-Domain phát hiện các sai sót dữ liệu. Tầng Giao diện Web Frontend được xây dựng hoàn toàn bằng React 18 theo đúng chỉ dẫn kiến trúc Decoupled của thầy PGS.TS. Nguyễn Văn Hậu, cung cấp 3 màn hình trực quan, nổi bật với tính năng What-If Weather cho phép cán bộ điều hành xem trước đường cong lưu lượng thay đổi thế nào nếu bão tuyết ập đến."*

---

<br>

---

# SLIDE 12: TỔNG KẾT & ĐỊNH HƯỚNG PHÁT TRIỂN

## Đóng góp của đề tài & Lời cảm ơn

* **Đóng góp chính**:
  1. Chứng minh bằng thực nghiệm sự nguy hại của rò rỉ dữ liệu chuỗi thời gian.
  2. Thiết kế Pipeline chuẩn Scikit-learn với mã hóa lượng giác $\sin/\cos$ mượt mà.
  3. Mô hình Random Forest tối ưu đạt MAE $251.64\text{ xe/h}$ và $R^2 = 0.9486$.
  4. Đóng gói hoàn chỉnh dịch vụ API và Web Dashboard 3 màn hình có kiểm thử tự động.
* **Hướng phát triển tương lai**:
  - Thử nghiệm các mô hình Gradient Boosting (XGBoost, LightGBM) và Deep Time-series (Informer, Temporal Fusion Transformer).
  - Mở rộng dữ liệu đa cảm biến (tích hợp camera và tốc độ lưu thông tức thời).
* **Lời cảm ơn**:
  - Nhóm xin trân trọng cảm ơn **PGS. TS. Nguyễn Văn Hậu** đã tận tình truyền đạt kiến thức và định hướng phương pháp luận khoa học nghiêm cẩn trong suốt học phần!

> 🎙️ **KỊCH BẢN THUYẾT MINH (SPEAKER NOTES - 40 GIÂY):**  
> *"Tóm lại, Project 20 đã giải quyết trọn vẹn bài toán dự báo lưu lượng giao thông I-94 theo đúng chuẩn mực khoa học chuỗi thời gian, từ khâu làm sạch, trích xuất đặc trưng lượng giác, thực thi 4 thí nghiệm bắt buộc cho đến đóng gói phần mềm hoàn chỉnh. Nhóm chúng em xin gửi lời cảm ơn chân thành và sâu sắc nhất tới thầy PGS.TS. Nguyễn Văn Hậu đã tận tâm hướng dẫn và truyền cảm hứng cho chúng em trong môn học Học máy cơ bản. Em xin chân thành cảm ơn thầy và các bạn đã chú ý lắng nghe, nhóm chúng em rất mong nhận được những câu hỏi và đóng góp quý báu từ thầy!"*
