import graphene

from {{cookiecutter.project_slug}}.users.schema import UsersQuery


class Query(graphene.ObjectType, UsersQuery):
    """
    This class will inherit from multiple Queries
    as we begin to add more apps to our project.

    See: https://docs.graphene-python.org/projects/django/en/latest/tutorial-plain/
    """


schema = graphene.Schema(query=Query)
