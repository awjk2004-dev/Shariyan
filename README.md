# Shariyan

Shariyan is a digital blood donation platform that connects blood donors with people who need blood in Kassala, Sudan. The system provides donor search, blood requests, notifications, messaging, reports, and an administrator dashboard.

## Main Technologies

- Backend: Python and FastAPI
- Database: MySQL with SQLAlchemy
- Authentication: JWT
- Frontend: HTML, CSS, and JavaScript
- Local tools: XAMPP, MySQL, phpMyAdmin, and Visual Studio Code
- Documentation: Swagger at `/docs`

## Requirements

Install the following before running the project:

- Python 3.12 or later
- XAMPP with MySQL enabled
- Visual Studio Code, recommended
- A modern web browser

## Project Setup

Open PowerShell in the project root:

```powershell
cd "C:\Users\AHMED\OneDrive\Desktop\Shariyan"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell blocks script activation, run the commands without activation:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Configure Environment Variables

Create `.env` from `.env.example`:

```powershell
Copy-Item .env.example .env
```

Update `.env` with your local database settings. Example:

```text
DATABASE_URL=mysql+pymysql://root:@127.0.0.1:3306/shariyan
SECRET_KEY=development-only-example-key-do-not-deploy-0123456789
ACCESS_TOKEN_EXPIRE_MINUTES=60
CORS_ORIGINS=http://localhost:5500,http://127.0.0.1:5500
ADMIN_BOOTSTRAP_TOKEN=use-a-long-random-token
RATE_LIMIT=60/minute
```

Do not publish `.env` or share its secret values. The `.env.example` file is only a safe configuration template.

## Start MySQL with XAMPP

1. Open the XAMPP Control Panel.
2. Start MySQL.
3. Open phpMyAdmin at `http://127.0.0.1/phpmyadmin`.
4. Create a database named `shariyan` if it does not already exist.
5. Make sure the database name and credentials match `DATABASE_URL` in `.env`.

## Apply Database Migrations

Run this command from the project root:

```powershell
.\.venv\Scripts\python.exe -m alembic upgrade head
```

## Start the Backend API

Open a PowerShell terminal in the project root:

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

API health check:

```text
http://127.0.0.1:8000/api/health
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## Start the Frontend

Open a second PowerShell terminal in the project root:

```powershell
.\.venv\Scripts\python.exe -m http.server 5500 --directory frontend
```

Open the main page:

```text
http://127.0.0.1:5500/index.html
```

Important pages:

```text
http://127.0.0.1:5500/about.html
http://127.0.0.1:5500/login.html
http://127.0.0.1:5500/donors.html
http://127.0.0.1:5500/requests.html
http://127.0.0.1:5500/leaderboard.html
http://127.0.0.1:5500/dashboard.html
http://127.0.0.1:5500/admin.html
```

The frontend does not require an external CDN for its main interface and can be served locally. The API and MySQL server must still be running to load and save live data.

## Create the First Administrator

1. Open the registration page:

```text
http://127.0.0.1:5500/register.html
```

2. Create the first user account.
3. Promote the first user to administrator using the bootstrap endpoint and the token from `.env`.

PowerShell example:

```powershell
$token = (Get-Content .env | Where-Object { $_ -like 'ADMIN_BOOTSTRAP_TOKEN=*' }) -replace '^ADMIN_BOOTSTRAP_TOKEN=',''
$headers = @{ 'X-Admin-Bootstrap-Token' = $token }
Invoke-RestMethod -Uri http://127.0.0.1:8000/api/auth/bootstrap-admin -Method Post -Headers $headers
```

Then sign in again. The administrator can open:

```text
http://127.0.0.1:5500/dashboard.html
http://127.0.0.1:5500/admin.html
```

The administrator dashboard provides statistics, request reports, user management, request status management, and city or neighborhood editing.

## Demo Data

To recreate the demo users, donors, and blood requests, make sure MySQL is running and execute:

```powershell
.\.venv\Scripts\python.exe backend\seed_demo_data.py
```

This command replaces the existing demo users, donors, and requests in the configured database. Use it only for development or demonstration environments.

The demo donor password is:

```text
demo12345
```

## Run Tests

The regular test suite uses an isolated SQLite database:

```powershell
.\.venv\Scripts\python.exe -m pytest backend/tests -q
```

The expected result is 9 passing tests when the MySQL connection test is enabled and configured.

To test the real MySQL connection:

```powershell
$env:MYSQL_TEST_DATABASE_URL = "mysql+pymysql://root:@127.0.0.1:3306/shريان"
.\.venv\Scripts\python.exe -m pytest backend/tests/test_mysql_connection.py -q
```

## Production Deployment Preparation

Generate separate random values for `SECRET_KEY` and `ADMIN_BOOTSTRAP_TOKEN` (at least 32 characters each), then set these variables in the hosting provider's secret/environment settings. For example, PowerShell can generate a random value with `[Convert]::ToBase64String([Security.Cryptography.RandomNumberGenerator]::GetBytes(48))`. Do not reuse the example value, commit production values, or upload `.env`:

```text
APP_ENV=production
DATABASE_URL=mysql+pymysql://USER:PASSWORD@HOST:PORT/DATABASE
DB_SSL_CA=/path/to/provider-ca.pem
SECRET_KEY=<random value with at least 32 characters>
ADMIN_BOOTSTRAP_TOKEN=<random value with at least 32 characters>
CORS_ORIGINS=https://your-frontend-domain.example
```

For Aiven, download its CA certificate and set `DB_SSL_CA` to the certificate path. Production startup rejects SQLite, missing CA verification, weak secrets, and non-HTTPS/local CORS origins. Interactive API documentation is disabled in production. Run migrations with `python -m alembic upgrade head` before starting the API, and do not run the demo-data seeder in production. Remove `ADMIN_BOOTSTRAP_TOKEN` from the hosting settings after creating the first administrator.

The frontend's Three.js and Cairo font files are stored under `frontend/vendor/` and `frontend/assets/`; static hosting does not need to publish `node_modules/`. When the hosting URLs are chosen, set the public backend API base URL (including `/api`) in `frontend/js/config.js`. This URL is public configuration, never a secret.

## Useful API Endpoints

- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me`
- `POST /api/auth/bootstrap-admin`
- `POST /api/donors/me`
- `GET /api/donors?blood_type=O%2B&city=كسلا`
- `GET /api/donors/leaderboard`
- `POST /api/requests`
- `GET /api/requests`
- `GET /api/notifications`
- `PATCH /api/notifications/{id}/read`
- `GET /api/admin/reports/overview`
- `PATCH /api/admin/users/{user_id}/city`

Detailed API documentation is available in [docs/API.md](docs/API.md).

## Project Structure

- `backend/`: FastAPI application, models, schemas, authentication, routers, and tests.
- `frontend/`: HTML pages, CSS files, and JavaScript.
- `alembic/`: Database migration files.
- `docs/`: API documentation, screenshots, and the Chapter Four Word document.
- `.env`: Local secrets and database configuration; do not publish it.
- `.env.example`: Safe configuration template.
- `requirements.txt`: Python dependencies.

## Notes

- The leaderboard score is currently a readiness indicator based on donor profile data, not a verified count of real donations.
- The demo data is for presentation and testing only.
- Change all development secrets before any real deployment.
