import os, json

def createUserCartFile(name: str, address: str):
    safeName = "".join(c for c in name if c.isalnum() or c in (' ', '_')).rstrip()
    folder = "users"
    os.makedirs(folder, exist_ok=True)
    filename = os.path.join(folder, f"{safeName}.json")
    if os.path.exists(filename):
        return 0
    data = {
        "name": name,
        "cart": {},
        "address": address,
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def displayRestaurants():
    with open("restaurants.json", "r") as f:
        data = json.load(f)
        restaurants = []
        for i in data:
            d = {}
            d["restaurantName"] = i["restaurantName"]
            d["address"] = i["address"]
            restaurants.append(d)
        return restaurants

def getMenu(name: str):
    safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '_')).rstrip()
    filepath = os.path.join("restaurants", f"{safe_name}.json")

    if not os.path.exists(filepath):
        print("Restaurant file not found.")
        return []

    with open(filepath, "r") as f:
        data = json.load(f)

    return data.get("menu", [])

def addToCart(username: str, restaurantName: str, itemName: str, price: float, quantity: int):
    safe_name = "".join(c for c in username if c.isalnum() or c in (' ', '_')).rstrip()
    filepath = os.path.join("users", f"{safe_name}.json")

    if not os.path.exists(filepath):
        print("User cart not found.")
        return

    with open(filepath, "r") as f:
        data = json.load(f)

    if "cart" not in data:
        data["cart"] = {}

    if restaurantName not in data["cart"]:
        data["cart"][restaurantName] = []

    # Append the selected item
    data["cart"][restaurantName].append({
        "item": itemName,
        "price": price,
        "quantity": quantity
    })

    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)

    print(f"✅ Added {quantity} x {itemName} to cart.")

def addOrderToRestaurant(restaurant: str, username: str, items: list):
    safe_name = "".join(c for c in restaurant if c.isalnum() or c in (' ', '_')).rstrip()
    filepath = os.path.join("restaurants", f"{safe_name}.json")

    if not os.path.exists(filepath):
        print(f"⚠️ Restaurant file not found: {restaurant}")
        return

    with open(filepath, "r") as f:
        data = json.load(f)

    if "orders" not in data:
        data["orders"] = []

    data["orders"].append({
        "user": username,
        "items": items,
    })

    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)

def checkoutCart(username: str):
    safe_name = "".join(c for c in username if c.isalnum() or c in (' ', '_')).rstrip()
    user_file = os.path.join("users", f"{safe_name}.json")

    if not os.path.exists(user_file):
        print("User not found.")
        return

    with open(user_file, "r") as f:
        user_data = json.load(f)

    cart = user_data.get("cart", {})
    if not cart:
        print("🛒 Your cart is empty.")
        return

    print(f"\n🧾 Cart for {username}:")
    total = 0

    for rest_name, items in cart.items():
        print(f"\nFrom {rest_name}:")
        for item in items:
            subtotal = item["price"] * item["quantity"]
            total += subtotal
            print(f"- {item['item']} x {item['quantity']} = ₹{subtotal}")

    print(f"\n💰 Total Amount: ₹{total}")

    confirm = input("\nProceed to payment? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("❌ Checkout cancelled.")
        return

    # Step 1: Add to restaurant's orders
    for restaurant, items in cart.items():
        addOrderToRestaurant(restaurant, username, items)

    # Step 2: Clear the cart
    user_data["cart"] = {}
    with open(user_file, "w") as f:
        json.dump(user_data, f, indent=4)

    print("✅ Payment successful. Order placed!")

def searchDishAcrossRestaurants(dish_name: str):
    folder = "restaurants"
    results = []

    for filename in os.listdir(folder):
        if filename.endswith(".json"):
            path = os.path.join(folder, filename)
            with open(path, "r") as f:
                data = json.load(f)
                menu = data.get("menu", [])
                
                for item in menu:
                    if item["item"].lower() == dish_name.lower():
                        results.append({
                            "restaurantName": data["name"],
                            "address": data["address"]
                        })
                        break

    return results

