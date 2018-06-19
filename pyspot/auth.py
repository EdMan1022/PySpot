import datetime


class Auth(object):
    """
    Models an OAuth 2.0 token
    """

    # Subtract buffer from expiration limit when calculating the expiration time
    # to prevent letting the token expire because of network time losses
    buffer_time = 60

    @property
    def expired(self):
        """
        Checks if the auth token is expired or not

        :return: (Bool) True if expired, False if not
        """
        return self.expires_at < datetime.datetime.now()
