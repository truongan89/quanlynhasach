Dưới đây là phiên bản cập nhật của `README.md` cho **Bookstore Management System**, bao gồm cây thư mục dự án (project directory tree) để minh họa cấu trúc hệ thống. Nội dung vẫn giữ nguyên phong cách tổng quan, không chứa code mẫu, và tích hợp đầy đủ các yêu cầu trước đó cùng yêu cầu mới về quản lý nhà sách.

---

# Bookstore Management System

## Giới thiệu

Bookstore Management System là một hệ thống quản lý nhà sách toàn diện, xây dựng bằng **Flask**, hỗ trợ quản lý sách, đơn hàng, bán hàng, và báo cáo doanh thu. Hệ thống được thiết kế bảo mật, hiệu quả, với khả năng xử lý tác vụ ngầm và mở rộng linh hoạt, phù hợp cho môi trường thực tế.

---

## Tính năng chính

### Quản lý người dùng
- Đăng ký, đăng nhập, phân quyền (admin, quản lý kho, nhân viên, khách hàng).
- Gửi email xác nhận bất đồng bộ sau khi đăng ký.

### Quản lý sách
- **Nhập sách** (quản lý kho):
  - Biểu mẫu nhập sách với các trường: mã sách, tên sách, thể loại, số lượng, giá.
  - Quy định: Số lượng nhập tối thiểu 150, chỉ nhập khi tồn kho dưới 300.
  - Thêm, xóa, cập nhật, tìm kiếm sách (dành cho quản lý).
- **Bán sách** (nhân viên):
  - Biểu mẫu bán sách hỗ trợ quét mã vạch để nhập mã sách.
  - Cập nhật tồn kho sau khi bán.

### Đặt sách online
- **Khách hàng**:
  - Đặt sách qua biểu mẫu online, chọn thanh toán tại quầy hoặc trực tuyến.
  - Giao hàng miễn phí nếu thanh toán trực tuyến.
  - Quy định: Đơn thanh toán tại quầy bị hủy sau 48 tiếng nếu không nhận.
- **Tác vụ ngầm**: Gửi email thông báo khi đặt hàng và tự động hủy đơn sau 48 tiếng (nếu áp dụng).

### Thống kê và báo cáo (quản trị)
- **Doanh thu**:
  - Bảng và biểu đồ (Chart.js) theo tháng, phân loại theo thể loại sách.
- **Tần suất bán sách**:
  - Thống kê số lần bán của từng đầu sách theo tháng.
- Xuất báo cáo dưới dạng CSV (chạy ngầm).

### Thay đổi quy định (quản trị)
- Điều chỉnh:
  - Số lượng nhập tối thiểu.
  - Số lượng tồn tối thiểu trước khi nhập.
  - Thời gian hủy đơn hàng nếu không nhận (mặc định 48 tiếng).
- Lưu thay đổi vào `constants.py` hoặc database.

### Bảo mật
- Chống DDoS (rate limiting), SQL Injection, XSS, CSRF, brute-force.
- HTTPS trong production.
- Giới hạn đăng nhập sai (5 lần, khóa 15 phút).

### Tác vụ ngầm
- Gửi email thông báo (đặt hàng, hủy đơn).
- Tạo báo cáo CSV.
- Kiểm tra và hủy đơn hàng tự động sau thời gian quy định.

### Ghi log
- Ghi lại hành động: nhập sách, bán sách, đặt hàng, thay đổi quy định.
- Log các sự kiện bảo mật (tấn công, vượt giới hạn yêu cầu).

### Dashboard
- Tổng quan: số sách tồn kho, đơn hàng, doanh thu, hoạt động gần đây.

---

## Công nghệ sử dụng

- **Backend**: Flask, SQLAlchemy, Celery
- **Database**: PostgreSQL (production), SQLite (dev/test)
- **Bảo mật**: Flask-Talisman, Flask-Limiter, Bleach
- **Frontend**: Jinja2, Bootstrap, Chart.js (biểu đồ)
- **DevOps**: Redis, Gunicorn, Nginx
- **Testing**: Pytest

---

## Cấu trúc thư mục

Dưới đây là cây thư mục của dự án:

```
bookstore_management/
│
├── app/                        # Ứng dụng Flask chính
│   ├── __init__.py             # Khởi tạo Flask, Celery, bảo mật
│   ├── constants.py            # Hằng số dùng chung (quy định, tên file, v.v.)
│   ├── models/                 # Mô hình dữ liệu
│   │   ├── __init__.py
│   │   ├── customer.py         # Model Customer (Thông tin khách hàng)
│   │   ├── book.py             # Model Book (sách)
│   │   ├── book_import.py      # Model Book Import (lịch sử nhập sách)
│   │   ├── cate.py             # Model Cate (loại sách)
│   │   ├── log.py              # Model Log (log)
│   │   ├── order.py            # Model Order (đơn hàng)
│   │   ├── order_detail.py     # Model Order Detail (chi tiết đơn hàng)
│   │   ├── sale.py             # Model Sale (Lịch sử bán hàng)
│   │   ├── setting.py          # Model Setting (Cấu hình hệ thống)
│   │   └── account.py          # Model Account (Tài khoản)
│   ├── routes/                 # Các tuyến đường
│   │   ├── __init__.py
│   │   ├── auth.py             # Đăng nhập/đăng ký
│   │   ├── book.py             # Nhập/bán/quản lý sách
│   │   ├── order.py            # Đặt sách online
│   │   ├── report.py           # Thống kê và báo cáo ( nâng cấp sau )
│   │   ├── settings.py         # Thay đổi quy định
│   │   └── dashboard.py        # Dashboard ( nâng cấp sau )
│   ├── templates/              # HTML templates
│   │   ├── base.html           # Template cơ sở
│   │   ├── auth/               # Đăng nhập/đăng ký
│   │   ├── book/               # Nhập/bán sách
│   │   ├── order/              # Đặt sách
│   │   ├── report/             # Báo cáo
│   │   ├── settings/           # Quy định
│   │   └── dashboard.html      # Dashboard
│   ├── static/                 # CSS, JS, hình ảnh
│   │   ├── css/
│   │   ├── js/                 # Chart.js cho biểu đồ
│   │   └── images/
│   ├── forms/                  # Biểu mẫu
│   │   ├── __init__.py
│   │   ├── login.py            # Form đăng nhập
│   │   ├── register.py         # Form đăng ký
│   │   ├── book.py             # Form nhập sách
│   │   ├── sale.py             # Form bán sách
│   │   └── order.py            # Form đặt sách
│   ├── utils/                  # Hàm tiện ích
│   │   ├── __init__.py
│   │   ├── email.py            # Task gửi email
│   │   ├── reports.py          # Task tạo báo cáo
│   │   ├── logging.py          # Ghi log
│   │   ├── security.py         # Bảo mật
│   │   └── barcode.py          # Xử lý mã vạch
│   └── api/                    # RESTful API (dự kiến)
│       ├── __init__.py
│       └── book.py             # API sách
│
├── migrations/                 # Quản lý thay đổi database
│   └── versions/               # File migration
│
├── tests/                      # Unit tests
│   ├── __init__.py
│   ├── test_auth.py            # Test xác thực
│   ├── test_book.py            # Test quản lý sách
│   ├── test_order.py           # Test đặt sách
│   └── test_report.py          # Test báo cáo
│
├── logs/                       # File log
│   ├── app.log                 # Log ứng dụng
│   └── security.log            # Log bảo mật
│
├── config.py                   # Cấu hình môi trường
├── celery_worker.py            # Khởi chạy Celery worker
├── requirements.txt            # Danh sách thư viện
├── .env                        # Biến môi trường
├── run.py                      # File chạy Flask
└── README.md                   # Tài liệu này
```

---

## Đối tượng sử dụng

- **Quản trị**: Theo dõi doanh thu, thay đổi quy định.
- **Quản lý kho**: Nhập và quản lý sách.
- **Nhân viên**: Bán sách tại quầy.
- **Khách hàng**: Đặt sách online.
- **Nhà phát triển**: Tùy chỉnh hệ thống.

---

## Yêu cầu chức năng

### 1. Nhập sách
- Biểu mẫu: Mã sách, tên, thể loại, số lượng, giá.
- Quy định: Nhập tối thiểu 150 cuốn, chỉ nhập khi tồn kho dưới 300.

### 2. Đặt sách
- Biểu mẫu: Chọn sách, số lượng, phương thức thanh toán (tại quầy/trực tuyến).
- Quy định: Đơn thanh toán tại quầy hủy sau 48 tiếng nếu không nhận.

### 3. Bán sách
- Biểu mẫu: Nhập mã sách (quét mã vạch), số lượng, tính tổng tiền.
- Cập nhật tồn kho tức thì.

### 4. Thống kê, báo cáo
- Doanh thu theo tháng/thể loại (bảng, biểu đồ).
- Tần suất bán từng đầu sách theo tháng.

### 5. Thay đổi quy định
- Giao diện quản trị để chỉnh: số lượng nhập tối thiểu, tồn tối thiểu, thời gian hủy đơn.

---

## Hướng dẫn cài đặt

1. **Yêu cầu**: Python 3.8+, Redis, PostgreSQL.
2. **Clone**: `git clone <repository-url>`.
3. **Cài đặt**: `pip install -r requirements.txt`.
4. **Cấu hình**: Tạo `.env` với `SECRET_KEY`, `DATABASE_URL`, `REDIS_URL`, v.v.
5. **Chạy**:
   - Flask: `python run.py`.
   - Celery: `celery -A celery_worker.celery worker --loglevel=info`.

---

## Triển khai Production

- Dùng Gunicorn + Nginx.
- Bật HTTPS qua Flask-Talisman.
- Giám sát Celery với Flower.
- Bảo mật thêm với Cloudflare/WAF.

---

## Mở rộng

- Tích hợp API cho ứng dụng di động.
- Thêm hỗ trợ quét mã vạch qua webcam.
- Tạo thông báo real-time khi đơn hàng được đặt.
- Hỗ trợ đa ngôn ngữ.

---

## Liên hệ

Liên hệ qua email: `your-email@example.com` hoặc tạo issue trên repository để được hỗ trợ.

---

### **Ghi chú**
- Cây thư mục phản ánh đầy đủ các thành phần cần thiết cho hệ thống nhà sách, bao gồm các module mới như `order.py`, `sale.py`, `barcode.py`.
- Các yêu cầu cũ (bảo mật, tác vụ ngầm, v.v.) được giữ nguyên và tích hợp hài hòa với yêu cầu mới.

Nếu bạn cần điều chỉnh hoặc bổ sung thêm chi tiết vào cây thư mục hoặc nội dung, hãy cho tôi biết nhé!



## Tính năng chính

### Quản lý người dùng
- Đăng ký, đăng nhập, phân quyền (admin, quản lý kho, nhân viên, khách hàng).
- Gửi email xác nhận bất đồng bộ sau khi đăng ký.

### Quản lý sách
- **Nhập sách** (quản lý kho):
  - Biểu mẫu nhập sách với các trường: mã sách, tên sách, thể loại, số lượng, giá.
  - Quy định: Số lượng nhập tối thiểu 150, chỉ nhập khi tồn kho dưới 300.
  - Thêm, xóa, cập nhật, tìm kiếm sách (dành cho quản lý).
- **Bán sách** (nhân viên):
  - Biểu mẫu bán sách hỗ trợ quét mã vạch để nhập mã sách.
  - Cập nhật tồn kho sau khi bán.

### Đặt sách online
- **Khách hàng**:
  - Đặt sách qua biểu mẫu online, chọn thanh toán tại quầy hoặc trực tuyến.
  - Giao hàng miễn phí nếu thanh toán trực tuyến.
  - Quy định: Đơn thanh toán tại quầy bị hủy sau 48 tiếng nếu không nhận.
- **Tác vụ ngầm**: Gửi email thông báo khi đặt hàng và tự động hủy đơn sau 48 tiếng (nếu áp dụng).

### Thống kê và báo cáo (quản trị)
- **Doanh thu**:
  - Bảng và biểu đồ (Chart.js) theo tháng, phân loại theo thể loại sách.
- **Tần suất bán sách**:
  - Thống kê số lần bán của từng đầu sách theo tháng.
- Xuất báo cáo dưới dạng CSV (chạy ngầm).

### Thay đổi quy định (quản trị)
- Điều chỉnh:
  - Số lượng nhập tối thiểu.
  - Số lượng tồn tối thiểu trước khi nhập.
  - Thời gian hủy đơn hàng nếu không nhận (mặc định 48 tiếng).
- Lưu thay đổi vào `constants.py` hoặc database.

### Tác vụ ngầm
- Gửi email thông báo (đặt hàng, hủy đơn).
- Tạo báo cáo CSV.
- Kiểm tra và hủy đơn hàng tự động sau thời gian quy định.

### Ghi log
- Ghi lại hành động: nhập sách, bán sách, đặt hàng, thay đổi quy định.
- Log các sự kiện bảo mật (tấn công, vượt giới hạn yêu cầu).

### Dashboard
- Tổng quan: số sách tồn kho, đơn hàng, doanh thu, hoạt động gần đây.



bookstore_management/
│
├── app/                        # Ứng dụng Flask chính
│   ├── __init__.py             # Khởi tạo Flask
│   ├── constants.py            # Hằng số dùng chung (quy định, tên file, v.v.)
│   ├── models/                 # Mô hình dữ liệu
│   │   ├── __init__.py
│   │   ├── customer.py         # Model Customer (Thông tin khách hàng)
│   │   ├── book.py             # Model Book (sách)
│   │   ├── book_import.py      # Model Book Import (lịch sử nhập sách)
│   │   ├── cate.py             # Model Cate (loại sách)
│   │   ├── log.py              # Model Log (log)
│   │   ├── order.py            # Model Order (đơn hàng)
│   │   ├── order_detail.py     # Model Order Detail (chi tiết đơn hàng)
│   │   ├── sale.py             # Model Sale (Lịch sử bán hàng)
│   │   ├── setting.py          # Model Setting (Cấu hình hệ thống)
│   │   └── account.py          # Model Account (Tài khoản)
│   ├── routes/                 # Các tuyến đường
│   ├── templates/              # HTML templates
│   ├── static/                 # CSS, JS, hình ảnh
│   ├── forms/                  # Biểu mẫu
│   ├── utils/                  # Hàm tiện ích
│   └── api/                    # RESTful API (dự kiến)
├── migrations/                 # Quản lý thay đổi database
├── tests/                      # Unit tests
├── logs/                       # File log
├── config.py                   # Cấu hình môi trường
├── requirements.txt            # Danh sách thư viện
├── .env                        # Biến môi trường
├── app.py                      # File chạy Flask
└── README.md                   # Tài liệu này