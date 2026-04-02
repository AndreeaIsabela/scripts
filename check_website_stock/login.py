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


def _validate_env():
  missing = [var for var in ("SHOP_URL", "SHOP_EMAIL", "SHOP_PASSWORD") if not os.getenv(var)]
  if missing:
    sys.exit(f"Missing required env vars: {', '.join(missing)}")


def login(sb):
  sb.open(os.getenv("SHOP_URL"))
  sb.type(SELECTORS["username"], os.getenv("SHOP_EMAIL"))
  sb.type(SELECTORS["password"], os.getenv("SHOP_PASSWORD"))
  sb.click(SELECTORS["submit"])
  sb.wait_for_ready_state_complete()
  if "/products" not in sb.get_current_url():
    raise RuntimeError(f"Login failed — unexpected URL after submit: {sb.get_current_url()}")
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
    pass  # session closes here
