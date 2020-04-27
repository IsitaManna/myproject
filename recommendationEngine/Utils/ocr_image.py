import json
import pyocr
import pyocr.builders
from PIL import Image
import requests
import base64
import pandas as pd
import glob
from django.core.files import File
from djang.conf import settings
from recommendationEngine.models import OCRImage


def ocr_extract_from_images():
    floorTags=["balcony/ porch","bath","bedroom","bonus","closet","deck/outdoor space","den","dining room",
           "door","entry","firepit/fireplace","garage","hot tub","kitchen/living room","kitchen","laundry",
           "living room","mudroom","office","pantry","stair","storage","sunroom","utility","WIC","window",
           "living/ dining","kitchen/dining","hall","linen","Misc/cinema"]
    
    rootdir = settings.OCR_IMAGE_DIR
    
    imgLists = glob.glob(rootdir+"*.jpg")

    for img in imgLists:

        imgname = img.split('.')[0].split('/')[-1]
        print("starting with ",img)

        
        with open(img, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            encoded_string = encoded_string.decode("utf-8")
            string1="data:image/jpg;base64,"+encoded_string

            parameters = {"language":"eng",
                            "isOverlayRequired":"false",
                            'base64image': string1,
                            "iscreatesearchablepdf":"true"}
            headers= {"apiKey":"49d0787feb88957"}
            response = requests.post("https://api.ocr.space/parse/image",data=parameters,headers=headers)
            try:
                tags_api = response.json()['ParsedResults'][0]['ParsedText'].split('\n')
            except (KeyError, IndexError):
                continue
            
            tags_API = []
            for item in tags_api:
                if len(item)>=3:
                    if item.strip() != '':
                        if '\r' in item:
                            tags_API.append(item[:-1])
                        else:
                            tags_API.append(item)

            dictAPI = {}
            tagdict = {}
            dictAPI ['image_name'] = imgname
            for i in floorTags:
                count1 = 0
                for item in tags_API:
                    if len(item)>=len(i):
                        if i.upper() in item:

                            count1 += 1
                    else:
                        if item in i.upper():

                            count1 += 1
                tagdict[i]=count1

            dictAPI['tag_vector'] = tagdict
            print('Data ',dictAPI)
            ocr_image = OCRImage(data_dict=json.dumps(dictAPI['tag_vector']))
            ocr_image.image_path.save(img.split('/')[-1], File(image_file))
            ocr_image.save()
