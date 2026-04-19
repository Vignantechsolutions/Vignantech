# Vignan TechSolutions - Corporate Training Platform

A full-stack Django web application for Vignan TechSolutions, an MSME registered technology company.

## Tech Stack
- **Backend:** Django 5.2, Python 3.10
- **Frontend:** Bootstrap 5, HTML5, CSS3, JavaScript
- **Database:** MySQL
- **Payments:** Razorpay
- **PDF:** ReportLab
- **Deployment:** Gunicorn + WhiteNoise

## Features
- Dynamic Internships, Courses, Projects management
- Student registration & login portal
- Razorpay payment integration
- Automatic PDF certificate generation
- Certificate verification system
- Admin panel with full CRUD
- Email notifications
- SEO-ready (sitemap, robots.txt, meta tags)
- Responsive design (mobile, tablet, desktop)

---

## Quick Start

### 1. Clone & Setup
```bash
cd Vignan
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

### 2. Configure Environment
Edit `.env` file with your credentials:
```
DB_NAME=vignan_techsolutions
DB_USER=root
DB_PASSWORD=your_mysql_password
RAZORPAY_KEY_ID=rzp_test_xxxx
RAZORPAY_KEY_SECRET=xxxx
EMAIL_HOST_USER=your@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

### 3. Create MySQL Database
```sql
CREATE DATABASE vignan_techsolutions CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### 5. Run Development Server
```bash
python manage.py runserver
```
Visit: http://127.0.0.1:8000

---

## Admin Panel
URL: http://127.0.0.1:8000/admin/
- Add internships, courses, projects
- Manage students and payments
- Issue certificates (mark enrollment as "completed" → use "Issue certificates" action)

## Adding Content
1. Login to admin panel
2. Add **Categories** first (for courses)
3. Add **Courses** with modules and materials
4. Add **Internships** with topics and benefits
5. Add **Projects** with screenshots
6. Add **Testimonials**

---

## Deployment (Production)

### Environment
```
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECRET_KEY=<strong-random-key>
```

### Gunicorn
```bash
gunicorn vignan_tech.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

### Nginx Config (example)
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /static/ { alias /path/to/Vignan/staticfiles/; }
    location /media/  { alias /path/to/Vignan/media/; }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### SSL (Let's Encrypt)
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## Project Structure
```
Vignan/
├── vignan_tech/        # Project settings & URLs
├── core/               # Home, About, Contact, Corporate Training
├── accounts/           # Auth, Student Profile, Dashboard
├── courses/            # Course listing & detail
├── internships/        # Internship listing & detail
├── projects/           # Project portfolio
├── payments/           # Razorpay integration, Enrollment
├── certificates/       # PDF generation & verification
├── templates/          # All HTML templates
├── static/             # CSS, JS, images
├── media/              # User uploads
├── .env                # Environment variables
└── requirements.txt
```

---

## Payment Flow
1. Student clicks "Enroll Now" on course/internship
2. Razorpay order is created → checkout page shown
3. Student pays via Razorpay modal
4. Callback verifies HMAC signature
5. Enrollment status set to "active"

## Certificate Flow
1. Admin marks enrollment as "completed"
2. Admin selects enrollments → "Issue certificates" action
3. PDF certificate auto-generated with unique UUID
4. Student downloads from dashboard
5. Anyone can verify at `/certificates/verify/`

---

## Security
- CSRF protection on all forms
- HMAC signature verification for Razorpay
- Password hashing (Django default: PBKDF2)
- Login required decorators on protected views
- Production security headers (HSTS, XSS, etc.) when DEBUG=False

---

© 2024 Vignan TechSolutions. All rights reserved.
