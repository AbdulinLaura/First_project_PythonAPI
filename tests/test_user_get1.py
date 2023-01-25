import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserGet(BaseCase):

    user1_email = ""
    user1_password = ""
    user1_id = 0

    user2_email = ""
    user2_password = ""
    user2_id = 0

    def setup_class(self):
        self.user1_email, self.user1_password, self.user1_id = self.create_new_user(self)
        self.user2_email, self.user2_password, self.user2_id = self.create_new_user(self)

    def test_get_user_details_not_auth(self):
        response = requests.get(f"https://playground.learnqa.ru/api/user/{self.user1_id}")

        expected_fields = ["email", "firstName", "lastName"]
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_keys(response, expected_fields)

    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': self.user1_email,
            'password': self.user1_password
        }

        response1 = requests.post('https://playground.learnqa.ru/api/user/login', data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_headers(response1, "x-csrf-token")
        user_from_auth = self.get_json_value(response1, "user_id")
        response2 = requests.get(
            "https://playground.learnqa.ru/api/user/" + str(user_from_auth),
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    def test_get_user_details_auth_other_user(self):
        data = {
            'email': self.user1_email,
            'password': self.user1_password
        }

        response1 = requests.post('https://playground.learnqa.ru/api/user/login', data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_headers(response1, "x-csrf-token")

        response2 = requests.get(
            f"https://playground.learnqa.ru/api/user/{self.user2_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        expected_fields = ["email", "firstName", "lastName"]
        Assertions.assert_json_has_key(response2, "username")
        Assertions.assert_json_has_not_keys(response2, expected_fields)

