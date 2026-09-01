import getpass
import json
import os

# --- File Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EMPLOYEES_FILE = os.path.join(BASE_DIR, "employees.json")
MENUS_FILE = os.path.join(BASE_DIR, "menus.json")

# --- Load JSON Data ---
def load_json(filepath, default_value):
    if not os.path.exists(filepath):
        print(f"\nWarning: Could not find file {filepath}")
        return default_value
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as error:
        print(f"\nError reading file: {error}")
        return default_value

# --- Loading employee data, if file not found setup default admin login ---
EMPLOYEES = load_json(EMPLOYEES_FILE, {"admin": "admin123"})
MENUS = load_json(MENUS_FILE, {"Drinks": [], "Food": [], "Books": []})

# --- Global App State ---
active_discount = 0.0
shopping_cart = {}


# --- Helper Functions ---
def print_banner(title):
    print("\n" + "=" * 60)
    print(f"  {title.upper()}")
    print("=" * 60)


def calculate_totals():
    subtotal = 0.0
    for item_name in shopping_cart:
        item_info = shopping_cart[item_name]
        subtotal += item_info["price"] * item_info["quantity"]

    subtotal = round(subtotal, 2)
    discount_amount = round(subtotal * (active_discount / 100.0), 2)
    final_total = round(subtotal - discount_amount, 2)

    if final_total < 0:
        final_total = 0.0

    return subtotal, discount_amount, final_total


def show_cart():
    print_banner("Your Cart")
    
    if len(shopping_cart) == 0:
        print("Your cart is currently empty.")
        return False

    print(f"{'#':<4} {'Item':<30} {'Qty':<6} {'Price':<10} {'Total'}")
    print("-" * 60)

    line_number = 1
    for item_name, details in shopping_cart.items():
        line_total = round(details["price"] * details["quantity"], 2)
        print(f"[{line_number}]  {item_name:<30} x{details['quantity']:<5} €{details['price']:<9.2f} €{line_total:.2f}")
        line_number += 1

    print("-" * 60)
    subtotal, discount_amt, total = calculate_totals()
    print(f"Subtotal: €{subtotal:.2f}")
    if active_discount > 0:
        print(f"Discount ({active_discount}% OFF): -€{discount_amt:.2f}")
    print(f"Total to Pay: €{total:.2f}")
    return True


# --- Customer Cart Management ---
def edit_cart_item():
    item_keys = list(shopping_cart.keys())
    choice = input("\nEnter item line number to change (or B to cancel): ").strip()
    
    if choice.lower() == "b":
        return

    if not choice.isdigit():
        print("Please enter a valid number.")
        return

    index = int(choice) - 1
    if index < 0 or index >= len(item_keys):
        print("Number not found in cart.")
        return

    selected_item = item_keys[index]
    new_qty_input = input(f"Enter new quantity for '{selected_item}' (0 to delete): ").strip()

    if not new_qty_input.isdigit():
        print("Invalid number entered.")
        return

    new_qty = int(new_qty_input)
    if new_qty <= 0:
        del shopping_cart[selected_item]
        print(f"Removed '{selected_item}' from cart.")
    else:
        shopping_cart[selected_item]["quantity"] = new_qty
        print(f"Updated quantity to {new_qty}.")


def manage_cart():
    global active_discount

    while True:
        has_items = show_cart()
        if not has_items:
            break

        print("\n[1] Checkout and Pay")
        print("[2] Change Item Quantity or Remove")
        print("[3] Clear Entire Cart")
        print("[B] Go Back")

        choice = input("\nChoice: ").strip().lower()

        if choice == "1":
            _, _, total = calculate_totals()
            confirm = input(f"\nPay €{total:.2f}? (Y/N): ").strip().lower()
            if confirm == "y":
                print("\nThank you for your purchase! Enjoy your order.")
                shopping_cart.clear()
                active_discount = 0.0
                break
        elif choice == "2":
            edit_cart_item()
        elif choice == "3":
            shopping_cart.clear()
            print("Cart has been cleared.")
            break
        elif choice == "b":
            break
        else:
            print("Please pick 1, 2, 3, or B.")


# --- Customer Menu Browsing ---
def browse_category(category_name, item_list):
    while True:
        print_banner(f"{category_name} Menu")
        
        if len(item_list) == 0:
            print("No items in this category yet.")
            break

        for i in range(len(item_list)):
            item = item_list[i]
            name = item[0]
            price = item[1]
            print(f"[{i + 1}] {name:<35} €{price:.2f}")

        choice = input("\nPick an item number (or B to return): ").strip()
        if choice.lower() == "b":
            break

        if not choice.isdigit():
            print("Invalid input. Enter a number from the list.")
            continue

        item_index = int(choice) - 1
        if item_index < 0 or item_index >= len(item_list):
            print("Invalid item number.")
            continue

        chosen_item = item_list[item_index]
        name = chosen_item[0]
        price = chosen_item[1]
        desc = chosen_item[2]

        print(f"\n--- {name} ---")
        print(f"Price: €{price:.2f}")
        print(f"Details: {desc}")

        qty_str = input("\nHow many would you like to add? (or press Enter to cancel): ").strip()
        if qty_str.isdigit() and int(qty_str) > 0:
            qty = int(qty_str)
            if name in shopping_cart:
                shopping_cart[name]["quantity"] += qty
            else:
                shopping_cart[name] = {"price": price, "quantity": qty}
            print(f"Added {qty}x {name} to your cart!")
        else:
            print("Cancelled.")


def customer_flow():
    categories = list(MENUS.keys())

    while True:
        total_items = 0
        for item in shopping_cart.values():
            total_items += item["quantity"]

        banner_text = "Customer Hub"
        if active_discount > 0:
            banner_text += f" (Special {active_discount}% OFF Sale!)"
        print_banner(banner_text)

        for i in range(len(categories)):
            cat = categories[i]
            print(f"[{i + 1}] {cat} Menu")
        
        cart_option_number = len(categories) + 1
        print(f"[{cart_option_number}] View Cart & Checkout ({total_items} items)")
        print("[B] Return to Main Menu")

        choice = input("\nChoice: ").strip().lower()
        if choice == "b":
            break

        if not choice.isdigit():
            print("Please enter a valid option number.")
            continue

        chosen_num = int(choice)
        if 1 <= chosen_num <= len(categories):
            selected_cat = categories[chosen_num - 1]
            browse_category(selected_cat, MENUS[selected_cat])
        elif chosen_num == cart_option_number:
            manage_cart()
        else:
            print("Invalid menu number.")


# --- Employee Portal ---
def employee_flow():
    global active_discount

    print_banner("Employee Access")
    username = input("Username (or B to cancel): ").strip()
    if username.lower() == "b":
        return

    password = getpass.getpass("Password: ").strip()

    if username not in EMPLOYEES or EMPLOYEES[username] != password:
        print("\nLogin failed. Incorrect username or password.")
        return

    print(f"\nWelcome back, {username}!")

    while True:
        print_banner("Employee Dashboard")
        print(f"Active Promotional Discount: {active_discount}%\n")
        print("[1] Set Promotional Discount")
        print("[2] Remove Promotional Discount")
        print("[3] View Total Items in Store")
        print("[4] Log Out")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            discount_input = input("Enter discount percentage (e.g. 10 or 20): ").strip()
            try:
                percent = float(discount_input)
                if percent > 0 and percent <= 90:
                    active_discount = round(percent, 2)
                    print(f"Discount updated to {active_discount}%!")
                else:
                    print("Please enter a number between 1 and 90.")
            except Exception:
                print("Invalid number.")
        elif choice == "2":
            active_discount = 0.0
            print("Discount reset back to 0%.")
        elif choice == "3":
            total_count = 0
            for item_list in MENUS.values():
                total_count += len(item_list)
            print(f"Total products listed across all menus: {total_count}")
        elif choice == "4":
            print("Logged out successfully.")
            break
        else:
            print("Please pick 1, 2, 3, or 4.")


# --- Main Application Loop ---
while True:
    print_banner("Cool Beans Coffee & Books")
    print("[1] Customer Menu")
    print("[2] Employee Login")
    print("[Q] Quit Application")

    main_choice = input("\nChoice: ").strip().lower()

    if main_choice == "1":
        customer_flow()
    elif main_choice == "2":
        employee_flow()
    elif main_choice == "q":
        print("\nThank you for visiting Cool Beans. Goodbye!")
        break
    else:
        print("Please choose 1, 2, or Q.")