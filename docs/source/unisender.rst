Low-level API Unisender
=======================

Usage::

    from django_tasker_unisender.unisender import Unisender

    unisender = Unisender(api_key="<< api key >>")
    lists = unisender.get_lists()
    print(lists)


.. autoclass:: django_tasker_unisender.unisender.Unisender
    :members:
