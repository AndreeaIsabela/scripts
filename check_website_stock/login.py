import json
import os
import sys
from contextlib import contextmanager
from dotenv import load_dotenv
from seleniumbase import SB

load_dotenv()

# Selectors, update these if the site's HTML changes
SELECTORS = {
  "username": "#username",
  "password": "#password",
  "submit": "button[type='submit']",
}

LOGGED_IN_SELECTOR = os.getenv("LOGGED_IN_SELECTOR", 'a[href*="edit-account"]')

COOKIES_FILE = os.path.join(os.path.dirname(__file__), "cookies.json")


def _validate_env():
  missing = [var for var in ("SHOP_URL", "SHOP_EMAIL", "SHOP_PASSWORD") if not os.getenv(var)]
  if missing:
    sys.exit(f"Missing required env vars: {', '.join(missing)}")


def _try_cookie_login(sb):
  if not os.path.exists(COOKIES_FILE):
    return False
  with open(COOKIES_FILE) as f:
    cookies = json.load(f)
  sb.uc_open_with_reconnect(os.getenv("SHOP_URL"), reconnect_time=4)
  for cookie in cookies:
    cookie.pop("sameSite", None)
    try:
      sb.add_cookie(cookie)
    except Exception:
      pass
  sb.open(os.getenv("SHOP_URL"))
  sb.wait_for_ready_state_complete()
  return sb.is_element_visible(LOGGED_IN_SELECTOR)


def login(sb):
  if _try_cookie_login(sb):
    print("Login successful (session restored from cookies).")
    return

  print("No valid session cookies found, attempting form login...")
  sb.uc_open_with_reconnect(os.getenv("SHOP_URL"), reconnect_time=4)
  sb.type(SELECTORS["username"], os.getenv("SHOP_EMAIL"))
  sb.type(SELECTORS["password"], os.getenv("SHOP_PASSWORD"))
  # Handle the embedded Cloudflare Turnstile widget
  sb.uc_gui_click_captcha()
  sb.execute_script("document.querySelector(\"button[type='submit']\").click()")
  sb.wait_for_ready_state_complete()
  if not sb.is_element_visible(LOGGED_IN_SELECTOR):
    sb.open(os.getenv("SHOP_URL"))
    sb.wait_for_ready_state_complete()
  if not sb.is_element_visible(LOGGED_IN_SELECTOR):
    sys.exit(
      "Login failed — Cloudflare is blocking automated form submission.\n"
      "Run 'python get_cookies.py' to save a fresh session manually."
    )
  print("Login successful.")


@contextmanager
def logged_in_session():
  _validate_env()
  headless = os.getenv("HEADLESS", "false").lower() == "true"
  with SB(uc=True, headless=headless) as sb:
    login(sb)
    yield sb


if __name__ == "__main__":
  with logged_in_session() as sb:
    pass
