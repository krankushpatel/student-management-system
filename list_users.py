
from database_connect import user_collection

print("Listing all users:")
for user in user_collection.find():
    print(f"Username: {user.get('username')}, Role: {user.get('role')}")
