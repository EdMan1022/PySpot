import datetime

import requests

from .auth import Auth


class UserAuth(Auth):
    """
    Models OAuth 2.0 token where refresh tokens are used to get a new auth token
    """

    # Subtract buffer from expiration limit when calculating the expiration time
    # to prevent letting the token expire because of network time losses
    buffer_time = 60

    def __init__(self, client_id, client_secret, redirect_uri, token,
                 refresh_url, grant_type='refresh_token', header_type='Bearer'):
        """

        :param client_id:
        :param client_secret:
        :param redirect_uri:
        :param token: Database ORM, must have commit method implemented on it
        :param refresh_url: URL hit to perform token refresh
        :param grant_type:
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.token = token
        self.refresh_url = refresh_url
        self.grant_type = grant_type
        self.header_type = header_type

    @property
    def expires_in(self):
        return self.token.expires_in

    @property
    def expires_at(self):
        return (datetime.datetime.now() + datetime.timedelta(
            self.expires_in - self.buffer_time))

    def _refresh_request(self):
        return requests.post(
            self.refresh_url,
            data={
                "grant_type": self.grant_type,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "redirect_uri": self.redirect_uri,
                "refresh_token": self.token.refresh_token
            })

    def refresh_auth_token(self):
        response = self._refresh_request()
        response_data = response.json()

        self.token.access_token = response_data['access_token']
        self.token.refresh_token = response_data['refresh_token']
        self.token.expires_in = response_data['expires_in']
        self.token.commit()

    @property
    def header(self):
        return "{} {}".format(self.header_type, self.token.access_token)
