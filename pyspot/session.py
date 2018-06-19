import requests

from .auth import Auth


class Session(object):
    """
    Session handler for an API

    Creates a new access_token and tracks its lifespan,
    refreshing if it runs out
    """

    refresh_token_url = "oauth/v1/token"
    header_key = 'headers'
    access_token_key = 'Authorization'
    url_key = 'url'
    grant_type = 'authorization_code'

    def __init__(self, base_url: str, auth_token,
                 auto_base: bool = True,
                 version: int = 1):

        self._auth = auth_token

        self.base_url = base_url
        self.auto_base = auto_base

        self.rest_base = "{}/rest/v{}".format(self.base_url, version)

    @property
    def auth(self):

        if self._auth.expired:
            self._auth.refresh_auth_token()

        return self._auth

    @property
    def auth_header(self):
        return "{} {}".format(self.auth.header_type, self.auth.access_token)

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
