class Inventory:
    """Manages a collection of Product objects.

    Responsibility (SRP): store, add, search and display products.
    It does not read user input, show the menu or touch files.
    """

    def __init__(self):
        self.__products = []

    def add_product(self, product):
        """Add a product. Returns False if the product ID already exists."""
        if self.search_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def search_product(self, keyword):
        """Find a product by exact ID (case-insensitive). Returns Product or None."""
        for product in self.__products:
            if product.get_product_id().lower() == keyword.lower():
                return product
        return None

    def search_by_name(self, keyword):
        """Return a list of products whose name contains the keyword."""
        return [p for p in self.__products
                if keyword.lower() in p.get_name().lower()]

    def display_all(self):
        if not self.__products:
            print("Inventory is empty.")
            return
        for product in self.__products:
            product.display_information()

    def get_products(self):
        """Return a copy of the product list so callers cannot alter the original."""
        return list(self.__products)
