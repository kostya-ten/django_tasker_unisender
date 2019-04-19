import os

import requests
from django.conf import settings


def get_request(method: str = None, data: dict = None) -> object:
    url = "{url}/{method}".format(url="https://api.unisender.com/ru/api", method=method)
    api_key = getattr(settings, 'UNISENDER_API_KEY', os.environ.get('UNISENDER_API_KEY'))

    if data:
        data = {**data, **{'format': 'json', 'api_key': api_key, 'platform': 'Django module django_tasker_unisender'}}
    else:
        data = {'format': 'json', 'api_key': api_key, 'platform': 'Django module django_tasker_unisender'}

    response = requests.request(method='POST', url=url, data=data)

    json = response.json()
    if json.get('error'):
        raise requests.HTTPError("Unisender error: {error}".format(error=json.get('error')))
    return json.get('result')


# Lists
def create_list(title: str = None) -> int:
    """
    Checks the validity of a mobile phone number.

    :param title: List name. It must be unique in your account.
    :returns: Identifier campaign list
    """
    result = get_request(method='createList', data={'title': title})
    return result.get('id')


def get_lists() -> list:
    """
    It is a method to get the list of all available campaign lists.

    :returns: Array, each array element is an object dict with the following id and title fields.
    """
    return get_request(method='getLists')


def delete_list(list_id: int = None) -> None:
    """
     It is a method to delete a list.

     :param list_id: Identifier campaign list
     """
    get_request(method='deleteList', data={'list_id': list_id})


def update_list(list_id: int = None, title: str = None) -> None:
    get_request(method='updateList', data={'list_id': list_id, 'title': title})


# Fields
def create_field(name: str = None, field_type: str = None, public_name: str = None) -> int:
    result = get_request(method='createField', data={'name': name, 'type': field_type, 'public_name': public_name})
    return int(result.get('id'))


def update_field(field_id: int = None, name: str = None, public_name: str = None) -> None:
    get_request(method='updateField', data={'id': field_id, 'name': name, 'public_name': public_name})


def delete_field(field_id: int = None) -> None:
    get_request(method='deleteField', data={'id': field_id})


def subscribe(list_ids: int = None, fields: dict = None, double_optin: int = 3, overwrite: int = 1) -> int:
    data = {'list_ids': list_ids, 'double_optin': double_optin, 'overwrite': overwrite}
    for key, value in fields.items():
        data[key] = value

    result = get_request(method='subscribe', data=data)
    return int(result.get('person_id'))
