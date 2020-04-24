import pyocr
import pyocr.builders
from PIL import Image
import requests
import base64
import pandas as pd
import glob


def ocr_extract_from_images():
    floorTags=["balcony/ porch","bath","bedroom","bonus","closet","deck/outdoor space","den","dining room",
           "door","entry","firepit/fireplace","garage","hot tub","kitchen/living room","kitchen","laundry",
           "living room","mudroom","office","pantry","stair","storage","sunroom","utility","WIC","window",
           "living/ dining","kitchen/dining","hall","linen","Misc/cinema"]
    rootdir = "/home/sancharig/Documents/Biloba/GAN Model/images_onedrive/done/"
    # basedir = "/home/sancharig/Documents/Biloba/GAN Model/updated house/"
    imgLists = glob.glob(rootdir+"*.jpg")
    imgtagslist = []
    for img in imgLists:
        imgname = img.split('.')[0].split('/')[-1]
        print("starting with",imgname)
    #     wordCoordList = get_ocr_tags(img)

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
        tags_api = response.json()['ParsedResults'][0]['ParsedText'].split('\n')
        tags_API = []
        for item in tags_api:
            if len(item)>=3:
                if item.strip() != '':
                    if '\r' in item:
                        tags_API.append(item[:-1])
                    else:
                        tags_API.append(item)
    #     print(tags_API)
    #     print("__________________")
        dictAPI = {}
        tagdict = {}
        dictAPI ['image_name'] = imgname
        for i in floorTags:
            count1 = 0
            for item in tags_API:
                if len(item)>=len(i):
                    if i.upper() in item:
    #                     print(item)
                        count1 += 1
                else:
                    if item in i.upper():
    #                     print(item)
                        count1 += 1
            tagdict[i]=count1
        dictAPI['tag_vector'] = tagdict
        print(dictAPI) 
        imgtagslist.append(dictAPI)
    ocrimages = pd.DataFrame(imgtagslist)
    ocrimages.to_csv("ocrimages.csv")