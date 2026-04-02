import os
import importlib.util
from dotenv import load_dotenv
from login import logged_in_session
from check_product_availability import check_product_availability

load_dotenv()

_sender_path = os.path.join(os.path.dirname(__file__), "..", "message_sender", "main.py")
_spec = importlib.util.spec_from_file_location("message_sender", _sender_path)
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)
send_message = _module.send_message


def _get_product_urls():
  raw = os.getenv("PRODUCT_URLS", "")
  return [url.strip() for url in raw.split(",") if url.strip()]


if __name__ == "__main__":
  product_urls = _get_product_urls()

  with logged_in_session() as sb:
    results = check_product_availability(sb, product_urls)

    to = os.getenv("TO")

    for item in results:
      if item["in_stock"]:
        message = f"In stock: {item['name']}\n{item['url']}"
        send_message(to, message)
