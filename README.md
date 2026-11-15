# AIS Canteen Pre-order (starter)

A small Flask Progressive Web App you build over four lessons, then test in
the last one. Students pre-order their canteen lunch; the app saves each order.

## Run it

### Option A: GitHub Codespace (nothing to install)

Open the repo in a Codespace. It installs Flask and the SQLite Viewer
extension for you. In the terminal:

```
python main.py
```

Then click the forwarded port 5000.

### Option B: your own laptop with VS Code

Make a virtual environment first. It is a private copy of Python just for this
project. Inside it, the commands `python` and `pip` work the same on every
laptop (on a Mac, `python` does not exist until you do this).

**Easiest way, inside VS Code**

1. Open the project folder in VS Code and install the **Python** extension.
2. Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows), type
   **Python: Create Environment**, choose **Venv**, pick your Python 3, and
   tick `requirements.txt` when it asks what to install.
3. Open a new terminal (**Terminal > New Terminal**). You should see
   `(.venv)` at the start of the line. If you do, `python` and `pip` now work.

**Or in the terminal**

```
# Mac
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate

# Both
pip install -r requirements.txt
```

Then run the app:

```
python main.py
```

Open http://127.0.0.1:5000

When you write the menu SQL (Period 1), build the database with
`python setup_db.py` before running the app.

**Still no `(.venv)` in the terminal?** Press `Cmd+Shift+P` / `Ctrl+Shift+P`,
choose **Python: Select Interpreter**, pick the one inside `.venv`, then open a
new terminal.

**No virtual environment?** It also works without one if you use `python3` and
`python3 -m pip install -r requirements.txt` on a Mac. A virtual environment is
the safer choice because newer Python installs can refuse a plain `pip install`.

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
