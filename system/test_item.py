from starter_code.models.store import StoreModel
from starter_code.models.item import ItemModel
from starter_code.models.user import UserModel
from tests.general_base_test import GeneralBaseTest
import json


class ItemTest(GeneralBaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()  # making sure the General base test setup works as well
        with self.app() as client:
            with self.app_context():
                UserModel('test user', '1234').save_to_db()
                auth_request = client.post('auth', data=json.dumps({'username': 'test user', 'password': '1234'}),
                                           headers={'Content-Type': 'application/json'})
                auth_token = json.loads(auth_request.data)['access_token']
                self.access_token = {'Authorization': f'JWT {auth_token}'}

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():

                response = client.get('/item/test')

                expected = {
                    'message': 'Could not authorize. Did you include a valid Authorization header?'
                }
                self.assertIsNone(ItemModel.find_by_name('test'))
                self.assertEqual(401, response.status_code)
                self.assertDictEqual(expected, json.loads(response.data))

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/item/test', headers=self.access_token)

                self.assertIsNone(ItemModel.find_by_name('test'))
                self.assertEqual(404, response.status_code)
                self.assertDictEqual({'message': 'Item not found'}, json.loads(response.data))

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test store').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                response = client.get('/item/test', headers=self.access_token)

                self.assertIsNotNone(ItemModel.find_by_name('test'))
                self.assertEqual(200, response.status_code)
                self.assertDictEqual({'name': 'test', 'price': 19.99}, json.loads(response.data))

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test store').save_to_db()
                response = client.post('/item/test', data={'price': 19.99, 'store_id': 1})

                self.assertIsNotNone(ItemModel.find_by_name('test'))
                self.assertEqual(201, response.status_code)
                self.assertDictEqual({'name': 'test', 'price': 19.99}, json.loads(response.data))

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test store').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()

                self.assertIsNotNone(ItemModel.find_by_name('test'))
                response = client.delete('/item/test')

                self.assertIsNone(ItemModel.find_by_name('test'))
                self.assertEqual(200, response.status_code)
                self.assertDictEqual({"message": "Item 'test' deleted"}, json.loads(response.data))

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test store').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                response = client.post('/item/test', data={'price': 19.99, 'store_id': 1})

                expected = {'message': 'An item with name \'test\' already exists.'}
                self.assertEqual(400, response.status_code)
                self.assertDictEqual(expected, json.loads(response.data))

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test store').save_to_db()
                response = client.put('/item/test', data={'price': 19.99, 'store_id': 1})

                self.assertEqual(200, response.status_code)
                self.assertDictEqual({'name': 'test', 'price': 19.99}, json.loads(response.data))

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test store').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()

                response = client.get('/item/test', headers=self.access_token)
                self.assertDictEqual({'name': 'test', 'price': 19.99}, json.loads(response.data))

                response = client.put('/item/test', data={'price': 17.99, 'store_id': 1})

                self.assertEqual(200, response.status_code)
                self.assertDictEqual({'name': 'test', 'price': 17.99}, json.loads(response.data))

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test store').save_to_db()

                response = client.get('/items')
                self.assertEqual(200, response.status_code)
                self.assertDictEqual({'items': []}, json.loads(response.data))

                ItemModel('test', 19.99, 1).save_to_db()
                ItemModel('test2', 17.99, 1).save_to_db()
                response = client.get('/items')

                expected = {
                    'items': [
                        {
                         'name': 'test',
                         'price': 19.99
                         }, {
                         'name': 'test2',
                         'price': 17.99}
                    ]
                }
                self.assertDictEqual(expected, json.loads(response.data))

