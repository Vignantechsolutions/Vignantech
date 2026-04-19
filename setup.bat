@echo off
echo ============================================
echo  Vignan TechSolutions - Setup Script
echo ============================================
echo.
echo IMPORTANT: Before running this script:
echo 1. Open .env file and set DB_PASSWORD to your MySQL root password
echo 2. Make sure MySQL Server 8.0 is running
echo.
pause

echo [1/5] Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (echo ERROR: pip install failed && pause && exit /b 1)
echo Done.
echo.

echo [2/5] Creating MySQL database...
echo Enter your MySQL root password when prompted:
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p -e "CREATE DATABASE IF NOT EXISTS vignan_techsolutions CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci; SELECT 'Database ready!' AS Status;"
if %errorlevel% neq 0 (echo ERROR: Database creation failed. Check your MySQL password in .env && pause && exit /b 1)
echo Done.
echo.

echo [3/5] Running Django migrations...
python manage.py migrate
if %errorlevel% neq 0 (echo ERROR: Migration failed && pause && exit /b 1)
echo Done.
echo.

echo [4/5] Loading sample data...
python manage.py load_sample_data
echo Done.
echo.

echo [5/5] Collecting static files...
python manage.py collectstatic --noinput
echo Done.
echo.

echo ============================================
echo  Setup Complete!
echo ============================================
echo.
echo Now create your admin account:
python manage.py createsuperuser
echo.
echo Start the development server:
echo   python manage.py runserver
echo.
echo URLs:
echo   Website : http://127.0.0.1:8000
echo   Admin   : http://127.0.0.1:8000/admin/
echo.
pause
