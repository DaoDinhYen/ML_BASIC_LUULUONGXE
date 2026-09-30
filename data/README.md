# HỒ SƠ DỮ LIỆU: METRO INTERSTATE TRAFFIC VOLUME
## (DATA CARD & DATASET SPECIFICATION)

**Đề tài**: Project 20 — Dự báo lưu lượng giao thông với chia tập theo thời gian  
**Học phần**: Học máy cơ bản (Lớp 12523W.1) — **Giảng viên hướng dẫn**: PGS. TS. Nguyễn Văn Hậu  
**Khoa Công nghệ Thông tin — Trường Đại học Sư phạm Kỹ thuật Hưng Yên (UTEHY)**  
**Nhóm sinh viên thực hiện**: Nguyễn Văn An (MSV: 12523001) & Trần Thị Bình (MSV: 12523002)

---

## 📌 1. NGUỒN GỐC & THÔNG TIN ĐỊNH DANH BỘ DỮ LIỆU

* **Tên bộ dữ liệu**: Metro Interstate Traffic Volume
* **Nguồn cung cấp chính thức**: UCI Machine Learning Repository
  * **Trang web dữ liệu**: [https://archive.ics.uci.edu/dataset/492/metro%2Binterstate%2Btraffic%2Bvolume](https://archive.ics.uci.edu/dataset/492/metro%2Binterstate%2Btraffic%2Bvolume)
  * **DOI chính thức**: [https://doi.org/10.24432/C5X60B](https://doi.org/10.24432/C5X60B)
* **Tổ chức thu thập dữ liệu gốc**: Sở Giao thông Vận tải bang Minnesota, Hoa Kỳ (Minnesota Department of Transportation - MnDOT).
* **Người đóng góp (Donor)**: John Hogue (john.d.hogue '@' gmail.com).
* **Giấy phép bản quyền (License)**: **Creative Commons Attribution 4.0 International (CC BY 4.0)**.
  * *Quyền sử dụng*: Cho phép tự do chia sẻ, sao chép, phân phối và tùy biến dữ liệu phục vụ nghiên cứu khoa học và giáo dục với điều kiện ghi công đúng tác giả.
* **Trích dẫn khoa học chuẩn (Citation)**:
  > Hogue, J. (2019). Metro Interstate Traffic Volume [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5X60B
* **Tệp dữ liệu sử dụng**: `data/Metro_Interstate_Traffic_Volume.csv`
  * **Kích thước tệp thô**: 3,237,208 bytes (~3.24 MB).
  * **Mã băm toàn vẹn (SHA-256 Checksum)**: `749c90d720360a4215bb15345526073c079ba4cc95e3fa558796d083f85fce9e`
  * **Khoảng thời gian quan trắc**: Từ **02/10/2012 09:00:00** đến **30/09/2018 23:00:00** (~6 năm liên tục).

---

## 📍 2. PHẠM VI KHÔNG GIAN & ĐẶC TẢ TRẠM QUAN TRẮC

* **Tuyến đường**: Tuyến đường cao tốc liên bang **Interstate 94 (I-94)**.
* **Khu vực địa lý**: Đoạn hành lang giữa hai thành phố kết nghĩa Minneapolis và Saint Paul (vùng đô thị Twin Cities), bang Minnesota, Hoa Kỳ.
* **Trạm quan trắc**: Trạm đếm lưu lượng giao thông tự động **MN DoT ATR Station 301** (Automatic Traffic Recorder).
* **Hướng di chuyển (Direction)**: **Westbound (Hướng Tây)** — Các phương tiện di chuyển theo hướng từ Saint Paul sang Minneapolis.
* **Đơn vị quan sát (Observation Unit)**: Một giờ đồng hồ tại mặt cắt ngang của trạm đo ATR 301.

---

## 📖 3. TỪ ĐIỂN DỮ LIỆU (DATA DICTIONARY)

Bộ dữ liệu thô bao gồm **48,204 bản ghi** và **9 trường thuộc tính**, được đặc tả chi tiết như sau:

| STT | Tên thuộc tính | Kiểu dữ liệu | Đơn vị đo | Vai trò | Miền giá trị | Thời điểm khả dụng | Mô tả ý nghĩa nghiệp vụ |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| 1 | `date_time` | `datetime` | YYYY-MM-DD HH:MM:SS | Time Identifier | 2012-10-02 đến 2018-09-30 | Có sẵn trước | Mốc thời gian quan trắc theo giờ địa phương (CST/CDT). |
| 2 | `holiday` | `string` | Tên ngày lễ | Feature (Categorical) | 11 ngày lễ liên bang hoặc 'None' | Có sẵn trước (Lịch) | Tên ngày lễ quốc gia Hoa Kỳ (Labor Day, Thanksgiving, Christmas Day,...) |
| 3 | `temp` | `float` | Kelvin (K) | Feature (Numeric) | $0.0 - 310.07\text{ K}$ (Thực tế sau làm sạch: $243 - 310\text{ K}$) | Dự báo thời tiết | Nhiệt độ không khí trung bình trong giờ quan trắc. |
| 4 | `rain_1h` | `float` | mm | Feature (Numeric) | $0.0 - 9,831.3\text{ mm}$ (Thực tế sau clip: $0 - 100\text{ mm}$) | Dự báo thời tiết | Lượng mưa tích lũy đo được trong 1 giờ quan trắc. |
| 5 | `snow_1h` | `float` | mm | Feature (Numeric) | $0.0 - 0.51\text{ mm}$ | Dự báo thời tiết | Lượng tuyết rơi tích lũy đo được trong 1 giờ quan trắc. |
| 6 | `clouds_all` | `integer` | Phần trăm (%) | Feature (Numeric) | $0 - 100\%$ | Dự báo thời tiết | Tỷ lệ mây che phủ bầu trời do trạm khí tượng ghi nhận. |
| 7 | `weather_main` | `string` | Danh mục | Feature (Categorical) | 11 loại (Clear, Clouds, Rain, Snow, Mist, Fog, Thunderstorm,...) | Dự báo thời tiết | Nhóm phân loại thời tiết chính trong giờ quan trắc. |
| 8 | `weather_description`| `string` | Văn bản mô tả | Feature (Text/Sub-category) | 38 mô tả chi tiết (light rain, heavy snow, sky is clear,...) | Dự báo thời tiết | Mô tả chi tiết trạng thái khí tượng (được giản lược qua `weather_main`). |
| 9 | `traffic_volume` | `integer` | Xe / giờ | **Target (Mục tiêu)** | $0 - 7,280\text{ xe/h}$ | Chỉ biết sau giờ $t$ | Tổng số lượng phương tiện lưu thông qua trạm ATR 301 hướng Tây trong giờ $t$. |

---

## 🔍 4. BÁO CÁO KIỂM TOÁN CHẤT LƯỢNG DỮ LIỆU (DATA QUALITY AUDIT)

Quy trình tiền xử lý và làm sạch dữ liệu trong module `src/data.py` được thực thi với các phát hiện và can thiệp kỹ thuật cụ thể:

### 4.1. Trùng lặp mốc thời gian (`date_time` Duplicates)
* **Thực trạng**: Bộ dữ liệu thô có **$7,629$ bản ghi trùng mốc `date_time`**. Nguyên nhân là do trạm khí tượng địa phương ghi nhận đồng thời nhiều hiện tượng thời tiết phụ trong cùng một giờ (ví dụ vừa có 'Rain' vừa có 'Mist').
* **Xử lý**: Loại bỏ trùng lặp và giữ bản ghi quan sát đầu tiên (`drop_duplicates(subset=['date_time'], keep='first')`), đưa dữ liệu về **$40,565$ mốc giờ duy nhất**.

### 4.2. Lỗi cảm biến nhiệt độ phần cực đoan ($0.0\text{ Kelvin}$)
* **Thực trạng**: Phát hiện **$10$ bản ghi có nhiệt độ $0.0\text{ Kelvin}$** (tương đương $-273.15^\circ\text{C}$ — độ không tuyệt đối phi lý trong khí quyển Trái Đất). Đây là lỗi gián đoạn tín hiệu phần cứng của cảm biến nhiệt độ.
* **Xử lý**: Lọc bỏ an toàn $10$ bản ghi lỗi này (`df = df[df['temp'] > 0.0]`) hoặc gán bằng trung vị lịch sử của tháng tương ứng, không để giá trị phi vật lý làm sai lệch độ dốc mô hình.

### 4.3. Ngoại lệ lượng mưa cực đoan do tràn bộ đếm (`rain_1h` Outliers)
* **Thực trạng**: Ngày 11/07/2016, cảm biến ghi nhận lượng mưa **$9,831.3\text{ mm/h}$**. Đây là mức mưa bất khả thi (kỷ lục thế giới chỉ khoảng $305\text{ mm/h}$), gây ra bởi lỗi tràn bit bộ tích lũy đo mưa.
* **Xử lý**: Cắt tỉa (clip) tại ngưỡng an toàn $100.0\text{ mm/h}$ (`df['rain_1h'] = df['rain_1h'].clip(upper=100.0)`).

### 4.4. Xử lý giá trị rỗng cột `holiday`
* **Thực trạng**: Cột `holiday` có **$48,143$ dòng để trống** do chỉ có các ngày lễ lớn mới được ghi tên.
* **Xử lý**: Thay thế toàn bộ các giá trị trống/NaN thành chuỗi `'None'` rõ ràng (`df['holiday'] = df['holiday'].replace({'': 'None', np.nan: 'None'})`).

### 4.5. Thống kê dữ liệu sau làm sạch chuẩn mực
* **Số dòng dữ liệu sạch cuối cùng**: **$40,565$ dòng**.
* **Phân phối biến mục tiêu `traffic_volume`**:
  * Giá trị nhỏ nhất (Min): $0\text{ xe/h}$
  * Tứ phân vị thứ nhất (Q1): $1,193\text{ xe/h}$
  * Trung vị (Median): $3,380\text{ xe/h}$
  * Giá trị trung bình (Mean): $3,259.8\text{ xe/h}$
  * Tứ phân vị thứ ba (Q3): $4,933\text{ xe/h}$
  * Giá trị lớn nhất (Max): $7,280\text{ xe/h}$
  * Độ lệch chuẩn (Std): $1,986.8\text{ xe/h}$

---

## ⏳ 5. CHIẾN LƯỢC PHÂN CHIA CHUỖI THỜI GIAN (CHRONOLOGICAL TIME SPLIT)

Tuân thủ nghiêm ngặt phương pháp luận **Bài 7: Rò rỉ dữ liệu, chia tập đúng và đánh giá trung thực**:
* Tuyệt đối **KHÔNG** sử dụng `train_test_split(..., shuffle=True)` trong quy trình đánh giá chính.
* Phân chia xuôi dòng theo trục thời gian với tỷ lệ $70\% - 15\% - 15\%$:

```text
Trục thời gian: 2012-10-02 ──────────────────────► 2017-05-18 ────────► 2018-01-20 ────────► 2018-09-30
Tập dữ liệu:    [==== TẬP TRAIN (70%) ====]       [= TẬP VAL (15%) =]   [= TẬP TEST (15%) =]
Số lượng mẫu:   28,395 bản ghi                    6,085 bản ghi         6,085 bản ghi
Mục đích:       Học trọng số, imputer, scaler     Chọn siêu tham số     Khóa niêm phong, đánh giá 1 lần
```

---

## 📥 6. HƯỚNG DẪN TÁI TẠO VÀ TẢI DỮ LIỆU TỰ ĐỘNG

Dữ liệu gốc đã được đính kèm sẵn trong thư mục `data/Metro_Interstate_Traffic_Volume.csv`. Trong trường hợp cần tải lại trực tiếp từ nguồn chính thức của UCI:

```bash
# Tải tệp nén gốc từ UCI Machine Learning Repository
curl -o data/Metro_Interstate_Traffic_Volume.csv.gz https://archive.ics.uci.edu/static/public/492/metro+interstate+traffic+volume.zip

# Hoặc tải trực tiếp bằng script Python:
python -c "
import urllib.request, zipfile, io, os
url = 'https://archive.ics.uci.edu/static/public/492/metro+interstate+traffic+volume.zip'
print('Đang tải dữ liệu từ UCI Repository...')
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    with zipfile.ZipFile(io.BytesIO(resp.read())) as z:
        z.extractall('data/')
print('Tải và giải nén thành công vào thư mục data/!')
"
```
