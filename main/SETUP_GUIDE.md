# 🚀 UPDATERS - Complete Development Environment Setup Guide

## 📋 Prerequisites

- Python 3.10+ installed
- pip (Python package manager)
- Git (for version control)
- PostgreSQL (optional, only for production-like testing)

---

## 🔧 Step-by-Step Setup Instructions

### 1️⃣ Clone the Repository (if not already done)

```bash
git clone <repository-url>
cd UPDATERS
```

### 2️⃣ Create a Virtual Environment

**Windows (PowerShell):**
```powershell
cd main
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
cd main
python -m venv venv
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
cd main
python3 -m venv venv
source venv/bin/activate
```

### 3 Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Expected packages to be installed:**
- Django 5.2.7
- pillow 12.0.0 (image processing)
- python-decouple 3.8 (environment variables)
- dj-database-url 3.0.1 (database configuration)
- whitenoise 6.11.0 (static files)
- gunicorn 23.0.0 (production server)
- psycopg2-binary 2.9.11 (PostgreSQL adapter)

### 4 Configure Environment Variables

Copy the example environment file:

```bash
copy .env.example .env
```

Edit .env and set your values:

```env
SECRET_KEY=your-generated-secret-key-here
DEBUG=True
```

** Generate a SECRET_KEY:**

Option 1 - Using Python:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Option 2 - Online generator:
Visit: https://djecrety.ir/

### 5 Run Database Migrations

```bash
python manage.py migrate
```

This will create the SQLite database with all necessary tables.

### 6 Load Initial Data (Categories)

```bash
python manage.py loaddata feed/fixtures/categories.json
```

This loads the predefined categories (Política, Economia, Internacional, etc.)

### 7 Create a Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

### 8 Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 9 Run the Development Server

```bash
python manage.py runserver
```

The application will be available at: **http://127.0.0.1:8000/**

Admin panel: **http://127.0.0.1:8000/admin/**

---

##  Project Structure

```
UPDATERS/
 main/                      # Django project root
    core/                  # Project settings
       settings.py        # Main configuration
       urls.py            # URL routing
       wsgi.py            # WSGI configuration
    feed/                  # News feed app
       models.py          # Article, Category, ArticleViewLog
       views.py           # Views for articles
       templates/         # HTML templates
       static/            # CSS, JS, images
       fixtures/          # Initial data
    login/                 # Authentication app
       views.py           # Login/Register views
       templates/         # Auth templates
    media/                 # User-uploaded files
    staticfiles/           # Collected static files (generated)
    requirements.txt       # Python dependencies
    .env.example           # Environment variables template
    Procfile               # Production deployment config
    manage.py              # Django management script
 README.md
```

---

##  Database Configuration

### Development (Default)
- **Database**: SQLite
- **File**: main/db.sqlite3
- **No additional setup required**

### Production (PostgreSQL)
Set the DATABASE_URL environment variable:

```env
DATABASE_URL=postgresql://username:password@host:port/database
```

---

##  Frontend Dependencies

**No build tools required!** This project uses traditional Django templates with:
- Plain CSS (in eed/static/feed/css/)
- Plain JavaScript (if any)
- No npm, webpack, or vite needed

---

##  Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| SECRET_KEY |  Yes | None | Django secret key for cryptographic signing |
| DEBUG |  No | False | Enable debug mode (True for development) |
| DATABASE_URL |  No | SQLite | PostgreSQL connection string (production) |
| RENDER_EXTERNAL_HOSTNAME |  No | None | Hostname for Render.com deployment |

---

##  Testing the Setup

### 1. Check if all migrations are applied:
```bash
python manage.py showmigrations
```

All migrations should have [X] marks.

### 2. Verify installed apps:
```bash
python manage.py check
```

Should show: **System check identified no issues (0 silenced).**

### 3. Test the admin panel:
- Go to http://127.0.0.1:8000/admin/
- Login with your superuser credentials
- You should see: Articles, Categories, Article View Logs, Users

### 4. Create a test article:
- In admin, go to "Articles"
- Click "Add Article"
- Fill in the form and upload an image
- Save and view on the homepage

---

##  Production Deployment (Render.com)

### Prerequisites:
1. Create account on Render.com
2. Create a PostgreSQL database
3. Create a Web Service

### Environment Variables (Render):
```
SECRET_KEY=<your-production-secret-key>
DEBUG=False
DATABASE_URL=<provided-by-render-postgres>
RENDER_EXTERNAL_HOSTNAME=<your-app>.onrender.com
```

### Build Command:
```bash
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
```

### Start Command:
```bash
gunicorn core.wsgi --log-file -
```

---

##  Troubleshooting

### Issue: "No module named 'decouple'"
**Solution:** Make sure you're in the virtual environment and run:
```bash
pip install python-decouple
```

### Issue: "SECRET_KEY not found"
**Solution:** Create a .env file in the main/ directory with:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
```

### Issue: "No such table: feed_category"
**Solution:** Run migrations:
```bash
python manage.py migrate
python manage.py loaddata feed/fixtures/categories.json
```

### Issue: Images not displaying
**Solution:** Make sure you're running in DEBUG mode or have collected static files:
```bash
python manage.py collectstatic
```

### Issue: "Pillow" installation fails on Windows
**Solution:** Install Visual C++ Build Tools or use a pre-built wheel:
```bash
pip install --upgrade pillow
```

---

##  Quick Start Commands (Summary)

```bash
# Navigate to project
cd main

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell

# Install dependencies
pip install -r requirements.txt

# Setup environment
copy .env.example .env
# Edit .env and add SECRET_KEY

# Setup database
python manage.py migrate
python manage.py loaddata feed/fixtures/categories.json
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Run server
python manage.py runserver
```

---

##  Verification Checklist

- [ ] Virtual environment created and activated
- [ ] All dependencies installed (pip list shows Django, pillow, etc.)
- [ ] .env file created with SECRET_KEY
- [ ] Database migrations applied
- [ ] Categories loaded from fixtures
- [ ] Superuser created
- [ ] Static files collected
- [ ] Development server runs without errors
- [ ] Admin panel accessible
- [ ] Can create and view articles

---

##  Additional Resources

- **Django Documentation**: https://docs.djangoproject.com/en/5.2/
- **Pillow Documentation**: https://pillow.readthedocs.io/
- **WhiteNoise Documentation**: http://whitenoise.evans.io/
- **Render Deployment Guide**: https://render.com/docs/deploy-django

---

##  Need Help?

If you encounter any issues not covered in this guide, please:
1. Check the Django error messages carefully
2. Verify all environment variables are set correctly
3. Ensure you're in the virtual environment
4. Check that all migrations are applied

---

** You're all set! Happy coding with UPDATERS! **
