# KUSA UMD Official Website

**Live Site**: [https://www.umdkusa.com](https://www.umdkusa.com)  
![License: Proprietary](https://img.shields.io/badge/License-Proprietary-blue.svg)

Official website of the Korean Undergraduate Student Association (KUSA) at the
University of Maryland. A Flask application that serves the public KUSA pages,
provides an authenticated document (file) upload area, and renders a news feed
scraped from an external source with optional AI-generated Korean comments.

---

## 🌟 Highlights
- **Poetry-based dependency management**: Reproducible installs via Poetry and `poetry.lock`.
- **Database via SQLAlchemy + Alembic**: SQLite by default for local development, PostgreSQL in production. Schema migrations are managed with Flask-Migrate.
- **Authenticated upload area**: HTTP Basic Auth–protected upload/delete endpoints with brute-force protection (per-IP failed-attempt blocking).
- **AI news feed**: Scrapes recent articles and (when an OpenAI key is configured) annotates each with a one-line Korean comment.

---

## 🛠 Tech Stack
**Backend**: Flask (Python 3.11+) | **ORM/DB**: SQLAlchemy, Flask-Migrate (Alembic); SQLite (dev) / PostgreSQL (prod)  
**Integrations**: OpenAI API (news comments), `requests` + BeautifulSoup (news scraping)  
**Frontend**: Jinja2 templates, HTML5, CSS3 (Bootstrap), vanilla JS  
**Tooling**: Poetry, pytest, ruff, pyright

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.11 or newer
- [Poetry](https://python-poetry.org/)

### 2. Clone & Install
```bash
git clone https://github.com/sueun-dev/umd-kusa-official-website.git
cd umd-kusa-official-website
poetry install   # Installs all dependencies (incl. dev tools)
```

### 3. Configure Environment (optional)
All settings have working defaults, so the app runs without any configuration
(it falls back to a local SQLite database `app.db` and the credentials
`admin` / `password`). For anything beyond local tinkering, create a `.env`
file in the project root:

```dotenv
# Database (defaults to sqlite:///app.db if unset)
DATABASE_URL="postgresql+psycopg2://user:password@localhost:5432/kusa_db"

# Flask session secret (defaults to an insecure value if unset)
FLASK_SECRET_KEY="your-random-secret-key"

# Credentials for the /upload and /delete admin area
UPLOAD_USERNAME="admin"
UPLOAD_PASSWORD="change-me"

# Optional: enable AI comments on the /news page
OPENAI_API_KEY="sk-..."
OPENAI_DEFAULT_MODEL="gpt-4o-mini"
```

> Note: the variable names above are read directly by `app/config.py` and
> `app/routes/new.py`. If `OPENAI_API_KEY` / `OPENAI_DEFAULT_MODEL` are not set,
> the news page still renders and each item simply shows "코멘트 없음".

### 4. (Optional) Run database migrations
For a fresh local SQLite database this step is not required — `run.py` calls
`db.create_all()` on startup. To apply the tracked Alembic migrations instead:

```bash
poetry run flask --app run db upgrade
```

### 5. Run the App
```bash
poetry run python run.py   # Starts the Flask dev server on http://127.0.0.1:8080
```

---

## 🧭 Routes
| Path                 | Method     | Description                                              |
| -------------------- | ---------- | ------------------------------------------------------- |
| `/`                  | GET        | Home page                                               |
| `/about`             | GET        | About page                                              |
| `/news/`             | GET        | News feed (scraped + optional AI comments, 24h cache)   |
| `/upload`            | GET/POST   | Authenticated file upload area                           |
| `/delete/<file_id>`  | POST       | Delete an uploaded file (authenticated)                  |
| `/download/<filename>` | GET      | Download an uploaded file                                |
| `/api`               | GET        | JSON list of uploaded files                              |
| `/robots.txt`        | GET        | robots.txt                                               |

---

## 🔒 Security Features
- **Brute-force protection**: After `MAX_ATTEMPTS` (default **7**) failed Basic-Auth
  logins, the source IP is blocked for `BLOCK_TIME` (default **24 hours**). Tracking
  is in-memory and resets on restart (see `app/decorators.py`).
- **Upload restrictions**:
  - Allowed extensions: `pdf, docx, png, jpeg, jpg, gif, bmp, svg, txt, rtf, csv, html`
    (see `Config.ALLOWED_EXTENSIONS`).
  - Maximum request size: **12 MB** (`MAX_CONTENT_LENGTH`).
  - Filenames are sanitized with Werkzeug's `secure_filename`.

---

## 🧪 Testing & Linting
```bash
poetry run pytest    # Run the test suite (tests/)
poetry run ruff check .   # Lint
poetry run pyright       # Type-check
```

---

## ☁️ Deployment Notes
Production runs the same app behind Nginx with HTTPS, backed by PostgreSQL.

1. Provision a Linux instance and set the `.env` variables above (use a real
   `DATABASE_URL`, `FLASK_SECRET_KEY`, and `UPLOAD_USERNAME` / `UPLOAD_PASSWORD`).
2. Apply migrations: `poetry run flask --app run db upgrade`.
3. Serve with a production WSGI server (e.g. Gunicorn) behind Nginx, and obtain
   TLS certificates with Certbot:
   ```bash
   sudo certbot --nginx -d umdkusa.com -d www.umdkusa.com
   ```

---

## 📂 Project Layout
```
app/
  __init__.py     # App factory (create_app), db & migrate setup
  config.py       # Configuration & environment variables
  models.py       # SQLAlchemy models (PDFFile)
  decorators.py   # Basic-Auth + IP brute-force protection
  exceptions.py   # Custom error handlers
  utils.py        # Helpers (allowed_file)
  routes/
    main.py       # Home, about, upload/delete/download, /api
    new.py        # /news feed + OpenAI comment generation
migrations/       # Alembic / Flask-Migrate
templates/        # Jinja2 templates
static/           # CSS, JS, images, libs
tests/            # pytest suite
run.py            # Entry point (port 8080)
```

---

## 📜 License
Proprietary software owned by the Korean Undergraduate Student Association (KUSA)
at the University of Maryland.
**Unauthorized use, modification, or distribution is strictly prohibited.**

---

## 🇰🇷 한국어 요약
메릴랜드 대학교 한인 학부생 협회(KUSA) 공식 웹사이트입니다.

**기술 스택**: Flask (Python 3.11+), SQLAlchemy/Flask-Migrate, SQLite(개발)·PostgreSQL(운영), OpenAI API  
**주요 기능**:
- Poetry 기반 의존성 관리
- HTTP Basic 인증으로 보호되는 파일 업로드/삭제 영역
- 로그인 실패 시 IP 차단(기본 7회 실패 후 24시간 차단)
- 외부 뉴스 스크래핑 + (키 설정 시) AI 한국어 코멘트 생성

**실행 방법**:
1. `poetry install`로 패키지 설치
2. (선택) `.env`에 `DATABASE_URL`, `FLASK_SECRET_KEY`, `UPLOAD_USERNAME/UPLOAD_PASSWORD` 등 설정
3. `poetry run python run.py`로 서버 실행 (http://127.0.0.1:8080)

---

## Developer
**Developer**: Sueun Cho

**E-mail**: sueun.dev@gmail.com

**LinkedIn**: [LinkedIn](https://www.linkedin.com/in/sueun-cho-625262252/)
