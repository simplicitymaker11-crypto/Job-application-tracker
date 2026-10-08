# Job Application Tracker

A web app for job seekers to keep all their applications in one place. Add the company, role, date and status of each application, then search, edit or delete them as things change.

## Features
- Add, edit and delete job applications
- Search by company, role or status
- Track each application's status: Applied, Approved, Rejected or Pending
- Color-coded status labels

## Tech stack
Python, Flask, Flask-SQLAlchemy (SQLAlchemy 2), SQLite, Jinja2, HTML/CSS, and JavaScript (`fetch` for delete).

## Setup (Windows, PowerShell)

Requires Python 3.14.4.

1. Clone the repository:
```
   git clone https://github.com/simplicitymaker11-crypto/Job-application-tracker.git
   cd Job-application-tracker
```
2. Create and activate a virtual environment:
```
   python -m venv env
   env\Scripts\activate
```
3. Install dependencies:
```
   python -m pip install -r requirements.txt
```
4. Create the database tables (first run only):
```
   python -c "from app import app, db; app.app_context().push(); db.create_all()"
```
5. Start the app:
```
   python app.py
```
6. Open http://127.0.0.1:5000 in your browser.

## Usage
- **Add:** click *Add*, fill in company, role, date (optional, defaults to today) and status.
- **Search:** type in the header search box and press Enter. It matches company, role or status, ignoring case. An empty search shows everything.
- **Edit:** click *Edit* on a row.
- **Delete:** click *Delete* on a row and confirm. The row is removed through a `DELETE` request.

## Project structure
```
app.py              Flask app, database model and routes
requirements.txt    Pinned dependencies
templates/          Jinja2 templates (index, add, edit, about, contact, _header)
static/             CSS and logo image
instance/           SQLite database (created locally, not tracked by git)
```

## Routes
| Route | Method | Purpose |
|---|---|---|
| `/` | GET | List all applications |
| `/add` | GET, POST | Show and submit the add form |
| `/edit/<id>` | GET, POST | Show and submit the edit form |
| `/delete/<id>` | DELETE | Delete an application |
| `/search?q=` | GET | Filter by company, role or status |

## Known limitations
- No login: anyone who can reach the app can edit or delete every record, so it is for local use only.
- SQLite only. It is not configured for a hosted deployment.
- `app.py` runs with `debug=True`, which must be turned off before any deployment.
- Searching for `%` or `_` acts as a wildcard rather than a literal character.

## Author
Uzair Bashir