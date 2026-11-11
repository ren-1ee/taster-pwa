# AIS Canteen Pre-order (starter)

A small Flask Progressive Web App you build over three lessons, then test in
Lesson 4. Students pre-order their canteen lunch; the app saves each order.

## Run it

**On your laptop**
```
pip install -r requirements.txt
python setup_db.py      # after you write your SQL in it (Period 1)
python main.py
```
Open http://127.0.0.1:5000

**In a GitHub Codespace**
Open the repo in a Codespace. It installs Flask and the SQLite Viewer
extension automatically. Then run `python main.py` and click the forwarded
port 5000.

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

## What you build

Look for `# TODO` in the code. Each one belongs to a lesson.

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
| `templates/` | The pages (`base`, `login`, `dashboard`, `menu`, `my_orders`) |
| `static/` | Stylesheet, icon, manifest, service worker, `app.js` |
| `requirements.txt` | Flask |

Training sandbox: fake data only, debug off. Only ever test your own copy.
