import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import pytest
import random
import string


class TestUserRegister(BaseCase):
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

    def generate_random_string(self, length):
        letters = string.ascii_lowercase
        rand_string = ''.join(random.choice(letters) for i in range(length))
        return rand_string

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_cod_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @pytest.mark.parametrize('password,username,first_name,last_name,email,error', data1)
    def test_create_user_without_one_parametrize(self, password, username, first_name, last_name, email, error):
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

    def test_create_user_without_at(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email)

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_cod_status(response, 400)
        assert response.text == "Invalid email format", f"{email}-error has not been appeared"

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_cod_status(response, 400)
        assert response.content.decode(
            'utf-8') == f"Users with email '{email}' already exists", f"Unexpected response.content '{response.content}'"
