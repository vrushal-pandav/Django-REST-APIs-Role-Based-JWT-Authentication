
# 🔐 Django REST APIs – Email OTP Login + JWT Authentication
This project provides a secure authentication system using Django REST Framework and JWT tokens. It features email-based OTP (One-Time Password) login, JWT token handling (login, verify, refresh, logout), and follows best practices to protect sensitive credentials.

## 🚀 Features
- ✅ Send OTP to email for passwordless login
- 🔑 Login using Email + OTP
- 🔁 Refresh access token using refresh token
- ✅ Verify token validity
- 🚪 Logout by blacklisting refresh token (JWT)
- 🔒 Secure SMTP email integration (with environment variables)
- 📦 Fully documented Postman collection included

## 📂 Technology Stack
- Django & Django REST Framework (DRF)
- SimpleJWT (for token authentication)
- Gmail SMTP (for sending OTP emails)

## 📘 API Documentation

A complete API reference for this Django authentication system is available below:

🔗 [View Postman API Docs](https://documenter.getpostman.com/view/45298281/2sB3BALsJ8).


## 🛠️ How to Run This Project

Follow these steps to run the project locally:

### ✅ Prerequisites

- Python 3.8 or higher
- Git
- Virtualenv (recommended)
- Gmail account (for sending OTP emails)

---
# 🔧 Setup Instructions


### 1️⃣ Clone the Repository
(type this command on git bash terminal)<br>
git clone https://github.com/vrushal-pandav/Django-REST-APIs-Role-Based-JWT-Authentication.git<br>
cd Django-REST-APIs-Role-Based-JWT-Authentication

### 2️⃣ Create & Activate a Virtual Environment
#### For Windows command
python -m venv venv<br>
venv\Scripts\activate

#### For macOS/Linux command
python3 -m venv venv<br>
source venv/bin/activate

### 3️⃣ Install Dependencies
pip install django djangorestframework djangorestframework-simplejwt

### 4️⃣ Change in settings.py file at bottom
EMAIL_HOST_USER =  Set your email adrdress such as example: 'example@gmail.com'<br>
EMAIL_HOST_PASSWORD =  Set your generated pass key...

If you dont know what is passkey and how to generate then search on youtube    

### 5️⃣ Run Migrations
python manage.py migrate

### 6️⃣ Start the Server
python manage.py runserver


### 📮 API Endpoints

| Endpoint                 | Method | Description                        |
| ------------------------ | ------ | ---------------------------------- |
| `/auth/email-otp/`       | POST   | Send OTP to user's email           |
| `/auth/email-otp-login/` | POST   | Login using email and OTP          |
| `/api/v1/token/refresh/` | POST   | Refresh access token               |
| `/api/v1/token/verify/`  | POST   | Verify token validity              |
| `/api/v1/token/logout/`  | POST   | Logout and blacklist refresh token |

### 🔑 Authentication Format
Use the returned access token in the header for protected routes:<br>
Authorization: Bearer <access_token>

