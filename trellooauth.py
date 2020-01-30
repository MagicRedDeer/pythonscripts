requestUrl = "https://trello.com/1/OAuthGetRequestToken"
accessUrl = "https://trello.com/1/OAuthGetAccessToken"
authorizeUrl = "https://trello.com/1/OAuthAuthorizeToken"


key = '05fd0465d26ae98cb514fa477dfdb78f267b0b13792d9444ac7c9d1975fb121e'
client = '09a4f53ad33237315071ec225addf4e7'

from requests_oauthlib import OAuth1, OAuth1Session
import requests

class TrelloOAuth(object):
    def __init__(self, client_key, client_secret):
        self.client_key = client_key
        self.client_secret = client_secret

    def hello(self, args1, arg2):
        """some function docs

        :args1: TODO
        :arg2: TODO
        :returns: TODO

        """
        return None
