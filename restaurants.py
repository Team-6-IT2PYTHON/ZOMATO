import json
import os

RESTAURANT_FILE = "restaurants.json"
ORDERS_FILE = "orders.json"

def loadRestaurants():
    if not os.path.exists(RESTAURANT_FILE) or os.path.getsize(RESTAURANT_FILE) == 0:
        return []
    with open(RESTAURANT_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def saveRestaurants(restaurants):
    with open(RESTAURANT_FILE, "w") as f:
        json.dump(restaurants, f, indent=4)

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
    restaurants = loadRestaurants()
    restaurantName = input("Enter restaurant name: ")
    if any(r["restaurantName"] == restaurantName for r in restaurants):
        print("Restaurant alredy exists")
        return
    password = input("Enter password: ")
    address = input("Enter address: ")
    restaurants.append({
        "restaurantName": restaurantName,
        "password": password,
        "address": address,
    })
    saveRestaurants(restaurants)
    print("Registered succesfully!")

def login():
    restaurants = loadRestaurants()
    restaurantName = input("Enter username: ")
    password = input("Enter password: ")

    for i in restaurants:
        if i["restaurantName"] == restaurantName and i["password"] == password:
            print(f"Welcome back, Restaurant {restaurantName}!")
            return i
    print("Invalid username or password!")
    return None

def viewPendingOrders(restaurant_name: str):
    safe_name = "".join(c for c in restaurant_name if c.isalnum() or c in (' ', '_')).rstrip()
    filepath = os.path.join("restaurants", f"{safe_name}.json")

    if not os.path.exists(filepath):
        print("❌ Restaurant file not found.")
        return

    with open(filepath, "r") as f:
        data = json.load(f)

    orders = data.get("orders", [])

    if not orders:
        print("✅ No pending orders.")
        return

    print(f"\n📦 Pending Orders for {data['name']}:\n" + "-" * 40)

    for index, order in enumerate(orders, start=1):
        user = order.get("user", "") or "Guest"
        print(f"\nOrder {index} by {user}:")

        total = 0
        for item in order["items"]:
            subtotal = item["price"] * item["quantity"]
            total += subtotal
            print(f" - {item['item']} x {item['quantity']} = ₹{subtotal}")

        print(f"Total: ₹{total}")
        print("-" * 40)

    try:
        choice = input("\nEnter the order number that has been prepared (or press Enter to skip): ").strip()
        if not choice:
            print("✅ No orders marked as prepared.")
            return

        order_index = int(choice) - 1
        if 0 <= order_index < len(orders):
            prepared_order = orders.pop(order_index)

            # Add restaurant info and order ID to the order
            prepared_order["restaurant"] = restaurant_name
            prepared_order["restaurant_address"] = data.get("address", "")
            prepared_order["order_id"] = f"{restaurant_name}_{len(loadOrders()) + 1}"
            prepared_order["status"] = "ready_for_delivery"

            # Add to orders.json for delivery partners
            all_orders = loadOrders()
            all_orders.append(prepared_order)
            saveOrders(all_orders)

            print(f"✅ Order #{choice} marked as prepared and ready for delivery.")

            # Update restaurant file
            data["orders"] = orders
            with open(filepath, "w") as f:
                json.dump(data, f, indent=4)
        else:
            print("❌ Invalid order number.")
    except ValueError:
        print("❌ Invalid input. Please enter a valid number.")

def deleteRestaurant(name: str):
    safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '_')).rstrip()
    filepath = os.path.join("restaurants", f"{safe_name}.json")
    if os.path.exists(filepath):
        os.remove(filepath)
    else:
        print("Restaurant file not found.")
    try:
        with open("restaurants.json", "r") as f:
            data = json.load(f)
        updated_data = [r for r in data if r["restaurantName"] != name]

        with open("restaurants.json", "w") as f:
            json.dump(updated_data, f, indent=4)

        print(f"{name}' hs been removed from zomato")
    except Exception as e:
        print(f"❌ Error updating restaurants.json: {e}")
