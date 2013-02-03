# coding: utf-8
import os
from zaimapi import Zaim


consumer_key = unicode(os.environ.get("ZAIM_CONSUMER_KEY", ""))
consumer_secret = unicode(os.environ.get("ZAIM_CONSUMER_SECRET", ""))


def main():
    assert consumer_key, 'Please set "ZAIM_CONSUMER_KEY".'
    assert consumer_secret, 'Please set "ZAIM_CONSUMER_SECRET".'

    zaim = Zaim(consumer_key, consumer_secret)
    request_token = zaim.get_request_token()
    print "REQUEST_TOKEN:", request_token
    auth_url = zaim.get_authorize_url(request_token)
    print "AUTHORIZE_URL:", auth_url
    oauth_verifier = unicode(raw_input("oauth_verifier? : "))
    print "OAUTH_VERIFIER:", oauth_verifier
    access_token = zaim.get_access_token(request_token, oauth_verifier)
    print "ACCESS_TOKEN:", access_token


if __name__ == '__main__':
    main()
