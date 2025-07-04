# BinGo / bingo-backend 🍃♻️

Django + Celery back-end that powers the BinGo mobile app  
(scan QR → upload photo → ChatGPT classifies trash → points & rewards).

---

## 1 · Quick start (macOS 13 + Homebrew)

```bash
# Clone
git clone https://github.com/SedrakyanGnel/bingo-backend.git
cd bingo-backend

# System deps
brew update
brew install python@3.12 redis postgresql@15

# Start Redis as a login service (survives reboots)
brew services start redis          # \`redis-cli ping\` → PONG

# Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python libs
pip install --upgrade pip wheel setuptools
pip install -r requirements.txt    # or paste the list below
```

<details>
<summary><strong>requirements.txt (if you need to generate it)</strong></summary>

```
Django~=5.0
djangorestframework
djangorestframework-simplejwt
django-environ
pillow
psycopg2-binary
celery
redis
boto3
django-storages
openai
```
</details>

---

## 2 · Environment variables

Create a file named **\`.env\`** in the project root:

```env
DJANGO_SECRET_KEY=change-me-please
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
DJANGO_DEBUG=True
```

*(anything not set falls back to sane defaults; database defaults to SQLite in dev)*

---

## 3 · Database & static/media

```bash
python manage.py migrate
python manage.py createsuperuser
```

Uploaded photos land in \`media/\` (local).  
Static collection is skipped in development.

---

## 4 · Run services

### 4.1 Django dev server
```bash
python manage.py runserver 0.0.0.0:8000
```
*Open <http://localhost:8000/admin/> and log in.*

### 4.2 Celery worker (AI queue)
```bash
celery -A bingo worker -l INFO -Q ai
```
*Needs Redis reachable at \`redis://localhost:6379/0\` (see step 1).*

Now:

* \`POST /api/token/\` → receive JWT  
* \`POST /api/scans/\` (multipart: \`bin\`, \`image\`) → photo saved, Celery pushes it to GPT-4o, points awarded when classified.  
* \`GET /api/balance/\` → current balance  
* \`GET /api/rewards/\` + \`POST /api/redemptions/\` → shop workflow

---

## 5 · Handy one-liner for fresh installs

```bash
brew install redis python@3.12 && brew services start redis && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python manage.py migrate && python manage.py runserver
```

---

## 6 · Optional: Docker compose

```bash
docker compose up -d        # redis + web + worker
```

| Service    | Port | Notes                       |
|------------|------|-----------------------------|
| Django API | 8000 | \`localhost:8000\`            |
| Redis      | 6379 | broker / result backend     |
| Celery     | —    | runs in background container|

---

## 7 · Troubleshooting

| Symptom | Fix |
|---------|-----|
| \`Cannot connect to redis://localhost:6379\` | \`brew services start redis\` or \`docker compose up redis\` |
| \`ImportError: openai …\` | \`pip install openai\` inside **the same** \`venv\`; then restart worker |
| \`media/ … 404\` | in dev URLs are auto-served; ensure \`MEDIA_URL\`, \`MEDIA_ROOT\` are set in \`settings.py\` |

---

### © 2025 BinGo Team
Feel free to open issues or PRs!
