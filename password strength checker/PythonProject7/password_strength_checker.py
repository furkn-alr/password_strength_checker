import string
import random
from datetime import datetime

def is_common_password(user_password, filename='common_passwords.txt'):
    with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            if user_password.strip().lower() == line.strip().lower():
                return True
    return False


def generate_strong_password(length = 12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def log_password_attempt(password, valid, reasons):
    with open("logs.txt", "a", encoding="utf-8") as log:
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        masked = '*' * len(password)
        status = "Valid" if valid else "Invalid"
        reason_text = " | ".join(reasons) if reasons else "None"
        log.write(f"[{time}] {masked} → {status} → {reason_text}\n")


def password_strength_checker(password):
    reasons = []
    # checks if the password is common
    if is_common_password(password):
        reasons.append("Common password")
        log_password_attempt(password, False, reasons)
        print("This password is one of the most common to guess, try a stronger password.")
        return False

    length = len(password) >= 8            #conditions
    number = any(char.isdigit()for char in password)
    lowercase_letter = any(char.islower()for char in password)
    uppercase_letter = any(char.isupper()for char in password)
    punctuation = any(char in string.punctuation for char in password)

               #conditions are getting checked
    if all([length, number, lowercase_letter, uppercase_letter, punctuation]):
        return True
    else:
        print("Password does not include: ")
    if not length: reasons.append("Password is too short")

    if not number: reasons.append("Missing number")

    if not lowercase_letter: reasons.append("Missing lowercase letter")

    if not uppercase_letter: reasons.append("Missing uppercase letter")

    if not punctuation: reasons.append("Missing punctuation")

    valid = all([length, number, lowercase_letter, uppercase_letter, punctuation])

    log_password_attempt(password, True, [])

    if valid:
        return True
    else:
        print("Password does not include: ")
        for r in reasons:
            print(f"- {r}")
        return False

while True:            #creating a loop until the password is valid
    password = input("Please enter a password: ")
    if password_strength_checker(password):
        print("Password is strong and valid.")
        break
    else:
        print("Try again.\n")

    suggest = input("Would you like a suggestion? (y/n): ").lower()
    if suggest == "y":
        while True:
            suggestion = generate_strong_password()
            print(f" Suggested: {suggestion}")
            again = input("Would you like another suggestion? (y/n): ").lower()
            if again != "y":
                break

