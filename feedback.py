#

def collectFeedback(username, restaurant_name):
    print("\n===== Feedback Section =====")
    
    try:
        rating = float(input(f"Rate {restaurant_name} (1.0 to 5.0): "))
        if not (1.0 <= rating <= 5.0):
            print("❌ Rating must be between 1 and 5.")
            return
    except ValueError:
        print("❌ Invalid input for rating.")
        return

    review = input("Write your feedback: ").strip()

    # Save to file
    with open("reviews.txt", "a") as f:
        f.write(f"User: {username}\nRestaurant: {restaurant_name}\nRating: {rating}\nReview: {review}\n{'-'*40}\n")

    print(" Thank you for your feedback!")
