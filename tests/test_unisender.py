from django.test import TestCase
from django_tasker_unisender import unisender


class BaseTest(TestCase):

    def test_list(self):
        list_id = unisender.create_list('test_py')
        self.assertRegex(str(list_id), '^[0-9]+$')

        lists = unisender.get_list()

        test_data = None
        for item in lists:
            if item.get('title') == 'test_py':
                test_data = item

        if not test_data:
            raise Exception('Not found test_py')

        unisender.delete_list(list_id=list_id)

