from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from django.http import HttpResponse, HttpRequest, JsonResponse
from recommendationEngine.serializers import UserSerializer, GroupSerializer
from django.http import HttpResponse
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, schema
from .models import *

import pandas as pd
import numpy as np
import math
import time
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

def index(request):
    return HttpResponse("Hello, world. You're at the recommendationEngine index.")

def get_customer_response_data():
    all_cust_resps = CustomerResponse.objects.all()
    custData = []
    col_ids = []
    for item in all_cust_resps:
        customerRespObj = CustomerResponse.objects.filter(custRespID = item.custRespID)
        data = list(customerRespObj.values())
        custData.append(data)
    for i in custData:
        qid = i[0]['questionID_id']
        col_ids.append(qid)
    custidList = []
    for cust in custData:
        custid = cust[0]['custID_id']
        custidList.append(custid)
    column_ids = np.unique(np.array(col_ids))
    cust_ids = np.unique(np.array(custidList))
    respData = []
    for customer in cust_ids:
        customerDict = {}
        custEmail = Customer.objects.get(custID = customer).email
        customerDict["Email Address"] = custEmail
        custRespObj = CustomerResponse.objects.filter(custID = customer)
        dataList = CustomerResponse.objects.filter(custID = customer).values()
        timeList = []
        for t in dataList:
            timeList.append(t['timestamp'])
        customerDict["Timestamp"] = max(timeList)
        for col in column_ids:
            question = Questions.objects.get(questionID = col).Question
            responseIDbycust = CustomerResponse.objects.get(custID=customer,questionID=col).responseID_id
            respByCust = Responses.objects.get(responseID=responseIDbycust).response
            customerDict[question] = respByCust
        respData.append(customerDict)
    df = pd.DataFrame(respData)
    # print(df)
    return df

def dataPreprocess():
    df = get_customer_response_data()
    # df = pd.read_excel("/home/sancharig/Documents/Biloba/Sample Survey - Property buying questionnaire (Responses).xlsx")
    df["Email Address"] = df["Email Address"].apply(lambda x:x.split('@')[0])
    columns = df.columns
    cat_cols = []
    for c in columns:
        if c not in ["Email Address","Timestamp"]:
            cat_cols.append(c)
    dummies = pd.get_dummies(df[cat_cols],drop_first=True)
    df = pd.concat([df,dummies],axis = 1)
    df = df.drop(cat_cols,axis = 1)
    dcols = df.columns
    dummy_cols = []
    for c in dcols:
        if c not in ["Email Address","Timestamp"]:
            dummy_cols.append(c)
    df1 = df[dummy_cols]
    return df,df1

def getVectors():
    df,df1 = dataPreprocess()
    dictList = []
    for i in range(0,len(df.index)):
        dictUser = {}
        dictUser['User'] = df['Email Address'].iloc[i]
        dictUser['Vector'] = np.array(df1.iloc[i]).astype(int)
        dictList.append(dictUser)
    return dictList

def getSimilarityMatrix(dictList):
    eucldDistList = []
    for item in range(0,len(dictList)):
        for i in range(0,len(dictList)):
            user2 = dictList[i]['User']
            dictEucld = {}
            dictEucld['User1'] = dictList[item]['User']
            dictEucld['User2'] = user2
            dictEucld['Eucld_Dist'] = np.linalg.norm(dictList[item]['Vector'] - dictList[i]['Vector'])
            eucldDistList.append(dictEucld)
    euclDistdf = pd.DataFrame(eucldDistList)
    return euclDistdf

def getSimilarUsers(new_user,vect):
    dictUser = {}
    dictUser['User'] = new_user
    dictUser['Vector'] = vect
    list1 = getVectors()
    list1.append(dictUser)
    df = getSimilarityMatrix(list1)
    dfRanks = df[df['User1']==new_user].sort_values(by = "Eucld_Dist",ascending=False)
    dfRanks = dfRanks[~(dfRanks["Eucld_Dist"]==0)]
    rank = []
    for r in range(0,len(dfRanks.index)):
        rank.append(r+1)
    dfRanks["Rank"]=rank
    print(dfRanks)
    return dfRanks.head(5)['User1']


@csrf_exempt
@api_view(['POST'])
def recommendImagesBasedOnRating(request):
    new_user = request.data['username']
    vect = np.random.randint(2,size=33)
    ratings = pd.read_csv("/home/sancharig/Documents/Biloba/floorplan_ratings.csv")
    users = getSimilarUsers(new_user,vect)
    simUserRatings = ratings[ratings['User1'].isin(users)]
    images = simUserRatings.columns[1:]
    recommendedImages = []
    for col in images: 
        imgDict = {}
        imgDict['Image'] = col
        imgDict["RatingMean"] = simUserRatings[col].mean()
        recommendedImages.append(imgDict)
    recommendedImgdf = pd.DataFrame(recommendedImages)
    recommendedImgdf = recommendedImgdf.sort_values(by='RatingMean',ascending=False)
    response = {'status':200,'data':recommendedImgdf['Image'][:3]}
    return Response(response)
    