class Product:
    """Represents and manages a single product.

    Responsibility (SRP): store product information and manage its own state.
    It does not load/save files, show menus or ask the user for input.
    """

    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = float(price)
        self.__stock = int(stock)

    # --- Read-only access to the private attributes ---
    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    # --- Behaviour ---
    def update_stock(self, quantity):
        """Set the stock level. Rejects negative values so stock stays valid."""
        if quantity < 0:
            raise ValueError("Stock cannot be negative.")
        self.__stock = quantity

    def display_information(self):
        print(f"ID: {self.__product_id} | Name: {self.__name} | "
              f"Price: ${self.__price:.2f} | Stock: {self.__stock}")

    # --- Conversion helpers so file handling never touches private attributes ---
    def to_dict(self):
        return {
            "product_id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["product_id"], data["name"], data["price"], data["stock"])
