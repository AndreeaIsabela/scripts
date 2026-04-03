# Check Website Stock

Logs into a shop account, checks a list of product pages for stock availability, and sends a WhatsApp notification via Twilio when an item is in stock.

Uses [SeleniumBase](https://seleniumbase.io/) with undetected Chrome to bypass bot detection.

## Setup

```bash
pip install seleniumbase python-dotenv twilio
```

Copy `.env_example` to `.env` and fill in your credentials:

```bash
cp .env_example .env
```

### Environment variables

| Variable | Description |
|---|---|
| `SHOP_URL` | Login page URL |
| `SHOP_EMAIL` | Account email |
| `SHOP_PASSWORD` | Account password |
| `LOGGED_IN_SELECTOR` | CSS selector for an element that is only present when logged in (used to verify authentication) |
| `HEADLESS` | `true` to run without opening a browser window (default: `false`) |
| `PRODUCT_URLS` | Comma-separated list of product page URLs to check |
| `SID` | Twilio account SID |
| `AUTH_TOKEN` | Twilio auth token |
| `FROM` | Twilio sender number (SMS) |
| `FROM_WS` | Twilio sender number (WhatsApp) |
| `TO` | Recipient phone number |

## First-time session setup

The shop login page uses a Cloudflare Turnstile CAPTCHA that blocks automated form submission. To work around this, the script uses saved session cookies instead of filling the login form.

Before running the stock checker for the first time, save your session:

```bash
python get_cookies.py
```

A browser window opens. Log in normally — once the script detects you are logged in it saves the cookies to `cookies.json` and closes automatically.

**You will need to re-run `get_cookies.py` when your session expires** (roughly every 14 days, or sooner if you did not check "Remember me").

> `cookies.json` contains your session tokens — do not commit it to version control.

## Usage

Run the full stock check and notification flow:

```bash
python main.py
```

This will:
1. Restore your session from `cookies.json`
2. Visit each URL in `PRODUCT_URLS` and check stock status
3. Send a WhatsApp message via Twilio for every in-stock item

To refresh your session manually:

```bash
python get_cookies.py
```

## How it works

1. `get_cookies.py` — opens a browser for manual login and saves the session cookies to `cookies.json`
2. `login.py` — loads cookies from `cookies.json` and verifies the session is active; falls back to form-based login if cookies are missing
3. `check_product_availability.py` — visits each URL in `PRODUCT_URLS` and checks for in-stock/out-of-stock selectors
4. `main.py` — orchestrates all of the above, then sends a WhatsApp notification for each in-stock item

## Configuration

If the site's HTML changes, update the selectors in `.env` and at the top of each file:

**`.env`**
```
LOGGED_IN_SELECTOR=a[href*="edit-account"]
```

**`check_product_availability.py`**
```python
PRODUCT_NAME_SELECTOR = "h1.product_title.entry-title"
IN_STOCK_SELECTOR = ".single_add_to_cart_button.button:not(.disabled):not([disabled])"
OUT_OF_STOCK_SELECTOR = "p.stock.out-of-stock"
```
