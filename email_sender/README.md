# Email Sender

A simple CLI script to send HTML emails via SMTP using customisable templates.

## Prerequisites

- Python 3.10+
- `python-dotenv`

```bash
pip install python-dotenv
```

## Gmail App Password

Gmail requires an **App Password** instead of your regular account password when using SMTP. To generate one:

1. Go to your Google Account at [myaccount.google.com](https://myaccount.google.com)
2. Select **Security** in the left sidebar
3. Make sure **2-Step Verification** is turned on
4. Search for **"App passwords"**
5. Click **App passwords**, then choose **"Other (Custom name)"** 
6. Enter a name and click **Generate**
7. Copy the password and paste it as `SMTP_PASSWORD` in your `.env` file

## Environment Variables

| Variable | Description | Example |
|---|---|---|
| `SMTP_HOST` | SMTP server hostname | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP server port | `587` |
| `SMTP_USER` | Your email address (used to authenticate) | `you@gmail.com` |
| `SMTP_PASSWORD` | Your app password (not your account password) | `abcd efgh ijkl mnop` |
| `SENDER_NAME` | Display name shown in the From field | `Your Name` |

## Usage

```bash
python main.py --to RECIPIENT --subject "SUBJECT" --template TEMPLATE [--sub KEY=VALUE ...]
```

Substitutions can be passed as `key=value` pairs or as a single JSON string.

## CLI Arguments

| Argument | Required | Description |
|---|---|---|
| `--to` | Yes | Recipient email address |
| `--subject` | Yes | Email subject line |
| `--template` | Yes | Template filename from the `templates/` folder |
| `--sub` | No | Template variable substitutions (key=value or JSON) |

## Examples

**Welcome email:**

```bash
python main.py \
  --to isabela@example.com \
  --subject "Welcome to Isabela's emails!" \
  --template welcome.html \
  --sub name=Isabela app_name=Isabela's emails login_url=https://app.example.com/login
```

**Newsletter:**

```bash
python main.py \
  --to isabela@example.com \
  --subject "The Example — March 2026" \
  --template newsletter.html \
  --sub '{"name":"Isabela","month":"March 2026","article1_title":"Why Python Still Wins","article1_summary":"A deep look at why Python remains the go-to language for data and scripting in 2026.","article2_title":"Docker in 5 Minutes","article2_summary":"Everything you need to containerise your first app, from zero to running.","unsubscribe_url":"https://example.com/unsubscribe"}'
```

**Promotional email:**

```bash
python main.py \
  --to isabela@example.com \
  --subject "Your exclusive 30% off — today only" \
  --template promo.html \
  --sub name=Isabela product_name="Example" discount_pct=30 promo_code=SAVE30 original_price=99 sale_price=69 offer_expiry="April 1, 2026" cta_url=https://example.com/buy
```

## Templates

All templates live in the `templates/` folder and use [Python's string.Template](https://docs.python.org/3/library/string.html#template-strings) syntax (`$varname` or `${varname}`).

### `welcome.html`

| Variable | Description | Example |
|---|---|---|
| `$name` | Recipient's first name | `Isabela` |
| `$app_name` | Product or app name | `Isabela's emails` |
| `$login_url` | URL for the "Get Started" button | `https://app.example.com/login` |

### `newsletter.html`

| Variable | Description | Example |
|---|---|---|
| `$name` | Recipient's first name | `Isabela` |
| `$month` | Issue month/date label | `March 2026` |
| `$article1_title` | First article headline | `Why Python Still Wins` |
| `$article1_summary` | First article summary text | `A deep look at...` |
| `$article2_title` | Second article headline | `Docker in 5 Minutes` |
| `$article2_summary` | Second article summary text | `Everything you need...` |
| `$unsubscribe_url` | Unsubscribe link in footer | `https://example.com/unsubscribe` |

### `promo.html`

| Variable | Description | Example |
|---|---|---|
| `$name` | Recipient's first name | `Isabela` |
| `$product_name` | Product being promoted | `Example` |
| `$discount_pct` | Discount percentage (number only) | `30` |
| `$promo_code` | Coupon code to display | `SAVE30` |
| `$original_price` | Original price, no currency symbol | `99` |
| `$sale_price` | Sale price, no currency symbol | `69` |
| `$offer_expiry` | Offer expiry date | `April 1, 2026` |
| `$cta_url` | URL for the "Claim Your Discount" button | `https://example.com/buy` |

