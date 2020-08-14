import requests
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from django.forms.models import model_to_dict
from django.conf import settings
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from recommendationEngine.models import UserResponse, StyleImage, UserStyle, OCRImage
from recommendationEngine.Utils.gan_postprocess import *

class OuterShapeStyleView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_response = UserResponse.objects.get(user=request.user, question_id=4)
        if user_response.answer.answer == '1':
            child_li = StyleImage.objects.filter(bedroom=1)
        elif user_response.answer.answer == '2':
            child_li = StyleImage.objects.filter(bedroom=2)
        elif user_response.answer.answer == '3':
            child_li = StyleImage.objects.filter(bedroom=3)
        elif user_response.answer.answer == '4':
            child_li = StyleImage.objects.filter(bedroom=4)
        response_li = []
        for child in child_li:
            di = {
                "image_path":child.image_path.name,
                "id": child.id
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
        if StyleImage.objects.get(id=request.data['id']).parent_id:
            UserStyle.objects.update_or_create(
                    user=request.user,
                    defaults={'style_id': request.data['id']}
                )
            image_pth = UserStyle.objects.get(
                user=request.user
            ).style.image_path.path

            length = UserStyle.objects.get(
                user=request.user
            ).style.length

            width = UserStyle.objects.get(
                user=request.user
            ).style.width

            bedrooms = UserStyle.objects.get(
                user=request.user
            ).style.bedroom

            print("length,width,#bedrooms: ",length,width,bedrooms)
            files = {'file': open(image_pth, 'rb')} 
            req = requests.post(settings.GAN_HOST+'/input',files=files)
            print('#'*20)
            # x,y=get_bedroom_pos(image_pth)
            get_image = requests.get(settings.GAN_HOST+'/output/'+req.json()['image_path'],stream=True).raw
            image = np.asarray(bytearray(get_image.read()), dtype="uint8")
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            # plan,dim_list=convert_result(image)
            color_tag = pd.DataFrame(settings.PLAN_COLOR_DICT)
            plan,dim_list = gan_convert(image, color_tag,length,width,bedrooms)
            plan=Image.fromarray(plan)
            buffer = BytesIO()
            plan.save(fp=buffer, format='png')
            print('DONE')
            if not OCRImage.objects.filter(user=request.user).exists():
                ocr_img = OCRImage(data_dict=None, dim_dict=dim_list, user=request.user)
                ocr_img.image_path.save(name='GAN_image.png',content=ContentFile(buffer.getvalue()))
            else:
                print('not')
                ocr_img = OCRImage.objects.get(user=request.user)
                ocr_img.dim_dict=dim_list
                ocr_img.image_path.save(name='GAN_image.png',content=ContentFile(buffer.getvalue()))

        else:
            return Response(data={"message":"id has no parent","status":400}, status=400)
        
        return Response(data={"message":"Success","dimesion":dim_list,"status":201}, status=201)