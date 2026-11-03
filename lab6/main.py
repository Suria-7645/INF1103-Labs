import json
import os

from product import Product
from inventory import Inventory

FILENAME = "inventory.json"


# ---------------- File handling ----------------
def load_inventory(inventory, filename=FILENAME):
    """Load products from a JSON file into the inventory."""
    if not os.path.exists(filename):
        print("No saved inventory found. Starting with an empty inventory.")
        return
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        for item in data:
            inventory.add_product(Product.from_dict(item))
        print(f"Loaded {len(data)} product(s) from {filename}.")
    except (json.JSONDecodeError, KeyError, ValueError):
        print("Could not read inventory file. Starting with an empty inventory.")


def save_inventory(inventory, filename=FILENAME):
    """Save all products in the inventory to a JSON file."""
    data = [p.to_dict() for p in inventory.get_products()]
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Inventory saved to {filename}.")


# ---------------- Menu ----------------
def show_menu():
    print("\n=== Inventory Management System ===")
    print("1. Display all products")
    print("2. Add a product")
    print("3. Update stock")
    print("4. Search for a product")
    print("5. Save inventory")
    print("6. Exit")


def add_product_flow(inventory):
    product_id = input("Product ID: ").strip()
    name = input("Name: ").strip()
    if not product_id or not name:
        print("Product ID and name cannot be empty.")
        return
    try:
        price = float(input("Price: "))
        stock = int(input("Stock quantity: "))
        if price < 0 or stock < 0:
            print("Price and stock cannot be negative.")
            return
    except ValueError:
        print("Invalid number entered. Product not added.")
        return
    if inventory.add_product(Product(product_id, name, price, stock)):
        print("Product added.")
    else:
        print("A product with that ID already exists.")


def update_stock_flow(inventory):
    product = inventory.search_product(input("Product ID to update: ").strip())
    if product is None:
        print("Product not found.")
        return
    try:
        quantity = int(input(f"New stock for {product.get_name()}: "))
        product.update_stock(quantity)
        print("Stock updated.")
    except ValueError as e:
        print(f"Invalid input: {e}")


def search_flow(inventory):
    keyword = input("Enter product ID or name: ").strip()
    product = inventory.search_product(keyword)
    if product is not None:
        product.display_information()
        return
    matches = inventory.search_by_name(keyword)
    if matches:
        for p in matches:
            p.display_information()
    else:
        print("No matching product found.")


def main():
    inventory = Inventory()
    load_inventory(inventory)

    while True:
        show_menu()
        choice = input("Choose an option (1-6): ").strip()
        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            add_product_flow(inventory)
        elif choice == "3":
            update_stock_flow(inventory)
        elif choice == "4":
            search_flow(inventory)
        elif choice == "5":
            save_inventory(inventory)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1-6.")


if __name__ == "__main__":
    main()
