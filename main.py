import users
import restaurants
import menu
import userCart
import feedback


def main():
    while True:
        print("\n===== Zomato App =====")
        print("1. Register as user")
        print("2. Login as user")
        print("3. Register as restaurant")
        print("4. Login as restaurant")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            users.register()

        elif choice == "2":
            user = users.login()
            if user:
                print(f"Address on file: {user['address']}")
                userCart.createUserCartFile(name = user["username"], address = user["address"])
                while True:
                    print(f"\n===== Options for {user['username']} =====")
                    print("1. Search by Restaurant")
                    print("2. Search by Dish")
                    print("3. Exit")
                    userChoice = input("Choose an options: ")

                    if userChoice == "3":
                        print("Going back to main menu")
                        break
                    
                    elif userChoice == "1":
                        allRestaurants = userCart.displayRestaurants()

                        if not allRestaurants:
                            print("No restaurants available.")
                            continue

                        print("\nAvailable restaurants are:")
                        for i, item in enumerate(allRestaurants):
                            print(f"{i+1}. {item['restaurantName']} : {item['address']}")

                        try:
                            viewMenu = int(input("\nEnter number to view menu: "))
                            if viewMenu < 1 or viewMenu > len(allRestaurants):
                                print("Invalid input")
                                continue
                        except ValueError:
                            print("Please enter a valid number.")
                            continue

                        selectedRestaurant = allRestaurants[viewMenu - 1]["restaurantName"]
                        menu_items = userCart.getMenu(selectedRestaurant)

                        if not menu_items:
                            print("No menu items available.")
                            continue

                        print(f"\nMenu for {selectedRestaurant}:")
                        for i, item in enumerate(menu_items, start=1):
                            print(f"{i}. {item['item']} - ₹{item['price']}")

                        while True:
                            try:
                                choice = input("\nEnter item number to add to cart (or 'done' to stop): ")
                                if choice.lower() == 'done':
                                    userCart.checkoutCart(user["username"])
                                    feedback.collectFeedback(user["username"], selectedRestaurant)
                                    
                                    break

                                item_index = int(choice) - 1
                                if item_index < 0 or item_index >= len(menu_items):
                                    print("Invalid item number.")
                                    continue

                                quantity = int(input("Enter quantity: "))
                                selected_item = menu_items[item_index]

                                userCart.addToCart(user["username"], selectedRestaurant, selected_item["item"], selected_item["price"], quantity)

                            except ValueError:
                                print("Invalid input.")
                                continue
                    
                    elif userChoice == "2":
                        dish = input("Enter dish to search: ").strip()
                        found = userCart.searchDishAcrossRestaurants(dish)
                        if found:
                            print("\nFound in:")
                            for i, res in enumerate(found, start=1):
                                print(f"{i}. {res['restaurantName']} ({res['address']})")
                        else:
                            print("No restaurants found with that dish.")

        elif choice == "3":
            restaurants.register()

        elif choice == "4":
            restaurant = restaurants.login()
            if restaurant:
                print(f"Address on file: {restaurant['address']}")
                menu.createRestaurantFile(name = restaurant["restaurantName"], address = restaurant["address"])
                while True:
                    print(f"\n===== {restaurant['restaurantName']} Restaurant =====")
                    print("1. Menu details")
                    print("2. Order details")
                    print("3. Delete restaurant")
                    print("4. Exit")
                    restaurantChoice = input("Choose an option: ")

                    if restaurantChoice == "1":
                        while True:
                            print("\n1. View Menu")
                            print("2. Add menu items")
                            print("3. Delete menu items")
                            print("4. Update menu items")
                            print("5. Exit")
                            menuChoice = input("Choose an option: ")

                            if menuChoice == "1":
                                menu.viewMenu(restaurant["restaurantName"])
                            
                            elif menuChoice == "2":
                                menu.addMenu(restaurant["restaurantName"])
                            
                            elif menuChoice == "3":
                                menu.deleteMenu(restaurant["restaurantName"])
                            
                            elif menuChoice == "4":
                                menu.updateMenu(restaurant["restaurantName"])

                            elif menuChoice == "5":
                                print("Exiting menu option!")
                                break

                            else:
                                print("Invalid choice!")
                    
                    elif restaurantChoice == "4":
                        print("Exiting resturant view!")
                        break
                        
                    elif restaurantChoice == "2":
                        print("Showing pending orders!")
                        restaurants.viewPendingOrders(restaurant["restaurantName"])

                    elif restaurantChoice == "3":
                        restaurants.deleteRestaurant(restaurant["restaurantName"])
                        break
                    else:
                        print("Invalid choice!")
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
