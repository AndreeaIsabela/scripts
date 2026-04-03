"""
Run this once (or whenever your session expires) to save a logged-in session.

    python get_cookies.py

A browser window opens. Log in normally — the script saves your cookies
automatically once it detects you're logged in, then closes.
"""
import json
import os
from dotenv import load_dotenv
from seleniumbase import SB

load_dotenv()

SHOP_URL = os.getenv("SHOP_URL")
LOGGED_IN_SELECTOR = os.getenv("LOGGED_IN_SELECTOR", 'a[href*="edit-account"]')
COOKIES_FILE = os.path.join(os.path.dirname(__file__), "cookies.json")

print(f"Opening {SHOP_URL}")
print("Log in manually in the browser. The script will save cookies and close automatically.\n")

with SB(uc=True, headless=False) as sb:
    sb.open(SHOP_URL)
    print("Waiting up to 2 minutes for you to complete login...")
    sb.wait_for_element_visible(LOGGED_IN_SELECTOR, timeout=120)
    cookies = sb.get_cookies()

with open(COOKIES_FILE, "w") as f:
    json.dump(cookies, f, indent=2)

print(f"Saved {len(cookies)} cookies to {COOKIES_FILE}")
print("You can now run main.py")
