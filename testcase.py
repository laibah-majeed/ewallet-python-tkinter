import unittest
from user import User

class TestEWalletBasic(unittest.TestCase):

    def setUp(self):
        self.user = User("ali", "pass123", "03123456789", 1000.0)

    def test_login_success(self):
        self.assertEqual(self.user.username, "ali")
        self.assertEqual(self.user.password, "pass123")

    def test_login_failure_wrong_password(self):
        self.assertNotEqual(self.user.password, "wrongpass")

    def test_money_deposit(self):
        result = self.user.deposit(500)
        self.assertTrue(result)
        self.assertEqual(self.user.balance, 1500.0)

if __name__ == '__main__':
    unittest.main()
