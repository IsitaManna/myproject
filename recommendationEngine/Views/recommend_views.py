import json
import logging

logger = logging.getLogger(__name__)

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from recommendationEngine.models import User, UserResponse, Rating, OCRImage,Answer
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
        print("User id: ",request.user.id)
        answer=UserResponse.objects.filter(user_id=request.user.id).filter(question_id=1).values_list('answer_id', flat=True)[0]
        sqftarea=Answer.objects.filter(id=answer).values_list('answer', flat=True)[0]
        print("Option Chosen:",sqftarea)
        if sqftarea=="Less than 1000 sq. ft.":
            lower_cap=int(sqftarea.split()[2])
        else:
            lower_cap=int(sqftarea.split('-')[0])
        plans = OCRImage.objects.filter(user=request.user)
        li = []
        dim_li=[]
        for i in plans:
            dim=eval(i.dim_dict)
        # {'room': '1', 'area_perc': 'living room-18.87'}
        for d in dim:
            area=round(float(d['area_perc'].split('-')[-1])/100*lower_cap,2)
            dim_li.append({'room':d['room'],'area_perc':d['area_perc'].split("-")[0]+'-'+str(area)})
        # print(dim_li)
        for i in plans:
            print(eval(i.dim_dict))
            li.append({"img": str(i.image_path),"dimension":dim_li, "dist": 3.0, "id": i.id})
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
        return Response(data=data,status=200)

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
        try:
            sim_list = find_similar_user(request.user)
            reco = find_similar_plan(sim_list)
            print(reco)
            records=[]
            for r in reco:
                dict1={}
                dict1["img"]=r["image__image_path"]
                dict1["dist"]=r["rating__avg"]
                dict1['id']=r["image_id"]
                dict1['dim_dict']=eval(OCRImage.objects.get(id=r["image_id"]).dim_dict)
                records.append(dict1)
            # reco = [
            #     {
            #         "img":r["image__image_path"],
            #         "dist": r["rating__avg"],
            #         "id": r["image_id"]
            #     } for r in reco
            # ]
            # print(type(reco))
            print(records)
            return Response(
                data={"recommendation": records},
                status=200
            )
        except Exception as e:
            return Response(
                data={"recommendation": e},
                status=403
            )
