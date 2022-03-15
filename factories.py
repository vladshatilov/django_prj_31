import factory.django

from ads.models import Ads
from auth_user.models import Profile
from main_avito import settings

# from django.contrib.auth import get_user_model
#
# User = get_user_model()
# from django.contrib.auth.models import User

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile #User #User #settings.AUTH_USER_MODEL

    # username = "vlad2"
    username = factory.Faker("name")
    password = "test"
    birth_date = "1964-01-25"
    email = "ayhout@ya.ru"


class AdsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ads

    name = "fixture_name"
    author = "Author_fix"
    price = 69
    description = "Fixture_description."
    address = "TORONTOTOKYO"
    is_published = True
    author_id = factory.SubFactory(UserFactory)
