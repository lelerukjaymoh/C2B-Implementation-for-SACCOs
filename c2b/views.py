from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from c2b.models import C2bPayment
from django.http import JsonResponse
from c2b.logic import Pay
import pprint
import json

def home(request):
    pay = Pay()
    access_token = pay.get_token()
    response = pay.register_url(access_token)
    pprint.pprint(response)
    print('')
    r = pay.c2b_payment(access_token)
    print('********************************')
    pprint.pprint(r)
    print('')
    return render(request, 'home.html', {})

@csrf_exempt
def validation(request):
    print('--------------- validation ---------------')
    data = json.loads(request.body)
    pprint.pprint(data)
    print('')
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))

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

class TransactionsListView(ListView):
    model = C2bPayment
    template_name = 'transactions.html'