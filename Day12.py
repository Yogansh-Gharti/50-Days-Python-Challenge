import hashlib
import requests
import secrets
import string
import pyperclip
import math

SYMBOLS = "!@#$%^&*()_+-=[]{}<>?/"

def calculate_entropy(password):
    pool = 0

    if any(c.islower() for c in password):
        pool += 26

    if any(c.isupper() for c in password):
        pool += 26

    if any(c.isdigit() for c in password):
        pool += 10

    if any(c in SYMBOLS for c in password):
        pool += len(SYMBOLS)

    if pool == 0:
        return 0

    return round(len(password) * math.log2(pool), 2)


def strength(entropy):

    if entropy < 40:
        return "Weak"

    elif entropy < 60:
        return "Medium"

    elif entropy < 80:
        return "Strong"

    return "Very Strong"


def breach_check(password):

    sha1 = hashlib.sha1(
        password.encode()
    ).hexdigest().upper()

    prefix = sha1[:5]

    suffix = sha1[5:]

    url = (
        f"https://api.pwnedpasswords.com/range/{prefix}"
    )

    response = requests.get(url)

    if response.status_code != 200:
        return "API Error"

    for line in response.text.splitlines():

        hash_suffix, count = line.split(":")

        if hash_suffix == suffix:
            return f"⚠ Leaked {count} times"

    return "✅ Not Found"


def generate_password(length=16):

    chars = (
        string.ascii_letters +
        string.digits +
        SYMBOLS
    )

    password = "".join(
        secrets.choice(chars)
        for _ in range(length)
    )

    pyperclip.copy(password)

    return password


while True:

    print("\n===== PASSWORD SECURITY SUITE =====")

    print("1. Analyze Password")
    print("2. Generate Secure Password")
    print("3. Exit")

    choice = input("Choice: ")

    if choice == "1":

        password = input("Enter Password: ")

        entropy = calculate_entropy(password)

        print(
            f"\nEntropy : {entropy} bits"
        )

        print(
            f"Strength: {strength(entropy)}"
        )

        print(
            breach_check(password)
        )

    elif choice == "2":

        password = generate_password()

        print(
            "\nGenerated Password:"
        )

        print(password)

        print(
            "\n✅ Copied to Clipboard"
        )

        with open(
            "password_history.txt",
            "a"
        ) as file:

            file.write(password + "\n")

    elif choice == "3":
        break

    else:
        print("Invalid Choice")
