from django.test import TestCase


class BaseTest(TestCase):

    def test_base(self):
        self.assertEqual(True, True)

    def test_model(self):
        from . import models

        for item in dir(models):
            print(item)
