#authentication.py
import hashlib
from database_connect import user_collection as userc


def hashing(password):
    passw = hashlib.sha256(password.encode()).hexdigest()
    return passw

def register_user(username, password, role, student_id = None):
    if userc.find_one({"username": username}):
      return False, "username already exists...."
    
    dic = {
        
        "username" : username,
        "password": hashing(password),
        "role": role
    }
    if student_id:
       dic["student_id"] = student_id

    userc.insert_one(dic)
    return True, "User created successfully"
    


def login():
    print("---------Login---------\n")
    username = input("Enter Username: ").strip()
    password = input("Enter Password: ").strip()

    user = userc.find_one({"username": username})

    if not user:
        print("Username not found!")
        return None

    if user["password"] != hashing(password):
        print("Password does not match!")
        return None

    return user

def change_password(user: dict):
    if not user or "username" not in user:
        print("Invalid user. Please log in again.")
        return False, "invalid user"

    old_password = input("Enter current password: ").strip()
    new_password = input("Enter new password: ").strip()
    confirm_password = input("Re-enter new password: ").strip()

    # Check old password
    if hashing(old_password) != user.get("password"):
        print("Current password is incorrect!")
        return False, "old password incorrect"

    # Match check
    if new_password != confirm_password:
        print("New password and confirm password do not match!")
        return False, "confirm mismatch"

    if not new_password:
        print("Password cannot be empty.")
        return False, "empty password"

    # Update password for the specific user
    userc.update_one(
        {"username": user["username"]},
        {"$set": {"password": hashing(new_password)}}
    )
    print("Password changed successfully...")


def create_new_staff_user():
    print("\n=== CREATE STAFF USER ===")
    username = input("Staff Username: ").strip()
    password = input("Staff Password: ").strip()

    msg = register_user(username, password, role="staff")
    print(msg)