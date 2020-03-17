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
from .custom_schema import create_customer_schema,fetch_customer_schema,fetch_login_customer_schema

@csrf_exempt
@api_view(['POST'])
@schema(create_customer_schema)
def registerCustomer(request):
    email = request.data['email'].strip()
    fName = request.data['fName']
    lName = request.data['lName']
    password = request.data['password']
    contactNo = request.data['contactNo']
    city = request.data['city']
    country = request.data['country']
    createdDate = time.strftime('%Y-%m-%d %H:%M:%S')
    checkExistingCustomer = Customer.objects.filter(email = email).exists()
    if(checkExistingCustomer == True):
        message = "Customer already exists"
        status = 409
    else:
        newCustomerObj = Customer(email = email, fName = fName, lName= lName, password = password, contactNo = contactNo, city = city, country = country, createdDate = createdDate)
        newCustomerObj.save()
        message = "User successfully registered"
        status = 200
    response = {"status":status,"message":message}
    return Response(response)

@csrf_exempt
@api_view(['POST'])
def fetchAllCustomers(request):
    custData = []
    all_customers = Customer.objects.all()
    for cust in all_customers:
        customerObj = Customer.objects.filter(email = cust.email)
        data = list(customerObj.values())
        custData.append(data)

    return JsonResponse(custData,safe=False)

@csrf_exempt
@api_view(['POST'])
@schema(fetch_customer_schema)
def fetchCustomerById(request):
    email = request.data['email']
    customerObj = Customer.objects.filter(email = email)
    data = list(customerObj.values())
    return JsonResponse(data,safe=False)


@csrf_exempt
@api_view(['POST'])
@schema(fetch_login_customer_schema)
def loginCustomer(request):
    email = request.data['email']
    password = request.data['password']
    checkExistingCustomer = Customer.objects.filter(email = email).exists()
    if checkExistingCustomer == True:
        customerObj = Customer.objects.get(email = email)

        if customerObj.password == password:
            status = 200
            message = "Login Successful!"
        else:
            status = 404
            message = "Kindly check your credentials and then try logging in!"
    else:
        status = 404
        message = "Customer email does not exist."
    response = {"status" : status,"message" : message}
    return Response(response)
