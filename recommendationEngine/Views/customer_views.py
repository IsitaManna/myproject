import json

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from recommendationEngine.models import User, UserResponse
from recommendationEngine.Utils.vectorize import get_vectors


class CustomerSignupView(APIView):

    def post(self, request):
        email = request.data['email'].strip()
        fName = request.data['fName']
        lName = request.data['lName']
        password = request.data['password']
        contactNo = request.data['contactNo']
        city = request.data['city']
        country = request.data['country']

        if User.objects.filter(username=email).exists():

            response = {"message":"Customer already exists", "status":409}
            status = 409
        else:
            user = User(
                username=email,
                first_name=fName,
                last_name=lName,
                contact_no=contactNo,
                city=city,
                country=country
            )
            user.set_password(password)
            user.save()
            tk = Token.objects.create(user=user)
            response = {
                "message": "User successfully registered",
                "username": user.username,
                "user_id": user.id,
                "token": f'Token {tk.key}',
                "status": 201
            }

            status = 201

        return Response(data=response, status=status)




class CustomerLoginView(APIView):

    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        if User.objects.filter(username=email).exists():
            user = User.objects.get(username=email)

            if user.check_password(password):
                response = {
                    "message": "Login Successful!",
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "user_id": user.id,
                    "token": f'Token {user.auth_token}',
                    'status': 200
                }
                return Response(data=response,status=200)

                
            else:
                status = 403
                message = "Kindly check your credentials and then try logging in!"
        else:
            status = 404
            message = "User email does not exist."
        response = {"status" : status,"message" : message}
        return Response(data=response)


class CustomerResponseView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request.data['answers'])
        UserResponse.objects.filter(user_id=request.user.id).filter(question_id=16).delete()
        for i in request.data['answers']:
            if i['QuesID']==16:
                for j in range(0,len(i['ResponseID'])):
                    resp=UserResponse.objects.filter(user_id=request.user.id).filter(question_id=16).values_list('answer_id', flat=True)
                    responseli=[]
                    for item in resp:
                        responseli.append(item)
                    if int(i['ResponseID'][j]) not in responseli:
                        userrespobj=UserResponse(user_id=request.user.id,question_id=i['QuesID'],answer_id=int(i['ResponseID'][j]))
                        userrespobj.save()
                    
            else:
                UserResponse.objects.update_or_create(
                    question_id=i['QuesID'],
                    user_id=request.user.id,
                    defaults={'answer_id': i['ResponseID']}
                )
        user_response_list = list(UserResponse.objects.filter(
            user_id=request.user.id
        ).values_list('answer_id', flat=True))
        
        vec = get_vectors(user_response_list)

        v_dict = {"Vector": vec}

        request.user.vector = json.dumps(v_dict)
        request.user.save()

        return Response(data={"message":"Submisson Successful", 'status':201}, status=201)
