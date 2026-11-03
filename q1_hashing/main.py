from datetime import datetime, date

from hash_table import HashTable
from product import Product, SAMPLE_PRODUCTS


def ask_text(prompt):
    """Ask for text that cannot be empty."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  This cannot be empty. Please try again.")


def ask_product_id(prompt):
    """Ask for an ID in the format 3 letters + 3 digits, e.g. MED007."""
    while True:
        value = input(prompt).strip().upper()
        if len(value) == 6 and value[:3].isalpha() and value[3:].isdigit():
            return value
        print("  ID must be 3 letters followed by 3 digits (e.g. MED007).")


def ask_float(prompt):
    """Ask for a number with decimals that is 0 or more (e.g. a price)."""
    while True:
        try:
            value = float(input(prompt))
            if value >= 0:
                return value
        except ValueError:  # the user typed something that isn't a number
            pass
        print("  Please enter a number that is 0 or more (e.g. 5.90).")


def ask_int(prompt):
    """Ask for a whole number that is 0 or more (e.g. stock)."""
    while True:
        try:
            value = int(input(prompt))
            if value >= 0:
                return value
        except ValueError:
            pass
        print("  Please enter a whole number that is 0 or more (e.g. 120).")


def ask_date(prompt):
    """Ask for a real, future date in the format YYYY-MM-DD."""
    while True:
        value = input(prompt).strip()
        try:
            expiry = datetime.strptime(value, "%Y-%m-%d").date()   # text -> real date
        except ValueError:
            print("  Please use the format YYYY-MM-DD (e.g. 2027-08-31).")
            continue                                              # ask again
        if expiry <= date.today():
            print("  This date is today or has already passed. Expired stock cannot be added.")
            continue
        return value


def ask_yes_no(prompt):
    """Ask a yes/no question. Returns True for yes, False for no."""
    while True:
        value = input(prompt).strip().lower()
        if value in ("y", "yes"):
            return True
        if value in ("n", "no"):
            return False
        print("  Please type y or n.")


# Fixed list of categories, so every product uses the same spelling.
CATEGORIES = ["Painkiller", "Antibiotic", "Antihistamine", "Antacid", "Supplement", "Other"]


def ask_category(prompt):
    """Show the category list and ask the user to pick one by number."""
    print(prompt)
    for number, name in enumerate(CATEGORIES, start=1):
        print(f"    {number}. {name}")
    while True:
        choice = input("  Choose a category number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(CATEGORIES):
            return CATEGORIES[int(choice) - 1]
        print(f"  Please enter a number from 1 to {len(CATEGORIES)}.")


def insert_product(table):
    """Option 1: add a new product."""
    print("\n--- Insert a new product ---")
    product_id = ask_product_id("Product ID (e.g. MED007): ")

    if table.search(product_id) is not None:  # IDs must be unique
        print(f"  {product_id} already exists. Use Edit to change it.")
        return

    product = Product(
        product_id,
        ask_text("Name: "),
        ask_category("Category:"),
        ask_float("Price (RM): "),
        ask_int("Stock: "),
        ask_date("Expiry date (YYYY-MM-DD): "),
        ask_yes_no("Prescription required? (y/n): "),
    )
    slot = table.insert(product_id, product)
    print(f"  Inserted {product_id} into slot {slot}.")


def search_by_id(table):
    """Option 2: find one product by its ID - uses the hash, O(1) on average."""
    product_id = ask_product_id("\nEnter product ID: ")
    product = table.search(product_id)
    if product is None:
        print(f"  {product_id} not found.")
    else:
        print(f"  Found {product_id}:")
        print(product.details())


def search_by_name(table):
    """Option 3: find products whose name contains some text - checks every slot, O(n)."""
    text = ask_text("\nEnter part of the name (e.g. vitamin): ").lower()
    matches = [p for _, p in table.items() if text in p.name.lower()]
    if not matches:
        print(f"  No product name contains '{text}'.")
    else:
        print(f"  {len(matches)} match(es):")
        for p in matches:
            print(f"  {p}")


def edit_product(table):
    """Option 4: change the details of an existing product."""
    product_id = ask_product_id("\nEnter product ID to edit: ")
    product = table.search(product_id)
    if product is None:
        print(f"  {product_id} not found.")
        return

    print("  Current details:")
    print(product.details())
    print("  Enter the new details:")
    product.name = ask_text("Name: ")
    product.category = ask_category("Category:")
    product.price = ask_float("Price (RM): ")
    product.stock = ask_int("Stock: ")
    product.expiry_date = ask_date("Expiry date (YYYY-MM-DD): ")
    product.prescription_required = ask_yes_no("Prescription required? (y/n): ")
    # No need to insert again: the table holds this same Product object,
    # so changing it here changes it inside the table too.
    print(f"  {product_id} updated.")


def delete_product(table):
    """Option 5: remove a product (the slot becomes a tombstone)."""
    product_id = ask_product_id("\nEnter product ID to delete: ")
    if table.delete(product_id):
        print(f"  {product_id} deleted.")
    else:
        print(f"  {product_id} not found.")


def list_products(table):
    """Option 6: show every product, sorted by ID."""
    products = sorted((p for _, p in table.items()), key=lambda p: p.product_id)
    print(f"\n--- All products ({len(products)}) ---")
    for p in products:
        print(f"  {p}")


def show_table(table):
    """Option 7: show every slot, so collisions and probing are visible."""
    print("\n--- Hash table slots ---")
    table.display()


# Menu number -> (label, function). Adding a new option only needs one new line here.
MENU = {
    "1": ("Insert product", insert_product),
    "2": ("Search product by ID", search_by_id),
    "3": ("Search product by name", search_by_name),
    "4": ("Edit product", edit_product),
    "5": ("Delete product", delete_product),
    "6": ("List all products", list_products),
    "7": ("Show hash table slots", show_table),
}


def main():
    # Create the table and load the pre-defined products (brief Q1 #2).
    table = HashTable(11)
    for p in SAMPLE_PRODUCTS:
        table.insert(p.product_id, p)  # key = ID, value = whole Product
    print(f"Loaded {table.count} pre-defined products.")

    # Keep showing the menu until the user chooses 0.
    while True:
        print("\n========== PHARMACY INVENTORY ==========")
        for number, (label, _) in MENU.items():
            print(f" {number}. {label}")
        print(" 0. Exit")
        print("========================================")
        choice = input("Choose an option: ").strip()

        if choice == "0":
            print("Goodbye!")
            break
        if choice in MENU:
            _, action = MENU[choice]
            action(table)  # run the chosen option
        else:
            print("  Invalid option, please choose 0-7.")


if __name__ == "__main__":
    main()