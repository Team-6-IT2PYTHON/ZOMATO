import json
import os

PARTNERS_FILE = "partners.json"
ORDERS_FILE = "orders.json"

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

def loadOrders():
    if not os.path.exists(ORDERS_FILE) or os.path.getsize(ORDERS_FILE) == 0:
        return []
    with open(ORDERS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def saveOrders(orders):
    with open(ORDERS_FILE, "w") as f:
        json.dump(orders, f, indent=4)

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

def viewAvailableOrders():
    orders = loadOrders()

    if not orders:
        print("✅ No orders available for delivery.")
        return None

    print("\n🚚 Available Orders for Delivery:\n" + "-" * 50)

    for index, order in enumerate(orders, start=1):
        user = order.get("user", "Guest")
        restaurant = order.get("restaurant", "Unknown Restaurant")
        restaurant_address = order.get("restaurant_address", "Unknown Address")

        print(f"\nOrder {index}:")
        print(f"Customer: {user}")
        print(f"Restaurant: {restaurant} ({restaurant_address})")
        print("Items:")

        total = 0
        for item in order["items"]:
            subtotal = item["price"] * item["quantity"]
            total += subtotal
            print(f" - {item['item']} x {item['quantity']} = ₹{subtotal}")

        print(f"Total: ₹{total}")
        print("-" * 50)

    try:
        choice = input("\nEnter the order number you want to deliver (or press Enter to go back): ").strip()
        if not choice:
            return None

        order_index = int(choice) - 1
        if 0 <= order_index < len(orders):
            selected_order = orders.pop(order_index)
            saveOrders(orders)  # Save updated orders list
            return selected_order, choice
        else:
            print("❌ Invalid order number.")
            return None
    except ValueError:
        print("❌ Invalid input. Please enter a valid number.")
        return None

def completeDelivery(partner_name: str, order_data: tuple):
    if not order_data:
        return

    order, order_number = order_data

    print(f"\n🚚 You have picked up Order #{order_number}")
    print(f"Delivering to: {order.get('user', 'Guest')}")

    confirm = input("\nHave you completed the delivery? (yes/no): ").strip().lower()
    if confirm == "yes":
        # Calculate earnings (assume 10% of order total)
        total = sum(item["price"] * item["quantity"] for item in order["items"])
        earnings = round(total * 0.1, 2)

        # Update partner earnings
        updatePartnerEarnings(partner_name, earnings, order.get("restaurant", "Unknown"))

        print(f"✅ Delivery completed!")
        print(f"💰 You earned ₹{earnings} from this delivery!")
    else:
        # Put the order back in the queue
        orders = loadOrders()
        orders.append(order)
        saveOrders(orders)
        print("❌ Delivery cancelled. Order returned to queue.")

def updatePartnerEarnings(partner_name: str, amount: float, restaurant: str):
    safe_name = "".join(c for c in partner_name if c.isalnum() or c in (' ', '_')).rstrip()
    filepath = os.path.join("partners", f"{safe_name}.json")

    if not os.path.exists(filepath):
        print("❌ Partner file not found.")
        return

    with open(filepath, "r") as f:
        data = json.load(f)

    if "earnings" not in data:
        data["earnings"] = {}

    # Add earnings by restaurant
    if restaurant not in data["earnings"]:
        data["earnings"][restaurant] = 0

    data["earnings"][restaurant] += amount

    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)

def viewEarnings(partner_name: str):
    safe_name = "".join(c for c in partner_name if c.isalnum() or c in (' ', '_')).rstrip()
    filepath = os.path.join("partners", f"{safe_name}.json")

    if not os.path.exists(filepath):
        print("❌ Partner file not found.")
        return

    with open(filepath, "r") as f:
        data = json.load(f)

    earnings = data.get("earnings", {})

    if not earnings:
        print("💰 No earnings yet.")
        return

    print(f"\n💰 Earnings for {partner_name}:\n" + "-" * 30)
    total_earnings = 0

    for restaurant, amount in earnings.items():
        print(f"{restaurant}: ₹{amount}")
        total_earnings += amount

    print("-" * 30)
    print(f"Total Earnings: ₹{total_earnings}")
