import requests
from django.contrib.auth import get_user_model

ACCESS_TOKEN_URL = "https://github.com/login/oauth/access_token"
PROFILE_DATA_URL = "https://api.github.com/user?access_token={token}"

User = get_user_model()

CLIENT_ID = "65e2afa2b501c7f81b5d"
CLIENT_SECRET = "e5b60dbe3cfc4ac409958bae0f2c92023b52bca8"
REDIRECT_URI = "http://localhost:8080/login/github_callback"
ACCEPT_TYPE = ("application/json",)


class GithubOAuth2Authentication(object):
    def authenticate(self, code):
        payload = {
            "code": code,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
        }
        headers = {"Accept": ACCEPT_TYPE}
        response = requests.post(ACCESS_TOKEN_URL, params=payload, headers=headers)
        json = response.json()
        access_token = json["access_token"]
        try:
            return User.objects.get(token=access_token)
        except User.DoesNotExist:
            user_info = self.get_user_info(access_token)
            return User.objects.create(**user_info)

    def get_user_info(self, token):
        response = requests.post(PROFILE_DATA_URL.format(token=token))
        json = response.json()
        username = json["login"]
        password = User.objects.make_random_password(length=10)
        return {username: username, password: password, token: token}

    def get_user(self, token):
        try:
            return User.objects.get(token=token)
        except User.DoesNotExist:
            return None
