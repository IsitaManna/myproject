from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from recommendationEngine.serializers import UserSerializer, GroupSerializer
from django.http import HttpResponse
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, schema

import pandas as pd
import numpy as np
import math
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

def index(request):
    return HttpResponse("Hello, world. You're at the recommendationEngine index.")
  

def dataPreprocess():
    df = pd.read_excel("/home/sancharig/Documents/Biloba/Sample Survey - Property buying questionnaire (Responses).xlsx")
    df["Email Address"] = df["Email Address"].apply(lambda x:x.split('@')[0])
    cat_cols = ['Which square foot apartment is appropriate for you?',
           'What type of residential property do you prefer?',
           'Do you prefer a terrace garden (if you opt for a terrace house)?',
           'What type should the building be?', 'How many bedrooms do you prefer?',
            'How many bathrooms are preferred?', 'How many balcony do you want?',
           'Where do you prefer your balcony?',
           'Do you want a walkin closet in your bedroom?',
           'Would you prefer car parking along with your property?',
           'Do you need a separate dining room?',
           'Is hall cum kitchen good for you?', 'Do you have pets at home?',
           'How often do you have guests?', 'How often do you party?']
    dummies = pd.get_dummies(df[cat_cols],drop_first=True)
    df = pd.concat([df,dummies],axis = 1)
    df = df.drop(cat_cols,axis = 1)
    cols = ['Which square foot apartment is appropriate for you?_500 - 700 sqft', 'Which square foot apartment is appropriate for you?_700 - 1000 sqft', 'What type of residential property do you prefer?_Condominium', 'What type of residential property do you prefer?_Serviced apartment', 'What type of residential property do you prefer?_Terrace house', 'Do you prefer a terrace garden (if you opt for a terrace house)?_No', 'Do you prefer a terrace garden (if you opt for a terrace house)?_Yes', 'What type should the building be?_Landed', 'How many bedrooms do you prefer?_3 bedroom', 'How many bedrooms do you prefer?_more', 'How many balcony do you want?_2', 'How many balcony do you want?_3', 'How many balcony do you want?_more', 'Where do you prefer your balcony?_With bedroom', 'Where do you prefer your balcony?_With dining room', 'Where do you prefer your balcony?_With living room', 'Do you want a walkin closet in your bedroom?_No',
       'Do you want a walkin closet in your bedroom?_Yes', 'Would you prefer car parking along with your property?_No', 'Would you prefer car parking along with your property?_Yes', 'Do you need a separate dining room?_No', 'Do you need a separate dining room?_Yes', 'Is hall cum kitchen good for you?_No', 'Is hall cum kitchen good for you?_Yes', 'Do you have pets at home?_No', 'Do you have pets at home?_Yes', 'How often do you have guests?_Often', 'How often do you have guests?_Rarely', 'How often do you have guests?_Very Rarely', 'How often do you party?_Often', 'How often do you party?_Rarely', 'How often do you party?_Very Rarely']
    df1 = df[cols]
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
        dictEucld = {}
        dictEucld['User1'] = dictList[item]['User']
        print(dictEucld['User1'] )
        for i in range(0,len(dictList)):
            user2 = dictList[i]['User']
            dictEucld[user2] = np.linalg.norm(dictList[item]['Vector'] - dictList[i]['Vector'])
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
    dfRanks = df[["User1",new_user]].sort_values(by = new_user)
    dfRanks = dfRanks[~(dfRanks[new_user]==0)]
    rank = []
    for r in range(0,len(dfRanks.index)):
        rank.append(r+1)
    dfRanks["Rank"]=rank
    return dfRanks.head(5)['User1']

@csrf_exempt
@api_view(['POST'])
def recommendImagesBasedOnRating(request):
    new_user = request.data['username']
    vect = np.random.randint(2,size=32)
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
    response = {'status':404,'data':recommendedImgdf['Image'][:3]}
    return Response(response)
    