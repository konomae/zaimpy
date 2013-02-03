# coding: utf-8
import urlparse
import requests
from requests_oauthlib import OAuth1


# Zaim API ver 0.9.1
API_ROOT = "https://api.zaim.net/v1/"

request_token_url = API_ROOT + "auth/request"
authorize_url = "https://www.zaim.net/users/auth"
access_token_url = API_ROOT + "auth/access"


class Zaim(object):
    def __init__(self, consumer_key, consumer_secret, access_token_key=None, access_token_secret=None):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.set_access_token(access_token_key, access_token_secret)

    def set_access_token(self, access_token_key, access_token_secret):
        self.access_token_key = access_token_key
        self.access_token_secret = access_token_secret

    def get_request_token(self, callback_url=u"http://oob/"):
        auth = OAuth1(self.consumer_key, self.consumer_secret, callback_uri=callback_url)
        r = requests.post(request_token_url, auth=auth)
        r.raise_for_status()

        request_token = dict(urlparse.parse_qsl(r.text))
        return request_token

    def get_authorize_url(self, request_token):
        return "{0}?oauth_token={1}".format(authorize_url, request_token["oauth_token"])

    def get_access_token(self, request_token, oauth_verifier):
        auth = OAuth1(self.consumer_key, self.consumer_secret, request_token["oauth_token"], request_token["oauth_token_secret"], verifier=oauth_verifier)
        r = requests.post(access_token_url, auth=auth)
        r.raise_for_status()

        access_token = dict(urlparse.parse_qsl(r.text))
        return access_token

    def get_pay_genres(self, lang=None):
        endpoint = API_ROOT + "genre/pay.json"

        data = None
        if lang:
            data = {"lang": lang}
        r = requests.post(endpoint, data=data)
        r.raise_for_status()
        return r.json()["genres"]

    def get_income_categories(self, lang=None):
        endpoint = API_ROOT + "category/income.json"

        data = None
        if lang:
            data = {"lang": lang}
        r = requests.post(endpoint, data=data)
        r.raise_for_status()
        return r.json()["categories"]

    def get_pay_categories(self, lang=None):
        endpoint = API_ROOT + "category/pay.json"

        data = None
        if lang:
            data = {"lang": lang}
        r = requests.post(endpoint, data=data)
        r.raise_for_status()
        return r.json()["categories"]

    def get_user_info(self):
        endpoint = API_ROOT + "user/verify_credentials.json"

        auth = OAuth1(self.consumer_key, self.consumer_secret, self.access_token_key, self.access_token_secret)
        r = requests.post(endpoint, auth=auth)
        r.raise_for_status()
        return r.json()["user"]

    def get_currencies(self):
        endpoint = API_ROOT + "currency/index.json"

        r = requests.post(endpoint)
        r.raise_for_status()

        return r.json()["currencies"]

    def get_currency_sign(self, currency_code):
        currencies = self.get_currencies()
        for d in currencies:
            if d["currency_code"] == currency_code:
                return d["unit"]
        raise RuntimeError("Invalid currency code")

    def create_pay(self, **params):
        endpoint = API_ROOT + "pay/create.json"

        params = {
            "category_id": params["pay_genre"][:3],
            "genre_id": params["pay_genre"],
            "price": unicode(params["price"]),
            "date": params["date"].strftime("%Y-%m-%d") if params["date"] else "",
            "comment": params["comment"],
        }

        auth = OAuth1(self.consumer_key, self.consumer_secret, self.access_token_key, self.access_token_secret)
        r = requests.post(endpoint, data=params, auth=auth)
        r.raise_for_status()

        return r.json()

    def create_income(self, **params):
        endpoint = API_ROOT + "income/create.json"

        params = {
            "category_id": params["income_category"],
            "price": unicode(params["price"]),
            "date": params["date"].strftime("%Y-%m-%d") if params["date"] else "",
            "comment": params["comment"],
        }

        auth = OAuth1(self.consumer_key, self.consumer_secret, self.access_token_key, self.access_token_secret)
        r = requests.post(endpoint, data=params, auth=auth)
        r.raise_for_status()

        return r.json()

    def get_money_records(self):
        endpoint = API_ROOT + "money/index.json"

        auth = OAuth1(self.consumer_key, self.consumer_secret, self.access_token_key, self.access_token_secret)
        r = requests.post(endpoint, auth=auth)
        r.raise_for_status()

        return r.json()["money"]
