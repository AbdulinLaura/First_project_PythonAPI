import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime
import pytest


class TestUserRegister2(BaseCase):
    email = 'vinkotov@example.com'
    data1 = [
        ({'password': ''}, {'username': 'learnqa'}, {'firstName': 'learnqa'}, {'lastName': 'learnqa'}, {'email': email},
         'password'),
        ({'password': '123'}, {'username': ''}, {'firstName': 'learnqa'}, {'lastName': 'learnqa'}, {'email': email},
         'username'),
        ({'password': '123'}, {'username': 'learnqa'}, {'firstName': ''}, {'lastName': 'learnqa'}, {'email': email},
         'firstName'),
        ({'password': '123'}, {'username': 'learnqa'}, {'firstName': 'learnqa'}, {'lastName': ''}, {'email': email},
         'lastName'),
        ({'password': '123'}, {'username': 'learnqa'}, {'firstName': 'learnqa'}, {'lastName': 'learnqa'}, {'email': ''},
         'email')
    ]

    user_name1 = [
        ("Р"),
        ("Q'"),
        ("1"),
        ("@"),
        (" ")
    ]

    user_name2 = [
        (249, 200),
        (250, 200),
        (251, 400),
        (300, 400)
    ]

    def setup_method(self):
        self.base_part = 'learnqa'
        self.domain = 'example.com'
        self.random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        self.email = f"{str(self.base_part)}{self.random_part}@{self.domain}"

    @pytest.mark.parametrize('password,username,first_name,last_name,email,error', data1)
    def test_user_without_one_parametrize(self, password, username, first_name, last_name, email, error):
        data = {
            'password': password["password"],
            'username': username["username"],
            'firstName': first_name["firstName"],
            'lastName': last_name["lastName"],
            'email': email["email"]
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_cod_status(response, 400)
        assert response.text == f"The value of '{error}' field is too short"

    def test_user1_without_at(self):
        email = f"{str(self.base_part)}{self.random_part}{self.domain}"
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_cod_status(response, 400)
        assert response.text == "Invalid email format", f"{email}-error has not been appeared"

    @pytest.mark.parametrize('username', user_name1)
    def test_user2_with_short_name(self, username):
        data = {
            'password': '123',
            'username': username,
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        print(response.text)

        Assertions.assert_cod_status(response, 400)
        assert response.text == "The value of 'username' field is too short", f"{username} error has not been appeared"

    @pytest.mark.parametrize('username_length,expected_status_code', user_name2)
    def test_create_user_with_name_more_normal_value(self, username_length, expected_status_code):
        user_name = self.generate_random_string(username_length)
        data = {
            'password': '123',
            'username': user_name,
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }

        print(user_name)
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_cod_status(response, expected_status_code)
