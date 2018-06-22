import datetime
from unittest import mock

from . import BaseTestClass

from pyspot import (
    Session,
    UserAuth,
    CredentialsAuth,
    ApiTimer
)


class BaseOAuthTest(BaseTestClass):

    def setUp(self):
        super(BaseOAuthTest, self).setUp()
        self.access_token = 'test'
        self.token_type = 'test'
        self.expires_in = 3599
        self.scope = 'test'

        self.test_base_url = 'test'
        self.test_identity_url = 'test'
        self.test_client_id = 'test'
        self.test_client_secret = 'test'
        self.test_redirect_uri = 'test'
        self.test_token = mock.MagicMock()
        self.test_refresh_url = 'test'


class TestSession(BaseOAuthTest):
    target_path = 'pyspot.session'

    def setUp(self):
        super(TestSession, self).setUp()
        self.requests_patch = self.create_patch('requests')

        self.mock_response = mock.MagicMock()
        self.requests_patch.get.return_value = self.mock_response
        self.expired_patch = self.create_patch('expired',
                                               path='pyspot.auth.Auth')
        self.auth_requests_patch = self.create_patch(
            'requests', path='pyspot.user_auth')

        self.auth = UserAuth(self.test_client_id, self.test_client_secret,
                             self.test_redirect_uri, self.test_token,
                             self.test_refresh_url)

        self.session = Session(
            self.test_base_url,
            self.auth,
        )

    def test_init(self):
        self.assertIsInstance(self.session, Session)

    def test_request(self):
        self.session.get('test')


class TestUserAuth(BaseOAuthTest):
    target_path = UserAuth.__module__

    def setUp(self):
        super(TestUserAuth, self).setUp()
        self.requests_patch = self.create_patch('requests')

    def test_init(self):
        UserAuth(self.test_client_id, self.test_client_secret,
                 self.test_redirect_uri, self.test_token, self.test_refresh_url)

    def test_refresh(self):
        user_auth = UserAuth(
            self.test_client_id, self.test_client_secret,
            self.test_redirect_uri, self.test_token, self.test_refresh_url
        )
        user_auth.refresh_auth_token()


class TestApiTimer(BaseTestClass):
    target_path = ApiTimer.__module__

    def setUp(self):
        self.sleep_patch = self.create_patch('time.sleep')

    def test_init(self):
        timer = ApiTimer(
            request_limit_n=10, request_limit_t=10,
            buffer_n=1, buffer_t=1, wait_buffer_t=1)

    def test_over_limit(self):
        """
        Tests that too many requests calls a sleep operation and resets counts
        :return:
        """
        request_n = 3
        timer = ApiTimer(request_limit_n=request_n - 1, request_limit_t=40,
                         buffer_n=0, buffer_t=0, wait_buffer_t=0)

        for i in range(request_n):
            timer.check_request()

        self.assertTrue(self.sleep_patch.called)
        self.assertTrue(timer.request_n < request_n)

    def test_not_over_limit(self):
        """
        Tests that requests under the limit don't trigger a sleep

        :return:
        """
        request_n = 3
        timer = ApiTimer(request_limit_n=request_n + 1, request_limit_t=40,
                         buffer_n=0, buffer_t=0, wait_buffer_t=0)

        for i in range(request_n):
            timer.check_request()

        self.assertFalse(self.sleep_patch.called)
        self.assertEqual(timer.request_n, request_n)

    def test_reset_limit(self):
        """
        Tests that reset behaves as expected by manually resetting
        :return:
        """

        timer = ApiTimer(request_limit_n=10, request_limit_t=40,
                         buffer_n=0, buffer_t=0, wait_buffer_t=0)
        check_time = datetime.datetime.now()
        timer.check_request()

        # Assert start time is before the check made above
        self.assertLess(timer.start_time, check_time)

        # Assert that the number of requests is greater than 0
        self.assertGreater(timer.request_n, 0)

        timer.reset_limit()

        # Assert start time is after the check made above (it has been reset)
        self.assertGreater(timer.start_time, check_time)

        # Assert that the request number is 0
        self.assertEqual(timer.request_n, 0)
