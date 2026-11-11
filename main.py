"""
AIS Canteen Pre-order (starter).

A Flask PWA you build over three lessons, then test in Lesson 4.

What is already here (the skeleton):
  - sign in / sign out
  - a dashboard with a canteen feedback board
  - a menu page that lists today's items

What YOU build (look for the `# TODO` markers):
  - Period 2: an `orders` table, and saving an order when a student picks an item
  - Period 3: a "My orders" page that shows each student their own orders

Run:    python main.py
Open:   http://127.0.0.1:5000        (on your own laptop)
        or the forwarded port 5000   (in a GitHub Codespace)

Sandbox: fake data only, debug mode off. In a Codespace each student has their
own private copy, so nothing you do reaches anyone else.
"""

import os
import base64
import secrets
import sqlite3
from datetime import datetime

from flask import (
    Flask, request, redirect, url_for, make_response, render_template,
    jsonify, send_from_directory, g,
)

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(APP_DIR, "ais.db")

app = Flask(__name__)


# --------------------------------------------------------------------------
# Today's canteen menu.
# This is a plain Python list, so you can edit it freely. Each item has an
# id (used by the order form), a name, and a price in dollars.
# --------------------------------------------------------------------------
MENU = [
    {"id": "nasi-lemak",   "name": "Nasi lemak",            "price": 3.50},
    {"id": "schnitzel",    "name": "Chicken schnitzel wrap", "price": 4.50},
    {"id": "laksa",        "name": "Singapore laksa",        "price": 4.00},
    {"id": "veg-sushi",    "name": "Vegetable sushi (6 pc)", "price": 3.80},
    {"id": "pie",          "name": "Aussie beef pie",        "price": 3.20},
    {"id": "fruit-cup",    "name": "Fresh fruit cup",        "price": 2.00},
    {"id": "mango-smoothie", "name": "Mango smoothie",        "price": 3.00},
]


def menu_lookup(item_id):
    """Return the menu item with this id, or None."""
    for item in MENU:
        if item["id"] == item_id:
            return item
    return None


# --------------------------------------------------------------------------
# Secrets (flags, the admin key, the admin password). These are not committed
# to the repo, so reading the code on GitHub does not hand you the answers.
# The order (later wins): a random value, then an optional local ctf_config.py,
# then environment variables (e.g. Codespaces secrets).
# --------------------------------------------------------------------------
def _rand_flag():
    return "FLAG{" + secrets.token_hex(6) + "}"


_cfg = {
    "FLAG_SQLI": _rand_flag(),
    "FLAG_XSS": _rand_flag(),
    "FLAG_SECRET": _rand_flag(),
    "ADMIN_API_KEY": "ais-admin-key-" + secrets.token_hex(3),
    "ADMIN_PASSWORD": secrets.token_urlsafe(9),
}
try:  # optional local override file (ctf_config.py is gitignored)
    import ctf_config as _local  # type: ignore
    for _k in _cfg:
        if hasattr(_local, _k):
            _cfg[_k] = getattr(_local, _k)
except Exception:
    pass
for _k in _cfg:  # environment variables win
    if os.environ.get(_k):
        _cfg[_k] = os.environ[_k]

FLAG_SQLI = _cfg["FLAG_SQLI"]
FLAG_XSS = _cfg["FLAG_XSS"]
FLAG_SECRET = _cfg["FLAG_SECRET"]
ADMIN_API_KEY = _cfg["ADMIN_API_KEY"]
ADMIN_PASSWORD = _cfg["ADMIN_PASSWORD"]


# --------------------------------------------------------------------------
# Database (seeded with fake data on first run)
# --------------------------------------------------------------------------
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT NOT NULL,
            message TEXT NOT NULL
        );

        -- TODO (Period 2): create an `orders` table.
        -- Each row is one student's order of one menu item. You will want:
        --   id        INTEGER PRIMARY KEY AUTOINCREMENT
        --   username  TEXT NOT NULL      (who ordered)
        --   item      TEXT NOT NULL      (the item name)
        --   price     REAL NOT NULL      (the price at the time)
        --   created   TEXT NOT NULL      (when they ordered)
        -- Write the CREATE TABLE IF NOT EXISTS statement here, then re-run.
        """
    )
    cur = db.execute("SELECT COUNT(*) AS n FROM users")
    if cur.fetchone()["n"] == 0:
        # admin is inserted first on purpose.
        db.executemany(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            [
                ("admin", ADMIN_PASSWORD, "admin"),
                ("aisha", "sunflower22", "user"),
                ("ben", "basketball7", "user"),
                ("chloe", "mango-lassi", "user"),
                ("lachlan", "redgum-koala", "user"),
                ("mia", "surfs-up-2011", "user"),
            ],
        )
    cur = db.execute("SELECT COUNT(*) AS n FROM feedback")
    if cur.fetchone()["n"] == 0:
        db.executemany(
            "INSERT INTO feedback (author, message) VALUES (?, ?)",
            [
                ("mia", "Please bring back the chicken rice on Mondays!"),
                ("ben", "The 9am pre-order cut-off is a bit early."),
            ],
        )
    db.commit()
    db.close()


# --------------------------------------------------------------------------
# Session helpers (a plain cookie; this is a classroom app, not production)
# --------------------------------------------------------------------------
def current_user():
    uid = request.cookies.get("uid")
    if not uid:
        return None
    row = get_db().execute(
        "SELECT username, role FROM users WHERE username = ?", (uid,)
    ).fetchone()
    return row


# --------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------
@app.route("/")
def index():
    if current_user():
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", error=None)

    username = request.form.get("username", "")
    password = request.form.get("password", "")

    # Look up the user by the username and password they typed, then sign
    # them in by setting a cookie.
    query = (
        "SELECT username, role FROM users "
        "WHERE username = '" + username + "' AND password = '" + password + "'"
    )
    try:
        row = get_db().execute(query).fetchone()
    except sqlite3.Error:
        row = None

    if row is None:
        return render_template("login.html", error="Incorrect username or password.")

    resp = make_response(redirect(url_for("dashboard")))
    resp.set_cookie("uid", row["username"], samesite="Lax")
    return resp


@app.route("/logout")
def logout():
    resp = make_response(redirect(url_for("login")))
    resp.delete_cookie("uid")
    resp.delete_cookie("debug_token")
    return resp


@app.route("/dashboard")
def dashboard():
    user = current_user()
    if not user:
        return redirect(url_for("login"))

    feedback = get_db().execute(
        "SELECT author, message FROM feedback ORDER BY id DESC"
    ).fetchall()

    admin_flag = FLAG_SQLI if user["role"] == "admin" else None

    resp = make_response(
        render_template(
            "dashboard.html",
            username=user["username"],
            role=user["role"],
            feedback=feedback,
            admin_flag=admin_flag,
        )
    )
    # A debug token the admin widget uses. Left readable by JavaScript for now.
    resp.set_cookie("debug_token", FLAG_XSS, samesite="Lax", httponly=False)
    return resp


@app.route("/menu")
def menu():
    """Show today's menu. Each item has an 'Order' button (built in menu.html)."""
    user = current_user()
    if not user:
        return redirect(url_for("login"))
    return render_template("menu.html", username=user["username"], menu=MENU)


@app.route("/order", methods=["POST"])
def place_order():
    user = current_user()
    if not user:
        return redirect(url_for("login"))

    item_id = request.form.get("item", "")
    item = menu_lookup(item_id)
    if item is None:
        return redirect(url_for("menu"))

    # TODO (Period 2): save this order.
    # Insert one row into the `orders` table using a PARAMETERISED query, so the
    # values go in as data, never as SQL. For example:
    #
    #   db = get_db()
    #   db.execute(
    #       "INSERT INTO orders (username, item, price, created) "
    #       "VALUES (?, ?, ?, ?)",
    #       (user["username"], item["name"], item["price"],
    #        datetime.now().strftime("%Y-%m-%d %H:%M")),
    #   )
    #   db.commit()
    #
    # Then send the student to their orders page.
    return redirect(url_for("my_orders"))


@app.route("/my-orders")
def my_orders():
    user = current_user()
    if not user:
        return redirect(url_for("login"))

    # TODO (Period 3): read THIS student's orders.
    # Select from `orders` WHERE username = ? (parameterised), newest first.
    # Work out how many orders there are and the total price, then pass them to
    # the template. For now we pass an empty list so the page still loads.
    #
    #   rows = get_db().execute(
    #       "SELECT item, price, created FROM orders "
    #       "WHERE username = ? ORDER BY id DESC", (user["username"],)
    #   ).fetchall()
    #   total = sum(r["price"] for r in rows)
    #
    orders = []
    total = 0.0
    return render_template(
        "my_orders.html", username=user["username"], orders=orders, total=total
    )


@app.route("/feedback", methods=["POST"])
def post_feedback():
    user = current_user()
    if not user:
        return redirect(url_for("login"))
    message = request.form.get("message", "").strip()
    if message:
        db = get_db()
        db.execute(
            "INSERT INTO feedback (author, message) VALUES (?, ?)",
            (user["username"], message),
        )
        db.commit()
    return redirect(url_for("dashboard"))


@app.route("/api/admin/feedback")
def admin_feedback_api():
    # The admin feed. It expects the secret admin key in the X-API-Key header.
    key = request.headers.get("X-API-Key", "")
    if key != ADMIN_API_KEY:
        return jsonify({"error": "unauthorized", "hint": "missing or wrong X-API-Key"}), 401
    rows = get_db().execute("SELECT author, message FROM feedback ORDER BY id DESC").fetchall()
    return jsonify({
        "flag": FLAG_SECRET,
        "feedback": [dict(r) for r in rows],
    })


@app.route("/config.js")
def config_js():
    # Client configuration, loaded by every page and cached by the service
    # worker. It carries the settings the front-end needs.
    b64 = base64.b64encode(ADMIN_API_KEY.encode()).decode()
    body = (
        "// Client configuration for the AIS Canteen Pre-order app.\n"
        "// Loaded by every page and cached by the service worker.\n"
        "const APP_CONFIG = {\n"
        '  apiBase: "/api",\n'
        "  pollSeconds: 30,\n"
        '  adminApiKeyB64: "' + b64 + '"\n'
        "};\n"
    )
    resp = app.response_class(body, mimetype="application/javascript")
    resp.headers["Cache-Control"] = "no-store"
    return resp


@app.route("/sw.js")
def service_worker():
    resp = send_from_directory(os.path.join(APP_DIR, "static"), "sw.js")
    resp.headers["Content-Type"] = "application/javascript"
    resp.headers["Service-Worker-Allowed"] = "/"
    return resp


if __name__ == "__main__":
    init_db()
    host = os.environ.get("HOST", "0.0.0.0")   # 0.0.0.0 so Codespaces can forward port 5000
    port = int(os.environ.get("PORT", "5000"))
    app.run(host=host, port=port, debug=False)
