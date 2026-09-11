total_inventory = 0
failed_entries = 0

while True:
    user_input = input("Enter stock quantity (or 'quit' to exit): ").strip()

    if user_input.lower() == "quit":
        break

    if not user_input.isdigit():
        print("Error: Please enter a valid whole number.")
        failed_entries += 1
        continue

    quantity = int(user_input)

    if quantity < 0:
        print("Error: Negative numbers are not allowed.")
        failed_entries += 1
        continue

    total_inventory += quantity
    print(f"Accepted. Current total inventory: {total_inventory}")

    if total_inventory > 500:
        print("ALERT: Overstock! Total inventory has exceeded 500 units.")
        break
    elif total_inventory == 500:
        print("Notice: Inventory has reached exactly 500 units.")
    else:
        pass

print("\n--- Inventory Report ---")
print(f"Total Units Processed: {total_inventory}")
print(f"Number of Failed/Rejected Entries: {failed_entries}")
    


