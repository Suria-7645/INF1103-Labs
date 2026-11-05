import json
import os

from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from inventory import Inventory

FILENAME = "inventory.json"

PRODUCT_TYPES = {
    "physical": PhysicalProduct,
    "digital": DigitalProduct,
}


def load_inventory(inventory, filename=FILENAME):
    if not os.path.exists(filename):
        print("No saved inventory found. Starting with an empty inventory.")
        return
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        products = [PRODUCT_TYPES[item["type"]].from_dict(item) for item in data]
    except (json.JSONDecodeError, KeyError, ValueError, TypeError):
        print("Could not read inventory file. Starting with an empty inventory.")
        return
    for product in products:
        inventory.add_product(product)
    print(f"Loaded {len(products)} product(s) from {filename}.")


def save_inventory(inventory, filename=FILENAME):
    data = [p.to_dict() for p in inventory.get_products()]
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Inventory saved to {filename}.")


def show_menu():
    print("\n=== Inventory Management System ===")
    print("1. Display all products")
    print("2. Add a product")
    print("3. Update stock")
    print("4. Search for a product")
    print("5. Save inventory")
    print("6. Exit")


def show_product_details(product):
    product.display_information()
    print(f"    {product.get_fulfilment_info()}")
    if isinstance(product, CanBeShipped):
        print(f"    Shipping cost: ${product.calculate_shipping_cost():.2f}")


def add_product_flow(inventory):
    print("Product type:")
    print("  1. Physical")
    print("  2. Digital")
    type_choice = input("Choose a type (1-2): ").strip()
    if type_choice not in ("1", "2"):
        print("Invalid product type.")
        return
    name = input("Name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    try:
        price = float(input("Price: "))
        stock = int(input("Stock quantity: "))
        if price < 0 or stock < 0:
            print("Price and stock cannot be negative.")
            return
        product_id = inventory.generate_id()
        if type_choice == "1":
            weight = float(input("Weight (kg): "))
            product = PhysicalProduct(product_id, name, price, stock, weight)
        else:
            download_size = float(input("Download size (MB): "))
            product = DigitalProduct(product_id, name, price, stock, download_size)
    except ValueError as e:
        print(f"Invalid input: {e} Product not added.")
        return
    inventory.add_product(product)
    print(f"Product added with ID {product.get_product_id()}.")


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
        show_product_details(product)
        return
    matches = inventory.search_by_name(keyword)
    if matches:
        for p in matches:
            show_product_details(p)
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
