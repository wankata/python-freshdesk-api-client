import requests_mock

from unittest import TestCase
from ..contacts import Contact, create_contact
from .. import exceptions as e
from .. import settings


class ContactModelTests(TestCase):
    def test_initialize_empty_contact_creates_instance(self):
        contact = Contact()
        self.assertIsInstance(contact, Contact)

    def test_initialize_empty_contact_creates_instance_without_attrs(self):
        contact = Contact()
        for missing in Contact.__slots__:
            with self.assertRaises(AttributeError):
                getattr(contact, missing)

    def test_initialize_with_invalid_attrs_raises_exception(self):
        with self.assertRaises(AttributeError):
            Contact({'invalid_attribute': 'value'})

    def test_assign_invalid_attrs_raises_exception(self):
        contact = Contact()
        with self.assertRaises(AttributeError):
            contact.invalid_attribute = 'value'

    def test_initialize_with_valid_attrs_sets_them_ok(self):
        contact = Contact({'name': 'ivan', 'id': 5})
        self.assertEqual(contact.name, 'ivan')
        self.assertEqual(contact.id, 5)

    def test_assign_valid_attrs_sets_them_ok(self):
        contact = Contact()
        contact.name = 'ivan'
        contact.id = 5
        self.assertEqual(contact.name, 'ivan')
        self.assertEqual(contact.id, 5)

    def test_initialize_with_valid_attrs_do_not_touch_the_other_attrs(self):
        contact_dict = {'name': 'ivan', 'id': 5}
        contact = Contact(contact_dict)

        for attr in Contact.__slots__:
            if attr not in contact_dict.keys():
                with self.subTest(attr=attr):
                    with self.assertRaises(AttributeError):
                        getattr(contact, attr)

    def test_assign_valid_attrs_do_not_touch_the_other_attrs(self):
        contact = Contact()
        contact.name = 'ivan'
        contact.id = 5

        for attr in Contact.__slots__:
            if attr not in ['name', 'id']:
                with self.subTest(attr=attr):
                    with self.assertRaises(AttributeError):
                        getattr(contact, attr)


@requests_mock.Mocker()
class CreateContactTests(TestCase):
    def test_create_contact_returns_correct_instance_and_data(self, mock):
        mock.post(settings.API_URL.format(subdomain='subdomain', endpoint='/contacts'),
                  json=_CONTACT_JSON, status_code=201)
        contact = create_contact('subdomain', {'name': 'ivan', 'email': 'email@domain.com'})

        self.assertIsInstance(contact, Contact)
        self.assertEqual(contact.name, 'ivan')
        self.assertEqual(contact.email, 'email@domain.com')

    def test_create_contact_raises_unsupported_status_exception_on_302(self, mock):
        mock.post(settings.API_URL.format(subdomain='subdomain', endpoint='/contacts'),
                  status_code=302)

        with self.assertRaises(e.UnsupportedResponseStatus):
            create_contact('subdomain', {})

    def test_create_contact_raises_freshdesk_client_error_on_500(self, mock):
        mock.post(settings.API_URL.format(subdomain='subdomain', endpoint='/contacts'),
                  status_code=500)

        with self.assertRaises(e.FreshdeskClientError):
            create_contact('subdomain', {})


_CONTACT_JSON: dict = {'active': False, 'address': None, 'company_id': None, 'view_all_tickets':
                       None, 'deleted': False, 'description': None, 'email': 'email@domain.com',
                       'id': 80013181750, 'job_title': None, 'language': 'en', 'mobile': None,
                       'name': 'ivan', 'phone': None, 'time_zone': 'Eastern Time (US & Canada)',
                       'twitter_id': None, 'custom_fields': {}, 'tags': [], 'other_emails': [],
                       'facebook_id': None, 'created_at': '2021-03-24T12:52:00Z', 'updated_at':
                       '2021-03-24T12:52:00Z', 'csat_rating': None, 'preferred_source': None,
                       'other_companies': [], 'unique_external_id': None, 'avatar': None}
