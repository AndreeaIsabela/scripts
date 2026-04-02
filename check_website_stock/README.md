# Check Website Stock

Logs into a shop account, checks a list of product pages for stock availability, and sends an SMS/WhatsApp notification via Twilio when an item is in stock.

Uses [SeleniumBase](https://seleniumbase.io/) with undetected Chrome to bypass bot detection and captchas.

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
| `HEADLESS` | `true` to run without opening a browser window (default: `false`) |
| `PRODUCT_URLS` | Comma-separated list of product page URLs to check |
| `SID` | Twilio account SID |
| `AUTH_TOKEN` | Twilio auth token |
| `FROM` | Twilio sender number (SMS) |
| `FROM_WS` | Twilio sender number (WhatsApp) |
| `TO` | Recipient phone number |

## Usage

Run the full stock check and notification flow:

```bash
python main.py
```

To test login only:

```bash
python login.py
```

## How it works

1. `login.py` — opens the shop login page and authenticates using SeleniumBase
2. `check_product_availability.py` — visits each URL in `PRODUCT_URLS` and checks for in-stock/out-of-stock selectors
3. `main.py` — orchestrates both, then calls `message_sender` to send a notification for each in-stock item

## Configuration

If the site's HTML changes, update the selectors at the top of each file:

**`login.py`**
```python
SELECTORS = {
  "username": "#username",
  "password": "#password",
  "submit": "button[type='submit']",
}
```

**`check_product_availability.py`**
```python
PRODUCT_NAME_SELECTOR = "h1.product_title.entry-title"
IN_STOCK_SELECTOR = ".single_add_to_cart_button.button:not(.disabled):not([disabled])"
OUT_OF_STOCK_SELECTOR = "p.stock.out-of-stock"
```
