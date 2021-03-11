class TestUser:
    def test_string_representation(self, user_instance):
        assert str(user_instance) == user_instance.username
    {%- if cookiecutter.use_django_rest_framework == 'n' %}

    def test_get_absolute_url(self, user_instance):
        assert user_instance.get_absolute_url() == f"/users/{user_instance.username}/"
    {%- endif %}
