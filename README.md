# Student Exam Management System (GScore)

Dự án quản lý kết quả thi sinh viên sử dụng Django REST Framework cho backend và React.js cho frontend.

## Yêu cầu hệ thống

- Python 3.8+
- Node.js 14+ và npm/yarn
- MySQL 5.7+ hoặc 8.0+
- pip và Git

## Cài đặt Backend (Django)

### 1. Clone và tạo môi trường ảo

```bash
git clone <repository-url>
cd <project-folder>

# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

Hoặc:

```bash
pip install django djangorestframework django-cors-headers django-oauth-toolkit cloudinary python-dotenv pymysql drf-yasg django-unfold django-extensions
```

### 3. Tạo database MySQL

```sql
CREATE DATABASE g_score CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. Cấu hình file .env

Tạo file `.env` trong thư mục gốc:

```properties
DB_ENGINE=django.db.backends.mysql
DB_NAME=g_score
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306

SECRET_KEY=django-insecure-eid-2s-$5zpu7&-y&b35kd6&^51pi^zp6y)k0odzr=ja-5%r*6
DEBUG=True

CLIENT_ID=
CLIENT_SECRET=

CLOUNDINARY_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
```

### 5. Chạy migrations và tạo superuser

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

## Cài đặt Frontend (React.js)

### 1. Cài đặt dependencies

```bash
cd frontend
npm install
```

### 2. Tạo file .env

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_CLIENT_ID=
REACT_APP_CLIENT_SECRET=
```

## Cấu hình OAuth2 Application

### 1. Khởi động server

```bash
python manage.py runserver
```

### 2. Tạo OAuth2 Application

Truy cập: `http://127.0.0.1:8000/o/applications/register/`

- Name: `GScore Application`
- Client type: **Confidential**
- Authorization grant type: **Resource owner password-based**
- Redirect uris: `http://localhost:5173/callback`

Nhấn Save và copy Client ID và Client Secret.

### 3. Cập nhật .env

Backend (.env):
```properties
CLIENT_ID=your_client_id_here
CLIENT_SECRET=your_client_secret_here
```

Frontend (.env):
```env
REACT_APP_CLIENT_ID=your_client_id_here
REACT_APP_CLIENT_SECRET=your_client_secret_here
```

## Cấu hình Cloudinary

1. Đăng ký tại: https://cloudinary.com/users/register_free
2. Vào Dashboard lấy Cloud Name, API Key, API Secret
3. Cập nhật vào file .env:

```properties
CLOUNDINARY_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

## Cấu hình Admin và Import dữ liệu

### 1. Truy cập GScore Admin

`http://127.0.0.1:8000/gscore-admin/`

### 2. Tạo khóa học

Course Manage → Course → Add Course

Điền thông tin:
- Course Name
- Course Code
- Description

### 3. Import CSV

Score Attributes → Import Student Exam Results

File CSV mẫu:
```csv
registration_number,student_name,course_code,score,exam_date
2021001,Nguyen Van A,CS101,8.5,2024-01-15
```

## Chạy ứng dụng

### Backend
```bash
cd <project-folder>
source venv/bin/activate  # Windows: venv\Scripts\activate
python manage.py runserver
```

### Frontend
```bash
cd frontend
npm start
```

Backend: `http://localhost:8000`
Frontend: `http://localhost:5173`

## API Endpoints

### Authentication
POST `/o/token/` - Lấy access token

### Student Exam Result
GET `/student-exam-result/{registration_number}/` - Lấy kết quả thi

### Users
POST `/users/lecturer-register/` - Đăng ký giảng viên
POST `/users/student-register/` - Đăng ký sinh viên
GET `/users/{id}/` - Lấy thông tin user

## Troubleshooting

### Lỗi database
- Kiểm tra MySQL đã chạy
- Kiểm tra thông tin trong .env

### Lỗi OAuth2
- Kiểm tra Client ID/Secret trong .env
- Không có khoảng trắng thừa

### Lỗi CORS
- Kiểm tra CORS_ALLOWED_ORIGINS trong settings.py
- Cài đặt django-cors-headers

## File .gitignore

```gitignore
.env
*.env
__pycache__/
venv/
node_modules/
*.log
db.sqlite3
staticfiles/
```
