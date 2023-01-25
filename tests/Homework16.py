import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import pytest


class TestUserEditNegativeCheck(BaseCase):
    user1_email = ""
    user1_password = ""
    user1_id = 0

    user2_email = ""
    user2_password = ""
    user2_id = 0

    def setup_class(self):
        self.user1_email, self.user1_password, self.user1_id = self.create_new_user(self)
        self.user2_email, self.user2_password, self.user2_id = self.create_new_user(self)

    def test_user_just_create_edit_not_auth(self):
        data = self.prepare_registration_data()
        response = requests.put(f"https://playground.learnqa.ru/api/user/{self.user1_id}", data=data)
        Assertions.assert_cod_status(response, 400)

    def test_user_just_create_edit_other_user(self):
        new_data = self.prepare_registration_data()
        login_data = {
            'email': self.user1_email,
            'password': self.user1_password
        }

        response1 = requests.post('https://playground.learnqa.ru/api/user/login', data=login_data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_headers(response1, "x-csrf-token")
        response = requests.put(
            f"https://playground.learnqa.ru/api/user/{self.user2_id}",
            data=new_data,
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_cod_status(response, 400)

    data1 = [
        ('email', 'qwerty1234.mail.ru'),
        ('firstName', '1')
    ]

    @pytest.mark.parametrize('field_name,value', data1)
    def test_user_auth_wrong_parameters(self, field_name, value):
        new_data = self.prepare_registration_data()
        new_data[field_name] = value
        login_data = {
            'email': self.user2_email,
            'password': self.user2_password
        }

        response1 = requests.post('https://playground.learnqa.ru/api/user/login', data=login_data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_headers(response1, "x-csrf-token")
        user_from_auth = self.get_json_value(response1, "user_id")
        response = requests.put(
            f"https://playground.learnqa.ru/api/user/{user_from_auth}",
            data=new_data,
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_cod_status(response, 400)

