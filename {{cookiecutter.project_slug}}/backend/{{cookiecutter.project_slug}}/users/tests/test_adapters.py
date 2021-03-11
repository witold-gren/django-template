from django.test import override_settings

from {{cookiecutter.project_slug}}.users import adapters


class TestAdapters:
    @override_settings(ACCOUNT_ALLOW_REGISTRATION=False)
    def test_is_open_for_signup_in_accountadapter_when_set_settings(self, rf):
        signup = adapters.AccountAdapter().is_open_for_signup(rf)
        assert signup is False

    @override_settings()
    def test_is_open_for_signup_in_accountadapter_when_not_set_settings(
        self, rf, settings
    ):
        del settings.ACCOUNT_ALLOW_REGISTRATION
        signup = adapters.AccountAdapter().is_open_for_signup(rf)
        assert signup is True

    @override_settings(ACCOUNT_ALLOW_REGISTRATION=False)
    def test_is_open_for_signup_in_socialaccountadapter_when_set_settings(self, rf):
        signup = adapters.SocialAccountAdapter().is_open_for_signup(rf, True)
        assert signup is False

    @override_settings()
    def test_is_open_for_signup_in_socialaccountadapter_when_not_set_settings(
        self, rf, settings
    ):
        del settings.ACCOUNT_ALLOW_REGISTRATION
        signup = adapters.SocialAccountAdapter().is_open_for_signup(rf, True)
        assert signup is True
