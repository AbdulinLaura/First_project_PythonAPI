import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import pytest


class TestUserDelete(BaseCase):
    user1_email = ""
    user1_password = ""
    user1_id = 0

    user2_email = ""
    user2_password = ""
    user2_id = 0

    def setup_class(self):
        self.user1_email, self.user1_password, self.user1_id = self.create_new_user(self)
        self.user2_email, self.user2_password, self.user2_id = self.create_new_user(self)

    def test_remove_user1(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response = requests.post("https://playground.learnqa.ru/api/user/login", data=data)
        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_headers(response, "x-csrf-token")
        user_id = self.get_json_value(response, "user_id")

        response2 = requests.delete(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        assert response2.text == "Please, do not delete test users with ID 1, 2, 3, 4 or 5.", f"User with id {user_id} deleted"

        response3 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}
                                 )

        expected_fields = ["id", "username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response3, expected_fields)

    def test_remove_user2(self):
        data = self.prepare_registration_data()

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_cod_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

        email = data['email']
        password = data['password']
        user_id = self.get_json_value(response, "id")

        login_data = {
            'email': email,
            'password': password
        }

        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_headers(response2, "x-csrf-token")

        response3 = requests.delete(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_cod_status(response3, 200)

        response4 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}
                                 )

        print(response4.text)
        assert response4.text == "User not found", f"User {user_id} not deleted"
        expected_fields = ["id", "username", "email", "firstName", "lastName"]
        Assertions.assert_cod_status(response4, 404)

    def test_remove_other_user(self):
        data_user1 = {
            'email': self.user1_email,
            'password': self.user1_password
        }
        response = requests.post("https://playground.learnqa.ru/api/user/login", data=data_user1)
        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_headers(response, "x-csrf-token")

        response2 = requests.delete(
            f"https://playground.learnqa.ru/api/user/{self.user2_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        print(response2.status_code)




