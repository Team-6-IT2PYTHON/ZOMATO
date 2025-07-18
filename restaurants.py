import json
import os

RESTAURANT_FILE = "restaurants.json"

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
