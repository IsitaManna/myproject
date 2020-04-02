from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from django.forms.models import model_to_dict

from recommendationEngine.models import UserResponse, Question, Answer


class QuestionResponseView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        question_list = []
        user_responses = UserResponse.objects.filter(user=request.user)
        
        for question in Question.objects.all().prefetch_related('question_response'):
            q_dict = model_to_dict(question)
            a_dict = list(question.question_response.all().values())
            if user_responses:
                u_dict = {
                    "answer_id": user_responses.filter(question=question)[0].__dict__['answer_id']
                }

            else:
                u_dict = {"answer_id": 0}
            question_list.append(
                {
                    "Question": q_dict,
                    "Answer": a_dict,
                    "User_Response": u_dict
                }
            )
        
        return Response(data=question_list, status=200) 