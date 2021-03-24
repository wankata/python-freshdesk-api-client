# Python Freshdesk API Client

This is a simple API client for Freshdesk, written in Python.

The client implements **v2** of the API.


## Setup

The Freshdesk API Client works with token authentication.
To use methods, requiring authentication, provide a token as environment variable `FRESHDESK_TOKEN`


## General Usage

The Freshdesk API Client defines model classes for each data type, which cover the response json.

The model classes don't allow you to assign attributes, not defined in the model, so they try to
protect you from typos.

The attributes follow 1:1 the json attribute names, provided by Freshdesk.


## contacts module


### general usage

`from freshdesk_api_client import contacts`


### create_contact()

`contacts.create_contact(subdomain: str, contact: dict) -> Contact`

[Freshdesk documentation](https://developers.freshdesk.com/api/#create_contact)

The method does require authentication.

It raises FreshdeskClientError or subclass of it on anything but 201 OK.

It returns contacts.Contact instance.

NB!: `'preferred_source'`, `'facebook_id'`, `'csat_rating'` are **UNDOCUMENTED** attributes,
returned by Freshdesk. The Contact model contains those attributes, but they shouldn't be provided
to create_contact's contact dictionary

The contact dictionary may contain everything from contacts.Contact, except:
- active
- deleted
- id
- created_at
- updated_at,
- preferred_source
- facebook_id
- csat_rating

For further details on required fields etc., please check the [Freshdesk
documentation](https://developers.freshdesk.com/api/#create_contact)

The contacts.Contact instance, returned by create_contact() includes the following attributes:
- active
- address
- avatar
- company_id
- view_all_tickets,
- custom_fields
- deleted
- description
- email
- id
- job_title,
- language
- mobile
- name
- other_emails
- phone
- tags,
- time_zone
- twitter_id
- unique_external_id
- other_companies,
- created_at
- updated_at,
- preferred_source
- facebook_id
- csat_rating


## TODOs:
- Validate post data against required fields
- Implement avatar upload
- Implement Rate limits


## For developers only

If you want to patch something, play around, run the tests, just follow the instructions below.

## Prerequisites

You need to have [Docker CE](https://docs.docker.com/install/ "Install Docker CE") and [Docker
Compose](https://docs.docker.com/compose/install/ "Install Docker Compose") installed.

If your environment is other than GNU/Linux, there may be some differences in the interaction with
Docker, so please follow the [Docker documentation](https://docs.docker.com/ "Docker documentation")
if something doesn't suits you.


## Setup Local Docker Environment

Under `environment/` you'll find all the configuration files, you need to run the
project on docker.

To prepare your environment, you need to cd `./environment` and:
- Sync the `.env.tmpl` file to `.env` and modify it if needed.
- run `$ docker-compose up --build`

That's all!

## Utility scripts

To run all the linters and tests, you need to:
  - `$ cd environment`
  - `$ docker-compose exec app bash -c "./run_checks.py --help"`


## Basic conventions

To keep things clean, we use:
- [gitlint](https://jorisroovers.com/gitlint/ "gitlint documentation") to keep eye on our commit
  messages. See the .gitlint file for our custom rules.
- [flake8](https://flake8.pycqa.org/en/latest/index.html "flake8 documentation") to keep our code
  clean. See the .flake8 file for our custom rules.
- [mypy](https://mypy.readthedocs.io/en/stable/ "mypy documentation") to check our types statically.
