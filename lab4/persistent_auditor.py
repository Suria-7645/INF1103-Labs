ORDERS_FILE = "orders.txt"


def load_inventory():
    orders = []
    try:
        with open(ORDERS_FILE, "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = [part.strip() for part in line.split(",")]
                if len(parts) != 3 or not parts[0].isdigit() or not parts[2].isdigit():
                    continue  # skip malformed lines instead of crashing
                orders.append([int(parts[0]), parts[1], int(parts[2])])
    except FileNotFoundError:
        pass  # no file yet: start with an empty inventory
    return orders


def display_orders(orders):
    print("Current Orders:\n")
    if not orders:
        print("(no orders yet)")
    for order_id, product, quantity in orders:
        print(f"{order_id}, {product}, {quantity}")
    print()


def get_product_name():
    name = input("Enter Product Name: ").strip()

    if name.lower() == "quit":
        return "quit"

    if not name or "," in name:
        print("Error: Product name cannot be empty or contain commas.")
        return "invalid"

    if not any(char.isalpha() for char in name):
        print("Error: Product name must contain letters, not just numbers.")
        return "invalid"

    return name


def get_valid_quantity():
    user_input = input("Enter Quantity: ").strip()

    if not user_input.isdigit() or int(user_input) == 0:
        print("Error: Please enter a positive whole number.")
        return "invalid"

    return int(user_input)


def process_delivery(current_total, new_value):
    return current_total + new_value


def generate_report(orders_added, failed_attempts):
    print("\n--- Order Report ---")
    print(f"Orders Added This Session: {orders_added}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")


def main():
    orders = load_inventory()
    total_inventory = sum(order[2] for order in orders)
    orders_added = 0
    failed_entries = 0

    display_orders(orders)

    while True:
        product = get_product_name()

        if product == "quit":
            break

        if product == "invalid":
            failed_entries += 1
            continue

        quantity = get_valid_quantity()

        if quantity == "invalid":
            failed_entries += 1
            continue

        total_inventory = process_delivery(total_inventory, quantity)
        orders_added += 1

        print(f"\nAccepted: {product}, {quantity}")
        print(f"Running total inventory: {total_inventory}\n")

        if total_inventory > 500:
            print("ALERT: Overstock! Total inventory has exceeded 500 units.")
            break

    generate_report(orders_added, failed_entries)


if __name__ == "__main__":
    main()
