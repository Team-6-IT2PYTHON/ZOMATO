import json, os

def createRestaurantFile(name: str, address: str):
    safeName = "".join(c for c in name if c.isalnum() or c in (' ', '_')).rstrip()
    folder = "restaurants"
    os.makedirs(folder, exist_ok=True)
    filename = os.path.join(folder, f"{safeName}.json")
    if os.path.exists(filename):
        return 0
    data = {
        "name": name,
        "menu": {},
        "address": address,
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def viewMenu(name: str):
    safeName = "".join(c for c in name if c.isalnum() or c in (' ', '_')).rstrip()
    filepath = os.path.join("restaurants", f"{safeName}.json")
    if not os.path.exists(filepath):
        print("Restaurant not found.")
        return

    with open(filepath, "r") as f:
        data = json.load(f)

    menu = data.get("menu", [])

    if not menu:
        print("Menu is empty.")
        return

    print(f"Menu for {data['name']}:")
    for item in menu:
        print(f"- {item['item']}: ₹{item['price']}")

def addMenu(name: str):
    safeName = "".join(c for c in name if c.isalnum() or c in (' ', '_')).rstrip()
    filepath = os.path.join("restaurants", f"{safeName}.json")
    if not os.path.exists(filepath):
        print("Restaurant not found.")
        return

    with open(filepath, "r") as f:
        data = json.load(f)
    if "menu" not in data or not isinstance(data["menu"], list):
        data["menu"] = []

    while True:
        item = input("Enter item name (or type 'done' to finish): ").strip()
        if item.lower() == "done":
            break
        try:
            price = float(input(f"Enter price for {item}: ₹"))
        except ValueError:
            print("Invalid price. Try again.")
            continue
        data["menu"].append({
            "item": item,
            "price": price
        })
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)
    print("Menu updated successfully.")

def deleteMenu(name: str):
    safeName = "".join(c for c in name if c.isalnum() or c in (' ', '_')).rstrip()
    filepath = os.path.join("restaurants", f"{safeName}.json")
    if not os.path.exists(filepath):
        print("Restaurant not found.")
        return
    with open(filepath, "r") as f:
        data = json.load(f)
    menu = data.get("menu", [])
    if not menu:
        print("Menu is empty.")
        return

    print(f"\nMenu for {data['name']}:")
    for i, item in enumerate(menu):
        print(f"{i + 1}. {item['item']} - ₹{item['price']}")
    try:
        choice = int(input("\nEnter the number of the item to delete: "))
        if 1 <= choice <= len(menu):
            removed_item = menu.pop(choice - 1)
            print(f"Deleted item: {removed_item['item']}")
        else:
            print("Invalid choice.")
            return
    except ValueError:
        print("Invalid input.")
        return
    data["menu"] = menu
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)
    print("Menu updated successfully.")

def updateMenu(name: str):
    safeName = "".join(c for c in name if c.isalnum() or c in (' ', '_')).rstrip()
    filepath = os.path.join("restaurants", f"{safeName}.json")
    if not os.path.exists(filepath):
        print("Restaurant not found.")
        return
    with open(filepath, "r") as f:
        data = json.load(f)
    menu = data.get("menu", [])
    if not menu:
        print("Menu is empty.")
        return
    print(f"\nMenu for {data['name']}:")
    for i, item in enumerate(menu):
        print(f"{i + 1}. {item['item']} - ₹{item['price']}")
    try:
        choice = int(input("\nEnter the number of the item to update: "))
        if 1 <= choice <= len(menu):
            newItem = input("Enter new item name: ")
            newPrice = float(input(f"Enter price for {newItem}: ₹"))
            menu[i]["item"] = newItem
            menu[i]["price"] = newPrice
    except ValueError:
        print("Invalid choice.")
        return
    data["menu"] = menu
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)
    print("Menu updated successfully.")
