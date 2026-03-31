# Message Sender

A simple CLI script to send SMS or WhatsApp messages via Twilio.

## Prerequisites

- Python 3.10+
- `twilio`
- `python-dotenv`

```bash
pip install twilio python-dotenv
```

## Twilio Setup

1. Sign up at [twilio.com](https://www.twilio.com) and get your **Account SID** and **Auth Token** from the Twilio Console dashboard
2. Get a Twilio phone number (for SMS) and/or enable WhatsApp Sandbox (for WhatsApp)
3. Add the credentials to your `.env` file

## Environment Variables

| Variable | Description | Example |
|---|---|---|
| `SID` | Twilio Account SID | `ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |
| `AUTH_TOKEN` | Twilio Auth Token | `your_auth_token_here` |
| `FROM` | Twilio phone number for SMS | `+14155552671` |
| `FROM_WS` | Twilio WhatsApp sender number | `+14155238886` |

## Usage

```bash
python main.py --to RECIPIENT --message "MESSAGE" [--whatsapp]
```

## CLI Arguments

| Argument | Required | Description |
|---|---|---|
| `--to` | Yes | Recipient phone number in E.164 format |
| `--message` | Yes | Message body to send |
| `--whatsapp` | No | Send via WhatsApp instead of SMS |

## Examples

**Send an SMS:**

```bash
python main.py --to +14155552671 --message "Hello!"
```

**Send a WhatsApp message:**

```bash
python main.py --to +14155552671 --message "Hello via WhatsApp!" --whatsapp
```
