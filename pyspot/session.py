import requests

from .api_timer import ApiTimer


class Session(object):
    """
    Session handler for an API

    Creates a new access_token and tracks its lifespan,
    refreshing if it runs out
    """

    header_key = 'headers'
    access_token_key = 'Authorization'
    url_key = 'url'

    def __init__(
            self, base_url: str, auth_token,
            auto_base: bool = True,
            version: int = 1,
            api_timer: ApiTimer=None
    ):

        self._auth = auth_token

        self.base_url = base_url
        self.auto_base = auto_base
        self.version = version
        self.api_timer = api_timer

        self.rest_base = "{}".format(self.base_url)

    @property
    def auth(self):

        if self._auth.expired:
            self._auth.refresh_auth_token()

        return self._auth

    @property
    def auth_header(self):
        return self.auth.header

    def _http_request(self, url, *args, **kwargs):

        if self.api_timer:
            self.api_timer.check_request()

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
