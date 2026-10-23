# CampusFix AI

A compact Flask + SQLite campus maintenance tracker. Students can submit free text without sharing their identity, receive a ticket ID, and check ticket status. Admins can search, filter, assign, and update tickets.

## Local run (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Set a real `SECRET_KEY` and `ADMIN_PASSWORD_HASH` in `.env`. To generate a hash without writing a password to source control:

```powershell
py -c "from getpass import getpass; from werkzeug.security import generate_password_hash; print(generate_password_hash(getpass('Admin password: ')))"
```

Paste the printed hash as `ADMIN_PASSWORD_HASH`. Load `.env` into the current PowerShell session (Flask does not load it automatically):

```powershell
Get-Content .env | Where-Object { $_ -match '^\s*[^#].*=.*$' } | ForEach-Object { $name,$value = $_ -split '=',2; Set-Item -Path "Env:$name" -Value $value }
flask --app app run --debug
```

The database initializes automatically. Without `GEMINI_API_KEY`, reporting works in manual mode. If configured, extraction uses the official Google GenAI Python SDK. Gemini failures fall back to the original report. Priority is always assessed by deterministic server-side rules.

To add sample data explicitly, use `flask --app app seed-demo` against a demo database. This inserts visibly ordinary demo examples; do not run it on production.

## Tests

```powershell
py -m unittest discover -s tests -v
```

## Deploy to Render

1. Push this project to a Git repository and create a Render **Web Service** from it.
2. Runtime: Python. Build command: `pip install -r requirements.txt`. Start command: `gunicorn app:app` (also in `Procfile`).
3. Add environment variables: `SECRET_KEY` (random, long secret), `ADMIN_PASSWORD_HASH` (Werkzeug hash generated above), `DATABASE_PATH` (for example `/var/data/campusfix.sqlite`), `COOKIE_SECURE=true`, and optionally `GEMINI_API_KEY` and `GEMINI_MODEL`.
4. Attach a persistent disk and mount it at `/var/data` if you want SQLite records to survive deploys/restarts. Set `DATABASE_PATH=/var/data/campusfix.sqlite`. Without persistent storage, the SQLite file may be ephemeral.

The app initializes the schema at startup. The initial admin credential is the password whose Werkzeug hash you provide in `ADMIN_PASSWORD_HASH`; keep the plaintext password in a password manager and never commit it. Use HTTPS in production. The app sets HttpOnly/SameSite cookies and supports secure cookies through `COOKIE_SECURE`. Set `TRUST_PROXY=1` only when hosted behind a trusted single proxy.

## Push to a public repository

Replace the URL with your own repository:

```powershell
git init
git add .
git commit -m "Build CampusFix AI MVP"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

If the remote is already configured, use `git add .`, `git commit -m "Build CampusFix AI MVP"`, and `git push`.

## Notes

- Public ticket pages intentionally omit assignee and reporter information.
- Priority labels communicate triage rules, not a confirmed hazard. Immediate danger must be reported to campus authorities/emergency services; the app does not provide emergency response.
- Optional photos are not enabled in this MVP.
- Configure a persistent disk for SQLite on Render. For higher traffic or multiple instances, use managed PostgreSQL instead.
