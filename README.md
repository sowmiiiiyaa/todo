# Simple Flask To‑Do App

This is a minimal responsive To‑Do app using Flask and SQLite with a soft pastel lavender theme.

Quick start (PowerShell):

```powershell
python -m venv venv
.\.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000 in your browser.

Notes:
- The SQLite DB is stored at `instance/todos.db` and is created automatically.
- Routes:
  - `GET /` — list todos
  - `POST /add` — add a todo (form field `title`)
  - `POST /toggle/<id>` — toggle complete
  - `POST /delete/<id>` — delete todo
