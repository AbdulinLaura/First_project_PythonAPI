import requests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserAuth(BaseCase):
    exclude_params = [
        ("no_cookie"), ("no token")
    ]
    def setup_method(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        self.response1 = requests.post('https://playground.learnqa.ru/api/user/login', data=data)

        self.auth_sid = self.get_cookie(self.response1, "auth_sid")
        self.token = self.get_headers(self.response1, "x-csrf-token")
        self.user_from_auth = self.get_json_value(self.response1, "user_id")

    def test_user_auth(self):
        response2 = requests.get(
            "https://playground.learnqa.ru/api/user/auth",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )
        Assertions.assert_json_value_by_name(
            response2,
            "user_id",
            self.user_from_auth,
            "User id from auth method is not equal to user id from check method"
        )


    @pytest.mark.parametrize('condition', exclude_params)
    def test_negativ_auth_check(self, condition):
        auth_sid = self.response1.cookies.get("auth_sid")
        token = self.response1.headers.get("x-csrf-token")
        if condition == "no_cookie":
            response2 = requests.get(
            "https://playground.learnqa.ru/api/user/auth", headers={"x-csrf-token": token}
            )
        else:
            response2 = requests.get(
            "https://playground.learnqa.ru/api/user/auth", cookies= {"auth_sid":auth_sid}
            )
        Assertions.assert_json_value_by_name(
            response2,
            "user_id",
            0,
            f"User is authorised with condition {condition}"
        )