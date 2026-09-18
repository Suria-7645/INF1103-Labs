def get_valid_input():
    """Prompt once. Return an int, 'quit', or 'invalid'."""
    user_input = input("Enter delivery quantity (or 'quit' to exit): ").strip()

    if user_input.lower() == "quit":
        return "quit"

    if not user_input.isdigit():
        print("Error: Please enter a valid whole number.")
        return "invalid"

    value = int(user_input)

    if value < 0:
        print("Error: Negative numbers are not allowed.")
        return "invalid"

    return value


def process_delivery(current_total, new_value):
    """Add new_value to current_total and return the new total."""
    return current_total + new_value


def calculate_tax(amount):
    """Return 10% tax on a single delivery amount."""
    return amount * 0.10


def generate_report(total_units, failed_attempts):
    """Print the final summary."""
    print("\n--- Delivery Report ---")
    print(f"Total Deliveries Processed: {total_units}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")


def main():
    total_inventory = 0
    deliveries_processed = 0
    failed_entries = 0

    while True:
        result = get_valid_input()

        if result == "quit":
            break

        if result == "invalid":
            failed_entries += 1
            continue

        # result is a valid int at this point
        total_inventory = process_delivery(total_inventory, result)
        tax = calculate_tax(result)
        deliveries_processed += 1

        print(f"Accepted delivery of {result} units. Tax on this delivery: {tax:.2f}")
        print(f"Running total inventory: {total_inventory}")

        if total_inventory > 500:
            print("ALERT: Overstock! Total inventory has exceeded 500 units.")
            break

    generate_report(deliveries_processed, failed_entries)


if __name__ == "__main__":
    main()