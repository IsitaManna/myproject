from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from django.forms.models import model_to_dict

from recommendationEngine.models import UserResponse, StyleImage, UserStyle


class OuterShapeStyleView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_response = UserResponse.objects.get(user=request.user, question_id=4)
        if user_response.answer.answer == '1':
            child_li = StyleImage.objects.filter(bedroom=1).values_list('parent_id', flat=True)
            parents = StyleImage.objects.filter(id__in=child_li)
        elif user_response.answer.answer == '2':
            child_li = StyleImage.objects.filter(bedroom=2).values_list('parent_id', flat=True)
            parents = StyleImage.objects.filter(id__in=child_li)
        elif user_response.answer.answer == '3':
            child_li = StyleImage.objects.filter(bedroom=3).values_list('parent_id', flat=True)
            parents = StyleImage.objects.filter(id__in=child_li)
        elif user_response.answer.answer == '4':
            child_li = StyleImage.objects.filter(bedroom=4).values_list('parent_id', flat=True)
            parents = StyleImage.objects.filter(id__in=child_li)
        else:
            child_li = StyleImage.objects.filter(parent__isnull=False).values_list('parent_id', flat=True)
            parents = StyleImage.objects.filter(id__in=child_li)
        response_li = []
        for parent in parents:
            di = {
                "image_path":parent.image_path.name,
                "id": parent.id
            }
            response_li.append(di)
        

        return Response(data=response_li, status=200)

    def post(self, request):
        user_response = UserResponse.objects.get(user=request.user, question_id=4)
        if user_response.answer.answer == '1':
            children = StyleImage.objects.filter(bedroom=1, parent_id=request.data['id'])

        elif user_response.answer.answer == '2':
            children = StyleImage.objects.filter(bedroom=2, parent_id=request.data['id'])
        elif user_response.answer.answer == '3':
            children = StyleImage.objects.filter(bedroom=3, parent_id=request.data['id'])
        elif user_response.answer.answer == '4':
            children = StyleImage.objects.filter(bedroom=4, parent_id=request.data['id'])
        else:
            children = StyleImage.objects.filter(parent_id=request.data['id'])

        response_li = []
        for child in children:
            di = {
                "image_path":child.image_path.name,
                "id": child.id
            }
            response_li.append(di)
        
        return Response(data=response_li, status=200)



class BedroomStyleView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if StyleImage.objects.get(id=request.data['id']).parent:
            UserStyle.objects.update_or_create(
                    user=request.user,
                    defaults={'style_id': request.data['id']}
                )
        else:
            return Response(data={"message":"id has no parent","status":400}, status=400)
        
        return Response(data={"message":"Success","status":201}, status=201)