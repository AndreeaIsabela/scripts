import smtplib
import sys
import json
import os
from email.message import EmailMessage
from string import Template
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def parse_substitutions(raw: list) -> dict:
    if not raw:
        return {}
    if len(raw) == 1:
        try:
          return json.loads(raw[0])
        except (json.JSONDecodeError, ValueError):
          pass
    result = {}
    for item in raw:
        if '=' not in item:
          raise ValueError(f'Invalid substitution: "{item}". Use key=value pairs or a single JSON string.')
        k, _, v = item.partition('=')
        result[k.strip()] = v.strip()
    return result


def send_email(to: str, subject: str, template: str, substitutions: dict) -> None:
    smtp_host = os.environ.get('SMTP_HOST')
    smtp_port = int(os.environ.get('SMTP_PORT', 587))
    smtp_user = os.environ.get('SMTP_USER')
    smtp_password = os.environ.get('SMTP_PASSWORD')
    sender_name = os.environ.get('SENDER_NAME', smtp_user)

    for name, value in [('SMTP_HOST', smtp_host), ('SMTP_USER', smtp_user), ('SMTP_PASSWORD', smtp_password)]:
      if not value:
        raise ValueError(f'Missing required environment variable: {name}')

    template_path = Path(__file__).parent / 'templates' / template
    if not template_path.exists():
      raise FileNotFoundError(f'Template not found: {template_path}')

    html = Template(template_path.read_text()).substitute(substitutions)

    msg = EmailMessage()
    msg['from'] = sender_name
    msg['to'] = to
    msg['subject'] = subject
    msg.set_content(html, 'html')

    with smtplib.SMTP(host=smtp_host, port=smtp_port) as smtp:
      smtp.ehlo()
      smtp.starttls()
      smtp.login(smtp_user, smtp_password)
      smtp.send_message(msg)

    print(f'Email sent to {to}')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Send an HTML email using a template.')
    parser.add_argument('--to', required=True, help='Recipient email address')
    parser.add_argument('--subject', required=True, help='Email subject line')
    parser.add_argument('--template', required=True, help='Template filename (e.g. welcome.html)')
    parser.add_argument('--sub', nargs='*', default=[], metavar='KEY=VALUE', help='Template substitutions as key=value pairs or a single JSON string')
    args = parser.parse_args()

    try:
      substitutions = parse_substitutions(args.sub)
      send_email(args.to, args.subject, args.template, substitutions)
    except (ValueError, FileNotFoundError, KeyError) as e:
      print(f'Error: {e}', file=sys.stderr)
      sys.exit(1)
