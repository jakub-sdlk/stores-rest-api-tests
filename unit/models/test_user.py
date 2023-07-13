from starter_code.models.user import UserModel
from tests.unit.unit_base_test import UnitBaseTest
import pytest


class UserTest(UnitBaseTest):
	def test_create_user(self):
		user = UserModel("test", 1234)

		self.assertEqual("test", user.username)
		self.assertEqual(1234, user.password)
