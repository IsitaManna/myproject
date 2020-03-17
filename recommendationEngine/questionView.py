from django.shortcuts import render
from .models import Questions
from django.http import HttpResponse, HttpRequest, JsonResponse
from rest_framework.views import APIView, Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes, schema, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import json
import time
import configparser, uuid
from .custom_schema import create_question_schema, update_question_schema, delete_question_schema

@csrf_exempt
@api_view(['POST'])
@schema(create_question_schema)
def insertQuestion(request):
    question = request.data['question']
    checkExistingQuestion = Questions.objects.filter(Question = question).exists()
    if(checkExistingQuestion == True):
        message = "Question already exists"
        status = 409
    else:
        newQuestionObj = Questions(Question = question)
        newQuestionObj.save()
        message = "Question successfully inserted"
        status = 200
    response = {"status":status,"message":message}
    return Response(response)

@csrf_exempt
@api_view(['POST'])
def fetchAllQuestions(request):
    questionData = []
    all_questions = Questions.objects.all()
    for question in all_questions:
        questionObj = Questions.objects.filter(Question = question.Question)
        data = list(questionObj.values())
        questionData.append(data)
    return JsonResponse(questionData,safe=False)

@csrf_exempt
@api_view(['POST'])
@schema(update_question_schema)
def updateQuestion(request):
    id = request.data['id']
    question = request.data['question']
    Questions.objects.filter(id = id).update(Question = question)
    message = "Question successfully updated"
    status = 200
    response = {"status":status,"message":message}
    return Response(response)

@csrf_exempt
@api_view(['POST'])
@schema(delete_question_schema)
def deleteQuestion(request):
    id = request.data['id']
    Questions.objects.filter(id = id).delete()
    message = "Question successfully deleted"
    status = 200
    response = {"status":status,"message":message}
    return Response(response)