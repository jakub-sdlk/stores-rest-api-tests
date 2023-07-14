from starter_code.models.user import UserModel
from tests.general_base_test import GeneralBaseTest


class UserTest(GeneralBaseTest):
	def test_crud(self):
		with self.app_context():
			user = UserModel('test', 'abcd')

			self.assertIsNone(UserModel.find_by_username('test'))
			self.assertIsNone(UserModel.find_by_id(1))

			user.save_to_db()

			self.assertIsNotNone(UserModel.find_by_username('test'))
			self.assertIsNotNone(UserModel.find_by_id(1))