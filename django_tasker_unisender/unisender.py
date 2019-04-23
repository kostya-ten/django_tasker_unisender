import os

import requests
from django.conf import settings


class Unisender:
    """Base class to work with low-level API Unisender
    """

    def __init__(self, api_key: str = None):
        if not api_key:
            self.api_key = getattr(settings, 'UNISENDER_API_KEY', os.environ.get('UNISENDER_API_KEY'))
        else:
            self.api_key = api_key

    def get_request(self, method: str = None, data: dict = None) -> object:
        url = "{url}/{method}".format(url="https://api.unisender.com/ru/api", method=method)

        if data:
            data = {
                **data,
                **{
                    'format': 'json',
                    'api_key': self.api_key,
                    'platform': 'Django module django_tasker_unisender'
                }
            }
        else:
            data = {'format': 'json', 'api_key': self.api_key, 'platform': 'Django module django_tasker_unisender'}

        response = requests.request(method='POST', url=url, data=data)

        json = response.json()
        if json.get('error'):
            raise requests.HTTPError("Unisender error: {error}".format(error=json.get('error')))
        return json.get('result')

    # Lists
    def create_list(self, title: str) -> int:
        """
        Checks the validity of a mobile phone number.

        :param title: List name. It must be unique in your account.
        :returns: Identifier campaign list
        """
        result = self.get_request(method='createList', data={'title': title})
        return result.get('id')

    def get_lists(self) -> list:
        """It is a method to get the list of all available campaign lists.

        :returns: Array, each array element is an object dict with the following id and title fields.
        """
        return self.get_request(method='getLists')

    def delete_list(self, list_id: int) -> None:
        """It is a method to delete a list.

         :param list_id: Identifier campaign list
         """
        self.get_request(method='deleteList', data={'list_id': list_id})

    def update_list(self, list_id: int, title: str) -> None:
        """It is a method to change campaign list properties.

        :param list_id: Identifier campaign list.
        :param title: List name. It must be unique in your account.
        """
        self.get_request(method='updateList', data={'list_id': list_id, 'title': title})

    # Fields
    def create_field(self, name: str, field_type: str, public_name: str = None) -> int:
        """It is a method to create a new user field, the value of which can be set for each recipient,
        and then it can be substituted in the letter.

        :parameter name: Variable to be substituted. It must be unique and case sensitive.
                    Also, it is not recommended to create a field with the same name as the standard field names
                    (tags, email, phone, email_status, phone_status, etc.) as the importContacts.
                    Admissible characters: Latin letters, numbers, «_» and «-».
                    The first character must be a letter. No spaces are allowed.
        :parameter field_type: Field type Possible options:
                            (string — string, text — one or more strings, number — integer or number with decimal point
                            date — date (the DD.MM.YYYY, DD-MM-YYYY, YYYY.MM.DD, YYYY-MM-DD format is supported)
                            bool — 1/0, yes/no
                            )
        :parameter public_name: Field name.
                                If it is not used, an automatical generation by the «name» field will take place.

        :return: Identifier field_id
        """
        result = self.get_request(method='createField', data={'name': name, 'type': field_type, 'public_name': public_name})
        return int(result.get('id'))

    def update_field(self, field_id: int, name: str, public_name: str = None) -> None:
        """It is a method to change user field parameters.

        :parameter field_id: Identifier field_id
        :parameter name: Field name. It must be unique and case insensitive.
                         Also, it is not recommended to create a field with the same name as the standard field names
                         (tags, email, phone, email_status, phone_status, etc.)
                         as the importContacts method will work incorrectly.
        :parameter public_name: Field name. Name of the «variable for substitution».
                                field in the personal account.
                                If it is not used, an automatically generation by the «name» field will take place.
                                Admissible characters: Latin letters, numbers, «_» and «-».
                                The first character must be a letter. No spaces are allowed.
        """
        self.get_request(method='updateField', data={'id': field_id, 'name': name, 'public_name': public_name})

    def delete_field(self, field_id: int) -> None:
        """It is a method to delete a user field.

           :parameter field_id: Identifier field_id
        """
        self.get_request(method='deleteField', data={'id': field_id})

    def get_fields(self) -> list:
        """Array, each array element is an object with the id, name, type, is_visible and view_pos fields.

        """
        return self.get_request(method='getFields')

    def subscribe(self, list_ids: list, fields: dict, double_optin: int = 3, overwrite: int = 0) -> int:
        """This method adds contacts (email address and/or mobile phone numbers) of the contact to one or several lists,
            and also allows you to add/change values of additional fields and tags.

            :parameter list_ids: List codes separated by comma in which a contact is to be added.
            :parameter fields: Dictionaries of additional fields.
            :parameter double_optin: It obtains the value of 0, 3, or 4. (3 by default)
                                    (see https://www.unisender.com/en/support/api/partners/subscribe/)
            :parameter overwrite: Field and tag rewriting mode, the number from 0 to 2 (0 by default).
                                  It sets what needs to be done in case of existence of a contact
                                  (the contact is identified by the email address and/or phone number).
            :return: Identifier person
        """
        if list_ids:
            list_ids = ",".join(map(str, list_ids))

        data = {'list_ids': list_ids, 'double_optin': double_optin, 'overwrite': overwrite}
        for key, value in fields.items():
            data[key] = value

        result = self.get_request(method='subscribe', data=data)
        return int(result.get('person_id'))

    def exclude(self, contact_type: str, contact: str, list_ids: list = None) -> None:
        """The method excludes the contact’s email or phone number from one or several lists.

           :parameter contact_type: The type of the contact to be excluded is either ’email’ or ‘phone’
           :parameter contact: Email or phone being excluded
           :parameter list_ids: List codes separated by comma from which contacts are being excluded.
                                If it is not specified, contacts will be excluded from all lists.
        """
        if list_ids:
            list_ids = ",".join(map(str, list_ids))

        self.get_request(
            method='exclude',
            data={
                'contact_type': contact_type,
                'contact': contact,
                'list_ids': list_ids,
            }
        )


    #def get_email(self):