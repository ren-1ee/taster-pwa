"""
AIS Canteen Pre-order (starter).

A Flask PWA you build over three lessons, then test in Lesson 4.

What is already here (the skeleton):
  - the app set-up, the database helper and the sign-in cookie helper
  - a dashboard with a canteen feedback board

What YOU build (look for the `# TODO` markers):
  - Period 1: the menu database (in setup_db.py), then read it in /menu
  - Period 2: the login and logout routes (and the login form)
  - Period 3: save each order, then show each student their own orders

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
# Database helper. Python includes the sqlite3 library, so there is nothing to
# install. get_db() gives you a connection to the file ais.db.
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
    """Create the users and feedback tables and seed them with fake data.

    The menu and orders tables are NOT made here. You build those yourself in
    setup_db.py.
    """
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
# Who is signed in? A cookie called "uid" holds the username. This helper is
# given. You set the cookie yourself when you build the login (Period 2).
# --------------------------------------------------------------------------
def current_user():
    uid = request.cookies.get("uid")
    if not uid:
        return None
    row = get_db().execute(
        "SELECT username, role FROM users WHERE username = ?", (uid,)
    ).fetchone()
    return row


@app.context_processor
def inject_user():
    # Makes `user` available in every template, so the menu bar can show
    # "Sign in" or "Log out" depending on who is signed in.
    return {"user": current_user()}


# --------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------
@app.route("/")
def index():
    if current_user():
        return redirect(url_for("dashboard"))
    return redirect(url_for("menu"))


# ---- Period 2: login and logout -----------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", error=None)

    username = request.form.get("username", "")
    password = request.form.get("password", "")

    # TODO (Period 2): check the sign-in.
    # 1. Build a SQL query that finds the user with this username AND password.
    #    You build the query text by joining pieces together with +, e.g.
    #       "SELECT username, role FROM users WHERE username = '" + username + ...
    # 2. Run it:   row = get_db().execute(query).fetchone()
    # 3. If row is None, show login.html again with an error message.
    # 4. Otherwise set the cookie  uid = row["username"]  and redirect to the
    #    dashboard (see how make_response and set_cookie are used below).
    return render_template("login.html", error="Sign-in is not built yet.")


@app.route("/logout")
def logout():
    # TODO (Period 2): sign the user out.
    # Make a redirect response to the login page, delete the "uid" cookie and
    # the "debug_token" cookie from it (resp.delete_cookie("uid")), and return it.
    return redirect(url_for("login"))


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


# ---- Period 1: the menu --------------------------------------------------
@app.route("/menu")
def menu():
    """Show today's menu, read from the menu table you made in setup_db.py."""
    # TODO (Period 1): read every row of the menu table.
    # Use get_db().execute("SELECT ... FROM menu").fetchall() to get the
    # id, name and price of each item. Then pass the rows to the page.
    items = []
    return render_template("menu.html", menu=items)


# ---- Period 3: orders ----------------------------------------------------
@app.route("/order", methods=["POST"])
def place_order():
    user = current_user()
    if not user:
        return redirect(url_for("login"))

    item_id = request.form.get("item", "")
    item = get_db().execute(
        "SELECT name, price FROM menu WHERE id = ?", (item_id,)
    ).fetchone()
    if item is None:
        return redirect(url_for("menu"))

    # TODO (Period 3): save this order.
    # Insert one row into the `orders` table: the username, the item name, the
    # price and the time. Then call db.commit() so it is really saved.
    # The time:  datetime.now().strftime("%Y-%m-%d %H:%M")
    return redirect(url_for("my_orders"))


@app.route("/my-orders")
def my_orders():
    user = current_user()
    if not user:
        return redirect(url_for("login"))

    # TODO (Period 3): read THIS student's orders.
    # Select item, price and created from `orders` for this username only,
    # newest first. Work out the total price, then pass both to the template.
    # For now we pass an empty list so the page still loads.
    orders = []
    total = 0.0
    return render_template("my_orders.html", orders=orders, total=total)


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


@app.route("/offline")
def offline():
    # The page the service worker shows when there is no internet.
    return render_template("offline.html")


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
