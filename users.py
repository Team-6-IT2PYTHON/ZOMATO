import json
import os

USER_FILE = "users.json"


def load_users():
    if not os.path.exists(USER_FILE) or os.path.getsize(USER_FILE) == 0:
        return []
    with open(USER_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

def register():
    users = load_users()
    username = input("Enter username: ")
    if any(u['username'] == username for u in users):
        print("Username already exists!")
        return

    password = input("Enter password: ")
    address = input("Enter address: ")

    users.append({
        "username": username,
        "password": password,
        "address": address
    })

    save_users(users)
    print("Registered successfully!")

def login():
    users = load_users()
    username = input("Enter username: ")
    password = input("Enter password: ")

    for user in users:
        if user["username"] == username and user["password"] == password:
            print(f"Welcome back, {username}!")
            return user
    print("Invalid username or password!")
    return None
