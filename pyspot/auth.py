import datetime


class Auth(object):
    """
    Models an OAuth 2.0 token
    """

    # Subtract buffer from expiration limit when calculating the expiration time
    # to prevent letting the token expire because of network time losses
    buffer_time = 60

    def __init__(self, access_token: str, token_type: str, expires_in: int,
                 scope: str):
        self.access_token = access_token
        self.token_type = token_type
        self.expires_in = expires_in
        self.scope = scope
        self.type = 'Bearer'

        if self.expires_in <= self.buffer_time:
            raise ValueError(
                ("The token expires in less time than the "
                 "buffer time.\nBuffer: {}\nexpires_in: {}".format(
                    self.buffer_time, self.expires_in)))

        self.created_at = datetime.datetime.now()

        self.expires_at = self.created_at - datetime.timedelta(
            seconds=(self.expires_in - self.buffer_time)
        )

    def expired(self):
        """
        Checks if the auth token is expired or not

        :return: (Bool) True if expired, False if not
        """
        return self.expires_at > datetime.datetime.now()
