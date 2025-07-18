import users
import restaurants

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

        elif choice == "3":
            restaurants.register()

        elif choice == "4":
            restaurant = restaurants.login()
            if restaurant:
                print(f"Address on file: {restaurant['address']}")
                
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
