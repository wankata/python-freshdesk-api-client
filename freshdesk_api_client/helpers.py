import json
import requests

from . import settings


def post(subdomain: str, endpoint: str, data: dict) -> requests.Response:
    url = settings.API_URL.format(subdomain=subdomain, endpoint=endpoint)

    # Password may be anything, when we use authentication token
    authentication = requests.auth.HTTPBasicAuth(settings.AUTH_TOKEN, 'None')

    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, auth=authentication, headers=headers, data=json.dumps(data))

    response.raise_for_status()

    return response
