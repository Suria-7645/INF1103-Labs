import os
import tempfile
import unittest

from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from inventory import Inventory
from main import load_inventory, save_inventory


class TestProducts(unittest.TestCase):
    def setUp(self):
        self.physical = PhysicalProduct("P001", "Guitar", 500.0, 5, 3.5)
        self.digital = DigitalProduct("P002", "Operating System", 99.0, 100, 4200.0)

    def test_physical_stores_weight(self):
        self.assertEqual(self.physical.get_weight(), 3.5)

    def test_digital_stores_download_size(self):
        self.assertEqual(self.digital.get_download_size(), 4200.0)

    def test_subclasses_implement_fulfilment_info(self):
        self.assertIn("shipping", self.physical.get_fulfilment_info())
        self.assertIn("digitally", self.digital.get_fulfilment_info())

    def test_product_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            Product("P999", "Generic", 1.0, 1)

    def test_physical_shipping_cost_depends_on_weight(self):
        light = PhysicalProduct("P003", "Pen", 2.0, 10, 0.1)
        heavy = PhysicalProduct("P004", "Anvil", 80.0, 2, 50.0)
        self.assertAlmostEqual(light.calculate_shipping_cost(), 5.2)
        self.assertAlmostEqual(heavy.calculate_shipping_cost(), 105.0)
        self.assertGreater(heavy.calculate_shipping_cost(),
                           light.calculate_shipping_cost())

    def test_physical_is_shippable_digital_is_not(self):
        self.assertIsInstance(self.physical, CanBeShipped)
        self.assertNotIsInstance(self.digital, CanBeShipped)
        self.assertFalse(hasattr(self.digital, "calculate_shipping_cost"))

    def test_negative_values_rejected(self):
        with self.assertRaises(ValueError):
            PhysicalProduct("P005", "Bad", 1.0, 1, -1)
        with self.assertRaises(ValueError):
            DigitalProduct("P006", "Bad", 1.0, 1, -1)
        with self.assertRaises(ValueError):
            self.physical.update_stock(-1)


class TestInventory(unittest.TestCase):
    def setUp(self):
        self.inventory = Inventory()
        self.physical = PhysicalProduct("P001", "Guitar", 500.0, 5, 3.5)
        self.digital = DigitalProduct("P002", "Operating System", 99.0, 100, 4200.0)
        self.inventory.add_product(self.physical)
        self.inventory.add_product(self.digital)

    def test_add_and_duplicate(self):
        self.assertFalse(self.inventory.add_product(self.physical))
        self.assertEqual(len(self.inventory.get_products()), 2)

    def test_search_by_id_and_name(self):
        self.assertIs(self.inventory.search_product("p001"), self.physical)
        self.assertEqual(self.inventory.search_by_name("operating"), [self.digital])
        self.assertIsNone(self.inventory.search_product("P404"))

    def test_update_stock(self):
        self.inventory.search_product("P001").update_stock(12)
        self.assertEqual(self.physical.get_stock(), 12)

    def test_generate_id(self):
        self.assertEqual(self.inventory.generate_id(), "P003")
        self.assertEqual(Inventory().generate_id(), "P001")


class TestPersistence(unittest.TestCase):
    def test_round_trip_preserves_types_and_attributes(self):
        original = Inventory()
        original.add_product(PhysicalProduct("P001", "Guitar", 500.0, 5, 3.5))
        original.add_product(DigitalProduct("P002", "Operating System", 99.0, 100, 4200.0))
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "inventory.json")
            save_inventory(original, path)
            restored = Inventory()
            load_inventory(restored, path)
        physical = restored.search_product("P001")
        digital = restored.search_product("P002")
        self.assertIsInstance(physical, PhysicalProduct)
        self.assertIsInstance(digital, DigitalProduct)
        self.assertEqual(physical.get_weight(), 3.5)
        self.assertEqual(digital.get_download_size(), 4200.0)
        self.assertEqual(digital.get_stock(), 100)

    def test_bad_file_gives_empty_inventory(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "inventory.json")
            with open(path, "w") as f:
                f.write('[{"product_id": "P001", "name": "Old", "price": 1, "stock": 1}]')
            inventory = Inventory()
            load_inventory(inventory, path)
        self.assertEqual(inventory.get_products(), [])


if __name__ == "__main__":
    unittest.main()
