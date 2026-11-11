"""
Template for local teacher secrets.

To run with known, stable flags on your own laptop:
    cp ctf_config.example.py ctf_config.py
then edit the values. ctf_config.py is gitignored, so it is never committed.

In GitHub Codespaces, set these names as repo secrets instead (Settings →
Secrets and variables → Codespaces). Environment variables override this file,
so every student's Codespace shares the flags you choose.

If you set nothing, the app still runs: it generates random flags on startup.
Attacks still work; you just will not know the exact flag strings in advance.
"""

FLAG_SQLI = "FLAG{change-me-flag-1}"
FLAG_XSS = "FLAG{change-me-flag-2}"
FLAG_SECRET = "FLAG{change-me-flag-3}"
ADMIN_API_KEY = "change-me-admin-key"
ADMIN_PASSWORD = "change-me-admin-password"
