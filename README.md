# AIS Canteen Pre-order (starter)

A small Flask Progressive Web App you build over three lessons, then test in
Lesson 4. Students pre-order their canteen lunch; the app saves each order.

## Run it

**On your laptop**
```
pip install -r requirements.txt
python main.py
```
Open http://127.0.0.1:5000

**In a GitHub Codespace**
Open the repo in a Codespace. It installs Flask automatically, then run
`python main.py` and click the forwarded port 5000.

Sign in with a seeded account, for example **aisha / sunflower22**.

## What is already built

- Sign in and sign out
- A dashboard with a canteen feedback board
- A `/menu` route that passes today's menu to the page

## What you build

Look for `# TODO` in the code. Each one belongs to a lesson.

- **Period 1 - Menu page.** In `templates/menu.html`, loop over the `menu`
  list so every item shows with an **Order** button (only one is hard-coded now).
- **Period 2 - Save the order.** In `main.py`, create the `orders` table in
  `init_db()`, then finish the `/order` route so it saves the chosen item with
  a **parameterised** `INSERT`.
- **Period 3 - My orders.** Finish the `/my-orders` route and
  `templates/my_orders.html` so each student sees their own orders and a total.

## Files

| File | What it is |
| --- | --- |
| `main.py` | The Flask app: routes, the menu, the database |
| `templates/` | The pages (`base`, `login`, `dashboard`, `menu`, `my_orders`) |
| `static/` | Stylesheet, icon, manifest, service worker, `app.js` |
| `requirements.txt` | Flask |

Training sandbox: fake data only, debug off. Only ever test your own copy.
