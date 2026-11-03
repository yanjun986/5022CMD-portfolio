class Product:
    """One medicine sold by the pharmacy."""
    def __init__(self, product_id, name, category, price, stock, expiry_date, prescription_required):
        self.product_id = product_id                        # str   e.g. "MED001" (hash table key)
        self.name = name                                    # str   e.g. "Paracetamol 500mg"
        self.category = category                            # str   e.g. "Painkiller"
        self.price = price                                  # float e.g. 5.90 (RM)
        self.stock = stock                                  # int   e.g. 120 units
        self.expiry_date = expiry_date                      # str   "YYYY-MM-DD"
        self.prescription_required = prescription_required  # bool  True = needs prescription

    def __str__(self):
        """One-line summary, used by print()."""
        return f"ID: {self.product_id} | Name: {self.name} | Price: RM{self.price:.2f} | Stock: {self.stock}"

    def details(self):
        """Full description, shown when a product is searched."""
        rx = "Yes" if self.prescription_required else "No"
        return (f"  ID                    : {self.product_id}\n"
                f"  Name                  : {self.name}\n"
                f"  Category              : {self.category}\n"
                f"  Price                 : RM {self.price:.2f}\n"
                f"  Stock                 : {self.stock}\n"
                f"  Expiry date           : {self.expiry_date}\n"
                f"  Prescription required : {rx}")

# Pre-defined records loaded into the hash table at start-up (brief Q1 #2)
SAMPLE_PRODUCTS = [
    Product("MED001", "Paracetamol 500mg", "Painkiller",    5.90, 120,
            "2027-08-31", False),
    Product("MED002", "Ibuprofen 200mg",   "Painkiller",    8.50,  80,
            "2027-03-15", False),
    Product("MED003", "Amoxicillin 250mg", "Antibiotic",   18.00,  40,
            "2026-12-31", True),
    Product("MED004", "Cetirizine 10mg",   "Antihistamine",12.40,  60,
            "2028-01-20", False),
    Product("MED005", "Omeprazole 20mg",   "Antacid",      22.30,  35,
            "2027-06-30", True),
    Product("MED006", "Vitamin C 1000mg",  "Supplement",   25.00,  90,
            "2028-05-01", False),
]

if __name__ == "__main__":
    p = SAMPLE_PRODUCTS[0]
    print(p)              # uses __str__
    print(p.details())    # uses details()