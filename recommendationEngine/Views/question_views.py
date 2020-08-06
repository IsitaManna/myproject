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
        print(request.user)
        user_responses = UserResponse.objects.filter(user=request.user)
        # print(user_responses.filter(question_id=16)[1].__dict__['answer_id'])
        for question in Question.objects.all():
            # print(type(question.id))
            q_dict = model_to_dict(question)
            # print(q_dict)
            if not  q_dict['image_path'].name:
                q_dict['image_path'] = None
            else:
                q_dict['image_path'] = q_dict['image_path'].name

            a_dict = list(question.question_response.all().values())
            if user_responses:
                if question.id==16:
                    # print("******question no:16********")
                    length=len(user_responses.filter(question_id=16).values_list())
                    vals=[]
                    for k in range(0,length):
                        vals.append(user_responses.filter(question_id=16)[k].__dict__['answer_id'])
                    u_dict = {
                        "answer_id": vals
                    }
                else:
                    u_dict = {
                        "answer_id": user_responses.filter(question=question)[0].__dict__['answer_id']
                    }
            else:
                u_dict = {"answer_id": 0}
            # print(u_dict)
            question_list.append(
                {
                    "Question": q_dict,
                    "Answer": a_dict,
                    "User_Response": u_dict
                }
            )
        # print(question_list)
        
        return Response(data=question_list, status=200) 