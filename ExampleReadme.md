Để quản lý các hằng số (constants) hoặc các giá trị được sử dụng chung trong nhiều file (như số lần đăng nhập tối đa, giới hạn rate limit, tên file log, v.v.), chúng ta sẽ tạo một file riêng biệt gọi là `constants.py`. File này sẽ được đặt trong thư mục `app/` để dễ dàng import và sử dụng ở mọi nơi trong dự án. Dưới đây là cách thực hiện và cách cập nhật `README.md` để phản ánh thay đổi này.

---

### **1. Thêm file `constants.py`**

#### **Vị trí**
File sẽ được đặt tại `app/constants.py`.

#### **Nội dung `app/constants.py`**
```python
# Các hằng số liên quan đến xác thực
MAX_LOGIN_ATTEMPTS = 5  # Số lần đăng nhập sai tối đa
LOGIN_LOCKOUT_MINUTES = 15  # Thời gian khóa sau khi vượt quá số lần thử (phút)

# Các hằng số liên quan đến rate limiting
RATE_LIMIT_PER_HOUR = "100/hour"  # Giới hạn 100 yêu cầu mỗi giờ

# Các hằng số liên quan đến file và log
LOG_DIR = "logs"
APP_LOG_FILE = "app.log"
SECURITY_LOG_FILE = "security.log"
REPORT_DIR = "static/reports"
PRODUCT_REPORT_FILE = "product_report.csv"

# Các hằng số liên quan đến email
EMAIL_FROM = "no-reply@yourdomain.com"
EMAIL_WELCOME_SUBJECT = "Welcome to Inventory Management"

# Các hằng số khác
DEFAULT_ROLE = "user"
PAGE_SIZE = 10  # Số mục trên mỗi trang trong danh sách
```

#### **Cách sử dụng**
- Trong các file khác, bạn chỉ cần import và sử dụng, ví dụ:
  ```python
  from app.constants import MAX_LOGIN_ATTEMPTS, SECURITY_LOG_FILE
  ```

---

### **2. Cập nhật các file liên quan**

#### **config.py**
Loại bỏ các hằng số đã được chuyển sang `constants.py`:
```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
    RATE_LIMIT_STORAGE_URI = os.getenv("REDIS_URL", "redis://localhost:6379/1")

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
```

#### **app/__init__.py**
Cập nhật để sử dụng `constants.py`:
```python
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from celery import Celery
import logging
from logging.handlers import RotatingFileHandler
from app.constants import SECURITY_LOG_FILE

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
limiter = Limiter(key_func=get_remote_address)

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config["CELERY_RESULT_BACKEND"],
        broker=app.config["CELERY_BROKER_URL"]
    )
    celery.conf.update(app.config)
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    celery.Task = ContextTask
    return celery

def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    migrate.init_app(app, db)
    Talisman(app, force_https=config_name == "production")
    limiter.init_app(app)

    handler = RotatingFileHandler(SECURITY_LOG_FILE, maxBytes=10000, backupCount=1)
    handler.setLevel(logging.WARNING)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("Application started")

    global celery
    celery = make_celery(app)

    from app.routes import auth, product, dashboard
    app.register_blueprint(auth.bp)
    app.register_blueprint(product.bp)
    app.register_blueprint(dashboard.bp)

    @app.errorhandler(429)
    def ratelimit_handler(e):
        app.logger.warning(f"Rate limit exceeded from IP: {request.remote_addr}")
        return "Too Many Requests", 429

    with app.app_context():
        db.create_all()

    return app

celery = None
```

#### **app/utils/security.py**
Cập nhật để dùng hằng số:
```python
from flask import request
from app import db, limiter
from app.models.failed_login import FailedLogin
from app.constants import MAX_LOGIN_ATTEMPTS, LOGIN_LOCKOUT_MINUTES, RATE_LIMIT_PER_HOUR
import bleach
import logging

def sanitize_input(data):
    if isinstance(data, str):
        return bleach.clean(data)
    return data

def check_login_attempts(email, max_attempts=MAX_LOGIN_ATTEMPTS):
    ip = request.remote_addr
    failed = FailedLogin.query.filter_by(ip_address=ip, email=email).first()
    
    if not failed:
        failed = FailedLogin(ip_address=ip, email=email, attempts=1)
        db.session.add(failed)
    else:
        failed.attempts += 1
        failed.last_attempt = datetime.utcnow()
    
    db.session.commit()
    
    if failed.is_locked(max_attempts):
        logging.warning(f"Brute-force attempt detected: IP={ip}, Email={email}, Attempts={failed.attempts}")
        return True
    return False

def apply_rate_limit():
    return limiter.limit(RATE_LIMIT_PER_HOUR)
```

#### **app/models/failed_login.py**
Cập nhật để dùng `LOGIN_LOCKOUT_MINUTES`:
```python
from app import db
from datetime import datetime, timedelta
from app.constants import LOGIN_LOCKOUT_MINUTES

class FailedLogin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    attempts = db.Column(db.Integer, default=0)
    last_attempt = db.Column(db.DateTime, default=datetime.utcnow)

    def is_locked(self, max_attempts):
        return self.attempts >= max_attempts and (datetime.utcnow() - self.last_attempt) < timedelta(minutes=LOGIN_LOCKOUT_MINUTES)
```

#### **app/utils/reports.py**
Cập nhật để dùng hằng số:
```python
from app import celery, db
from app.models.product import Product
from app.constants import REPORT_DIR, PRODUCT_REPORT_FILE
import csv
import os

@celery.task
def generate_product_report():
    products = Product.query.all()
    filepath = os.path.join(REPORT_DIR, PRODUCT_REPORT_FILE)
    
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Name", "Price"])
        for product in products:
            writer.writerow([product.id, product.name, product.price])
    
    return filepath
```

---

### **3. Cập nhật `README.md`**

Dưới đây là nội dung hoàn chỉnh của `README.md` với phần bổ sung về `constants.py`:

---

# Inventory Management System

Đây là một hệ thống quản lý được xây dựng bằng **Flask**, tích hợp các tính năng quản lý người dùng, sản phẩm, chạy tác vụ ngầm, ghi log, và bảo mật chống lại các cuộc tấn công phổ biến. Hệ thống phù hợp để triển khai trong môi trường thực tế (production-ready) và hỗ trợ kiểm thử (testing).

## Tính năng chính

### Quản lý người dùng
- Đăng ký, đăng nhập, đăng xuất với phân quyền (admin, user).
- Xác thực bảo mật (mã hóa mật khẩu bằng bcrypt).
- Gửi email xác nhận bất đồng bộ sau khi đăng ký.

### Quản lý dữ liệu
- CRUD (Create, Read, Update, Delete) cho sản phẩm.
- Tìm kiếm, lọc và phân trang danh sách sản phẩm.
- Tạo báo cáo sản phẩm (CSV) chạy ngầm.

### Tác vụ ngầm (Background Tasks)
- Sử dụng **Celery** với **Redis** để xử lý tác vụ bất đồng bộ (gửi email, tạo báo cáo).
- Hỗ trợ các tác vụ nặng mà không làm chậm trải nghiệm người dùng.

### Ghi log
- Ghi lại các hành động quan trọng (đăng nhập, đăng ký, tạo/sửa/xóa dữ liệu) vào file log.
- Ghi log các hành vi đáng nghi (tấn công brute-force, vượt quá giới hạn yêu cầu).

### Bảo mật
- **Chống DDoS**: Giới hạn số lượng yêu cầu (rate limiting) bằng Flask-Limiter.
- **Chống SQL Injection**: Sử dụng SQLAlchemy ORM với truy vấn tham số hóa.
- **Chống XSS**: Làm sạch đầu vào bằng Bleach và thêm Content-Security-Policy header.
- **Chống CSRF**: Bảo vệ form bằng Flask-WTF.
- **Chống Brute-force**: Khóa tài khoản tạm thời sau 5 lần đăng nhập sai trong 15 phút.
- **HTTPS**: Bật trong môi trường production qua Flask-Talisman.

### Dashboard
- Tổng quan hệ thống: số người dùng, sản phẩm, và hoạt động gần đây.

### API
- RESTful API cho phép tương tác từ ứng dụng bên ngoài (dự kiến phát triển thêm).

### Kiểm thử
- Unit test với Pytest cho routes và logic nghiệp vụ.
- Cơ sở dữ liệu riêng cho môi trường test (SQLite in-memory).

---

## Công nghệ sử dụng
- **Backend**: Flask, Flask-SQLAlchemy, Flask-Login, Flask-WTF, Flask-Migrate
- **Tác vụ ngầm**: Celery, Redis
- **Bảo mật**: Flask-Talisman, Flask-Limiter, Bleach, Werkzeug
- **Database**: PostgreSQL (production), SQLite (dev/test)
- **Frontend**: Jinja2, Bootstrap
- **Testing**: Pytest, Factory Boy

---

## Cấu trúc thư mục
```
inventory_management/
│
├── app/                        # Ứng dụng Flask
│   ├── __init__.py             # Khởi tạo Flask, Celery, và bảo mật
│   ├── constants.py            # Định nghĩa hằng số dùng chung
│   ├── models/                 # Mô hình dữ liệu
│   │   ├── user.py             # Model User
│   │   ├── product.py          # Model Product
│   │   └── failed_login.py     # Model theo dõi đăng nhập sai
│   ├── routes/                 # Tuyến đường
│   │   ├── auth.py             # Đăng nhập/đăng ký
│   │   ├── product.py          # Quản lý sản phẩm
│   │   └── dashboard.py        # Dashboard
│   ├── templates/              # HTML templates
│   ├── static/                 # CSS, JS, hình ảnh
│   ├── forms/                  # Form xử lý đầu vào
│   ├── utils/                  # Hàm tiện ích
│   │   ├── email.py            # Task gửi email
│   │   ├── reports.py          # Task tạo báo cáo
│   │   ├── logging.py          # Ghi log
│   │   └── security.py         # Bảo mật
│   └── api/                    # RESTful API (dự kiến)
│
├── migrations/                 # Quản lý thay đổi database
├── tests/                      # Unit tests
├── logs/                       # File log
│   ├── app.log                 # Log ứng dụng
│   └── security.log            # Log bảo mật
│
├── config.py                   # Cấu hình
├── celery_worker.py            # Khởi chạy Celery worker
├── requirements.txt            # Thư viện
├── .env                        # Biến môi trường
├── run.py                      # File chạy Flask
└── README.md                   # Tài liệu này
```

### Ghi chú về `constants.py`
- File `app/constants.py` chứa các hằng số được sử dụng chung như số lần đăng nhập tối đa, giới hạn rate limit, tên file log, v.v.
- Giúp dễ dàng quản lý và thay đổi các giá trị này ở một nơi duy nhất.

---

## Yêu cầu hệ thống
- Python 3.8+
- Redis (message broker và rate limiting)
- PostgreSQL (khuyến nghị cho production)

---

## Cài đặt

### 1. Clone repository
```bash
git clone <repository-url>
cd inventory_management
```

### 2. Tạo môi trường ảo
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Cài đặt thư viện
```bash
pip install -r requirements.txt
```

### 4. Cài đặt Redis
- Linux: `sudo apt install redis-server`
- Mac: `brew install redis`
- Windows: Tải Redis từ https://github.com/tporadowski/redis/releases
- Chạy Redis: `redis-server`

### 5. Cấu hình biến môi trường
Tạo file `.env` trong thư mục gốc với nội dung:
```
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost/dbname  # Hoặc sqlite:///dev.db
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
REDIS_URL=redis://localhost:6379/1
```

### 6. Khởi tạo database
```bash
flask db init    # (Nếu chưa có migrations/)
flask db migrate
flask db upgrade
```

---

## Chạy ứng dụng

### 1. Chạy Flask
```bash
python run.py
```
- Truy cập: `http://localhost:5000`

### 2. Chạy Celery Worker
```bash
celery -A celery_worker.celery worker --loglevel=info
```

### 3. Chạy kiểm thử (nếu cần)
```bash
pytest tests/
```

---

## Triển khai trong Production

### 1. Cấu hình
- Sử dụng `config.ProductionConfig` trong `app/__init__.py`.
- Đảm bảo HTTPS được bật (Flask-Talisman).

### 2. Server
- Dùng **Gunicorn** làm WSGI server:
  ```bash
  gunicorn -w 4 -b 0.0.0.0:8000 run:app
  ```
- Kết hợp **Nginx** làm reverse proxy.

### 3. Giám sát
- Dùng **Flower** để theo dõi Celery:
  ```bash
  celery -A celery_worker.celery flower
  ```
- Truy cập: `http://localhost:5555`

### 4. Bảo mật
- Thêm Cloudflare hoặc AWS WAF để tăng cường chống DDoS.
- Cài Fail2Ban để chặn IP đáng nghi dựa trên log.

---

## Hướng dẫn sử dụng

### Đăng ký và đăng nhập
- Truy cập `/auth/register` để tạo tài khoản → nhận email xác nhận.
- Đăng nhập tại `/auth/login`.

### Quản lý sản phẩm
- Thêm/sửa/xóa sản phẩm tại `/product/` (yêu cầu đăng nhập).
- Tạo báo cáo tại `/product/generate-report` → file CSV tải về từ `static/reports/`.

### Bảo mật
- Đăng nhập sai 5 lần → khóa IP tạm thời trong 15 phút.
- Gửi quá 100 yêu cầu/giờ → bị chặn (HTTP 429).

---

## Phát triển thêm
- **API**: Mở rộng thư mục `app/api/` để hỗ trợ RESTful API.
- **Captcha**: Tích hợp Flask-Recaptcha chống bot.
- **Thông báo real-time**: Dùng Flask-SocketIO.
- **Tác vụ định kỳ**: Thêm Celery Beat để chạy báo cáo hàng ngày.

---

## Góp ý và hỗ trợ
Nếu gặp vấn đề hoặc muốn mở rộng tính năng, hãy tạo issue trên repository hoặc liên hệ qua email: `your-email@example.com`.

---

### **Kết quả**
- File `constants.py` giúp tập trung các giá trị dùng chung, dễ bảo trì và mở rộng.
- `README.md` đã được cập nhật để phản ánh sự thay đổi này, đảm bảo người dùng hiểu rõ cấu trúc và cách sử dụng.

Nếu bạn cần thêm hằng số nào khác hoặc muốn điều chỉnh nội dung, hãy cho tôi biết nhé!