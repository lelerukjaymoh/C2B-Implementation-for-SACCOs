from django.conf import settings
import requests
from requests.auth import HTTPBasicAuth
import pprint

class Pay:
    consumer_key = settings.CONSUMER_KEY
    consumer_secret = settings.CONSUMER_SECRET
    shortcode = settings.SHORTCODE
    base_url = settings.BASE_URL

    def get_token(self):
        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        
        r = requests.get(api_URL, auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret))

        return r.json()['access_token']

    def register_url(self, access_token):
        url_register = 'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl'
        headers = {'Authorization': 'Bearer %s' % access_token, 'content-type': 'application/json'}
        body = {
            "ShortCode": "%s" % self.shortcode,
            "ResponseType": "Completed",
            "ConfirmationURL": "%s/confirmation" % self.base_url,
            "ValidationURL": "%s/validation" % self.base_url
        }

        response = requests.post(url_register, headers=headers, json=body)
        print(url_register, headers, body)

        return response.json()

    def c2b_payment(self, access_token):
        payment_url = 'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate'
        headers = {'Authorization': 'Bearer %s' % access_token, 'content-type': 'application/json'}
        body = {
            "ShortCode": "%s" % self.shortcode,
            "CommandID": "CustomerPayBillOnline",
            "Amount": "10",
            "Msisdn": "254708374149",
            "BillRefNumber": "account"
        }

        response = requests.post(payment_url, headers=headers, json=body)
        return response.json()