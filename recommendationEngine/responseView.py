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
from .custom_schema import create_response_schema,fetch_response_schema
from .questionView import *

@csrf_exempt
@api_view(['POST'])
@schema(create_response_schema)
def insertResponse(request):
    questionID = request.data['QuestionID']
    answer = request.data['answer']
    # newResponseObj = Responses(questionID = Questions.objects.get(questionID = QuestionID), response =  answer)
    if len(answer) == 1:
        newResponseObj = Responses(questionID = Questions.objects.get(questionID = questionID), response=  answer)
        newResponseObj.save()
    else:
        for ans in answer:
            newResponseObj = Responses(questionID = Questions.objects.get(questionID = questionID), response=  ans)
            newResponseObj.save()
    status = 400
    message = "Response inserted successfully!"
    response = {"status":status,"message":message}
    return Response(response)

@csrf_exempt
@api_view(['GET'])
def fetchAllResponses(request):
    respData = []
    all_response = Responses.objects.all()
    for resp in all_response:
        responseObj = Responses.objects.filter(questionID = resp.questionID)
        data = list(responseObj.values())
        respData.append(data)

    return JsonResponse(respData,safe=False)

@csrf_exempt
@api_view(['GET'])
@schema(fetch_response_schema)
def fetchResponsesByID(request):
    questionID = request.data['questionID']
    responseObj = Responses.objects.filter(questionID = questionID)
    data = list(responseObj.values())
    return JsonResponse(data,safe=False)

@csrf_exempt
@api_view(['GET'])
def fetchQuestionResponses(request):
    quesRespData = []
    questionData = []
    all_questions = Questions.objects.all()
    for question in all_questions:
        questionObj = Questions.objects.filter(Question = question.Question)
        data = list(questionObj.values())
        questionData.append(data)
    for ques in questionData:
        quesRespDict = {}
        quesDict = {}
        questionID = ques[0]['questionID']
        quesDict['QuesID'] = questionID
        quesDict['question'] = ques[0]['Question']
        responseObj = Responses.objects.filter(questionID = questionID)
        print(responseObj)
        respData = list(responseObj.values())
        responses = []
        for resp in respData:
            respDict = {}
            respDict['ResponseID'] = resp['responseID']
            respDict['response'] = resp['response']
            responses.append(respDict)
        quesRespDict['Question'] = quesDict
        quesRespDict['answer'] = responses
        quesRespData.append(quesRespDict)
    return Response(quesRespData)
