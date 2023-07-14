from starter_code.models.store import StoreModel
from starter_code.models.item import ItemModel
from tests.general_base_test import GeneralBaseTest


class StoreTest(GeneralBaseTest):
    def test_create_store_items_empty(self):
        store = StoreModel("test store")

        self.assertListEqual(store.items.all(), [])

    def test_crud(self):
        with self.app_context():
            store = StoreModel("test store")
            self.assertIsNone(StoreModel.find_by_name("test store"))

            store.save_to_db()
            self.assertIsNotNone(StoreModel.find_by_name("test store"))
            self.assertEqual("test store", StoreModel.find_by_name("test store").name)

            store.delete_from_db()
            self.assertIsNone(StoreModel.find_by_name("test store"))

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel("test store")
            item = ItemModel("test item", 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(1, store.items.count())
            self.assertEqual("test item", store.items.first().name)

    def test_store_json(self):
        with self.app_context():
            store = StoreModel("test store")
            store.save_to_db()
            expected = {
                'id': 1,
                'name': 'test store',
                'items':
                    []
            }

            self.assertEqual(expected, store.json())

            guitar = ItemModel("guitar", 100, 1)
            guitar.save_to_db()
            expected2 = {
                'id': 1,
                'name': 'test store',
                'items':
                    [
                        {'name': 'guitar',
                         'price': 100
                         }
                    ]
            }

            self.assertEqual(expected2, store.json())

            piano = ItemModel("piano", 1200, 1)
            piano.save_to_db()

            expected3 = {
                'id': 1,
                'name': 'test store',
                'items':
                    [
                        {'name': 'guitar',
                         'price': 100
                         },
                        {'name': 'piano',
                         'price': 1200
                         }
                    ]
            }

            self.assertEqual(expected3, store.json())

            book = ItemModel("book", 19.99, 2)
            book.save_to_db()

            self.assertEqual(expected3, store.json())