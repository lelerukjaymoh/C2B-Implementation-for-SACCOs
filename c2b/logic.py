from django.conf import settings
import requests
from requests.auth import HTTPBasicAuth
import pprint

class SetCallback:
    # Get credentials from settings
    consumer_key = settings.CONSUMER_KEY
    consumer_secret = settings.CONSUMER_SECRET
    shortcode = settings.SHORTCODE
    base_url = settings.BASE_URL


    """ 

    get_token hits the authentication endpoint with Base-64 encoding of Consumer Key + ":" + Consumer Secret and 
    returns an access token

    """

    def get_token(self):
        authentication_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials" # Endpoint
        response = requests.get(authentication_URL, auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret))
        if response.status_code == 200: # Check if it was successfull then continue
            print(response.json())
            return response.json()['access_token']



    """ 

    register_url registers the callback urls (Confirmation and Validation URLs) and sets the default action to be taken
    in case the validation URL is unreachable. 

    """
    def register_url(self, access_token):
        url_register = 'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl'
        headers = {'Authorization': 'Bearer %s' % access_token, 'content-type': 'application/json'}
        body = {
            "ShortCode": "%s" % self.shortcode,
            "ResponseType": "Completed",
            "ConfirmationURL": "%s/api/v1/c2b/confirmation" % self.base_url,
            "ValidationURL": "%s/api/v1/c2b/validation" % self.base_url
        }

        response = requests.post(url_register, headers=headers, json=body)
        pprint.pprint(response.json())
        print(url_register, headers, body)

        if response.status_code == 200:
            return response.json()
        else:
            print('Register urls response contains error')
        


    """ 

    c2b_payment_simulator is only used in Sandbox enviroment to simulate a C2B transaction by a client to a paybill. 

    """


    def c2b_payment_simulator(self, access_token):
        # payment_url is a sandbox endpoint for simulating a C2B transaction
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