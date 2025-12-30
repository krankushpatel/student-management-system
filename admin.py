from authentication import register_user

print("\n=== CREATE NEW ADMIN ===")
username = input("Staff Username: ").strip()
password = input("Staff Password: ").strip()

success, msg = register_user(username, password, role="admin")
print(msg)