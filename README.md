# AIS Canteen Pre-order (starter)

A small Flask Progressive Web App you build over four lessons, then test in
the last one. Students pre-order their canteen lunch; the app saves each order.

All commands here are for a Mac, so they use `python3`. Use **Google Chrome**
for this unit: later lessons use its DevTools.

The app runs on port **8000**, not 5000, because AirPlay Receiver uses port
5000 on a Mac.

## Run it

### Option A: GitHub Codespace (nothing to install)

Open the repo in a Codespace. It installs Flask and the SQLite Viewer
extension for you. In the terminal:

```
python3 main.py
```

Your app opens in a new browser tab. If it does not, open the **Ports** tab
and click the globe icon on port 8000.

### Option B: your own Mac with VS Code

Make a virtual environment first. It is a private copy of Python just for this
project, so installing Flask never clashes with anything else on your Mac.

**Easiest way, inside VS Code**

1. Open the project folder in VS Code and install the **Python** extension.
2. Press `Cmd+Shift+P`, type **Python: Create Environment**, choose **Venv**,
   pick your Python 3, and tick `requirements.txt` when it asks what to install.
3. Open a new terminal (**Terminal > New Terminal**). You should see
   `(.venv)` at the start of the line.

**Or in the terminal**

```
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

Then run the app:

```
python3 main.py
```

Open http://127.0.0.1:8000 in **Google Chrome**.

Save a file and refresh the page to see your change: the app reloads itself.
If the terminal shows an error and the app stops, fix the error and run
`python3 main.py` again.

When you write the menu SQL (Period 1), build the database with
`python3 setup_db.py` before running the app.

**No `(.venv)` in the terminal?** Press `Cmd+Shift+P`, choose
**Python: Select Interpreter**, pick the one inside `.venv`, then open a new
terminal.

SQLite itself comes with Python (the `sqlite3` library), so there is nothing
extra to install. The SQLite Viewer extension just lets you look inside
`ais.db` by clicking the file in VS Code.

Test accounts (for when your login works): **aisha / sunflower22**,
**ben / basketball7**.

## What is already built

- The app set-up, the database helper (`get_db()`) and the sign-in cookie helper
- The `users` and `feedback` tables, filled with fake data
- A dashboard with a canteen feedback board
- The page frame (`base.html`) with a menu bar
- The manifest, the service worker and an offline page (the PWA parts)
- `foundations.py`, a Python warm-up you run in Period 0

## What you build

Look for `# TODO` in the code. Each one belongs to a lesson.

- **Period 0 - Foundations.** Finish the TODOs in `foundations.py`: functions,
  tuples and dictionaries.
- **Period 1 - The menu.** In `setup_db.py`, write the SQL to create a `menu`
  table and insert at least seven items. Run it, look at it in the SQLite
  Viewer. Then in `main.py` read the menu rows in `/menu`, and in
  `templates/menu.html` loop over them.
- **Period 2 - Login and logout.** Build the sign-in form in
  `templates/login.html`, the `/login` route and the `/logout` route in
  `main.py`.
- **Period 3 - Orders.** Add the `orders` table in `setup_db.py`, save an
  order in `/order`, and show each student their own orders in `/my-orders`
  and `templates/my_orders.html`.

## Files

| File | What it is |
| --- | --- |
| `main.py` | The Flask app: routes and the database helper |
| `setup_db.py` | You write the SQL that builds the menu and orders tables |
| `foundations.py` | Period 0 Python warm-up |
| `templates/` | The pages (`base`, `login`, `dashboard`, `menu`, `my_orders`, `offline`) |
| `static/` | Stylesheet, icon, manifest, service worker, `app.js` |
| `requirements.txt` | Flask |

Training sandbox: fake data only, debug off. Only ever test your own copy.
