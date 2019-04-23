from os import urandom

from django.test import TestCase
from django_tasker_unisender import unisender


class BaseTest(TestCase):
    def setUp(self) -> None:
        self.unisender = unisender.Unisender()

    def test_list(self):
        random = urandom(2).hex()

        list_id = self.unisender.create_list(title="test_py_{random}".format(random=random))
        self.assertRegex(str(list_id), '^[0-9]+$')

        test_data = None
        for item in self.unisender.get_lists():
            if item.get('id') == list_id:
                self.assertEqual(item.get('title'), "test_py_{random}".format(random=random))
                test_data = True

        if not test_data:
            raise Exception('Not found test_py')

        self.unisender.delete_list(list_id=list_id)

    def test_field(self):
        random = urandom(2).hex()

        field_id = self.unisender.create_field(
            name="test_py_{random}".format(random=random),
            field_type="string",
            public_name="test_py_public_name_{random}".format(random=random)
        )
        self.assertRegex(str(field_id), '^[0-9]+$')

        test_data = None
        for item in self.unisender.get_fields():
            if item.get('id') == field_id:
                self.assertEqual(item.get('name'), "test_py_{random}".format(random=random))
                self.assertEqual(item.get('public_name'), "test_py_public_name_{random}".format(random=random))
                self.assertEqual(item.get('type'), "string")
                test_data = True

        if not test_data:
            raise Exception('Not found test_field')

        self.unisender.delete_field(field_id=field_id)

    def test_subscribe_exclude(self):
        random = urandom(2).hex()
        list_id = self.unisender.create_list(title="test_list_{random}".format(random=random))
        self.assertRegex(str(list_id), '^[0-9]+$')

        person_id = self.unisender.subscribe(list_ids=[list_id], fields={'fields[email]': 'test@example.com'})
        self.assertRegex(str(person_id), '^[0-9]+$')

        self.unisender.exclude(contact_type="email", contact='test@example.com', list_ids=[list_id])
        self.unisender.delete_list(list_id=list_id)
