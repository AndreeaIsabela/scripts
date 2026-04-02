import os
from login import login

# Selectors, update these if the site's HTML changes
PRODUCT_NAME_SELECTOR = "h1.product_title.entry-title"
IN_STOCK_SELECTOR = ".single_add_to_cart_button.button:not(.disabled):not([disabled])"
OUT_OF_STOCK_SELECTOR = "p.stock.out-of-stock"
def _ensure_logged_in(sb, url):
  if sb.is_text_visible("register and login to shop"):
    print("Session lost retry log in...")
    login(sb)
    sb.open(url)


def check_product_availability(sb, product_urls):
  """
  Checks stock availability for a list of product URLs.

  Args:
    sb: An active SeleniumBase session (already logged in).
    product_urls: List of product page URLs to check.

  Returns:
    List of dicts with keys: url, name, in_stock (True/False/None).
  """
  results = []

  for url in product_urls:
    sb.open(url)
    _ensure_logged_in(sb, url)

    name = url
    if sb.is_element_visible(PRODUCT_NAME_SELECTOR):
      name = sb.get_text(PRODUCT_NAME_SELECTOR)

    if sb.is_element_visible(IN_STOCK_SELECTOR):
      in_stock = True
      print(f"IN STOCK:     {name} — {url}")
    elif sb.is_element_visible(OUT_OF_STOCK_SELECTOR):
      in_stock = False
      print(f"OUT OF STOCK: {name} — {url}")
    else:
      in_stock = None
      print(f"UNKNOWN:      {name} — {url}")

    results.append({"url": url, "name": name, "in_stock": in_stock})

  return results
