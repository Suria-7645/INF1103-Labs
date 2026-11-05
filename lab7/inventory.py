class Inventory:
    def __init__(self):
        self.__products = []

    def generate_id(self):
        highest = 0
        for product in self.__products:
            digits = "".join(c for c in product.get_product_id() if c.isdigit())
            if digits:
                highest = max(highest, int(digits))
        return f"P{highest + 1:03d}"

    def add_product(self, product):
        if self.search_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def search_product(self, keyword):
        for product in self.__products:
            if product.get_product_id().lower() == keyword.lower():
                return product
        return None

    def search_by_name(self, keyword):
        return [p for p in self.__products
                if keyword.lower() in p.get_name().lower()]

    def display_all(self):
        if not self.__products:
            print("Inventory is empty.")
            return
        for product in self.__products:
            product.display_information()

    def get_products(self):
        return list(self.__products)
