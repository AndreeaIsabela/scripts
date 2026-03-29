# Password Checker

Check whether passwords have been exposed in known data breaches using the [Have I Been Pwned](https://haveibeenpwned.com/API/v3#PwnedPasswords) Pwned Passwords API.

Passwords are never sent in plain text — only the first 5 characters of the SHA-1 hash are transmitted (k-anonymity model).

## Prerequisites

- **Python 3.10+**
- **requests** library

```bash
pip install requests
```

## Usage

```bash
python main.py <passwords_file.txt>
```

Each line in the file is treated as one password. Blank lines are ignored.

An `example_passwords.txt` file is included for reference.

## Example

```bash
python main.py example_passwords.txt
```

```
password : 10284813 times
password1 : 2441854 times
superSecretPassword : 0, was NOT found
bestPassword : 0, was NOT found
Done!
```
