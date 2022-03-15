import pytest
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ErrorDetail

from ads.models import Ads
from factories import AdsFactory

User = get_user_model()

from auth_user.models import Profile
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
def test_ad_create(client, user_login_token):
    expected_response = {
        "name": "test_create_ad",
        "author": "Павел",
        "author_id": 1,
        "price": 50,
        "description": "Твердый переплет, состояние прекрасное. По всем вопросам лучше писать, звонок могу не услышать. Передам у м. Студенческая.",
        "address": "Москва, м. Студенческая",
        "is_published": False,
        "poster": None,
        "category_id": None
    }
    response = client.post('/user/register/', {
        "username": "test",
        "password": "test",
        "birth_date": "2006-04-25",
        "email": "shatilovvlad@ya.ru"
    }, format='json')
    assert response.status_code == 400  # because i already create him via fixtures

    response = client.post('/ad/create/', {
        "name": "test_create_ad",
        "author": "Павел",
        "price": 50,
        "description": "Твердый переплет, состояние прекрасное. По всем вопросам лучше писать, звонок могу не услышать. Передам у м. Студенческая.",
        "address": "Москва, м. Студенческая",
        "is_published": True
    }, content_type='application/json', HTTP_AUTHORIZATION="Bearer " + user_login_token['access'])

    assert expected_response == response.data

    response_bad = client.post('/ad/create/', {
        "name": "test_create_ad",
        "author": "Павел",
        "price": 50,
        "description": "Твердый переплет, состояние прекрасное. По всем вопросам лучше писать, звонок могу не услышать. Передам у м. Студенческая.",
        "address": "Москва, м. Студенческая",
        "is_published": True
    }, content_type='application/json')
    expected_bad_response = {'detail': ErrorDetail(string='Authentication credentials were not provided.', code='not_authenticated')}
    assert expected_bad_response == response_bad.data



@pytest.mark.django_db
def test_selection_create_and_get_one(client):
    ads2 = AdsFactory.create_batch(5)
    expected_response = {
        "id": 1,
        "name": "test",
        "items": [
            2, 3, 4
        ],
        "owner": 2
    }

    user = Profile.objects.first()
    # a = SlidingToken.for_user(user)
    # a2 = RefreshToken.for_user(user)
    # a3 = str(RefreshToken.for_user(user))
    access_token_for_first_user = str(RefreshToken.for_user(user).access_token)

    response = client.post('/selection/create/', {
        "items": [2, 3, 4],
        "name": "test"
    }, content_type='application/json', HTTP_AUTHORIZATION="Bearer " + access_token_for_first_user)
    assert response.status_code == 201
    resp_check = client.get('/ad/', format='json')
    user_check = client.get('/user/', format='json')
    test = resp_check.data
    assert expected_response == response.data



    detail_ad = client.get('/ad/2/', format='json', HTTP_AUTHORIZATION="Bearer " + access_token_for_first_user)
    ad = Ads.objects.get(pk=2)
    exp_ans = {
        "id": 2,
        "name": "fixture_name",
        "author": "Author_fix",
        "author_id": 2,
        "price": 69,
        "description": "Fixture_description.",
        "address": "TORONTOTOKYO",
        "is_published": True,
        "poster": None,
        "category_id": None
    }
    assert exp_ans == detail_ad.data



@pytest.mark.django_db
def test_ad_create2(client, user_login_token):
    expected_response = {
        "name": "test_create_ad",
        "author": "Павел",
        "author_id": 7,
        "price": 50,
        "description": "Твердый переплет, состояние прекрасное. По всем вопросам лучше писать, звонок могу не услышать. Передам у м. Студенческая.",
        "address": "Москва, м. Студенческая",
        "is_published": False,
        "poster": None,
        "category_id": None
    }
    response = client.post('/user/register/', {
        "username": "test",
        "password": "test",
        "birth_date": "2006-04-25",
        "email": "shatilovvlad@ya.ru"
    }, format='json')

    response = client.post('/ad/create/', {
        "name": "test_create_ad",
        "author": "Павел",
        "price": 50,
        "description": "Твердый переплет, состояние прекрасное. По всем вопросам лучше писать, звонок могу не услышать. Передам у м. Студенческая.",
        "address": "Москва, м. Студенческая",
        "is_published": True
    }, content_type='application/json', HTTP_AUTHORIZATION="Bearer " + user_login_token['access'])
    assert response.status_code == 201
    assert expected_response == response.data


@pytest.mark.django_db
def test_ads_get(client, user_login_token):
    exp_res = {
        "count": 0,
        "next": None,
        "previous": None,
        "results": []
    }
    response = client.get('/ad/')

    assert response.status_code == 200
    assert exp_res == response.data

def test_b():
    assert True
