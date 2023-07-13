from starter_code.models.item import ItemModel
from starter_code.models.store import StoreModel
from tests.general_base_test import GeneralBaseTest


class ItemTest(GeneralBaseTest):
    def test_crud(self):
        with self.app_context():
            StoreModel('Test store').save_to_db()
            item = ItemModel('test', 19.99, 1)

            self.assertIsNone(ItemModel.find_by_name('test'),
                              "Found an item with name {}, but expected not to.".format(item.name))

            item.save_to_db()

            self.assertIsNotNone(ItemModel.find_by_name('test'))

            item.delete_from_db()

            self.assertIsNone(ItemModel.find_by_name('test'))

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel("test_store")
            item = ItemModel("test_item", 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual("test_store", item.store.name)
            self.assertEqual(1, item.store.id)

