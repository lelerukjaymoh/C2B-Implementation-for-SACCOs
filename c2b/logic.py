from django.conf import settings
import requests
from requests.auth import HTTPBasicAuth
import africastalking

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
        if response.status_code == 200:
            return response.json()

    
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


class Notify:
    # Get the Africas Talking credentials
    AT_username = settings.AT_USERNAME
    AT_api_key = settings.AT_API_KEY

    def __init__(self):
        # Initialising the Africas Talking SDK
        africastalking.initialize(self.AT_username, self.AT_api_key)

        # Get the SMS service
        self.sms = africastalking.SMS

    def notify_customer(self, first_name, amount, account_no, phone_number):
        recipients = [phone_number]
        message = f"Hello {first_name}, we have received your payment of {amount} for the account {account_no}. Thanks for choosing Neno Sacco"
       
        try:
            response = self.sms.send(message, recipients)
        except Exception as e:
            print ('Encountered an error while sending: %s' % str(e))