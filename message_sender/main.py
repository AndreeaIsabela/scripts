import argparse
from dotenv import load_dotenv
import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

load_dotenv()

def send_message(to: str, message: str, whatsapp: bool = False)-> None:
  client = Client(os.environ.get('SID'), os.environ.get('AUTH_TOKEN'))
  result = client.messages.create(
    from_= f'{os.environ.get('FROM_WS') if whatsapp else os.environ.get('FROM')}',
    body= message,
    to= f'{"whatsapp:" if whatsapp else ""}{to}'
  )
  print('Done!')

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Send a message using twilio')
  parser.add_argument('--to', required=True, help='Recipient phone number')
  parser.add_argument('--message', required=True, help='message')
  parser.add_argument('--whatsapp', action='store_true', help='Send via WhatsApp')
  args = parser.parse_args()

  try:
    send_message(args.to, args.message, args.whatsapp)
  except (ValueError, FileNotFoundError, KeyError, TwilioRestException) as e:
    raise SystemExit(f'Error: {e}')
