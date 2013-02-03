# coding: utf-8
import os
from zaimapi import Zaim


consumer_key = unicode(os.environ.get("ZAIM_CONSUMER_KEY", ""))
consumer_secret = unicode(os.environ.get("ZAIM_CONSUMER_SECRET", ""))
access_token_key = unicode(os.environ.get("ZAIM_ACCESS_TOKEN_KEY", ""))
access_token_secret = unicode(os.environ.get("ZAIM_ACCESS_TOKEN_SECRET", ""))


def main():
    assert consumer_key, 'Please set "ZAIM_CONSUMER_KEY".'
    assert consumer_secret, 'Please set "ZAIM_CONSUMER_SECRET".'
    assert access_token_key, 'Please set "ZAIM_ACCESS_TOKEN_KEY".'
    assert access_token_secret, 'Please set "ZAIM_ACCESS_TOKEN_SECRET".'

    zaim = Zaim(consumer_key, consumer_secret, access_token_key, access_token_secret)
    print zaim.get_pay_genres("ja")
    print zaim.get_income_categories("ja")
    print zaim.get_pay_categories("ja")
    print zaim.get_user_info()
    print zaim.get_currencies()
    print zaim.get_currency_sign("JPY")
    print zaim.get_money_records()


if __name__ == '__main__':
    main()