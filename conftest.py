from pytest_factoryboy import register

from factories import AdsFactory, UserFactory

pytest_plugins = "tests.fixtures"

register(UserFactory)
register(AdsFactory)
