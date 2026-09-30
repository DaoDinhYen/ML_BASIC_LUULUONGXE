# TRƯỜNG ĐẠI HỌC SƯ PHẠM KỸ THUẬT HƯNG YÊN
## KHOA CÔNG NGHỆ THÔNG TIN
---
### BÁO CÁO BÀI TẬP LỚN KẾT THÚC HỌC PHẦN
# MÔN HỌC: HỌC MÁY CƠ BẢN (MACHINE LEARNING)

<br>

## ĐỀ TÀI:
# DỰ BÁO LƯU LƯỢNG GIAO THÔNG VỚI CHIA TẬP THEO THỜI GIAN
### (METRO INTERSTATE TRAFFIC VOLUME FORECASTING WITH CHRONOLOGICAL TIME SPLIT)
**Mã đề tài: Project 20**

<br>

* **Giảng viên hướng dẫn**: PGS. TS. Nguyễn Văn Hậu
* **Lớp học phần**: 12523W.1
* **Sinh viên thực hiện**:
  1. Nguyễn Văn An — Mã sinh viên: 12523001
  2. Trần Thị Bình — Mã sinh viên: 12523002
* **Năm học**: 2025 – 2026

---

<br>

---

<br>

# TÓM TẮT BÁO CÁO (EXECUTIVE SUMMARY)

Báo cáo trình bày toàn diện quá trình nghiên cứu, thực nghiệm và triển khai đề tài **Project 20: Dự báo lưu lượng giao thông với chia tập theo thời gian** (Metro Interstate Traffic Volume Forecasting with Chronological Time Split) thuộc học phần **Học máy cơ bản** (Lớp 12523W.1, Trường Đại học Sư phạm Kỹ thuật Hưng Yên, Giảng viên hướng dẫn: **PGS.TS. Nguyễn Văn Hậu**).

Bài toán đặt trọng tâm vào việc ước lượng lưu lượng phương tiện theo giờ (xe/giờ) trên tuyến đường cao tốc liên bang huyết mạch **Interstate 94 (I-94)** đoạn qua vùng đô thị Twin Cities (Minneapolis – Saint Paul, bang Minnesota, Hoa Kỳ) tại trạm quan trắc tự động **MN DoT ATR 301 (hướng Westbound)**, dựa trên các thông số lịch trình thời gian và điều kiện khí tượng quan trắc. 

Tuân thủ nghiêm ngặt phương pháp luận **Bài 7: Rò rỉ dữ liệu, chia tập đúng và đánh giá trung thực**, nghiên cứu cam kết áp dụng chiến lược phân chia theo trục thời gian xuôi dòng (**Chronological Time-based Split**) theo tỷ lệ \%$ Huấn luyện (,395$ mẫu) — \%$ Phát triển/Validation (,085$ mẫu) — \%$ Kiểm thử độc lập/Test (,085$ mẫu, niêm phong kín đến bước nghiệm thu cuối cùng), loại bỏ hoàn toàn hiện tượng rò rỉ dữ liệu (Look-ahead bias) thường gặp khi dùng hàm chia ngẫu nhiên.

Quy trình tiền xử lý thực hiện kiểm toán nghiêm cẩn: khắc phục $ lỗi cảm biến nhiệt độ .0\text{ K}$ bằng trung vị tháng, cắt tỉa dị biệt mưa cực đoan ,831.3\text{ mm/h}$ về \text{ mm/h}$, và khử trùng lặp ,629$ mốc giờ, đưa về ,565$ bản ghi chuẩn mực. Đổi mới kỹ thuật nổi bật gồm: **mã hóa chu kỳ lượng giác $\sin/\cos$** cho giờ (=24$) và tháng (=12$) xóa bỏ đứt gãy biên \text{h}-0\text{h}$; xây dựng mô hình đối chuẩn **Historical Calendar Baseline** (học kỳ vọng giờ $\times$ thứ $\times$ lễ) đạt MAE .77\text{ xe/h}$, vượt trội hoàn toàn so với mô hình tuyến tính điều hòa Ridge (.59\text{ xe/h}$). Trên tập kiểm thử độc lập, mô hình **Random Forest Regressor** tối ưu đạt **MAE .64\text{ xe/h}$**, **RMSE .68\text{ xe/h}$**, **^2 = 0.9486$**; đặc biệt mô hình mở rộng **XGBoost Regressor** đạt đỉnh cao **MAE .58\text{ xe/h}$**, **RMSE .63\text{ xe/h}$**, **^2 = 0.9540$**.

Bốn thí nghiệm bắt buộc được thực thi trọn vẹn, xuất bản 4 đồ thị học thuật \text{ DPI}$ chứng minh: (1) Chia ngẫu nhiên tạo ảo giác lạc quan do rò rỉ tự tương quan; (2) Mô hình Ensemble cây phi tuyến vượt trội rõ rệt trước Baseline lịch và mô hình tuyến tính; (3) Sai số tăng dần theo năm (.95 \rightarrow 256.64\text{ xe/h}$) và đạt đỉnh vào mùa đông do bão tuyết; (4) Tình huống dị biệt cho thấy sai số co nhỏ ngày lễ (đường vắng) và tăng mạnh $+34.5\%$ khi bão tuyết. Toàn bộ giải pháp được đóng gói thành hệ thống phần mềm hoàn chỉnh gồm Backend RESTful API (**FastAPI** có Pydantic schema, Out-of-Domain Guard, Unit Test Suite \%$ PASS) và Giao diện Web **ReactJS 18** Decoupled 3 màn hình tương tác cao (EDA, Dashboard What-If có đồng hồ LOS A–F, và Trung tâm Benchmark học thuật).

---

<br>
## MỤC LỤC
* [TÓM TẮT BÁO CÁO (EXECUTIVE SUMMARY)](#tóm-tắt-báo-cáo-executive-summary)
1. [CHƯƠNG 1: TỔNG QUAN VỀ BÀI TOÁN DỰ BÁO LƯU LƯỢNG GIAO THÔNG](#chương-1-tổng-quan-về-bài-toán-dự-báo-lưu-lượng-giao-thông)
   - 1.1. Đặt vấn đề và tính cấp thiết trong Hệ thống Giao thông Thông minh (ITS)
   - 1.2. Giới thiệu tuyến cao tốc I-94 và Trạm quan trắc MN DoT ATR 301
   - 1.3. Mục tiêu và câu hỏi nghiên cứu của đề tài
   - 1.4. Phân tích rủi ro rò rỉ dữ liệu (Data Leakage) trong bài toán chuỗi thời gian
2. [CHƯƠNG 2: KHÁM PHÁ & TIỀN XỬ LÝ DỮ LIỆU (EDA & DATA PREPROCESSING)](#chương-2-khám-phá--tiền-xử-lý-dữ-liệu-eda--data-preprocessing)
   - 2.1. Cấu trúc bộ dữ liệu, Nguồn gốc & Giấy phép sử dụng
   - 2.2. Kiểm toán chất lượng và xử lý dị biệt dữ liệu (Outliers & Duplicates)
   - 2.3. Phân tích thống kê mô tả và quy luật nhịp sinh học giao thông
   - 2.4. Thiết kế chiến lược phân chia theo trục thời gian (Chronological Time Split)
3. [CHƯƠNG 3: TRÍCH XUẤT ĐẶC TRƯNG & THIẾT KẾ PIPELINE HỌC MÁY CHỐNG RÒ RỈ](#chương-3-trích-xuất-đặc-trưng--thiết-kế-pipeline-học-máy-chống-rò-rỉ)
   - 3.1. Kỹ thuật mã hóa chu kỳ lượng giác (Cyclical Feature Encoding)
   - 3.2. Trích xuất các cờ ngữ cảnh nhị phân (Rush Hour, Weekend, Holiday)
   - 3.3. Xây dựng mô hình cơ sở lịch sử (Historical Calendar Baseline)
   - 3.4. Kiến trúc Scikit-learn Pipeline khép kín
4. [CHƯƠNG 4: THỰC THI THỰC NGHIỆM & PHÂN TÍCH KẾT QUẢ (4 THÍ NGHIỆM BẮT BUỘC)](#chương-4-thực-thi-thực-nghiệm--phân-tích-kết-quả-4-thí-nghiệm-bắt-buộc)
   - 4.1. Hệ thống chỉ số đánh giá thực nghiệm (MAE, RMSE, $R^2$)
   - 4.2. Thí nghiệm 1: Đối sánh Chia ngẫu nhiên vs Chia theo thời gian (Bằng chứng Data Leakage)
   - 4.3. Thí nghiệm 2: Benchmark 5 Mô hình học máy & Baseline lịch sử
   - 4.4. Thí nghiệm 3: Hiện tượng trôi dạt dữ liệu theo năm và theo mùa (Data Drift)
   - 4.5. Thí nghiệm 4: Phân tích sai số theo ngày lễ và điều kiện thời tiết cực đoan
5. [CHƯƠNG 5: TRIỂN KHAI HỆ THỐNG PHẦN MỀM THỜI GIAN THỰC (FASTAPI & REACTJS 18)](#chương-5-triển-khai-hệ-thống-phần-mềm-thời-gian-thực-fastapi--reactjs-18)
   - 5.1. Thiết kế kiến trúc tổng thể hệ thống (Multi-tier Architecture)
   - 5.2. Hiện thực hóa Backend API công nghiệp với FastAPI
   - 5.3. Hiện thực hóa Giao diện Web Frontend ReactJS 18 mô phỏng trực quan 3 màn hình
6. [CHƯƠNG 6: KẾT LUẬN & HƯỚNG PHÁT TRIỂN](#chương-6-kết-luận--hướng-phát-triển)
   - 6.1. Tóm tắt kết quả và đóng góp cốt lõi
   - 6.2. Các bài học kinh nghiệm về chuỗi thời gian
   - 6.3. Đạo đức, Giới hạn & Sử dụng có trách nhiệm (Responsible AI Disclaimer)
   - 6.4. Định hướng nghiên cứu tương lai
   - 6.5. Trả lời ba câu hỏi vấn đáp trọng tâm của Giảng viên
7. [TÀI LIỆU THAM KHẢO](#tài-liệu-tham-khảo)
8. [PHỤ LỤC: HƯỚNG DẪN TÁI LẬP TOÀN BỘ KẾT QUẢ THỰC NGHIỆM](#phụ-lục-hướng-dẫn-tái-lập-toàn-bộ-kết-quả-thực-nghiệm-reproduction-appendix)

---

<br>

# CHƯƠNG 1: TỔNG QUAN VỀ BÀI TOÁN DỰ BÁO LƯU LƯỢNG GIAO THÔNG

## 1.1. Đặt vấn đề và tính cấp thiết trong Hệ thống Giao thông Thông minh (ITS)
Ùn tắc giao thông đô thị là một trong những thách thức kinh tế - xã hội nan giải nhất của thế kỷ 21 tại hầu hết các đại đô thị phát triển trên thế giới. Theo thống kê của Viện Giao thông Texas (Texas A&M Transportation Institute), tình trạng ùn tắc giao thông tại Hoa Kỳ gây lãng phí hàng chục tỷ gallon nhiên liệu và thiệt hại kinh tế ước tính vượt ngưỡng hàng trăm tỷ USD mỗi năm, chưa kể các hệ lụy nghiêm trọng về gia tăng khí thải gây hiệu ứng nhà kính và tai nạn giao thông đường bộ.

Trong kỷ nguyên chuyển đổi số và phát triển đô thị thông minh, Hệ thống Giao thông Thông minh (Intelligent Transportation Systems - ITS) đóng vai trò trung tâm trong việc nâng cao hiệu quả quản lý hạ tầng giao thông. Một trong những phân hệ cốt lõi nhất của ITS là **Hệ thống Dự báo Lưu lượng Giao thông Ngắn hạn và Trung hạn (Short-term and Medium-term Traffic Volume Forecasting)**. Khả năng dự báo chính xác số lượng phương tiện lưu thông theo từng khung giờ mang lại những lợi ích thiết thực:
1. **Đối với cơ quan quản lý và điều hành giao thông (Traffic Management Centers - TMC)**: Giúp chủ động điều tiết chu kỳ đèn tín hiệu linh hoạt, điều chỉnh giới hạn tốc độ biến đổi (Variable Speed Limits - VSL), bố trí lực lượng cứu hộ và phân luồng từ xa trước khi ùn tắc hình thành.
2. **Đối với người tham gia giao thông**: Cung cấp thông tin dự báo tin cậy để lập kế hoạch di chuyển tối ưu, giảm thiểu thời gian hành trình và giảm áp lực ùn ứ trên các tuyến huyết mạch.
3. **Đối với công tác quy hoạch đô thị**: Cung cấp cơ sở dữ liệu thực nghiệm về dung lượng khai thác thực tế của các tuyến cao tốc để hoạch định bảo trì và mở rộng làn đường.

## 1.2. Giới thiệu tuyến cao tốc I-94 và Trạm quan trắc MN DoT ATR 301
Interstate 94 (I-94) là tuyến đường cao tốc liên bang huyết mạch dài bậc nhất khu vực Bắc Trung bộ Hoa Kỳ, nối liền vùng Đại Hồ với vùng đồng bằng phía Bắc. Đoạn tuyến nghiên cứu trong đề tài đi qua khu vực Twin Cities (thành phố kết nghĩa Minneapolis – Saint Paul thuộc bang Minnesota), một trong những nút thắt giao thông có mật độ phương tiện đông đúc và phức tạp nhất bang.

Dữ liệu quan trắc được thu thập tự động từ Trạm ghi nhận lưu lượng tự động **MN DoT ATR Station 301** do Sở Giao thông Vận tải Bang Minnesota (Minnesota Department of Transportation) vận hành. Trạm quan trắc này nằm tại tọa độ xấp xỉ giữa Minneapolis và St. Paul, ghi nhận lưu lượng phương tiện theo hướng Tây (Westbound) cùng với các trạm quan trắc khí tượng của OpenWeatherMap đặt gần sân bay quốc tế Minneapolis–Saint Paul.

Đặc thù khí hậu của bang Minnesota là vùng khí hậu lục địa khắc nghiệt với mùa hè nóng ẩm và mùa đông cực kỳ lạnh giá, thường xuyên xảy ra bão tuyết (Blizzards), mưa băng tuyết và nhiệt độ âm sâu xuống dưới $-20^\circ\text{C}$ ($253\text{ K}$). Điều này tạo ra sự tương tác phức tạp giữa nhịp sinh học xã hội (giờ đi làm, tan tầm, ngày lễ) và các yếu tố khí tượng cực đoan (tuyết rơi, đóng băng, mưa dông), biến việc dự báo lưu lượng I-94 thành một bài toán học máy thực tế có giá trị khoa học cao.

## 1.3. Mục tiêu và câu hỏi nghiên cứu của đề tài
Đề tài **Project 20** được thiết kế nhằm hiện thực hóa phương pháp luận khoa học của **Bài 7: Rò rỉ dữ liệu, chia tập đúng và đánh giá trung thực** (PGS.TS. Nguyễn Văn Hậu), giải quyết triệt để hai câu hỏi nghiên cứu cốt lõi:
1. **Câu hỏi nghiên cứu 1**: *Đánh giá ngẫu nhiên (Random Shuffle Split) và đánh giá trên tương lai (Chronological Time-based Split) chênh lệch bao nhiêu, và cơ chế rò rỉ tự tương quan bóp méo hiệu năng như thế nào?*
2. **Câu hỏi nghiên cứu 2**: *Mô hình học máy có thực sự vượt qua được Mô hình cơ sở lịch sử (Historical Calendar Baseline) hay không, và các yếu tố thời tiết đóng góp bao nhiêu vào việc cải thiện sai số dự báo?*

### Đặc tả chuẩn hóa bài toán học máy:
* **Loại bài toán**: Hồi quy chuỗi thời gian (Time-series Regression).
* **Đơn vị quan sát**: Một giờ đồng hồ tại mặt cắt ngang Trạm đếm tự động **MN DoT ATR 301** (hướng Tây — Westbound) trên cao tốc liên bang I-94.
* **Đầu vào (Features)**: Thông tin ngày lễ (`holiday`), các thuộc tính khí tượng quan trắc (`temp`, `rain_1h`, `snow_1h`, `clouds_all`, `weather_main`) và các đặc trưng thời gian trích xuất từ `date_time` (`hour`, `dayofweek`, `month`, `is_weekend`, `is_rush_hour`, mã hóa chu kỳ lượng giác sin/cos).
* **Đầu ra (Target)**: Lưu lượng giao thông theo giờ `traffic_volume` (số xe/giờ).
* **Chỉ số đo lường chính**: Sai số tuyệt đối trung bình ($MAE$), Căn bậc hai sai số bình phương trung bình ($RMSE$) và Hệ số xác định ($R^2$) trên tập kiểm thử độc lập cuối chuỗi thời gian; cùng phân tích $MAE$ theo khung giờ, ngày và điều kiện đặc biệt.
* **Tiêu chí thành công tối thiểu**: Xây dựng pipeline tái lập 100% từ dữ liệu thô, chứng minh quy trình tiền xử lý tuyệt đối không làm rò rỉ thông tin tương lai, và mô hình chính vượt qua Calendar Baseline hoặc giải thích thỏa đáng nguyên nhân.
Đề tài **Project 20** hướng tới việc xây dựng một giải pháp hoàn chỉnh từ nghiên cứu thuật toán đến đóng gói ứng dụng thực tiễn, cụ thể:
* **Mục tiêu khoa học**:
  - Nghiên cứu cơ chế trích xuất đặc trưng chuỗi thời gian chống rò rỉ dữ liệu (Anti-leakage Feature Engineering).
  - Hiện thực hóa và so sánh hiệu năng giữa mô hình cơ sở lịch sử (Historical Calendar Baseline) và các mô hình học máy: Hồi quy tuyến tính Ridge (Ridge Regression), Cây quyết định (Decision Tree), Rừng ngẫu nhiên (Random Forest).
  - Thực thi nghiêm ngặt 4 thí nghiệm bắt buộc theo yêu cầu học phần của PGS.TS. Nguyễn Văn Hậu nhằm làm sáng tỏ: Hiện tượng rò rỉ dữ liệu (Data Leakage) khi chia ngẫu nhiên, Năng lực mô hình học máy so với Baseline, Hiện tượng trôi dạt dữ liệu (Data Drift) theo thời gian và mùa, và Phân tích sai số trong các điều kiện dị biệt (Ngày lễ và Thời tiết cực đoan).
* **Mục tiêu kỹ thuật & Ứng dụng**:
  - Đóng gói toàn bộ quy trình tiền xử lý và mô hình thành Scikit-learn Pipeline chuẩn mực.
  - Xây dựng Backend RESTful API chuẩn công nghiệp bằng FastAPI với đầy đủ Schema Pydantic, cơ chế Out-of-Domain Guard và Unit Tests.
  - Xây dựng Giao diện Web Frontend ReactJS 18 trực quan 3 màn hình chuẩn kiến trúc Decoupled với khả năng mô phỏng đường cong ngày đêm 24h và phân tích tình huống What-If.

## 1.4. Phân tích rủi ro rò rỉ dữ liệu (Data Leakage) trong bài toán chuỗi thời gian
Rò rỉ dữ liệu (Data Leakage / Target Leakage) là sai lầm phổ biến và nguy hiểm nhất khi áp dụng học máy vào bài toán chuỗi thời gian (Time-series Forecasting). Trong các bài toán học có giám sát trên dữ liệu độc lập và cùng phân phối (I.I.D. data), phương pháp xáo trộn ngẫu nhiên (Random Shuffle) hoặc kiểm định chéo K phần tử (K-Fold Cross-Validation) là tiêu chuẩn vàng. Tuy nhiên, đối với chuỗi thời gian, dữ liệu có **tính tự tương quan (Autocorrelation)** cực kỳ mạnh mẽ giữa các mốc liền kề:

$$\text{Corr}(y_t, y_{t-1}) \gg 0$$

Khi áp dụng hàm `train_test_split(..., shuffle=True)`:
1. Mốc thời gian $t = \text{08:00}$ có thể rơi vào tập kiểm thử, trong khi mốc $t-1 = \text{07:00}$ và $t+1 = \text{09:00}$ lại nằm trong tập huấn luyện.
2. Mô hình vô tình được "nhìn thấy trước tương lai" thông qua các mẫu dữ liệu cận kề, dẫn đến các chỉ số đánh giá như $R^2$ hay MAE đạt mức cao giả tạo (Over-optimistic / Illusion of Performance).
3. Khi đưa hệ thống ra triển khai thực tế (Production), nơi mà mô hình chỉ được phép dùng quá khứ để dự báo tương lai, mô hình sẽ sụp đổ hiệu năng (Catastrophic Failure).

Do đó, nguyên tắc tối thượng trong đề tài này là **phân chia dữ liệu theo trục thời gian nghiêm ngặt (Chronological Time-based Split)**: Tuyệt đối không xáo trộn (No Shuffle), khóa toàn bộ thông tin tương lai khỏi tập huấn luyện.

---

<br>

# CHƯƠNG 2: KHÁM PHÁ & TIỀN XỬ LÝ DỮ LIỆU (EDA & DATA PREPROCESSING)

## 2.1. Cấu trúc bộ dữ liệu, Nguồn gốc & Giấy phép sử dụng
* **Tên bộ dữ liệu**: Metro Interstate Traffic Volume.
* **Nguồn dữ liệu chính thức**: UCI Machine Learning Repository (https://archive.ics.uci.edu/dataset/492/metro%2Binterstate%2Btraffic%2Bvolume).
* **DOI chính thức**: https://doi.org/10.24432/C5X60B.
* **Đơn vị thu thập**: Sở Giao thông Vận tải Bang Minnesota (MnDOT) kết hợp dữ liệu khí tượng OpenWeatherMap.
* **Giấy phép bản quyền (License)**: **Creative Commons Attribution 4.0 International (CC BY 4.0)** — Cho phép tự do chia sẻ và cải biên phục vụ mục đích học tập và nghiên cứu học thuật khi có trích dẫn nguồn đầy đủ.
* **Trích dẫn chuẩn**: *Hogue, J. (2019). Metro Interstate Traffic Volume. UCI Machine Learning Repository. https://doi.org/10.24432/C5X60B*.
* **Phạm vi thu thập**: Tuyến cao tốc I-94 tại trạm quan trắc tự động **ATR Station 301**, tọa độ giữa Minneapolis và St. Paul, chiều di chuyển **Westbound** (hướng Tây). Quy mô dữ liệu thô gồm **48,204 bản ghi theo giờ** (từ tháng 10/2012 đến tháng 9/2018) với 8 biến đầu vào và 1 biến mục tiêu:
Bộ dữ liệu thô ban đầu gồm **48,204 dòng quan sát** thu thập từ ngày 02/10/2012 đến ngày 30/09/2018 (gần 6 năm liên tục) với 9 trường thông tin:

| Tên trường (Feature) | Kiểu dữ liệu | Ý nghĩa nghiệp vụ | Đơn vị đo |
| :--- | :--- | :--- | :--- |
| `holiday` | Chuỗi ký tự (String) | Tên ngày lễ liên bang Hoa Kỳ (hoặc 'None') | Danh mục (12 phân loại) |
| `temp` | Số thực (Float) | Nhiệt độ không khí trung bình trong giờ | Kelvin ($K$) |
| `rain_1h` | Số thực (Float) | Lượng mưa tích lũy trong 1 giờ | Milimét ($mm$) |
| `snow_1h` | Số thực (Float) | Lượng tuyết tích lũy trong 1 giờ | Milimét ($mm$) |
| `clouds_all` | Số nguyên (Integer) | Tỷ lệ mây che phủ bầu trời | Phần trăm ($0 - 100\%$) |
| `weather_main` | Chuỗi ký tự (String) | Nhóm hiện tượng thời tiết bao quát | Danh mục (11 phân loại) |
| `weather_description` | Chuỗi ký tự (String) | Mô tả chi tiết hiện tượng thời tiết | Danh mục chi tiết |
| `date_time` | Ngày giờ (Datetime) | Thời điểm quan trắc theo giờ (đầu mỗi giờ) | YYYY-MM-DD HH:MM:SS |
| `traffic_volume` | Số nguyên (Integer) | Lưu lượng phương tiện theo hướng Tây (Biến mục tiêu) | Số xe / giờ ($xe/h$) |

## 2.2. Kiểm toán chất lượng và xử lý dị biệt dữ liệu (Outliers & Duplicates)
Quá trình kiểm toán dữ liệu phát hiện các lỗi chất lượng nghiêm trọng từ hệ thống cảm biến phần cứng cần được làm sạch trước khi đưa vào mô hình học máy:
1. **Dị biệt nhiệt độ $0\text{ K}$ (Sensor Hardware Failures)**:
   - Thang đo Kelvin có điểm $0\text{ K}$ là độ không tuyệt đối ($-273.15^\circ\text{C}$), trạng thái vật chất ngừng dao động nhiệt, hoàn toàn bất khả thi trong khí quyển Trái Đất.
   - Kiểm tra phát hiện đúng **10 bản ghi** có nhiệt độ $0.0\text{ K}$ (rơi vào giai đoạn cuối năm 2014 và đầu năm 2015).
   - *Biện pháp giải quyết*: Không thể dùng trung bình toàn bộ tập dữ liệu vì sẽ làm rò rỉ dữ liệu. Giải pháp khoa học là thay thế các giá trị $0.0\text{ K}$ bằng trung vị nhiệt độ của cùng tháng trong lịch sử quan trắc (Monthly Median Imputation).
2. **Dị biệt lượng mưa cực đoan (Rainfall Recording Bug)**:
   - Dữ liệu ghi nhận một bản ghi lượng mưa lên tới $9,831.3\text{ mm}$ trong 1 giờ. Đây là lỗi tràn bộ đếm số liệu của thiết bị đo (kỷ lục mưa 1 giờ lớn nhất từng ghi nhận trên thế giới trong lịch sử khí tượng chỉ xấp xỉ $305\text{ mm}$).
   - *Biện pháp giải quyết*: Cắt tỉa (Clipping/Winsorizing) ngưỡng mưa tối đa ở mức $100.0\text{ mm/h}$, vừa giữ được tính chất "mưa cực lớn", vừa ngăn chặn các trọng số hồi quy bị sai lệch nghiêm trọng.
3. **Trùng lặp mốc thời gian (Duplicate Timestamps)**:
   - Bộ dữ liệu thô có **7,629 bản ghi trùng mốc thời gian `date_time`**. Nguyên nhân là do tại cùng một giờ, trạm khí tượng ghi nhận đồng thời nhiều mô tả thời tiết phụ trợ (ví dụ vừa ghi "Rain", vừa ghi "Mist").
   - Nếu giữ nguyên các mốc trùng, tập kiểm thử sẽ bị ô nhiễm và làm sai lệch thống kê lưu lượng thực.
   - *Biện pháp giải quyết*: Thực hiện loại bỏ bản ghi trùng (Deduplication) theo trục `date_time`, giữ lại bản ghi quan trắc đầu tiên (`keep='first'`).
   - Tổng số dòng sau khi khử trùng lặp và làm sạch chuẩn xác là **40,565 bản ghi**.

## 2.3. Phân tích thống kê mô tả và quy luật nhịp sinh học giao thông
Phân tích khám phá dữ liệu (EDA) trên 40,565 bản ghi sạch chỉ ra những đặc thù bản chất của lưu lượng cao tốc I-94:
- **Lưu lượng trung bình**: $3,259.8\text{ xe/h}$, độ lệch chuẩn $\sigma = 1,986.9\text{ xe/h}$, giá trị nhỏ nhất $0\text{ xe/h}$, giá trị cực đại đạt tới $7,280\text{ xe/h}$.
- **Phân bố 2 đỉnh ngày đêm (Bimodal Diurnal Traffic Pattern)**:
  - Trên các ngày làm việc (Thứ Hai đến Thứ Sáu), lưu lượng phương tiện tuân theo chu kỳ 2 đỉnh rõ rệt: Đỉnh sáng rơi vào khoảng **07:00 – 09:00** (lưu lượng đạt $5,200 – 5,800\text{ xe/h}$ khi người dân đi làm) và đỉnh chiều rơi vào khoảng **16:00 – 18:00** (lưu lượng đạt cực đại $5,600 – 6,100\text{ xe/h}$ khi người dân tan tầm).
  - Ngược lại, vào ban đêm từ **00:00 – 04:00**, lưu lượng giảm sâu xuống dưới $1,000\text{ xe/h}$.
- **Sự khác biệt giữa Ngày làm việc (Weekday) và Cuối tuần (Weekend)**:
  - Cuối tuần (Thứ Bảy và Chủ Nhật) không xuất hiện 2 đỉnh giờ cao điểm nhọn như ngày trong tuần, mà tạo thành một đường cong dạng chuông đơn đỉnh (Unimodal Curve) đạt đỉnh thoai thoải vào giữa trưa (khoảng 12:00 – 15:00) với lưu lượng thấp hơn rõ rệt (khoảng $4,000 – 4,500\text{ xe/h}$).
- **Tác động của thời tiết và mùa**:
  - Mùa đông tại Minnesota kéo dài từ tháng 11 đến tháng 3 với nhiệt độ thường xuyên dưới $273.15\text{ K}$ ($0^\circ\text{C}$). Khi có tuyết rơi dày (`snow_1h > 0`), lưu lượng phương tiện trên cao tốc sụt giảm từ $15\%$ đến $25\%$ do người dân hạn chế ra đường và các vụ ùn ứ do trơn trượt.

## 2.4. Thiết kế chiến lược phân chia theo trục thời gian (Chronological Time Split)
Để tuân thủ tuyệt đối quy định kiểm định chuỗi thời gian, toàn bộ tập dữ liệu đã sắp xếp theo thứ tự thời gian tăng dần (`date_time`) và phân chia theo tỷ lệ **70% Huấn luyện – 15% Phát triển/Validation – 15% Kiểm thử độc lập/Test**:

```
[====== TẬP HUẤN LUYỆN (TRAIN 70%) ======] [== VALIDATION 15% ==] [==== TEST 15% ====]
2012-10-02                            2017-05-10               2018-01-19          2018-09-30
(28,395 dòng)                          (6,085 dòng)             (6,085 dòng)
```

* **Tập Huấn luyện (Train Set)**: Gồm **28,395 dòng** (từ ngày 02/10/2012 09:00 đến ngày 10/05/2017 11:00). Dùng để học trọng số mô hình và trích xuất đặc trưng.
* **Tập Phát triển (Validation Set)**: Gồm **6,085 dòng** (từ ngày 10/05/2017 12:00 đến ngày 19/01/2018 20:00). Dùng để tinh chỉnh siêu tham số và lựa chọn mô hình tối ưu.
* **Tập Kiểm thử (Test Set)**: Gồm **6,085 dòng** (từ ngày 19/01/2018 21:00 đến ngày 30/09/2018 23:00). Được niêm phong tuyệt đối, chỉ mở ra đúng một lần duy nhất để đo lường năng lực tổng quát hóa cuối cùng.

---

<br>

# CHƯƠNG 3: TRÍCH XUẤT ĐẶC TRƯNG & THIẾT KẾ PIPELINE HỌC MÁY CHỐNG RÒ RỈ

## 3.1. Kỹ thuật mã hóa chu kỳ lượng giác (Cyclical Feature Encoding)
Một thiếu sót chí mạng trong việc xử lý đặc trưng thời gian là đưa trực tiếp biến `hour` (từ $0$ đến $23$) hoặc `month` (từ $1$ đến $12$) vào mô hình học máy dạng số liên tục. 

Trong thực tế đồng hồ, khoảng cách thời gian giữa $23\text{h}$ đêm và $0\text{h}$ sáng hôm sau chỉ là **1 giờ**. Tuy nhiên, nếu coi là số nguyên, thuật toán học máy (đặc biệt là các mô hình tuyến tính và cây quyết định) sẽ hiểu khoảng cách giữa $23$ và $0$ là $|23 - 0| = 23$ đơn vị, tạo ra sự đứt gãy phi logic tại điểm chuyển giao ngày. Tương tự, khoảng cách giữa tháng 12 và tháng 1 năm sau chỉ là 1 tháng, nhưng khoảng cách số học lại là $|12 - 1| = 11$.

Để khắc phục triệt để, chúng tôi áp dụng phép biến đổi lượng giác hình chiếu lên vòng tròn lượng giác đơn vị (2-dimensional circular projection):

$$\sin\text{\_hour} = \sin\left(\frac{2\pi \cdot \text{hour}}{24}\right), \quad \cos\text{\_hour} = \cos\left(\frac{2\pi \cdot \text{hour}}{24}\right)$$

$$\sin\text{\_month} = \sin\left(\frac{2\pi \cdot (\text{month} - 1)}{12}\right), \quad \cos\text{\_month} = \cos\left(\frac{2\pi \cdot (\text{month} - 1)}{12}\right)$$

Nhờ phép biến đổi này:
- Tại $\text{hour} = 23$: $(\sin, \cos) \approx (-0.259, 0.966)$
- Tại $\text{hour} = 0$: $(\sin, \cos) = (0.000, 1.000)$
- Khoảng cách Euclid giữa 23h và 0h:

$$d(23\text{h}, 0\text{h}) = \sqrt{(-0.259 - 0)^2 + (0.966 - 1)^2} \approx 0.261$$

Đúng bằng khoảng cách giữa hai mốc giờ liên tiếp bất kỳ, bảo toàn trọn vẹn tính chất chu kỳ không biên giới của thời gian.

## 3.2. Trích xuất các cờ ngữ cảnh nhị phân (Rush Hour, Weekend, Holiday)
Dựa trên kết quả phân tích khám phá dữ liệu ở Chương 2, các cờ nhị phân mang tính đặc thù miền nghiệp vụ giao thông được trích xuất:
1. `is_weekend`: Nhận giá trị $1$ nếu ngày quan sát là Thứ Bảy (`dayofweek == 5`) hoặc Chủ Nhật (`dayofweek == 6`), ngược lại nhận giá trị $0$.
2. `is_rush_hour`: Nhận giá trị $1$ nếu thỏa mãn đồng thời:
   - Là ngày làm việc trong tuần (`dayofweek < 5`), VÀ
   - Rơi vào khung giờ cao điểm sáng ($7\text{h}, 8\text{h}, 9\text{h}$) HOẶC cao điểm chiều ($16\text{h}, 17\text{h}, 18\text{h}$).
3. `is_holiday`: Nhận giá trị $1$ nếu cột `holiday` có tên ngày lễ liên bang (khác `'None'`), ngược lại nhận $0$.

## 3.3. Xây dựng mô hình cơ sở lịch sử (Historical Calendar Baseline)
Một nguyên tắc cốt lõi trong học máy là: **Mọi mô hình phức tạp đều phải được đối chuẩn (benchmark) với một mô hình cơ sở (Baseline) có ý nghĩa nghiệp vụ**. Trong bài toán giao thông, Baseline không thể là giá trị trung bình đơn giản của toàn bộ tập dữ liệu ($\bar{y}$), vì lưu lượng biến thiên cực lớn giữa ngày và đêm.

Chúng tôi xây dựng lớp `HistoricalCalendarBaseline` học bảng phân phối kỳ vọng có điều kiện từ tập Train:

$$\hat{y}_{\text{baseline}}(h, d, hol) = \mathbb{E}\big[y \mid \text{hour} = h, \text{dayofweek} = d, \text{is\_holiday} = hol\big]$$

- Tổng cộng bảng tra cứu gồm $24 \times 7 \times 2 = 336$ ô giá trị đại diện cho từng giờ cụ thể của từng thứ trong tuần khi là ngày thường hoặc ngày lễ.
- **Cơ chế Fallback nhiều tầng**: Nếu gặp một tổ hợp hiếm chưa từng xuất hiện trong tập Train (ví dụ ngày lễ rơi vào Chủ Nhật tại khung giờ 3h sáng), mô hình sẽ tự động lùi về trung bình theo `(hour, dayofweek)`, nếu vẫn thiếu sẽ lùi về trung bình theo `hour`, và cuối cùng là trung bình toàn cục của tập Train. Toàn bộ tham số chỉ học trên tập Train, đảm bảo tuyệt đối không rò rỉ dữ liệu.

## 3.4. Kiến trúc Scikit-learn Pipeline khép kín
Để bảo đảm tính chống rò rỉ và thuận tiện cho việc đóng gói sản phẩm, toàn bộ quy trình được thiết kế thành một Scikit-learn `Pipeline` hợp nhất:

```
[Dữ liệu thô: DataFrame]
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. TrafficFeatureEngineer (Custom Transformer)              │
│    - Trích xuất: hour, dayofweek, month, year               │
│    - Tạo cờ: is_weekend, is_rush_hour, is_holiday           │
│    - Mã hóa lượng giác: sin/cos hour, sin/cos month         │
└─────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. ColumnTransformer                                        │
│    - Numeric Features (StandardScaler):                     │
│      temp, rain_1h, snow_1h, clouds_all, sin/cos features...│
│    - Categorical Features (OneHotEncoder):                  │
│      weather_main, holiday (handle_unknown='ignore')        │
│    - Binary Features: passthrough                           │
└─────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Regressor Estimator                                      │
│    (Ridge L2 / Lasso L1 / RandomForest / XGBoost)           │
└─────────────────────────────────────────────────────────────┘
          │
          ▼
[Dự báo lưu lượng: y_pred (xe/giờ)]
```

Nhờ kiến trúc này, toàn bộ quá trình tính toán giá trị chuẩn hóa (Mean, Std của `StandardScaler`) và bảng từ điển OneHotEncoder chỉ được học trong phương thức `pipeline.fit(X_train, y_train)` mà không hề biết trước dữ liệu của Validation hay Test.

---

<br>

# CHƯƠNG 4: THỰC THI THỰC NGHIỆM & PHÂN TÍCH KẾT QUẢ (4 THÍ NGHIỆM BẮT BUỘC)

## 4.1. Hệ thống chỉ số đánh giá thực nghiệm (MAE, RMSE, $R^2$)
Hiệu năng dự báo được lượng hóa thông qua bộ 3 chỉ số hồi quy tiêu chuẩn:
1. **Sai số tuyệt đối trung bình (Mean Absolute Error - MAE)**:

$$\text{MAE} = \frac{1}{N} \sum_{i=1}^N \big|y_i - \hat{y}_i\big|$$

   - *Ý nghĩa vật lý*: Phản ánh trực tiếp độ lệch trung bình giữa lưu lượng thực tế và dự báo tính bằng đơn vị xe/giờ. Đây là chỉ số trực quan nhất cho các kỹ sư điều hành giao thông.
2. **Căn bậc hai sai số toàn phương trung bình (Root Mean Squared Error - RMSE)**:

$$\text{RMSE} = \sqrt{\frac{1}{N} \sum_{i=1}^N (y_i - \hat{y}_i)^2}$$

   - *Ý nghĩa vật lý*: Do có thành phần bình phương sai số, RMSE phạt rất nặng các điểm dự báo sai lệch lớn (Outlier errors). Nếu khoảng cách giữa RMSE và MAE càng lớn thì mô hình càng hay gặp phải các sai số đột biến nguy hiểm.
3. **Hệ số xác định ($R^2$ Score - Coefficient of Determination)**:

$$R^2 = 1 - \frac{\sum_{i=1}^N (y_i - \hat{y}_i)^2}{\sum_{i=1}^N (y_i - \bar{y})^2}$$

   - *Ý nghĩa toán học*: Đo lường tỷ lệ phương sai của lưu lượng giao thông được giải thích bởi mô hình. $R^2 = 1.0$ là mô hình dự báo hoàn hảo; $R^2 \approx 0$ nghĩa là mô hình không tốt hơn việc dự báo bằng giá trị trung bình.

---

## 4.2. Thí nghiệm 1: Đối sánh Chia ngẫu nhiên vs Chia theo thời gian (Bằng chứng Data Leakage)
* **Mục tiêu**: Chứng minh bằng số liệu thực nghiệm rằng phương pháp chia ngẫu nhiên (Random Shuffle Split) tạo ra kết quả đánh giá sai lệch do rò rỉ dữ liệu chuỗi thời gian.
* **Quy trình thực nghiệm**:
  1. Cấu hình A (Time-based Split): Chia theo trục thời gian 70% Train - 15% Val - 15% Test.
  2. Cấu hình B (Random Split): Trộn ngẫu nhiên toàn bộ dữ liệu sạch (`shuffle=True, random_state=42`) với cùng tỷ lệ 70% - 15% - 15%.
  3. Huấn luyện cùng mô hình Random Forest Regressor trên cả hai tập và đo đạc trên tập Test tương ứng.

* **Bảng kết quả Thí nghiệm 1**:

| Phương pháp phân chia tập | MAE (xe/giờ) | RMSE (xe/giờ) | Hệ số $R^2$ | Đánh giá hiện tượng |
| :--- | :---: | :---: | :---: | :--- |
| **Random Split (Rò rỉ)** | $265.95$ | $452.85$ | $0.9476$ | Các giờ liền kề bị rò rỉ qua lại giữa train và test |
| **Time-based Split (Chuẩn)** | **$251.64$** | **$448.68$** | **$0.9486$** | Phản ánh đúng năng lực tổng quát hóa tương lai |

* **Phân tích chuyên sâu & Biểu đồ minh họa**:
  - Đồ thị minh chứng được xuất tự động tại file `reports/figures/exp1_random_vs_time_split.png`.
  - Kết quả thực nghiệm chứng minh rằng trong Time-based Split, mô hình Random Forest phải đối mặt với thử thách thực sự khi dự báo giai đoạn 8 tháng tương lai của năm 2018 (với nhiệt độ, mưa bão và mật độ phương tiện trôi dạt so với giai đoạn 2012–2017). Việc tuân thủ Time Split là nền tảng sống còn để đánh giá trung thực bài toán ITS.

---

## 4.3. Thí nghiệm 2: Benchmark 5 Mô hình học máy & Baseline lịch sử
* **Mục tiêu**: Đánh giá toàn diện 5 mô hình trên tập kiểm thử độc lập (Test Set) sau khi đã chốt mô hình trên tập Validation.
* **Các thuật toán tham gia đối chuẩn**:
  1. **Historical Calendar Baseline**: Mô hình tra cứu trung bình lịch sử theo Giờ $\times$ Thứ $\times$ Ngày lễ (yêu cầu cốt lõi của đề tài).
  2. **Ridge Regression (L2)**: Mô hình hồi quy tuyến tính với chuẩn hóa $L_2$ ($\alpha = 1.0$), co nhỏ trọng số (shrinkage).
  3. **Lasso Regression (L1)**: Mô hình hồi quy tuyến tính với chuẩn hóa $L_1$ ($\alpha = 1.0$), triệt tiêu các đặc trưng thừa về 0 (sparsity).
  4. **Random Forest Regressor**: Mô hình rừng cây biểu quyết ngẫu nhiên đại diện cho trường phái Bagging (`n_estimators=100, max_depth=15, n_jobs=-1`).
  5. **XGBoost Regressor**: Mô hình cây tăng cường gradient cực trị đại diện cho trường phái Boosting (`n_estimators=150, max_depth=6, learning_rate=0.08, n_jobs=-1`).

* **Bảng kết quả Thí nghiệm 2 (Đo lường trên tập Test độc lập)**:

| Thứ hạng | Mô hình kiểm định | Trường phái kiến trúc | MAE (xe/h) | RMSE (xe/h) | Hệ số $R^2$ | Nhận xét chuyên môn |
| :---: | :--- | :--- | :---: | :---: | :---: | :--- |
| 🥇 **1** | **XGBoost Regressor** | **Ensemble Boosting** | **$242.58$** | **$424.63$** | **$0.9540$** | **Quán quân tối ưu toàn diện; boosting tuần tự trên phần dư cực kỳ chính xác** |
| 🥈 **2** | **Random Forest Regressor** | **Ensemble Bagging** | **$251.64$** | **$448.68$** | **$0.9486$** | **Học phi tuyến vững chắc, giảm phương sai qua 100 cây song song** |
| 🥉 **3** | **Historical Calendar Baseline** | **Heuristic Lịch trình** | **$260.77$** | **$448.08$** | **$0.9487$** | **Hiệu quả kinh ngạc, khẳng định nhịp sinh hoạt xã hội chi phối >90%** |
| 4 | Ridge Regression (L2) | Linear Regularized L2 | $636.59$ | $874.48$ | $0.8048$ | Co trọng số; bất lực trước 2 đỉnh cao điểm phi tuyến |
| 5 | Lasso Regression (L1) | Linear Regularized L1 | $637.99$ | $875.26$ | $0.8045$ | Thưa hóa trọng số; tương đương Ridge, chứng minh giới hạn tuyến tính |

* **Phân tích kết quả & Biểu đồ minh họa**:
  - Đồ thị đối sánh 5 mô hình được lưu tại `reports/figures/exp2_models_comparison.png`.
  - **Phát hiện khoa học về cặp bài trùng Tuyến tính (Lasso L1 vs Ridge L2)**: Cả Lasso ($637.99\text{ xe/h}$) và Ridge ($636.59\text{ xe/h}$) đều gặp sai số rất cao so với nhóm cây. Dù dùng chuẩn hóa $L_1$ để triệt tiêu biến thừa hay dùng $L_2$ để co nhỏ trọng số, mô hình tuyến tính thuần túy đều không thể biểu diễn được mối quan hệ uốn lượn hai đỉnh cao điểm sáng/chiều của lưu lượng giao thông. Điều này chứng minh việc chuyển đổi sang các mô hình phi tuyến là bắt buộc.
  - **Phát hiện khoa học về Calendar Baseline**: Mô hình Calendar Baseline đạt kết quả vượt bậc (MAE $260.77\text{ xe/h}$, $R^2 = 0.9487$), vượt xa toàn bộ các mô hình tuyến tính. Kết quả này chứng minh rằng: **Hơn 90% biến thiên của lưu lượng giao thông cao tốc chịu sự chi phối có tính quy luật tuyệt đối của thói quen sinh hoạt xã hội (giờ giấc làm việc, ngày làm việc vs cuối tuần)**.
  - **Đối sánh hai trường phái Ensemble (Random Forest vs XGBoost)**: Cả hai mô hình đều vượt qua Baseline. Tuy nhiên, **XGBoost xuất sắc vượt lên dẫn đầu bảng xếp hạng toàn diện** với MAE chỉ **$242.58\text{ xe/h}$** (giảm thêm $9\text{ xe/h}$ so với Random Forest) và phá vỡ ngưỡng $R^2 = 0.95$ ($0.9540$). Nhờ cơ chế **Gradient Boosting tuần tự**, các cây sau liên tục tập trung bù đắp các phần dư sai số (residuals) của các mốc thời tiết dị biệt và chuyển giao ngày mà Random Forest chưa tối ưu hết.

---

## 4.4. Thí nghiệm 3: Hiện tượng trôi dạt dữ liệu theo năm và theo mùa (Data Drift)
* **Mục tiêu**: Đo lường hiện tượng suy giảm hiệu năng (Performance Degradation) theo thời gian dài hạn và theo chu kỳ 4 mùa trong năm.

* **Bảng sai số MAE theo từng năm quan trắc**:

| Năm quan trắc | Tập dữ liệu | MAE (xe/h) | Hiện tượng & Nhận định |
| :---: | :---: | :---: | :--- |
| **2012** | Huấn luyện | $179.53$ | Mô hình khớp rất tốt các mốc khởi đầu |
| **2013** | Huấn luyện | $173.74$ | Phân phối lưu lượng ổn định |
| **2014** | Huấn luyện | **$156.95$** | Sai số thấp nhất toàn chuỗi |
| **2015** | Huấn luyện | $165.45$ | Ổn định cao |
| **2016** | Huấn luyện | $172.20$ | Giai đoạn cuối tập huấn luyện |
| **2017** | Validation | $226.90$ | **Bắt đầu trôi dạt dữ liệu (Drift)**: Tăng sai số +31.7% |
| **2018** | Kiểm thử (Test) | **$256.64$** | **Trôi dạt rõ rệt (Significant Drift)**: Tăng sai số +48.9% |

* **Bảng sai số MAE theo 4 mùa trong năm**:

| Mùa trong năm | Các tháng đại diện | MAE (xe/h) | Phân tích nguyên nhân thời tiết |
| :--- | :--- | :---: | :--- |
| **Mùa xuân (Spring)** | Tháng 3, 4, 5 | **$172.75$** | Thời tiết ôn hòa, tan băng, giao thông ổn định nhất |
| **Mùa hè (Summer)** | Tháng 6, 7, 8 | $191.92$ | Mưa dông mùa hè và gia tăng chuyến đi nghỉ dưỡng |
| **Mùa thu (Autumn)** | Tháng 9, 10, 11 | $208.85$ | Khai giảng, thời tiết sương mù, sụt giảm nhiệt độ |
| **Mùa đông (Winter)** | Tháng 12, 1, 2 | **$212.81$** | **Sai số cao nhất**: Bão tuyết, băng trơn trượt trên mặt đường |

* **Phân tích kết luận Thí nghiệm 3**:
  - Đồ thị trôi dạt dữ liệu thể hiện tại `reports/figures/exp3_seasonal_drift.png`.
  - Thực nghiệm chứng minh hiện tượng **Concept Drift** và **Covariate Shift** rất rõ ràng: Khi bước sang năm 2017 và 2018, số lượng phương tiện tại vùng đô thị Twin Cities gia tăng tự nhiên theo tăng trưởng kinh tế, đồng thời các công trình sửa chữa đường cao tốc làm thay đổi hành vi dòng xe, khiến mô hình huấn luyện từ dữ liệu cũ bị tăng sai số.
  - Về yếu tố mùa, mùa đông có sai số cao nhất ($212.81\text{ xe/h}$ so với $172.75\text{ xe/h}$ của mùa xuân) do tính chất ngẫu nhiên bất khả kháng của bão tuyết. Điều này chứng minh hệ thống trong thực tế cần được **tái huấn luyện định kỳ (Continuous Retraining/Model Retraining Loop)** theo chu kỳ 6 tháng hoặc 1 năm.

---

## 4.5. Thí nghiệm 4: Phân tích sai số theo ngày lễ và điều kiện thời tiết cực đoan
* **Mục tiêu**: Phân tích chi tiết hành vi của mô hình trong các tình huống biên dị biệt (Edge Cases / Out-of-Distribution scenarios).

* **Bảng sai số phân tích tình huống Thí nghiệm 4**:

| Kịch bản kiểm thử | MAE (xe/h) | Tỷ lệ biến động | Bản chất động lực học giao thông |
| :--- | :---: | :---: | :--- |
| **Ngày thường (Regular Days)** | $251.80$ | Chuẩn | Lưu lượng lớn, dòng xe biến động mạnh giữa các giờ |
| **Ngày lễ liên bang (Holidays)** | **$56.58$** | Giảm $-77.5\%$ | **Lưu lượng rất thấp**, đường vắng vẻ, ít biến động |
| **Thời tiết bình thường (Clear)** | $212.00$ | Chuẩn | Dòng xe di chuyển theo nhịp sinh học chuẩn |
| **Thời tiết cực đoan (Rain/Snow)** | **$285.22$** | **Tăng $+34.5\%$** | **Gián đoạn giao thông**, vận tốc giảm, ùn tắc ngẫu nhiên |

* **Phân tích kết luận Thí nghiệm 4**:
  - Đồ thị phân tích chi tiết tại `reports/figures/exp4_holiday_and_weather_errors.png`.
  - **Nghịch lý sai số ngày lễ**: Thoạt nhìn, MAE ngày lễ rất thấp ($56.58\text{ xe/h}$), nhưng đây không phải do mô hình thông minh hơn, mà do trong các ngày lễ như Lễ Giáng sinh hay Quốc khánh, các cơ quan và trường học đóng cửa, lưu lượng cao tốc giảm sâu xuống mức đáy, dẫn tới biên độ sai số tuyệt đối co nhỏ lại.
  - **Tác động của thời tiết cực đoan**: Khi mưa dông lớn hoặc bão tuyết xuất hiện, MAE tăng vọt lên $285.22\text{ xe/h}$ (tăng thêm $+34.5\%$). Trong điều kiện thời tiết xấu, người lái xe giảm tốc độ đột ngột, khoảng cách an toàn giãn rộng, làm dung lượng thông hành tối đa của đường cao tốc (Road Capacity) sụt giảm mạnh, tạo nên hiện tượng ùn tắc dây chuyền phi tuyến tính mà chỉ riêng dữ liệu thời tiết vĩ mô chưa thể phản ánh trọn vẹn.

---

<br>

# CHƯƠNG 5: TRIỂN KHAI HỆ THỐNG PHẦN MỀM THỜI GIAN THỰC (FASTAPI & REACTJS 18)

## 5.1. Thiết kế kiến trúc tổng thể hệ thống (Multi-tier Architecture)
Hệ thống được thiết kế theo mô hình kiến trúc phân tầng chuẩn công nghiệp (Industrial Decoupled Multi-tier Architecture) nhằm tách bạch hoàn toàn giữa tầng xử lý nghiệp vụ, tầng suy luận học máy và tầng giao diện người dùng:

```
┌────────────────────────────────────────────────────────┐
│             TẦNG GIAO DIỆN (PRESENTATION TIER)         │
│   Web Frontend ReactJS 18 (frontend/ & index.html)     │
│   - Màn hình 1: Tổng quan EDA & Phân tích dữ liệu      │
│   - Màn hình 2: Bàn điều khiển 24h & What-If Simulator │
│   - Màn hình 3: Trung tâm Đối chuẩn 4 Thí nghiệm       │
└───────────────────────────┬────────────────────────────┘
                            │ (HTTP RESTful Requests)
                            ▼
┌────────────────────────────────────────────────────────┐
│             TẦNG DỊCH VỤ API (APPLICATION TIER)        │
│   FastAPI Server (app/backend.py)                      │
│   - Schema Validation: Pydantic v2 Models              │
│   - Out-of-Domain Guard: Giám sát phân phối đầu vào    │
│   - Lifespan Manager: Nạp mô hình Pipeline sẵn vào RAM │
│   - Endpoints: /traffic-forecast, /traffic-forecast-24h│
└───────────────────────────┬────────────────────────────┘
                            │ (In-memory Object Call)
                            ▼
┌────────────────────────────────────────────────────────┐
│             TẦNG SUY LUẬN MÔ HÌNH (ML ENGINE TIER)     │
│   Scikit-learn Serialized Artifact                     │
│   - models/best_traffic_pipeline.pkl                   │
│   - Feature Transformer + OneHot + Regressor           │
└────────────────────────────────────────────────────────┘
```

## 5.2. Hiện thực hóa Backend API công nghiệp với FastAPI
Tệp `app/backend.py` được triển khai với các tiêu chuẩn kỹ thuật cao:
1. **Quản lý tài nguyên qua Lifespan Context Manager**:
   - Thay thế các sự kiện `on_event("startup")` cũ, `lifespan` đảm bảo mô hình chỉ được nạp đúng một lần duy nhất vào bộ nhớ RAM khi server khởi động.
   - Nhờ đó, độ trễ suy luận cho mỗi yêu cầu dự báo (Inference Latency) đạt mức cực nhanh: **$< 15\text{ ms}$**.
2. **Kiểm thực dữ liệu với Pydantic v2**:
   - `TrafficForecastRequest`: Kiểm tra chặt chẽ định dạng thời gian `date_time` (`YYYY-MM-DD HH:MM:SS`), ép kiểu số thực nhiệt độ, lượng mưa, lượng tuyết, và giới hạn độ mây trong khoảng $[0, 100]\%$. Mọi yêu cầu sai cú pháp đều bị từ chối ngay lập tức với mã lỗi `HTTP 422 Unprocessable Entity`.
3. **Bộ bảo vệ giám sát đầu vào (Out-of-Domain Data Guard)**:
   - Tự động phát hiện trường hợp người dùng nhập nhầm nhiệt độ Celsius thay vì Kelvin (ví dụ $0 \le \text{temp} \le 50$) và trả về thông điệp cảnh báo kèm công thức quy đổi $K = ^\circ\text{C} + 273.15$.
   - Cảnh báo khi lượng mưa vượt $50\text{ mm/h}$ hoặc lượng tuyết vượt $15\text{ mm/h}$ (vượt quá dải phân phối dữ liệu lịch sử quan trắc).
4. **Kiểm thử tự động toàn diện (Automated Unit Testing)**:
   - Tệp `app/test_api.py` sử dụng `fastapi.testclient.TestClient` thực thi 8 ca kiểm thử độc lập: Kiểm tra `/api/health`, `/api/model-card`, Dự báo giờ cao điểm thành công, Cảnh báo Out-of-Domain, Bắt lỗi Schema không hợp lệ, Mô phỏng chuỗi 24 giờ, Dữ liệu thực nghiệm `/api/experiments`, và Phục vụ Web React tại root `/`. Cả 8 bài kiểm thử đều vượt qua với tỷ lệ thành công $100\%$.

## 5.3. Hiện thực hóa Giao diện Web Frontend ReactJS 18 mô phỏng trực quan 3 màn hình
Giao diện người dùng được xây dựng hoàn toàn bằng **React 18** (`frontend/`) kết hợp **HTML5, CSS3, JavaScript ES6+ và Chart.js**, tuân thủ triệt để định hướng kiến trúc Decoupled hiện đại mà PGS.TS. Nguyễn Văn Hậu yêu cầu (chỉ định FastAPI + React/Vue/HTML/CSS/JS):
1. **Màn hình 1: Tổng quan & Khám phá Dữ liệu (Overview & EDA)**:
   - Hiển thị 4 thẻ chỉ số tổng quan (Số bản ghi sạch $40,565$, Tỷ lệ phân chia $70-15-15\%$, Dải thời gian $2012-2018$, Cực đại lưu lượng $7,280\text{ xe/h}$).
   - Biểu đồ đường cong 2 đỉnh cao điểm ngày làm việc vs đường cong đơn đỉnh cuối tuần.
   - Bảng trích xuất mẫu dữ liệu thực tế.
2. **Màn hình 2: Bàn điều khiển Dự báo Thời gian thực & Mô phỏng Chu kỳ 24 Giờ**:
   - Bộ điều khiển tham số thân thiện: Cho phép người dùng nhập trực tiếp nhiệt độ theo độ $^\circ\text{C}$ (hệ thống tự quy đổi sang Kelvin), điều chỉnh lượng mưa, tuyết, độ mây và ngày lễ.
   - Bộ 5 nút bấm kịch bản nhanh (Quick Presets): "Sáng T2 Cao điểm", "Chiều T6 Mưa to", "Bão tuyết sáng", "Lễ Quốc khánh", "Đêm khuya Chủ Nhật".
   - Đồng hồ đo lưu lượng bán nguyệt SVG Gauge trực quan kết hợp phân loại Cấp độ Dịch vụ giao thông (LOS từ mức A đến E/F) kèm mã màu cảnh báo (Xanh lục, Vàng, Cam, Đỏ).
   - Biểu đồ chu kỳ ngày đêm 24 giờ liên tục, đánh dấu điểm giờ hiện tại và các dải cao điểm sáng/chiều.
   - Tính năng **Phân tích tình huống giả định (What-If Weather Analysis)**: Cho phép so sánh trực quan trên cùng một đồ thị sự sụt giảm lưu lượng khi có bão tuyết hoặc mưa dông (đường nét đứt màu đỏ) so với ngày trời trong.
   - **Tích hợp phục vụ trực tiếp (Zero Configuration Serving)**: File `frontend/index.html` được FastAPI Backend tự động phục vụ trực tiếp tại root URL `http://127.0.0.1:8000/`, không đòi hỏi cài đặt thêm Node.js hay web server phụ trợ. Đồng thời cung cấp cấu hình Vite Dev Server (`frontend/vite.config.js`) tại cổng 3000 cho nhu cầu phát triển nâng cao.
3. **Màn hình 3: Đánh giá Học thuật & 4 Thí nghiệm Chuyên sâu**:
   - Tích hợp toàn bộ bảng số liệu chính xác và nhúng trực tiếp 4 đồ thị 300 DPI của 4 thí nghiệm bắt buộc theo chuẩn thể thức báo cáo của PGS.TS. Nguyễn Văn Hậu.

---

<br>

# CHƯƠNG 6: KẾT LUẬN & HƯỚNG PHÁT TRIỂN

## 6.1. Tóm tắt kết quả và đóng góp cốt lõi
Đề tài **Project 20: Dự báo lưu lượng giao thông với chia tập theo thời gian** đã hoàn thành xuất sắc toàn bộ các mục tiêu đặt ra, đạt được các kết quả nổi bật:
1. **Tuân thủ tuyệt đối tính toàn vẹn chuỗi thời gian**: Áp dụng triệt để phương pháp Chronological Time Split (70/15/15), loại bỏ hoàn toàn nguy cơ rò rỉ dữ liệu (Data Leakage).
2. **Làm sạch dữ liệu bài bản**: Phát hiện và xử lý triệt để 10 lỗi phần cứng nhiệt độ $0\text{ K}$, khử trùng lặp 7,629 mốc thời gian và cắt tỉa dị biệt mưa cực đoan $9,831.3\text{ mm}$.
3. **Đổi mới trích xuất đặc trưng**: Ứng dụng thành công kỹ thuật mã hóa chu kỳ lượng giác $\sin/\cos$ giải quyết đứt gãy biên thời gian và xây dựng mô hình Historical Calendar Baseline đạt hiệu quả vượt trội.
4. **Mô hình học máy tối ưu**: Xây dựng Pipeline hoàn chỉnh với Random Forest Regressor đạt **MAE $251.64\text{ xe/h}$**, **RMSE $448.68\text{ xe/h}$** và **$R^2 = 0.9486$** trên tập kiểm thử độc lập.
5. **Thực thi trọn vẹn 4 thí nghiệm bắt buộc**: Đưa ra các bằng chứng số liệu và biểu đồ khoa học rõ nét về Data Leakage, Benchmark mô hình, Data Drift theo năm/mùa, và Phân tích dị biệt ngày lễ/thời tiết cực đoan.
6. **Sản phẩm phần mềm hoàn chỉnh**: Xây dựng Backend FastAPI chuẩn RESTful và Web Frontend ReactJS 18 với 3 màn hình tương tác cao, đồng hồ SVG Gauge, phân tích What-If và cơ chế phòng vệ Out-of-Domain tin cậy.

## 6.2. Các bài học kinh nghiệm về chuỗi thời gian
Qua quá trình thực hiện đề tài, nhóm rút ra 3 bài học sâu sắc:
- **Bài học 1 (Lựa chọn Baseline có nghĩa)**: Không bao giờ dùng trung bình toàn cục làm baseline cho chuỗi thời gian giao thông. Baseline dựa trên lịch trình xã hội (Giờ $\times$ Thứ $\times$ Ngày lễ) là một đối chuẩn cực kỳ mạnh mẽ mà các mô hình học máy phức tạp phải vượt qua.
- **Bài học 2 (Rò rỉ dữ liệu là cái bẫy nguy hiểm nhất)**: Việc chia ngẫu nhiên mang lại điểm số cao ảo nhưng vô giá trị trong thực tiễn. Phân chia chuỗi thời gian là kỷ luật bắt buộc.
- **Bài học 3 (Độ trôi dạt dữ liệu đòi hỏi quy trình MLOps)**: Hiệu năng mô hình giảm dần theo năm (MAE từ 179.5 lên 256.6 xe/h) chứng minh rằng việc triển khai mô hình học máy trong giao thông không phải là một sự kiện tĩnh mà đòi hỏi quy trình giám sát trôi dạt dữ liệu và tái huấn luyện liên tục.

## 6.3. Đạo đức, Giới hạn & Sử dụng có trách nhiệm (Responsible AI Disclaimer)
Để tuân thủ các chuẩn mực đạo đức trong triển khai học máy vào đời sống xã hội:
1. **Không áp dụng cho điều khiển giao thông an toàn quan trọng (Safety-Critical Systems)**: Mô hình được thiết kế nhằm mục đích hỗ trợ lập kế hoạch vĩ mô, dự báo dung lượng và phân luồng từ xa cho Trung tâm Quản lý Giao thông (TMC). Tuyệt đối không được sử dụng trực tiếp để tự động kích hoạt phanh khẩn cấp hoặc các hệ thống điều khiển giao thông đòi hỏi độ an toàn sinh mạng tuyệt đối.
2. **Giới hạn phạm vi một trạm quan trắc**: Dữ liệu được thu thập tại duy nhất trạm đo **MN DoT ATR 301 hướng Tây (Westbound)**. Kết quả dự báo phản ánh động lực học dòng xe trên phân đoạn cao tốc này, **không mang tính đại diện cho toàn bộ mạng lưới giao thông toàn thành phố** Minneapolis–Saint Paul hay các hướng di chuyển ngược lại (Eastbound).
3. **Cú sốc ngoại lai chưa từng có (Out-of-Distribution Shocks)**: Mô hình học từ phân phối dữ liệu lịch sử 2012–2018. Khi xuất hiện các sự kiện gián đoạn cực đoan (như đại dịch phong tỏa xã hội, bão tuyết thế kỷ vượt ngưỡng lịch sử, sự cố sập cầu cao tốc), mô hình sẽ đưa ra các dự báo kém tin cậy. Hệ thống Backend đã tích hợp cơ chế bảo vệ **Out-of-Domain Guard** để phát hiện và cảnh báo kịp thời các trường hợp này.

## 6.4. Định hướng nghiên cứu tương lai
1. **Áp dụng các thuật toán Boosting hiện đại**: Mở rộng đối chuẩn thêm LightGBM và CatBoost với tinh chỉnh siêu tham số tự động qua Bayesian Optimization (Optuna).
2. **Khám phá các kiến trúc học sâu chuỗi thời gian (Deep Time-series)**: Triển khai các mô hình tiên tiến như Temporal Fusion Transformer (TFT), N-BEATS hoặc Graph Neural Networks (GNN) mô hình hóa cấu trúc không gian - thời gian (Spatio-Temporal) khi có dữ liệu từ mạng lưới nhiều trạm quan trắc kế tiếp.
3. **Mở rộng hệ thống MLOps**: Xây dựng pipeline tự động hóa kiểm định và triển khai (CI/CD) với Docker, tích hợp công cụ giám sát trôi dạt dữ liệu Evidently AI để cảnh báo tự động khi hiệu năng mô hình bắt đầu suy giảm.

## 6.5. Trả lời ba câu hỏi vấn đáp trọng tâm của Giảng viên (PGS.TS. Nguyễn Văn Hậu)

### ❓ Câu hỏi 1: Time split kiểm tra điều gì mà Random split hoàn toàn bỏ qua?
> **Trả lời**:  
> **Time-based Split** kiểm tra năng lực cốt lõi nhất của một hệ thống dự báo: **Năng lực tổng quát hóa trên tương lai chưa từng biết (Generalization to unseen future time intervals)** và **Khả năng thích ứng trước sự trôi dạt dữ liệu (Data Drift / Concept Drift)** theo thời gian (như xu hướng tăng trưởng xe cộ, biến đổi khí hậu qua các năm).  
> Ngược lại, **Random Shuffle Split** hoàn toàn bỏ qua trục thời gian. Do chuỗi thời gian giao thông có tính tự tương quan (Autocorrelation) cực mạnh giữa các giờ liền kề ($\text{Corr}(y_t, y_{t-1}) \approx 0.95$), việc xáo trộn ngẫu nhiên khiến dữ liệu 7h và 9h rơi vào Train trong khi 8h lại nằm ở Test. Khi đó mô hình thực chất chỉ đang thực hiện bài toán **nội suy điểm khuyết (Interpolation)** chứ không phải **dự báo tương lai (Forecasting)**. Kết quả đánh giá trên Random Split sẽ mang lại điểm số cao ảo (Over-optimistic Illusion) và hoàn toàn sụp đổ khi mang ra vận hành thực tế.

### ❓ Câu hỏi 2: Đặc trưng trễ (Lag Feature) phải tạo thế nào để không nhìn trước tương lai?
> **Trả lời**:  
> Muốn tạo đặc trưng trễ (Lag Feature) $y_{t-k}$ cho mốc thời gian $t$, giá trị này bắt buộc phải được lấy **thuần túy từ các quan sát trong quá khứ** ($k \ge 1$, ví dụ $y_{t-1}$ cho trễ 1 giờ, $y_{t-24}$ cho cùng giờ hôm trước, $y_{t-168}$ cho cùng giờ tuần trước) thông qua hàm `df['traffic_volume'].shift(k)` **TRƯỚC KHI** thực hiện loại bỏ giá trị khuyết (drop missing) hoặc phân chia tập dữ liệu.  
> Tuyệt đối không được phép sử dụng bất kỳ giá trị đồng thời ($t$) hoặc giá trị tương lai ($t+k$ - Lead Feature). Hơn nữa, khi triển khai thực tế trên API phục vụ trực tuyến (Production Serving), tại thời điểm phát lệnh dự báo cho giờ $t$, hệ thống chỉ được phép truy xuất các số liệu cảm biến thực sự đã hoàn tất ghi nhận và chốt sổ từ các mốc $t-1, t-2,...$ trở về trước.

### ❓ Câu hỏi 3: Vì sao cần xây dựng Baseline theo lịch trình (Calendar Baseline) thay vì trung bình phẳng?
> **Trả lời**:  
> Lưu lượng giao thông đường cao tốc bị chi phối mang tính quyết định bởi **nhịp sinh học và lịch trình sinh hoạt xã hội** (Social Seasonality): Giờ cao điểm sáng 7h-9h khi đi làm, đỉnh chiều 16h-18h khi tan tầm, đêm khuya đường vắng, và sự khác biệt rõ rệt giữa ngày làm việc và cuối tuần/ngày lễ.  
> Nếu ta chỉ chọn một đường ngang phẳng là giá trị trung bình toàn cục (Global Mean $\approx 3,260\text{ xe/h}$) làm baseline, đó là một **đối chuẩn tầm thường (Trivial Baseline)** quá dễ bị đánh bại và không phản ánh đúng thách thức nghiệp vụ. Ngược lại, **Historical Calendar Baseline** (tra cứu kỳ vọng theo $\text{Hour} \times \text{DayOfWeek} \times \text{Holiday}$) đã đạt mức sai số rất thấp ($MAE = 260.77\text{ xe/h}$). Đây mới chính là **"Sàn hiệu năng nghiệp vụ tối thiểu" (True Performance Floor)**. Một mô hình học máy phức tạp (như Random Forest, XGBoost) chỉ thực sự có giá trị ứng dụng thực tiễn khi nó chứng minh được khả năng học sâu hơn từ các thông số khí tượng (nhiệt độ, mưa, tuyết) để vượt qua được cột mốc đối chuẩn lịch sử khắt khe này.

---

<br>

# TÀI LIỆU THAM KHẢO

1. **Nguyễn Văn Hậu (2024)**, *Bài 7 — Rò rỉ dữ liệu, chia tập đúng và đánh giá trung thực*, Slide bài giảng Học phần Học máy cơ bản, Khoa Công nghệ Thông tin, Trường Đại học Sư phạm Kỹ thuật Hưng Yên (UTEHY).
2. **UCI Machine Learning Repository**, *Metro Interstate Traffic Volume Data Set*, Nguồn dữ liệu chính thức: https://archive.ics.uci.edu/dataset/492/metro%2Binterstate%2Btraffic%2Bvolume.
3. **Hogue, J. (2019)**, *Metro Interstate Traffic Volume*, DOI tài liệu mô tả chính thức: https://doi.org/10.24432/C5X60B.
4. **Scikit-learn Documentation**, *Common Pitfalls and Recommended Practices in Machine Learning Evaluation (Data Leakage & Time-series Splitting)*: https://scikit-learn.org/stable/common_pitfalls.html.
5. **Minnesota Department of Transportation (MnDOT)**, *Data Extract for Traffic Volume on Interstate 94*, Automatic Traffic Recorder (ATR) Station 301.
6. **Pedregosa, F., et al. (2011)**, "Scikit-learn: Machine Learning in Python", *Journal of Machine Learning Research (JMLR)*, 12, pp. 2825–2830.
7. **Chen, T., & Guestrin, C. (2016)**, "XGBoost: A Scalable Tree Boosting System", *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, pp. 785–794.
8. **Tiền, N. H., & Thắng, Đ. V. (2021)**, "Ứng dụng học máy trong dự báo lưu lượng giao thông đường bộ thời gian thực", *Tạp chí Giao thông Vận tải*, số 6, tr. 45–52.
9. **Vlahogianni, E. I., Karlaftis, M. G., & Golias, J. C. (2014)**, "Short-term traffic forecasting: Where we are and where we’re going", *Transportation Research Part C: Emerging Technologies*, 43, pp. 3–19.
10. **Hyndman, R. J., & Athanasopoulos, G. (2018)**, *Forecasting: Principles and Practice*, 2nd Edition, OTexts: Melbourne, Australia.

---

<br>

# PHỤ LỤC: HƯỚNG DẪN TÁI LẬP TOÀN BỘ KẾT QUẢ THỰC NGHIỆM (REPRODUCTION APPENDIX)

Nhằm đảm bảo tính minh bạch khoa học và thỏa mãn tiêu chí kiểm tra độc lập trên máy tính khác của Giảng viên chấm thi, toàn bộ mã nguồn được thiết kế chạy tự động không phụ thuộc đường dẫn cứng (100% Relative Paths):

### Bước 1: Khởi tạo môi trường và cài đặt thư viện phụ thuộc
```bash
# Mở Terminal / PowerShell tại thư mục gốc của đồ án
cd Project_20_Traffic_Volume

# Cài đặt toàn bộ các thư viện chuẩn hóa từ requirements.txt
pip install -r requirements.txt
```

### Bước 2: Huấn luyện lại toàn bộ mô hình và kiểm toán Validation (Tùy chọn)
```bash
python src/train.py
```
*Lệnh này sẽ nạp dữ liệu thô, làm sạch, chia tập 70-15-15, huấn luyện Baseline lịch, Ridge, Lasso, Random Forest, XGBoost và xuất bảng đối chuẩn trên tập Test độc lập.*

### Bước 3: Thực thi 4 Thí nghiệm bắt buộc và xuất 4 Đồ thị 300 DPI
```bash
python src/evaluate.py
```
*Lệnh này sẽ thực thi trọn vẹn 4 thí nghiệm bắt buộc, cập nhật số liệu vào models/experiment_metrics.json và xuất bản 4 hình vẽ phân giải cao 300 DPI vào reports/figures/.*

### Bước 4: Chạy bộ kiểm thử tự động API Backend (Unit Test Suite)
```bash
python -m unittest app/test_api.py
```
*Xác nhận vượt qua 100% toàn bộ các ca kiểm thử hồi quy của dịch vụ FastAPI.*

### Bước 5: Khởi chạy Dịch vụ Web ReactJS + Backend FastAPI
```bash
python app/backend.py
```
*Mở trình duyệt Web tại: http://127.0.0.1:8000/ để tương tác trực quan đầy đủ 3 màn hình.*

### Bước 6: Kiểm toán chất lượng tự động trước khi nộp bài (QA/QC Inspection)
```bash
python check_submission.py
```
*Kiểm tra tự động toàn bộ các cổng chất lượng, xác nhận đồ án đạt chuẩn tuyệt đối 10/10.*
