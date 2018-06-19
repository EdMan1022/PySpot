from unittest import mock

from . import BaseTestClass

from pyspot import (
    Session,
    UserAuth,
    CredentialsAuth
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

        self.session = Session(
            self.test_base_url,
            self.test_identity_url,
            self.test_client_id,
            self.test_client_secret
        )

    def test_init(self):
        self.assertIsInstance(self.session, Session)

    def test_refresh_auth_token(self):
        """
        Tests that refreshing the access token results in a new auth token,
        more recent than the old one

        :return:
        """
        self.mock_response.json = mock.MagicMock()
        self.mock_response.json.return_value = {
            "access_token": '1',
            "token_type": self.token_type,
            "expires_in": self.expires_in,
            "scope": self.scope
        }

        # Refresh first token
        self.session.refresh_auth_token()

        # Record token values
        old_token = self.session.auth

        # Change the mocked_response token value
        self.mock_response.json.return_value['access_token'] = '2'

        # Get a new token
        self.session.refresh_auth_token()
        new_token = self.session.auth

        # Assert the tokens are different
        self.assertNotEqual(new_token.access_token, old_token.access_token)

        # Assert that the old token was created before the new token
        self.assertLess(old_token.created_at, new_token.created_at)

        # Assert that the old token expires before the new token
        self.assertLess(old_token.expires_at, new_token.expires_at)


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


