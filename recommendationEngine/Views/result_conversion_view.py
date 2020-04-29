import json

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
import matplotlib.pyplot as plt
from recommendationEngine.models import ColoredTextTestImage
from recommendationEngine.Utils.convert_img import *
import glob
from django.conf import settings
from django.core.files import File
import io
from django.core.files.images import ImageFile

class ResultConversionView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        rootdir = settings.GAN_TEST_IMAGE_DIR
        imgLists = glob.glob(rootdir+"*.png")
        for img in imgLists:
            imgname = img.split('.')[0].split('/')[-1]
            if 'fake' in imgname:
                colored_house,textcoordlist = convert_test_img(imgname,rootdir)
                img_dict = {}
                for item in textcoordlist:
                    room = item['text'].iloc[0]
                    img_dict[room] = item['area']
                # print(imgname, img_dict)
                im = Image.fromarray(colored_house)
                figure = io.BytesIO()
                plt.imshow(im)
                plt.savefig(figure, format="png")
                content_file = ImageFile(figure)
                col_text_testimg = ColoredTextTestImage(data_dict=img_dict)
                col_text_testimg.image_path.save(imgname,  content_file)
                col_text_testimg.save()
                # print(imgname +"saved in table")
        return Response(data={"Images successfully saved in the table!"}, status=200)

    def get(self, request):
        floor_area = request.data['floor_area']
        img_path = request.data['img_path']
        img_dims = ColoredTextTestImage.objects.filter(image_path=img_path).all()
        data = list(img_dims.values())
        data_dict = eval(data[0]['data_dict'])
        tot_area = sum(data_dict.values())
        dimen_dict = {}
        for item in data_dict:
            if item!='stair':
                dimen_dict[item] = round((data_dict[item]/tot_area)*floor_area,2)
        return Response(dimen_dict)

