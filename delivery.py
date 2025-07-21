import json
import os

PARTNERS_FILE = "partners.json"

def loadPartners():
    if not os.path.exists(PARTNERS_FILE) or os.path.getsize(PARTNERS_FILE) == 0:
        return []
    with open(PARTNERS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []
        
def saveUsers(partners):
    with open(PARTNERS_FILE, "w")as f:
        json.dump(partners, f, indent=4)


def register():
    partners = loadPartners()
    username = input("Enter username: ")
    if any(p['username'] == username for p in partners):
        print("Username already exists!")
        return

    password = input("Enter password: ")
    address = input("Enter address: ")

    partners.append({
        "username": username,
        "password": password,
        "address": address
    })

    saveUsers(partners)
    print("Registered successfully!")

def login():
    partners = loadPartners()
    username = input("Enter username: ")
    password = input("Enter password: ")

    for partner in partners:
        if partner["username"] == username and partner["password"] == password:
            print(f"Welcome back, {username}!")
            return partner
    print("Invalid username or password!")
    return None

def createPartnerFile(name: str, address: str):
    safeName = "".join(c for c in name if c.isalnum() or c in (' ', '_')).rstrip()
    folder = "partners"
    os.makedirs(folder, exist_ok=True)
    filename = os.path.join(folder, f"{safeName}.json")
    if os.path.exists(filename):
        return 0
    data = {
        "name": name,
        "earnings": {},
        "address": address,
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


