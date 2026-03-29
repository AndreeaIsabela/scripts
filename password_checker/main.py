import hashlib
import requests
import sys

def get_matches(head: str)-> requests.Response:
  try:
    url = 'https://api.pwnedpasswords.com/range/' + head
    response = requests.get(url, timeout=10)
    if(response.status_code != 200):
      raise RuntimeError(f'Error fetching: {response.status_code}, check the api and try again')
    return response
  except requests.exceptions.RequestException as error:
    raise RuntimeError(f'Network error: {error}') from error

def count_leaks(pass_hashes: str, hash_to_check: str) -> int:
  pass_hashes = (line.split(':') for line in pass_hashes.text.splitlines())
  for hash, count in pass_hashes:
    if hash == hash_to_check:
      return int(count)
  return 0

def check_password(password: str)-> int:
  sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
  head5, tail = sha1password[:5], sha1password[5:]
  response = get_matches(head5)
  return count_leaks(response, tail)

if __name__ == '__main__':
  if len(sys.argv) != 2:
    print('Usage: python main.py <example_passwords.txt>')
    sys.exit(1)
  with open(sys.argv[1], 'r') as f:
    passwords = [line.strip() for line in f if line.strip()]
  for password in passwords:
    count = check_password(password)
    if count:
      print(f'{password} : {count} times')
    else:
      print(f'{password} : 0, was NOT found')
  print('Done!')
