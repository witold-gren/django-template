import pytest


class TestUserQuery:
    query = """
    { 
        getUsers {
            id
            username
        }
    }
    """

    @pytest.mark.django_db
    def test_get_users_query(self, gql_client, user_factory):
        users = user_factory.create_batch(5)
        result = gql_client().execute(self.query)
        assert "errors" not in result
        assert len(result["data"]["getUsers"]) == len(users)

    @pytest.mark.django_db
    def test_get_user_query(self, gql_client, user_factory):
        users = user_factory.create_batch(5)
        query = f"""
        {{ '{{' }}
            getUser(username: \"{users[0].username}\") {{ '{{' }}
                id
                email
            {{ '}}' }}
        {{ '}}' }}
        """

        result = gql_client().execute(query)
        assert "errors" not in result
        assert result["data"]["getUser"]["email"] == users[0].email
