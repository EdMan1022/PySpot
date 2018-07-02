import datetime

import requests

from .auth import Auth


class CredentialsAuth(Auth):
    """
    Class for handling oauth 2.0 flow where static credentials are used to
    refresh the authentication token
    """

    def __init__(self, client_id, client_secret, refresh_url,
                 header_type: str = 'Bearer',
                 grant_type: str = 'client_credentials'):

        self.grant_type = grant_type
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_url = refresh_url
        self.header_type = header_type

        self.access_token = None
        self.token_type = None
        self.expires_in = None
        self.scope = None

        self.expires_at = datetime.datetime.now()

    @property
    def refresh_params(self):
        """
        Set up the parameters needed to refresh the API token
        :return:
        """
        return {
            "grant_type": self.grant_type,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

    @property
    def header(self):
        return "{} {}".format(self.header_type, self.access_token)

    def refresh_auth_token(self):
        """
        GETs a fresh auth token using static account credentials

        Called when the session is initialized,
        and if the token reaches the end of its lifespan
        :return: None
        """

        # Use the requests package to make the refresh request
        auth_response = requests.get(
            url=self.refresh_url,
            params=self.refresh_params
        )

        auth_data = auth_response.json()

        # Set token values based on the request response
        self.access_token = auth_data['access_token']
        self.token_type = auth_data['token_type']
        self.expires_in = int(auth_data['expires_in'])
        self.scope = auth_data['scope']

        self.expires_at = (datetime.datetime.now() + datetime.timedelta(
            self.expires_in - self.buffer_time))
