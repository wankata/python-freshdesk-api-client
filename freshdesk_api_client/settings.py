import os


API_URL = 'https://{subdomain}.freshdesk.com/api/v2{endpoint}'
AUTH_TOKEN = os.getenv('FRESHDESK_TOKEN', '')
