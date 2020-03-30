from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from recommendationEngine.models import User, UserResponse
from rest_framework.response import Response
from rest_framework.authtoken.models import Token



class CustomerSignupView(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        email = request.data['email'].strip()
        fName = request.data['fName']
        lName = request.data['lName']
        password = request.data['password']
        contactNo = request.data['contactNo']
        city = request.data['city']
        country = request.data['country']
        # createdDate = time.strftime('%Y-%m-%d %H:%M:%S')
        if User.objects.filter(username=email).exists():
        # if(checkExistingCustomer == True):
            message = "Customer already exists"
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
                "token": f'Token {tk.key}'
            }
            # message = 
            status = 201
        # response = {"message":message}
        return Response(data=response, status=status)




class CustomerLoginView(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        if User.objects.filter(username=email).exists():
        # if checkExistingCustomer == True:
            user = User.objects.get(username=email)
            # 
            if user.check_password(password):
                # tk = Token.objects.create(user=user)
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
        return Response(data=response,status=status)


class CustomerResponseView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request.data)
        bulk_ins = []
        for i in request.data['answers']:
            bulk_ins.append(UserResponse(
                user_id=request.user.id,
                question_id=i["QuesID"],
                answer_id=i["ResponseID"]
            ))
        UserResponse.objects.bulk_create(bulk_ins)
        return Response(data={"message":"Submisson Successful", 'status':201}, status=201)