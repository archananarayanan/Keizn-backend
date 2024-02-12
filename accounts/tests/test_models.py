from django.test import TestCase

from accounts.models import User

class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        User.objects.create(username='test', password='test', email='test@t.com')

    def test_username_label(self):
        user = User.objects.get(username='test')
        name = f'{user.username}'
        self.assertEqual(str(user), name)
