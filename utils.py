
#utils.py
from datetime import datetime

def input_non_empty_name(promot):
    while True:
        name = input(promot).strip()
        if name.replace(" ", "").isalpha():
            return name
        print("Name should contain only alphabets. Please enter a valid name.")


def input_non_empty(prompt):
    while True:
        val = input(prompt).strip()
        if val:
            return val
        print("This field cannot be empty.")

def input_int(prompt, min_value=None, max_value=None):
    while True:
        try:
            v = int(input(prompt))
            if min_value is not None and v < min_value:
                print(f"Value must be >= {min_value}")
                continue
            if max_value is not None and v > max_value:
                print(f"Value must be <= {max_value}")
                continue
            return v
        except:
            print("Enter a valid integer.")

def input_phone_10_digits(prompt):
    while True:
        value = input(prompt).strip()
        if value.isdigit() and len(value) == 10:
            return value
        print("Phone number must be exactly 10 digits and numbers only.")

def validate_date(prompt):
    while True:
        date_str = input(prompt).strip()
        try:
            return datetime.strptime(date_str, "%d-%m-%Y")
        except ValueError:
            print("Invalid date format. Please use DD-MM-YYYY.")

def pass_or_fail(marks, passing=33):
    return "PASS" if marks >= passing else "FAIL"
