ORDERS_FILE = "orders.txt"
STARTING_ID = 1001


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
                    continue
                orders.append([int(parts[0]), parts[1], int(parts[2])])
    except FileNotFoundError:
        pass
    return orders


def save_inventory(orders):
    with open(ORDERS_FILE, "w") as file:
        for order_id, product, quantity in orders:
            file.write(f"{order_id},{product},{quantity}\n")
    print(f"Order successfully saved to {ORDERS_FILE}")


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


def next_order_id(orders):
    if not orders:
        return STARTING_ID
    return max(order[0] for order in orders) + 1


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

        new_order = [next_order_id(orders), product, quantity]
        orders.append(new_order)
        total_inventory = process_delivery(total_inventory, quantity)
        orders_added += 1

        print("\nNew Order Added:")
        print(f"{new_order[0]},{new_order[1]},{new_order[2]}\n")
        save_inventory(orders)
        print()

        if total_inventory > 500:
            print("ALERT: Overstock! Total inventory has exceeded 500 units.")
            break

    generate_report(orders_added, failed_entries)


if __name__ == "__main__":
    main()