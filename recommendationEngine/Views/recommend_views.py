import json

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from recommendationEngine.models import User, UserResponse
from recommendationEngine.Utils.vectorize import get_customer_reponse_vect, get_vector_distance


class RecommendPlanView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_response = UserResponse.objects.filter(user_id=request.user.id)
        customer_vect = get_customer_reponse_vect(user_response)
        vector_dist = get_vector_distance(customer_vect)
        vector_dist.sort(key= lambda x : x['dist'], reverse=False)

        data = {
            "recommendation": vector_dist[:5]
        }
        return Response(data=data, status=200)
