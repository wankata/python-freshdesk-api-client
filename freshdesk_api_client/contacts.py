import requests

from requests.exceptions import HTTPError
from . import exceptions as e
from .helpers import post


class Contact:
    """
    Contact model

     A contact is a customer or a potential customer who has raised a support ticket through any
     channel.

     Read more on: https://developers.freshdesk.com/api/#contacts

     NB! 'preferred_source', 'facebook_id', 'csat_rating' are *UNDOCUMENTED* attributes!
     They are present in the returned Contact object, but should *not* be provided to create_contact
    """

    __slots__ = frozenset(('active', 'address', 'avatar', 'company_id', 'view_all_tickets',
                           'custom_fields', 'deleted', 'description', 'email', 'id', 'job_title',
                           'language', 'mobile', 'name', 'other_emails', 'phone', 'tags',
                           'time_zone', 'twitter_id', 'unique_external_id', 'other_companies',
                           'created_at', 'updated_at',
                           'preferred_source', 'facebook_id', 'csat_rating'))

    def __init__(self, initial: dict = None) -> None:
        """
        NB!: Non-allowed attributes raise AttributeError
        """

        if initial is None:
            initial = {}

        for attr, val in initial.items():
            setattr(self, attr, val)


def create_contact(subdomain: str, contact: dict) -> Contact:
    """
    https://developers.freshdesk.com/api/#create_contact
    """

    url = '/contacts'

    _validate_contact(contact)

    try:
        response: requests.Response = post(subdomain, url, data=contact)
    except HTTPError as exc:
        raise e.FreshdeskClientError from exc

    if response.status_code == 201:
        return Contact(response.json())
    else:
        raise e.UnsupportedResponseStatus(response.status_code)


def _validate_contact(contact: dict) -> None:
    excluded_attrs = {'active', 'deleted', 'id', 'created_at', 'updated_at',
                      'preferred_source', 'facebook_id', 'csat_rating'}
    valid_attrs = Contact.__slots__ - excluded_attrs
    post_params = set(contact)

    if not post_params.issubset(valid_attrs):
        raise e.InvalidPostParams(*(post_params - valid_attrs))
