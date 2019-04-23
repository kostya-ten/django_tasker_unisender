from django.test import TestCase


class BaseTest(TestCase):

    def test_base(self):
        self.assertEqual(True, True)


