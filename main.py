from users import register, login

def main():
    while True:
        print("\n===== Zomato App =====")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            register()
        elif choice == "2":
            user = login()
            if user:
                print(f"Address on file: {user['address']}")
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
