# LAB 8 — KIỂM THỬ HIỆU NĂNG VỚI APACHE JMETER

**Sinh viên:** Trần Văn Nhật · **MSSV:** 23010625  
**Môn học:** Kiểm thử phần mềm · **Bài thực hành:** Lab 8

> **Trạng thái:** Đã xây dựng mã nguồn API và test plan JMeter. **Chưa có bằng chứng chạy JMeter thực tế hoặc ảnh chụp kết quả.** Sau khi chạy theo hướng dẫn, bổ sung ảnh và số liệu đo được vào các mục phía dưới. Không coi số lần gửi dự kiến là số liệu kiểm thử thực tế.

## 1. Mục tiêu

- Tìm hiểu Apache JMeter: Test Plan, Thread Group, HTTP Request, Assertions và Listener.
- Tạo hệ thống API nhỏ để kiểm thử trên **localhost**, tránh gây tải lên website của bên thứ ba.
- Thiết kế tải đồng thời và đo thời gian phản hồi, throughput, tỷ lệ lỗi, percentiles.
- Chụp ảnh màn hình cấu hình và kết quả, đưa vào README của GitHub.

## 2. Lý thuyết Apache JMeter

Apache JMeter là công cụ mã nguồn mở dùng để kiểm thử tải (load testing) và đo hiệu năng HTTP API, web services và nhiều giao thức khác. **Thread Group** cấu hình số người dùng ảo, ramp-up và số vòng lặp. **HTTP Request** gửi yêu cầu. **Assertion** xác nhận kết quả kỳ vọng. **Listener** hiển thị và tổng hợp số liệu.

| Thuật ngữ | Ý nghĩa |
|---|---|
| Samples | Tổng số yêu cầu đã thực hiện |
| Average / Median (ms) | Thời gian phản hồi trung bình / trung vị |
| 90th / 95th / 99th percentile | Mốc thời gian mà 90% / 95% / 99% yêu cầu không vượt quá |
| Throughput | Số yêu cầu hệ thống xử lý trong một đơn vị thời gian |
| Error % | Tỷ lệ request không đạt kết quả kỳ vọng |
| Ramp-up | Thời gian tăng dần đến số user đã cấu hình |

**Tài liệu học:** [Trang Apache JMeter](https://jmeter.apache.org/) · [User Manual](https://jmeter.apache.org/usermanual/index.html) · [Getting Started](https://jmeter.apache.org/usermanual/get-started.html).

## 3. Cấu trúc repository

```text
23010625_JMeter_Lab8-/
├── README.md                 # Báo cáo và hướng dẫn
├── api/
│   ├── __init__.py
│   └── server.py             # API Python chạy trên localhost:8000
├── jmeter/
│   └── lab8_local_api.jmx    # Kịch bản JMeter
├── tests/
│   └── test_api.py           # Test chức năng độc lập
├── screenshots/              # Bổ sung ảnh chụp thật sau khi chạy
└── .gitignore
```

## 4. API được kiểm thử

API mẫu sử dụng thư viện chuẩn Python, không cần cài thêm thư viện.

| HTTP | Endpoint | Kết quả kỳ vọng |
|---|---|---|
| GET | `/health` | 200, `{"status":"ok"}` |
| GET | `/api/items` | 200, JSON danh sách 3 sản phẩm |
| POST | `/api/echo` | 200, trả lại JSON đã gửi |
| GET | `/api/slow` | 200, trì hoãn mô phỏng khoảng 200 ms |

Khởi động tại thư mục gốc (Python 3):

```bash
python -m api.server
```

Mở một terminal khác và xác nhận API:

```bash
python -m unittest discover -s tests -v
```

Truy cập `http://127.0.0.1:8000/health` để xem phản hồi.

## 5. Cài đặt và chạy JMeter

1. Cài Java theo yêu cầu phiên bản JMeter đang sử dụng; tải JMeter từ [trang chính thức](https://jmeter.apache.org/download_jmeter.cgi).
2. Giải nén, chạy `bin/jmeter.bat` (Windows) hoặc `bin/jmeter` (Linux/macOS).
3. **Giữ API Python chạy** trên máy cùng lúc.
4. JMeter → **File → Open** → chọn `jmeter/lab8_local_api.jmx`.
5. Kiểm tra Thread Group, HTTP Request Defaults và 4 HTTP Request.
6. Chạy thử nhỏ bằng nút **Start**; xem **Aggregate Report**. Để kiểm thử tải chính thức, dùng non-GUI theo lệnh bên dưới.

### Cấu hình test plan

| Tham số | Giá trị |
|---|---|
| Users (threads) | 10 |
| Ramp-up | 10 giây |
| Loops mỗi user | 10 |
| Samplers mỗi loop | 4 |
| Tổng requests **dự kiến** | 10 × 10 × 4 = **400** |
| Đích | `127.0.0.1:8000` |

Số request thực tế có thể khác nếu test bị dừng sớm hoặc xảy ra sự cố.

### Chạy non-GUI và xuất báo cáo HTML

Mở terminal ở thư mục gốc repo, đảm bảo `jmeter` nằm trong PATH. Trước **mỗi lần chạy**, xóa hoặc đổi tên thư mục output cũ để đường dẫn `results/html` chưa tồn tại (JMeter yêu cầu report directory trống).

**Windows PowerShell:**

```powershell
New-Item -ItemType Directory -Force results | Out-Null
jmeter -n -t jmeter/lab8_local_api.jmx -l results/lab8.jtl -e -o results/html
```

**Linux/macOS:**

```bash
mkdir -p results
jmeter -n -t jmeter/lab8_local_api.jmx -l results/lab8.jtl -e -o results/html
```

Mở `results/html/index.html` để xem biểu đồ và thống kê. Thư mục `results` được bỏ qua trong Git; nếu muốn nộp số liệu, hãy chọn kết quả phù hợp và loại bỏ mọi dữ liệu nhạy cảm trước khi commit.

## 6. Các trường hợp kiểm thử

| Test case | Mục đích | Tiêu chí quan sát |
|---|---|---|
| TC01 GET /health | Kiểm tra health endpoint | HTTP 200; Error % |
| TC02 GET /api/items | Đọc danh sách sản phẩm | Response time, throughput |
| TC03 POST /api/echo | Gửi/nhận payload JSON | HTTP 200, response body |
| TC04 GET /api/slow | API có độ trễ chủ động | Average, P95, P99 |

**Lưu ý:** Test plan đã có HTTP 200 assertion cho TC01. Các request khác được kiểm tra lỗi HTTP qua JMeter; đối chiếu nội dung response bằng GUI khi nghiệm thu. Với TC04, thời gian phản hồi có thể lớn hơn 200 ms do overhead và scheduler.

## 7. Báo cáo kết quả thực nghiệm

**Chưa chạy JMeter trong môi trường tạo repository.** Điền số liệu có thật từ Aggregate Report hoặc HTML dashboard sau khi chạy. Không tự điền giá trị giả định.

| Label | # Samples | Average (ms) | Min | Max | 90% line | 95% line | Error % | Throughput |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| GET - health | Chưa đo | — | — | — | — | — | — | — |
| GET - items | Chưa đo | — | — | — | — | — | — | — |
| POST - echo | Chưa đo | — | — | — | — | — | — | — |
| GET - slow 200ms | Chưa đo | — | — | — | — | — | — | — |
| **TOTAL** | **Chưa đo** | — | — | — | — | — | — | — |

### 7.1. Hình minh họa bắt buộc

Sau khi chạy, lưu ảnh **chụp màn hình thật** với các tên sau rồi commit lên `screenshots/`:

1. `01-test-plan.png`: cửa sổ JMeter với cây Test Plan và Thread Group.
2. `02-http-request.png`: cấu hình một HTTP Request (host, port, method, path).
3. `03-aggregate-report.png`: bảng Aggregate Report sau khi thực hiện.
4. `04-html-dashboard.png`: Dashboard HTML từ lần chạy non-GUI.
5. `05-api-running.png`: terminal API đang chạy hoặc kết quả `/health`.

Khi có ảnh, bỏ dấu comment ở các dòng dưới để chúng hiện trên README:

<!-- ![Test Plan](screenshots/01-test-plan.png) -->
<!-- ![HTTP Request](screenshots/02-http-request.png) -->
<!-- ![Aggregate Report](screenshots/03-aggregate-report.png) -->
<!-- ![HTML Dashboard](screenshots/04-html-dashboard.png) -->
<!-- ![API Running](screenshots/05-api-running.png) -->

## 8. Nhận xét và kết luận

Sau khi chạy và có số liệu, nhận xét dựa trên **Average, P95, throughput, Error %**, so sánh TC04 với các endpoint còn lại và lý giải ảnh hưởng của độ trễ mô phỏng. Nếu Error % > 0, kiểm tra response code, assertion failures và server logs trước khi kết luận hệ thống lỗi hiệu năng. Test ngắn với 10 users trên localhost **chỉ mang tính học tập**, không đại diện năng lực tải trong môi trường production.

**Kết luận hiện tại:** Đã chuẩn bị API minh họa và kịch bản JMeter có thể tải về/chạy thử. Báo cáo đo thực nghiệm và ảnh chụp chưa được xác nhận, cần hoàn thiện bằng lần chạy trên máy thực tế.

---
*Tác giả: Trần Văn Nhật — 23010625 | Lab 8 Apache JMeter*
