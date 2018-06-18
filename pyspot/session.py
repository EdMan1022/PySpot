import requests

from .auth import Auth


class Session(object):
    """
    Session handler for an API

    Creates a new access_token and tracks its lifespan,
    refreshing if it runs out
    """

    refresh_token_url = "oauth/token"
    header_key = 'headers'
    access_token_key = 'Authorization'
    url_key = 'url'

    def __init__(self, base_url: str, identity_url: str, client_id: str,
                 client_secret: str, auto_base: bool=True, version: int=1):

        self._auth = None

        self.base_url = base_url
        self.identity_url = identity_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.auto_base = auto_base

        self.rest_base = "{}/rest/v{}".format(self.base_url, version)

    def refresh_auth_token(self):
        """
        GETs a fresh auth token from the HubSpot auth endpoint

        Called when the session is initialized,
        and if the token reaches the end of its lifespan
        :return: None
        """

        # Set up the parameters needed to refresh the API token
        auth_token_params = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        # Use the requests package to make the refresh request
        auth_response = requests.get(
            url="{}/{}".format(self.identity_url, self.refresh_token_url),
            params=auth_token_params
        )

        # Initialize a new Auth instance using the response
        self._auth = Auth(**auth_response.json())

    @property
    def auth(self):

        if not self._auth:
            self.refresh_auth_token()

        elif self._auth.expired():
            self.refresh_auth_token()

        return self._auth

    @property
    def auth_header(self):
        return "{} {}".format(self.auth.type, self.auth.access_token)

    def _http_request(self, url, *args, **kwargs):

        if self.auto_base:
            # If the passed url is missing a leading slash, add one
            if url[0] != '/':
                url = '/' + url

            updated_url = "{}{}".format(self.rest_base, url)
            kwargs[self.url_key] = updated_url
        else:
            kwargs[self.url_key] = url

        if kwargs.get(self.header_key):
            kwargs[self.header_key][self.access_token_key] = \
                self.auth_header
        else:
            kwargs[self.header_key] = \
                {self.access_token_key: self.auth_header}
        return args, kwargs

    def get(self, url, *args, **kwargs):
        args, kwargs = self._http_request(url, *args, **kwargs)
        return requests.get(*args, **kwargs)

    def post(self, url, *args, **kwargs):
        args, kwargs = self._http_request(url, *args, **kwargs)
        return requests.post(*args, **kwargs)

    def put(self, url, *args, **kwargs):
        args, kwargs = self._http_request(url, *args, **kwargs)
        return requests.put(*args, **kwargs)

    def delete(self, url, *args, **kwargs):
        args, kwargs = self._http_request(url, *args, **kwargs)
        return requests.delete(*args, **kwargs)
