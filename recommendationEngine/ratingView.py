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
from .custom_schema import create_customer_schema, fetch_customer_schema, create_rating_schema, update_rating_schema


@csrf_exempt
@api_view(['POST'])
@schema(create_rating_schema)
def insertImageRating(request):
    email = request.data['email']
    imageID = request.data['imageID']
    rating = request.data['rating']
    checkExistingCustomer = User.objects.filter(username=email).exists()
    if(checkExistingCustomer == True):
        newDataObj = Rating(user=User.objects.get(username=email),imageID=imageID,rating=rating)
        newDataObj.save()
        message = "Data successfully entered"
        status = 200
    else:
        message = "No such user in Customer"
        status = 309
    response = {"status":status,"message":message}
    return Response(response)

@csrf_exempt
@api_view(['POST'])
@schema(fetch_customer_schema)
def fetchImageRatingByEmail(request):
    email = request.data['email']
    checkExisting = Rating.objects.filter(email = email).exists()
    if(checkExisting == True):
        ratingObj = Rating.objects.filter(email = email)
        data = list(ratingObj.values())
        return JsonResponse(data,safe=False)
    else:
        message = "User has not rated anything"
        status = 309
        response = {"status":status,"message":message}
        return Response(response)   

@csrf_exempt
@api_view(['POST'])
@schema(update_rating_schema)
def updateImageRating(request):
    email = request.data['email']
    imageID = request.data['imageID']
    rating = request.data['rating']
    checkExistingCustomer = Customer.objects.filter(email=email).exists()
    if(checkExistingCustomer==True):
        checkExistingRatings = Rating.objects.filter(email = Customer.objects.get(email = email), imageID = imageID).exists()
        if(checkExistingCustomer == True and checkExistingRatings == True):
            Rating.objects.filter(email = Customer.objects.get(email = email), imageID = imageID).update(rating = rating)
            message = "Data successfully updated"
            status = 200
        else:
            message = "Data does not exist"
            status = 309
    else:
        message = "Data does not exist"
        status = 309
    response = {"status":status,"message":message}
    return Response(response)