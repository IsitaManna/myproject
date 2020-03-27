from django.shortcuts import render
from .models import *
from django.http import HttpResponse, HttpRequest, JsonResponse
from rest_framework.views import APIView, Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes, schema, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import json
import time
import configparser, uuid
from .custom_schema import create_customer_response_schema


@csrf_exempt
@api_view(['POST'])
@schema(create_customer_response_schema)
def create_customer_response(request):
    print(request.data)
    email = request.data['email']
    questionID = request.data['questionID']
    responseID = request.data['responseID']
    checkExistingCustomer = Customer.objects.filter(email=email).exists()
    if checkExistingCustomer == True:
        custID = Customer.objects.get(email=email).custID
        checkExistingQuestion = Question.objects.filter(questionID=questionID).exists()
        checkExistingResponse = Response.objects.filter(responseID=responseID).exists()
        if (checkExistingQuestion == True) and (checkExistingResponse == True):
            createdDate = time.strftime('%Y-%m-%d %H:%M:%S')
            newCustRespObj = UserResponse(custID=Customer.objects.get(email=email),questionID=Question.objects.get(questionID=questionID),responseID=Response.objects.get(responseID=responseID),timestamp=createdDate)
            newCustRespObj.save()
            status = 200
            message = "Customer's response is recorded successfully"
    else:
        status = 404
        message = "Customer is not registered with us!"
    response = {"status":status,"message":message}
    return Response(response)
    