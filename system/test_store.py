from starter_code.models.store import StoreModel
from starter_code.models.item import ItemModel
from tests.general_base_test import GeneralBaseTest
import json


class StoreTest(GeneralBaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                self.assertIsNone(StoreModel.find_by_name('test'))

                response = client.post(
                    '/store/test'
                )

                self.assertEqual(201, response.status_code)
                self.assertIsNotNone(StoreModel.find_by_name('test'))
                self.assertDictEqual({'id': 1, 'name': 'test', 'items': []}, json.loads(response.data))

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    '/store/test'
                )

                response = client.post(
                    '/store/test'
                )
                expected = {'message': "A store with name 'test' already exists."}
                self.assertEqual(400, response.status_code)
                self.assertDictEqual(expected, json.loads(response.data))

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    '/store/test'
                )

                self.assertIsNotNone(StoreModel.find_by_name('test'))

                response = client.delete(
                    '/store/test'
                )

                self.assertIsNone(StoreModel.find_by_name('test'))
                self.assertEqual(200, response.status_code)
                self.assertDictEqual({"message": "Store 'test' deleted"}, json.loads(response.data))

    def test_delete_non_existing_store(self):
        with self.app() as client:
            with self.app_context():
                self.assertIsNone(StoreModel.find_by_name('test'))

                response = client.delete(
                    '/store/test'
                )

                self.assertEqual(404, response.status_code)
                self.assertDictEqual({'message': 'Store not found'}, json.loads(response.data))

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    '/store/test'
                )

                response = client.get(
                    '/store/test'
                )

                self.assertEqual('test', StoreModel.find_by_name('test').name)
                self.assertEqual(200, response.status_code)
                self.assertDictEqual({'id': 1, 'name': 'test', 'items': []}, json.loads(response.data))

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                self.assertIsNone(StoreModel.find_by_name('test'))

                response = client.get(
                    '/store/test'
                )

                self.assertIsNone(StoreModel.find_by_name('test'))
                self.assertEqual(404, response.status_code)
                self.assertEqual({'message': 'Store not found'}, json.loads(response.data))

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    '/store/test'
                )
                ItemModel('shirt', 10, 1).save_to_db()
                ItemModel('shorts', 20, 1).save_to_db()

                response = client.get(
                    '/store/test'
                )

                expected = {
                    'id': 1,
                    'name': 'test',
                    'items': [
                        {
                            'name': 'shirt',
                            'price': 10
                        }, {
                            'name': 'shorts',
                            'price': 20}
                            ]
                    }

                self.assertEqual(200, response.status_code)
                self.assertEqual(expected, json.loads(response.data))

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    '/store/test'
                )

                response = client.get('/stores')

                expected = {'stores': [{'id': 1, 'name': 'test', 'items': []}]}
                self.assertEqual(200, response.status_code)
                self.assertEqual(expected, json.loads(response.data))

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    '/store/test'
                )

                ItemModel('shirt', 10, 1).save_to_db()
                ItemModel('shorts', 20, 1).save_to_db()

                response = client.get('/stores')

                expected = {
                    'stores': [
                        {
                            'id': 1,
                            'name': 'test',
                            'items': [
                                {
                                    'name': 'shirt',
                                    'price': 10
                                }, {
                                    'name': 'shorts',
                                    'price': 20}
                            ]
                        }
                    ]
                }

                self.assertEqual(200, response.status_code)
                self.assertEqual(expected, json.loads(response.data))
