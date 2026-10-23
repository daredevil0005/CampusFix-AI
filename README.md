# 🏫 CampusFix-AI
### AI-Powered Campus Maintenance & Complaint Management System

CampusFix-AI is an AI-assisted campus maintenance platform that simplifies how students and campus members report maintenance issues. Powered by **Google Gemini**, it transforms natural-language complaints into structured maintenance tickets, helping campus staff organize, prioritize, and manage reported problems efficiently.

Built as a hackathon project with a focus on practical AI integration, security, and usability.

---

## ✨ Features

- **AI-Powered Complaint Processing:** Uses Google Gemini to extract structured information from natural-language complaints.
- **Smart Ticket Generation:** Creates maintenance tickets with unique ticket IDs.
- **Complaint Categorization:** Organizes reports into Plumbing, Electrical, Facilities, Cleaning, Safety, and Other.
- **Priority Classification:** Rule-based priority assignment for Normal, High, and Urgent issues.
- **Missing Information Suggestions:** Gemini can suggest follow-up questions for incomplete reports.
- **Duplicate Suggestions:** Shows potentially related open tickets at the same location.
- **Ticket Tracking:** Users can check their submitted ticket status.
- **Staff Dashboard:** View, search, filter, and manage maintenance tickets.
- **Admin Authentication:** Password-hash-based staff login.
- **AI Fallback:** Maintains basic complaint submission functionality when AI processing is unavailable.

---

## 🧠 How It Works

1. A user submits a campus maintenance complaint and location.
2. Gemini analyzes the complaint and attempts to extract structured information.
3. The backend validates the extracted fields.
4. A deterministic Python rules engine assigns ticket priority.
5. The application generates a ticket ID and stores the ticket in SQLite.
6. Campus staff can review, assign, update, and resolve tickets through the dashboard.

**AI is advisory:** Priority assignment and privileged operations are handled by backend logic rather than being delegated to Gemini.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend logic |
| Flask | Web application framework |
| Google Gemini API | AI-powered complaint processing |
| SQLite | Ticket database |
| HTML & CSS | User interface |
| JavaScript | Frontend interactions |
| Werkzeug | Password hashing and request utilities |
| python-dotenv | Local environment configuration |

---

## 📂 Project Structure

```text
CampusFix-AI/
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── Procfile
├── README.md
│
├── static/
│   ├── app.js
│   └── style.css
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── submitted.html
│   ├── ticket.html
│   └── admin.html
│
└── tests/
    └── test_app.py
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+ (use a version compatible with your installed dependencies)
- Git
- Google Gemini API key
- pip

### 1. Clone the repository

```bash
git clone https://github.com/daredevil0005/CampusFix-AI.git
cd CampusFix-AI
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run the application using the virtual environment's Python executable directly.

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create your local `.env` file:

```powershell
Copy-Item .env.example .env
```

Generate a strong Flask secret key:

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

Generate an admin password hash:

```powershell
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash(input('New admin password: ')))"
```

Open `.env` and configure:

```env
SECRET_KEY=your_generated_secret_key
DATABASE_PATH=./campusfix.db
ADMIN_PASSWORD_HASH=your_generated_password_hash
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.5-flash
COOKIE_SECURE=false
TRUST_PROXY=0
```

Replace the placeholder values with your own credentials.

**Security:** Never commit `.env` or expose your API key, password, or secret key.

### 5. Run the application

```powershell
python app.py
```

Open the application:

http://127.0.0.1:5000

---

## 🖥️ Application Usage

### For Users
1. Open the CampusFix-AI homepage.
2. Describe the maintenance problem.
3. Provide the issue location and category if requested.
4. Submit the complaint.
5. Save the generated ticket ID.
6. Track the ticket using its reference.

### For Campus Staff
1. Navigate to `/admin/login`.
2. Sign in using the configured admin password.
3. Review reported maintenance tickets.
4. Search and filter tickets.
5. Update ticket status and assignee.

Available ticket statuses:
- Submitted
- In Progress
- Resolved
- Closed

---

## 🔐 Security Considerations

- Environment variables are used for application secrets.
- Passwords are verified using Werkzeug password hashing.
- CSRF protection is implemented for POST requests.
- Session cookies use HTTP-only and SameSite settings.
- Proxy handling should only be enabled behind a properly configured trusted proxy.
- User-submitted content should be treated as untrusted input.
- Gemini output is not trusted for priority decisions or privileged operations.

**Production deployment:** Use HTTPS, secure cookie settings, strong secrets, and an appropriate persistent database. Configure environment variables through the hosting platform rather than committing credentials.

---

## 🧪 Testing

Run the test suite with:

```bash
python -m pytest -q
```

Make sure the test dependencies are installed before running tests.

---

## 🌱 Future Improvements

- Role-based access control for maintenance staff.
- Email or notification alerts for ticket updates.
- More advanced duplicate detection.
- Analytics for recurring campus maintenance issues.
- Image attachments for maintenance reports.
- Improved audit logs and reporting.
- Production-ready database deployment.

---

## 🎯 Project Goal

CampusFix-AI aims to bridge the gap between human-reported campus problems and structured maintenance workflows through practical AI-assisted automation.

It demonstrates how generative AI can improve real-world processes while keeping critical application decisions under backend control.

---

## 👨‍💻 Developer

**GitHub:** [@daredevil0005](https://github.com/daredevil0005)

**Repository:** [CampusFix-AI](https://github.com/daredevil0005/CampusFix-AI)

---

*Built with Python, Flask, Google Gemini, and a passion for solving real-world problems.*


- Public ticket pages intentionally omit assignee and reporter information.
- Priority labels communicate triage rules, not a confirmed hazard. Immediate danger must be reported to campus authorities/emergency services; the app does not provide emergency response.
- Optional photos are not enabled in this MVP.
- Configure a persistent disk for SQLite on Render. For higher traffic or multiple instances, use managed PostgreSQL instead.
