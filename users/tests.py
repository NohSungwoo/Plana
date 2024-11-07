from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class TestSignUp(APITestCase):

    NAME = "SignUp Test"
    URL = "/api/v1/users/signup/"

    def test_signup(self):
        # 정상 회원 가입 요청
        response = self.client.post(
            self.URL,
            data={
                "email": "tester@test.com",
                "password": "123test",
                "nickname": "digimon",
                "gender": "male",
                "birthday": "1995-08-17",
            },
        )

        data = response.json()

        self.assertEqual(response.status_code, 201, "Status code isn't 201")
        self.assertEqual(data["email"], "tester@test.com")
        self.assertEqual(data["nickname"], "digimon")
        self.assertEqual(data["gender"], "male")
        self.assertEqual(data["birthday"], "1995-08-17")

    def test_need_password(self):
        # password 가 없는 경우
        response = self.client.post(
            self.URL,
            data={
                "email": "tester@test.com",
                "nickname": "digimon",
                "gender": "male",
                "birthday": "1995-08-17",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_serializer_data(self):

        response = self.client.post(
            self.URL,
            data={
                "email": "invalid-email-format",  # 실패
                "password": "123",
                "nickname": "ash",
                "gender": "unknown",  # 실패
                "birthday": "invalid-date-format",  # 실패
            },
        )

        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(data["email"], ["Enter a valid email address."])
        self.assertEqual(data["gender"], ['"unknown" is not a valid choice.'])
        self.assertEqual(
            data["birthday"],
            ["Date has wrong format. Use one of these formats instead: YYYY-MM-DD."],
        )


class TestLogin(APITestCase):

    URL = "/api/v1/users/login/"

    def setUp(self):
        user = User.objects.create(email="tester@naver.com", birthday="1995-08-17")
        user.set_password("123123")
        user.save()

    def test_login(self):
        # 정상 로그인 요청
        response = self.client.post(
            self.URL, data={"email": "tester@naver.com", "password": "123123"}
        )
        data = response.json()

        self.assertEqual(
            response.status_code, status.HTTP_200_OK, {"login data invalid"}
        )
        self.assertEqual(data["email"], "tester@naver.com", "email value error")

    def test_missing_data(self):
        # 값이 누락된 경우
        response = self.client.post(self.URL, data={"email": "unknown"})
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(data, {"detail": "Missing data"})

    def test_invalid_data(self):
        # 값이 잘못된 경우
        response = self.client.post(
            self.URL, data={"email": "tester", "password": "1212"}
        )
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(data, {"detail": "It's not valid"})
