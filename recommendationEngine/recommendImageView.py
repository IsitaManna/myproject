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
from .custom_schema import recommend_images_based_on_input
import pandas as pd
import numpy as np
import math
import time
import json 
from scipy.spatial import distance
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

def index(request):
    return HttpResponse("Hello, world. You're at the recommendationEngine index.")

def get_customer_response_data():
    all_cust_resps = UserResponse.objects.all()
    custData = []
    col_ids = []
    for item in all_cust_resps:
        customerRespObj = UserResponse.objects.filter(id=item.id)
        data = list(customerRespObj.values())
        custData.append(data)
    for i in custData:
        qid = i[0]['question_id']
        col_ids.append(qid)
    custidList = []
    for cust in custData:
        custid = cust[0]['user_id']
        custidList.append(custid)
    column_ids = np.unique(np.array(col_ids))
    cust_ids = np.unique(np.array(custidList))
    respData = []
    for customer in cust_ids:
        customerDict = {}
        custEmail = User.objects.get(id = customer).username
        customerDict["Email Address"] = custEmail
        # custRespObj = UserResponse.objects.filter(user_id=customer)
        dataList = UserResponse.objects.filter(user_id=customer).values()
        timeList = []
        for t in dataList:
            timeList.append(t['created_at'])
        customerDict["Timestamp"] = max(timeList)
        for col in column_ids:
            question = Question.objects.get(id=col).question
            responseIDbycust = UserResponse.objects.get(user_id=customer,question_id=col).answer_id
            respByCust = Answer.objects.get(id=responseIDbycust).answer
            customerDict[question] = respByCust
        respData.append(customerDict)
    df = pd.DataFrame(respData)
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
    dummies = pd.get_dummies(df[cat_cols],drop_first=False)
    # print('Dummies ', dummies)
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
    
@csrf_exempt
@api_view(['POST'])
@schema(recommend_images_based_on_input)
def recommendImagesBasedOnInputTest(request):
    # ocrimages = pd.read_csv("/home/tebackup/Workspace/Laiout/ocrimages.csv")
    floorTags=["balcony/ porch","bath","bedroom","bonus","closet","deck/outdoor space","den","dining room",
           "door","entry","firepit/fireplace","garage","hot tub","kitchen/living room","kitchen","laundry",
           "living room","mudroom","office","pantry","stair","storage","sunroom","utility","WIC","window",
           "living/ dining","kitchen/dining","hall","linen","Misc/cinema"]
    customer = request.data['CustID']
    dataList = UserResponse.objects.filter(user_id=customer).values()
    # print(dataList)
    custDict = {}
    for tag in floorTags:
        if (tag == "closet") or (tag == "dining room") or (tag == "kitchen") or (tag == "living room"):
            custDict[tag] = 1
        else:
            custDict[tag] = 0
    for data in dataList:
        if data['question_id'] == 4:
            custDict["bedroom"] = int(Answer.objects.get(id=data["answer_id"]).answer)
        elif data['question_id'] == 5:
            custDict["bath"] = int(Answer.objects.get(id=data["answer_id"]).answer)
        elif data['question_id'] == 7:
            custDict["living room"] = 1
            custDict['den'] = 1
        elif data['question_id'] == 9:
            ans = Answer.objects.get(id=data["answer_id"]).answer
            if ans.lower() == "yes":
                custDict["firepit/fireplace"] = 1
        elif data['question_id'] == 10:
            ans = Answer.objects.get(id=data["answer_id"]).answer
            if ans.lower() == "yes":
                custDict["bonus"] = 1
        elif data['question_id'] == 11:
            ans = Answer.objects.get(id=data["answer_id"]).answer
            if ans.lower() == "yes":
                custDict["office"] = 1
        elif data['question_id'] == 8:
            ans = Answer.objects.get(id=data["answer_id"]).answer
            if ans == "Mud Room":
                custDict['mudroom'] = 1
            elif ans == "Small Laundry Area":
                custDict["laundry"] = 1
    # print(np.array(custDict.values()))
    custvect = list(custDict.values())
    # print(custDict.keys())
    imglist = []
    imgdistList = []
    new_li = []
    ocrimages = OCRImage.objects.all()
    for img in ocrimages:
        # # imgdist = {}
        # imglist.append(img)
        # imgdict = eval(ocrimages[ocrimages['image_name']==img]['tag_vector'].iloc[0])
        # print('\nImage Dict- ',imgdict)
        imgdict = json.loads(img.data_dict)
        print(imgdict)
        imgvect = list(imgdict.values())
        print('\n\n Image vect',imgvect)
        # print(imgdict.keys())
        dst = distance.euclidean(custvect, imgvect)
        # imgdist['dist'] = dst
        print('distance- ', dst)
        imgdistList.append(dst)
        new_li.append({"img":str(img.image_path),"dist":dst})
    # recom_img_index = imgdistList.index(min(imgdistList))
    print('index- ',new_li)
    img_name = imglist[recom_img_index]
    print(img_name, "index at ",recom_img_index, "eucld dist: ",min(imgdistList))
    # return JsonResponse(custDict,safe=False)
    return JsonResponse({"hell":"ohh"},safe=False)


@csrf_exempt
@api_view(['GET'])
@schema(recommend_images_based_on_input)
def recommendImagesBasedOnInput(request):
    di = [
        {
            "id":1,
            "image": "media/floor_plans/142.jpg",
            "dist": 0.021
        },
        {
            "id":2,
            "image": "media/floor_plans/142.jpg",
            "dist": 0.023
        },

    ]
    return JsonResponse(di,safe=False)