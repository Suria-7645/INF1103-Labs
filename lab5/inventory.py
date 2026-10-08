# PHASE C: save_inventory() added (menu option 5 and automatic save on exit)
import json
import os

FILENAME = "inventory.json"


def load_inventory():
    """Load inventory from file if it exists, else return an empty list."""
    if os.path.exists(FILENAME):
        print(f"{FILENAME} found.")
        try:
            with open(FILENAME, "r") as f:
                inventory = json.load(f)
            print("Inventory loaded successfully.")
            return inventory
        except (json.JSONDecodeError, OSError):
            print("Could not read file. Starting with empty inventory.")
    else:
        print(f"{FILENAME} not found. Starting with empty inventory.")
    return []


def save_inventory(inventory):
    """Save inventory (including transaction history) to file."""
    with open(FILENAME, "w") as f:
        json.dump(inventory, f, indent=4)


def find_product(inventory, product_id):
    for product in inventory:
        if product["id"].lower() == product_id.lower():
            return product
    return None


def get_number(prompt, cast, minimum=0):
    """Keep asking until a valid number >= minimum is entered."""
    while True:
        try:
            value = cast(input(prompt))
            if value < minimum:
                print(f"Value must be at least {minimum}.")
                continue
            return value
        except ValueError:
            print("Invalid number, try again.")


def next_product_id(inventory):
    """Return the next ID in sequence: P001, P002, P003, ..."""
    highest = 0
    for product in inventory:
        digits = product["id"][1:]
        if digits.isdigit():
            highest = max(highest, int(digits))
    return f"P{highest + 1:03d}"


def add_product(inventory):
    print("\nAdd New Product")
    product_id = next_product_id(inventory)
    print(f"Product ID: {product_id}")
    name = input("Product Name: ").strip()
    price = get_number("Price: ", float)
    stock = get_number("Stock Quantity: ", int)

    inventory.append({
        "id": product_id,
        "name": name,
        "price": price,
        "stock": stock,
        # every stock change is recorded, not just the running total
        "history": [{"type": "initial", "amount": stock}],
    })
    print("Product added successfully!")


def update_stock(inventory):
    print("\nUpdate Stock")
    product = find_product(inventory, input("Enter Product ID: ").strip())
    if not product:
        print("Product not found.")
        return
    print("Product Found:")
    print(f"Name: {product['name']}")
    print(f"Current Stock: {product['stock']}")
    new_stock = get_number("New Stock Quantity: ", int)

    change = new_stock - product["stock"]
    product["stock"] = new_stock
    product["history"].append({"type": "update", "amount": change})
    print("Stock updated successfully!")


def search_product(inventory):
    print("\nSearch Product")
    product = find_product(inventory, input("Enter Product ID: ").strip())
    if not product:
        print("Product not found.")
        return
    print("Product Found")
    print("-" * 48)
    print(f"ID: {product['id']}")
    print(f"Name: {product['name']}")
    print(f"Price: ${product['price']:.2f}")
    print(f"Stock: {product['stock']}")
    amounts = [f"{t['amount']:+d}" if t["type"] == "update" else str(t["amount"])
               for t in product["history"]]
    print(f"Transaction History: {', '.join(amounts)}")
    print("-" * 48)


def display_all(inventory):
    print("\nCurrent Inventory")
    print("-" * 48)
    if not inventory:
        print("No products in inventory.")
    for p in inventory:
        print(f"ID: {p['id']} | Name: {p['name']} | "
              f"Price: ${p['price']:.2f} | Stock: {p['stock']}")
    print("-" * 48)


def show_menu():
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    inventory = load_inventory()
    show_menu()

    while True:
        choice = input("\nEnter option: ").strip()
        if choice == "1":
            display_all(inventory)
        elif choice == "2":
            add_product(inventory)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            search_product(inventory)
        elif choice == "5":
            print("Saving inventory...")
            save_inventory(inventory)
            print(f"Inventory saved successfully to {FILENAME}.")
        elif choice == "6":
            print("Saving inventory before exit...")
            save_inventory(inventory)
            print("Inventory saved successfully.")
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please enter 1-6.")


if __name__ == "__main__":
    main()