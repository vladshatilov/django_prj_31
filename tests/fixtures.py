import pytest


@pytest.fixture
@pytest.mark.django_db
def user_login_token(client, django_user_model):
    django_user_model.objects.create_user(username="test", password="test", birth_date="2006-04-25",
                                          email="shatilovvlad@ya.ru")
    response = client.post('/user/token/', {
        "username": "test",
        "password": "test"
    }, format='json')
    return response.data
