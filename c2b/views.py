from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from c2b.models import C2bPayment
from django.http import JsonResponse
from c2b.logic import SetCallback
import pprint
import json


"""" A register_url is a view used for registering the callback urls """

def register_url(request):
    pay = SetCallback()
    access_token = pay.get_token()
    response = pay.register_url(access_token)
    return HttpResponse("<h3>Registering Urls was a <u>" + response['ResponseDescription'] + "</u></h3>")


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
    print('-------------- confirmation ------------------')
    mpesa_body =request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)
    pprint.pprint(mpesa_payment)

    payment = C2bPayment(
        first_name=mpesa_payment['FirstName'],
        last_name=mpesa_payment['LastName'],
        middle_name=mpesa_payment['MiddleName'],
        description=mpesa_payment['TransID'],
        phone_number=mpesa_payment['MSISDN'],
        amount=mpesa_payment['TransAmount'],
        reference=mpesa_payment['BillRefNumber'],
        organization_balance=mpesa_payment['OrgAccountBalance'],
        type=mpesa_payment['TransactionType'],
    )
    payment.save()


    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))

""" TransactionsListView lists all transactions by fetching from the database and displaying in template """

class TransactionsListView(ListView):
    model = C2bPayment
    template_name = 'transactions.html'