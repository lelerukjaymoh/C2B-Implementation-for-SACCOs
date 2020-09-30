from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from c2b.models import C2bPayment
from django.http import JsonResponse
from c2b.logic import SetCallback, Notify
import json


"""" A register_url is a view used for registering the callback urls """
# NOTE: The register_url should only be used once to register the callback urls, after successfull registration the url for 
# the view should be disabled by probably deleting the url for the register_url view in urls.py.

def register_url(request):
    callback = SetCallback()
    access_token = callback.get_token()
    response = callback.register_url(access_token)
    html = "<html><body>The callback urls registration response is a : <b>%s</b> </body></html>" % str(response['ResponseDescription'])
    return HttpResponse(html)


"""" Validation endpoint that validates transactions """

@csrf_exempt
def validation(request):
    # This validation endpoint has been included incase there need to scale the app's funtionality in the future and 
    # include the validation of a transaction. As of now all transactions are accepted

    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))


"""" Confirmation endpoint that confirms transactions """

@csrf_exempt
def confirmation(request):
    mpesa_body =request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body) 

    # Get payment details from response
    first_name = mpesa_payment['FirstName']
    amount = mpesa_payment['TransAmount']
    account_no = mpesa_payment['BillRefNumber']
    phone_number = mpesa_payment['MSISDN']
    

    payment = C2bPayment(
        first_name = first_name,
        last_name = mpesa_payment['LastName'],
        middle_name = mpesa_payment['MiddleName'],
        description = mpesa_payment['TransID'],
        phone_number = phone_number,
        amount = amount,
        reference = account_no,
        organization_balance = mpesa_payment['OrgAccountBalance'],
        type = mpesa_payment['TransactionType'],
    )
    payment.save()

    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }

    # Notifying customer on successful transaction --> COMMENTED OUT SENDING NOTIFICATIONS TO CUSTOMERS
    # notify = Notify()
    # notify.notify_customer(first_name, amount, account_no, phone_number)

    return JsonResponse(dict(context))

""" TransactionsListView lists all transactions by fetching from the database and displaying in template """

class TransactionsListView(ListView):
    model = C2bPayment
    template_name = 'transactions.html'