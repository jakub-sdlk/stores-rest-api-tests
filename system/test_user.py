from starter_code.models.user import UserModel
from tests.general_base_test import GeneralBaseTest
import json


class UserTest(GeneralBaseTest):
	def test_register_user(self):
		with self.app() as client:
			with self.app_context():
				response = client.post(
					'/register', data={'username': 'test', 'password': '1234'}
				)

				self.assertEqual(201, response.status_code)
				self.assertIsNotNone(UserModel.find_by_username('test'))
				self.assertDictEqual({'message': 'User created successfully.'}, json.loads(response.data))

	def test_register_and_login(self):
		with self.app() as client:
			with self.app_context():
				client.post(
					'/register', data={'username': 'test', 'password': '1234'}
				)
				auth_response = client.post(
					'/auth',
					json={'username': 'test', 'password': '1234'},
					headers={'Content-Type': 'application/json'}
				)

				self.assertIn('access_token', json.loads(auth_response.data).keys())

	def test_register_duplicate_user(self):
		with self.app() as client:
			with self.app_context():
				user = UserModel('test', 1234)
				user.save_to_db()
				response2 = client.post(
					'/register', data={'username': 'test', 'password': '1234'}
				)

				self.assertEqual(400, response2.status_code)
				self.assertDictEqual(
					{'message': 'A user with that username already exists'},
					json.loads(response2.data)
				)