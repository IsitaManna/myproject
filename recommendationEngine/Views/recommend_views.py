import json

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from recommendationEngine.models import User, UserResponse, Rating, OCRImage
from recommendationEngine.Utils.vectorize import (
    get_customer_reponse_vect,
    get_vector_distance,
    find_similar_plan,
    find_similar_user
)


class RecommendPlanView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        plans = OCRImage.objects.filter(user=request.user)
        li = []
        for i in plans:
            li.append({"img": str(i.image_path), "dist": 3.0, "id": i.id})
        data = {
            "recommendation": li
        }
        return Response(data=data, status=200)
        # user_response = UserResponse.objects.filter(user_id=request.user.id)
        # if user_response:
        #     customer_vect = get_customer_reponse_vect(user_response)
        #     vector_dist = get_vector_distance(customer_vect)
        #     vector_dist.sort(key= lambda x : x['dist'], reverse=False)

        #     data = {
        #         "recommendation": vector_dist[:5]
        #     }
        #     print(data)
        #     return Response(data=data, status=200)
        # else:
        #     return Response(data={"message":"Fill form first"}, status=400)


class RecommendationRatingView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_rating = Rating.objects.filter(user_id=request.user.id)
        if user_rating:
            rating = user_rating.values()

            data = {
                "rating": rating
            }
            return Response(data=data, status=200)
        else:
            return Response(
                data={"rating":[], "message":"No ratings present."},
                status=200
            )

    def post(self, request):
        for rating in request.data["rating"]:
            Rating.objects.update_or_create(
                image_id=rating['image_id'],
                user_id=request.user.id,
                defaults={'rating': rating['rating']}
            )
        
        user_rating = Rating.objects.filter(user=request.user.id).values()
        return Response(
            data={"rating":user_rating, "status":201},
            status=201
        )


class CollabFilteringRecommendView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sim_list = find_similar_user(request.user)
        reco = find_similar_plan(sim_list)
        reco = [
            {
                "img":r["image__image_path"],
                "dist": r["rating__avg"],
                "id": r["image_id"]
            } for r in reco
        ]
        
        return Response(
            data={"recommendation": reco},
            status=200
        )
